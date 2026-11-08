"""Assemblage d'une page HTML autonome à partir des pages encodées."""
from __future__ import annotations
import json
from pathlib import Path
from .page_model import PageAsset

class HtmlBuilder:
    """Insère les données JSON dans le template HTML embarqué."""
    def __init__(self, template_path: Path | None = None) -> None:
        self.template_path = template_path or Path(__file__).parent / "templates" / "viewer.html"

    def build(self, pages: list[PageAsset]) -> str:
        """Retourne le HTML complet, avec les images intégrées en base64."""
        template=self.template_path.read_text(encoding="utf-8")
        payload=json.dumps([page.as_dict() for page in pages],ensure_ascii=False,separators=(",",":"))
        if template.count("__PAGES_JSON__") != 1:
            raise ValueError("Le template doit contenir exactement un placeholder __PAGES_JSON__.")
        return template.replace("__PAGES_JSON__",payload)
