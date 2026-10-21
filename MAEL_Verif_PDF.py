"""
MAEL_Verif_PDF.py — Traitement de PDF multi-page pour la détection,
l'annotation et la légende de codes QR.

Workflow :
  1. Conversion du PDF d'entrée en PNG (un par page, DPI configurable).
  2. Pour chaque page : détection des QR (via qr_scan), analyse
     sémantique (via qr_parse), tri naturel (déjà fait par qr_parse),
     annotation de l'image, génération d'un PDF page avec textes
     sélectionnables et bandeau de légende.
  3. Fusion des PDF page en un seul PDF de sortie.

Architecture en couches :
  - qr_scan     : acquisition bas niveau (image → list[RawQr])
  - qr_parse    : analyse sémantique (list[RawQr] → list[TtsItem])
  - qr_dto      : DTO immuables partagés (RawQr, TtsItem)
  - ce module   : orchestration, enrichissement couleur, rendu PDF

Tout ce qui touche au RENDU VISUEL est défini dans la section
« Constantes de rendu » ci-dessous. C'est l'unique source de vérité.

Règle de troncature : un label superposé n'est tronqué QUE s'il dépasse
le bord droit de la page PDF. Les chevauchements entre labels sont
acceptés (compensés visuellement par le fond blanc semi-transparent et,
si possible, par un décalage vertical).

Note sur le fallback DPI :
  Si une page ne contient aucun QR à basse résolution, elle est
  reconvertie à plus haute résolution pour tenter une seconde détection
  (utile pour les QR imprimés en petit). Le PNG haute résolution n'est
  CONSERVÉ que s'il a effectivement permis la détection. Sinon, on
  revient au PNG d'origine pour garder des pages de taille homogène
  dans le PDF final.
"""

from __future__ import annotations

import sys
import tempfile
import shutil
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from fpdf import FPDF
from pypdf import PdfWriter
import pypdfium2 as pdfium

# Nouvelle architecture : trois modules autonomes
from qr_dto import TtsItem, CloudItem, WifiItem
from qr_scan import ImageScanner, ScanError
from qr_parse import (
    parse_all,
    MODE_LIRE, MODE_DICTER, MODE_EPELER, MODE_GD, MODE_NC, MODE_LS,
    MODE_WIFI, MODES_CLOUD,
)


# ======================================================================
# Constantes de rendu — SOURCE UNIQUE DE VÉRITÉ
# ======================================================================
# Toutes les valeurs ci-dessous définissent l'apparence finale du PDF.
# Modifiez-les ici, et uniquement ici.

# --- Libellés et symboles ---------------------------------------------
LABELS_TEXT: dict[str, str] = {
    MODE_GD: "♫ Google Drive",
    MODE_NC: "♫ NextCloud",
    MODE_LS: "♫ La Suite",
    MODE_WIFI: "Wifi",
}
LEGEND_ARROW = "►"               # sépare le n° du contenu : "01 ► Bonjour"

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
# DTO enrichi — associe un TtsItem à ses couleurs de rendu
# ======================================================================
@dataclass(frozen=True, slots=True)
class ColoredTtsItem:
    """
    Objet de rendu local : associe un `TtsItem` (objet métier neutre) aux
    couleurs nécessaires à l'affichage (cadre OpenCV, label fpdf2).

    Ce DTO est **local à ce module** : il ne fait pas partie du contrat
    partagé (qr_dto). Il matérialise la frontière entre la couche
    « données métier » et la couche « présentation ».

    Permet d'éviter de polluer `TtsItem` avec des préoccupations de
    couleur, conformément à la séparation des responsabilités.
    """

    item: TtsItem | CloudItem | WifiItem
    color_bgr: tuple[int, int, int]
    color_rgb: tuple[int, int, int]

    # Raccourcis pratiques pour le rendu, évitant d'écrire
    # `colored.item.raw.position` partout.
    @property
    def position(self):
        return self.item.raw.position

    @property
    def mode(self) -> str:
        return self.item.mode

    @property
    def text(self) -> str:
        return self.item.text


