# -*- coding: utf-8 -*-
"""
test_tts_setup.py
=================

Suite de tests unitaires (unittest, Python 3.13) pour la couche
``TtsSetupBuilder`` et les fonctions associées (``get_mode_message``,
suffixes du parseur QR, constantes).

Objectifs couverts
------------------

* Mode ``lire`` :
    - français / espagnol / anglais ;
    - variante régionale ``frCH`` avec repli automatique vers ``fr`` ;
    - repli vers la langue de référence avec ``logging.warning`` ;
    - langue totalement inconnue : ``to_show`` court, ``to_pronounce`` vide
      et message d'avertissement console.

* Mode ``cacher`` :
    - français -> ``"Écoute bien."`` ;
    - espagnol -> ``"Escucha bien."`` ;
    - langue sans message (ex. ``ko``) -> repli français ;
    - langue inconnue -> l'erreur l'emporte (``to_pronounce`` vide).

* Mode ``epeler`` :
    - français « Ça » -> tuple épelé attendu ;
    - chiffres ``"12"`` en français et anglais ;
    - variante régionale ``frCH`` -> repli vers ``epel_tts_fr`` ;
    - caractère ``""`` (ex. ``\\u200b``) conservé tel quel ;
    - dictionnaire absent (``ko``) -> message d'erreur localisé ;
    - émoji -> message « MAEL ne traite pas les émojis » ;
    - langue inconnue -> l'erreur de langue l'emporte ;
    - caractère absent du dict -> conservé tel quel.

* ``get_mode_message`` :
    - ``frCH`` -> repli français ;
    - clé absente / langue absente -> repli français.

* ``qr_parse`` : suffixe ``#c`` détecté, ``LANG_DEFAULT == 'fr'``.

Notes
-----
Les ``TtsItem`` sont construits **directement** (sans passer par la
déobfuscation MAEL), conformément à la consigne : on évite ainsi la
dépendance sur ``Obfus`` et on s'affranchit des paires clair/obfusqué
dans les fixtures.
"""

from __future__ import annotations

import logging
import os
import sys
import unittest

# Rend les modules du projet importables quand le test est lancé
# depuis n'importe quel répertoire via ``python -m unittest``.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.append(_HERE)

from qr_dto import RawQr, TtsItem                              # noqa: E402
from tts_setup import TtsSetupBuilder, MSG_MODE_NON_GERE       # noqa: E402
from mode_msg import get_mode_message                          # noqa: E402
from qr_parse import (                                         # noqa: E402
    _strip_suffix,
    SUFFIX_CACHER,
    SUFFIX_DICTER,
    SUFFIX_EPELER,
    MODE_CACHER,
    MODE_DICTER,
    MODE_EPELER,
    MODE_LIRE,
    LANG_DEFAULT,
)
import epel_tts                                                # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures : construction directe de TtsItem (pas de déobfuscation)
# ---------------------------------------------------------------------------


