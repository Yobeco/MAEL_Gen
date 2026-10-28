"""Adaptateur gTTS avec cache en mémoire et lecture audio par miniaudio."""

from __future__ import annotations

import io
import logging
import threading
from typing import Any

from tts_player import TtsPlayer
import audio_control

logger = logging.getLogger(__name__)


class GttsPlayer(TtsPlayer):
    """Moteur gTTS léger, dont les dépendances sont importées à la demande.

    Installation des dépendances audio et de synthèse :
    ``pip install gTTS miniaudio``.
    """

    def __init__(self) -> None:
        """Initialise le cache sans charger gTTS ni miniaudio."""
        super().__init__()
        self._cache: dict[tuple[str, str, bool], bytes] = {}
        self._cache_lock = threading.RLock()
        self._device: Any = None
        self._playback_done: threading.Event | None = None
        self._device_lock = threading.RLock()

    def _prepare(self, items: list[tuple[str, str, int]]) -> None:
        """Synthétise les éléments requis et conserve les MP3 en mémoire."""
        from gtts import gTTS

        for text, lang, speed in items:
            # Ne lance pas de nouvelles synthèses si stop_all() a invalidé ce play.
            if self._stop_event.is_set() or not audio_control.is_current(
                getattr(self, "_active_generation", -1)
            ):
                return
            key = (text, lang, speed < self.SPEED_NORMAL)
            with self._cache_lock:
                if key in self._cache:
                    continue
                output = io.BytesIO()
                gTTS(text=text, lang=lang, slow=key[2]).write_to_fp(output)
                self._cache[key] = output.getvalue()

    @staticmethod
    def _close_device(device: Any) -> None:
        """Arrête puis ferme un périphérique, sans masquer l'erreur initiale."""
        if device is None:
            return
        try:
            device.stop()
        except Exception:
            logger.debug("Le périphérique miniaudio était déjà arrêté.", exc_info=True)
        try:
            device.close()
        except Exception:
            logger.exception("Impossible de fermer le périphérique miniaudio.")

    def _say(self, text: str, lang: str, speed: int) -> None:
        """Décode puis lit le MP3 de façon bloquante et interruptible."""
        import miniaudio

        key = (text, lang, speed < self.SPEED_NORMAL)
        with self._cache_lock:
            content = self._cache.get(key)
        if content is None:
            self._prepare([(text, lang, speed)])
            with self._cache_lock:
                content = self._cache[key]

        stop_event = self._stop_event
        if stop_event.is_set():
            return

        decoded = miniaudio.decode(content)
        finished = threading.Event()
        device = None

        def pcm_stream():
            """Yield decoded PCM blocks and signal natural end or interruption."""
            frame = 0
            total_frames = decoded.num_frames
            samples_per_frame = decoded.nchannels
            try:
                requested_frames = yield b""
                while not stop_event.is_set() and frame < total_frames:
                    count = min(requested_frames, total_frames - frame)
                    if count <= 0:
                        requested_frames = yield b""
                        continue
                    first = frame * samples_per_frame
                    last = (frame + count) * samples_per_frame
                    frame = frame + count
                    requested_frames = yield decoded.samples[first:last].tobytes()
            finally:
                finished.set()

        stream = pcm_stream()
        next(stream)  # miniaudio expects a generator primed before start().
        published = False
        try:
            if stop_event.is_set():
                return
            device = miniaudio.PlaybackDevice(
                output_format=decoded.sample_format,
                nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate,
            )
            # Keep start and publication atomic relative to _stop_audio: stop()
            # can then always find and close a started device.
            with self._device_lock:
                if stop_event.is_set():
                    return
                self._device = device
                self._playback_done = finished
                published = True
                device.start(stream)
            finished.wait()
        finally:
            try:
                stream.close()
            except Exception:
                pass
            with self._device_lock:
                if self._device is device:
                    self._device = None
                    owned_device = device
                else:
                    # _stop_audio already detached and is closing it.
                    owned_device = None
                if self._playback_done is finished:
                    self._playback_done = None
            self._close_device(owned_device)
            if not published:
                self._close_device(device)

    def _stop_audio(self) -> None:
        """Signale la fin et arrête/ferme immédiatement le périphérique actif."""
        # The base class also sets this event; setting it here makes this method
        # safe when called directly and wakes the playback stream promptly.
        self._stop_event.set()
        with self._device_lock:
            device = self._device
            done = self._playback_done
            self._device = None
        if done is not None:
            done.set()
        self._close_device(device)
