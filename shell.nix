{ pkgs ? import <nixpkgs> {} }:

let
  # Python 3.13 (version la plus récente des deux fichiers)
  python = pkgs.python313;

  # Environnement Python sur-mesure contenant l'union des dépendances
  # des deux applications :
  #   - MAEL_V6.0.py       (générateur de QR codes)
  #   - MAEL_Verif_PDF.py  (annotation PDF de QR codes)
  #
  # Toutes les dépendances Python sont fournies par Nix (équivalents
  # des paquets pip listés dans requirements.txt). Aucun `pip install`
  # n'est nécessaire.
  pythonEnv = python.withPackages (ps: with ps; [
    # --- Interface graphique -------------------------------------------
    tkinter        # Fournit le module 'tkinter' (équivalent de 'tk')
    ttkbootstrap   # Surcouche de style pour Tkinter (utilisé par MAEL_V6.0)
    pillow         # Fournit 'PIL' (utilisé pour qrcode et les images)

    # --- Génération de QR codes (MAEL_V6.0) ----------------------------
    qrcode         # Fournit le module 'qrcode'

    # --- Détection et annotation PDF (MAEL_Verif_PDF) ------------------
    zxing-cpp      # Fournit le module 'zxingcpp' (lecture des QR codes)
    opencv4        # Fournit 'cv2' (remplace 'opencv-python' de pip)
    numpy          # Dépendance interne d'opencv4, explicite pour la clarté
    fpdf2          # Fournit le module 'fpdf' (génération PDF)
    pypdfium2      # Rendu PDF → image (module 'pypdfium2')
    pypdf          # Fusion de PDF (module 'pypdf')

    # --- Presse-papier (MAEL_V6.0, prévu pour usage futur) -------------
    pyperclip      # Équivalent du paquet pip 'clipboard'

    # --- Synthèse vocale (TTS) -----------------------------------------
    gtts           # Synthèse vocale en ligne (Google Text-to-Speech)
    miniaudio      # Lecture audio pour la maquette TTS

    # --- Outils de développement ---------------------------------------
    ipython
    pytest
    black
    ruff
  ]);

  # 🔊 AJOUT AUDIO (1/3) : bibliothèques chargées dynamiquement par
  # miniaudio à l'exécution. Sans elles, miniaudio retombe sur le
  # backend "Null" (aucun son).
  audioLibs = with pkgs; [ alsa-lib libpulseaudio pipewire ];

in
pkgs.mkShell {
  name = "mael-env";

  buildInputs = [
    # Interpréteur Python + toutes ses bibliothèques
    pythonEnv

    # --- Bibliothèques système pour Tkinter ----------------------------
    pkgs.tk           # Runtime Tcl/Tk (parfois nécessaire sous NixOS)
    pkgs.tcl          # Bibliothèque Tcl (utilisée par Tkinter)

    # --- Outils système pour le presse-papier sous Linux ---------------
    # MAEL_V6.0.py détecte automatiquement la présence de "xclip" via
    # shutil.which() et prévient l'utilisateur s'il manque. Le fournir
    # ici garantit que la copie d'image fonctionne out-of-the-box.
    pkgs.xclip        # Session X11 (chemin utilisé par MAEL_V6.0.py)
    pkgs.xsel         # Fallback X11, utile pour vider le presse-papier en test
    pkgs.wl-clipboard # Session Wayland (si xclip indisponible)

    # --- Outils de développement ---------------------------------------
    pkgs.git
  ] ++ audioLibs;     # 🔊 AJOUT AUDIO (2/3)

  shellHook = ''
    # 🔊 AJOUT AUDIO (3/3) : permet à miniaudio de trouver ALSA/PulseAudio
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath audioLibs}:$LD_LIBRARY_PATH

    echo "🚀 Environnement NixOS pour MAEL activé."
    echo "🐍 Version Python : $(python --version)"
    echo "📦 Modules Python : tkinter, ttkbootstrap, qrcode, pillow, cv2,"
    echo "                    numpy, zxingcpp, fpdf, pypdf, pypdfium2, pyperclip, gtts, miniaudio"
    echo "🖥️  Presse-papier  : xclip, xsel, wl-clipboard"
    echo "🧰 Dev tools      : ipython, pytest, black, ruff, git"
    echo "🔊 Audio          : alsa-lib, libpulseaudio, pipewire"
    echo ""
    echo "Pour lancer les applications :"
    echo "  python MAEL_V6.0.py"
    echo "  python MAEL_Verif_PDF.py <fichier.pdf>"
    echo ""

    # Rendre les modules du dossier courant importables
    # (utile pour 'from MAEL_obfus import Obfus' et
    #  'from MAEL_Verif_PDF import QrPdfProcessor')
    export PYTHONPATH="$PWD:$PYTHONPATH"

    export PS1="[MAEL] \w $ "
  '';
}
