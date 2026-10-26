"""
qr_parse.py — Analyse sémantique des codes QR.

Ce module a **une seule responsabilité** : transformer une liste de
`RawQr` (observations physiques brutes, encore obfusquées) en une liste
de `TtsItem` (objets métier enrichis : texte clair, langue, mode).

Rôle dans l'écosystème :

    qr_scan  ──produit──►  list[RawQr]  ──consommé par──►  qr_parse
                                                             (ce module)
    qr_parse ──produit──►  list[TtsItem] ──consommé par──►  MAEL_Verif_PDF

Ce module est totalement **indépendant du hardware** : il n'importe ni
zxingcpp, ni OpenCV, ni numpy. Il ne voit jamais une image. Il ne sait
pas d'où viennent les `RawQr` qu'il reçoit.

Pipeline d'analyse (par QR) :
  1. Déobfuscation du texte brut (via MAEL_obfus).
  2. Extraction du préfixe /gd/ (Google Drive) s'il est présent.
  3. Extraction du suffixe #d / #e (mode dicter / épeler) s'il est présent.
  4. Extraction du préfixe <xxXXX> (langue) s'il est présent.
  5. Nettoyage du texte : retrait du préfixe et du suffixe.
  6. Construction d'un TtsItem.

Après analyse, tous les QR sont triés dans l'ordre naturel de lecture :
de haut en bas (regroupement en lignes), puis de gauche à droite dans
chaque ligne.

Règles d'extraction (par ordre de priorité) :
  1. Préfixe /gd/ :
        mode = "gd", lang = None
        texte = ID pur (le /gd/ retiré, et tout suffixe #d/#e retiré)
  2. Suffixe #d / #e / #c (sans /gd/) :
        mode = "dicter", "epeler" ou "cacher"
        texte = texte sans le suffixe, et sans le préfixe <xxXXX> éventuel
        lang = code du préfixe s'il existe, sinon LANG_DEFAULT
  3. Préfixe <xxXXX> seul :
        mode = "lire", lang = code extrait
        texte = texte sans le préfixe
  4. Aucun préfixe, aucun suffixe :
        mode = "lire", lang = LANG_DEFAULT, texte inchangé
"""

from __future__ import annotations

from qr_dto import (
    RawQr,
    TtsItem,
    CloudItem,
    WifiItem,
)

from MAEL_obfus import Obfus


# Modes du domaine — définis ici pour que qr_dto reste limité aux DTO.
MODE_LIRE = "lire"
MODE_DICTER = "dicter"
MODE_EPELER = "epeler"
MODE_CACHER = "cacher"
MODE_GD = "gd"
MODE_NC = "nc"
MODE_LS = "ls"
MODE_WIFI = "wifi"
# Langue par defaut utilisee quand aucun prefixe <xxXXX> n'est detecte.
# On utilise le code court "fr" (cle racine du dictionnaire lang_tts)
# pour rester aligne avec la resolution de langue de TtsSetupBuilder.
LANG_DEFAULT = "fr"
MODES_CLOUD = (MODE_GD, MODE_NC, MODE_LS)


# ======================================================================
# Constantes de parsing — règles internes d'extraction
# ======================================================================
# Ces constantes décrivent COMMENT on extrait le sens d'un texte brut.
# Elles ne font pas partie du contrat public (contrairement aux MODE_*
# qui définissent les valeurs légitimes du champ `mode` de TtsItem).

# Préfixe Google Drive
GD_PREFIX = "/gd/"
CLOUD_PREFIXES = {
    "gd": (MODE_GD, "♫ Google Drive"),
    "nc": (MODE_NC, "♫ NextCloud"),
    "ls": (MODE_LS, "♫ La Suite"),
}

# Suffixes de mode
SUFFIX_DICTER = "#d"
SUFFIX_EPELER = "#e"
SUFFIX_CACHER = "#c"

# Paramètre du tri naturel : tolérance verticale relative à la hauteur
# d'un QR pour considérer que deux QR appartiennent à la même ligne.
ROW_TOLERANCE_RATIO = 0.5


# ======================================================================
# Obfuscateur — instance unique, sans état
# ======================================================================
# La classe Obfus est sans attribut d'instance : un singleton module est
# suffisant et évite de recréer un objet à chaque appel.
_obfusor = Obfus()


# ======================================================================
# Extraction du préfixe langue <xxXXX>
# ======================================================================
def _extract_lang(text: str) -> tuple[str | None, str]:
    """
    Détecte un préfixe <xxXXX> en début de chaîne.

    Retourne (lang, texte_sans_préfixe). Si aucun préfixe n'est trouvé,
    retourne (None, text).
    """
    if not text.startswith("<"):
        return None, text
    end = text.find(">")
    if end == -1:
        return None, text
    return text[1:end], text[end + 1:]


