"""Infrastructure abstraite de lecture des configurations de synthèse vocale."""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod

from qr_dto import TtsSetup
import audio_control
from audio_control import StoppablePlayback

logger = logging.getLogger(__name__)


class TtsPlayer(StoppablePlayback, ABC):
    """Orchestre les modes de lecture et leur exécution interruptible."""

    SPEED_NORMAL = 100
    SPEED_SLOW = 80
    PAUSE_NORMAL = 0.05
    PAUSE_SLOW = 0.3
    PAUSE_FACT_NORMAL = 0.3
    PAUSE_FACT_SLOW = 0.5
    PAUSE_REPEAT = 1.0
    PAUSE_MIN = 0.3
    PAUSE_MAX = 4.0

    def __init__(self) -> None:
        """Initialise l'état de lecture et son verrou de synchronisation."""
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.RLock()
        audio_control.register(self)

    @abstractmethod
    def _say(self, text: str, lang: str, speed: int) -> None:
        """Lit le texte de façon bloquante, jusqu'à la fin de l'audio."""
        raise NotImplementedError

    @abstractmethod
    def _stop_audio(self) -> None:
        """Interrompt immédiatement l'audio du moteur concret."""
        raise NotImplementedError

    def _prepare(self, items: list[tuple[str, str, int]]) -> None:
        """Prépare éventuellement les éléments avant la lecture."""

    @property
    def is_playing(self) -> bool:
        """Indique si le thread de lecture est encore actif."""
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def play(self, setup: TtsSetup, slow: bool = False) -> None:
        """Arrête la lecture précédente puis démarre celle de ``setup`` en arrière-plan."""
        if setup.mode == "dicter" and len(setup.to_pronounce) != len(setup.list_gds):
            raise ValueError(
                "En mode dicter, to_pronounce et list_gds doivent avoir la même longueur."
            )
        audio_control.stop_all()
        ancien_thread = self._thread
        if ancien_thread is not None and ancien_thread is not threading.current_thread():
            ancien_thread.join()
        event = threading.Event()
        token = audio_control.new_generation()
        with self._lock:
            self._stop_event = event
            self._active_generation = token
            thread = threading.Thread(
                target=self._play_setup,
                args=(setup, slow, event, token),
                name="TtsPlayer",
                daemon=True,
            )
            self._thread = thread
            thread.start()

    def stop(self) -> None:
        """Demande l'arrêt du thread et interrompt l'audio en cours."""
        with self._lock:
            event = self._stop_event
            event.set()
        try:
            self._stop_audio()
        except Exception:
            logger.exception("Échec lors de l'arrêt du moteur audio.")

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> float:
        """Limite une durée à l'intervalle inclusif indiqué."""
        return max(minimum, min(maximum, value))

    def _play_setup(
        self, setup: TtsSetup, slow: bool, event: threading.Event, token: int
    ) -> None:
        """Prépare les segments puis exécute l'algorithme du mode demandé."""
        try:
            if setup.lang is None or event.is_set() or not audio_control.is_current(token):
                return
            plan = self._build_plan(setup, slow)
            self._prepare(plan)
            if event.is_set() or not audio_control.is_current(token):
                return
            if setup.mode == "dicter":
                self._play_dicter(setup, slow, event)
            else:
                self._play_segments(plan, slow, event)
        except Exception:
            logger.exception("Erreur pendant la lecture du mode %r.", setup.mode)

    def _build_plan(self, setup: TtsSetup, slow: bool) -> list[tuple[str, str, int]]:
        """Construit le préchargement nécessaire au mode et à la vitesse."""
        lang = setup.lang or ""
        if setup.mode == "dicter":
            return [
                (text, lang, self.SPEED_NORMAL)
                for text in setup.to_pronounce
            ] + (
                [(text, lang, self.SPEED_SLOW) for text in setup.to_pronounce]
                if slow else []
            )
        speed = self.SPEED_SLOW if slow else self.SPEED_NORMAL
        return [(text, lang, speed) for text in setup.to_pronounce]

    def _play_segments(
        self,
        plan: list[tuple[str, str, int]],
        slow: bool,
        event: threading.Event,
    ) -> None:
        """Lit les modes lire, cacher et épeler avec leur pause fixe."""
        pause = self.PAUSE_SLOW if slow else self.PAUSE_NORMAL
        for text, lang, speed in plan:
            if event.is_set() or not audio_control.is_current(getattr(self, "_active_generation", -1)):
                break
            self._say(text, lang, speed)
            if event.is_set():
                break
            if event.wait(pause):
                break

    def _play_dicter(
        self,
        setup: TtsSetup,
        slow: bool,
        event: threading.Event,
    ) -> None:
        """Lit chaque groupe en espaçant les pauses selon sa longueur."""
        assert setup.lang is not None
        factor = self.PAUSE_FACT_SLOW if slow else self.PAUSE_FACT_NORMAL
        for index, text in enumerate(setup.to_pronounce):
            if event.is_set() or not audio_control.is_current(
                getattr(self, "_active_generation", -1)
            ):
                break
            self._say(text, setup.lang, self.SPEED_NORMAL)
            if event.is_set():
                break
            if slow:
                if event.wait(self.PAUSE_REPEAT):
                    break
                if event.is_set():
                    break
                self._say(text, setup.lang, self.SPEED_SLOW)
                if event.is_set():
                    break
            pause = self._clamp(
                len(setup.list_gds[index]) * factor,
                self.PAUSE_MIN,
                self.PAUSE_MAX,
            )
            if event.wait(pause):
                break
