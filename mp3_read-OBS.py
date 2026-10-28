"""Lecteur MP3 asynchrone et propriétaire de la sortie audio."""
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
    """Lit des fichiers en arrière-plan, avec invalidation par génération."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._done = threading.Event()
        self._device: Any = None
        self._generation = 0

    @property
    def is_playing(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def play(self, path: str) -> None:
        """Arrête le son courant puis démarre le fichier demandé."""
        if not isinstance(path, (str, os.PathLike)) or not Path(path).is_file():
            raise ValueError("Le chemin MP3 doit désigner un fichier existant.")
        self.stop()
        with self._lock:
            self._generation += 1
            generation = self._generation
            event = threading.Event()
            done = threading.Event()
            self._stop_event, self._done = event, done
            thread = threading.Thread(
                target=self._play_file, args=(str(path), generation, event, done),
                name="Mp3Reader", daemon=True,
            )
            self._thread = thread
            thread.start()

    def stop(self) -> None:
        """Interrompt le son courant et invalide son thread de lecture."""
        with self._lock:
            self._generation += 1
            event, done, device = self._stop_event, self._done, self._device
            self._device = None
            event.set()
            done.set()
        self._close_device(device)

    def wait(self, timeout: float | None = None) -> bool:
        """Attend la fin (ou l'interruption) du son courant; renvoie True si fini."""
        with self._lock:
            done = self._done
        return done.wait(timeout)

    def _current(self, generation: int, event: threading.Event) -> bool:
        with self._lock:
            return generation == self._generation and not event.is_set()

    def _play_file(self, path: str, generation: int, event: threading.Event,
                   done: threading.Event) -> None:
        device = stream = None
        try:
            import miniaudio
            decoded = miniaudio.decode_file(path)
            if not self._current(generation, event):
                return
            ended = threading.Event()

            def pcm_stream():
                frame = 0
                try:
                    requested = yield b""
                    while self._current(generation, event) and frame < decoded.num_frames:
                        count = min(requested, decoded.num_frames - frame)
                        if count <= 0:
                            requested = yield b""
                            continue
                        first, last = frame * decoded.nchannels, (frame + count) * decoded.nchannels
                        frame += count
                        requested = yield decoded.samples[first:last].tobytes()
                finally:
                    ended.set()

            stream = pcm_stream()
            next(stream)
            device = miniaudio.PlaybackDevice(
                output_format=decoded.sample_format, nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate,
            )
            with self._lock:
                if generation != self._generation or event.is_set():
                    return
                self._device = device
                device.start(stream)
            ended.wait()
        except Exception:
            if self._current(generation, event):
                logger.exception("Impossible de lire le MP3 : %s", path)
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
            # Seuls les fichiers temporaires téléchargés par Mp3Fetch sont détruits.
            if Path(path).name.startswith("mael_cloud_") and Path(path).suffix == ".mp3":
                try:
                    Path(path).unlink(missing_ok=True)
                except OSError:
                    logger.warning("Impossible de supprimer le MP3 temporaire %s", path)
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
    return MiniaudioMp3Reader(**kwargs)
