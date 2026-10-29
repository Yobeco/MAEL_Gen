# -*- coding: utf-8 -*-
"""
tts_setup.py — Construction d'un ``TtsSetup`` à partir d'un ``TtsItem``.

Ce module contient la classe :class:`TtsSetupBuilder`, chargée de
transformer un ``TtsItem`` (déjà analysé par ``qr_parse``) en un
``TtsSetup`` prêt à l'emploi pour la couche de synthèse vocale.

Responsabilités
---------------
1. Normaliser prudemment la clé de langue portée par le ``TtsItem``
   (suppression d'éventuels chevrons ou espaces superflus).
2. Résoudre la langue vers un **code gTTS** en consultant le
   dictionnaire ``lang_tts`` :

   * langue absente (``None``) → repli systématique sur le français
     (``"fr"``) ;
   * clé exacte présente → on lit la colonne ``gTTS`` correspondante ;
   * clé exacte sans code gTTS → repli sur la langue de référence
     (deux premières lettres) ;
   * variante régionale inconnue (référence connue) → repli avec
     avertissement ;
   * langue totalement inconnue → erreur : ``lang = None``, message
     ultra-court affiché à l'écran et dans les logs.

3. Ventiler le contenu selon le **mode** :

   * ``"lire"`` → ``to_pronounce`` contient le texte clair,
     ``to_show`` reprend ce même texte ;
   * ``"cacher"`` → on prononce le texte, mais ``to_show`` est un
     message localisé (« Écoute bien. » dans la langue du contenu) ;
   * ``"epeler"`` → on prononce l'**épellation** du texte (chaque
     point de code remplacé par sa lecture dans le dictionnaire
     ``epel_tts_xx``) et ``to_show`` est un message localisé
     (« Écoute les lettres. »). Le texte est segmenté **sans
     normalisation** (un élément par point de code). Les émojis et
     les langues sans dictionnaire d'épellation déclenchent des
     messages d'erreur courts.
   * tout autre mode → message ``"Mode non géré"`` à l'écran et
     avertissement en console.

Le module n'effectue aucune I/O et n'importe pas ``gTTS`` ; il se
contente de produire une *configuration* que la couche audio
exploitera ensuite.
"""

from __future__ import annotations

import logging
import unicodedata
from typing import Optional

from lang_tts import lang_tts

from qr_dto import TtsItem, TtsSetup

from mode_msg import FALLBACK_LANG, MsgKey, get_mode_message, has_message
from mael_modes import Mode

from dicter_tts import decouper_gds


# Le dictionnaire d'épellation ``epel_tts`` est facultatif : si le
# module n'est pas disponible (par exemple en environnement allégé),
# on retombe sur l'erreur « dict absent » dès qu'un mode épeler
# est demandé.
try:
    import epel_tts  # noqa: F401  (utilisé via getattr dynamique)
except ImportError:  # pragma: no cover — module absent de l'environnement
    epel_tts = None  # type: ignore[assignment]


# ----------------------------------------------------------------------
# Logger de module
# ----------------------------------------------------------------------
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Constantes locales (lisibles, on évite les nombres magiques)
# ----------------------------------------------------------------------

#: Mode pour lequel la lecture intégrale du texte est demandée.
MODE_LIRE: Mode = Mode.LIRE

#: Clé de repli utilisée quand ``TtsItem.lang`` vaut ``None``.
DEFAULT_LANG_KEY: str = FALLBACK_LANG



# ----------------------------------------------------------------------
# Helpers privés
# ----------------------------------------------------------------------

