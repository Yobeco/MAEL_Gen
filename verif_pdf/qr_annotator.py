"""Annotation graphique des codes QR sur les images."""
from __future__ import annotations
from pathlib import Path
from .render_constants import *
from .qr_detector import QrDetector, qr_scan_and_parse

def annotate_qr_codes(
    image_path: str | Path,
    output_path: str | Path,
    page_number: int | None = None,
    detector: "QrDetector | None" = None,
) -> Path:
    """
    Écrit une copie de l'image avec, pour chaque QR code :
      - un quadrilatère coloré (couleur selon le mode),
      - un numéro à deux chiffres incrusté au centre.

    Tous les paramètres visuels sont lus depuis les constantes de rendu.
    """
    import cv2
    import numpy as np

    src = Path(image_path).resolve()
    dst = Path(output_path).resolve()

    img = cv2.imread(str(src))
    if img is None:
        raise ValueError(f"Impossible de lire l'image: {src}")

    qr_items = qr_scan_and_parse(src, page_number=page_number, detector=detector)

    for i, qr in enumerate(qr_items, 1):
        pos = qr.position
        color = qr.color_bgr

        pts = np.array(
            [
                [pos.top_left.x, pos.top_left.y],
                [pos.top_right.x, pos.top_right.y],
                [pos.bottom_right.x, pos.bottom_right.y],
                [pos.bottom_left.x, pos.bottom_left.y],
            ],
            dtype=np.int32,
        ).reshape((-1, 1, 2))

        cv2.polylines(
            img, [pts], isClosed=True,
            color=color,
            thickness=QR_FRAME_THICKNESS,
            lineType=cv2.LINE_AA,
        )

        cx = (pos.top_left.x + pos.top_right.x
              + pos.bottom_right.x + pos.bottom_left.x) / 4.0
        cy = (pos.top_left.y + pos.top_right.y
              + pos.bottom_right.y + pos.bottom_left.y) / 4.0

        side_top = np.hypot(pos.top_right.x - pos.top_left.x,
                            pos.top_right.y - pos.top_left.y)
        side_left = np.hypot(pos.bottom_left.x - pos.top_left.x,
                             pos.bottom_left.y - pos.top_left.y)
        qr_size = (side_top + side_left) / 2.0

        target_height_px = qr_size * QR_NUMBER_SCALE_RATIO
        font_scale = max(0.5, target_height_px / 22.0)
        text_thickness = max(2, int(round(font_scale * 3)))

        label = f"{i:02d}"
        (text_w, text_h), _baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness
        )
        text_x = int(cx - text_w / 2)
        text_y = int(cy + text_h / 2)

        cv2.putText(img, label, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                    (255, 255, 255), text_thickness + 4, cv2.LINE_AA)
        cv2.putText(img, label, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                    color, text_thickness, cv2.LINE_AA)

    dst.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(dst), img):
        raise IOError(f"Échec de l'écriture: {dst}")

    return dst

class QrAnnotator:
    """Applique cadres et numéros à une image de page."""
    def annotate(self, image_path: str | Path, output_path: str | Path, *, page_number: int | None = None, detector: QrDetector | None = None) -> Path:
        """Annote une image et retourne le chemin du PNG produit."""
        return annotate_qr_codes(image_path, output_path, page_number=page_number, detector=detector)
