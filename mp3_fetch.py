"""Construction d'URL et téléchargement de MP3 cloud, sans lecture."""
from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

import dico_url
from qr_dto import CloudItem

logger = logging.getLogger(__name__)


class Mp3Fetch:
    """Télécharge un CloudItem vers un fichier MP3 temporaire."""

    DEFAULT_MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024

    def __init__(self, *, timeout: float = 30.0,
                 max_download_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
                 opener: Callable[..., Any] | None = None,
                 on_download_start: Callable[[], None] | None = None,
                 on_download_end: Callable[[], None] | None = None) -> None:
        self.timeout = timeout
        self.max_download_bytes = max_download_bytes
        self._opener = opener or urlopen
        self.on_download_start = on_download_start
        self.on_download_end = on_download_end

    def fetch(self, cloud_item: CloudItem) -> str:
        """Construit l'URL, télécharge le MP3 et renvoie le chemin temporaire."""
        if not isinstance(cloud_item, CloudItem):
            raise TypeError("fetch attend un CloudItem.")
        url = dico_url.build_url(cloud_item)
        request = Request(url, headers={"User-Agent": "MAEL-Scan/1.0"})
        temporary: str | None = None
        started = False
        try:
            if self.on_download_start:
                self.on_download_start()
            started = True
            fd, temporary = tempfile.mkstemp(prefix="mael_cloud_", suffix=".mp3")
            size = 0
            with os.fdopen(fd, "wb") as output:
                with self._opener(request, timeout=self.timeout) as response:
                    length = response.headers.get("Content-Length")
                    if length and int(length) > self.max_download_bytes:
                        raise ValueError(f"Fichier MP3 trop volumineux (limite {self.max_download_bytes} octets).")
                    while True:
                        chunk = response.read(min(64 * 1024, self.max_download_bytes - size + 1))
                        if not chunk:
                            break
                        size += len(chunk)
                        if size > self.max_download_bytes:
                            raise ValueError(f"Fichier MP3 trop volumineux (limite {self.max_download_bytes} octets).")
                        output.write(chunk)
            return temporary
        except Exception:
            if temporary and Path(temporary).exists():
                Path(temporary).unlink()
            raise
        finally:
            if started and self.on_download_end:
                try:
                    self.on_download_end()
                except Exception:
                    logger.exception("Erreur du callback de fin de téléchargement MP3.")
