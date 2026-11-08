"""Génération, conversion et assemblage des PDF de sortie."""
from __future__ import annotations
import sys
from pathlib import Path
from .render_constants import *
from .qr_detector import ColoredTtsItem, QrDetector, qr_scan_and_parse

def _find_utf8_font() -> Path:
    """Retourne le chemin de la police TrueType embarquée."""
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent

    font_path = base / "assets" / "fonts" / "DejaVuSans.ttf"
    if not font_path.exists():
        raise FileNotFoundError(
            f"Police introuvable : {font_path}\n"
            "Assurez-vous que 'assets/fonts/DejaVuSans.ttf' est bien présent."
        )
    return font_path

def _display_text_for(qr: ColoredTtsItem) -> str:
    """
    Retourne le texte à afficher pour un QR donné.

    - modes cloud et Wifi : on affiche le libellé de LABELS_TEXT.
    - QR TTS : 'lang → payload' (payload seul si langue absente).
    """
    if qr.mode in MODES_CLOUD or qr.mode == MODE_WIFI:
        return LABELS_TEXT[qr.mode]
    if qr.lang:
        return f"{qr.lang} {LANG_ARROW} {qr.text}"
    return qr.text

def generate_pdf_from_annotated_image(
    image_path: str | Path,
    output_pdf_path: str | Path,
    source_image_path: str | Path | None = None,
    verbose: bool = True,
    detector: "QrDetector | None" = None,
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
    import cv2
    from fpdf import FPDF

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
    qr_items = qr_scan_and_parse(detect_src, detector=detector)
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

class PDFWriter:
    """Produit les PDF enrichis et les PDF bruts de secours."""
    def write_page(self, image_path: str | Path, output_pdf_path: str | Path, *, source_image_path: str | Path | None = None, verbose: bool = True, detector: QrDetector | None = None) -> Path:
        """Génère le PDF enrichi d’une page."""
        return generate_pdf_from_annotated_image(image_path, output_pdf_path, source_image_path, verbose, detector)

    @staticmethod
    def png_to_pdf(png_path: Path, output_pdf_path: Path) -> Path:
        """Convertit une image PNG en PDF d’une page."""
        import cv2
        from fpdf import FPDF
        png_path = Path(png_path).resolve()
        output_pdf_path = Path(output_pdf_path).resolve()
        img = cv2.imread(str(png_path))
        if img is None:
            raise ValueError(f"Impossible de lire l'image: {png_path}")
        height, width = img.shape[:2]
        pdf = FPDF(orientation="P", unit="pt", format=(width, height))
        pdf.set_auto_page_break(auto=False); pdf.add_page()
        pdf.image(str(png_path), x=0, y=0, w=width, h=height)
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(output_pdf_path))
        return output_pdf_path

