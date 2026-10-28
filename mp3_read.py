"""Lecteur MP3 local asynchrone, avec arrêt coopératif de la sortie audio."""
from __future__ import annotations

import logging
import os
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Mp3Reader(ABC):
    """Contrat du lecteur MP3 : démarrer, arrêter, inspecter et attendre."""

    @abstractmethod
    def play(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_playing(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def wait(self, timeout: float | None = None) -> bool:
        raise NotImplementedError


class MiniaudioMp3Reader(Mp3Reader):
    """Lit un fichier MP3 local via miniaudio (le téléchargement est externe)."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._stop_event.set()
        self._done = threading.Event()
        self._done.set()
        self._device: Any = None

    @property
    def is_playing(self) -> bool:
        with self._lock:
            done = self._done
        return not done.is_set()

    def play(self, path: str) -> None:
        """Démarre la lecture d'un fichier MP3 local existant."""
        if not isinstance(path, (str, os.PathLike)):
            raise ValueError("Le chemin MP3 doit désigner un fichier local existant.")
        file_path = Path(path)
        if file_path.suffix.lower() != ".mp3" or not file_path.is_file():
            raise ValueError("Le chemin MP3 doit désigner un fichier local .mp3 existant.")

        self.stop()
        event = threading.Event()
        done = threading.Event()
        thread = threading.Thread(
            target=self._play_file,
            args=(str(file_path), event, done),
            name="Mp3Reader",
            daemon=True,
        )
        with self._lock:
            self._stop_event = event
            self._done = done
            self._thread = thread
        thread.start()

    def stop(self) -> None:
        """Demande l'arrêt, ferme la sortie et attend le thread au plus 0,5 s."""
        with self._lock:
            event, thread, device = self._stop_event, self._thread, self._device
            event.set()
            if self._device is device:
                self._device = None
        # Aucun appel miniaudio (y compris stop/close) ne se fait sous _lock.
        self._close_device(device)
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=0.5)

    def wait(self, timeout: float | None = None) -> bool:
        """Attend la fin de la lecture courante; True signifie qu'elle est terminée."""
        with self._lock:
            done = self._done
        return done.wait(timeout)

    def _play_file(self, path: str, event: threading.Event,
                   done: threading.Event) -> None:
        device = stream = None
        ended = threading.Event()
        try:
            import miniaudio

            decoded = miniaudio.decode_file(path)
            if event.is_set():
                return

            def pcm_stream():
                # Callback miniaudio : volontairement indépendant de tout verrou.
                frame = 0
                requested = yield b""
                try:
                    while not event.is_set() and frame < decoded.num_frames:
                        count = min(requested, decoded.num_frames - frame)
                        if count <= 0:
                            requested = yield b""
                            continue
                        first = frame * decoded.nchannels
                        last = (frame + count) * decoded.nchannels
                        frame += count
                        requested = yield decoded.samples[first:last].tobytes()
                finally:
                    ended.set()

            stream = pcm_stream()
            next(stream)
            device = miniaudio.PlaybackDevice(
                output_format=decoded.sample_format,
                nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate,
            )
            with self._lock:
                if event.is_set():
                    return
                self._device = device

            # start peut exécuter le callback synchrone; ne jamais le tenir sous _lock.
            device.start(stream)
            if not event.is_set():
                ended.wait()
        except Exception:
            if not event.is_set():
                logger.exception("Impossible de lire le MP3 local : %s", path)
        finally:
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    pass
            with self._lock:
                owned = device if self._device is device else None
                if self._device is device:
                    self._device = None
            self._close_device(owned)
            # Mp3Fetch nomme ses temporaires mael_cloud_*.mp3; les autres fichiers
            # locaux appartiennent à l'appelant et ne sont jamais supprimés.
            candidate = Path(path)
            if candidate.name.startswith("mael_cloud_") and candidate.suffix.lower() == ".mp3":
                try:
                    candidate.unlink(missing_ok=True)
                except OSError:
                    logger.warning("Impossible de supprimer le MP3 temporaire %s", candidate)
            done.set()

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
            logger.exception("Impossible de fermer le périphérique audio.")


def create_mp3_reader(**kwargs: Any) -> Mp3Reader:
    """Crée le lecteur matériel à chargement différé."""
    if kwargs:
        raise TypeError("create_mp3_reader n'accepte aucun argument.")
    return MiniaudioMp3Reader()
