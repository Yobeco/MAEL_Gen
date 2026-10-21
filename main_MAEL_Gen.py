"""
#############################################################################
#
#                    "MAEL Gen" (GPL v3)
#   Générateur de codes QR (V6.1) spécifique pour MAEL Scan
#   Application multi-plateforme
#   Multi-logiciel d'Assistance à l'Enseignement des Langues
#   "Donnez une voix à vos documents pédagogiques"
#
#############################################################################

        @@@@@@@@@@@@@                                 @@@@@@@@@@@@@
    @@@@@@                                                       @@@@@@
   @@@                                                               @@@
 @@@.                                                                  @@@
 @@                                                                     @@
@@@      @@@@@@@@@@@@@@@@@@@   @@         @@   @@@@@@@@@@@@@@@@@@@      @@@
@@       @@              @@@     @@@   @@@     @@@              @@       @@
@@       @@              @@@     @@@   @@@     @@@              @@       @@
@@       @@   @@@@@@@@   @@@   @@   @@@        @@@   @@@@@@@@   @@       @@
@@       @@   @@@@@@@@   @@@     @@@   @@@@@   @@@   @@@@@@@@   @@       @@
@@       @@   @@@@@@@@   @@@     @@@   @@@@@   @@@   @@@@@@@@   @@       @@
@@       @@   @@@@@@@@   @@@   @@@@@@@@        @@@   @@@@@@@@   @@       @@
         @@              @@@        @@@        @@@              @@
         @@              @@@        @@@        @@@              @@
         @@@@@@@@@@@@@@@@@@@   @@   @@@   @@   @@@@@@@@@@@@@@@@@@@
                               @@@@@@@@@@@
                               @@@@@@@@@@@
                      @@@@@@     @@@      @@   @@@   @@   @@@   @@
         @@   @@@@@@        @@@
         @@   @@@@@@        @@@                    -
         @@@@@   @@@@@   @@@@@@              @  @@%@%@@
         @@@@@              @@@@@          @#####     #%@@
         @@@@@              @@@@@        @@##@#%@@@@@@#####@@-
         @@      @@@  @@@@@@@@@@@      +@###@         #@@@%####@@%
                               @@    @@##@@@@@@@@@@@@@@##%@@@@@@@@
                               @@     @*@@%#%%%@@@@@%%%##%@@@@#@
         @@@@@@@@@@@@@@@@@@@           @##@-@@@%@@@@@@@@@@%##@%
         @@              @@@   @@        @#=#@@----*@@#* =#@@
         @@              @@@   @@         @#           #%@#
@@       @@   @@@@@@@@   @@@               =@%#%%%%@@@@                  @@
@@       @@   @@@@@@@@   @@@                                             @@
@@       @@   @@@@@@@@   @@@                             *               @@
@@       @@   @@@@@@@@   @@@   @@@@ @@@@    @@@@   @@@@@@@ @@@           @@
@@       @@              @@@   @@@@ @*@@   @@ @@   @@@@@@@ -@@           @@
@@       @@              @@@   @@ @@@ @@  @@@@@@@  @@      :@@           @@
@@@      @@@@@@@@@@@@@@@@@@@   @@ @@@ @@ @@@   @@@ @@@@@@@ @@@@@@@      @@@
 @@                                                                     @@
 @@@                                                                   @@@
   @@@                                                               @@@
    @@@@@@                                                       @@@@@@
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

>>>>> Améliorations prévues <<<<<
- Ajouter un menu : "Mode épeler mot par mot" ?
- Améliorer le mode dicter : dire la ponctuation, laisser plus de temps entre les mots. (MAEL Scan)
- Actualiser la doc
- Ajouter le mode épeler pour EN ES PT
- Voir les cas de caractères étranges issus de "copier / coller" (espaces insécables, plusieurs type de guillemets...)
- Faire charger les modules spécifiques à chaque OS une seule fois au début du programme en fonction de l'OS détecté.
- Permettre le glisser - déposer du code QR vers l'éditeur externe ???
- Réparer l'affichage de l'icône "Presse papier vide"
- Ajouter des icônes aux "toplevel"  --> À vérifier !
- Lancer une petit fenêtre qui propose l'installation de "xclip"

#############################################################################
#                   Informations pour le développement
#############################################################################

>>>>> Environnement de développement <<<<<

NixOS 26.05
Python 3.13

------------------------------------------------------------------------------
<<<<<<<   Gestion du presse-papier selon l'OS   >>>>>>>>>>
------------------------------------------------------------------------------
- Module pywin32 pour Windows :
    pip install pywin32
- Vérifier la l'installation de pywin32 :
    python -m pip show pywin32
------------------------------------------------------------------------------
- Module AppKit pour OSX :
    pip install PyObjC
- Vérifier la l'installation de AppKit :
    python -c "import AppKit"
--> Ne doit pas retourner d'erreur
------------------------------------------------------------------------------
- Pas de module python à installer pour Linux
Cependant, l'ordinateur Linux hôte nécessite "xclip" pour gérer le presse papier :
    sudo apt-get install xclip

- Aide à comprendre la gestion du presse papier :
Pour vider le presse papier pour tester le programme :
installer xsel :
    sudo apt-get install xsel
Puis :
    xsel -c -b
------------------------------------------------------------------------------
"""


import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog

import qrcode
from PIL import Image, ImageTk
import os, sys, shutil, tempfile, threading, queue, platform
from pathlib import Path

from MAEL_obfus import Obfus

try:
    from MAEL_Verif_PDF import QrPdfProcessor
    PDF_VERIF_AVAILABLE = True
    PDF_VERIF_ERROR = ""
