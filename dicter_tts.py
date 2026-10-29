# -*- coding: utf-8 -*-
"""
dicter_tts.py — Découpage du texte en groupes de souffle (GDS).

La segmentation est indépendante des dictionnaires de prononciation :
les mots composés connus sont d'abord reconnus, puis les mots et les
signes sont extraits sans normaliser leur casse ni leur graphie.
"""

from __future__ import annotations

import re


#: Locutions reconnues comme un seul groupe de souffle, par langue de référence.
COMPOSES_PAR_LANGUE: dict[str, tuple[str, ...]] = {
    "fr": (
        "au fur et à mesure",
        "à moins que",
        "à cause de",
        "au-dessus de",
        "en face de",
        "tout de suite",
        "ainsi que",
        "alors que",
        "après que",
        "attendu que",
        "aussitôt que",
        "autant que",
        "avant que",
        "bien que",
        "cependant que",
        "dès que",
        "de même que",
        "de sorte que",
        "depuis que",
        "grâce à",
        "parce que",
        "pendant que",
        "pourvu que",
        "selon que",
        "si bien que",
        "tant que",
        "tandis que",
        "vu que",
        "en effet",
        "peu à peu",
        "de temps en temps",
    ),
}

# Les lettres incluent les marques diacritiques combinantes. L'apostrophe
# ou le trait d'union n'est incorporé au mot que lorsqu'il est interne.
_MOT = r"[\w\u0300-\u036f]+(?:['’ʼ][\w\u0300-\u036f]+)*(?:[-‐‑][\w\u0300-\u036f]+(?:['’ʼ][\w\u0300-\u036f]+)*)*"
_TOKEN_RE = re.compile(rf"{_MOT}|…|\.{{3,}}|[^\w\s]", re.UNICODE)


def _tokens(texte: str) -> list[str]:
    """Renvoie les tokens complets (sans exposer les groupes internes)."""
    return [match.group(0) for match in _TOKEN_RE.finditer(texte)]


def decouper_gds(texte: str, langue: str = "fr") -> tuple[str, ...]:
    """Découpe ``texte`` en mots composés, mots et signes isolés.

    Les espaces ne produisent pas de GDS. L'apostrophe et les traits
    d'union internes restent dans le mot ; la ponctuation isolée forme
    un GDS. Les locutions de ``COMPOSES_PAR_LANGUE`` sont appariées sans
    tenir compte de la casse et leur graphie originale est conservée.

    Args:
        texte: Texte à segmenter.
        langue: Clé de langue, éventuellement régionale (ex. ``frCA``).

    Returns:
        Tuple immuable des groupes dans leur ordre d'apparition.
    """
    if not texte:
        return ()

    langue_ref = langue[:2].lower() if langue else "fr"
    composes = COMPOSES_PAR_LANGUE.get(langue_ref, ())
    if not composes:
        return tuple(_tokens(texte))

    alternatives = sorted(composes, key=len, reverse=True)
    morceaux = [re.escape(mot).replace(r"\ ", r"\s+") for mot in alternatives]
    compose_re = re.compile(
        rf"(?<!\w)(?:{'|'.join(morceaux)})(?!\w)", re.IGNORECASE | re.UNICODE
    )

    resultat: list[str] = []
    debut = 0
    for match in compose_re.finditer(texte):
        resultat.extend(_tokens(texte[debut:match.start()]))
        resultat.append(match.group(0))
        debut = match.end()
    resultat.extend(_tokens(texte[debut:]))
    return tuple(resultat)


# Alias anglais conservé pour faciliter l'intégration éventuelle avec
# d'autres modules Python du projet.
split_gds = decouper_gds
