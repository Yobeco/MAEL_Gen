"""Configuration de génération du lecteur PDF autonome."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Pdf2AppConfig:
    """Réglages du scan PDF et de l'encodage des pages."""
    dpi: int = 250
    fallback_dpi: int = 400
    display_dpi: int = 96
    avif_quality: int = 30
    avif_speed: int = 6
    max_width: int | None = None
    verbose: bool = True

    def __post_init__(self) -> None:
        if self.dpi <= 0 or self.fallback_dpi <= 0 or self.display_dpi <= 0:
            raise ValueError("Les DPI doivent être strictement positifs.")
        if not 0 <= self.avif_quality <= 100:
            raise ValueError("avif_quality doit être entre 0 et 100.")
        if not 0 <= self.avif_speed <= 10:
            raise ValueError("avif_speed doit être entre 0 et 10.")
        if self.max_width is not None and self.max_width < 1:
            raise ValueError("max_width doit être positif ou None.")
