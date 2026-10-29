"""Modes métier MAEL, compatibles avec les chaînes historiques."""
from enum import StrEnum


class Mode(StrEnum):
    LIRE = "lire"
    DICTER = "dicter"
    CACHER = "cacher"
    EPELER = "epeler"
