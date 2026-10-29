# -*- coding: utf-8 -*-
"""Scanner virtuel alimenté par les chaînes de démonstration MAEL."""
from __future__ import annotations

import random
from typing import Iterable

import MAEL_obfus
import test_list
from qr_scan import QrScanner, ScanError
from qr_dto import RawQr

_obfusor = MAEL_obfus.Obfus()


def _prepare_text(text: str) -> str:
    """Laisse les QR Wi-Fi en clair et obfusque les autres textes."""
    if text.startswith(("WIFI:", "wifi:")):
        return text
    return _obfusor.enobfus(text)


_DEFAULT_OBFUSCATED_TEXTS: list[str] = [
    _prepare_text(s) for s in test_list.strings_to_obfus
]


class VirtualScanner(QrScanner):
    """Émet un RawQr à chaque appel, depuis une liste de textes."""

    def __init__(
        self,
        texts: Iterable[str] | None = None,
        mode: str = "aleatoire",
        seed: int | None = None,
    ) -> None:
        if mode not in {"aleatoire", "sequentiel", "index"}:
            raise ValueError(f"Mode de scan inconnu : {mode!r}")
        self._texts = list(_DEFAULT_OBFUSCATED_TEXTS if texts is None else texts)
        self._mode = mode
        self._random = random.Random(seed)
        self._position = 0
        self._cycle: list[int] = []
        self._cycle_position = 0
        self._previous_cycle_last: int | None = None

    def _next_random_index(self) -> int:
        if not self._cycle or self._cycle_position >= len(self._cycle):
            self._cycle = list(range(len(self._texts)))
            self._random.shuffle(self._cycle)
            # Éviter une répétition à la frontière de deux cycles.
            if (len(self._cycle) > 1 and self._previous_cycle_last is not None
                    and self._cycle[0] == self._previous_cycle_last):
                self._cycle[0], self._cycle[1] = self._cycle[1], self._cycle[0]
            self._cycle_position = 0
        index = self._cycle[self._cycle_position]
        self._cycle_position += 1
        if self._cycle_position == len(self._cycle):
            self._previous_cycle_last = index
        return index

    def scan(self, source: object = None) -> list[RawQr]:
        if not self._texts:
            raise ScanError("La liste des textes du scanner virtuel est vide.")
        if isinstance(source, int):
            index = source
        elif self._mode == "index":
            raise ScanError("Le mode 'index' exige un index entier comme source.")
        elif self._mode == "aleatoire":
            index = self._next_random_index()
        else:
            index = self._position % len(self._texts)
            self._position += 1
        if index < 0 or index >= len(self._texts):
            raise ScanError(f"Index invalide : {index} (0..{len(self._texts)-1}).")
        return [RawQr(text=self._texts[index], position=None, format="QRCode", ec_level=None)]


__all__ = ["VirtualScanner", "_DEFAULT_OBFUSCATED_TEXTS"]


def _cli() -> None:
    scanner = VirtualScanner()
    print("Scanner virtuel MAEL — Entrée : suivant, numéro : index, q : quitter")
    while True:
        try:
            value = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if value.lower() == "q":
            break
        try:
            result = scanner.scan(int(value) if value else None)
        except ValueError:
            print("Saisir un numéro valide, Entrée ou q.")
            continue
        except ScanError as exc:
            print(f"[ScanError] {exc}")
            continue
        print(result[0].text)


if __name__ == "__main__":
    _cli()
