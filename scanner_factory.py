"""Fabrique à chargement différé des implémentations de scanner."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qr_scan import QrScanner


def create_scanner(hw: str | None = None, **kwargs: Any) -> "QrScanner":
    """Crée le scanner demandé; les modules matériels sont importés au besoin."""
    selected = hw if hw is not None else (os.environ.get("MAEL_HW") or "pc_virtual")
    if selected == "pc_pdf":
        from qr_scan import ImageScanner
        return ImageScanner(**kwargs)
    if selected == "pc_virtual":
        from qr_scan_virtual import VirtualScanner
        return VirtualScanner(**kwargs)
    if selected in {"rpi", "android", "ios", "web"}:
        raise NotImplementedError(f"Le scanner pour le hardware {selected!r} n'est pas implémenté.")
    raise ValueError(f"Hardware inconnu : {selected!r}")
