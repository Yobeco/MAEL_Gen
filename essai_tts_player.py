#!/usr/bin/env python3
"""Essai clavier de TtsPlayer avec un TtsSetup de démonstration.

Depuis le dossier contenant ce script :
    python essai_tts_player.py
    python essai_tts_player.py --sans-son
    python essai_tts_player.py --sans-son --mode dicter

Le TtsSetup est construit manuellement avec les champs disponibles dans
qr_dto.py. Dans cette version, le champ list_without_sub du diagramme
s'appelle list_gds dans l'API TtsSetup actuelle.
"""

from __future__ import annotations

import argparse
import sys
import time

from qr_dto import RawQr, TtsItem, TtsSetup
from tts_player import TtsPlayer
from tts_player_gtts import GttsPlayer

PHRASE = "Où vas-tu Zaïn ?"
PRONONCER_DICtee = ("Où", "vas-tu", "Zaïn", "point d'interrogation")
GROUPES_DICtee = ("Où", "vas-tu", "Zaïn", "?")


class FauxPlayer(TtsPlayer):
    """Lecteur factice : affiche les segments et les pauses, sans audio."""

    # Garder le déroulement du TtsPlayer, mais éviter les attentes longues
    # pendant un essai sans son.
    PAUSE_NORMAL = 0.01
    PAUSE_SLOW = 0.01
    PAUSE_FACT_NORMAL = 0.01
    PAUSE_FACT_SLOW = 0.01
    PAUSE_REPEAT = 0.01
    PAUSE_MIN = 0.01
    PAUSE_MAX = 0.03

    def _say(self, text: str, lang: str, speed: int) -> None:
        vitesse = "lente" if speed < self.SPEED_NORMAL else "normale"
        print(f"[FAUX AUDIO, {lang}, vitesse {vitesse}] {text}")
        print("[pause simulée selon l'algorithme de TtsPlayer]")

    def _stop_audio(self) -> None:
        pass


def make_setup(mode: str) -> TtsSetup:
    """Construit directement le DTO de configuration avec les vraies API."""
    raw = RawQr(text=PHRASE, position=None, format="demo", ec_level=None)
    item = TtsItem(
        raw=raw,
        original=PHRASE,
        text=PHRASE,
        lang="fr",
        mode=mode,
    )
    if mode == "dicter":
        pronounce = PRONONCER_DICtee
        gds = GROUPES_DICtee
    else:
        # Modes phrase entière (lire / cacher).
        pronounce = (PHRASE,)
        gds = ()
    return TtsSetup(
        item=item,
        mode=mode,
        lang="fr",
        to_pronounce=pronounce,
        to_show=PHRASE,
        list_gds=gds,
    )


def choose_mode(arg_mode: str | None) -> str:
    if arg_mode:
        return arg_mode
    while True:
        print("Mode de l'exemple : 1 = Lire, 2 = Dicter, 3 = Cacher")
        choice = input("Mode [1] : ").strip() or "1"
        modes = {"1": "lire", "2": "dicter", "3": "cacher"}
        if choice in modes:
            return modes[choice]
        print("Choix invalide.")


def wait_until_done(player: TtsPlayer) -> None:
    while player.is_playing:
        time.sleep(0.01)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sans-son", action="store_true",
        help="afficher les segments et pauses sans synthèse ni réseau",
    )
    parser.add_argument(
        "--mode", choices=("lire", "dicter", "cacher"),
        help="choisir directement le mode (sinon menu interactif)",
    )
    args = parser.parse_args()

    mode = choose_mode(args.mode)
    setup = make_setup(mode)
    player: TtsPlayer = FauxPlayer() if args.sans_son else GttsPlayer()

    print(f"\nTexte de démonstration : {PHRASE}")
    print(f"Mode : {mode} | langue : {setup.lang}")
    print("Commandes : 1 = Scanner / lecture normale, 2 = Répéter, "
          "3 = Répéter lentement, 0 = Quitter")
    try:
        while True:
            action = input("Action : ").strip()
            if action == "0":
                break
            if action not in {"1", "2", "3"}:
                print("Choix invalide.")
                continue
            # Dans cet essai sans scanner, « Scanner » lit le TtsSetup
            # prérempli ; « Répéter » rejoue le même exemple.
            print("Lecture de l'exemple…")
            player.play(setup, slow=(action == "3"))
            wait_until_done(player)
            print("Lecture terminée.\n")
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        player.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
