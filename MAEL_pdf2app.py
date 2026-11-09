#!/usr/bin/env python3
"""CLI MAEL : conversion d'un PDF en lecteur HTML autonome."""
from __future__ import annotations
import argparse
from pathlib import Path
from pdf2app import Pdf2App, Pdf2AppConfig

def build_parser() -> argparse.ArgumentParser:
    """Construit les options de ligne de commande."""
    parser=argparse.ArgumentParser(description="Convertit un PDF en lecteur HTML autonome avec repérage QR.")
    parser.add_argument("pdf",type=Path,help="PDF source")
    parser.add_argument("html",type=Path,nargs="?",default=None,help="Fichier HTML de sortie (par défaut : même nom que le PDF avec l’extension .html)")
    parser.add_argument("--dpi",type=int,default=250,help="DPI du scan QR (défaut : 250)")
    parser.add_argument("--fallback-dpi",type=int,default=400,help="DPI de la seconde passe (défaut : 400)")
    parser.add_argument("--display-dpi",type=int,default=170,help="DPI du rendu AVIF d'affichage (défaut : 170)")
    parser.add_argument("--quality",type=int,default=30,help="Qualité AVIF 0..100 (défaut : 30)")
    parser.add_argument("--speed",type=int,default=6,help="Vitesse AVIF 0..10 (défaut : 6)")
    parser.add_argument("--max-width",type=int,default=None,help="Largeur maximale optionnelle en pixels")
    parser.add_argument("--quiet",action="store_true",help="Réduit les messages d'avancement")
    return parser

def main() -> int:
    """Exécute le pipeline et retourne un code de sortie."""
    args=build_parser().parse_args()
    if args.html is None:
        args.html=Path(args.pdf).with_suffix(".html")
    config=Pdf2AppConfig(dpi=args.dpi,fallback_dpi=args.fallback_dpi,display_dpi=args.display_dpi,
                         avif_quality=args.quality,avif_speed=args.speed,max_width=args.max_width,verbose=not args.quiet)
    try:
        result=Pdf2App(config).run(args.pdf,args.html)
    except Exception as exc:
        print(f"Erreur : {exc}")
        return 1
    print(f"Lecteur créé : {result}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
