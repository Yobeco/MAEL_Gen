"""Tests rapides du scanner deux passes avec dépendances factices."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from PIL import Image

from verif_pdf.two_pass_scanner import TwoPassQrScanner
from verif_pdf.qr_detector import ScanError


class FakeRenderer:
    """Produit un PNG de repli et conserve les arguments reçus."""

    def __init__(self) -> None:
        self.calls: list[tuple[Path, int, Path]] = []

    def render_page(
        self, pdf_path: Path, page_index: int, dpi: int, output_dir: Path, pad: int = 4
    ) -> Path:
        self.calls.append((pdf_path, dpi, output_dir))
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"page_{page_index + 1:0{pad}d}.png"
        Image.new("RGB", (dpi, dpi // 2), "white").save(path)
        return path


class FakeDetector:
    """Retourne ou lève des résultats programmés dans l'ordre des scans."""

    def __init__(self, results: list[Any]) -> None:
        self.results = iter(results)
        self.paths: list[Path] = []

    def scan(self, path: Path) -> list[Any]:
        self.paths.append(Path(path))
        result = next(self.results)
        if isinstance(result, Exception):
            raise result
        return result


@pytest.fixture
def setup_case(tmp_path: Path):
    """Prépare page nominale, doubles et journal de test."""
    pdf = tmp_path / "source.pdf"
    pdf.touch()
    nominal_dir = tmp_path / "dpi_250"
    nominal_dir.mkdir()
    nominal = nominal_dir / "page_0001.png"
    Image.new("RGB", (250, 125), "white").save(nominal)
    renderer = FakeRenderer()
    logs: list[str] = []
    work_dir = tmp_path / "work"
    return pdf, nominal, renderer, logs, work_dir


def run_case(setup_case, outcomes: list[Any]):
    pdf, nominal, renderer, logs, work_dir = setup_case
    detector = FakeDetector(outcomes)
    scanner = TwoPassQrScanner(renderer, detector, 250, 400)
    result = scanner.scan_page(pdf, 0, nominal, work_dir, 1, logs.append)
    return result, renderer, detector, logs


def test_qr_trouve_a_la_premiere_passe(setup_case) -> None:
    items = [object()]
    result, renderer, detector, logs = run_case(setup_case, [items])
    assert result.items is items
    assert result.has_qr and not result.used_fallback
    assert result.dpi == 250 and result.width == 250 and result.height == 125
    assert result.png_path == detector.paths[0]
    assert renderer.calls == []
    assert logs == ["[info] page 1: 1 QR détecté(s)"]


def test_qr_trouve_uniquement_a_la_deuxieme_passe(setup_case) -> None:
    items = [object()]
    result, renderer, detector, logs = run_case(setup_case, [[], items])
    assert result.items is items and result.has_qr and result.used_fallback
    assert result.dpi == 400 and (result.width, result.height) == (400, 200)
    assert result.png_path == detector.paths[1]
    assert result.png_path.parent.name == "dpi_400"
    assert renderer.calls[0][1] == 400
    assert "[warn] page 1: aucun QR à 250 DPI, reconversion à 400 DPI" in logs
    assert logs[-1] == "[ok]   page 1: 1 QR détecté(s) à 400 DPI"


def test_aucun_qr_revient_au_png_nominal(setup_case) -> None:
    result, _renderer, _detector, logs = run_case(setup_case, [[], []])
    assert not result.has_qr and not result.used_fallback
    assert result.dpi == 250 and result.png_path.name == "page_0001.png"
    assert logs[-1] == (
        "[warn] page 1: toujours aucun QR à 400 DPI — page incluse à 250 DPI"
    )


def test_erreur_scan_nominal_garde_la_page_brute(setup_case) -> None:
    result, renderer, _detector, logs = run_case(
        setup_case, [ScanError("panne simulée")]
    )
    assert result.items == [] and not result.used_fallback and result.dpi == 250
    assert renderer.calls == []
    assert logs == [
        "[error] page 1: échec du scan (panne simulée) — page incluse brute"
    ]


def test_erreur_scan_secours_revient_au_nominal(setup_case) -> None:
    result, _renderer, _detector, logs = run_case(
        setup_case, [[], ScanError("panne simulée")]
    )
    assert result.items == [] and not result.used_fallback and result.dpi == 250
    assert logs[-1] == (
        "[error] page 1: échec du scan à 400 DPI (panne simulée) "
        "— page incluse à 250 DPI"
    )


def test_exception_non_scanerror_remonte(setup_case) -> None:
    with pytest.raises(RuntimeError, match="inattendue"):
        run_case(setup_case, [RuntimeError("inattendue")])
