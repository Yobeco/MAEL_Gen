"""Encodage AVIF via Pillow natif ou pillow-avif-plugin."""
from __future__ import annotations
from io import BytesIO
from PIL import Image

class AvifEncoder:
    """Encode des pages AVIF et expose les dimensions finales."""
    def __init__(self, quality: int = 30, speed: int = 6, max_width: int | None = None) -> None:
        self.quality, self.speed, self.max_width = quality, speed, max_width

    def encode(self, path: str, dpi: int) -> tuple[bytes, int, int]:
        """Ouvre une image, la réduit au besoin, puis la compresse en AVIF."""
        with Image.open(path) as source:
            image = source.convert("RGB")
        if self.max_width and image.width > self.max_width:
            height = max(1, round(image.height * self.max_width / image.width))
            image = image.resize((self.max_width, height), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        try:
            image.save(buffer, format="AVIF", quality=self.quality, speed=self.speed)
        except (KeyError, OSError) as exc:
            try:
                import pillow_avif  # noqa: F401 — enregistrement du plugin Pillow
                buffer = BytesIO()
                image.save(buffer, format="AVIF", quality=self.quality, speed=self.speed)
            except Exception as plugin_exc:
                raise RuntimeError("AVIF indisponible : installer Pillow>=11.2 ou pillow-avif-plugin.") from plugin_exc
        return buffer.getvalue(), image.width, image.height
