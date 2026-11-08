"""Configuration immuable du traitement PDF."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    """Paramètres du processus PDF."""
    dpi: int = 250
    fallback_dpi: int = 400
    verbose: bool = True
