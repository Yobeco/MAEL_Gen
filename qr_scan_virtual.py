"""
qr_scan_virtual.py — Scanner virtuel pour les tests de développement.

Ce module fournit une implémentation concrète de `QrScanner` qui ne lit
aucune source réelle : elle simule une caméra scannant **un seul code
QR à la fois**, en piochant dans une liste de textes obfusqués.

Rôle dans l'écosystème :

    VirtualScanner.scan() ──► list[RawQr] ──► qr_parse.parse_all()

Contrat public
--------------
  - Classe `VirtualScanner(QrScanner)` : respecte strictement le
    contrat de `qr_scan.QrScanner`.
  - Aucune I/O : ne lit ni fichier, ni caméra.
  - N'échoue jamais *naturellement* ; peut échouer *à la demande* via
    `error_to_raise` (mode permanent) ou `queue_error(exc)` (ponctuel).

Cycle de vie
------------
  - À l'init : mélange de la liste une fois, ordre figé.
  - Chaque `scan()` consomme le prochain texte de l'ordre.
  - Quand la liste est épuisée, `scan()` renvoie `[]`.
  - `reset()` remet le cycle à zéro (re-mélange avec le même seed).

Reproductibilité
----------------
  - `VirtualScanner(seed=None)` → aléatoire à chaque instanciation.
  - `VirtualScanner(seed=42)`  → séquence identique à chaque exécution.

Limites assumées (V1)
---------------------
  - Un seul QR par appel : ne teste pas le tri spatial de qr_parse.
  - Position constante : ne teste pas la variabilité géométrique.
  - Les textes par défaut n'exercent ni les modes `#d`/`#e`/`gd`, ni le
    préfixe langue `<xxXXX>` (tous produisent `mode="lire"`). Passer
    `texts=` pour couvrir ces cas.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from qr_dto import RawQr
from qr_scan import QrScanner, ScanError


# ======================================================================
#            Types privés de position factice (Option B de Q1)
# ======================================================================
# Ces types ne vivent que dans ce module. Ils satisfont le duck typing
# attendu par RawQr (attributs top_left, bottom_left, etc. avec .x/.y).
# Toute autre source de RawQr devra fournir sa propre normalisation.

@dataclass(frozen=True, slots=True)
class _Corner:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class _Position:
    top_left: _Corner
    top_right: _Corner
    bottom_right: _Corner
    bottom_left: _Corner


# Position constante : QR carré de 100×100 px, coin haut-gauche en (0, 0).
# center_y = 50.0, height = 100.0, left_x = 0.0 (cf. propriétés de RawQr).
_CONST_POSITION = _Position(
    top_left=_Corner(0.0, 0.0),
    top_right=_Corner(100.0, 0.0),
    bottom_right=_Corner(100.0, 100.0),
    bottom_left=_Corner(0.0, 100.0),
)


# ======================================================================
#          Textes obfusqués par défaut (constante de module)
# ======================================================================
# Ces chaînes sont les versions obfusquées de phrases françaises
# naturelles (voir les commentaires). Elles n'exercent pas les modes
# #d/#e/gd ni les préfixes langue : voir la limite assumée en tête.
_DEFAULT_OBFUSCATED_TEXTS: tuple[str, ...] = (
    '!ep!mup!pvD"fonf!vuvdp',       # Coucou tout le monde !
    "!féêtmb!È@twm!f!wb",           # Ça va les élèves ?
    "gwmŔáfub!V/j!j!!sïno",         # Un maître à œil vif.
    "/vt!vqfõeêêufDtjÇsp!ms!u!ü(",   # C’eût été drôle pour Æsius.
    "fïfVm!o",                      # Une île
    "ìOmp",                         # Noël
    "tb!Eðnv",                      # Du maïs
    "/vbb!!sgufpj!FbhoNáup!t!òom",  # El niño est fort à Managua.
    "gœv",                          # Œuf
    "sniÊféêq",                     # Éphémère
    "eèGfbb",                       # Façade
    "sÃfu",                         # Âtre
    "/eègb!esnf!sodfu(!oeufgŔm-ìOÁfbb!mf!ü!mfup!sãmtb!t!v(!mp!",  # À Noël, l'œuf est dans l'âtre contre le mûr de la façade.
)


# ======================================================================
#                       La classe VirtualScanner
# ======================================================================
class VirtualScanner(QrScanner):
    """
    Scanner virtuel : simule une caméra qui scanne un seul QR à la fois.

    Chaque appel à `scan()` consomme le prochain texte de la liste
    (ordre figé à l'init, mélangé avec `random.Random(seed)`). Une fois
    la liste épuisée, `scan()` retourne `[]`.

    Exemples
    --------
    >>> s = VirtualScanner(seed=42)
    >>> len(s.scan())          # 1 tant qu'il reste des textes
    1
    >>> s.scan()               # épuisé après len(_DEFAULT_OBFUSCATED_TEXTS) appels
    []

    >>> s = VirtualScanner(error_to_raise=ScanError("caméra absente"))
    >>> s.scan()               # lève ScanError à chaque appel
    Traceback (most recent call last):
        ...
    qr_scan.ScanError: caméra absente
    """

    def __init__(
        self,
        seed: int | None = None,
        texts: tuple[str, ...] | None = None,
        *,
        error_to_raise: ScanError | None = None,
    ) -> None:
        """
        Paramètres
        ----------
        seed : int | None
            Graine du tirage. `None` → aléatoire ; un entier → séquence
            reproductible entre exécutions.
        texts : tuple[str, ...] | None
            Liste de textes **obfusqués** à utiliser. `None` → liste par
            défaut (`_DEFAULT_OBFUSCATED_TEXTS`). Permet d'injecter des
            cas ciblés (`#d`, `#e`, `/gd/`, `<xxXXX>`…).
        error_to_raise : ScanError | None
            Mode **permanent** d'erreur : chaque `scan()` lève cette
            exception. `None` → comportement nominal.
        """
        self._seed = seed
        self._source_texts: tuple[str, ...] = (
            texts if texts is not None else _DEFAULT_OBFUSCATED_TEXTS
        )
        self._error_to_raise = error_to_raise
        self._pending_errors: list[ScanError] = []

        # Cycle : mélange une fois, ordre figé, curseur d'épuisement.
        self._order: list[str] = []
        self._cursor: int = 0
        self._shuffle_order()

    # ------------------------------------------------------------------
    #                     API publique du contrat
    # ------------------------------------------------------------------
    def scan(self, source: object = None) -> list[RawQr]:
        """
        Retourne la liste `[RawQr]` (0 ou 1 élément) simulée.

        Paramètres
        ----------
        source : object
            Ignoré. Présent uniquement pour satisfaire le contrat
            `QrScanner.scan()`. Valeur par défaut `None` pour permettre
            l'appel sans argument dans les tests.

        Retour
        ------
        list[RawQr]
            - `[raw]` s'il reste un texte à consommer ;
            - `[]` si le cycle est épuisé.

        Lève
        ----
        ScanError
            - si `error_to_raise` est défini (mode permanent) ;
            - si une erreur ponctuelle a été injectée via `queue_error`.
        """
        # 1. Mode permanent d'erreur (priorité absolue).
        if self._error_to_raise is not None:
            raise self._error_to_raise

        # 2. Erreur ponctuelle en attente.
        if self._pending_errors:
            raise self._pending_errors.pop(0)

        # 3. Cas nominal : cycle épuisé → liste vide.
        if self._cursor >= len(self._order):
            return []

        # 4. Cas nominal : consomme le prochain texte.
        text = self._order[self._cursor]
        self._cursor += 1
        return [self._make_raw(text)]

    # ------------------------------------------------------------------
    #                   Méthodes utilitaires de test
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Réinitialise le cycle et vide la file d'erreurs ponctuelles.

        - L'ordre de la liste est re-mélangé avec le **même** `seed`
          d'origine (si `seed=None`, le re-mélange est aléatoire).
        - Les erreurs injectées via `queue_error` sont oubliées.
        - `error_to_raise` (mode permanent d'init) n'est **pas** modifié.
        """
        self._pending_errors.clear()
        self._shuffle_order()

    def queue_error(self, exc: ScanError) -> None:
        """
        Programme une `ScanError` ponctuelle, levée au prochain `scan()`
        (FIFO si plusieurs erreurs sont empilées).

        Paramètres
        ----------
        exc : ScanError
            L'exception à lever. Levée telle quelle (non copiée).
        """
        if not isinstance(exc, ScanError):
            raise TypeError(
                f"queue_error attend une ScanError, reçu {type(exc).__name__}"
            )
        self._pending_errors.append(exc)

    # ------------------------------------------------------------------
    #                    Fabrique de RawQr simulés
    # ------------------------------------------------------------------
    def _make_raw(self, text: str) -> RawQr:
        """Construit un `RawQr` simulé à partir d'un texte obfusqué."""
        return RawQr(
            text=text,
            position=_CONST_POSITION,
            format="QRCode",
            ec_level="M",
        )

    # ------------------------------------------------------------------
    #                 Gestion interne de l'ordre du cycle
    # ------------------------------------------------------------------
    def _shuffle_order(self) -> None:
        """
        (Re)construit `self._order` en mélangeant `self._source_texts`
        avec un `random.Random` réinitialisé au seed d'origine.
        """
        rng = random.Random(self._seed)
        order = list(self._source_texts)
        rng.shuffle(order)
        self._order = order
        self._cursor = 0


# ======================================================================
#             Point d'entrée rapide pour tests manuels
# ======================================================================
if __name__ == "__main__":
    from qr_parse import parse_all

    print("=== Cycle épuisable avec seed=42 ===")
    scanner = VirtualScanner(seed=42)
    n = 0
    while True:
        raws = scanner.scan()
        if not raws:
            break
        n += 1
        items = parse_all(raws)
        item = items[0]
        print(f"  [{n:02d}] mode={item.mode!r} lang={item.lang!r} "
              f"text={item.text!r}")

    print(f"\nCycle épuisé après {n} scans. "
          f"(attendu : {len(_DEFAULT_OBFUSCATED_TEXTS)})")

    print("\n=== Même seed → même séquence (vérification) ===")
    s1 = VirtualScanner(seed=42)
    s2 = VirtualScanner(seed=42)
    seq1 = [s1.scan()[0].text for _ in range(3)]
    seq2 = [s2.scan()[0].text for _ in range(3)]
    print(f"  s1 : {seq1}")
    print(f"  s2 : {seq2}")
    print(f"  identiques : {seq1 == seq2}")

    print("\n=== reset() remet le cycle à zéro ===")
    s = VirtualScanner(seed=42)
    first_before = s.scan()[0].text
    s.scan()
    s.scan()
    s.reset()
    first_after = s.scan()[0].text
    print(f"  avant reset : {first_before!r}")
    print(f"  après reset : {first_after!r}")
    print(f"  identiques  : {first_before == first_after}")

    print("\n=== Injection ponctuelle de ScanError ===")
    s = VirtualScanner(seed=42)
    s.queue_error(ScanError("caméra débranchée"))
    try:
        s.scan()
    except ScanError as exc:
        print(f"  ScanError attrapée : {exc}")
    print(f"  scan suivant OK   : {s.scan()[0].text!r}")

    print("\n=== Mode permanent d'erreur ===")
    s = VirtualScanner(error_to_raise=ScanError("caméra absente"))
    for _ in range(2):
        try:
            s.scan()
        except ScanError as exc:
            print(f"  ScanError attrapée : {exc}")

    print("\n=== Cas texts= personnalisé (mode dicter) ===")
    from MAEL_obfus import Obfus
    obf = Obfus()
    custom = (obf.enobfus("Bonjour le monde#d"),)
    s = VirtualScanner(texts=custom)
    item = parse_all(s.scan())[0]
    print(f"  mode={item.mode!r} lang={item.lang!r} text={item.text!r}")
    print("")
    print("-#" * 50)
    print("")
