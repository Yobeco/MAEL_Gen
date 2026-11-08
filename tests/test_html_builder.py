"""Tests du HTML autonome."""
import re
from pdf2app.html_builder import HtmlBuilder
from pdf2app.page_model import PageAsset
from pdf2app.qr_geometry import QrZone

def test_html_embeds_pages_and_single_delegated_listener():
    page=PageAsset(1,"YWJj",10,20,[QrZone(.1,.2,.3,.3)])
    html=HtmlBuilder().build([page])
    assert 'data:image/avif;base64,' in html
    assert '"image":"YWJj"' in html and '"x":0.1' in html
    assert "Code QR cliqué" in html
    assert html.count("zones.addEventListener('click'")==1
    assert "__PAGES_JSON__" not in html
