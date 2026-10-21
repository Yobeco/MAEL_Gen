"""
qr_dto.py — Data Transfer Objects (DTO) immuables partagés par l'écosystème QR.

Ce module est neutre dans le graphe de dépendances :
  - il n'importe rien d'autre que la bibliothèque standard (dataclasses, typing) ;
  - il n'effectue aucune I/O ;
  - il ne contient aucune logique métier autre que des propriétés calculées pures ;
  - il ne connaît ni le hardware d'acquisition (zxingcpp, OpenCV, caméra…),
    ni l'obfuscation (MAEL_obfus), ni la présentation (couleurs, PDF).

Rôle central : définir les deux objets de transfert échangés entre les modules.

    qr_scan  ──produit──►  RawQr  ──consommé par──►  qr_parse
    qr_parse ──produit──►  TtsItem, CloudItem ou WifiItem ──consommés par──►  les UI

Convention de nommage :
  - Les champs sont en anglais (`text`, `format`…) pour rester cohérents avec
    la nomenclature Python et l'API zxingcpp.
  - Les champs métier restent neutres (`lang`, `mode`), leur vocabulaire est
    francophone (`"lire"`, `"dicter"`, `"epeler"`).

⚠️  Attention au doublon sémantique du nom `text` :
  - RawQr.text  = texte **brut tel que lu par le scanner** (encore obfusqué).
  - TtsItem.text = texte **clair, déobfusqué et nettoyé** (préfixe et suffixe retirés).
  Ce sont deux contenus distincts, à deux stades différents du pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


# ======================================================================
# Les constantes de mode vivent dans qr_parse afin que ce module reste
# limité aux DTO et n’introduise aucune dépendance circulaire.
# ======================================================================

# ======================================================================
#          DTO RawQr — sortie de qr_scan, entrée de qr_parse
# ======================================================================
@dataclass(frozen=True, slots=True)
class RawQr:
    """
    Représente **un code QR tel qu'il a été observé physiquement** dans
    une image ou un flux, sans aucune interprétation sémantique.

    Le DTO ne sait pas que le texte est obfusqué ; il ne connaît ni la
    langue, ni le mode. Il porte uniquement ce que le scanner a pu lire
    et localiser.

    Champs
    ------
    text : str
        Texte brut tel que lu par le scanner (encore obfusqué du point de
        vue de qr_parse).
    position : Any
        Position géométrique du QR dans l'image. La forme attendue est
        celle de zxingcpp : un objet exposant `top_left`, `top_right`,
        `bottom_right`, `bottom_left`, chacun avec des attributs `.x`
        et `.y`. Cette forme est un couplage implicite assumé : toute
        autre source devra normaliser sa position en amont.
    format : str
        Nom du format détecté (ex. "QRCode"). Utile pour les logs.
    ec_level : Optional[str]
        Niveau de correction d'erreur du QR, si le scanner le fournit.
        None sinon.
    """

    text: str
    position: Any
    format: str
    ec_level: Optional[str]

    # ------------------------------------------------------------------
    # Propriétés géométriques dérivées
    # ------------------------------------------------------------------
    # Ces propriétés décrivent intrinsèquement le QR physique : elles
    # ne relèvent pas d'une décision d'analyse, mais d'une lecture de
    # sa géométrie. Elles sont donc légitimement placées ici, sur le
    # DTO, plutôt que dans qr_parse.

    @property
    def center_y(self) -> float:
        """Ordonnée du centre vertical du QR (moyenne haut/bas gauche)."""
        return (self.position.top_left.y + self.position.bottom_left.y) / 2.0

    @property
    def height(self) -> float:
        """Hauteur du QR (valeur absolue de la différence haut/bas à gauche)."""
        return abs(self.position.bottom_left.y - self.position.top_left.y)

    @property
    def left_x(self) -> float:
        """Abscisse du bord gauche du QR (coin supérieur gauche)."""
        return self.position.top_left.x


# ======================================================================
# DTO TtsItem — sortie de qr_parse pour les contenus à lire
# ======================================================================
@dataclass(frozen=True, slots=True)
class TtsItem:
    """Contenu textuel enrichi à restituer par synthèse vocale."""

    raw: RawQr
    original: str
    text: str
    lang: Optional[str]
    mode: str


# ======================================================================
# DTO CloudItem — sortie de qr_parse pour les services cloud
# ======================================================================
@dataclass(frozen=True, slots=True)
class CloudItem:
    """Identifiant d’un document ou service cloud."""

    raw: RawQr
    mode: str
    id: str
    text: str


# ======================================================================
# DTO WifiItem — sortie de qr_parse pour les paramètres Wi-Fi
# ======================================================================
@dataclass(frozen=True, slots=True)
class WifiItem:
    """Paramètres d’un réseau Wi-Fi encodé dans un QR."""

    raw: RawQr
    mode: str
    type: str
    ssid: str
    password: str = field(repr=False)
    hide: bool = False
    text: str = "Wifi"

