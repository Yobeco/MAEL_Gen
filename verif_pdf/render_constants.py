"""Constantes de présentation du pipeline PDF."""
from __future__ import annotations

from qr_parse import (
    MODE_LIRE, MODE_DICTER, MODE_EPELER, MODE_GD, MODE_NC, MODE_LS,
    MODE_WIFI, MODES_CLOUD,
)

# Modifiez-les ici, et uniquement ici.

# --- Libellés et symboles ---------------------------------------------
LABELS_TEXT: dict[str, str] = {
    MODE_GD: "♫ Google Drive",
    MODE_NC: "♫ NextCloud",
    MODE_LS: "♫ La Suite",
    MODE_WIFI: "Wifi",
}
LEGEND_ARROW = "►"               # sépare le n° du contenu : "01 ► Bonjour"
LANG_ARROW = "→"                 # sépare la langue du payload : "fr → Bonjour"

# --- Couleurs (BGR pour OpenCV, RGB pour fpdf2) -----------------------
# Indexées par mode : "lire", "dicter", "epeler", cloud et wifi
COLORS_BGR: dict[str, tuple[int, int, int]] = {
    MODE_LIRE:   (255, 0, 0),      # bleu (défaut)
    MODE_DICTER: (0, 0, 255),      # rouge
    MODE_EPELER: (0, 100, 0),      # vert foncé
    MODE_GD:     (180, 105, 255),  # rose (hot pink)
    MODE_NC:     (180, 105, 255),  # rose (hot pink)
    MODE_LS:     (180, 105, 255),  # rose (hot pink)
    MODE_WIFI:   (80, 80, 80),     # gris foncé
}

COLORS_RGB: dict[str, tuple[int, int, int]] = {
    MODE_LIRE:   (0, 0, 255),
    MODE_DICTER: (255, 0, 0),
    MODE_EPELER: (0, 100, 0),
    MODE_GD:     (255, 105, 180),
    MODE_NC:     (255, 105, 180),
    MODE_LS:     (255, 105, 180),
    MODE_WIFI:   (80, 80, 80),
}

# --- Annotation de l'image (OpenCV) -----------------------------------
QR_FRAME_THICKNESS = 3           # épaisseur du cadre autour de chaque QR
QR_NUMBER_SCALE_RATIO = 0.40     # hauteur du numéro / taille du QR (0.40 = 40 %)

# --- Labels superposés sur l'image (fpdf2) ----------------------------
LABEL_FONT_SIZE = 32             # taille de police des labels
LABEL_TEXT_OFFSET = 8            # marge verticale au-dessus du QR
LABEL_MARGIN = 6.0               # marge blanche min. entre deux labels
                                 # (utilisée uniquement pour le décalage,
                                 #  pas pour la troncature)
LABEL_SHIFT_STEP = None          # pas de décalage (None → utilise LABEL_FONT_SIZE)
LABEL_SHIFT_MAX_UP = 8           # nb max de pas vers le haut
LABEL_SHIFT_MAX_DOWN = 4         # nb max de pas vers le bas
LABEL_BG = True                  # activer un fond blanc derrière le label
LABEL_BG_ALPHA = 0.7             # opacité du fond (0.0 → 1.0)
LABEL_BG_PADDING = 3.0           # marge intérieure du fond
LABEL_PAGE_MARGIN = 4.0          # marge de sécurité avec le bord droit
                                 # (sous laquelle on tronque)

# --- Bandeau de légende en bas du PDF (fpdf2) -------------------------
LEGEND_FONT_SIZE = 32            # taille de police de la légende
LEGEND_LINE_HEIGHT = 60          # hauteur d'une ligne de légende
LEGEND_PADDING = 20              # marge intérieure du bandeau
LEGEND_SEPARATOR = True          # trait de séparation entre deux lignes
LEGEND_SEPARATOR_COLOR = (200, 200, 200)   # gris clair
LEGEND_SEPARATOR_WIDTH = 0.5     # épaisseur du trait en points


# ======================================================================