class _FakeCorner:
    """Coin factice pour la géométrie du QR."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class _FakePos:
    """Position factice carrée 10x10."""

    def __init__(self) -> None:
        self.top_left = _FakeCorner(0.0, 0.0)
        self.top_right = _FakeCorner(10.0, 0.0)
        self.bottom_right = _FakeCorner(10.0, 10.0)
        self.bottom_left = _FakeCorner(10.0, 10.0)


def _raw(text: str = "RAW") -> RawQr:
    """Construit un RawQr minimal mais valide."""
    return RawQr(
        text=text,
        position=_FakePos(),
        format="QRCode",
        ec_level=None,
    )


def make_item(
    text: str,
    lang: str | None,
    mode: str = MODE_LIRE,
) -> TtsItem:
    """
    Construit un TtsItem sans passer par ``qr_parse``.
    """
    return TtsItem(
        raw=_raw(text),
        original=text,
        text=text,
        lang=lang,
        mode=mode,
    )


# ---------------------------------------------------------------------------
# Helper : capture des logs du module ``tts_setup``
# ---------------------------------------------------------------------------


class _LogCapture:
    """
    Gestionnaire de contexte capturant les ``LogRecord`` émis par le
    logger ``"tts_setup"`` pendant la durée du ``with``.
    """

    def __init__(self) -> None:
        self.records: list[logging.LogRecord] = []
        self._handler: logging.Handler | None = None
        self._previous_level: int = logging.NOTSET

    def __enter__(self) -> "_LogCapture":
        logger = logging.getLogger("tts_setup")
        self._previous_level = logger.level

        outer = self

        class _ListHandler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:  # noqa: D401
                outer.records.append(record)

        self._handler = _ListHandler()
        logger.addHandler(self._handler)
        logger.setLevel(logging.WARNING)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        logger = logging.getLogger("tts_setup")
        if self._handler is not None:
            logger.removeHandler(self._handler)
        logger.setLevel(self._previous_level)

    def warnings(self) -> list[logging.LogRecord]:
        """Retourne uniquement les enregistrements de niveau WARNING."""
        return [r for r in self.records if r.levelno >= logging.WARNING]


# ---------------------------------------------------------------------------
# Tests : mode ``lire``
# ---------------------------------------------------------------------------


class TestLire(unittest.TestCase):
    """Tests du mode ``lire``."""

    def test_lire_fr(self) -> None:
        """``lire`` en français : langue résolue et texte prononçable."""
        item = make_item("Bonjour", lang="fr", mode=MODE_LIRE)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.mode, MODE_LIRE)
        self.assertEqual(setup.speed, 100)
        self.assertEqual(setup.to_pronounce, ("Bonjour",))
        self.assertEqual(setup.to_show, "Bonjour")

    def test_lire_es(self) -> None:
        """``lire`` en espagnol : code gTTS ``es`` conservé."""
        item = make_item("Hola", lang="es", mode=MODE_LIRE)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "es")
        self.assertEqual(setup.to_pronounce, ("Hola",))
        self.assertEqual(setup.to_show, "Hola")

    def test_lire_en(self) -> None:
        """``lire`` en anglais : code gTTS ``en`` conservé."""
        item = make_item("Hello", lang="en", mode=MODE_LIRE)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "en")
        self.assertEqual(setup.to_pronounce, ("Hello",))

    def test_lire_frCH_repli_vers_fr(self) -> None:
        """
        ``lire`` en ``frCH`` : la table ``lang_tts`` ne fournit qu'un
        code gTTS générique ``fr`` -> repli automatique.
        """
        item = make_item("Salut", lang="frCH", mode=MODE_LIRE)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.to_pronounce, ("Salut",))
        self.assertEqual(setup.to_show, "Salut")

    def test_lang_none_repli_fr(self) -> None:
        """``lang=None`` -> repli français par défaut."""
        item = make_item("Coucou", lang=None, mode=MODE_LIRE)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.to_pronounce, ("Coucou",))

    def test_repli_reference_avec_warning(self) -> None:
        """
        Variante régionale inconnue ``esXX`` -> repli vers ``es`` et un
        ``logging.warning`` doit être émis sur la console.
        """
        item = make_item("texto", lang="esXX", mode=MODE_LIRE)

        with _LogCapture() as cap:
            setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "es")
        self.assertGreaterEqual(len(cap.warnings()), 1)

    def test_langue_inconnue_message_court(self) -> None:
        """
        Langue totalement inconnue (``xx``) : ``to_show`` est un
        message d'erreur court (< 40 caractères), ``to_pronounce`` est
        vide, ``lang is None``, et un warning est émis en console.
        """
        item = make_item("test", lang="xx", mode=MODE_LIRE)

        with _LogCapture() as cap:
            setup = TtsSetupBuilder().build(item)

        self.assertFalse(setup.ok)
        self.assertIsNone(setup.lang)
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(setup.to_show, "Langue inconnue : xx")
        self.assertLess(len(setup.to_show), 40)
        self.assertGreaterEqual(len(cap.warnings()), 1)


# ---------------------------------------------------------------------------
# Tests : mode ``cacher``
# ---------------------------------------------------------------------------


class TestCacher(unittest.TestCase):
    """Tests du mode ``cacher``."""

    def test_cacher_fr(self) -> None:
        """``cacher`` en français -> ``to_show = "Écoute bien."``."""
        item = make_item("secret", lang="fr", mode=MODE_CACHER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.to_pronounce, ("secret",))
        self.assertEqual(setup.to_show, "Écoute bien.")

    def test_cacher_es(self) -> None:
        """``cacher`` en espagnol -> ``to_show = "Escucha bien."``."""
        item = make_item("secreto", lang="es", mode=MODE_CACHER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "es")
        self.assertEqual(setup.to_pronounce, ("secreto",))
        self.assertEqual(setup.to_show, "Escucha bien.")

    def test_cacher_ko_repli_fr(self) -> None:
        """
        ``cacher`` en coréen (``ko``) : ``ko`` est connu côté TTS
        (``lang_tts["ko"][1] == "ko"``) mais ``get_mode_message`` n'a
        aucune traduction pour cette langue -> repli français
        (``"Écoute bien."``).
        """
        item = make_item("비밀", lang="ko", mode=MODE_CACHER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "ko")
        self.assertEqual(setup.to_pronounce, ("비밀",))
        self.assertEqual(setup.to_show, "Écoute bien.")

    def test_cacher_lang_inconnue_erreur_l_emporte(self) -> None:
        """
        ``cacher`` + langue inconnue : la résolution de langue échoue
        en premier, donc ``to_pronounce`` doit être vide et ``to_show``
        doit porter le message d'erreur.
        """
        item = make_item("secret", lang="xx", mode=MODE_CACHER)
        setup = TtsSetupBuilder().build(item)

        self.assertFalse(setup.ok)
        self.assertIsNone(setup.lang)
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(setup.to_show, "Langue inconnue : xx")
        self.assertNotEqual(setup.to_show, "Écoute bien.")


# ---------------------------------------------------------------------------
# Tests : mode ``epeler``
# ---------------------------------------------------------------------------


class TestEpeler(unittest.TestCase):
    """Tests du mode ``epeler``."""

    def test_epeler_ca_en_fr(self) -> None:
        """
        ``Ça`` en français : la cédille et l'accent grave sont
        remplacés par leur lecture ; les minuscules ``a`` aussi.
        """
        item = make_item("Ça", lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        # ``"Ça"`` se décompose en deux points de code : ``C`` puis
        # ``a`` (pas de normalisation NFC/NFKC). Le dict associe donc
        # ``C`` à « c majuscule » et ``a`` à « a ».
        self.assertEqual(
            setup.to_pronounce,
            ("c cédille majuscule", "a"),
        )
        self.assertEqual(setup.to_show, "Écoute les lettres.")

    def test_epeler_chiffres_fr(self) -> None:
        """``12`` en français : ``un`` puis ``deux``."""
        item = make_item("12", lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.to_pronounce, ("un", "deux"))
        self.assertEqual(setup.to_show, "Écoute les lettres.")

    def test_epeler_chiffres_en(self) -> None:
        """``12`` en anglais : ``one`` puis ``two``."""
        item = make_item("12", lang="en", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.to_pronounce, ("one", "two"))
        self.assertEqual(setup.to_show, "Listen to the letters.")

    def test_epeler_frCH_repli_dict_fr(self) -> None:
        """
        ``frCH`` est réduit à ``fr`` par ``_get_epel_dict`` : on
        retrouve le comportement du mode épeler en français.
        """
        item = make_item("12", lang="frCH", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.to_pronounce, ("un", "deux"))
        # ``to_show`` suit la langue d'origine (``frCH`` -> ``fr``).
        self.assertEqual(setup.to_show, "Écoute les lettres.")

    def test_epeler_caractere_vide_conserve(self) -> None:
        """
        Un caractère dont la valeur dans le dict est ``""``
        (par exemple ``\\u200b`` zero-width space) doit être
        conservé tel quel dans la liste (un élément ``""``).
        """
        payload = "a" + "\u200b" + "b"  # a, ZWSP vide, b
        item = make_item(payload, lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(
            setup.to_pronounce,
            ("a", "", "b"),
        )

    def test_epeler_dict_absent_ko(self) -> None:
        """
        Pas de ``epel_tts_ko`` -> message d'erreur localisé,
        ``to_pronounce`` vide, ``to_show`` court.
        """
        item = make_item("비밀", lang="ko", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "ko")
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(
            setup.to_show,
            "Mode épeler pas encore implémenté dans cette langue",
        )
        self.assertLess(len(setup.to_show), 60)

    def test_epeler_emoji(self) -> None:
        """
        Présence d'un émoji (``U+1F600``) : message d'erreur dédié,
        ``to_pronounce`` vide.
        """
        item = make_item("a\ufe0f", lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.lang, "fr")
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(setup.to_show, "MAEL ne traite pas les émojis")

    def test_epeler_emoji_zwj(self) -> None:
        """Un ZWJ isolé suffit à déclencher le message émoji."""
        item = make_item("\u200d", lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(setup.to_show, "MAEL ne traite pas les émojis")

    def test_epeler_lang_inconnue_erreur_l_emporte(self) -> None:
        """
        Langue totalement inconnue : l'erreur de langue est
        prioritaire sur la logique d'épellation.
        """
        item = make_item("12", lang="xx", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertFalse(setup.ok)
        self.assertIsNone(setup.lang)
        self.assertEqual(setup.to_pronounce, ())
        self.assertEqual(setup.to_show, "Langue inconnue : xx")

    def test_epeler_caractere_absent_du_dict(self) -> None:
        """
        Caractère absent du dict : conservé tel quel, sans planter.
        """
        # ``\\u2603`` (bonhomme de neige) est dans la plage 0x2600-0x27BF
        # donc traité comme émoji par ``_payload_has_emoji``. On
        # choisit plutôt un caractère hors dict *et* hors plage émoji :
        # l'avatar U+E000 (zone à usage privé, hors plage couverte).
        item = make_item("\ue000", lang="fr", mode=MODE_EPELER)
        setup = TtsSetupBuilder().build(item)

        self.assertTrue(setup.ok)
        # Caractère absent -> préservé tel quel dans la liste.
        self.assertEqual(setup.to_pronounce, ("\ue000",))


# ---------------------------------------------------------------------------
# Tests : ``get_mode_message`` (mode_msg.py)
# ---------------------------------------------------------------------------


class TestGetModeMessage(unittest.TestCase):
    """Tests de la table de traductions des messages de mode."""

    def test_frCH_vers_fr(self) -> None:
        """``frCH`` -> repli français pour « Mode cacher »."""
        msg = get_mode_message("Mode cacher", "frCH")
        self.assertEqual(msg, "Écoute bien.")

    def test_langue_none_repli_fr(self) -> None:
        """Langue ``None`` -> repli français."""
        msg = get_mode_message("Mode cacher", None)
        self.assertEqual(msg, "Écoute bien.")

    def test_langue_vide_repli_fr(self) -> None:
        """Langue ``""`` (fausse) -> repli français."""
        msg = get_mode_message("Mode dicter", "")
        self.assertEqual(msg, "Écoute la dictée.")

    def test_cle_inconnue_en_fr(self) -> None:
        """Clé absente -> la fonction retombe sur la clé brute."""
        msg = get_mode_message("Mode inexistant", "fr")
        self.assertEqual(msg, "Mode inexistant")

    def test_epeler_messages(self) -> None:
        """Vérifie la présence des messages d'erreur du mode épeler."""
        self.assertEqual(
            get_mode_message("Mode Epeler", "fr"),
            "Écoute les lettres.",
        )
        self.assertEqual(
            get_mode_message("Mode epeler non implemente", "fr"),
            "Mode épeler pas encore implémenté dans cette langue",
        )
        self.assertEqual(
            get_mode_message("Mode epeler emoji", "fr"),
            "MAEL ne traite pas les émojis",
        )