# ======================================================================
# Extraction du suffixe mode #d / #e
# ======================================================================
def _strip_suffix(text: str) -> tuple[str | None, str]:
    """
    Détecte un suffixe #d / #e / #c en fin de chaîne.

    Retourne (mode_ou_None, texte_sans_suffixe).
    """
    if text.endswith(SUFFIX_DICTER):
        return MODE_DICTER, text[: -len(SUFFIX_DICTER)]
    if text.endswith(SUFFIX_EPELER):
        return MODE_EPELER, text[: -len(SUFFIX_EPELER)]
    if text.endswith(SUFFIX_CACHER):
        return MODE_CACHER, text[: -len(SUFFIX_CACHER)]
    return None, text


def _split_wifi_fields(body: str) -> list[str]:
    """Sépare les champs WIFI en respectant les échappements."""
    fields: list[str] = []
    current: list[str] = []
    escaped = False
    for char in body:
        if escaped:
            current.extend(("\\", char))
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == ";":
            fields.append("".join(current))
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    if current:
        fields.append("".join(current))
    return fields


def _split_wifi_key_value(field_text: str) -> tuple[str, str] | None:
    """Extrait une paire WIFI clé/valeur, avec séparateur échappable."""
    escaped = False
    for index, char in enumerate(field_text):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == ":":
            return field_text[:index], field_text[index + 1:]
    return None


def _unescape_wifi(value: str) -> str:
    """Déséchappe les caractères réservés du format WIFI."""
    result: list[str] = []
    escaped = False
    for char in value:
        if escaped:
            if char in ";:\\\\,":
                result.append(char)
            else:
                result.extend(("\\", char))
            escaped = False
        elif char == "\\":
            escaped = True
        else:
            result.append(char)
    if escaped:
        result.append("\\")
    return "".join(result)


def _parse_wifi(decrypted: str, raw: RawQr) -> WifiItem | None:
    """Analyse un QR WIFI, sans jamais inclure le mot de passe dans les logs."""
    if not decrypted.startswith("WIFI:"):
        return None
    fields: dict[str, str] = {}
    for field_text in _split_wifi_fields(decrypted[5:]):
        if not field_text:
            continue
        pair = _split_wifi_key_value(field_text)
        if pair is None:
            raise ValueError("format WIFI invalide")
        key, value = pair
        fields[key] = _unescape_wifi(value)

    if "S" not in fields:
        raise ValueError("QR WIFI sans SSID")

    password = fields.get("P", "")
    wifi_type = fields.get("T", "nopass" if not password else "")
    hidden = fields.get("H", "false").lower() == "true"
    return WifiItem(raw, MODE_WIFI, wifi_type, fields["S"], password, hidden)


def _parse_cloud(decrypted: str, raw: RawQr) -> CloudItem | None:
    """Analyse un identifiant opaque de service cloud."""
    if not decrypted.startswith("/"):
        return None
    parts = decrypted.split("/", 2)
    if len(parts) != 3 or parts[1] not in CLOUD_PREFIXES or not parts[2]:
        return None
    mode, label = CLOUD_PREFIXES[parts[1]]
    return CloudItem(raw, mode, parts[2], label)


# ======================================================================
# Analyse sémantique d'un texte déobfusqué
# ======================================================================
def _parse_decrypted(decrypted: str) -> tuple[str, str | None, str, str]:
    """
    Analyse un texte déobfusqué et retourne :
        (texte, lang, mode, original)

    - texte    : contenu nettoyé (préfixe et suffixe retirés)
    - lang     : code langue (LANG_DEFAULT par défaut), ou None si mode GD
    - mode     : MODE_LIRE, MODE_DICTER, MODE_EPELER, MODE_CACHER ou MODE_GD
    - original : texte déobfusqué inchangé (avant tout retrait)
    """
    original = decrypted

    # --- Cas 1 : préfixe /gd/ -----------------------------------------
    if decrypted.startswith(GD_PREFIX):
        body = decrypted[len(GD_PREFIX):]
        # On retire aussi tout suffixe #d/#e résiduel (un ID Google
        # Drive ne peut pas contenir '#').
        _suffix_mode, body = _strip_suffix(body)
        return body, None, MODE_GD, original

    # --- Cas 2 & 3 : suffixe #d/#e éventuel ---------------------------
    suffix_mode, body = _strip_suffix(decrypted)

    # --- Extraction du préfixe <xxXXX> --------------------------------
    lang, body = _extract_lang(body)

    if suffix_mode is not None:
        # Cas 2 : suffixe présent → mode = dicter/epeler
        if lang is None:
            lang = LANG_DEFAULT
        return body, lang, suffix_mode, original

    # Cas 3 : préfixe seul, ou cas 4 : rien
    if lang is None:
        lang = LANG_DEFAULT
    return body, lang, MODE_LIRE, original


