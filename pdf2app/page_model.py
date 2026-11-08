"""Modèle d'une page du lecteur généré."""
from dataclasses import dataclass, field
from .qr_geometry import QrZone

@dataclass(slots=True)
class PageAsset:
    """Image et zones QR d'une page ; conserve les erreurs sans interrompre le lot."""
    index: int
    avif_base64: str
    width: int
    height: int
    zones: list[QrZone] = field(default_factory=list)
    error: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {"index": self.index, "image": self.avif_base64, "width": self.width,
                "height": self.height, "zones": [z.as_dict() for z in self.zones], "error": self.error}
