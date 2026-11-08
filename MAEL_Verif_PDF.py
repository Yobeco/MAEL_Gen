"""Point d’entrée CLI du traitement de vérification PDF MAEL."""
from __future__ import annotations
from pathlib import Path
from verif_pdf import ProcessingConfig, VerifPdf

__all__ = ["VerifPdf", "ProcessingConfig"]

def main() -> None:
    """Lance le traitement PDF depuis la ligne de commande."""
    import argparse
    parser=argparse.ArgumentParser(description="Traite un PDF multi-page : détecte et annote les QR codes.")
    parser.add_argument("input", type=str, help="PDF d'entrée")
    parser.add_argument("-o", "--output", type=str, default=None, help="PDF de sortie (défaut: <input>_annotated.pdf)")
    parser.add_argument("--dpi", type=int, default=250, help="DPI de conversion (défaut: 250)")
    parser.add_argument("--fallback-dpi", type=int, default=400, help="DPI de secours si aucun QR n'est détecté (défaut: 400, 0 pour désactiver)")
    parser.add_argument("--quiet", action="store_true", help="Mode silencieux")
    args=parser.parse_args(); input_path=Path(args.input)
    output_path=Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}_annotated.pdf")
    VerifPdf(ProcessingConfig(dpi=args.dpi, fallback_dpi=args.fallback_dpi, verbose=not args.quiet)).run(input_path, output_path)
    print(f"PDF généré : {output_path}")

if __name__ == "__main__": main()