def _normalize_lang_key(raw: Optional[str]) -> Optional[str]:
    """
    Normalise prudemment la clé de langue portée par un ``TtsItem``.

    Le pipeline amont peut, selon l'origine du QR, écrire la langue
    avec des décorations (``"<frCA>"``, ``" frCA "``, ``"« frCA »"``…).
    On retire les espaces, les chevrons et les guillemets courants
    pour retomber sur la clé canonique du dictionnaire ``lang_tts``.

    Paramètres
    ----------
    raw : Optional[str]
        Valeur brute telle que portée par ``TtsItem.lang``.

    Retour
    ------
    Optional[str]
        Clé nettoyée, ou ``None`` si l'entrée était vide / absente.
    """
    if raw is None:
        return None
    cleaned = raw.strip().strip("<>\"'«»").strip()
    return cleaned or None



def _gtts_for_key(key: str) -> Optional[str]:
    """
    Renvoie le code gTTS associé à la clé ``key`` dans ``lang_tts``.

    Le code gTTS est la **deuxième** colonne (indice 1) de chaque
    entrée du dictionnaire. On ne le déduit jamais de la clé : on lit
    strictement la valeur tabulée, même pour les codes atypiques
    (``"zh-CN"``, ``"yue"``, ``"iw"``, ``"fr-CA"``…).

    Paramètres
    ----------
    key : str
        Clé de langue telle qu'elle apparaît dans ``lang_tts``.

    Retour
    ------
    Optional[str]
        Code gTTS ou ``None`` si la clé est absente / sans support gTTS.
    """
    entry = lang_tts.get(key)
    if entry is None:
        return None
    return entry[1]


def _reference_key(key: str) -> str:
    """
    Calcule la clé de référence (langue « parente ») à partir d'une
    variante régionale. Convention simple : les deux premières lettres
    en minuscules. ``"frCA"`` → ``"fr"``, ``"zhHK"`` → ``"zh"``.
    """
    return key[:2].lower()


def _get_epel_dict(lang: Optional[str]) -> Optional[dict]:
    """
    Récupère le dictionnaire d'épellation ``epel_tts_xx`` associé à
    la langue ``lang`` (par exemple ``epel_tts_fr`` pour ``"fr"``).

    * La langue est d'abord réduite à ses deux premières lettres en
      minuscules (``"frCH"`` → ``"fr"``, ``"EN"`` → ``"en"``) ;
    * on renvoie ``None`` si le module ``epel_tts`` n'a pas pu être
      importé ou si l'attribut ``epel_tts_<lang2>`` est absent.
    """
    if epel_tts is None:
        return None
    if not lang:
        return None
    lang2 = lang[:2].lower() if len(lang) >= 2 else lang.lower()
    return getattr(epel_tts, f"epel_tts_{lang2}", None)


def _is_emoji_code_point(cp: int) -> bool:
    """
    Détecte si un point de code Unicode appartient à un assemblage
    émoji susceptible d'être mal épelé.

    On couvre :
      * les **sélecteurs** typiques des séquences émojis
        (``U+200D`` ZWJ, ``U+FE0F`` variation selector 16) ;
      * les **sélecteurs de teint** Fitzpatrick
        (``U+1F3FB`` … ``U+1F3FF``) ;
      * les **indicateurs régionaux** des drapeaux
        (``U+1F1E6`` … ``U+1F1FF``) ;
      * les grandes plages émojis historiques
        (``U+1F300`` … ``U+1FAFF``, ``U+2600`` … ``U+27BF``).

    On reste volontairement prudent : une chaîne contenant l'un de
    ces points de code est considérée comme relevant d'un émoji et
    déclenche le message d'erreur dédié.
    """
    # Sélecteurs explicites.
    if cp in (0x200D, 0xFE0F):
        return True
    # Sélecteurs de teint.
    if 0x1F3FB <= cp <= 0x1F3FF:
        return True
    # Indicateurs régionaux (drapeaux).
    if 0x1F1E6 <= cp <= 0x1F1FF:
        return True
    # Grandes plages émojis.
    if 0x1F300 <= cp <= 0x1FAFF:
        return True
    if 0x2600 <= cp <= 0x27BF:
        return True
    return False


def _payload_has_emoji(payload: str) -> bool:
    """Renvoie ``True`` si le payload contient un point de code « émoji »."""
    for ch in payload:
        if _is_emoji_code_point(ord(ch)):
            return True
    return False


