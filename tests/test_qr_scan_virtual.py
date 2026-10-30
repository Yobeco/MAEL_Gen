"""Tests unitaires du scanner virtuel MAEL."""
import pytest

from qr_scan import ScanError
from qr_scan_virtual import VirtualScanner


def test_un_cycle_aleatoire_couvre_chaque_element_sans_doublon():
    texts = ["alpha", "beta", "gamma", "delta"]
    scanner = VirtualScanner(texts, seed=11)
    cycle = [scanner.scan()[0].text for _ in texts]
    assert sorted(cycle) == sorted(texts)
    assert len(set(cycle)) == len(texts)


def test_nouveau_cycle_est_remelange_et_frontiere_sans_repetition():
    texts = [str(i) for i in range(7)]
    scanner = VirtualScanner(texts, seed=93)
    a = [scanner.scan()[0].text for _ in texts]
    b = [scanner.scan()[0].text for _ in texts]
    assert set(a) == set(texts) and set(b) == set(texts)
    assert a != b
    assert a[-1] != b[0]


def test_seed_reproductible():
    def cycle():
        scanner = VirtualScanner(list("abcdef"), seed=1234)
        return [scanner.scan()[0].text for _ in range(6)]
    assert cycle() == cycle()


def test_index_et_mode_sequentiel():
    scanner = VirtualScanner(["a", "b", "c"], mode="index")
    assert scanner.scan(2)[0].text == "c"
    with pytest.raises(ScanError):
        scanner.scan()
    sequential = VirtualScanner(["a", "b"], mode="sequentiel")
    assert [sequential.scan()[0].text for _ in range(5)] == ["a", "b", "a", "b", "a"]


def test_erreurs_liste_vide_et_index_invalide():
    with pytest.raises(ScanError):
        VirtualScanner([], mode="sequentiel").scan()
    scanner = VirtualScanner(["a"], mode="index")
    for index in (-1, 1):
        with pytest.raises(ScanError):
            scanner.scan(index)
    with pytest.raises(ValueError):
        VirtualScanner(["a"], mode="invalide")


def test_raw_qr_contient_les_champs_conformes():
    raw = VirtualScanner(["payload"]).scan()[0]
    assert raw.text == "payload"
    assert raw.position is None
    assert raw.format == "QRCode" and raw.ec_level is None
