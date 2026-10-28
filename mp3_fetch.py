"""Aiguillage d’un CloudItem vers l’URL et le lecteur MP3."""
from __future__ import annotations

from typing import Any

import dico_url
from qr_dto import CloudItem
from mp3_read import Mp3Reader, create_mp3_reader


class Mp3Fetch:
    """Reconstruit l’URL cloud puis la confie au lecteur MP3."""

    def __init__(self, mp3_read: Mp3Reader | None = None) -> None:
        self.mp3_read = mp3_read or create_mp3_reader()

    def fetch(self, cloud_item: CloudItem) -> str:
        """Lance la lecture du fichier référencé et retourne son URL."""
        if not isinstance(cloud_item, CloudItem):
            raise TypeError("fetch attend un CloudItem.")
        url = dico_url.build_url(cloud_item)
        self.mp3_read.play(url)
        return url

    def stop(self) -> None:
        """Arrête la lecture MP3 en cours."""
        self.mp3_read.stop()

    @property
    def is_playing(self) -> bool:
        """Indique si le lecteur MP3 est actif."""
        return self.mp3_read.is_playing