def _spell(payload: str, epel_dict: dict) -> tuple[str, ...]:
    """
    Épelle ``payload`` en substituant chaque point de code par la
    chaîne du dictionnaire ``epel_dict``.

    * On parcourt ``list(payload)`` (un élément par point de code,
      **sans normalisation** NFC/NFKC) ;
    * les entrées dont la valeur est la chaîne vide sont conservées
      telles quelles dans le tuple résultat (un élément ``""``) ;
    * les points de code absents du dict sont conservés tels quels
      et un ``logging.warning`` est émis pour information.

    Retour
    ------
    tuple[str, ...]
        Segments à prononcer successivement.
    """
    out: list[str] = []
    for ch in payload:
        if ch in epel_dict:
            out.append(epel_dict[ch])
        else:
            logger.warning(
                "Caractère U+%04X absent du dictionnaire d'épellation ; "
                "conservé tel quel dans la sortie.",
                ord(ch),
            )
            out.append(ch)
    return tuple(out)


# ----------------------------------------------------------------------
# Classe principale
# ----------------------------------------------------------------------

class TtsSetupBuilder:
    """
    Construit un :class:`TtsSetup` à partir d'un :class:`TtsItem`.

    Le builder est sans état : la même instance peut être réutilisée
    pour plusieurs items successifs. Il n'effectue aucune I/O et ne
    s'appuie sur aucun moteur TTS réel ; il se contente de produire
    une configuration que la couche de lecture exploitera ensuite.

    Algorithme de résolution de langue
    ----------------------------------
    1. ``item.lang`` ``None`` → français (``"fr"``).
    2. Clé exacte présente dans ``lang_tts`` avec un code gTTS valide →
       on l'utilise tel quel.
    3. Clé exacte présente mais code gTTS ``None`` → repli sur la
       langue de référence (2 premières lettres). Si la référence a
       aussi un code gTTS valide, on l'utilise (avec avertissement).
       Sinon, on bascule en erreur.
    4. Variante régionale inconnue (référence connue) → repli sur la
       référence avec un ``logging.warning``.
    5. Langue totalement inconnue → erreur :
       configuration de repli construite par ``_fallback_setup``.

    Ventilation par mode
    --------------------
    * ``"lire"`` → ``to_pronounce = (item.text,)``,
      ``to_show = item.text``.
    * ``"cacher"`` → ``to_pronounce = (item.text,)``,
      ``to_show = "Écoute bien."`` (localisé).
    * ``"epeler"`` → ``to_pronounce = épellation de item.text``,
      ``to_show = "Écoute les lettres."`` (localisé), ou message
      d'erreur court si la langue est sans dictionnaire
      d'épellation ou si le payload contient un émoji.
    * autre mode → configuration de repli localisée via ``_fallback_setup``
      + ``logging.warning`` en console.
    """

    # --------------------------------------------------------------
    # Construction
    # --------------------------------------------------------------

    def _fallback_setup(self, item: TtsItem, msg_key: MsgKey) -> TtsSetup:
        """Produit une configuration neutre, localisée selon l'item en erreur."""
        item_lang = _normalize_lang_key(item.lang)
        msg_lang = (
            item_lang
            if item_lang in lang_tts and has_message(msg_key, item_lang)
            else FALLBACK_LANG
        )
        return TtsSetup(
            item=item, mode=Mode.LIRE, lang=msg_lang,
            list_gds=(" ",), to_pronounce=(" ",),
            to_show=get_mode_message(msg_key, msg_lang),
        )

    # --------------------------------------------------------------
    # API publique
    # --------------------------------------------------------------

    def build(self, item: TtsItem) -> TtsSetup:
        """
        Construit le :class:`TtsSetup` correspondant à ``item``.

        Paramètres
        ----------
        item : TtsItem
            Item déjà analysé par ``qr_parse``. Seuls ``text``,
            ``mode`` et ``lang`` sont lus ; les autres champs sont
            simplement conservés tels quels dans le DTO résultat.

        Retour
        ------
        TtsSetup
            Configuration prête à l'emploi (ou en erreur, avec
            ``ok = False`` si la langue n'a pas pu être résolue).
        """
        # --- 1. Résolution de la langue ---------------------------
        key = _normalize_lang_key(item.lang)
        resolved_lang = self._resolve_lang(key)

        # --- 2. Ventilation selon le mode -------------------------
        return self._dispatch(item, resolved_lang)

    # --------------------------------------------------------------
    # Étapes internes
    # --------------------------------------------------------------

    def _resolve_lang(self, key: Optional[str]) -> Optional[str]:
        """
        Applique l'algorithme de résolution décrit dans la docstring
        de la classe. Renvoie le code gTTS retenu, ou ``None`` en cas
        d'échec. Journalise les replis et erreurs via ``logger``.
        """
        # Cas 1 : langue absente → français par défaut.
        if key is None:
            logger.info(
                "Langue absente sur le TtsItem, repli sur '%s'.",
                DEFAULT_LANG_KEY,
            )
            return _gtts_for_key(DEFAULT_LANG_KEY)

        # Cas 2 : clé exacte présente avec un code gTTS exploitable.
        gtts = _gtts_for_key(key)
        if gtts is not None:
            return gtts

        # Cas 3 : clé exacte SANS code gTTS → tentative sur la
        # langue de référence. Si elle-même n'a pas de code gTTS,
        # on bascule en erreur directement depuis la référence.
        ref_key = _reference_key(key)
        ref_gtts = _gtts_for_key(ref_key)

        if ref_key == key:
            logger.warning(
                "Langue '%s' présente mais sans code gTTS ; aucune "
                "solution de repli disponible.",
                key,
            )
            return None

        if ref_gtts is not None:
            logger.warning(
                "Langue '%s' non prise en charge par gTTS ; repli sur "
                "la langue de référence '%s' (code gTTS '%s').",
                key, ref_key, ref_gtts,
            )
            return ref_gtts

        if key != ref_key and ref_gtts is None and key in lang_tts:
            logger.warning(
                "Langue '%s' absente de lang_tts ; impossible de "
                "revenir à la langue de référence.",
                key,
            )
            return None

        # Cas 5 : langue totalement inconnue.
        logger.warning(
            "Langue totalement inconnue : '%s'.", key,
        )
        return None

    def _dispatch(
        self,
        item: TtsItem,
        resolved_lang: Optional[str],
    ) -> TtsSetup:
        """
        Construit le ``TtsSetup`` final en combinant langue résolue
        et mode demandé.

        Priorités d'erreur (de la plus haute à la plus basse) :

        1. langue inconnue (``resolved_lang is None``) ;
        2. payload émoji (mode ``epeler`` uniquement) ;
        3. dictionnaire d'épellation absent pour la langue ;
        4. mode « epeler » nominal ;
        5. mode « lire » / « cacher » nominaux ;
        6. tout autre mode → repli ``MsgKey.MODE_INCONNU``.
        """
        # --- Erreur de langue : on court-circuite le mode ---------
        if resolved_lang is None:
            logger.warning("Langue inconnue pour TtsItem : %r", item.lang)
            return self._fallback_setup(item, MsgKey.LANGUE_INCONNUE)

        # ------------------------------------------------------------------
        # Mode « dicter » : segmentation en GDS, avec substitution des
        # seuls signes de ponctuation connus du dictionnaire linguistique.
        # ------------------------------------------------------------------
        if item.mode == Mode.DICTER:
            if _payload_has_emoji(item.text):
                logger.warning(
                    "Mode dicter : émoji détecté dans le payload ; "
                    "sortie en erreur courte."
                )
                return self._fallback_setup(item, MsgKey.MODE_EPELER_EMOJI)

            epel_dict = _get_epel_dict(item.lang)
            if epel_dict is None:
                logger.warning(
                    "Mode dicter : aucun dictionnaire de ponctuation "
                    "disponible pour la langue '%s'.",
                    _normalize_lang_key(item.lang),
                )
                return self._fallback_setup(item, MsgKey.MODE_EPELER_NON_IMPLEMENTE)

            groupes = decouper_gds(item.text, item.lang or "fr")
            a_prononcer: list[str] = []
            for groupe in groupes:
                if groupe == "..." and "…" in epel_dict:
                    a_prononcer.append(epel_dict["…"])
                elif groupe and all(
                    unicodedata.category(caractere).startswith("P")
                    for caractere in groupe
                ):
                    if groupe in epel_dict:
                        a_prononcer.append(epel_dict[groupe])
                    else:
                        logger.warning(
                            "Ponctuation %r absente du dictionnaire "
                            "d'épellation ; conservée telle quelle.", groupe,
                        )
                        a_prononcer.append(groupe)
                else:
                    a_prononcer.append(groupe)

            return TtsSetup(
                item=item,
                mode=Mode(item.mode),
                lang=resolved_lang,
                to_pronounce=tuple(a_prononcer),
                to_show=get_mode_message(MsgKey.MODE_DICTER, item.lang),
                list_gds=groupes,
            )

        # ------------------------------------------------------------------
        # Mode « epeler » : la logique est plus riche (épellation,
        # détection d'émojis, dict absent). On la traite en amont pour
        # pouvoir court-circuiter proprement avec des messages courts.
        # ------------------------------------------------------------------
        if item.mode == Mode.EPELER:
            # Priorité 2 : émojis dans le payload.
            if _payload_has_emoji(item.text):
                logger.warning(
                    "Mode épeler : émoji détecté dans le payload ; "
                    "sortie en erreur courte."
                )
                return self._fallback_setup(item, MsgKey.MODE_EPELER_EMOJI)

            # Priorité 3 : dictionnaire d'épellation absent.
            epel_dict = _get_epel_dict(item.lang)
            if epel_dict is None:
                logger.warning(
                    "Mode épeler : Aucun dictionnaire d'épellation "
                    "disponible pour la langue '%s'.",
                    _normalize_lang_key(item.lang),
                )
                return self._fallback_setup(item, MsgKey.MODE_EPELER_NON_IMPLEMENTE)

            # Priorité 4 : épellation nominale.
            return TtsSetup(
                item=item,
                mode=Mode(item.mode),
                lang=resolved_lang,
                to_pronounce=_spell(item.text, epel_dict),
                to_show=get_mode_message(MsgKey.MODE_EPELER, item.lang),
            )

        # ------------------------------------------------------------------
        # Table de dispatch pour les autres modes supportés.
        # ------------------------------------------------------------------

        def _show_lire(_item, _resolved_lang):
            """Mode « lire » : on affiche le texte tel quel."""
            return _item.text

        def _show_cacher(_item, _resolved_lang):
            """
            Mode « cacher » : on affiche le message localisé
            « Écoute bien. » dans la langue du contenu lu.
            ``get_mode_message`` se charge du repli vers le français
            si la langue n'est pas connue.
            """
            return get_mode_message(MsgKey.MODE_CACHER, item.lang)

        _MODE_SHOW_BUILDERS = {
            MODE_LIRE: _show_lire,
            Mode.CACHER: _show_cacher,
        }

        show_builder = _MODE_SHOW_BUILDERS.get(item.mode)
        if show_builder is not None:
            return TtsSetup(
                item=item,
                mode=Mode(item.mode),
                lang=resolved_lang,
                to_pronounce=(item.text,),
                to_show=show_builder(item, resolved_lang),
            )

        # --- Mode non encore implémenté ---------------------------
        logger.warning(
            "Mode '%s' non géré par TtsSetupBuilder.", item.mode,
        )
        return self._fallback_setup(item, MsgKey.MODE_INCONNU)