# ======================================================================
# Couche présentation : enrichissement couleur d'un TtsItem
# ======================================================================
def color_choose(item: TtsItem | CloudItem | WifiItem) -> ColoredTtsItem:
    """
    Enrichit un `TtsItem` avec les couleurs de rendu correspondant à son
    mode. Retourne un `ColoredTtsItem` (objet de rendu local).

    Fonction pure : n'altère pas l'item d'origine (qui est de toute
    façon immuable).
    """
    mode = item.mode
    return ColoredTtsItem(
        item=item,
        color_bgr=COLORS_BGR[mode],
        color_rgb=COLORS_RGB[mode],
    )


def qr_scan_and_parse(
    image_path: str | Path,
    page_number: int | None = None,
) -> list[ColoredTtsItem]:
    """
    Point d'entrée unique du pipeline pour ce module :
        1. Scan bas niveau via qr_scan (image → list[RawQr]).
        2. Analyse sémantique via qr_parse (RawQr → TtsItem, tri inclus).
        3. Enrichissement couleur local (TtsItem → ColoredTtsItem).

    Retourne une liste éventuellement vide. Lève `ScanError` si
    l'acquisition échoue (fichier absent, image illisible…). Un QR dont
    l'analyse échoue est ignoré individuellement.
    """
    scanner = ImageScanner()
    raws = scanner.scan(image_path)

    # Chaque QR passe par qr_parse, y compris les QR WIFI.
    # Le try/except reste isolé afin qu'un QR invalide n'arrête pas la page.
    items = []
    for qr_number, raw in enumerate(raws, 1):
        try:
            items.extend(parse_all([raw]))
        except Exception:
            if page_number is not None:
                # Ne jamais afficher le contenu du QR : un mot de passe WIFI
                # pourrait y figurer.
                print(f"[error] page {page_number}: QR #{qr_number} ignoré (analyse invalide)")

    return [color_choose(item) for item in items]


# ======================================================================
# Annotation de l'image : cadres colorés + numéro au centre
# ======================================================================
def annotate_qr_codes(
    image_path: str | Path,
    output_path: str | Path,
    page_number: int | None = None,
) -> Path:
    """
    Écrit une copie de l'image avec, pour chaque QR code :
      - un quadrilatère coloré (couleur selon le mode),
      - un numéro à deux chiffres incrusté au centre.

    Tous les paramètres visuels sont lus depuis les constantes de rendu.
    """
    src = Path(image_path).resolve()
    dst = Path(output_path).resolve()

    img = cv2.imread(str(src))
    if img is None:
        raise ValueError(f"Impossible de lire l'image: {src}")

    qr_items = qr_scan_and_parse(src, page_number=page_number)

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


# ======================================================================
# Recherche de la police TrueType embarquée dans l'application
# ======================================================================
def _find_utf8_font() -> Path:
    """Retourne le chemin de la police TrueType embarquée."""
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent

    font_path = base / "assets" / "fonts" / "DejaVuSans.ttf"
    if not font_path.exists():
        raise FileNotFoundError(
            f"Police introuvable : {font_path}\n"
            "Assurez-vous que 'assets/fonts/DejaVuSans.ttf' est bien présent."
        )
    return font_path


# ======================================================================
#      Génération du PDF : image + labels + bandeau de légendes
# ======================================================================
def _display_text_for(qr: ColoredTtsItem) -> str:
    """
    Retourne le texte à afficher pour un QR donné.

    - modes cloud et Wifi : on affiche le libellé de LABELS_TEXT.
    - autres : on affiche `text` tel quel.
    """
    if qr.mode in MODES_CLOUD or qr.mode == MODE_WIFI:
        return LABELS_TEXT[qr.mode]
    return qr.text


