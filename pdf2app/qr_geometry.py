"""Conversion des quadrilatères QR en zones carrées relatives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class QrZone:
    """Zone cliquable dont les quatre mesures sont des fractions de page."""
    x: float
    y: float
    width: float
    height: float

    def as_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

def quad_to_square(position: Any, page_width: int | float, page_height: int | float) -> QrZone:
    """Englobe un quad par un carré centré et le normalise en 0..1."""
    if page_width <= 0 or page_height <= 0:
        raise ValueError("Les dimensions de page doivent être positives.")
    names = ("top_left", "top_right", "bottom_right", "bottom_left")
    points = [(float(getattr(position, n).x), float(getattr(position, n).y)) for n in names]
    left = min(p[0] for p in points); right = max(p[0] for p in points)
    top = min(p[1] for p in points); bottom = max(p[1] for p in points)
    side = max(right - left, bottom - top)
    if side <= 0:
        raise ValueError("Le quadrilatère QR est de taille nulle.")
    cx = (left + right) / 2; cy = (top + bottom) / 2
    return QrZone((cx - side / 2) / page_width, (cy - side / 2) / page_height,
                  side / page_width, side / page_height)
