"""Orchestration du scan QR et de la génération HTML autonome."""
from __future__ import annotations
import base64
import logging
from pathlib import Path
from pypdf import PdfReader
from .avif_encoder import AvifEncoder
from .config import Pdf2AppConfig
from .html_builder import HtmlBuilder
from .page_model import PageAsset
from .qr_geometry import quad_to_square
from verif_pdf.pdf_renderer import PdfRenderer
from verif_pdf.qr_detector import QrDetector
from verif_pdf.two_pass_scanner import TwoPassQrScanner

class Pdf2App:
    """Traite chaque page indépendamment et livre un HTML autonome."""
    def __init__(self, config: Pdf2AppConfig | None = None, renderer: PdfRenderer | None = None,
                 detector: QrDetector | None = None, html_builder: HtmlBuilder | None = None) -> None:
        self.config=config or Pdf2AppConfig(); self.renderer=renderer or PdfRenderer(); self.detector=detector or QrDetector()
        self.scanner=TwoPassQrScanner(self.renderer,self.detector,self.config.dpi,self.config.fallback_dpi)
        self.encoder=AvifEncoder(self.config.avif_quality,self.config.avif_speed,self.config.max_width)
        self.html_builder=html_builder or HtmlBuilder()

    def _log(self,message:str)->None:
        if self.config.verbose: print(message)

    def run(self,input_pdf:str|Path,output_html:str|Path)->Path:
        """Génère le HTML et continue après une erreur localisée à une page."""
        source=Path(input_pdf).resolve(); output=Path(output_html).resolve()
        if not source.is_file(): raise FileNotFoundError(f"PDF introuvable : {source}")
        output.parent.mkdir(parents=True,exist_ok=True)
        reader=PdfReader(str(source)); count=len(reader.pages)
        work=output.parent / f".{output.stem}_render"; work.mkdir(parents=True,exist_ok=True)
        nominal_dir=work / f"dpi_{self.config.dpi}"; nominal_dir.mkdir(parents=True,exist_ok=True)
        pages:list[PageAsset]=[]
        for i in range(count):
            page_error=None; zones=[]; png=None; scan=None
            try:
                png=self.renderer.render_page(source,i,self.config.dpi,nominal_dir,pad=len(str(count)))
                scan=self.scanner.scan_page(source,i,png,work,count,self._log)
                zones=[quad_to_square(q.position,scan.width,scan.height) for q in scan.items]
            except Exception as exc:
                page_error=f"{type(exc).__name__}: {exc}"; self._log(f"[error] page {i+1}: {page_error}")
            try:
                # Rend direct au DPI d'affichage : petit format, sans niveaux de gris.
                display_dir=work / f"dpi_{self.config.display_dpi}"
                display_dir.mkdir(parents=True,exist_ok=True)
                display_png=self.renderer.render_page(source,i,self.config.display_dpi,display_dir,pad=len(str(count)))
                encoded,w,h=self.encoder.encode(str(display_png),self.config.display_dpi)
                if scan is not None and scan.items and not page_error:
                    # Positions du rendu scan -> coordonnées relatives conservées; les carrés demeurent exacts à tout DPI.
                    pass
                pages.append(PageAsset(i+1,base64.b64encode(encoded).decode("ascii"),w,h,zones,page_error))
            except Exception as exc:
                message=f"{type(exc).__name__}: {exc}"; self._log(f"[error] page {i+1}: encodage AVIF impossible ({message})")
                if png is None:
                    # Aucun rendu pour cette page : conserver néanmoins sa place dans le lecteur.
                    pages.append(PageAsset(i+1,"",0,0,[],page_error or message))
                    continue
                try:
                    encoded,w,h=self.encoder.encode(str(png),self.config.dpi)
                    pages.append(PageAsset(i+1,base64.b64encode(encoded).decode("ascii"),w,h,zones,page_error or message))
                except Exception as fallback_exc:
                    # HTML conserve la page visible sous forme de message d'erreur, sans casser les autres pages.
                    pages.append(PageAsset(i+1,"",0,0,[],f"Échec AVIF : {fallback_exc}"))
        html=self.html_builder.build(pages); output.write_text(html,encoding="utf-8")
        self._log(f"[ok] HTML autonome créé : {output} ({output.stat().st_size} octets)")
        return output
