"""Contrôle audio global, thread-safe et indépendant du matériel audio."""
from __future__ import annotations

import threading
from abc import ABC, abstractmethod


class StoppablePlayback(ABC):
    """Interface abstraite minimale d'un lecteur interruptible."""

    @abstractmethod
    def stop(self) -> None: ...

    @property
    @abstractmethod
    def is_playing(self) -> bool: ...


class AudioControl:
    """Registre partagé des lecteurs et jeton de génération pour annulation."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._players: set[StoppablePlayback] = set()
        self._generation = 0

    def register(self, player: StoppablePlayback) -> StoppablePlayback:
        if not callable(getattr(player, "stop", None)) or not hasattr(player, "is_playing"):
            raise TypeError("Un lecteur doit exposer stop() et is_playing.")
        with self._lock:
            self._players.add(player)
        return player

    def unregister(self, player: StoppablePlayback) -> None:
        with self._lock:
            self._players.discard(player)

    def stop_all(self) -> None:
        """Invalide les opérations en cours puis arrête tous les lecteurs inscrits."""
        with self._lock:
            self._generation += 1
            players = tuple(self._players)
        for player in players:
            try:
                player.stop()
            except Exception:
                # Un lecteur défaillant ne doit pas empêcher l'arrêt des autres.
                import logging
                logging.getLogger(__name__).exception("Échec d'arrêt d'un lecteur audio.")

    def new_generation(self) -> int:
        with self._lock:
            self._generation += 1
            return self._generation

    def is_current(self, token: int) -> bool:
        with self._lock:
            return token == self._generation


_manager = AudioControl()
register = _manager.register
unregister = _manager.unregister
stop_all = _manager.stop_all
new_generation = _manager.new_generation
is_current = _manager.is_current
