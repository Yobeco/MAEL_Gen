# -*- coding: utf-8 -*-
"""
qr_scan_virtual.py
==================

Simulateur de scanneur de codes QR.

But
---
Fournir une liste ``_DEFAULT_OBFUSCATED_TEXTS`` qui reproduit le
contenu *tel qu'il sortirait d'un vrai scanneur* : autrement dit,
des chaînes **déjà obfusquées** par ``MAEL_obfus``.

À partir de la donnée brute ``test_list.strings_to_obfus`` (les
contenus *en clair* qu'on voudrait voir apparaître dans un QR),
on applique la transformation ``Obfus().enobfus`` à chaque entrée.
Le résultat simule ce que le déobfuscateur du pipeline retrouvera
plus tard via ``qr_parse``.

Note importante
---------------
Le module ``test_list`` est volontairement importé ici : il ne
contient aucune dépendance et n'introduit donc aucun cycle
d'imports (les modules métier — ``MAEL_obfus``, ``qr_parse``,
``tts_setup`` — ne dépendent pas de ``test_list``).
"""

from __future__ import annotations

import MAEL_obfus
import test_list


# On fabrique une seule fois la liste obfusquée, au chargement.
_obfusor = MAEL_obfus.Obfus()

_DEFAULT_OBFUSCATED_TEXTS: list[str] = [
    _obfusor.enobfus(s) for s in test_list.strings_to_obfus
]


__all__ = ["_DEFAULT_OBFUSCATED_TEXTS"]
