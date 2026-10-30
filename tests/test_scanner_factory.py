"""Tests de la fabrique de scanners."""
import pytest

from qr_scan import ImageScanner, QrScanner
from qr_scan_virtual import VirtualScanner
from scanner_factory import create_scanner


def test_hardware_defaut_et_virtual():
    assert isinstance(create_scanner("pc_virtual", texts=["x"]), VirtualScanner)
    assert isinstance(create_scanner(texts=["x"]), QrScanner)


def test_pc_pdf():
    assert isinstance(create_scanner("pc_pdf"), ImageScanner)


@pytest.mark.parametrize("hardware", ["rpi", "android", "ios", "web"])
def test_hardware_non_implimente(hardware):
    with pytest.raises(NotImplementedError, match=hardware):
        create_scanner(hardware)


def test_hardware_inconnu():
    with pytest.raises(ValueError, match="inconnu"):
        create_scanner("quantum")


def test_variable_environnement(monkeypatch):
    monkeypatch.setenv("MAEL_HW", "pc_virtual")
    assert isinstance(create_scanner(), VirtualScanner)
    monkeypatch.setenv("MAEL_HW", "android")
    with pytest.raises(NotImplementedError):
        create_scanner()