except ImportError as exc:
    PDF_VERIF_AVAILABLE = False
    PDF_VERIF_ERROR = str(exc)
    QrPdfProcessor = None


# ---------------------------------------------------------------------------
# Constantes (identiques à l'original)
# ---------------------------------------------------------------------------
_qrgen_os_label = {"Linux": "Linux", "Darwin": "macOS", "Windows": "Windows"}.get(
    platform.system(), platform.system()
)
qrgen_version = f"- V6.1 pour {_qrgen_os_label}"

coul_interface = "#FFFFFF"
color_mode = {"dicter": "#FF4040", "epeler": "#009900", "lire": "#0066CC"}
color_hover = {
    "lire": "#B3D9FF", "epeler": "#B3F0B3", "reserve": "#D9B3FF", "dicter": "#FFB3B3"
}

geom_horiz = "465x173"
geom_verti = "270x340"
ecart_h = 4
ecart_v = 1
LARGEUR_FRAME_LANG = 45

if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_DIR = os.path.join(tempfile.gettempdir(), "MAEL_Gen")
os.makedirs(TEMP_DIR, exist_ok=True)
QR_TEMP_PATH = os.path.join(TEMP_DIR, "QR_Tempor.png")

ICONES_AVEC_VARIANTE_SOMBRE = {
    "Copy-20px-QR.png", "PP-png-20px.png", "PP-str-20px.png", "PP-vid-20px.png",
}

obfusor = Obfus()


# ---------------------------------------------------------------------------
# Fonctions helper (hors classe, ne dépendent d'aucun état)
# ---------------------------------------------------------------------------
def resourcePath(relativePath):
    return os.path.join(BASE_DIR, relativePath)

def tempPath(filename):
    return os.path.join(TEMP_DIR, filename)