# ---------------------------------------------------------------------------
# Tests : ``qr_parse`` (constantes + détection des suffixes)
# ---------------------------------------------------------------------------


class TestQrParse(unittest.TestCase):
    """Tests rapides du parseur QR."""

    def test_suffix_cacher_detecte(self) -> None:
        """Le suffixe ``#c`` est détecté comme mode ``cacher``."""
        mode, body = _strip_suffix("Bonjour#c")
        self.assertEqual(mode, MODE_CACHER)
        self.assertEqual(body, "Bonjour")

    def test_suffix_dicter_detecte(self) -> None:
        """Le suffixe ``#d`` est détecté comme mode ``dicter``."""
        mode, body = _strip_suffix("Bonjour#d")
        self.assertEqual(mode, MODE_DICTER)
        self.assertEqual(body, "Bonjour")

    def test_suffix_epeler_detecte(self) -> None:
        """Le suffixe ``#e`` est détecté comme mode ``epeler``."""
        mode, body = _strip_suffix("Bonjour#e")
        self.assertEqual(mode, MODE_EPELER)
        self.assertEqual(body, "Bonjour")

    def test_pas_de_suffixe(self) -> None:
        """Sans suffixe, ``_strip_suffix`` retourne ``(None, texte)``."""
        mode, body = _strip_suffix("Bonjour")
        self.assertIsNone(mode)
        self.assertEqual(body, "Bonjour")

    def test_lang_default_fr(self) -> None:
        """La langue par défaut doit être ``'fr'``."""
        self.assertEqual(LANG_DEFAULT, "fr")

    def test_constantes_suffixes(self) -> None:
        """Vérifie la valeur des constantes de suffixes et de modes."""
        self.assertEqual(SUFFIX_CACHER, "#c")
        self.assertEqual(SUFFIX_DICTER, "#d")
        self.assertEqual(SUFFIX_EPELER, "#e")
        self.assertEqual(MODE_CACHER, "cacher")
        self.assertEqual(MODE_LIRE, "lire")


# ---------------------------------------------------------------------------
# Tests : intégrité de ``epel_tts`` (chiffres présents dans toutes les langues)
# ---------------------------------------------------------------------------


class TestEpelDigits(unittest.TestCase):
    """Vérifie la présence des chiffres 0-9 dans chaque dict."""

    def test_chiffres_toutes_langues(self) -> None:
        """Les chiffres ``0``..``9`` sont définis pour fr/es/en/pt/de/it."""
        for lang in ("fr", "es", "en", "pt", "de", "it"):
            d = getattr(epel_tts, f"epel_tts_{lang}")
            for digit in "0123456789":
                self.assertIn(digit, d, msg=f"{lang}:{digit} manquant")
                self.assertIsInstance(d[digit], str)
                self.assertNotEqual(d[digit], "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
