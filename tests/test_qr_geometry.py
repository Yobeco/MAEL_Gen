"""Tests unitaires de normalisation géométrique QR."""
from types import SimpleNamespace as NS
import pytest
from pdf2app.qr_geometry import quad_to_square

def point(x,y): return NS(x=x,y=y)
def test_quad_square_relative_and_centered():
    pos=NS(top_left=point(20,10),top_right=point(60,20),bottom_right=point(50,50),bottom_left=point(10,40))
    zone=quad_to_square(pos,100,100)
    assert zone.x==pytest.approx(0.1) and zone.y==pytest.approx(0.05)
    assert zone.width==pytest.approx(0.5) and zone.height==pytest.approx(0.5)
def test_invalid_dimensions():
    with pytest.raises(ValueError): quad_to_square(None,0,1)