def generate_pdf_from_annotated_image(
    image_path: str | Path,
    output_pdf_path: str | Path,
    source_image_path: str | Path | None = None,
    verbose: bool = True,
) -> Path:
    """
    Génère un PDF page avec l'image annotée en fond, les labels
    sélectionnables superposés, et le bandeau de légende.

    Tous les paramètres visuels sont lus depuis les constantes de rendu.

    Règle de troncature : un label n'est tronqué QUE s'il dépasse le bord
    droit de la page (avec une marge de sécurité LABEL_PAGE_MARGIN). Les
    chevauchements entre labels ne déclenchent plus aucune troncature :
    ils sont compensés, quand c'est possible, par un décalage vertical.
    """
    def log(msg: str) -> None:
        if verbose:
            print(f"[PDF] {msg}")

    src = Path(image_path).resolve()
    dst = Path(output_pdf_path).resolve()

    log(f"Image source    : {src}")
    log(f"PDF destination : {dst}")

    # 1) Dimensions de l'image
    img = cv2.imread(str(src))
    if img is None:
        raise ValueError(f"Impossible de lire l'image: {src}")
    height, width = img.shape[:2]
    log(f"Dimensions      : {width} x {height} px")

    # 2) Détection / parsing / coloration
    #    Si une image source différente est fournie (cas PDF multi-page
    #    avec fallback DPI), on analyse cette dernière.
    detect_src = Path(source_image_path).resolve() if source_image_path else src
    qr_items = qr_scan_and_parse(detect_src)
    log(f"QR codes        : {len(qr_items)} détecté(s)")

    # 3) Bandeau de légende
    legend_height = 0
    if qr_items:
        legend_height = LEGEND_PADDING * 2 + LEGEND_LINE_HEIGHT * len(qr_items)
    total_height = height + legend_height
    log(f"Hauteur totale  : {total_height} pt "
        f"(image {height} + légende {legend_height})")

    # 4) Canvas PDF
    pdf = FPDF(orientation="P", unit="pt", format=(width, total_height))
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    pdf.image(str(src), x=0, y=0, w=width, h=height)

    # 5) Bandeau blanc sous l'image
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(x=0, y=height, w=width, h=legend_height, style="F")

    # 6) Police
    font_file = _find_utf8_font()
    log(f"Police          : {font_file}")
    pdf.add_font("QRFont", "", str(font_file))
    pdf.set_font("QRFont", size=LABEL_FONT_SIZE)

    # ------------------------------------------------------------------
    # 7) Helpers de placement des labels
    # ------------------------------------------------------------------
    def _label_box(x: float, y_baseline: float, text: str) -> tuple[float, float, float, float]:
        """Retourne la boîte englobante approximative d'un label."""
        w = pdf.get_string_width(text)
        return (x, y_baseline - LABEL_FONT_SIZE * 0.80,
                x + w, y_baseline + LABEL_FONT_SIZE * 0.20)

    def _overlaps(b1, b2, margin: float) -> bool:
        x1, y1, x2, y2 = b1
        X1, Y1, X2, Y2 = b2
        return not (x2 + margin <= X1 or X2 + margin <= x1
                    or y2 + margin <= Y1 or Y2 + margin <= y1)

    def _is_free(x: float, y: float, text: str,
                 occupied: list[tuple[float, float, float, float]]) -> bool:
        """Vrai si le label à (x, y) n'entre en collision avec aucun label placé."""
        box = _label_box(x, y, text)
        return not any(_overlaps(box, b, LABEL_MARGIN) for b in occupied)

    def _fit_label_with_offset(
        text: str, x: float, y_natural: float,
        occupied: list[tuple[float, float, float, float]],
        step: float,
    ) -> tuple[str, float, int]:
        """
        Cherche une position verticale libre pour `text` en essayant
        d'éviter les chevauchements avec les labels déjà placés.

        Retourne (texte_final, y_final, décalage_en_pas). Si aucune
        position libre n'est trouvée, retourne ("", y_natural, 0) — le
        label sera alors placé à sa position naturelle, chevauchement
        accepté.
        """
        offsets: list[float] = [0.0]
        for k in range(1, LABEL_SHIFT_MAX_UP + 1):
            offsets.append(-k * step)
        for k in range(1, LABEL_SHIFT_MAX_DOWN + 1):
            offsets.append(+k * step)

        for offset in offsets:
            y = y_natural + offset
            if y < LABEL_FONT_SIZE:
                continue
            if y > height - LABEL_FONT_SIZE * 0.25:
                continue
            if _is_free(x, y, text, occupied):
                steps = int(round(offset / step)) if step else 0
                return text, y, steps

        return "", y_natural, 0

    def _truncate_to_page(text: str, x: float) -> str:
        """
        Tronque `text` avec « … » s'il dépasse le bord droit de la page,
        en respectant la marge LABEL_PAGE_MARGIN.

        Retourne une chaîne vide si même le raccourci minimal dépasse.
        """
        max_width = width - x - LABEL_PAGE_MARGIN
        if max_width <= 0:
            return ""
        if pdf.get_string_width(text) <= max_width:
            return text
        ellipsis = "…"
        for i in range(len(text) - 1, 0, -1):
            candidate = text[:i] + ellipsis
            if pdf.get_string_width(candidate) <= max_width:
                return candidate
        return ""

    def _draw_label_background(x: float, y_baseline: float, text: str) -> None:
        """
        Dessine un rectangle blanc derrière le label.

        La transparence est lue depuis LABEL_BG_ALPHA. Si la valeur est
        >= 1.0, on dessine un rectangle opaque sans passer par
        local_context.
        """
        if not LABEL_BG:
            return
        x1, y1, x2, y2 = _label_box(x, y_baseline, text)
        pad = LABEL_BG_PADDING

        if LABEL_BG_ALPHA >= 1.0:
            pdf.set_fill_color(255, 255, 255)
            pdf.rect(
                x=x1 - pad,
                y=y1 - pad,
                w=(x2 - x1) + 2 * pad,
                h=(y2 - y1) + 2 * pad,
                style="F",
            )
        else:
            with pdf.local_context(fill_opacity=LABEL_BG_ALPHA):
                pdf.set_fill_color(255, 255, 255)
                pdf.rect(
                    x=x1 - pad,
                    y=y1 - pad,
                    w=(x2 - x1) + 2 * pad,
                    h=(y2 - y1) + 2 * pad,
                    style="F",
                )

    # ------------------------------------------------------------------
    # 8) Placement des labels sur l'image
    # ------------------------------------------------------------------
    occupied: list[tuple[float, float, float, float]] = []
    step = LABEL_SHIFT_STEP if LABEL_SHIFT_STEP is not None else float(LABEL_FONT_SIZE)

    for i, qr in enumerate(qr_items, 1):
        label = _display_text_for(qr) or f"QR#{i}"
        color = qr.color_rgb

        pos = qr.position
        x = pos.top_left.x
        y_natural = max(pos.top_left.y - LABEL_TEXT_OFFSET, LABEL_FONT_SIZE)

        # Étape A : essai avec décalage vertical pour éviter un
        # chevauchement visuel. Aucune troncature n'est déclenchée ici.
        placed, final_y, steps = _fit_label_with_offset(
            label, x, y_natural, occupied, step,
        )

        # Étape B : si aucun emplacement libre, on accepte le chevauchement
        # et on place le label à sa position naturelle.
        if not placed:
            placed = label
            final_y = y_natural
            steps = 0

        # Étape C : troncature UNIQUEMENT si le label dépasse la page.
        final_label = _truncate_to_page(placed, x)

        if not final_label:
            log(f"Label QR #{i}    : {label!r} @ ({x:.1f}, {y_natural:.1f}) "
                f"— sauté (dépasse la page)")
            continue

        # Journalisation
        if steps == 0 and final_label == label:
            log(f"Label QR #{i}    : {final_label!r} "
                f"@ ({x:.1f}, {final_y:.1f}) [naturel]")
        elif steps != 0 and final_label == label:
            direction = "haut" if steps < 0 else "bas"
            log(f"Label QR #{i}    : {final_label!r} "
                f"@ ({x:.1f}, {final_y:.1f}) "
                f"[décalé {abs(steps)}×{step:.0f}pt vers le {direction}, "
                f"naturel y={y_natural:.1f}]")
        elif final_label == label:
            log(f"Label QR #{i}    : {final_label!r} "
                f"@ ({x:.1f}, {final_y:.1f}) [chevauchement accepté]")
        else:
            log(f"Label QR #{i}    : {label!r} → tronqué à {final_label!r} "
                f"(dépasse la page) @ ({x:.1f}, {final_y:.1f})")

        # Rendu : fond (optionnel) puis texte
        _draw_label_background(x, final_y, final_label)
        pdf.set_text_color(*color)
        pdf.text(x, final_y, final_label)

        occupied.append(_label_box(x, final_y, final_label))

    # ------------------------------------------------------------------
    # 9) Légende dans le bandeau blanc — jamais tronquée ni décalée
    # ------------------------------------------------------------------
    if qr_items:
        pdf.set_font("QRFont", size=LEGEND_FONT_SIZE)
        y_baseline = height + LEGEND_PADDING + LEGEND_FONT_SIZE

        for i, qr in enumerate(qr_items, 1):
            if LEGEND_SEPARATOR and i > 1:
                separator_y = y_baseline - LEGEND_FONT_SIZE * 0.8 \
                              - (LEGEND_LINE_HEIGHT - LEGEND_FONT_SIZE) / 2
                pdf.set_draw_color(*LEGEND_SEPARATOR_COLOR)
                pdf.set_line_width(LEGEND_SEPARATOR_WIDTH)
                pdf.line(
                    LEGEND_PADDING,
                    separator_y,
                    width - LEGEND_PADDING,
                    separator_y,
                )

            label = f"{i:02d} {LEGEND_ARROW} {_display_text_for(qr)}"
            color = qr.color_rgb
            pdf.set_text_color(*color)
            pdf.text(LEGEND_PADDING, y_baseline, label)
            y_baseline += LEGEND_LINE_HEIGHT

    # 10) Écriture
    dst.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(dst))

    if not dst.exists():
        raise IOError(
            f"fpdf2 n'a signalé aucune erreur mais le fichier "
            f"{dst} est introuvable après output()."
        )
    log(f"PDF écrit       : {dst.stat().st_size} octets")
    return dst


