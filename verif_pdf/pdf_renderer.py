"""Conversion des pages PDF en images PNG."""
from __future__ import annotations
from pathlib import Path
from typing import Any

class PdfRenderer:
    """Rend les pages PDF en PNG selon le DPI demandé."""
    def __init__(self, renderer: Any | None = None) -> None:
        self._renderer = renderer
    def _pdfium(self) -> Any:
        if self._renderer is None:
            import pypdfium2 as pdfium
            self._renderer = pdfium
        return self._renderer
    def render_page(self, pdf_path: Path, page_index: int, dpi: int, output_dir: Path, pad: int = 4) -> Path:
        """Rend une page précise dans le dossier de travail."""
        pdfium = self._pdfium(); scale = dpi / 72.0
        with pdfium.PdfDocument(str(pdf_path)) as doc:
            page = doc[page_index]; bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()
            out_path = output_dir / f"page_{page_index + 1:0{pad}d}.png"
            pil_image.save(str(out_path), format="PNG")
            return out_path
    def convert_pdf_to_pngs(self, pdf_path: Path, output_dir: Path, dpi: int, log: Any) -> list[Path]:
        """Convertit toutes les pages à la résolution nominale."""
        pdf_path = Path(pdf_path).resolve()
        if not pdf_path.exists(): raise FileNotFoundError(f"PDF introuvable: {pdf_path}")
        output_dir.mkdir(parents=True, exist_ok=True)
        with self._pdfium().PdfDocument(str(pdf_path)) as doc: n_pages = len(doc)
        log(f"[conv] {n_pages} page(s) à convertir à {dpi} DPI")
        paths=[]
        for i in range(n_pages):
            png=self.render_page(pdf_path, i, dpi, output_dir); paths.append(png)
            log(f"[conv]   page {i + 1:>{len(str(n_pages))}}/{n_pages} -> {png.name}")
        return paths
