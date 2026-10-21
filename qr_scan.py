"""
qr_scan.py — Acquisition bas niveau des codes QR.

Ce module a **une seule responsabilité** : produire une liste de `RawQr`
à partir d'une source quelconque (image, flux caméra, stub de test…).
Il ne connaît ni la sémantique du contenu, ni l'obfuscation, ni le rendu.

Rôle dans l'écosystème :

    [Source] ──► QrScanner.scan() ──► list[RawQr] ──► qr_parse.parse_all()
     (ce module)         (qr_dto)         (qr_parse)

Contrat public
--------------
  - Classe abstraite `QrScanner` : définit la seule méthode que tout
    scanner doit exposer : `scan() -> list[RawQr]`.
  - Exception `ScanError` : levée sur erreur d'acquisition (fichier
    introuvable, image corrompue, périphérique indisponible…).
  - Implémentation concrète `ImageScanner` : scanne un fichier image
    via zxingcpp + OpenCV.

Convention d'erreur
-------------------
  - Aucun QR trouvé      → liste vide `[]` (cas normal, pas une erreur).
  - Échec d'acquisition  → `ScanError` (fichier, format, hardware…).
  Cette distinction est essentielle : une page PDF sans QR n'est pas
  une anomalie, tandis qu'une image illisible en est une.

Cycle de vie
------------
  La V1 adopte un contrat **minimal** : seule `scan()` est obligatoire.
  Les scanners à état (caméra, flux vidéo) géreront leur cycle de vie
  en interne. Un contrat étendu (open / scan_once / close) pourra être
  introduit plus tard sans casser le contrat minimal.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import cv2
import zxingcpp

from qr_dto import RawQr


# ======================================================================
#                   Exception dédiée au module
# ======================================================================
class ScanError(Exception):
    """
    Erreur d'acquisition bas niveau : le scanner n'a pas pu produire de
    résultat exploitable (fichier absent, image illisible, périphérique
    indisponible…).

    À ne pas confondre avec le cas « aucun QR détecté », qui retourne
    une liste vide et n'est pas une erreur.
    """


# ======================================================================
#   Contrat abstrait — tout scanner doit respecter cette interface
# ======================================================================
class QrScanner(ABC):
    """
    Contrat abstrait d'un scanner de codes QR.

    Toute implémentation concrète (image, caméra Raspberry Pi, caméra
    de téléphone, stub de test…) doit exposer une méthode `scan()` qui
    retourne une liste de `RawQr` — éventuellement vide.

    Le contrat est **minimal** : il ne présume rien du cycle de vie, ni
    du hardware, ni de la source. Les scanners à état gèrent leur propre
    ouverture/fermeture en interne.
    """

    @abstractmethod
    def scan(self, source: object) -> list[RawQr]:
        """
        Retourne la liste des QR codes détectés dans la source.

        Paramètres
        ----------
        source : object
            La source à scanner. Son type concret dépend de l'implémentation :
              - ImageScanner   : chemin de fichier (str ou Path),
              - CameraScanner  : ignoré ou index de caméra,
              - VirtualScanner : ignoré.

        Retour
        ------
        list[RawQr]
            Liste éventuellement vide. L'ordre des éléments est celui
            du scanner ; le tri naturel est de la responsabilité de
            `qr_parse`.

        Lève
        ----
        ScanError
            Si l'acquisition échoue (source inaccessible, format non
            supporté, hardware indisponible…).
        """
        raise NotImplementedError


# ======================================================================
#            Implémentation concrète : scan d'un fichier image
# ======================================================================
class ImageScanner(QrScanner):
    """
    Scanner de codes QR à partir d'un fichier image (PNG, JPEG…).

    Utilise zxingcpp pour la détection, avec les options `try_rotate`
    et `try_downscale` activées pour maximiser le taux de détection sur
    les images issues de PDF ou de captures variées.

    Cette implémentation est **one-shot** : chaque appel à `scan()` est
    indépendant, sans état conservé entre les appels.
    """

    def __init__(
        self,
        try_rotate: bool = True,
        try_downscale: bool = True,
    ) -> None:
        """
        Paramètres
        ----------
        try_rotate : bool
            Autorise zxingcpp à tester des rotations (utile pour les
            QR imprimés à l'envers ou pivotés).
        try_downscale : bool
            Autorise zxingcpp à sous-échantillonner l'image pour
            accélérer la détection sur les grandes images.
        """
        self._try_rotate = try_rotate
        self._try_downscale = try_downscale

    def scan(self, source: object) -> list[RawQr]:
        """
        Détecte les QR codes dans le fichier image `source`.

        Paramètres
        ----------
        source : str | Path
            Chemin du fichier image à analyser.

        Retour
        ------
        list[RawQr]
            Liste éventuellement vide.

        Lève
        ----
        ScanError
            - si le chemin ne correspond pas à un fichier existant ;
            - si l'image ne peut pas être lue par OpenCV.
        """
        path = Path(str(source)).resolve()

        if not path.exists():
            raise ScanError(f"Fichier introuvable : {path}")

        if not path.is_file():
            raise ScanError(f"Le chemin ne désigne pas un fichier : {path}")

        img = cv2.imread(str(path))
        if img is None:
            raise ScanError(
                f"Impossible de lire l'image (format non supporté ou "
                f"fichier corrompu) : {path}"
            )

        return self._detect(img)

    # ------------------------------------------------------------------
    #          Détection interne — reçoit une image déjà chargée
    # ------------------------------------------------------------------
    def _detect(self, img) -> list[RawQr]:
        """
        Applique zxingcpp sur une image OpenCV déjà chargée et convertit
        les résultats en `RawQr`.

        Cette méthode est séparée de `scan()` pour permettre à d'autres
        scanners (par ex. un scanner vidéo) de réutiliser la même
        logique de détection sans repasser par le système de fichiers.
        """
        try:
            results = zxingcpp.read_barcodes(
                img,
                formats=zxingcpp.BarcodeFormat.QRCode,
                try_rotate=self._try_rotate,
                try_downscale=self._try_downscale,
            )
        except Exception as exc:
            # zxingcpp peut lever diverses exceptions selon la version ;
            # on les encapsule pour ne pas laisser fuiter de détail
            # d'implémentation au consommateur.
            raise ScanError(f"Échec de la détection zxingcpp : {exc}") from exc

        return [
            RawQr(
                text=r.text,
                position=r.position,
                format=r.format.name,
                ec_level=getattr(r, "ec_level", None),
            )
            for r in results
            if r.valid
        ]


# ======================================================================
#             Point d'entrée rapide pour tests manuels
# ======================================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage : python qr_scan.py <chemin_image>")
        sys.exit(1)

    scanner = ImageScanner()
    try:
        qrs = scanner.scan(sys.argv[1])
    except ScanError as exc:
        print(f"[ScanError] {exc}")
        sys.exit(1)

    print(f"{len(qrs)} QR code(s) détecté(s).")
    for i, qr in enumerate(qrs, 1):
        print(f"  [{i:02d}] format={qr.format}  ec={qr.ec_level}  "
              f"center_y={qr.center_y:.1f}  left_x={qr.left_x:.1f}")
        print(f"       text (brut) = {qr.text!r}")