# ======================================================================
# Tri naturel des QR codes (de haut en bas, puis de gauche à droite)
# ======================================================================
def _sort_qr_items(items: list[TtsItem | CloudItem | WifiItem]) -> list[TtsItem | CloudItem | WifiItem]:
    """
    Trie les TtsItem dans l'ordre naturel de lecture :
      - de haut en bas (regroupement en lignes selon ROW_TOLERANCE_RATIO),
      - puis de gauche à droite à l'intérieur de chaque ligne.

    Le tri s'appuie sur les propriétés géométriques exposées par RawQr
    (`center_y`, `height`, `left_x`), accessibles via `item.raw`.
    """
    if len(items) <= 1:
        return list(items)

    by_y = sorted(items, key=lambda it: it.raw.center_y)

    rows: list[list[TtsItem | CloudItem | WifiItem]] = []
    current_row: list[TtsItem | CloudItem | WifiItem] = [by_y[0]]
    current_center_y = by_y[0].raw.center_y
    current_height = by_y[0].raw.height

    for item in by_y[1:]:
        item_center_y = item.raw.center_y
        item_height = item.raw.height
        tolerance = max(current_height, item_height) * ROW_TOLERANCE_RATIO

        if abs(item_center_y - current_center_y) <= tolerance:
            current_row.append(item)
            current_height = max(current_height, item_height)
        else:
            rows.append(current_row)
            current_row = [item]
            current_center_y = item_center_y
            current_height = item_height

    rows.append(current_row)

    sorted_items: list[TtsItem | CloudItem | WifiItem] = []
    for row in rows:
        row_sorted = sorted(row, key=lambda it: it.raw.left_x)
        sorted_items.extend(row_sorted)

    return sorted_items


# ======================================================================
# API publique
# ======================================================================
def parse_all(raws: list[RawQr]) -> list[TtsItem | CloudItem | WifiItem]:
    """
    Analyse une liste de `RawQr` et retourne la liste des `TtsItem`
    correspondants, triés dans l'ordre naturel de lecture.

    Paramètres
    ----------
    raws : list[RawQr]
        Liste d'observations brutes produites par un scanner (par
        exemple `qr_scan.ImageScanner`). Peut être vide.

    Retour
    ------
    list[TtsItem]
        Liste de même longueur que `raws` (sauf cas exceptionnel :
        aucun filtrage n'est effectué ici). Triée par position.
        Retourne `[]` si `raws` est vide.

    Notes
    -----
    Cette fonction est pure : elle ne modifie pas les `RawQr` reçus et
    ne produit aucun effet de bord. Un appel répété avec les mêmes
    entrées produit les mêmes sorties.
    """
    if not raws:
        return []

    items: list[TtsItem | CloudItem | WifiItem] = []

    for raw in raws:
        # Les QR WIFI sont des QR standard en clair : ne pas les déobfusquer.
        if raw.text.startswith("WIFI:"):
            items.append(_parse_wifi(raw.text, raw))
            continue

        decrypted = _obfusor.deobfus(raw.text) or ""
        cloud_item = _parse_cloud(decrypted, raw)
        if cloud_item is not None:
            items.append(cloud_item)
            continue

        text, lang, mode, original = _parse_decrypted(decrypted)
        items.append(TtsItem(raw=raw, original=original, text=text, lang=lang, mode=mode))

    return _sort_qr_items(items)


# ======================================================================
# Point d'entrée rapide pour tests manuels
# ======================================================================
if __name__ == "__main__":
    import sys
    from qr_scan import ImageScanner, ScanError

    if len(sys.argv) < 2:
        print("Usage : python qr_parse.py <chemin_image>")
        sys.exit(1)

    scanner = ImageScanner()
    try:
        raws = scanner.scan(sys.argv[1])
    except ScanError as exc:
        print(f"[ScanError] {exc}")
        sys.exit(1)

    print(f"{len(raws)} QR code(s) brut(s) détecté(s).")

    items = parse_all(raws)
    print(f"{len(items)} élément(s) produit(s) après analyse.\n")

    for i, item in enumerate(items, 1):
        print(f"  [{i:02d}] mode={item.mode!r}  lang={item.lang!r}")
        print(f"       original = {item.original!r}")
        print(f"       text     = {item.text!r}")
        print(f"       position = center_y={item.raw.center_y:.1f}  "
              f"left_x={item.raw.left_x:.1f}")
        print()
