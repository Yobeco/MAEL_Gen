"""Contrat et implémentation miniaudio pour lire un MP3 distant."""
from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class Mp3Reader(ABC):
    """Contrat minimal d’un lecteur MP3 piloté par URL."""

    @abstractmethod
    def play(self, url: str) -> None:
        """Démarre la lecture de l’URL, sans bloquer l’appelant."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Interrompt la lecture et libère le périphérique audio."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_playing(self) -> bool:
        """Indique si le téléchargement ou la lecture est en cours."""
        raise NotImplementedError


class MiniaudioMp3Reader(Mp3Reader):
    """Lecteur non bloquant : récupère le MP3 en mémoire, puis le décode."""

    DEFAULT_MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024

    def __init__(self, *, timeout: float = 30.0,
                 max_download_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
                 opener: Callable[..., Any] | None = None) -> None:
        self.timeout = timeout
        self.max_download_bytes = max_download_bytes
        self._opener = opener or urlopen
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._device: Any = None
        self._playback_done: threading.Event | None = None

    @property
    def is_playing(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def play(self, url: str) -> None:
        """Arrête la lecture précédente, puis démarre le chargement en tâche de fond."""
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            raise ValueError("L’URL MP3 doit utiliser http ou https.")
        self.stop()
        previous = self._thread
        if previous is not None and previous is not threading.current_thread():
            previous.join()
        event = threading.Event()
        with self._lock:
            self._stop_event = event
            self._thread = threading.Thread(
                target=self._play_url, args=(url, event), name="Mp3Reader", daemon=True
            )
            self._thread.start()

    def stop(self) -> None:
        """Signale l’arrêt et ferme le périphérique audio courant."""
        self._stop_event.set()
        with self._lock:
            device = self._device
            done = self._playback_done
            self._device = None
        if done is not None:
            done.set()
        self._close_device(device)

    def _download(self, url: str, event: threading.Event) -> bytes:
        request = Request(url, headers={"User-Agent": "MAEL-Scan/1.0"})
        with self._opener(request, timeout=self.timeout) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > self.max_download_bytes:
                raise ValueError(
                    f"Fichier MP3 trop volumineux (limite {self.max_download_bytes} octets)."
                )
            chunks: list[bytes] = []
            size = 0
            while not event.is_set():
                chunk = response.read(min(64 * 1024, self.max_download_bytes - size + 1))
                if not chunk:
                    break
                size += len(chunk)
                if size > self.max_download_bytes:
                    raise ValueError(
                        f"Fichier MP3 trop volumineux (limite {self.max_download_bytes} octets)."
                    )
                chunks.append(chunk)
            if event.is_set():
                return b""
            return b"".join(chunks)

    def _play_url(self, url: str, event: threading.Event) -> None:
        device = None
        stream = None
        finished = None
        try:
            content = self._download(url, event)
            if event.is_set() or not content:
                return
            import miniaudio

            decoded = miniaudio.decode(content)
            finished = threading.Event()

            def pcm_stream():
                frame = 0
                total_frames = decoded.num_frames
                samples_per_frame = decoded.nchannels
                try:
                    requested_frames = yield b""
                    while not event.is_set() and frame < total_frames:
                        count = min(requested_frames, total_frames - frame)
                        if count <= 0:
                            requested_frames = yield b""
                            continue
                        first = frame * samples_per_frame
                        last = (frame + count) * samples_per_frame
                        frame += count
                        requested_frames = yield decoded.samples[first:last].tobytes()
                finally:
                    finished.set()

            stream = pcm_stream()
            next(stream)
            if event.is_set():
                return
            device = miniaudio.PlaybackDevice(
                output_format=decoded.sample_format,
                nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate,
            )
            with self._lock:
                if event.is_set():
                    return
                self._device = device
                self._playback_done = finished
                device.start(stream)
            finished.wait()
        except Exception:
            if not event.is_set():
                logger.exception("Impossible de récupérer ou lire le MP3 : %s", url)
        finally:
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    pass
            with self._lock:
                owned_device = device if self._device is device else None
                if self._device is device:
                    self._device = None
                if self._playback_done is finished:
                    self._playback_done = None
            self._close_device(owned_device)

    @staticmethod
    def _close_device(device: Any) -> None:
        if device is None:
            return
        try:
            device.stop()
        except Exception:
            logger.debug("Le périphérique audio était déjà arrêté.", exc_info=True)
        try:
            device.close()
        except Exception:
            logger.exception("Impossible de fermer le périphérique miniaudio.")


def create_mp3_reader(**kwargs: Any) -> Mp3Reader:
    """Fabrique le lecteur configuré pour la plateforme actuelle."""
    return MiniaudioMp3Reader(**kwargs)
