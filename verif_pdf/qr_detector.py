"""Détection des QR bruts et enrichissement pour la présentation."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from qr_dto import TtsItem, CloudItem, WifiItem, RawQr
from .render_constants import *
from qr_scan import ImageScanner, ScanError
from qr_parse import parse_all



class QrDetector:
    """Adapte le scanner QR du projet et retourne des objets RawQr."""
    def __init__(self, scanner: Any | None = None) -> None:
        self._scanner = scanner
    def scan(self, image_path: str | Path) -> list[RawQr]:
        """Détecte les QR d’une image sans interprétation sémantique."""
        if self._scanner is None:
            self._scanner = ImageScanner()
        return self._scanner.scan(image_path)

@dataclass(frozen=True, slots=True)
class ColoredTtsItem:
    """
    Objet de rendu local : associe un `TtsItem` (objet métier neutre) aux
    couleurs nécessaires à l'affichage (cadre OpenCV, label fpdf2).

    Ce DTO est **local à ce module** : il ne fait pas partie du contrat
    partagé (qr_dto). Il matérialise la frontière entre la couche
    « données métier » et la couche « présentation ».

    Permet d'éviter de polluer `TtsItem` avec des préoccupations de
    couleur, conformément à la séparation des responsabilités.
    """

    item: TtsItem | CloudItem | WifiItem
    color_bgr: tuple[int, int, int]
    color_rgb: tuple[int, int, int]

    # Raccourcis pratiques pour le rendu, évitant d'écrire
    # `colored.item.raw.position` partout.
    @property
    def position(self) -> object:
        return self.item.raw.position

    @property
    def mode(self) -> str:
        return self.item.mode

    @property
    def text(self) -> str:
        return self.item.text

    @property
    def lang(self) -> str | None:
        """Langue TTS ; None pour les QR cloud et Wifi."""
        return self.item.lang if isinstance(self.item, TtsItem) else None

def color_choose(item: TtsItem | CloudItem | WifiItem) -> ColoredTtsItem:
    """
    Enrichit un `TtsItem` avec les couleurs de rendu correspondant à son
    mode. Retourne un `ColoredTtsItem` (objet de rendu local).

    Fonction pure : n'altère pas l'item d'origine (qui est de toute
    façon immuable).
    """
    mode = item.mode
    return ColoredTtsItem(
        item=item,
        color_bgr=COLORS_BGR[mode],
        color_rgb=COLORS_RGB[mode],
    )

def qr_scan_and_parse(
    image_path: str | Path,
    page_number: int | None = None,
    detector: "QrDetector | None" = None,
) -> list[ColoredTtsItem]:
    """
    Point d'entrée unique du pipeline pour ce module :
        1. Scan bas niveau via qr_scan (image → list[RawQr]).
        2. Analyse sémantique via qr_parse (RawQr → TtsItem, tri inclus).
        3. Enrichissement couleur local (TtsItem → ColoredTtsItem).

    Retourne une liste éventuellement vide. Lève `ScanError` si
    l'acquisition échoue (fichier absent, image illisible…). Un QR dont
    l'analyse échoue est ignoré individuellement.
    """
    scanner = detector or QrDetector()
    raws = scanner.scan(image_path)

    # Chaque QR passe par qr_parse, y compris les QR WIFI.
    # Le try/except reste isolé afin qu'un QR invalide n'arrête pas la page.
    items = []
    for qr_number, raw in enumerate(raws, 1):
        try:
            items.extend(parse_all([raw]))
        except Exception:
            if page_number is not None:
                # Ne jamais afficher le contenu du QR : un mot de passe WIFI
                # pourrait y figurer.
                print(f"[error] page {page_number}: QR #{qr_number} ignoré (analyse invalide)")

    return [color_choose(item) for item in items]
