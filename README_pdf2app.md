# MAEL_pdf2app

Génère un lecteur HTML autonome (images AVIF intégrées) et superpose des zones carrées invisibles sur les QR détectés. L'exécution du paquet `verif_pdf` requiert les dépendances listées dans `requirements.txt` ainsi que le module privé `MAEL_obfus` du projet hôte.

```sh
python MAEL_pdf2app.py document.pdf lecteur.html --dpi 250 --fallback-dpi 400 --display-dpi 96 --quality 30 --speed 6
```

AVIF : Pillow ≥ 11.2 embarque le support AVIF natif sur les plateformes compatibles. Sinon, installer `pillow-avif-plugin` (enregistrement Pillow via `import pillow_avif`). Aucun passage en niveaux de gris n'est effectué. Les pages sont rendues séparément : les échecs de scan restent localisés à leur page.

Les zones sont normalisées par les dimensions du PNG effectivement scanné; le format relatif les rend indépendantes du DPI. Le lecteur conserve les AVIF en data URI, sans ressource externe.
