# -*- coding: utf-8 -*-
"""
manual_tts_setup.py
===================

But
---
Faire tourner le pipeline ``qr_scan -> qr_parse -> tts_setup``
sans avoir à fabriquer une vraie image de QR code, en s'appuyant
sur ``qr_scan_virtual`` (qui fournit des contenus **déjà obfusqués**
comme s'ils sortaient d'un vrai scanneur) puis sur le déobfuscateur
réel de ``MAEL_obfus`` (via le pipeline de ``qr_parse``).

Exécution
---------
    # 1. Avec la liste d'exemples (contenus obfusqués) par défaut
    python3 manual_tts_setup.py

    # 2. Avec des contenus passés en arguments
    python3 manual_tts_setup.py "<contenu obfusqué 1>" "<contenu obfusqué 2>"

    # 3. Mode interactif
    python3 manual_tts_setup.py -i
"""

from __future__ import annotations

import logging
import os
import sys
from pprint import pformat
from typing import Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_UPLOADS = "/mnt/user-data/uploads"

for path in (_HERE, _UPLOADS):
    if path not in sys.path:
        sys.path.append(path)

logging.basicConfig(
    level=logging.WARNING,
    format="[%(levelname)s] %(name)s: %(message)s",
)

# Imports métier (après ajustement de sys.path).
# NOTE : on ne stub plus ``Obfus.deobfus`` : le déobfuscateur
# ``qr_parse._obfusor`` (instance globale) doit pouvoir retrouver
# la chaîne en clair à partir des contenus *obfusqués* fournis
# par ``qr_scan_virtual``.
from qr_dto import RawQr  # noqa: E402
import qr_parse  # noqa: E402
from tts_setup import TtsSetupBuilder, TtsSetup  # noqa: E402

# Contenus de QR simulés (déjà obfusqués).
import qr_scan_virtual  # noqa: E402

EXAMPLES: list[str] = list(qr_scan_virtual._DEFAULT_OBFUSCATED_TEXTS)


class _FakeCorner:
    """Coin d'un bounding-box fictif."""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class _FakePosition:
    def __init__(self) -> None:
        self.top_left = _FakeCorner(0.0, 0.0)
        self.top_right = _FakeCorner(10.0, 0.0)
        self.bottom_right = _FakeCorner(10.0, 10.0)
        self.bottom_left = _FakeCorner(0.0, 10.0)


def make_raw(text: str) -> RawQr:
    return RawQr(
        text=text,
        position=_FakePosition(),
        format="QRCode",
        ec_level=None,
    )


def process_one(content: str, index: int) -> None:
    """
    Traite un contenu de QR déjà obfusqué via le pipeline
    complet : déobfuscation (qr_parse) puis construction du
    ``TtsSetup`` correspondant.
    """
    header = f"--- Cas #{index} ---"
    print(header)
    print(f"  contenu brut : {content!r}")

    raw = make_raw(content)

    try:
        items = qr_parse.parse_all([raw])
    except Exception as exc:  # noqa: BLE001
        print(f"  ERREUR parse_all : {exc!r}")
        print()
        return

    if not items:
        print("  (aucun item produit)")
        print()
        return

    builder = TtsSetupBuilder()

    for it in items:
        # Affichage lisible du TtsItem.
        print(f"  TtsItem:")
        print(f"      original = {it.original!r}")
        print(f"      text     = {it.text!r}")
        print(f"      lang     = {it.lang!r}")
        print(f"      mode     = {it.mode!r}")

        try:
            setup: TtsSetup = builder.build(it)
        except Exception as exc:  # noqa: BLE001
            print(f"  ERREUR TtsSetupBuilder.build : {exc!r}")
            continue

        print(f"  TtsSetup.to_dict() :")
        print(pformat(setup.to_dict(), indent=8))

        print(f"  TtsSetup.ok : {setup.ok}")
    print()


def run_examples(examples: list[str]) -> None:
    """Boucle sur une liste de contenus."""
    print(f"=== {len(examples)} cas à traiter ===")
    print()
    for i, content in enumerate(examples, start=1):
        process_one(content, index=i)


def run_interactive() -> None:
    print("=== Mode interactif ===")
    print()
    i = 0
    while True:
        try:
            line = input("contenu> ").rstrip("\n")
        except EOFError:
            print()
            break
        if not line:
            break
        i += 1
        process_one(line, index=i)


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-i", "--interactive"):
        run_interactive()
        return 0

    if argv:
        run_examples(argv)
    else:
        run_examples(EXAMPLES)

    print("=== Terminé ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
