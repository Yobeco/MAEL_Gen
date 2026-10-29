"""Contrat commun des moteurs de synthèse vocale."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TtsPlayer(ABC):
    """Définit la synthèse d'un texte vers un fichier MP3 temporaire.

    La vitesse est un pourcentage entier (100 = normale, 80 = lente).
    Chaque implémentation le convertit selon les capacités de son moteur :
    un moteur continu peut utiliser ``speed / 100`` comme facteur (1 = 100 %,
    borné entre 0 et 2), tandis que gTTS ne propose que lent/normal.
    """

    @staticmethod
    def _speed_factor(speed: int) -> float:
        """Convertit un pourcentage en facteur moteur borné entre 0 et 2."""
        return max(0.0, min(2.0, speed / 100.0))

    @abstractmethod
    def synthesize(self, text: str, lang: str, speed: int = 100) -> str:
        """Crée ou retrouve un MP3 à la vitesse demandée et renvoie son chemin."""
        raise NotImplementedError
