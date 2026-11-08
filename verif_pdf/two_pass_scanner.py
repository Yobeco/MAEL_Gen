"""Stratégie de détection QR en deux passes pour les pages PDF."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image

from .pdf_renderer import PdfRenderer
from .qr_detector import QrDetector, ScanError
from .qr_dto import RawQr


@dataclass(frozen=True)
class PageScanResult:
    """Résultat du scan d'une page et caractéristiques du PNG retenu."""

    page_index: int
    png_path: Path
    dpi: int
    width: int
    height: int
    items: list[RawQr]
    used_fallback: bool

    @property
    def has_qr(self) -> bool:
        """Indique si au moins un élément a été détecté."""
        return bool(self.items)


class TwoPassQrScanner:
    """Scanne une page à DPI nominal, puis au DPI de secours si nécessaire."""

    def __init__(
        self,
        renderer: PdfRenderer,
        detector: QrDetector,
        dpi: int,
        fallback_dpi: int,
    ) -> None:
        """Initialise les dépendances et les résolutions des deux passes."""
        self.renderer = renderer
        self.detector = detector
        self.dpi = dpi
        self.fallback_dpi = fallback_dpi

    @staticmethod
    def _dimensions(png_path: Path) -> tuple[int, int]:
        """Lit la largeur et la hauteur du PNG en pixels."""
        with Image.open(png_path) as image:
            return image.size

    def scan_page(
        self,
        pdf_path: str | Path,
        page_index: int,
        nominal_png_path: str | Path,
        work_dir: str | Path,
        page_count: int,
        log: Callable[[str], None],
    ) -> PageScanResult:
        """Scanne la page rendue à DPI nominal, avec repli éventuel.

        Les erreurs ``ScanError`` suivent les mêmes règles que l'orchestrateur
        historique : une erreur nominale conserve directement le PNG brut ;
        une erreur en secours revient au PNG nominal.
        """
        nominal_png = Path(nominal_png_path)
        try:
            items = self.detector.scan(nominal_png)
        except ScanError as exc:
            log(
                f"[error] page {page_index + 1}: échec du scan ({exc}) "
                "— page incluse brute"
            )
            width, height = self._dimensions(nominal_png)
            return PageScanResult(
                page_index, nominal_png, self.dpi, width, height, [], False
            )

        if items:
            log(f"[info] page {page_index + 1}: {len(items)} QR détecté(s)")
            width, height = self._dimensions(nominal_png)
            return PageScanResult(
                page_index, nominal_png, self.dpi, width, height, items, False
            )

        if self.fallback_dpi <= self.dpi:
            log(f"[info] page {page_index + 1}: aucun QR détecté")
            width, height = self._dimensions(nominal_png)
            return PageScanResult(
                page_index, nominal_png, self.dpi, width, height, items, False
            )

        log(
            f"[warn] page {page_index + 1}: aucun QR à {self.dpi} DPI, "
            f"reconversion à {self.fallback_dpi} DPI"
        )
        fallback_dir = Path(work_dir) / f"dpi_{self.fallback_dpi}"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        fallback_png = self.renderer.render_page(
            Path(pdf_path).resolve(),
            page_index,
            self.fallback_dpi,
            fallback_dir,
            pad=len(str(page_count)),
        )
        try:
            fallback_items = self.detector.scan(fallback_png)
        except ScanError as exc:
            log(
                f"[error] page {page_index + 1}: échec du scan à "
                f"{self.fallback_dpi} DPI ({exc}) — page incluse à "
                f"{self.dpi} DPI"
            )
            width, height = self._dimensions(nominal_png)
            return PageScanResult(
                page_index, nominal_png, self.dpi, width, height, [], False
            )

        if fallback_items:
            log(
                f"[ok]   page {page_index + 1}: {len(fallback_items)} QR "
                f"détecté(s) à {self.fallback_dpi} DPI"
            )
            width, height = self._dimensions(fallback_png)
            return PageScanResult(
                page_index,
                Path(fallback_png),
                self.fallback_dpi,
                width,
                height,
                fallback_items,
                True,
            )

        log(
            f"[warn] page {page_index + 1}: toujours aucun QR à "
            f"{self.fallback_dpi} DPI — page incluse à {self.dpi} DPI"
        )
        width, height = self._dimensions(nominal_png)
        return PageScanResult(
            page_index, nominal_png, self.dpi, width, height, fallback_items, False
        )