# ======================================================================
# Classe orchestratrice
# ======================================================================
class QrPdfProcessor:
    """
    Orchestre le traitement d'un PDF multi-page.

    Seuls les paramètres liés au PROCESSUS sont exposés (DPI, fallback,
    verbosité). Tous les paramètres de rendu sont définis dans la
    section « Constantes de rendu » en tête de module.

    API publique inchangée : constructeur et méthode `run`.
    """

    def __init__(
        self,
        dpi: int = 250,
        fallback_dpi: int = 400,
        verbose: bool = True,
    ) -> None:
        self.dpi = dpi
        self.fallback_dpi = fallback_dpi
        self.verbose = verbose

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _render_page(
        self,
        pdf_path: Path,
        page_index: int,
        dpi: int,
        output_dir: Path,
        pad: int = 4,
    ) -> Path:
        scale = dpi / 72.0
        with pdfium.PdfDocument(str(pdf_path)) as doc:
            page = doc[page_index]
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()
            out_path = output_dir / f"page_{page_index + 1:0{pad}d}.png"
            pil_image.save(str(out_path), format="PNG")
            return out_path

    def convert_pdf_to_pngs(self, pdf_path: Path, output_dir: Path) -> list[Path]:
        pdf_path = Path(pdf_path).resolve()
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF introuvable: {pdf_path}")
        output_dir.mkdir(parents=True, exist_ok=True)

        with pdfium.PdfDocument(str(pdf_path)) as doc:
            n_pages = len(doc)

        self._log(f"[conv] {n_pages} page(s) à convertir à {self.dpi} DPI")
        paths: list[Path] = []
        for i in range(n_pages):
            png = self._render_page(pdf_path, i, self.dpi, output_dir)
            paths.append(png)
            self._log(f"[conv]   page {i + 1:>{len(str(n_pages))}}/{n_pages} -> {png.name}")
        return paths

    def process_single_page(
        self,
        png_path: Path,
        work_dir: Path,
        page_number: int | None = None,
    ) -> Path:
        png_path = Path(png_path).resolve()
        stem = png_path.stem
        annotated_png = work_dir / f"{stem}_annotated.png"
        page_pdf = work_dir / f"{stem}.pdf"

        annotate_qr_codes(png_path, annotated_png, page_number=page_number)

        generate_pdf_from_annotated_image(
            image_path=annotated_png,
            output_pdf_path=page_pdf,
            source_image_path=png_path,
            verbose=False,
        )
        return page_pdf

    @staticmethod
    def _png_to_pdf(png_path: Path, output_pdf_path: Path) -> Path:
        png_path = Path(png_path).resolve()
        output_pdf_path = Path(output_pdf_path).resolve()

        img = cv2.imread(str(png_path))
        if img is None:
            raise ValueError(f"Impossible de lire l'image: {png_path}")
        height, width = img.shape[:2]

        pdf = FPDF(orientation="P", unit="pt", format=(width, height))
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        pdf.image(str(png_path), x=0, y=0, w=width, h=height)

        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(output_pdf_path))
        return output_pdf_path

    def merge_pdfs(self, pdf_paths: list[Path], output_path: Path) -> Path:
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        writer = PdfWriter()
        for pdf_path in pdf_paths:
            writer.append(str(Path(pdf_path).resolve()))
        writer.write(str(output_path))
        writer.close()

        self._log(f"[merge] {len(pdf_paths)} page(s) fusionnée(s) -> {output_path}")
        return output_path

    def run(self, input_pdf: str | Path, output_pdf: str | Path) -> Path:
        input_pdf = Path(input_pdf).resolve()
        output_pdf = Path(output_pdf).resolve()

        if not input_pdf.exists():
            raise FileNotFoundError(f"PDF introuvable: {input_pdf}")

        self._log("=" * 60)
        self._log(f"  Traitement de : {input_pdf}")
        self._log(f"  Sortie        : {output_pdf}")
        self._log(f"  DPI           : {self.dpi} (fallback: {self.fallback_dpi})")
        self._log("=" * 60)

        with tempfile.TemporaryDirectory(prefix="qr_pdf_") as tmp:
            tmp_dir = Path(tmp)
            png_dir = tmp_dir / "png"
            work_dir = tmp_dir / "work"
            png_dir.mkdir()
            work_dir.mkdir()

            # Étape 1 : PDF → PNG (basse résolution nominale)
            png_paths = self.convert_pdf_to_pngs(input_pdf, png_dir)

            # Étape 2 : fallback DPI page par page
            #
            # Principe : si aucune détection à basse résolution, on tente
            # une reconversion à plus haute résolution. Le PNG haute
            # résolution n'est CONSERVÉ que s'il a effectivement permis
            # la détection. Sinon, on revient au PNG d'origine pour
            # garantir des pages de taille homogène dans le PDF final.
            final_pngs: list[Path] = []
            scanner = ImageScanner()

            for i, png_path in enumerate(png_paths):
                # --- 1) Tentative de scan à basse résolution -----------
                try:
                    raws = scanner.scan(png_path)
                except ScanError as exc:
                    self._log(
                        f"[error] page {i + 1}: échec du scan ({exc}) "
                        f"— page incluse brute"
                    )
                    final_pngs.append(png_path)
                    continue

                # --- 2) Cas nominal : QR détecté(s) à basse résolution --
                if raws:
                    self._log(f"[info] page {i + 1}: {len(raws)} QR détecté(s)")
                    final_pngs.append(png_path)
                    continue

                # --- 3) Aucun QR à basse résolution --------------------
                # Sous-cas (a) : fallback désactivé → page brute au DPI nominal.
                if self.fallback_dpi <= self.dpi:
                    self._log(f"[info] page {i + 1}: aucun QR détecté")
                    final_pngs.append(png_path)
                    continue

                # Sous-cas (b) : fallback activé → on retente à plus haute
                # résolution, et on ne CONSERVE le PNG haute résolution
                # que s'il a effectivement permis la détection.
                self._log(
                    f"[warn] page {i + 1}: aucun QR à {self.dpi} DPI, "
                    f"reconversion à {self.fallback_dpi} DPI"
                )
                fallback_png = self._render_page(
                    input_pdf, i, self.fallback_dpi, png_dir,
                    pad=len(str(len(png_paths))),
                )
                final_png = png_dir / f"page_{i + 1:04d}_hi.png"
                shutil.move(str(fallback_png), str(final_png))

                try:
                    raws_hi = scanner.scan(final_png)
                except ScanError as exc:
                    self._log(
                        f"[error] page {i + 1}: échec du scan à "
                        f"{self.fallback_dpi} DPI ({exc}) "
                        f"— page incluse à {self.dpi} DPI"
                    )
                    # Échec du scan haute résolution : le fallback n'a
                    # rien apporté, on revient au PNG d'origine.
                    final_pngs.append(png_path)
                    continue

                if raws_hi:
                    # Le fallback a payé : on conserve le PNG haute
                    # résolution, indispensable puisque le QR n'était
                    # pas visible à basse résolution.
                    self._log(
                        f"[ok]   page {i + 1}: {len(raws_hi)} QR "
                        f"détecté(s) à {self.fallback_dpi} DPI"
                    )
                    final_pngs.append(final_png)
                else:
                    # Le fallback a échoué : on REVIENT au PNG d'origine
                    # pour éviter d'introduire dans le PDF final une page
                    # de taille différente, plus lourde et sans apport.
                    self._log(
                        f"[warn] page {i + 1}: toujours aucun QR "
                        f"à {self.fallback_dpi} DPI "
                        f"— page incluse à {self.dpi} DPI"
                    )
                    final_pngs.append(png_path)

            # Étape 3 : traitement page par page
            page_pdfs: list[Path] = []
            for i, png_path in enumerate(final_pngs):
                self._log(f"[page] traitement de la page {i + 1}…")
                try:
                    page_pdf = self.process_single_page(
                        png_path, work_dir, page_number=i + 1
                    )
                    page_pdfs.append(page_pdf)
                except Exception as exc:
                    self._log(
                        f"[error] page {i + 1}: échec du traitement "
                        f"({exc}) — page incluse brute"
                    )
                    fallback_pdf = work_dir / f"{png_path.stem}_brut.pdf"
                    self._png_to_pdf(png_path, fallback_pdf)
                    page_pdfs.append(fallback_pdf)

            # Étape 4 : fusion
            if not page_pdfs:
                raise RuntimeError("Aucune page n'a pu être traitée.")
            self.merge_pdfs(page_pdfs, output_pdf)

        self._log("=" * 60)
        self._log("  Traitement terminé.")
        self._log("=" * 60)
        return output_pdf


# ======================================================================
# Point d'entrée
# ======================================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Traite un PDF multi-page : détecte et annote les QR codes."
    )
    parser.add_argument("input", type=str, help="PDF d'entrée")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="PDF de sortie (défaut: <input>_annotated.pdf)"
    )
    parser.add_argument("--dpi", type=int, default=250,
                        help="DPI de conversion (défaut: 250)")
    parser.add_argument("--fallback-dpi", type=int, default=400,
                        help="DPI de secours si aucun QR n'est détecté "
                             "(défaut: 400, 0 pour désactiver)")
    parser.add_argument("--quiet", action="store_true",
                        help="Mode silencieux")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_name(f"{input_path.stem}_annotated.pdf")
    )

    processor = QrPdfProcessor(
        dpi=args.dpi,
        fallback_dpi=args.fallback_dpi,
        verbose=not args.quiet,
    )
    processor.run(input_path, output_path)
    print(f"PDF généré : {output_path}")
