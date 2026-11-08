"""Orchestration du traitement PDF multi-page."""
from __future__ import annotations
import tempfile
from pathlib import Path
from typing import Any
from pypdf import PdfWriter
from .config import ProcessingConfig
from .pdf_renderer import PdfRenderer
from .qr_detector import QrDetector
from .qr_annotator import QrAnnotator
from .pdf_writer import PDFWriter
from .two_pass_scanner import TwoPassQrScanner

class VerifPdf:
    """Orchestre le rendu, la détection, l’annotation et la fusion."""
    def __init__(self, config: ProcessingConfig, renderer: PdfRenderer | None = None, detector: QrDetector | None = None, annotator: QrAnnotator | None = None, pdf_writer: PDFWriter | None = None, two_pass_scanner: TwoPassQrScanner | None = None) -> None:
        self.config=config
        self.renderer=renderer or PdfRenderer()
        self.detector=detector or QrDetector()
        self.annotator=annotator or QrAnnotator()
        self.pdf_writer=pdf_writer or PDFWriter()
        self.two_pass_scanner=two_pass_scanner or TwoPassQrScanner(
            self.renderer, self.detector, config.dpi, config.fallback_dpi
        )
    def _log(self, msg: str) -> None:
        if self.config.verbose: print(msg)
    def process_single_page(self, png_path: Path, work_dir: Path, page_number: int | None = None) -> Path:
        """Annote une page et en produit le PDF enrichi."""
        png_path=Path(png_path).resolve(); stem=png_path.stem
        annotated_png=work_dir / f"{stem}_annotated.png"; page_pdf=work_dir / f"{stem}.pdf"
        self.annotator.annotate(png_path, annotated_png, page_number=page_number, detector=self.detector)
        self.pdf_writer.write_page(annotated_png, page_pdf, source_image_path=png_path, verbose=False, detector=self.detector)
        return page_pdf
    def _png_to_pdf(self, png_path: Path, output_pdf_path: Path) -> Path:
        return self.pdf_writer.png_to_pdf(png_path, output_pdf_path)
    def merge_pdfs(self, pdf_paths: list[Path], output_path: Path) -> Path:
        """Fusionne les PDF des pages dans l’ordre d’origine."""
        output_path=Path(output_path).resolve(); output_path.parent.mkdir(parents=True, exist_ok=True)
        writer=PdfWriter()
        for pdf_path in pdf_paths: writer.append(str(Path(pdf_path).resolve()))
        writer.write(str(output_path)); writer.close()
        self._log(f"[merge] {len(pdf_paths)} page(s) fusionnée(s) -> {output_path}")
        return output_path
    def run(self, input_pdf: str | Path, output_pdf: str | Path) -> Path:
        """Traite toutes les pages du PDF, en gardant les pages en échec brutes."""
        input_pdf=Path(input_pdf).resolve(); output_pdf=Path(output_pdf).resolve()
        if not input_pdf.exists(): raise FileNotFoundError(f"PDF introuvable: {input_pdf}")
        self._log("=" * 60); self._log(f"  Traitement de : {input_pdf}"); self._log(f"  Sortie        : {output_pdf}")
        self._log(f"  DPI           : {self.config.dpi} (fallback: {self.config.fallback_dpi})"); self._log("=" * 60)
        with tempfile.TemporaryDirectory(prefix="qr_pdf_") as tmp:
            tmp_dir=Path(tmp); png_dir=tmp_dir / "png"; work_dir=tmp_dir / "work"; png_dir.mkdir(); work_dir.mkdir()
            nominal_dir=png_dir / f"dpi_{self.config.dpi}"
            png_paths=self.renderer.convert_pdf_to_pngs(input_pdf, nominal_dir, self.config.dpi, self._log)
            final_pngs=[]
            for i, png_path in enumerate(png_paths):
                result=self.two_pass_scanner.scan_page(
                    input_pdf, i, png_path, png_dir, len(png_paths), self._log
                )
                final_pngs.append(result.png_path)
            page_pdfs=[]
            for i, png_path in enumerate(final_pngs):
                self._log(f"[page] traitement de la page {i + 1}…")
                try: page_pdfs.append(self.process_single_page(png_path, work_dir, page_number=i + 1))
                except Exception as exc:
                    self._log(f"[error] page {i + 1}: échec du traitement ({exc}) — page incluse brute")
                    page_pdfs.append(self._png_to_pdf(png_path, work_dir / f"{png_path.stem}_brut.pdf"))
            if not page_pdfs: raise RuntimeError("Aucune page n'a pu être traitée.")
            self.merge_pdfs(page_pdfs, output_pdf)
        self._log("=" * 60); self._log("  Traitement terminé."); self._log("=" * 60)
        return output_pdf
