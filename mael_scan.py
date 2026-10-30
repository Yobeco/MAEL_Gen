"""Orchestrateur MAEL Scan, seul décideur des enchaînements audio."""
from __future__ import annotations

import logging
import os
import threading
from dataclasses import replace
from typing import Any

from qr_dto import CloudItem, TtsItem, TtsSetup, WifiItem
from wifi_setup import WifiSetup
from tts_setup import TtsSetupBuilder
from mode_msg import MsgKey, get_mode_message

logger = logging.getLogger(__name__)


class MaelScan:
    """Coordonne scanner, parsing, synthèse et lecture séquentielle."""

    SPEED_PCT_NORMAL = 100
    SPEED_PCT_SLOW = 80
    PAUSE_NORMAL = 0.05
    PAUSE_SLOW = 0.3
    PAUSE_FACT_NORMAL = 0.3
    PAUSE_FACT_SLOW = 0.5
    PAUSE_REPEAT = 1.0
    PAUSE_MIN = 0.3
    PAUSE_MAX = 4.0

    def __init__(self, tts_player: Any, wifi_setup: WifiSetup | None = None,
                 scanner: Any | None = None, mp3_fetch: Any | None = None,
                 on_audio_status: Any | None = None, reader: Any | None = None) -> None:
        self.tts_player = tts_player
        self.wifi_setup = wifi_setup or WifiSetup()
        self.scanner = scanner
        self.mp3_fetch = mp3_fetch
        self.on_audio_status = on_audio_status
        self.tts_setup_builder = TtsSetupBuilder()
        self.last_tts_item: TtsItem | None = None
        self.last_tts_setup: TtsSetup | None = None
        if reader is None:
            from mp3_read import create_mp3_reader
            reader = create_mp3_reader()
        self.reader = reader
        self._generation = 0
        self._generation_lock = threading.RLock()
        self._cancel = threading.Event()
        self._thread: threading.Thread | None = None

    def stop(self) -> None:
        """Interrompt la lecture et invalide toute action audio en cours."""
        with self._generation_lock:
            self.reader.stop()
            self._generation += 1
            self._cancel.set()

    def _new_request(self) -> tuple[int, threading.Event]:
        """Interrompt l'audio précédent et réserve un jeton de requête neuf."""
        with self._generation_lock:
            self.reader.stop()
            self._generation += 1
            self._cancel.set()
            self._cancel = threading.Event()
            return self._generation, self._cancel

    def _current(self, generation: int, event: threading.Event) -> bool:
        with self._generation_lock:
            return generation == self._generation and not event.is_set()

    def scan(self, source: object | None = None) -> list[TtsItem | CloudItem | WifiItem]:
        """Scanne et analyse les QR; exécute leurs actions audio en fond."""
        generation, event = self._new_request()
        if self.scanner is None:
            from scanner_factory import create_scanner
            self.scanner = create_scanner("pc_pdf" if source is not None else None)
        raws = self.scanner.scan(source)
        from qr_parse import MODE_LIRE, parse_all
        items = parse_all(raws)
        actions: list[tuple[str, Any]] = []
        for item in items:
            if isinstance(item, TtsItem):
                self.last_tts_item = item
                setup = self.tts_setup_builder.build(item)
                self.last_tts_setup = setup
                actions.append(("tts", setup))
            elif isinstance(item, WifiItem):
                wifi_tts_item = TtsItem(
                    raw=item.raw, original=item.raw.text, text="Code QR Wifi",
                    lang="fr", mode=MODE_LIRE,
                )
                setup = replace(
                    self.tts_setup_builder.build(wifi_tts_item),
                    mode=MODE_LIRE, lang="fr", list_gds=("Code QR Wifi",),
                    to_pronounce=("Code QR Wifi",), to_show="Code QR Wifi",
                )
                self.last_tts_setup = setup
                self.wifi_setup.apply(item)
                actions.append(("tts", setup))
            elif isinstance(item, CloudItem):
                actions.append(("cloud", item))
        self._thread = threading.Thread(
            target=self._run_actions, args=(actions, generation, event),
            name="MaelScanAudio", daemon=True,
        )
        self._thread.start()
        return items

    def _run_actions(self, actions: list[tuple[str, Any]], generation: int,
                     event: threading.Event, slow: bool = False) -> None:
        for kind, item in actions:
            if not self._current(generation, event):
                return
            try:
                if kind == "cloud":
                    self._play_cloud(item, generation, event)
                else:
                    self._play_setup(item, slow, generation, event)
            except Exception:
                if self._current(generation, event):
                    logger.exception("Erreur pendant l'action audio MAEL Scan.")

    def _play_cloud(self, item: CloudItem, generation: int, event: threading.Event) -> None:
        """Télécharge un MP3 cloud, puis en confie la lecture au lecteur."""
        base_setup = self.tts_setup_builder.build(TtsItem(
            raw=item.raw, original=item.text, text=item.text, lang="fr", mode="lire"
        ))
        def download_start() -> None:
            if self.on_audio_status and self._current(generation, event):
                self.on_audio_status(replace(
                    base_setup,
                    to_pronounce=(),
                    to_show=get_mode_message(MsgKey.MODE_MP3_TELECHARGEMENT, base_setup.lang)
                ))

        def download_end() -> None:
            if self.on_audio_status and self._current(generation, event):
                self.on_audio_status(replace(base_setup, to_pronounce=(), to_show=""))

        if self.mp3_fetch is None:
            from mp3_fetch import Mp3Fetch
            self.mp3_fetch = Mp3Fetch(
                on_download_start=download_start, on_download_end=download_end
            )
        else:
            if hasattr(self.mp3_fetch, "on_download_start"):
                self.mp3_fetch.on_download_start = download_start
            if hasattr(self.mp3_fetch, "on_download_end"):
                self.mp3_fetch.on_download_end = download_end

        try:
            path = self.mp3_fetch.fetch(item)
        except Exception:
            if self.on_audio_status and self._current(generation, event):
                self.on_audio_status(replace(
                    base_setup,
                    to_pronounce=(),
                    to_show=get_mode_message(MsgKey.MODE_MP3_ERREUR, base_setup.lang),
                ))
            raise

        if not self._current(generation, event):
            try:
                os.unlink(path)
            except OSError:
                pass
            return
        if not self._play_if_current(path, generation, event):
            try:
                os.unlink(path)
            except OSError:
                pass
            return
        self._wait_reader(generation, event)

    def _play_setup(self, setup: TtsSetup, slow: bool, generation: int,
                    event: threading.Event) -> None:
        if setup.lang is None or not self._current(generation, event):
            return
        if setup.mode == "dicter":
            self._play_dicter(setup, slow, generation, event)
            return
        pause = self.PAUSE_SLOW if slow else self.PAUSE_NORMAL
        for text in setup.to_pronounce:
            if not self._current(generation, event):
                return
            speed = self.SPEED_PCT_SLOW if slow else self.SPEED_PCT_NORMAL
            if not text or not text.strip():
                continue
            path = self.tts_player.synthesize(text, setup.lang, speed=speed)
            if not self._current(generation, event):
                return
            if not self._play_if_current(path, generation, event):
                return
            if not self._wait_reader(generation, event):
                return
            if event.wait(pause):
                return

    def _play_dicter(self, setup: TtsSetup, slow: bool, generation: int,
                     event: threading.Event) -> None:
        """Dicte les GDS, avec répétition lente et pauses interruptibles."""
        if len(setup.to_pronounce) != len(setup.list_gds):
            raise ValueError("En mode dicter, to_pronounce et list_gds doivent avoir la même longueur.")
        if setup.lang is None:
            return
        factor = self.PAUSE_FACT_SLOW if slow else self.PAUSE_FACT_NORMAL
        for index, text in enumerate(setup.to_pronounce):
            if not self._current(generation, event):
                return
            path = self.tts_player.synthesize(text, setup.lang, speed=self.SPEED_PCT_NORMAL)
            if not self._current(generation, event):
                return
            if not self._play_if_current(path, generation, event):
                return
            if not self._wait_reader(generation, event):
                return
            if slow:
                if event.wait(self.PAUSE_REPEAT) or not self._current(generation, event):
                    return
                path = self.tts_player.synthesize(text, setup.lang, speed=self.SPEED_PCT_SLOW)
                if not self._current(generation, event):
                    return
                if not self._play_if_current(path, generation, event):
                    return
                if not self._wait_reader(generation, event):
                    return
            pause = max(self.PAUSE_MIN, min(self.PAUSE_MAX, len(setup.list_gds[index]) * factor))
            if event.wait(pause):
                return

    def _play_if_current(self, path: str, generation: int, event: threading.Event) -> bool:
        """Publie un nouveau son de façon atomique vis-à-vis d'un scan concurrent."""
        with self._generation_lock:
            if generation != self._generation or event.is_set():
                return False
            self.reader.play(path)
            return True

    def _wait_reader(self, generation: int, event: threading.Event) -> bool:
        """Attend le segment audio sans empêcher stop() d'interrompre la lecture."""
        while self._current(generation, event):
            waiter = getattr(self.reader, "wait", None)
            if waiter is not None:
                try:
                    finished = waiter(timeout=0.05)
                except TypeError:
                    finished = waiter(0.05)
                # False signifie seulement que le délai de polling a expiré,
                # pas que le segment audio est terminé. Continuer à attendre
                # en vérifiant entre-temps le jeton d'annulation.
                if finished:
                    return self._current(generation, event)
                continue
            if not getattr(self.reader, "is_playing", False):
                return True
            if event.wait(0.05):
                return False
        return False

    def repeat(self, slow: bool = False) -> None:
        """Rejoue le dernier TtsSetup à vitesse normale ou lente."""
        if self.last_tts_setup is None:
            return
        generation, event = self._new_request()
        self._thread = threading.Thread(
            target=self._run_actions, args=([("tts", self.last_tts_setup)], generation, event, slow),
            name="MaelScanRepeat", daemon=True,
        )
        self._thread.start()

    def repeat_slow(self) -> None:
        """Relit le dernier TtsSetup à vitesse lente."""
        self.repeat(slow=True)


def scan(tts_player: Any, source: object | None = None,
         wifi_setup: WifiSetup | None = None, scanner: Any | None = None,
         mp3_fetch: Any | None = None, reader: Any | None = None) -> list[TtsItem | CloudItem | WifiItem]:
    """Point d'entrée fonctionnel pratique pour un scan ponctuel."""
    return MaelScan(tts_player, wifi_setup=wifi_setup, scanner=scanner,
                    mp3_fetch=mp3_fetch, reader=reader).scan(source)
