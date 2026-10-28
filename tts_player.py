"""Contrat commun des moteurs de synthèse vocale."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TtsPlayer(ABC):
    """Définit la synthèse d'un texte vers un fichier MP3 temporaire."""

    @abstractmethod
    def synthesize(self, text: str, lang: str, slow: bool = False) -> str:
        """Crée ou retrouve un MP3 et renvoie son chemin."""
        raise NotImplementedError
