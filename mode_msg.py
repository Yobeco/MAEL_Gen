# -*- coding: utf-8 -*-
"""
mode_msg.py
===========

Traductions des **messages courts** affichés à l'écran par la couche
``TtsSetupBuilder``.

Les clés internes (``"Mode cacher"``, ``"Mode dicter"``, ``"Mode Epeler"``,
``"Mode épeler indisponible"``, ``"Mode épeler émojis"``) sont consommées
par la fonction utilitaire :func:`get_mode_message` (mode, langue) qui
renvoie le texte traduit, avec un repli français en cas de langue ou
de clé inconnue.

Conventions
-----------

* Les clés de premier niveau sont des codes langue courts ISO 639-1
  (deux lettres minuscules, par ex. ``"fr"``, ``"es"``). Cela reste
  aligné avec la résolution de langue effectuée par ``TtsSetupBuilder``
  (clé racine ``"fr"``, ``"es"``, etc.).
* Les langues non couvertes retombent toujours sur le français.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Mapping des noms de langue « humain » -> code court 2 lettres.
# Utile pour rebrancher facilement un texte d'origine en clair.
# ----------------------------------------------------------------------
_LANG_NAMES = {
    "Français": "fr",
    "Espagnol": "es",
    "Anglais": "en",
    "Portugais": "pt",
    "Allemand": "de",
    "Italien": "it",
}

# ----------------------------------------------------------------------
# Table des traductions
# ----------------------------------------------------------------------
# On distingue trois familles de clés :
#   * ``"Mode cacher"`` / ``"Mode dicter"`` / ``"Mode Epeler"`` :
#     messages de succès affichés à l'écran lors du lancement de
#     chaque mode (équivalent de « Écoute bien. »).
#   * ``"Mode epeler non implemente"`` : message d'erreur pour les
#     langues dont le dictionnaire ``epel_tts_xx`` est absent
#     (coréen, japonais, chinois, russe, grec...).
#   * ``"Mode epeler emoji"`` : message d'erreur lorsqu'un caractère
#     du payload relève d'une séquence émoji (ZWJ, sélecteurs de
#     teint, indicateurs régionaux, etc.).
# ----------------------------------------------------------------------
traductions = {
    "fr": {
        # Messages de succès
        "Mode cacher": "Écoute bien.",
        "Mode dicter": "Écris la dictée.",
        "Mode Epeler": "Écoute les lettres.",
        # Messages d'erreur spécifiques au mode épeler
        "Mode epeler non implemente":
            "Mode épeler pas encore implémenté dans cette langue",
        "Mode epeler emoji":
            "MAEL ne traite pas les émojis",
    },
    "es": {
        "Mode cacher": "Escucha bien.",
        "Mode dicter": "Escribe el dictado.",
        "Mode Epeler": "Escucha las letras.",
        "Mode epeler non implemente":
            "Modo deletrear aún no implementado en este idioma",
        "Mode epeler emoji":
            "MAEL no procesa los emojis",
    },
    "en": {
        "Mode cacher": "Listen carefully.",
        "Mode dicter": "Write down the dictation.",
        "Mode Epeler": "Listen to the letters.",
        "Mode epeler non implemente":
            "Spelling mode not yet implemented in this language",
        "Mode epeler emoji":
            "MAEL does not process emojis",
    },
    "pt": {
        "Mode cacher": "Escuta bem.",
        "Mode dicter": "Escreve o ditado.",
        "Mode Epeler": "Escuta as letras.",
        "Mode epeler non implemente":
            "Modo soletrar ainda não implementado neste idioma",
        "Mode epeler emoji":
            "O MAEL não processa emojis",
    },
    "de": {
        "Mode cacher": "Hör gut zu.",
        "Mode dicter": "Schreib das Diktat auf.",
        "Mode Epeler": "Hör dir die Buchstaben an.",
        "Mode epeler non implemente":
            "Buchstabiermodus in dieser Sprache noch nicht implementiert",
        "Mode epeler emoji":
            "MAEL verarbeitet keine Emojis",
    },
    "it": {
        "Mode cacher": "Ascolta bene.",
        "Mode dicter": "Scrivi il dettato.",
        "Mode Epeler": "Ascolta le lettere.",
        "Mode epeler non implemente":
            "Modalità spelling non ancora implementata in questa lingua",
        "Mode epeler emoji":
            "MAEL non gestisce le emoji",
    },
}


def get_mode_message(mode_key: str, lang: str | None) -> str:
    """
    Retourne le message localisé associé à ``mode_key`` pour la langue ``lang``.

    Paramètres
    ----------
    mode_key : str
        Clé interne du message, par ex. ``"Mode cacher"``,
        ``"Mode dicter"``, ``"Mode Epeler"``, ``"Mode epeler non
        implemente"`` ou ``"Mode epeler emoji"``.
    lang : str | None
        Code langue ou variante (par ex. ``"fr"``, ``"frCH"``,
        ``"es"``). La fonction normalise en extrayant les deux
        premières lettres en minuscules.

    Retour
    ------
    str
        Le texte traduit. Si la langue ou la clé est absente du
        dictionnaire, repli sur le français (``"fr"``).
    """
    # Langue absente ou None : repli direct.
    if not lang:
        lang_short = "fr"
    else:
        # ``"frCH"`` -> ``"fr"``, ``"EN"`` -> ``"en"``, ``"es"`` -> ``"es"``.
        lang_short = lang[:2].lower() if len(lang) >= 2 else lang.lower()

    # Recherche dans la langue demandée, sinon repli français.
    table = traductions.get(lang_short, traductions.get("fr", {}))
    if mode_key in table:
        return table[mode_key]

    # Repli français global.
    fallback = traductions.get("fr", {})
    if mode_key in fallback:
        return fallback[mode_key]

    # Dernier recours : on retourne la clé brute plutôt que None.
    return mode_key
