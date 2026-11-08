"""Génération de lecteurs HTML autonomes à partir de PDF."""
from .app_builder import Pdf2App
from .config import Pdf2AppConfig
from .html_builder import HtmlBuilder
from .qr_geometry import QrZone, quad_to_square
__all__=["Pdf2App","Pdf2AppConfig","HtmlBuilder","QrZone","quad_to_square"]
