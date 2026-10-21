"""
#############################################################################
#
#   Application "MAEL Gen" - GPL v3
#   Multi-logiciel d'Assistance à l'Enseignement des Langues
#   "Donnez une voix à vos documents pédagogiques"
#
#   Générateur de codes QR dédiè aux applications :
#   - "MAEL Scan" (GPL v3)
#   - "MAEL Phrases" (GPL v3)
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
- Actualiser la doc
- Étudier le cas : "Mode dictée" + link Google Drive
- Ajouter le mode épeler pour EN ES PT
- Corriger le bug de l'accent séparé de la lettre sous LINUX ?
- Étudier les messages Warning
- Faire charger les modules spécifiques à chaque OS une seule fois au début
  du programme en fonction de l'OS détecté.
- Permettre le glisser - déposer du code QR vers l'éditeur externe
- Réparer l'affichage de l'icône "Presse papier vide"
- Ajouter des icônes aux "toplevel"  --> À vérifier !

#############################################################################
#                   Informations pour le développement
#############################################################################

>>>>> Environnement de développement <<<<<

NixOS 26.05
Python 3.13

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

###### IMPORTATION DES MODULES ######

import tkinter as tk                     # Conservé pour PhotoImage, IntVar, StringVar, constantes (END, LEFT, ...)
import ttkbootstrap as ttkb              # Widgets et fenêtre thématiques
from ttkbootstrap.dialogs import Messagebox  # Boîtes de dialogue thématiques
from tkinter import filedialog           # Sélecteur de fichiers (pas d'équivalent ttkbootstrap)

import qrcode
from PIL import Image, ImageTk

import os        # Pour utiliser "xclip" et copier le png dans le presse-papier sous Linux.
import sys       # Pour chemin relatif
import shutil    # Pour vérifier la présence de "xclip" sous Linux
import tempfile  # Pour écrire les fichiers temporaires hors du dossier des ressources
import threading # Pour lancer le traitement PDF dans un thread séparé
import queue     # Pour la communication thread → UI

from pathlib import Path   # Pour la manipulation des chemins PDF

import platform  # Pour détecter l'OS et choisir le module correspondant

# Import de la classe d'obfuscation depuis le fichier externe MAEL_obfus.py
from MAEL_obfus import Obfus

# Import conditionnel du traitement PDF (peut échouer si les dépendances ne sont pas installées).
# Un flag et un message d'erreur permettent de dégrader proprement l'application au lieu de planter au démarrage.
try:
    from MAEL_Verif_PDF import QrPdfProcessor
    PDF_VERIF_AVAILABLE = True
    PDF_VERIF_ERROR = ""
except ImportError as exc:
    PDF_VERIF_AVAILABLE = False
    PDF_VERIF_ERROR = str(exc)
    QrPdfProcessor = None   # Placeholder pour éviter un NameError si l'entrée de menu est appelée

############## PARAMÈTRES SELON LA VERSION et l'OS #####################
# ---------------------------
# >>>> Nom de la version <<<<
# ---------------------------
# Version construite dynamiquement à partir du nom réel de l'OS détecté.
# On traduit la valeur brute renvoyée par platform.system() en un libellé
# lisible ; si l'OS n'est pas dans le dictionnaire, on affiche la valeur brute.
_qrgen_os_label = {
    "Linux":   "Linux",
    "Darwin":  "macOS",
    "Windows": "Windows",
}.get(platform.system(), platform.system())

qrgen_version = f"- V6.1 pour {_qrgen_os_label}"

# ----------------------------
#     >>>> Couleurs <<<<
# ----------------------------
# Couleurs de référence pour la cohérence avec l'ancien design Tk.
# En ttkbootstrap, les couleurs de fond sont gérées par le thème ;
# ces valeurs servent uniquement pour :
#   - la couleur du texte des labels de mode (label_mode)
#   - la couleur de la bordure du cadre QR (frame_qr)
#   - la couleur des styles personnalisés des boutons (voir plus bas)
coul_interface = "#FFFFFF"
color_mode = {"dicter": "#FF4040", "epeler": "#009900", "lire": "#0066CC"}

# Couleurs de texte pour chaque bouton de mode (fg) et couleur de survol (bg léger)
color_hover = {
    "lire":    "#B3D9FF",   # Bleu clair
    "epeler":  "#B3F0B3",   # Vert clair
    "reserve": "#D9B3FF",   # Violet clair
    "dicter":  "#FFB3B3",   # Rouge clair
}

# -------------------------------
# >>>> Dimensions selon l'OS <<<<
# -------------------------------
geom_horiz = "465x173"        # Pour Linux et OSX
# geom_horiz = "470x190"        # Pour Windows

geom_verti = "270x340"        # Pour Linux et OSX
# geom_verti = "300x390"        # Pour Windows

# Écartement entre le widgets de la taille (en px)
ecart_h = 4    # Disposition vertical sous Linux
ecart_v = 1    # Disposition horizontal sous Linux
# ecart_h = 3    # Disposition vertical sous OSX
# ecart_v = 1    # Disposition horizontal sous OSX
# ecart_h = 4    # Disposition vertical sous Windows
# ecart_v = 5    # Disposition horizontal sous Windows

# Largeur fixe du cadre "frame_lang" (langue / pays / mode / bouton Copier), en pixels
LARGEUR_FRAME_LANG = 45


#################################################################
# >>>>> Dossiers : ressources (lecture) et temporaires (écriture) <<<<<
#################################################################

# Dossier du script (ou du bundle PyInstaller)
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sous-dossier temporaire dédié à MAEL Gen (créé si absent)
TEMP_DIR = os.path.join(tempfile.gettempdir(), "MAEL_Gen")
os.makedirs(TEMP_DIR, exist_ok=True)

# Chemin du PNG temporaire du QR code (hors dossier des ressources)
QR_TEMP_PATH = os.path.join(TEMP_DIR, "QR_Tempor.png")


#################################################################

global_lang = "fr"          # Conserver la langue en cas de changement de disposition
global_pays = "FRA"
global_errCorr = 3          # qrcode.constants.ERROR_CORRECT_Q

# Comment traiter l'information écrite dans le champ de texte :
global_type = 0             # 0 = langue  /  1 = Borel Maisonny  /  2 = Abécedaire Consigny FR  /  3 = Abécedaire Consigny FR
global_mode = "lire"     # lecture / dictee / epeler
global_balise = ""          # Balise par défaut

# Contenu du widget de saisie, conservé en mémoire lors d'un changement de disposition.
global_text_saisi = ""

# Taille courante du code QR, conservée entre les changements de disposition.
global_size = "150"

# Thème courant ttkbootstrap : "litera" (clair) ou "darkly" (sombre).
# Conservé entre les changements de disposition pour que l'utilisateur
# ne perde pas son choix.
global_theme = "litera"

# Icônes pour lesquelles une variante "mode sombre" existe.
# --> Le suffixe "-W" est inséré avant l'extension du fichier
#     quand le thème courant est "darkly".
#     Toute icône absente de cet ensemble est utilisée telle quelle,
#     quel que soit le thème.
ICONES_AVEC_VARIANTE_SOMBRE = {
    "Copy-20px-QR.png",
    "PP-png-20px.png",
    "PP-str-20px.png",
    "PP-vid-20px.png",
}

# Instance unique de la classe d'obfuscation (aucun état d'instance : un singleton suffit)
obfusor = Obfus()


# ================================================================= #
#   Styles personnalisés ttkbootstrap pour les boutons de mode       #
# ================================================================= #
# On définit quatre styles de bouton "TButton" personnalisés, un par
# mode, avec une couleur de texte et une couleur de survol cohérentes
# avec l'ancien design Tk. ttkbootstrap gère nativement les états
# "active" (survol) via style.map(), ce qui remplace avantageusement
# l'ancien bind_hover() manuel.
#
# Le fond du bouton est lu dynamiquement depuis le thème courant
# (style.colors.bg), afin de rester cohérent lorsqu'on bascule entre
# thème clair et thème sombre.

def _install_custom_button_styles(style):
    """
    Installe les styles personnalisés pour les 4 boutons de mode
    (L / E / C / D) sur l'objet Style ttkbootstrap fourni.

    Chaque style conserve la couleur de texte de son mode, adopte le
    fond du thème courant et passe à une teinte claire au survol, en
    cohérence avec color_hover.
    """
    # Fond du thème courant : blanc cassé en clair, sombre en sombre.
    bg = style.colors.bg

    # (couleur de texte, couleur de survol, couleur de bordure)
    styles = {
        "Lecture": ("#0066CC", color_hover["lire"],   "#0066CC"),
        "Epeler":  ("#009900", color_hover["epeler"], "#009900"),
        "Reserve": ("#9933FF", color_hover["reserve"],"#9933FF"),
        "Dicter":  ("#FF4040", color_hover["dicter"], "#FF4040"),
    }

    for name, (fg, hover_bg, bordercolor) in styles.items():
        style_name = f"{name}.TButton"
        style.configure(
            style_name,
            foreground=fg,
            background=bg,
            bordercolor=bordercolor,
            focuscolor=bordercolor,
            lightcolor=bg,
            darkcolor=bg,
        )
        # États du bouton : normal (fond du thème, texte coloré) et
        # survol/actif (fond teinté, texte coloré).
        style.map(
            style_name,
            background=[("active", hover_bg), ("!active", bg)],
            foreground=[("active", fg),       ("!active", fg)],
        )


# ================================================================= #
#   Couleurs du widget de saisie selon le thème                      #
# ================================================================= #
# Le fond du widget "text_saisi" doit suivre le thème (clair → fond
# clair, sombre → fond sombre). La couleur du texte est choisie pour
# rester lisible sur ce fond : bleu foncé en clair, bleu clair en
# sombre.
#
# La fonction ci-dessous est appelée à la création de la fenêtre et à
# chaque basculement de thème. Elle renvoie un tuple (bg, fg).

def _get_text_saisi_colors(style):
    """
    Retourne les couleurs (bg, fg) à appliquer au widget de saisie
    selon le thème courant.
    """
    # Couleur de fond des champs de saisie du thème courant.
    # ttkbootstrap expose inputbg pour ce cas précis ; si l'attribut
    # n'est pas disponible, on retombe sur le fond général.
    colors = style.colors
    try:
        bg = colors.inputbg
    except AttributeError:
        bg = colors.bg

    # Couleur du texte : bleu foncé en thème clair, bleu clair en sombre.
    fg = "blue" if global_theme == "litera" else "#B3D9FF"

    return bg, fg


# Mettre toute l'application dans une fonction pour pouvoir la relancer avec le paramètre vertical "v" ou horizontal "h"
# Il doit exister un moyen avec des class, mais je dois étudier pour comprendre ça à fond

def application(disp):

    ###### FENETRE PRINCIPALE ######

    # ttkbootstrap : fenêtre principale thématique.
    # Le thème est choisi dynamiquement depuis global_theme, de manière
    # à ce que le choix "clair / sombre" de l'utilisateur survive à un
    # changement de disposition (qui détruit et recrée la fenêtre).
    root = ttkb.Window(themename=global_theme)

    # Installer les styles personnalisés pour les boutons de mode.
    # À faire une fois la Window créée, avant toute création de widget.
    _install_custom_button_styles(root.style)

    # Couleurs du widget de saisie, adaptées au thème courant.
    # Ces variables sont lues par qr_actu() pour restaurer l'état normal
    # après une alerte visuelle (par exemple un collage de PNG).
    TEXT_SAISI_BG, TEXT_SAISI_FG = _get_text_saisi_colors(root.style)

    id_boucle = None            # Déclarer id_boucle comme variable locale
    id_debounce = None          # Déclarer id_debounce pour le debounce du champ de texte
    qr_deja_genere = False      # Drapeau : aucun QR n'a encore été généré au démarrage

    root['padx'] = 5  # Marge horizontale de 20 pixels
    root['pady'] = 5  # Marge verticale de 10 pixels
    root.title(f"MAEL Gen {qrgen_version}")
    root.attributes('-topmost', True)  # Maintenir la fenêtre toujours au dessus

    root.resizable(width=False, height=False)

    if disp == "h":
        global ecart_h
        ecart = ecart_h

    if disp == "v":
        global ecart_v
        ecart = ecart_v

    ###### FONCTIONS ET VARIABLES ######

    # Variable glogale pour recevoir la taille du code QR
    new_size_var = tk.IntVar()  # Créez une variable IntVar
    new_size_var.set(100)  # Définissez la valeur initiale

    # Création de la fonction pour rendre locale la recherche des fichiers sons (Nécessaire pour le paquet exécutable)
    # --> Pointe désormais vers le dossier du script, pas le cwd.
    def resourcePath(relativePath):
        return os.path.join(BASE_DIR, relativePath)

    # Sélection d'icône selon le thème courant.
    # --> Pour les icônes listées dans ICONES_AVEC_VARIANTE_SOMBRE,
    #     on insère le suffixe "-W" avant l'extension en mode sombre.
    #     Exemple : "PP-vid-20px.png" → "PP-vid-20px-W.png".
    def icon_path(base_name):
        """
        Retourne le chemin absolu de l'icône demandée, en tenant compte
        du thème courant :
          - thème clair : nom d'origine,
          - thème sombre : nom avec suffixe "-W" (si la variante existe).
        """
        if global_theme == "darkly" and base_name in ICONES_AVEC_VARIANTE_SOMBRE:
            name, ext = os.path.splitext(base_name)
            return resourcePath(f"assets/{name}-W{ext}")
        return resourcePath(f"assets/{base_name}")

    # Chemin des fichiers temporaires (hors dossier des ressources)
    def tempPath(filename):
        return os.path.join(TEMP_DIR, filename)

    # Ajout d'une icône de l'application
    root.iconphoto(True, tk.PhotoImage(file=resourcePath('assets/icon.png')))

    # --------   Gestion de la robustesse des code QR (Niveau de correction)   --------#

    # Fonction pour actualiser le texte d'un menu avec un nouveau texte
    def clicked(menu, index, new_text):
        menu.entryconfigure(index, label=new_text)

    # 4 fonctions changeant la robustesse des codes RQ et actualisant les menus en conséquence
    def Robust_Bas():
        global global_errCorr
        ec = 1  # qrcode.constants.ERROR_CORRECT_L
        qr_actu(None, ec,
                1)  # Actualiser le code QR si changement de langue - "None" nécessaire parce que la fonction n'est pas appelée par un événement ?
        global_errCorr = ec
        clicked(menuRobust, 0, "*  7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Moy():
        global global_errCorr
        ec = 0  # qrcode.constants.ERROR_CORRECT_M
        qr_actu(None, ec, 1)
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "* 15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Qua():
        global global_errCorr
        ec = 3  # qrcode.constants.ERROR_CORRECT_Q
        qr_actu(None, ec, 1)
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "* 25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Haut():
        global global_errCorr
        ec = 2  # qrcode.constants.ERROR_CORRECT_H
        qr_actu(None, ec, 1)
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "* 30% : plus robuste - plus grand")

    # --------   Création d'une fonction créant le code QR   --------#
    # "ec" --> variable locale de "error_correction"
    # copy --> 0 = ne copie pas le code QR dans le presse papier / 1 = copie-le
    def qr_actu(event, ec, copy):

        nonlocal qr_deja_genere

        # Réinitialiser la couleur du fond et la couleur du texte du widget "text_saisi"
        # --> On restaure les couleurs adaptées au thème courant, pas un blanc codé en dur.
        #     C'est ce qui évite que la zone de texte redevienne blanche à chaque frappe
        #     lorsqu'on est en thème sombre.
        text_saisi.configure(bg=TEXT_SAISI_BG, fg=TEXT_SAISI_FG)

        # Actualiser le fond de cadre du code QR (bordure visible autour du code QR)
        frame_qr.config(background=color_mode[global_mode])

        # Création et initialisation de l'objet qrcode.QRCode()
        qr = qrcode.QRCode(
            version=None,
            error_correction=ec,
            box_size=5,
            border=1
        )

        # --------   Création de la balise   --------#

        # Liste des exceptions : balises longues non réductibles = alternatives aux pays par défaut pour MIT app inventor
        except_list = ["<enAUS>", "<enIND>", "<enUSA>", "<esESP>", "<frCAN>", "<nlBEL>", "<ptPRT>"]

        # Liste des URL à adapter
            # Cas 0 -->        Google Drive
        url_list = ["https://drive.google.com/file/d/"]
        conv_list = ["/gd/"]          # Balise qui sera remplacée dans MAEl Scan par : https://drive.google.com/uc?id=

        # Création des balises longues
        balise_longue = "<" + langue.get() + pays.get() + ">"

        # --------   Vérification que ce n'est pas un .png qui est collé   --------#

        text_colle = text_saisi.get("1.0", tk.END).strip()

        # Si le texte commence par la séquence hexdécimale d'un .png, vide le Widget "text_saisi"
        if "0x89 0x50" in text_colle:
            text_colle = ""
            text_saisi.delete("1.0", tk.END)
            text_saisi.configure(bg="#ffd4d4", fg="red")
            text_saisi.insert("1.0", "Vous collez autre chose que du texte.")

        # Fonction qui modifie les URL pour les rendre compatibles avec MAEL
        def adapt_url():
            nonlocal text_colle
            # ==> Cas Google Drive :
            if url_list[0] in text_colle:
                text_colle = text_colle.replace(url_list[0], conv_list[0])
                indice = text_colle.rfind("/view")
                if indice != -1:
                    text_colle = text_colle[:indice]

         # Création d'une fonction pour créer la balise courte à partir de la balise longue.
        def compres_balise(bl):
            global global_balise

            if global_type == 0:
                if bl in except_list:
                    if url_list[0] in text_colle:
                        balise = ""
                    else:
                        balise = balise_longue
                elif bl == "<frFRA>":
                    if len(text_colle) < 4:
                        balise = "<fr>"
                    else:
                        balise = ""
                elif url_list[0] in text_colle:
                    balise = ""
                else:
                    balise = "<" + langue.get() + ">"

            if global_type == 1:
                if url_list[0] in text_colle:
                    balise = ""
                else:
                    balise = "-bm-"

            if global_type == 2:
                if url_list[0] in text_colle:
                    balise = ""
                else:
                    balise = "*fr*"

            if global_type == 3:
                if url_list[0] in text_colle:
                    balise = ""
                else:
                    balise = "*es*"

            global_balise = balise
            return balise

        balise_courte = compres_balise(balise_longue)

        # --------   Création du texte qui sera mis dans le code QR   --------#

        adapt_url()

        text = balise_courte + text_colle

        # Ajouter la balise de fin pour le mode "Dictée" ou "Èpeler"
        if global_mode == "dicter":
            text = text + "#d"
        if global_mode == "epeler":
            text = text + "#e"

        # Obfusquer le texte à mettre dans le code QR (remplace l'ancienne fonction encrypt())
        text = obfusor.enobfus(text)

        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # --------   Redimensionnement de l'objet qr   --------#

        nonlocal new_size_var

        try:
            int(entry_size.get())
        except ValueError:
            new_size_var.set(150)
            entry_size.delete(0, tk.END)
            entry_size.insert(0, str(new_size_var.get()))

        new_size_var.set(int(entry_size.get()))

        if new_size_var.get() > 150:
            new_size_var.set(150)
        if new_size_var.get() < 50:
            new_size_var.set(50)

        entry_size.delete(0, tk.END)
        entry_size.insert(0, str(new_size_var.get()))

        resized_img = img.resize((new_size_var.get(), new_size_var.get()))

        # --------   Création / affichage du fichier PNG   --------#

        resized_img.save(tempPath("QR_Tempor.png"))

        fond_qr = Image.open(tempPath("QR_Tempor.png"))
        fond_qr = fond_qr.convert('RGBA')
        logo_a_sup = Image.open(resourcePath('assets/Bouche.png'))

        h_sup = round(new_size_var.get() / 6)
        l_sup = round(new_size_var.get() * 1.5 / 6)

        logo_a_sup = logo_a_sup.resize((l_sup, h_sup))

        x = round((new_size_var.get() - l_sup) / 2)
        y = round((new_size_var.get() - h_sup) / 2)

        fond_qr.paste(logo_a_sup, (x, y), logo_a_sup)
        fond_qr.save(tempPath("QR_Tempor.png"))

        mod_indic = Image.new('RGBA', (5, 5), color_mode[global_mode])

        pos = int(fond_qr.size[0] - 5)

        fond_qr.paste(mod_indic, (pos, pos), mod_indic)
        fond_qr.save(tempPath("QR_Tempor.png"))

        img_code = ImageTk.PhotoImage(Image.open(tempPath("QR_Tempor.png")))
        label_qr.configure(image=img_code)
        label_qr.image = img_code

        # Le QR existe maintenant : activer le bouton "Copier"
        if not qr_deja_genere:
            qr_deja_genere = True
            button_copy.config(state="normal")

        if copy == 1:
            copie_png(tempPath("QR_Tempor.png"))

    # --------   Fonction copiant l'image dans le presse papier   --------#

    def copie_png(image_path):
        if platform.system() == 'Windows':

            try:
                from io import BytesIO
                import win32clipboard
            except ImportError:
                Messagebox.show_error(
                    "Le module 'pywin32' est requis pour copier le code QR "
                    "dans le presse-papier sous Windows.\n\n"
                    "Installez-le avec la commande :\n"
                    "    pip install pywin32",
                    "Module manquant",
                    parent=root,
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

            actu_icon_mem("png")

        elif platform.system() == 'Darwin':

            try:
                from AppKit import NSPasteboard, NSPasteboardTypePNG, NSImage
                from io import BytesIO
            except ImportError:
                Messagebox.show_error(
                    "Le module 'PyObjC' (AppKit) est requis pour copier le code QR "
                    "dans le presse-papier sous macOS.\n\n"
                    "Installez-le avec la commande :\n"
                    "    pip install PyObjC",
                    "Module manquant",
                    parent=root,
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
                    "Le programme 'xclip' est requis pour copier le code QR "
                    "dans le presse-papier sous Linux.\n\n"
                    "Installez-le avec la commande :\n"
                    "    sudo apt-get install xclip",
                    "Programme manquant",
                    parent=root,
                )
                return

            image_path = tempPath("QR_Tempor.png")
            os.system(f'xclip -selection clipboard -t image/png -i "{image_path}"')

        else:
            Messagebox.show_error(
                f"La copie du code QR dans le presse-papier n'est pas "
                f"prise en charge sur ce système : {platform.system()}.",
                "OS non pris en charge",
                parent=root,
            )

    # ------ Fonction servant à extraire les codes "langue" et "pays" depuis le nom du menu ------#

    # Variables pour recevoir la langue et le pays choisis.
    langue = tk.StringVar()
    langue.set(global_lang)
    pays = tk.StringVar()
    pays.set(global_pays)

    # Fonction qui extrait du nom du menu le code du pays et le code de la langue
    def extract_lang_pays(name):
        langue.set(name[len(name) - 6] + name[len(name) - 5])
        global global_lang
        global_lang = langue.get()

        pays.set(name[len(name) - 3] + name[len(name) - 2] + name[len(name) - 1])
        global global_pays
        global_pays = pays.get()

        global global_type
        global_type = 0

        global global_errCorr
        qr_actu(None, global_errCorr, 1)

    # Fonction qui place -bm- devant le son de la liste Borel Maisonny
    def borel_Maisonny():
        print("borel_Maisonny")

        langue.set("bm")
        global global_lang
        global_lang = "bm"

        pays.set("FR")
        global global_pays
        global_pays = "FR"

        global global_type
        global_type = 1

        global global_errCorr
        qr_actu(None, global_errCorr, 1)

    # Fonction qui place *fr* devant les lettres et mots de l'abécedaire de Albane Consigny
    def abeced_Consigny_fr():
        print("Abécédaire Consigny FR")

        langue.set("ac")
        global global_lang
        global_lang = "ac"

        pays.set("FR")
        global global_pays
        global_pays = "FR"

        global global_type
        global_type = 2

        global global_errCorr
        qr_actu(None, global_errCorr, 1)

    # Fonction qui place *es* devant les lettres et mots de l'abécedaire de Albane Consigny
    def abeced_Consigny_es():
        print("Abécédaire Consigny ES")

        langue.set("ac")
        global global_lang
        global_lang = "ac"

        pays.set("ES")
        global global_pays
        global_pays = "ES"

        global global_type
        global_type = 3

        global global_errCorr
        qr_actu(None, global_errCorr, 1)

    # ================================================================ #
    #   Fonctions liées au menu "Vérification" (traitement PDF)        #
    # ================================================================ #

    def _launch_pdf_processing(input_pdf, output_pdf):
        """
        Lance le traitement PDF dans un thread séparé et affiche une
        fenêtre de progression avec le log du processeur.
        """
        prog = ttkb.Toplevel(root)
        prog.title("Vérification PDF - Traitement en cours")
        prog.attributes('-topmost', 1)
        prog.geometry("780x500")
        prog.resizable(True, True)
        prog.transient(root)
        prog.grab_set()

        header = ttkb.Label(
            prog,
            text=f"Traitement de : {Path(input_pdf).name}",
            font=("Arial", 11, "bold"),
        )
        header.pack(pady=(10, 5))

        log_frame = ttkb.Frame(prog)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        log_text = ttkb.Text(
            log_frame,
            font=("Courier", 9),
            wrap="word",
            height=20,
        )
        log_text.pack(side="left", fill="both", expand=True)

        scroll = ttkb.Scrollbar(log_frame, command=log_text.yview)
        scroll.pack(side="right", fill="y")
        log_text.config(yscrollcommand=scroll.set)

        status = ttkb.Label(
            prog,
            text="Traitement en cours...",
            font=("Arial", 10, "italic"),
            bootstyle="info",
        )
        status.pack(pady=(0, 5))

        close_btn = ttkb.Button(
            prog, text="Fermer", bootstyle="secondary",
            state="disabled", width=12,
        )
        close_btn.pack(pady=(0, 10))

        done_flag = {"done": False, "success": False, "error": None}
        old_stdout = sys.stdout
        msg_queue = queue.Queue()

        class _QWriter:
            def write(self, s):
                if s:
                    msg_queue.put(s)
            def flush(self):
                pass

        def worker():
            try:
                processor = QrPdfProcessor(
                    dpi=250,
                    fallback_dpi=400,
                    verbose=True,
                )
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
                    status.config(
                        text=f"Terminé - PDF écrit : {output_pdf}",
                        bootstyle="success",
                    )
                    Messagebox.show_info(
                        f"Le PDF annoté a été généré :\n\n{output_pdf}",
                        "Traitement terminé",
                        parent=prog,
                    )
                else:
                    status.config(
                        text=f"Erreur : {done_flag['error']}",
                        bootstyle="danger",
                    )
                    Messagebox.show_error(
                        f"Une erreur est survenue :\n\n{done_flag['error']}",
                        "Erreur de traitement",
                        parent=prog,
                    )

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
                    "Veuillez attendre la fin du traitement avant de fermer "
                    "cette fenêtre.",
                    "Traitement en cours",
                    parent=prog,
                )

        prog.protocol("WM_DELETE_WINDOW", on_close)

        sys.stdout = _QWriter()
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        prog.after(100, poll)

    def verif_pdf():
        """
        Callback du menu Outils → Vérification.
        """
        if not PDF_VERIF_AVAILABLE:
            Messagebox.show_error(
                "Impossible d'importer MAEL_Verif_PDF.\n\n"
                f"Erreur : {PDF_VERIF_ERROR}\n\n"
                "Vérifiez que toutes les dépendances sont installées "
                "(cv2, numpy, zxingcpp, fpdf2, pypdf, pypdfium2).",
                "Dépendances manquantes",
                parent=root,
            )
            return

        root.attributes('-topmost', 0)
        input_pdf = filedialog.askopenfilename(
            parent=root,
            title="Sélectionner le PDF à vérifier",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
        )
        root.attributes('-topmost', 1)

        if not input_pdf:
            return

        input_path = Path(input_pdf)
        suggested_output = input_path.with_name(f"{input_path.stem}_annotated.pdf")

        root.attributes('-topmost', 0)
        output_pdf = filedialog.asksaveasfilename(
            parent=root,
            title="Enregistrer le PDF annoté",
            initialfile=suggested_output.name,
            initialdir=str(input_path.parent),
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        root.attributes('-topmost', 1)

        if not output_pdf:
            return

        if Path(input_pdf).resolve() == Path(output_pdf).resolve():
            Messagebox.show_error(
                "Le fichier de sortie ne peut pas être identique au fichier "
                "d'entrée. Choisissez un autre nom.",
                "Chemins identiques",
                parent=root,
            )
            return

        _launch_pdf_processing(input_pdf, output_pdf)

    ###### WIDGETS ######

    # ---------   Création de l'interface   ---------#

    # Cadre des champs et boutons
    frame_input = ttkb.Frame(root)
    # Cadre réservé au code QR
    # --> tk.Frame conservé : nécessite un changement dynamique de fond
    #     selon le mode, ce que les widgets ttk ne permettent pas
    #     simplement. Le contraste visuel reste minime.
    frame_qr = tk.Frame(root, background=color_mode[global_mode], bd=4, relief="sunken")

    # Méthode grid() qui dépend de la disposition choisie
    def disp_horiz():
        root.geometry(geom_horiz)
        frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
        frame_qr.grid(row=0, column=1, padx=2, pady=2)
        root.rowconfigure(0, weight=1, minsize=155)
        root.columnconfigure(1, weight=1, minsize=155)

    def disp_vertic():
        root.geometry(geom_verti)
        frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
        frame_qr.grid(row=1, column=0, padx=2, pady=2)
        root.rowconfigure(1, weight=1, minsize=155)
        root.columnconfigure(0, weight=1, minsize=155)

    if disp == "h":
        disp_horiz()
    if disp == "v":
        disp_vertic()

    # Création des frame secondaires
    frame_text = ttkb.Frame(frame_input)
    frame_settings = ttkb.Frame(frame_input)

    frame_text.pack(expand=True, fill="both", ipadx=5, ipady=0, pady=0)
    frame_settings.pack(expand=True, fill="both", ipadx=5, ipady=0)

    # frame_lang : largeur fixe (voir LARGEUR_FRAME_LANG en haut du fichier)
    frame_lang = ttkb.Frame(frame_text, width=LARGEUR_FRAME_LANG)
    frame_data = ttkb.Frame(frame_text)

    # Empêche frame_lang d'ajuster sa largeur à son contenu : il garde la largeur fixée.
    frame_lang.pack_propagate(False)

    frame_lang.pack(expand=False, fill="y", ipadx=0, ipady=0, pady=0, side=tk.LEFT)
    frame_data.pack(expand=True, fill="both", ipadx=0, ipady=0, pady=0, side=tk.LEFT)

    # Création de la barre des menu
    menuBar = ttkb.Menu(root)

    # ---------   Création fenêtre "toplevel" - Aide   ---------#

    def toplevel_aide():
        toplevel = ttkb.Toplevel(root)
        toplevel.title(f"Aide pour MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)
        toplevel.resizable(width=False, height=False)

        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('assets/icon.png')))

        frame_Image = ttkb.Frame(toplevel, padding=20)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        restrictions_label = ttkb.Label(
            frame_Image,
            text="Restrictions :"
                 + "\n- MAEL ne peut pas encore prononcer seuls, les mots formés du son d'une seule voyelle."
                 + "\nExemples : 'haut', 'ou', 'eau', 'un', 'on', 'haie', 'es', 'est'..."
                 + "\nCes mots doivent être accompagnés d'un contexte ou d'un déterminant."
                 + "\nPour prononcer des voyelles seules, utilisez les 'Sons Borel-Maisonny'"
                 + "\nMenu : Langues > Spécial > Sons Borel-Maisonny",
            font=("Arial", 10),
            justify="left",
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
                font=("Arial", 11),
                bootstyle="warning",
            )
            install_xclip.pack(side="bottom", fill="both", pady=5)

    # ---------   Création fenêtre "toplevel" - Informations   ---------#

    def toplevel_info():
        toplevel = ttkb.Toplevel(root)
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
            frame_Licence,
            text="Logiciel sous licence GNU GPL v3",
            font=("Arial", 11),
            anchor="center",
        )
        licence_label.pack(side="bottom", fill="both", pady=0)

    # ---------   Création fenêtre "toplevel" - Borel-Maisonny   ---------#

    def toplevel_BM():
        toplevel = ttkb.Toplevel(root)
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

    def toplevel_AC():
        toplevel = ttkb.Toplevel(root)
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

    # ---------   Menu / sous-menus des langues   ---------#

    # Création du menu "Langues"
    menuLangue = ttkb.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Langues", menu=menuLangue)

    # Création du menu "A" --> Va avoir des sous-menus
    menu_A = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="A", menu=menu_A)

    list_A = ["Afrikaans af-ZAF", "Allemand de-DEU", "Anglais en-AUS",
              "Anglais en-IND", "Anglais en-GBR", "Anglais en-USA",
              "Arabe ar-SAU"]

    for name in list_A:
        command = lambda n=name: extract_lang_pays(n)
        menu_A.add_command(label=name, command=command)

    # Création du menu "B-D" --> Va avoir des sous-menus
    menu_B_D = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="B-D", menu=menu_B_D)

    list_B_D = ["Basque eu-ESP", "Bengali bn-IND", "Bulgare bg-BGR", "Catalan ca-ESP",
                "Chinois zh-CHN", "Coréen ko-KOR", "Danois da-DNK"]

    for name in list_B_D:
        command = lambda n=name: extract_lang_pays(n)
        menu_B_D.add_command(label=name, command=command)

    # Création du menu "E-G" --> Va avoir des sous-menus
    menu_E_G = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="E-G", menu=menu_E_G)

    list_E_G = ["Espagnol es-ESP", "Espagnol es-USA", "Finnois fi-FIN", "Français fr-CAN",
                "Français fr-FRA", "Galicien gl-ESP", "Grec el-GRC", "Gujarati gu-IND"]

    for name in list_E_G:
        command = lambda n=name: extract_lang_pays(n)
        menu_E_G.add_command(label=name, command=command)

    # Création du menu "H-K" --> Va avoir des sous-menus
    menu_H_K = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="H-K", menu=menu_H_K)

    list_H_K = ["Hébreu he-ISR", "Hindi hi-IND", "Hongrois hu-HUN", "Indonésien id-IDN",
                "Islandais is-ISL", "Italien it-ITA", "Japonais ja-JPN"]

    for name in list_H_K:
        command = lambda n=name: extract_lang_pays(n)
        menu_H_K.add_command(label=name, command=command)

    # Création du menu "L-M" --> Va avoir des sous-menus
    menu_L_M = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="L-M", menu=menu_L_M)

    list_L_M = ["Kannada kn-IND", "Letton lv-LVA", "Lituanien lt-LTU", "Malais ms-MYS",
                "Malayalam ml-IND", "Marathi mr-IND"]

    for name in list_L_M:
        command = lambda n=name: extract_lang_pays(n)
        menu_L_M.add_command(label=name, command=command)

    # Création du menu "N-P" --> Va avoir des sous-menus
    menu_N_P = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="N-P", menu=menu_N_P)

    list_N_P = ["Néerlandais nl-BEL", "Néerlandais nl-NLD", "Norvégien nb-NOR", "Panjabi pa-IND",
                "Philippin tl-PHL", "Polonais pl-POL", "Portugais pt-BRA", "Portugais pt-PRT"]

    for name in list_N_P:
        command = lambda n=name: extract_lang_pays(n)
        menu_N_P.add_command(label=name, command=command)

    # Création du menu "Q-S" --> Va avoir des sous-menus
    menu_Q_S = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="Q-S", menu=menu_Q_S)

    list_Q_S = ["Roumain ro-ROU", "Russe ru-RUS", "Serbe sr-SRB", "Slovaque sk-SVK", "Suédois sv-SWE"]

    for name in list_Q_S:
        command = lambda n=name: extract_lang_pays(n)
        menu_Q_S.add_command(label=name, command=command)

    # Création du menu "T-Z" --> Va avoir des sous-menus
    menu_T_Z = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="T-Z", menu=menu_T_Z)

    list_T_Z = ["Tamoul ta-IND", "Tchèque cs-CZE", "Télougou te-IND", "Thaï th-THA",
                "Turc tr-TUR", "Ukrainien uk-UKR", "Vietnamien vi-VNM"]

    for name in list_T_Z:
        command = lambda n=name: extract_lang_pays(n)
        menu_T_Z.add_command(label=name, command=command)

    # Création du menu "Spécial" --> Va avoir des sous-menus
    menu_Special = ttkb.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="Spécial", menu=menu_Special)
    menu_Special.add_command(label="Sons Borel-Maisonny", command=borel_Maisonny)
    menu_Special.add_command(label="Abécédaire Consigny FR", command=abeced_Consigny_fr)
    menu_Special.add_command(label="Abécédaire Consigny ES", command=abeced_Consigny_es)

    # ---------   Menu "Paramètres"   ---------#

    menuParam = ttkb.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Paramètres", menu=menuParam)

    # ---------   Sous-menu "Robustesse"   ---------#

    menuRobust = ttkb.Menu(menuParam, tearoff=0)
    menuParam.add_cascade(label="Robustesse", menu=menuRobust)

    txt_07 = "  7% : moins robuste - mois grand"
    txt_15 = " 15%"
    txt_25 = " 25%"
    txt_30 = " 30% : plus robuste - plus grand"

    if global_errCorr == 1:
        txt_07 = f"*{txt_07}"
    elif global_errCorr == 0:
        txt_15 = f"*{txt_15}"
    elif global_errCorr == 2:
        txt_30 = f"*{txt_30}"
    else:
        txt_25 = f"*{txt_25}"

    menuRobust.add_command(label=txt_07, command=Robust_Bas)
    menuRobust.add_command(label=txt_15, command=Robust_Moy)
    menuRobust.add_command(label=txt_25, command=Robust_Qua)
    menuRobust.add_command(label=txt_30, command=Robust_Haut)

    # ---------   Sous-menu "Vertical / Horizontal"   ---------#

    dp = disp

    if disp == "h":
        text_menu = "Disposition vertical"
    else:
        text_menu = "Disposition horizontal"

    def relaunch_new_disp_param(d=dp, txt=text_menu):
        nonlocal id_boucle
        nonlocal id_debounce
        global global_text_saisi
        global global_size

        menuParam.entryconfigure(1, label=txt)

        # --- Sauvegarde de l'état AVANT destruction de la fenêtre ---
        global_text_saisi = text_saisi.get("1.0", tk.END).strip()
        global_size = entry_size.get()

        if d == "h":
            d = "v"
        else:
            d = "h"

        # Annuler d'abord la boucle périodique, puis remettre id_boucle à None
        if id_boucle is not None:
            root.after_cancel(id_boucle)
            id_boucle = None
        # Annuler aussi le debounce éventuellement en cours
        if id_debounce is not None:
            root.after_cancel(id_debounce)
            id_debounce = None

        root.destroy()

        # =================================================================
        #   CORRECTION : réinitialiser le singleton Style de ttkbootstrap
        # =================================================================
        # Style est un singleton qui conserve une référence vers la fenêtre
        # sur laquelle il a été créé. Après root.destroy(), cette référence
        # devient orpheline, et la nouvelle ttkb.Window() ne peut plus
        # appliquer le thème (les widgets retombent sur le gris par défaut
        # de ttk).
        #
        # En remettant Style.instance à None, on force ttkbootstrap à
        # recréer un Style propre, rattaché à la nouvelle fenêtre.
        ttkb.Style.instance = None

        application(d)

    menuParam.add_command(label=text_menu, command=relaunch_new_disp_param)

    # ---------   Sous-menu "Thème"   ---------#

    # Bascule entre thème clair ("litera") et thème sombre ("darkly").
    # Le libellé de l'entrée indique l'action à venir :
    #   - en thème clair   → "Thème sombre"
    #   - en thème sombre  → "Thème clair"
    #
    # Le changement de thème est appliqué à chaud via Style.theme_use().
    # Les styles personnalisés des boutons de mode, les couleurs du widget
    # de saisie et les icônes sensibles au thème sont réinstallés/mis à jour.

    def toggle_theme():
        global global_theme
        nonlocal TEXT_SAISI_BG, TEXT_SAISI_FG, photo_copy

        # Inverser le thème courant
        if global_theme == "litera":
            global_theme = "darkly"
        else:
            global_theme = "litera"

        # Appliquer le nouveau thème à la fenêtre
        root.style.theme_use(global_theme)

        # Réinstaller les styles personnalisés des boutons de mode :
        # leur fond doit suivre le nouveau thème (clair ou sombre).
        _install_custom_button_styles(root.style)

        # Recalculer et appliquer les couleurs du widget de saisie selon
        # le nouveau thème.
        TEXT_SAISI_BG, TEXT_SAISI_FG = _get_text_saisi_colors(root.style)
        text_saisi.configure(bg=TEXT_SAISI_BG, fg=TEXT_SAISI_FG)

        # Restaurer la bordure colorée du cadre QR (tk.Frame, fond posé
        # manuellement : theme_use() peut le réinitialiser).
        frame_qr.config(background=color_mode[global_mode])

        # Mettre à jour le libellé de l'entrée de menu
        # (index 2 : Robustesse = 0, Disposition = 1, Thème = 2)
        if global_theme == "litera":
            menuParam.entryconfigure(2, label="Thème sombre")
        else:
            menuParam.entryconfigure(2, label="Thème clair")

        # =================================================================
        #   Rechargement des icônes sensibles au thème
        # =================================================================
        # Icône du bouton "Copier" (utilisée une seule fois, à la création) :
        # il faut donc explicitement la remplacer.
        photo_copy = tk.PhotoImage(file=icon_path("Copy-20px-QR.png"))
        button_copy.config(image=photo_copy)

        # Icône mémoire : son contenu dépend de l'état du presse-papier.
        # On relance un scan complet pour recharger la bonne icône (png, str
        # ou vid) dans la variante correspondant au nouveau thème.
        scan_clipboard()

    # Libellé initial selon le thème de démarrage
    theme_label = "Thème sombre" if global_theme == "litera" else "Thème clair"
    menuParam.add_command(label=theme_label, command=toggle_theme)

    # ---------   Menu "Outils"   ---------#

    menuOutils = ttkb.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Outils", menu=menuOutils)

    menuOutils.add_command(label="Vérification", command=verif_pdf)

    # ---------   Menu "Information"   ---------#

    menuInfos = ttkb.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Infos", menu=menuInfos)
    menuInfos.add_command(label='Aide', command=toplevel_aide)
    menuInfos.add_command(label='Sons Borel-Maisonny', command=toplevel_BM)
    menuInfos.add_command(label='Abécédaire Consigny', command=toplevel_AC)
    menuInfos.add_command(label='À propos de "MAEL Gen"', command=toplevel_info)

    root.config(menu=menuBar)

    # ---------   Labels de langue et de pays   --------- #
    # Note : plus de label vide ici. Sous ttkbootstrap, les marges internes
    # des widgets ttk placent naturellement label_lang au bon niveau, sans
    # avoir besoin du petit label-espaceur qui existait en Tkinter pur.

    label_lang = ttkb.Label(
        frame_lang,
        textvariable=langue,
        font=("Arial", 10, "italic"),
    )
    label_lang.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

    label_pay = ttkb.Label(
        frame_lang,
        textvariable=pays,
        font=("Arial", 8, "italic"),
    )
    label_pay.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

    # ---------   Création d'un Label() pour afficher mode dictée / lecture / épeler   --------- #

    label_mode = ttkb.Label(
        frame_lang,
        text="",
        font=("Arial", 10, "italic"),
    )
    label_mode.pack(ipadx=0, ipady=2, pady=2, side=tk.TOP)

    # ---------   Initialisation du label_mode selon le mode de démarrage    ---------#

    if global_mode == "lire":
        label_mode.config(text="Lect", foreground=color_mode["lire"])
    if global_mode == "dicter":
        label_mode.config(text="Dict", foreground=color_mode["dicter"])
    if global_mode == "epeler":
        label_mode.config(text="Épel", foreground=color_mode["epeler"])

    # ---------   Bouton pour copier le code QR    ---------#

    def copy_QR():
        if not qr_deja_genere:
            return
        copie_png(tempPath("QR_Tempor.png"))

    # Icône du bouton selon le thème courant (variante "-W" en mode sombre).
    photo_copy = tk.PhotoImage(file=icon_path("Copy-20px-QR.png"))

    button_copy = ttkb.Button(
        frame_lang,
        image=photo_copy,
        command=copy_QR,
        state="disabled",
        bootstyle="secondary-outline",
    )
    button_copy.pack(ipadx=0, ipady=0, pady=1, side=tk.TOP)

    # ---------   Widget Text() pour recevoir le texte à mettre dans le code QR    ---------#

    text_saisi = ttkb.Text(frame_data, width=30, height=5)
    text_saisi.pack(side=tk.LEFT)

    # Appliquer les couleurs adaptées au thème dès la création
    text_saisi.configure(bg=TEXT_SAISI_BG, fg=TEXT_SAISI_FG)

    def delete_png(event):
        string = "0x89 0x50"
        index = text_saisi.search(string, "1.0", "end")
        if index:
            text_saisi.delete(index, "end")

    def paste_text(event):
        text_saisi.delete("1.0", tk.END)
        text_saisi.event_generate('<<Paste>>')

        global global_errCorr
        qr_actu(event, global_errCorr, 1)

    text_saisi.bind("<Control-v>", delete_png)

    def on_key_release(event):
        nonlocal id_debounce
        if id_debounce is not None:
            root.after_cancel(id_debounce)
        id_debounce = root.after(300, lambda: qr_actu(None, global_errCorr, 1))

    text_saisi.bind("<KeyRelease>", on_key_release)
    text_saisi.bind("<Button-3>", paste_text)

    # ============================================================ #
    #   Zone "Paramètres" : [icone] [Taille] [Mode] [mémoire]      #
    # ============================================================ #

    # ---------   Logo de l'application, tout à gauche   ---------#

    icon_logo = ImageTk.PhotoImage(Image.open(resourcePath("assets/icon-20px.png")))
    label_logo = ttkb.Label(frame_settings, image=icon_logo)
    label_logo.grid(row=0, column=0, padx=(ecart, 20), sticky="w")

    # ---------   Sous-frame "Taille" (label au-dessus, entrée en dessous)   ---------#

    frame_size = ttkb.Frame(frame_settings)
    frame_size.grid(row=0, column=1, padx=ecart, sticky="nsew")

    label_size = ttkb.Label(
        frame_size,
        text="Taille :",
        font=("Arial", 11),
    )
    label_size.grid(row=0, column=0)

    entry_size = ttkb.Entry(frame_size, width=5, justify="center")
    entry_size.insert(0, global_size)
    entry_size.grid(row=1, column=0, pady=2)

    entry_size.bind("<Return>", lambda event: qr_actu(event, global_errCorr, 1))
    entry_size.bind("<KP_Enter>", lambda event: qr_actu(event, global_errCorr, 1))
    entry_size.bind("<Control-v>",
                    lambda event: root.after_idle(
                        lambda: qr_actu(None, global_errCorr, 1)
                    ))

    # ---------   Sous-frame "Mode" (label au-dessus, boutons en dessous)   ---------#

    frame_mode = ttkb.Frame(frame_settings)
    frame_mode.grid(row=0, column=2, padx=ecart, sticky="nsew")

    label_mode_titre = ttkb.Label(
        frame_mode,
        text="Mode :",
        font=("Arial", 11),
    )
    label_mode_titre.grid(row=0, column=0, columnspan=4, pady=(0, 2))

    # ---------   Boutons de mode : L / E / C / D   ---------#
    # Chaque bouton utilise un style personnalisé défini au démarrage
    # par _install_custom_button_styles() :
    #   L (bleu)   : style "Lecture.TButton"
    #   E (vert)   : style "Epeler.TButton"
    #   C (violet) : style "Reserve.TButton" (désactivé)
    #   D (rouge)  : style "Dicter.TButton"
    #
    # L'effet de survol est géré par style.map() côté ttkbootstrap,
    # ce qui remplace l'ancien bind_hover() manuel.

    def mode_lire():
        global global_mode
        global_mode = "lire"
        label_mode.config(text="Lect", foreground=color_mode["lire"])
        qr_actu(None, global_errCorr, 1)

    def mode_epeler():
        global global_mode
        global_mode = "epeler"
        label_mode.config(text="Épel", foreground=color_mode["epeler"])
        qr_actu(None, global_errCorr, 1)

    def mode_dicter():
        global global_mode
        global_mode = "dicter"
        label_mode.config(text="Dict", foreground=color_mode["dicter"])
        qr_actu(None, global_errCorr, 1)

    btn_common = {
        "width": 2,
        "padding": (1, 0),
    }

    button_L = ttkb.Button(
        frame_mode, text="L",
        style="Lecture.TButton",
        command=mode_lire,
        **btn_common,
    )
    button_L.grid(row=1, column=0, padx=1)

    button_E = ttkb.Button(
        frame_mode, text="E",
        style="Epeler.TButton",
        command=mode_epeler,
        **btn_common,
    )
    button_E.grid(row=1, column=1, padx=1)

    button_C = ttkb.Button(
        frame_mode, text="C",
        style="Reserve.TButton",
        state="disabled",
        **btn_common,
    )
    button_C.grid(row=1, column=2, padx=1)

    button_D = ttkb.Button(
        frame_mode, text="D",
        style="Dicter.TButton",
        command=mode_dicter,
        **btn_common,
    )
    button_D.grid(row=1, column=3, padx=1)

    # ---------   Mémoire de travail, tout à droite   ---------#

    # Icône initiale selon le thème courant (variante "-W" en mode sombre).
    icon_mem_str = ImageTk.PhotoImage(Image.open(icon_path("PP-vid-20px.png")))
    label_mem = ttkb.Label(frame_settings, image=icon_mem_str)
    label_mem.grid(row=0, column=3, padx=7, sticky="e")

    # ---------   Répartition équilibrée des colonnes de frame_settings   ---------#

    frame_settings.columnconfigure(0, weight=0)
    frame_settings.columnconfigure(1, weight=1)
    frame_settings.columnconfigure(2, weight=1)
    frame_settings.columnconfigure(3, weight=0)
    frame_settings.rowconfigure(0, weight=1)

    def actu_icon_mem(mem):
        # Icône sélectionnée selon le thème courant (variante "-W" en mode sombre).
        icon_mem_png = ImageTk.PhotoImage(Image.open(icon_path(f"PP-{mem}-20px.png")))
        label_mem.configure(image=icon_mem_png)
        label_mem.image = icon_mem_png

    def scan_clipboard():
        try:
            contenu = root.clipboard_get()

            if "0x89 0x50" in contenu:
                actu_icon_mem("png")
            else:
                actu_icon_mem("str")

        except tk.TclError:
            actu_icon_mem("vid")

            if platform.system() in ('Windows', 'Darwin'):
                actu_icon_mem("png")

    def periodic_scan_clipboard():
        nonlocal id_boucle
        scan_clipboard()
        id_boucle = root.after(500, periodic_scan_clipboard)

    periodic_scan_clipboard()

    # ---------   Label() recevant les images de codes QR   ---------#

    img_code = ImageTk.PhotoImage(Image.open(resourcePath("assets/Bienvenue.png")))
    label_qr = ttkb.Label(frame_qr, image=img_code)
    label_qr.pack()

    # ---------   Restauration de l'état si changement de disposition ---------#
    if global_text_saisi:
        text_saisi.insert("1.0", global_text_saisi)
        qr_actu(None, global_errCorr, 1)

    # ---------   Fermer l'application avec "ctrl+q"   ---------#

    def quit_application(event):
        nonlocal id_boucle
        nonlocal id_debounce
        if id_boucle is not None:
            root.after_cancel(id_boucle)
            id_boucle = None
        if id_debounce is not None:
            root.after_cancel(id_debounce)
            id_debounce = None
        root.destroy()

    root.bind_all("<Control-q>", quit_application)

    ###### BOUCLE PRINCIPALE DE TKinter ######

    root.mainloop()


disp = "h"               # Commencer en mode horizontal
application(disp)        # Lancer la fonction principale