# ---------------------------------------------------------------------------
# La classe principale
# ---------------------------------------------------------------------------
class MaelGenApp:
    """Application MAEL Gen — générateur de QR codes."""

    def __init__(self):
        # ---------- état initial (anciennes globales) ----------
        self.lang = "fr"
        self.pays = "FRA"
        self.errCorr = 3          # qrcode.constants.ERROR_CORRECT_Q
        self.type_texte = 0       # 0=langue, 1=BM, 2=AC-fr, 3=AC-es
        self.mode = "lire"
        self.balise = ""
        self.text_saisi_sauve = ""
        self.size = "150"
        self.theme = "litera"
        self.disp = "h"           # orientation courante

        # ---------- timers ----------
        self.id_boucle = None
        self.id_debounce = None
        self.qr_deja_genere = False

        # ---------- fenêtre ----------
        self.root = ttkb.Window(themename=self.theme)
        self._install_custom_button_styles()
        self.TEXT_SAISI_BG, self.TEXT_SAISI_FG = self._get_text_saisi_colors()

        self.root['padx'] = 5
        self.root['pady'] = 5
        self.root.title(f"MAEL Gen {qrgen_version}")
        self.root.attributes('-topmost', True)
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(
            False, tk.PhotoImage(file=resourcePath('assets/icon.png'))
        )

        # ---------- construire les widgets ----------
        self._create_variables()
        self._create_frames()
        self._create_menu()
        self._build_content()
        self._appliquer_disposition()     # place self.disp (h ou v)
        self._restaurer_saisie_si_besoin()
        self._periodic_scan_clipboard()
        self.root.bind_all("<Control-q>", self.quit_application)

    # ==================================================================
    # Propriétés dérivées pour compatibilité avec le code existant
    # (dans l'original, c'étaient des StringVar lues directement)
    # ==================================================================
    @property
    def langue(self):
        return self._var_langue.get()

    @langue.setter
    def langue(self, val):
        self._var_langue.set(val)

    @property
    def pays_var(self):
        return self._var_pays.get()

    @pays_var.setter
    def pays_var(self, val):
        self._var_pays.set(val)

    # ==================================================================
    # ① Créer les tk.StringVar / IntVar (pour le binding automatique)
    # ==================================================================
    def _create_variables(self):
        self._var_langue = tk.StringVar(value=self.lang)
        self._var_pays = tk.StringVar(value=self.pays)
        self.new_size_var = tk.IntVar(value=100)

    # ==================================================================
    # ② Créer les frames principales (vides, le contenu suit)
    # ==================================================================
    def _create_frames(self):
        self.frame_input = ttkb.Frame(self.root)
        self.frame_qr = tk.Frame(
            self.root, background=color_mode[self.mode], bd=4, relief="sunken"
        )

    # ==================================================================
    # ③ Construire tout le contenu (widgets, menus…)
    #    C'est l'ancien corps de application(), découpé en morceaux.
    # ==================================================================
    def _build_content(self):
        self._build_frame_input()
        self._build_label_qr()

    def _build_frame_input(self):
        # --- sous-frames ---
        self.frame_text = ttkb.Frame(self.frame_input)
        self.frame_settings = ttkb.Frame(self.frame_input)
        self.frame_text.pack(expand=True, fill="both", ipadx=5, ipady=0, pady=0)
        self.frame_settings.pack(expand=True, fill="both", ipadx=5, ipady=0)

        # frame_lang + frame_data
        self.frame_lang = ttkb.Frame(self.frame_text, width=LARGEUR_FRAME_LANG)
        self.frame_data = ttkb.Frame(self.frame_text)
        self.frame_lang.pack_propagate(False)
        self.frame_lang.pack(expand=False, fill="y", ipadx=0, ipady=0, pady=0, side=tk.LEFT)
        self.frame_data.pack(expand=True, fill="both", ipadx=0, ipady=0, pady=0, side=tk.LEFT)

        # ----- widgets dans frame_lang -----
        self.label_lang = ttkb.Label(
            self.frame_lang, textvariable=self._var_langue,
            font=("Arial", 10, "italic"),
        )
        self.label_lang.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

        self.label_pay = ttkb.Label(
            self.frame_lang, textvariable=self._var_pays,
            font=("Arial", 8, "italic"),
        )
        self.label_pay.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

        self.label_mode = ttkb.Label(
            self.frame_lang, text="",
            font=("Arial", 10, "italic"),
        )
        self.label_mode.pack(ipadx=0, ipady=2, pady=2, side=tk.TOP)
        self._sync_label_mode()

        # bouton copier
        self.photo_copy = tk.PhotoImage(file=self.icon_path("Copy-20px-QR.png"))
        self.button_copy = ttkb.Button(
            self.frame_lang, image=self.photo_copy,
            command=self.copy_QR, state="disabled",
            bootstyle="secondary-outline",
        )
        self.button_copy.pack(ipadx=0, ipady=0, pady=1, side=tk.TOP)

        # ----- widget de saisie -----
        self.text_saisi = ttkb.Text(self.frame_data, width=30, height=5)
        self.text_saisi.pack(side=tk.LEFT)
        self.text_saisi.configure(bg=self.TEXT_SAISI_BG, fg=self.TEXT_SAISI_FG)
        self.text_saisi.bind("<Control-v>", self._delete_png)
        self.text_saisi.bind("<KeyRelease>", self._on_key_release)
        self.text_saisi.bind("<Button-3>", self._paste_text)

        # ----- frame_settings -----
        self._build_settings()

    def _build_settings(self):
        # logo
        icon_logo = ImageTk.PhotoImage(Image.open(resourcePath("assets/icon-20px.png")))
        self.label_logo = ttkb.Label(self.frame_settings, image=icon_logo)
        self.label_logo.image = icon_logo
        self.label_logo.grid(row=0, column=0, padx=(ecart_h, 20), sticky="w")

        # taille
        frame_size = ttkb.Frame(self.frame_settings)
        frame_size.grid(row=0, column=1, padx=ecart_h, sticky="nsew")
        ttkb.Label(frame_size, text="Taille :", font=("Arial", 11)).grid(row=0, column=0)
        self.entry_size = ttkb.Entry(frame_size, width=5, justify="center")
        self.entry_size.insert(0, self.size)
        self.entry_size.grid(row=1, column=0, pady=2)
        self.entry_size.bind("<Return>", lambda e: self.qr_actu(None, self.errCorr, 1))
        self.entry_size.bind("<KP_Enter>", lambda e: self.qr_actu(None, self.errCorr, 1))
        self.entry_size.bind(
            "<Control-v>",
            lambda e: self.root.after_idle(lambda: self.qr_actu(None, self.errCorr, 1)),
        )

        # mode (boutons L/E/C/D)
        frame_mode = ttkb.Frame(self.frame_settings)
        frame_mode.grid(row=0, column=2, padx=ecart_h, sticky="nsew")
        ttkb.Label(frame_mode, text="Mode :", font=("Arial", 11)).grid(
            row=0, column=0, columnspan=4, pady=(0, 2)
        )

        btn_common = {"width": 2, "padding": (1, 0)}
        ttkb.Button(
            frame_mode, text="L", style="Lecture.TButton",
            command=self.mode_lire, **btn_common,
        ).grid(row=1, column=0, padx=1)
        ttkb.Button(
            frame_mode, text="E", style="Epeler.TButton",
            command=self.mode_epeler, **btn_common,
        ).grid(row=1, column=1, padx=1)
        ttkb.Button(
            frame_mode, text="C", style="Reserve.TButton",
            state="disabled", **btn_common,
        ).grid(row=1, column=2, padx=1)
        ttkb.Button(
            frame_mode, text="D", style="Dicter.TButton",
            command=self.mode_dicter, **btn_common,
        ).grid(row=1, column=3, padx=1)

        # indicateur mémoire presse-papier
        self.icon_mem_str = ImageTk.PhotoImage(
            Image.open(self.icon_path("PP-vid-20px.png"))
        )
        self.label_mem = ttkb.Label(self.frame_settings, image=self.icon_mem_str)
        self.label_mem.grid(row=0, column=3, padx=7, sticky="e")

        self.frame_settings.columnconfigure(0, weight=0)
        self.frame_settings.columnconfigure(1, weight=1)
        self.frame_settings.columnconfigure(2, weight=1)
        self.frame_settings.columnconfigure(3, weight=0)
        self.frame_settings.rowconfigure(0, weight=1)

    def _build_label_qr(self):
        img_code = ImageTk.PhotoImage(Image.open(resourcePath("assets/Bienvenue.png")))
        self.label_qr = ttkb.Label(self.frame_qr, image=img_code)
        self.label_qr.image = img_code
        self.label_qr.pack()

    # ==================================================================
    # ④ Menu (identique à l'original)
    # ==================================================================
    def _create_menu(self):
        menuBar = ttkb.Menu(self.root)

        # Langues (tous les sous-menus)
        menuLangue = ttkb.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Langues", menu=menuLangue)
        self._build_lang_menu(menuLangue)

        # Paramètres
        menuParam = ttkb.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Paramètres", menu=menuParam)
        self._build_param_menu(menuParam)

        # Outils
        menuOutils = ttkb.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Outils", menu=menuOutils)
        menuOutils.add_command(label="Vérification", command=self.verif_pdf)

        # Infos
        menuInfos = ttkb.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Infos", menu=menuInfos)
        menuInfos.add_command(label='Aide', command=self.toplevel_aide)
        menuInfos.add_command(label='Sons Borel-Maisonny', command=self.toplevel_BM)
        menuInfos.add_command(label='Abécédaire Consigny', command=self.toplevel_AC)
        menuInfos.add_command(label='À propos de "MAEL Gen"', command=self.toplevel_info)

        self.root.config(menu=menuBar)

    # ------------------------------------------------------------------
    # sous-menus langues (construction factorisée)
    # ------------------------------------------------------------------
    def _build_lang_menu(self, menuLangue):
        menus_dict = {
            "A":   ["Afrikaans af-ZAF","Allemand de-DEU","Anglais en-AUS",
                    "Anglais en-IND","Anglais en-GBR","Anglais en-USA","Arabe ar-SAU"],
            "B-D": ["Basque eu-ESP","Bengali bn-IND","Bulgare bg-BGR","Catalan ca-ESP",
                    "Chinois zh-CHN","Coréen ko-KOR","Danois da-DNK"],
            "E-G": ["Espagnol es-ESP","Espagnol es-USA","Finnois fi-FIN","Français fr-CAN",
                    "Français fr-FRA","Galicien gl-ESP","Grec el-GRC","Gujarati gu-IND"],
            "H-K": ["Hébreu he-ISR","Hindi hi-IND","Hongrois hu-HUN","Indonésien id-IDN",
                    "Islandais is-ISL","Italien it-ITA","Japonais ja-JPN"],
            "L-M": ["Kannada kn-IND","Letton lv-LVA","Lituanien lt-LTU","Malais ms-MYS",
                    "Malayalam ml-IND","Marathi mr-IND"],
            "N-P": ["Néerlandais nl-BEL","Néerlandais nl-NLD","Norvégien nb-NOR","Panjabi pa-IND",
                    "Philippin tl-PHL","Polonais pl-POL","Portugais pt-BRA","Portugais pt-PRT"],
            "Q-S": ["Roumain ro-ROU","Russe ru-RUS","Serbe sr-SRB","Slovaque sk-SVK","Suédois sv-SWE"],
            "T-Z": ["Tamoul ta-IND","Tchèque cs-CZE","Télougou te-IND","Thaï th-THA",
                    "Turc tr-TUR","Ukrainien uk-UKR","Vietnamien vi-VNM"],
        }
        for label, entries in menus_dict.items():
            sub = ttkb.Menu(menuLangue, tearoff=0)
            menuLangue.add_cascade(label=label, menu=sub)
            for name in entries:
                sub.add_command(label=name, command=lambda n=name: self.extract_lang_pays(n))

        special = ttkb.Menu(menuLangue, tearoff=0)
        menuLangue.add_cascade(label="Spécial", menu=special)
        special.add_command(label="Sons Borel-Maisonny", command=self.borel_Maisonny)
        special.add_command(label="Abécédaire Consigny FR", command=self.abeced_Consigny_fr)
        special.add_command(label="Abécédaire Consigny ES", command=self.abeced_Consigny_es)

    # ------------------------------------------------------------------
    # sous-menu Paramètres
    # ------------------------------------------------------------------
    def _build_param_menu(self, menuParam):
        # Robustesse
        menuRobust = ttkb.Menu(menuParam, tearoff=0)
        menuParam.add_cascade(label="Robustesse", menu=menuRobust)

        txt_07 = "  7% : moins robuste - mois grand"
        txt_15 = " 15%"
        txt_25 = " 25%"
        txt_30 = " 30% : plus robuste - plus grand"
        if self.errCorr == 1:   txt_07 = f"*{txt_07}"
        elif self.errCorr == 0: txt_15 = f"*{txt_15}"
        elif self.errCorr == 2: txt_30 = f"*{txt_30}"
        else:                   txt_25 = f"*{txt_25}"

        menuRobust.add_command(label=txt_07, command=self.Robust_Bas)
        menuRobust.add_command(label=txt_15, command=self.Robust_Moy)
        menuRobust.add_command(label=txt_25, command=self.Robust_Qua)
        menuRobust.add_command(label=txt_30, command=self.Robust_Haut)
        self._menuRobust = menuRobust  # pour MAJ future

        # Disposition
        self._label_disp = "Disposition vertical" if self.disp == "h" else "Disposition horizontal"
        menuParam.add_command(label=self._label_disp, command=self._toggle_disposition)

        # Thème
        theme_label = "Thème sombre" if self.theme == "litera" else "Thème clair"
        menuParam.add_command(label=theme_label, command=self.toggle_theme)
        self._menuParam = menuParam  # conservé pour MAJ des libellés

    # ==================================================================
    # ⑤ Disposition : appliquer la grille selon self.disp
    # ==================================================================
    def _appliquer_disposition(self):
        # --- nettoyage des anciens poids de colonnes et lignes ---
        self.root.columnconfigure(0, weight=0, minsize=0)
        self.root.columnconfigure(1, weight=0, minsize=0)
        self.root.rowconfigure(0, weight=0, minsize=0)
        self.root.rowconfigure(1, weight=0, minsize=0)

        if self.disp == "h":
            self.root.geometry(geom_horiz)
            self.frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
            self.frame_qr.grid(row=0, column=1, padx=2, pady=2)
            self.root.rowconfigure(0, weight=1, minsize=155)
            self.root.columnconfigure(1, weight=1, minsize=155)
        else:
            self.root.geometry(geom_verti)
            self.frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
            self.frame_qr.grid(row=1, column=0, padx=2, pady=2)
            self.root.rowconfigure(1, weight=1, minsize=155)
            self.root.columnconfigure(0, weight=1, minsize=155)

    def _toggle_disposition(self):
        """Bascule entre horizontal et vertical SANS détruire la fenêtre."""
        # Sauvegarder le contenu du champ texte et la taille
        self.text_saisi_sauve = self.text_saisi.get("1.0", tk.END).strip()
        self.size = self.entry_size.get()

        # Inverser
        self.disp = "v" if self.disp == "h" else "h"

        # MAJ libellé du menu
        self._label_disp = "Disposition vertical" if self.disp == "h" else "Disposition horizontal"
        self._menuParam.entryconfigure(1, label=self._label_disp)

        # Ré-appliquer la grille
        self.frame_input.grid_forget()
        self.frame_qr.grid_forget()
        self._appliquer_disposition()

    # ==================================================================
    # Restaurer le texte saisi après un changement de disposition
    # ==================================================================
    def _restaurer_saisie_si_besoin(self):
        if self.text_saisi_sauve:
            self.text_saisi.insert("1.0", self.text_saisi_sauve)
            self.qr_actu(None, self.errCorr, 1)

    # ==================================================================
    # ⑥ Méthodes métier (ex-fonctions globales) — comportement inchangé
    # ==================================================================
    def extract_lang_pays(self, name):
        self.lang = name[-6:-4]
        self._var_langue.set(self.lang)
        self.pays = name[-3:]
        self._var_pays.set(self.pays)
        self.type_texte = 0
        self.qr_actu(None, self.errCorr, 1)

    def borel_Maisonny(self):
        self.lang = "bm"; self._var_langue.set(self.lang)
        self.pays = "FR"; self._var_pays.set(self.pays)
        self.type_texte = 1
        self.qr_actu(None, self.errCorr, 1)

    def abeced_Consigny_fr(self):
        self.lang = "ac"; self._var_langue.set(self.lang)
        self.pays = "FR"; self._var_pays.set(self.pays)
        self.type_texte = 2
        self.qr_actu(None, self.errCorr, 1)

    def abeced_Consigny_es(self):
        self.lang = "ac"; self._var_langue.set(self.lang)
        self.pays = "ES"; self._var_pays.set(self.pays)
        self.type_texte = 3
        self.qr_actu(None, self.errCorr, 1)

    def mode_lire(self):
        self.mode = "lire"
        self._sync_label_mode()
        self.qr_actu(None, self.errCorr, 1)

    def mode_epeler(self):
        self.mode = "epeler"
        self._sync_label_mode()
        self.qr_actu(None, self.errCorr, 1)

    def mode_dicter(self):
        self.mode = "dicter"
        self._sync_label_mode()
        self.qr_actu(None, self.errCorr, 1)

    def _sync_label_mode(self):
        lib = {"lire": "Lect", "dicter": "Dict", "epeler": "Épel"}.get(self.mode, "")
        self.label_mode.config(text=lib, foreground=color_mode[self.mode])

    # Robustesse
    def Robust_Bas(self):
        self.errCorr = 1
        self._sync_robust_menu(0)
        self.qr_actu(None, self.errCorr, 1)

    def Robust_Moy(self):
        self.errCorr = 0
        self._sync_robust_menu(1)
        self.qr_actu(None, self.errCorr, 1)

    def Robust_Qua(self):
        self.errCorr = 3
        self._sync_robust_menu(2)
        self.qr_actu(None, self.errCorr, 1)

    def Robust_Haut(self):
        self.errCorr = 2
        self._sync_robust_menu(3)
        self.qr_actu(None, self.errCorr, 1)

    def _sync_robust_menu(self, active):
        texts = [
            "*  7% : moins robuste - mois grand",
            "* 15%",
            "* 25%",
            "* 30% : plus robuste - plus grand",
        ]
        plain = [
            "   7% : moins robuste - mois grand",
            "  15%",
            "  25%",
            "  30% : plus robuste - plus grand",
        ]
        for i in range(4):
            self._menuRobust.entryconfigure(i, label=texts[i] if i == active else plain[i])

    # ==================================================================
    # QR (ex qr_actu) — strictement identique à l'original
    # ==================================================================
    def qr_actu(self, event, ec, copy):
        self.text_saisi.configure(bg=self.TEXT_SAISI_BG, fg=self.TEXT_SAISI_FG)
        self.frame_qr.config(background=color_mode[self.mode])

        qr = qrcode.QRCode(version=None, error_correction=ec, box_size=5, border=1)

        except_list = ["<enAUS>","<enIND>","<enUSA>","<esESP>","<frCAN>","<nlBEL>","<ptPRT>"]
        url_list = ["https://drive.google.com/file/d/"]
        conv_list = ["/gd/"]

        balise_longue = "<" + self.lang + self.pays + ">"
        text_colle = self.text_saisi.get("1.0", tk.END).strip()

        if "0x89 0x50" in text_colle:
            text_colle = ""
            self.text_saisi.delete("1.0", tk.END)
            self.text_saisi.configure(bg="#ffd4d4", fg="red")
            self.text_saisi.insert("1.0", "Vous collez autre chose que du texte.")

        def adapt_url():
            nonlocal text_colle
            if url_list[0] in text_colle:
                text_colle = text_colle.replace(url_list[0], conv_list[0])
                indice = text_colle.rfind("/view")
                if indice != -1:
                    text_colle = text_colle[:indice]

        def compres_balise(bl):
            if self.type_texte == 0:
                if bl in except_list:
                    balise = "" if url_list[0] in text_colle else balise_longue
                elif bl == "<frFRA>":
                    balise = "<fr>" if len(text_colle) >= 4 else ""
                elif url_list[0] in text_colle:
                    balise = ""
                else:
                    balise = "<" + self.lang + ">"
            elif self.type_texte == 1:
                balise = "" if url_list[0] in text_colle else "-bm-"
            elif self.type_texte == 2:
                balise = "" if url_list[0] in text_colle else "*fr*"
            else:
                balise = "" if url_list[0] in text_colle else "*es*"
            self.balise = balise
            return balise

        balise_courte = compres_balise(balise_longue)
        adapt_url()
        text = balise_courte + text_colle
        if self.mode == "dicter":
            text += "#d"
        if self.mode == "epeler":
            text += "#e"
        text = obfusor.enobfus(text)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        try:
            int(self.entry_size.get())
        except ValueError:
            self.entry_size.delete(0, tk.END)
            self.entry_size.insert(0, "150")
        new_size = int(self.entry_size.get())
        new_size = max(50, min(150, new_size))
        self.entry_size.delete(0, tk.END)
        self.entry_size.insert(0, str(new_size))
        self.new_size_var.set(new_size)

        resized_img = img.resize((new_size, new_size))
        resized_img.save(tempPath("QR_Tempor.png"))

        fond_qr = Image.open(tempPath("QR_Tempor.png")).convert('RGBA')
        logo_a_sup = Image.open(resourcePath('assets/Bouche.png'))
        h_sup = round(new_size / 6)
        l_sup = round(new_size * 1.5 / 6)
        logo_a_sup = logo_a_sup.resize((l_sup, h_sup))
        x = round((new_size - l_sup) / 2)
        y = round((new_size - h_sup) / 2)
        fond_qr.paste(logo_a_sup, (x, y), logo_a_sup)

        mod_indic = Image.new('RGBA', (5, 5), color_mode[self.mode])
        pos = new_size - 5
        fond_qr.paste(mod_indic, (pos, pos), mod_indic)
        fond_qr.save(tempPath("QR_Tempor.png"))

        img_code = ImageTk.PhotoImage(Image.open(tempPath("QR_Tempor.png")))
        self.label_qr.configure(image=img_code)
        self.label_qr.image = img_code

        if not self.qr_deja_genere:
            self.qr_deja_genere = True
            self.button_copy.config(state="normal")

        if copy == 1:
            self.copie_png(tempPath("QR_Tempor.png"))

    # ==================================================================
    # Copier (presse-papier) — identique à l'original
    # ==================================================================
    def copy_QR(self):
        if not self.qr_deja_genere:
            return
        self.copie_png(tempPath("QR_Tempor.png"))

    def copie_png(self, image_path):
        if platform.system() == 'Windows':
            try:
                from io import BytesIO
                import win32clipboard
            except ImportError:
                Messagebox.show_error(
                    "Le module 'pywin32' est requis…", "Module manquant", parent=self.root
                )
                return
            def send_to_clipboard(clip_type, data):
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(clip_type, data)
                win32clipboard.CloseClipboard()
            filepath = tempPath("QR_Tempor.png")
            image = Image.open(filepath)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            send_to_clipboard(win32clipboard.CF_DIB, data)
            self.actu_icon_mem("png")

        elif platform.system() == 'Darwin':
            try:
                from AppKit import NSPasteboard, NSPasteboardTypePNG, NSImage
                from io import BytesIO
            except ImportError:
                Messagebox.show_error(
                    "Le module 'PyObjC' (AppKit) est requis…", "Module manquant", parent=self.root
                )
                return
            image_path = tempPath("QR_Tempor.png")
            image = Image.open(image_path)
            with BytesIO() as buffer:
                image.save(buffer, format='PNG')
                img_data = buffer.getvalue()
            ns_image = NSImage.alloc().initWithData_(img_data)
            pasteboard = NSPasteboard.generalPasteboard()
            pasteboard.clearContents()
            pasteboard.setData_forType_(ns_image.TIFFRepresentation(), NSPasteboardTypePNG)

        elif platform.system() == 'Linux':
            if shutil.which("xclip") is None:
                Messagebox.show_error(
                    "Le programme 'xclip' est requis…", "Programme manquant", parent=self.root
                )
                return
            image_path = tempPath("QR_Tempor.png")
            os.system(f'xclip -selection clipboard -t image/png -i "{image_path}"')
        else:
            Messagebox.show_error(
                f"OS non pris en charge : {platform.system()}.", "OS non pris en charge",
                parent=self.root,
            )

    # ==================================================================
    # Événements de saisie
    # ==================================================================
    def _delete_png(self, event):
        string = "0x89 0x50"
        index = self.text_saisi.search(string, "1.0", "end")
        if index:
            self.text_saisi.delete(index, "end")

    def _paste_text(self, event):
        self.text_saisi.delete("1.0", tk.END)
        self.text_saisi.event_generate('<<Paste>>')
        self.qr_actu(event, self.errCorr, 1)

    def _on_key_release(self, event):
        if self.id_debounce is not None:
            self.root.after_cancel(self.id_debounce)
        self.id_debounce = self.root.after(300, lambda: self.qr_actu(None, self.errCorr, 1))

    # ==================================================================
    # Icône du presse-papier
    # ==================================================================
    def actu_icon_mem(self, mem):
        img = ImageTk.PhotoImage(Image.open(self.icon_path(f"PP-{mem}-20px.png")))
        self.label_mem.configure(image=img)
        self.label_mem.image = img

    def scan_clipboard(self):
        try:
            contenu = self.root.clipboard_get()
            if "0x89 0x50" in contenu:
                self.actu_icon_mem("png")
            else:
                self.actu_icon_mem("str")
        except tk.TclError:
            self.actu_icon_mem("vid")
            if platform.system() in ('Windows', 'Darwin'):
                self.actu_icon_mem("png")

    def _periodic_scan_clipboard(self):
        self.scan_clipboard()
        self.id_boucle = self.root.after(500, self._periodic_scan_clipboard)

    def quit_application(self, event=None):
        if self.id_boucle is not None:
            self.root.after_cancel(self.id_boucle)
        if self.id_debounce is not None:
            self.root.after_cancel(self.id_debounce)
        self.root.destroy()

    # ==================================================================
    # Thème
    # ==================================================================
    def toggle_theme(self):
        self.theme = "darkly" if self.theme == "litera" else "litera"
        self.root.style.theme_use(self.theme)
        self._install_custom_button_styles()
        self.TEXT_SAISI_BG, self.TEXT_SAISI_FG = self._get_text_saisi_colors()
        self.text_saisi.configure(bg=self.TEXT_SAISI_BG, fg=self.TEXT_SAISI_FG)
        self.frame_qr.config(background=color_mode[self.mode])
        label = "Thème sombre" if self.theme == "litera" else "Thème clair"
        self._menuParam.entryconfigure(2, label=label)
        self.photo_copy = tk.PhotoImage(file=self.icon_path("Copy-20px-QR.png"))
        self.button_copy.config(image=self.photo_copy)
        self.scan_clipboard()

    # ==================================================================
    # PDF (ex verif_pdf + _launch_pdf_processing) — identique
    # ==================================================================
    def verif_pdf(self):
        if not PDF_VERIF_AVAILABLE:
            Messagebox.show_error(
                f"Impossible d'importer MAEL_Verif_PDF.\n\n{PDF_VERIF_ERROR}",
                "Dépendances manquantes", parent=self.root,
            )
            return
        self.root.attributes('-topmost', 0)
        input_pdf = filedialog.askopenfilename(
            parent=self.root, title="Sélectionner le PDF à vérifier",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
        )
        self.root.attributes('-topmost', 1)
        if not input_pdf:
            return
        input_path = Path(input_pdf)
        suggested_output = input_path.with_name(f"{input_path.stem}_annotated.pdf")
        self.root.attributes('-topmost', 0)
        output_pdf = filedialog.asksaveasfilename(
            parent=self.root, title="Enregistrer le PDF annoté",
            initialfile=suggested_output.name,
            initialdir=str(input_path.parent),
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        self.root.attributes('-topmost', 1)
        if not output_pdf:
            return
        if Path(input_pdf).resolve() == Path(output_pdf).resolve():
            Messagebox.show_error(
                "Le fichier de sortie ne peut pas être identique au fichier d'entrée.",
                "Chemins identiques", parent=self.root,
            )
            return
        self._launch_pdf_processing(input_pdf, output_pdf)

    def _launch_pdf_processing(self, input_pdf, output_pdf):
        prog = ttkb.Toplevel(self.root)
        prog.title("Vérification PDF - Traitement en cours")
        prog.attributes('-topmost', 1)
        prog.geometry("780x500")
        prog.resizable(True, True)
        prog.transient(self.root)
        prog.grab_set()
        header = ttkb.Label(prog, text=f"Traitement de : {Path(input_pdf).name}",
                            font=("Arial", 11, "bold"))
        header.pack(pady=(10, 5))
        log_frame = ttkb.Frame(prog)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        log_text = ttkb.Text(log_frame, font=("Courier", 9), wrap="word", height=20)
        log_text.pack(side="left", fill="both", expand=True)
        scroll = ttkb.Scrollbar(log_frame, command=log_text.yview)
        scroll.pack(side="right", fill="y")
        log_text.config(yscrollcommand=scroll.set)
        status = ttkb.Label(prog, text="Traitement en cours...",
                            font=("Arial", 10, "italic"), bootstyle="info")
        status.pack(pady=(0, 5))
        close_btn = ttkb.Button(prog, text="Fermer", bootstyle="secondary",
                                state="disabled", width=12)
        close_btn.pack(pady=(0, 10))
        done_flag = {"done": False, "success": False, "error": None}
        old_stdout = sys.stdout
        msg_queue = queue.Queue()

        class _QWriter:
            def write(self, s):
                if s: msg_queue.put(s)
            def flush(self): pass

        def worker():
            try:
                processor = QrPdfProcessor(dpi=250, fallback_dpi=400, verbose=True)
                processor.run(input_pdf, output_pdf)
                done_flag["success"] = True
            except Exception as exc:
                done_flag["error"] = str(exc)
                msg_queue.put(f"\n[ERREUR] {exc}\n")
            finally:
                done_flag["done"] = True

        def poll():
            try:
                while True:
                    msg = msg_queue.get_nowait()
                    log_text.insert(tk.END, msg)
            except queue.Empty:
                pass
            log_text.see(tk.END)
            if done_flag["done"]:
                sys.stdout = old_stdout
                if done_flag["success"]:
                    status.config(text=f"Terminé - PDF écrit : {output_pdf}", bootstyle="success")
                    Messagebox.show_info(f"Le PDF annoté a été généré :\n\n{output_pdf}",
                                         "Traitement terminé", parent=prog)
                else:
                    status.config(text=f"Erreur : {done_flag['error']}", bootstyle="danger")
                    Messagebox.show_error(f"Une erreur est survenue :\n\n{done_flag['error']}",
                                          "Erreur de traitement", parent=prog)
                close_btn.config(state="normal", command=prog.destroy)
                prog.grab_release()
            else:
                prog.after(100, poll)

        def on_close():
            if done_flag["done"]:
                sys.stdout = old_stdout
                prog.destroy()
            else:
                Messagebox.show_info(
                    "Veuillez attendre la fin du traitement avant de fermer cette fenêtre.",
                    "Traitement en cours", parent=prog,
                )
        prog.protocol("WM_DELETE_WINDOW", on_close)
        sys.stdout = _QWriter()
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        prog.after(100, poll)

    # ==================================================================
    # Fenêtres d'aide / info
    # ==================================================================
    def toplevel_aide(self):
        toplevel = ttkb.Toplevel(self.root)
        toplevel.title(f"Aide pour MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)
        toplevel.resizable(width=False, height=False)
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('assets/icon.png')))
        frame_Image = ttkb.Frame(toplevel, padding=20)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        restrictions_label = ttkb.Label(
            frame_Image,
            text="Restrictions :\n- MAEL ne peut pas encore prononcer seuls, les mots formés du son d'une seule voyelle.\n"
                 "Exemples : 'haut', 'ou', 'eau', 'un', 'on', 'haie', 'es', 'est'...\n"
                 "Ces mots doivent être accompagnés d'un contexte ou d'un déterminant.\n"
                 "Pour prononcer des voyelles seules, utilisez les 'Sons Borel-Maisonny'\n"
                 "Menu : Langues > Spécial > Sons Borel-Maisonny",
            font=("Arial", 10), justify="left",
        )
        restrictions_label.pack(side="bottom", pady=5)
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("assets/Aide-V4.png")))
        image_aide = ttkb.Label(frame_Image, image=img_png)
        image_aide.image = img_png
        image_aide.pack(side="bottom", fill="both", expand=True)
        if platform.system() == 'Linux':
            install_xclip = ttkb.Label(
                frame_Image,
                text="Sous Linux, installez \"xclip\" avant la première utilisation --> sudo apt-get install xclip",
                font=("Arial", 11), bootstyle="warning",
            )
            install_xclip.pack(side="bottom", fill="both", pady=5)

    def toplevel_info(self):
        toplevel = ttkb.Toplevel(self.root)
        toplevel.title(f"À propos de MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)
        toplevel.resizable(width=False, height=False)
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('assets/icon.png')))
        frame_Image = ttkb.Frame(toplevel, padding=20)
        frame_Texte = ttkb.Frame(toplevel, padding=20)
        frame_Licence = ttkb.Frame(toplevel, padding=3)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        frame_Texte.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        frame_Licence.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        img_text = ImageTk.PhotoImage(Image.open(resourcePath("assets/Infos-450px.png")))
        interf_MAELScan = ttkb.Label(frame_Image, image=img_text)
        interf_MAELScan.image = img_text
        interf_MAELScan.pack(side="left", fill="both", expand=True)
        img_screenShot = ImageTk.PhotoImage(Image.open(resourcePath("assets/Interface_MAEL_Scan_450px.png")))
        interf_MAELScan2 = ttkb.Label(frame_Image, image=img_screenShot)
        interf_MAELScan2.image = img_screenShot
        interf_MAELScan2.pack(side="left", fill="both", expand=True)
        licence_label = ttkb.Label(
            frame_Licence, text="Logiciel sous licence GNU GPL v3",
            font=("Arial", 11), anchor="center",
        )
        licence_label.pack(side="bottom", fill="both", pady=0)

    def toplevel_BM(self):
        toplevel = ttkb.Toplevel(self.root)
        toplevel.title(f"Sons Borel-Maisonny - MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)
        toplevel.resizable(width=False, height=False)
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('assets/icon.png')))
        frame_Image = ttkb.Frame(toplevel, padding=10)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("assets/Borel-Maisonny.png")))
        image_BM = ttkb.Label(frame_Image, image=img_png)
        image_BM.image = img_png
        image_BM.pack(side="bottom", fill="both", expand=True)

    def toplevel_AC(self):
        toplevel = ttkb.Toplevel(self.root)
        toplevel.title(f"Abécédaire Consigny - MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)
        toplevel.resizable(width=False, height=False)
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('assets/icon.png')))
        frame_Image = ttkb.Frame(toplevel, padding=10)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("assets/Abecedaire_Consigny.png")))
        image_BM = ttkb.Label(frame_Image, image=img_png)
        image_BM.image = img_png
        image_BM.pack(side="bottom", fill="both", expand=True)

    # ==================================================================
    # Utilitaires internes
    # ==================================================================
    def icon_path(self, base_name):
        if self.theme == "darkly" and base_name in ICONES_AVEC_VARIANTE_SOMBRE:
            name, ext = os.path.splitext(base_name)
            return resourcePath(f"assets/{name}-W{ext}")
        return resourcePath(f"assets/{base_name}")

    def _install_custom_button_styles(self):
        style = self.root.style
        bg = style.colors.bg
        styles = {
            "Lecture": ("#0066CC", color_hover["lire"],   "#0066CC"),
            "Epeler":  ("#009900", color_hover["epeler"], "#009900"),
            "Reserve": ("#9933FF", color_hover["reserve"],"#9933FF"),
            "Dicter":  ("#FF4040", color_hover["dicter"], "#FF4040"),
        }
        for name, (fg, hover_bg, bordercolor) in styles.items():
            style_name = f"{name}.TButton"
            style.configure(style_name, foreground=fg, background=bg,
                            bordercolor=bordercolor, focuscolor=bordercolor,
                            lightcolor=bg, darkcolor=bg)
            style.map(style_name,
                      background=[("active", hover_bg), ("!active", bg)],
                      foreground=[("active", fg),       ("!active", fg)])

    def _get_text_saisi_colors(self):
        colors = self.root.style.colors
        try:
            bg = colors.inputbg
        except AttributeError:
            bg = colors.bg
        fg = "blue" if self.theme == "litera" else "#B3D9FF"
        return bg, fg


# ======================================================================
# Point d'entrée (3 lignes au lieu de 2000)
# ======================================================================
if __name__ == "__main__":
    app = MaelGenApp()
    app.root.mainloop()
