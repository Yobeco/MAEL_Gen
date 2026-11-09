"""Orchestration du scan QR et de la génération HTML autonome."""
from __future__ import annotations
import base64
import importlib
import logging
import os
import sys
from dataclasses import replace
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


# Modules loaded once, lazily: their package can differ between deployments.
_QR_MODULE = None
_TTS_BUILDER = None
_QR_IMPORT_ATTEMPTED = False
_IMPORT_DIAGNOSTIC_EMITTED = False


def _module_candidates(filename: str) -> list[Path]:
    """Find package modules close to pdf2app/ or the caller's working tree."""
    roots: list[Path] = []
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        current = start
        # Limit upward traversal; never search the entire filesystem.
        for _ in range(4):
            if current not in roots:
                roots.append(current)
            if current.parent == current:
                break
            current = current.parent

    found: list[Path] = []
    skipped = {".git", ".venv", "venv", "node_modules", "__pycache__", "site-packages"}
    for root in roots:
        # Include root and up to three directory levels below it.
        for directory, dirs, files in os.walk(root):
            rel = Path(directory).relative_to(root)
            depth = len(rel.parts)
            dirs[:] = [d for d in dirs if d not in skipped and not d.startswith(".")]
            if depth >= 3:
                dirs[:] = []
            if filename in files:
                candidate = Path(directory) / filename
                if candidate not in found:
                    found.append(candidate)
    return found


def _import_file_as_package(module_file: Path):
    """Import a relative-importing module by its package-qualified name."""
    package_dir = module_file.parent
    grandparent = str(package_dir.parent.resolve())
    if grandparent not in sys.path:
        sys.path.insert(0, grandparent)
    return importlib.import_module(f"{package_dir.name}.{module_file.stem}")


def _load_qr_dependencies():
    """Resolve parser/TTS imports once; preserve the historical package imports first."""
    global _QR_MODULE, _TTS_BUILDER, _QR_IMPORT_ATTEMPTED, _IMPORT_DIAGNOSTIC_EMITTED
    if _QR_IMPORT_ATTEMPTED:
        return _QR_MODULE, _TTS_BUILDER
    _QR_IMPORT_ATTEMPTED = True
    searched: list[str] = []

    # The earlier working scanner imported parser objects from verif_pdf.
    parser_names = ["verif_pdf.qr_parse", "pdf2app.qr_parse", "qr_parse"]
    for name in parser_names:
        searched.append(name)
        try:
            _QR_MODULE = importlib.import_module(name)
            break
        except Exception:
            pass
    if _QR_MODULE is None:
        for module_file in _module_candidates("qr_parse.py"):
            searched.append(str(module_file))
            try:
                _QR_MODULE = _import_file_as_package(module_file)
                break
            except Exception as exc:
                logging.getLogger(__name__).debug("Échec import candidat %s: %s", module_file, exc)
                continue

    # Keep the established top-level tts_setup import first.
    tts_names = ["tts_setup"]
    if _QR_MODULE is not None:
        package_name = _QR_MODULE.__name__.rsplit(".", 1)[0] if "." in _QR_MODULE.__name__ else None
        if package_name:
            tts_names.append(f"{package_name}.tts_setup")
    for name in dict.fromkeys(tts_names):
        searched.append(name)
        try:
            _TTS_BUILDER = importlib.import_module(name).TtsSetupBuilder
            break
        except Exception:
            pass
    if _TTS_BUILDER is None:
        for module_file in _module_candidates("tts_setup.py"):
            searched.append(str(module_file))
            try:
                _TTS_BUILDER = _import_file_as_package(module_file).TtsSetupBuilder
                break
            except Exception:
                continue

    if (_QR_MODULE is None or _TTS_BUILDER is None) and not _IMPORT_DIAGNOSTIC_EMITTED:
        _IMPORT_DIAGNOSTIC_EMITTED = True
        bases = f"{Path(__file__).resolve().parent} et {Path.cwd().resolve()} (remontée limitée, 3 niveaux)"
        logging.getLogger(__name__).error(
            "Import QR/TTS incomplet; fichiers recherchés autour de %s; imports essayés: %s",
            bases, ", ".join(searched),
        )
    return _QR_MODULE, _TTS_BUILDER


def _is_cloud_item(item, cloud_type=None) -> bool:
    """Recognize cloud results even when their package's class import failed."""
    if cloud_type is not None:
        try:
            if isinstance(item, cloud_type):
                return True
        except TypeError:
            pass
    return (type(item).__name__ == "CloudItem" or
            hasattr(item, "id") or hasattr(item, "opaque"))


def _parse_qr_payload(qr):
    """Return (tts, cloud) while keeping import and class identity failures harmless."""
    parser, tts_builder = _load_qr_dependencies()
    if parser is None:
        # _load_qr_dependencies emitted the single actionable diagnostic.
        return None, None
    parsed = parser.parse_all([qr])
    if len(parsed) != 1:
        raise ValueError("le QR ne produit pas un élément sémantique unique")
    item = parsed[0]
    if _is_cloud_item(item, getattr(parser, "CloudItem", None)):
        return None, {"id": getattr(item, "id", getattr(item, "opaque", None)),
                      "mode": getattr(item, "mode", None),
                      "text": getattr(item, "text", None)}
    if tts_builder is None:
        # The missing TTS import was already reported once; keep scanning.
        return None, None
    if hasattr(item, "text") and hasattr(item, "mode"):
        setup = tts_builder().build(item)
        data = setup.to_dict()
        data["mode"] = getattr(setup, "mode", None)
        return data, None
    raise ValueError("le QR ne contient ni élément CloudItem ni élément TTS exploitable")


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
                zones=[]
                for qr_index, qr in enumerate(scan.items, start=1):
                    tts=None
                    cloud=None
                    try:
                        # Résolution mise en cache: aucun import n'est refait par QR.
                        tts, cloud = _parse_qr_payload(qr)
                    except Exception as exc:
                        logging.getLogger(__name__).warning(
                            "QR ignoré pour le QR %s de la page %s : %s: %s",
                            qr_index, i+1, type(exc).__name__, exc,
                        )
                    zone=quad_to_square(qr.position,scan.width,scan.height)
                    zones.append(replace(zone,tts=tts,cloud=cloud))
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
