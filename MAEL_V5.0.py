"""
#############################################################################
# 
#   Application multi-plateforme - "MAEL Gen" - GPL v3
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
       @@@@@@@@@@@@@@                                 @@@@@@@@@@@@@@ 

>>>>> Améliorations prévues <<<<<
- Ajouter un menu : "Mode épeler mot par mot" ?
- Actualiser la doc
- Étudier le cas : "Mode dictée" + link Google Drive
- Ajouter le mode épeler pour EN ES PT
- Corriger le bug de l'accent séparé de la lettre sous LINUX ?
- Étudier les messages Warning
- Faire charger les modules spécifiques à chaque OS une seule fois au début du programme en fonction de l'OS détecté.
- Permettre le glisser - déposer du code QR vers l'éditeur externe
- Réparer l'affichage de l'icône "Presse papier vide"
- Ajouter des icônes aux "toplevel"  --> À vérifier !

#############################################################################
#                   Informations pour le développement
#############################################################################

>>>>> Environnement de développement <<<<<

Ubuntu 24.04.3
Python 3.12.3

Voir quelle version de python est installée :
    python3 --version
    which python3.xx
Installer le dernier ?    

Installer pip :
    sudo apt update
    sudo apt install python3-pip
    pip3 --version

>>>>> Environnement virtuel <<<<<
    sudo apt install python3.xx-venv
    
Aller dans le dossier du projet :
    python3.xx -m venv env

Activer l'environnement :
    source env/bin/activate

---> Installer tous les modules :
Contenu du fichier "requirements.txt" dans le dossier du projet
    tk
    qrcode[pil]
    opencv-python
    clipboard

Pour tout installer d'un coup :
    pip install -r requirements.txt
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

###### IMPORTATION DES MODULES ######

import tkinter as tk
import qrcode
from PIL import Image, ImageTk

import os        # Pour utiliser "xclip" et copier le png dans le presse-papier sous Linux.
import sys       # Pour chemin relatif

import platform  # Pour détecter l'OS et choisir le module correspondant

############## PARAMÈTRES SELON LA VERSION et l'OS #####################
# ---------------------------
# >>>> Nom de la version <<<<
# ---------------------------
qrgen_version = "- V5.0 pour Linux"

# ----------------------------
#     >>>> Couleurs <<<<
# ----------------------------
coul_interface = "#FFFFFF"       # Pour ressembler à MAEL Android
# Variable des couleurs des modes
color_mode = {"dicter":"red", "epeler":"green", "lire":"blue"}

# -------------------------------
# >>>> Dimensions selon l'OS <<<<
# -------------------------------
geom_horiz = "465x173"        # Pour Linux et OSX
# geom_horiz = "470x190"        # Pour Windows

geom_verti = "270x300"        # Pour Linux et OSX
# geom_verti = "300x350"        # Pour Windows

# Écartement entre le widgets de la taille (en px)
ecart_h = 4    # Disposition vertical sous Linux
ecart_v = 1    # Disposition horizontal sous Linux
# ecart_h = 3    # Disposition vertical sous OSX
# ecart_v = 1    # Disposition horizontal sous OSX
# ecart_h = 4    # Disposition vertical sous Windows
# ecart_v = 5    # Disposition horizontal sous Windows


#################################################################

global_lang = "fr"          # Conserver la langue en cas de changement de disposition
global_pays = "FRA"
global_errCorr = 3          # qrcode.constants.ERROR_CORRECT_Q

# Comment traiter l'information écrite dans le champ de texte :
global_type = 0             # 0 = langue  /  1 = Borel Maisonny  /  2 = Abécedaire Consigny FR  /  3 = Abécedaire Consigny FR
global_mode = "lire"     # lecture / dictee / epeler
global_balise = ""          # Balise par défaut

# Fonction pour encrypter

def encrypt(mot_a_encrypt):
    # Clés : liste des caractères qui déplacés +1 ne sont plus compatibles avec les QRcode
    # Valeurs : Valeur à assigner à la place de chr +1
    # --> À compléter en cas de bug
    encrypt_excl_dict = {"0x7e": "0xa0"}  # Tilde +1 = 0x7f <control> --> U+00A1	¡	0xc2 0xa1	INVERTED EXCLAMATION MARK

    # # # # # # # # # # # # # # # # # # # # #
    #     Décalage UTF-8 des caractères     #
    # # # # # # # # # # # # # # # # # # # # #

    # Fonction pour décaler les lettres du mot
    def shift(word, shift_value):  # "mot" = le mot à décaler / "shift_value" = 1 ou -1 point UTF-8


        shifted_word = ""

        # Création d'un nouveau string en décalant chaque lettre de "decal"
        for letter in word:

            # Trouver l'héxadécimal du caractère
            hex_letter = hex(ord(letter))

            if hex_letter in encrypt_excl_dict:  # Si "hex_letter" est dans excl_dict

                print("!!! Caractère non-décalable détecté !!!")

                # Aller chercher la valeur de remplacement prévue dans le dictionnaire
                # excl_dict["0x7e"] --> retourne la valeur de la clé "0x7e" dans excl_dict
                # int(excl_dict["0x7e"], 16) --> convertir en int l'héxadécimal "0x7e" (sous forme de string)
                # chr() --> renvoie le caractère correspondant à l'int
                replace_a = chr(int(encrypt_excl_dict[hex_letter], 16))

                a = replace_a  # Donner la valeur de remplacement
            else:
                a = chr(ord(letter) + shift_value)  # Sinon, l'incrémenter

            shifted_word = shifted_word + a  # Ajouter la lettre au mot

        return shifted_word


    # # # # # # # # # # # # # # # # # # # # #
    #          Mélanger les lettres         #
    # # # # # # # # # # # # # # # # # # # # #


    def shuffler(mot_a_encrypt):
        # Liste recevant les lettres mélangées du mot entré
        local_mixed_word = []

        # Créer une liste des éléments impaires
        i = 1

        # Mettre dans local_mixed_word les éléments impaires
        while i < len(mot_a_encrypt):
            local_mixed_word.append(mot_a_encrypt[i])
            i = i + 2

        # Ajouter à la suite dans local_mixed_word les éléments paires
        i = 0
        while i < len(mot_a_encrypt):
            local_mixed_word.append(mot_a_encrypt[i])
            i = i + 2

        # Inverser le sens des éléments de la liste obtenue
        local_mixed_word.reverse()

        # Convertir la liste en chaîne de caractères
        local_mixed_word_str = "".join(local_mixed_word)

        # Renvoyer cette liste (de lettres mélangées) pour être envoyée dans le code QR
        return local_mixed_word_str

    return shift(shuffler(mot_a_encrypt), 1)




# Mettre toute l'application dans une fonction pour pouvoir la relancer avec le paramètre vertical "v" ou horizontal "h"
# Il doit exister un moyen avec des class, mais je dois étudier pour comprendre ça à fond

def application(disp):
    
    ###### FENETRE PRINCIPALE ######

    root = tk.Tk()

    id_boucle = None  # Déclarer id_boucle comme variable locale

    root['padx'] = 5  # Marge horizontale de 20 pixels
    root['pady'] = 5  # Marge verticale de 10 pixels
    root.title(f"MAEL Gen {qrgen_version}")
    root.attributes('-topmost', 1)  # Maintenir la fenêtre toujours au dessus

    root.config(bg=coul_interface)
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
    def resourcePath(relativePath):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relativePath)
        return os.path.join(os.path.abspath("."), relativePath)

    # Ajout d'une icône de l'application
    root.iconphoto(False, tk.PhotoImage(file=resourcePath('Medias/icon.png')))

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
        # print("Robustesse L : 7%")
        global_errCorr = ec  # Actualiser la variable nonlocal pour que les bind() tiennent compte de la nouvelle valeur
        # Enregistrer cette valeur dans une variable globale pour qu'elle se maintienne lors du changement de disposition
        clicked(menuRobust, 0, "*  7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Moy():
        global global_errCorr
        ec = 0  # qrcode.constants.ERROR_CORRECT_M
        qr_actu(None, ec, 1)
        # print("Robustesse M : 15%")
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "* 15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Qua():
        global global_errCorr
        ec = 3  # qrcode.constants.ERROR_CORRECT_Q
        qr_actu(None, ec, 1)
        # print("Robustesse Q : 25%")
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "* 25%")
        clicked(menuRobust, 3, "  30% : plus robuste - plus grand")

    def Robust_Haut():
        global global_errCorr
        ec = 2  # qrcode.constants.ERROR_CORRECT_H
        qr_actu(None, ec, 1)
        # print("Robustesse H : 30%")
        global_errCorr = ec
        clicked(menuRobust, 0, "   7% : moins robuste - mois grand")
        clicked(menuRobust, 1, "  15%")
        clicked(menuRobust, 2, "  25%")
        clicked(menuRobust, 3, "* 30% : plus robuste - plus grand")

    # --------   Création d'une fonction créant le code QR   --------#
    # "ec" --> variable locale de "error_correction"
    # copy --> 0 = ne copie pas le code QR dans le presse papier / 1 = copie-le
    def qr_actu(event, ec, copy):

        # Réinitilaiser la couleur du fond et la couleur du texte du widget "text_saisi" à chaque rafraichissement
        text_saisi.configure(bg="White", fg='blue')

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
        # (Seulement pour les langues ayant différents pays)
        except_list = ["<enAUS>", "<enIND>", "<enUSA>", "<esESP>", "<frCAN>", "<nlBEL>", "<ptPRT>"]
        # Fonctionnel ?    x           x         x          x          x          x          x
        # Défaut MITapp :           en GBR                es ESP     fr FRA     nl NLD     pt PRT
        # Défaut MAEL   :           en GBR                es USA     fr FRA     nl NLD     pt BRA
        # Le code de MAEL ajuste les pays par défaut.
        
        # Liste des URL à adapter 
            # Cas 0 -->        Google Drive
        url_list = ["https://drive.google.com/file/d/"]
        conv_list = ["/gd/"]          # Balise qui sera remplacée dans MAEl Scan par : https://drive.google.com/uc?id=

        # Création des balises longues
        balise_longue = "<" + langue.get() + pays.get() + ">"

        # --------   Vérification que ce n'est pas un .png qui est collé   --------#

        # Création d'une variable recevant le texte à tester
        # La méthode get() de la classe Text ajoute un retour à la ligne à la fin de la chaîne de caractères récupérée.
        # --> Brouille les codes *xx* qui vont chercher le fichier mp3.
        text_colle = text_saisi.get("1.0", tk.END).strip()  # La méthode strip() supprime les espaces blancs en début et en fin de chaîne. Dans ce cas, elle supprimera le retour à la ligne à la fin de la chaîne.

        # Si le texte commence par la séquence hexdécimale d'un .png, vide le Widget "text_saisi"
        if "0x89 0x50" in text_colle:
            text_colle = ""
            text_saisi.delete("1.0", tk.END)  # Effacer le Widget "text_saisi"
            text_saisi.configure(bg="#ffd4d4", fg="red")  # Alerter en mettant le fond rose
            text_saisi.insert("1.0", "Vous collez autre chose que du texte.")
        
        # Fonction qui modifie les URL pour les rendre compatibles avec MAEL
        def adapt_url():
            nonlocal text_colle        # Aller chercher text_colle
            # ==> Cas Google Drive :
            if url_list[0] in text_colle:            # Si c'est un lien Google Drive
                text_colle = text_colle.replace(url_list[0], conv_list[0])     # Le remplacer par le début d'URL valide
                indice = text_colle.rfind("/view")   # Localiser l'indice où commence "/view"
                text_colle = text_colle[:indice]     # Tronquer l'adresse après cet indice (inclus)

         # Création d'une fonction pour créer la balise courte à partir de la balise longue.
        def compres_balise(bl):
            global global_balise
            
            if global_type == 0:
                if bl in except_list:                    # Les balises non réductibles
                    if url_list[0] in text_colle:        # Si le contenu du champ d'écriture contien une URL contenu dans la liste des URL connues
                        balise = ""
                    else:
                        balise = balise_longue           
                elif bl == "<frFRA>":                    # Français par défault
                    if len(text_colle) < 4:              # Si le texte est < à 4 lettres : MAEL scan va a bugguer, il faut ajouter la balise <fr>
                        balise = "<fr>"
                    else:
                        balise = ""
                elif url_list[0] in text_colle:          # Si le contenu du champ d'écriture contien une URL contenu dans la liste des URL connues
                    balise = ""
                else:
                    balise = "<" + langue.get() + ">"    # Balises avec un seul pays : pas de code pays


            if global_type == 1:                     # C'est un son Borel-Maisonny
                if url_list[0] in text_colle:        # Si le contenu du champ d'écriture contien une URL contenu dans la liste des URL connues
                    balise = ""
                else:
                    balise = "-bm-" 

                
            if global_type == 2:                    # C'est une lettre ou un mot de l'abécédaire Consigny en Français
                if url_list[0] in text_colle:       # Si le contenu du champ d'écriture contien une URL contenu dans la liste des URL connues
                    balise = ""
                else:
                    balise = "*fr*"                
                
            
            if global_type == 3:                    # C'est une lettre ou un mot de l'abécédaire Consigny en Espagnol
                if url_list[0] in text_colle:       # Si le contenu du champ d'écriture contien une URL contenu dans la liste des URL connues
                    balise = ""
                else:
                    balise = "*es*"

            global_balise = balise
            # print (global_balise)

            return balise

        balise_courte = compres_balise(balise_longue)
        
        # --------   Création du texte qui sera mis dans le code QR   --------#

        adapt_url()
        
        # Concaténer la balise courte avec le texte collé dans le Widget "text_saisi"
        text = balise_courte + text_colle

        # Ajouter la balise de fin pour le mode "Dictée" ou "Èpeler"
        if global_mode == "dicter":
            text = text + "#d"
        if global_mode == "epeler":
            text = text + "#e"

        # Encrypter le texte a mettre dans le code QR s
        text = encrypt(text)

        # Donner la variable "text" à l'objet "qr"
        qr.add_data(text)

        # Le paramètre "fit=True" complète "version=None" de l'objet qrcode.QRCode() pour obtenir la version automatiquement (Si j'ai bien compris...)
        qr.make(fit=True)

        # Création d'une image du code QR (couleurs paramétrables)
        img = qr.make_image(fill_color="black", back_color="white")

        # --------   Redimensionnement de l'objet qr   --------#

        # Variable pour recevoir ce qui a été rentré dans "entry_size"
        nonlocal new_size_var

        # Vérifier le contenu de "entry_size" est convertible en nombre
        try:
            int(entry_size.get())  # Essai d'une conversion en integer. Si OK --> continue
        except ValueError:  # Si une erreur est retournée ("ValueError" dans ce cas)
            new_size_var.set(150)  # Réinitialiser la valeur avec un nombre par défaut
            entry_size.delete(0, tk.END)  # Effacer le Widget "entry_size"
            entry_size.insert(0, str(new_size_var.get()))  # Actualiser "entry_size" avec le nombre par défaut

        #  "entry_size.get()" est maintenant obligatoirement un string convertible en nombre : le convertir en integer
        new_size_var.set(int(entry_size.get()))

        # Interdire les valeurs supérieures à 150px
        if new_size_var.get() > 150:
            new_size_var.set(150)
        # Interdire les valeurs supérieures à 1px
        if new_size_var.get() < 1:
            new_size_var.set(1)

        # Réinitialiser "entry_size" avec un int inférieur <= 150 et >1
        entry_size.delete(0, tk.END)
        entry_size.insert(0, str(new_size_var.get()))
        # Synchroniser la valeur dans "entry_size" avec le Widget Scale() "scale_size"
        # scale_size.set(new_size_var.get())  # Nécessaire avec des variables de contrôle ???

        # Redimentionner le code QR carré avant sa conversion en png
        resized_img = img.resize((new_size_var.get(), new_size_var.get()))  # (largeur, hauteur)

        # --------   Création / affichage du fichier PNG   --------#

        # Sauvegarde de l'image dans un fichier png
        resized_img.save(resourcePath("Medias/QR_Tempor.png"))

        fond_qr = Image.open(resourcePath('Medias/QR_Tempor.png'))    # Ouvrir le png du code couleurs
        fond_qr = fond_qr.convert('RGBA')               # Convertir le codeQR en RGBA pour garder le logo en couleurs
        logo_a_sup = Image.open(resourcePath('Medias/Bouche.png'))

        # Redimensionner le logo à superposer
        # Choix des dimensions
        h_sup = round(new_size_var.get() / 6)             # Calcul de la hauteur de Bouche.png
        l_sup = round(new_size_var.get() * 1.5 /6)        # Calcul de la largeur de Bouche.png
        
        logo_a_sup = logo_a_sup.resize((l_sup, h_sup))

        # Placement du logo au centre du code QR
        ## x = round((largeur_fond - largeur_superpose) / 2)
        ## y = round((hauteur_fond - hauteur_superpose) / 2)

        x = round((new_size_var.get() - l_sup) / 2)
        y = round((new_size_var.get() - h_sup) / 2)

        # Ajout du logo sur l'image
        # fond_qr.paste(logo_a_sup, (x, y), Masque_alpha_de_l_m_logo_a_sup)
        fond_qr.paste(logo_a_sup, (x, y), logo_a_sup)

        # Enregistrer le code QR avec la bouche au dessus
        fond_qr.save(resourcePath("Medias/QR_Tempor.png"))

        # Créer du carré indicateur de mode
        mod_indic = Image.new('RGBA', (5, 5), color_mode[global_mode])

        # Superposer le carré indicateur de mode sur l'image existante en bas à droite
        pos = int(fond_qr.size[0]-5)

        fond_qr.paste(mod_indic, (pos, pos), mod_indic)
        fond_qr.save(resourcePath("Medias/QR_Tempor.png"))

        
        # Aller chercher le fichier png pour créer un objet et l'afficher dans le Label()
        img_code = ImageTk.PhotoImage(Image.open(resourcePath("Medias/QR_Tempor.png")))
        label_qr.configure(image=img_code)

        label_qr.image = img_code  # Mettre à jour la référence de l'image pour éviter la suppression par le "ramasse miettes"
        # print(type(label_qr))
        if copy == 1:
            # Lancer la fonction qui enverra l'image dans le presse papier selon l'OS de l'utilisateur
            copie_png(resourcePath("Medias/QR_Tempor.png"))

        # Affichage du texte complet inclus dans le code QR
        # print(text)

    # --------   Fonction copiant l'image dans le presse papier   --------#

    # Une méthode différente est nécessaire selon l'OS de l'utilisateur
    def copie_png(image_path):
        if platform.system() == 'Windows':

            # Importer les modules win32clipboard et io pour Windows
            from io import BytesIO
            import win32clipboard

            # Pour copier le fichier .png dans le presse papier sous Windows
            def send_to_clipboard(clip_type, data):
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(clip_type, data)
                win32clipboard.CloseClipboard()

            filepath = resourcePath("Medias/QR_Tempor.png")
            image = Image.open(filepath)

            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            send_to_clipboard(win32clipboard.CF_DIB, data)

            actu_icon_mem("png")      # Actualiser l'icone du presse papier

        elif platform.system() == 'Darwin':
            try:
                from AppKit import NSPasteboard, NSPasteboardTypePNG, NSImage
                from io import BytesIO
            except ImportError:
                pass

            # Chemin du fichier image
            image_path = resourcePath("Medias/QR_Tempor.png")

            # Ouvrir l'image avec Pillow
            image = Image.open(image_path)

            # Enregistrer l'image dans un objet BytesIO au format PNG
            with BytesIO() as buffer:
                image.save(buffer, format='PNG')
                img_data = buffer.getvalue()

            # Créer un objet NSImage à partir des données de l'image
            ns_image = NSImage.alloc().initWithData_(img_data)

            # Copier l'image dans le presse-papier
            pasteboard = NSPasteboard.generalPasteboard()
            pasteboard.clearContents()
            pasteboard.setData_forType_(ns_image.TIFFRepresentation(), NSPasteboardTypePNG)


        elif platform.system() == 'Linux':
            # Utiliser la méthode xclip pour Linux
            image_path = resourcePath("Medias/QR_Tempor.png")
            # print(image_path)

            # {image_path} entre "" pour que les espaces soient acceptés...
            os.system(f'xclip -selection clipboard -t image/png -i "{image_path}"')

        else:
            print("OS non pris en charge...")

    # ------ Fonction servant à extraire les codes "langue" et "pays" depuis le nom du menu ------#

    # Variables pour recevoir la langue et le pays choisis.
    langue = tk.StringVar()
    langue.set(global_lang)
    pays = tk.StringVar()
    pays.set(global_pays)

    # Fonction qui extrait du nom du menu le code du pays et le code de la langue
    def extract_lang_pays(name):
        langue.set(name[len(name) - 6] + name[len(name) - 5])  # Mise dans la variable de contrôle de la concaténation du 6e et 5e cacatère en partant de la fin
        global global_lang
        global_lang = langue.get()  # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        # (f"global_lang = {global_lang}")

        pays.set(name[len(name) - 3] + name[len(name) - 2] + name[
            len(name) - 1])  # idem avec les 3 derniers caractères pour le code du pays
        global global_pays
        global_pays = pays.get()  # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        # print(f"global_pays = {global_pays}")

        global global_type
        global_type = 0       # Type d'information écrite dans le cadre de texte = Langue

        global global_errCorr
        qr_actu(None, global_errCorr, 1)  # Actualiser le code QR si changement de langue - "None" nécessaire parce que la fonction n'est pas appelée par un événement ?

    # Fonction qui place -bm- devant le son de la liste Borel Maisonny
    def borel_Maisonny():
        print("borel_Maisonny")
        
        langue.set("bm")
        global global_lang
        global_lang = "bm"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        pays.set("FR")
        global global_pays
        global_pays = "FR"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        global global_type
        global_type = 1       # Type d'information écrite dans le cadre de texte = Borel Maisonny
        
        # Actualiser le code QR si changement de langue - "None" nécessaire parce que la fonction n'est pas appelée par un événement ?
        global global_errCorr
        qr_actu(None, global_errCorr, 1)
        

    # Fonction qui place *fr* devant les lettres et mots de l'abécedaire de Albane Consigny
    def abeced_Consigny_fr():
        print("Abécédaire Consigny FR")
        
        langue.set("ac")
        global global_lang
        global_lang = "ac"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        pays.set("FR")
        global global_pays
        global_pays = "FR"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        global global_type
        global_type = 2       # Type d'information écrite dans le cadre de texte = Abécédaire Consigny
        
        # Actualiser le code QR si changement de langue - "None" nécessaire parce que la fonction n'est pas appelée par un événement ?
        global global_errCorr
        qr_actu(None, global_errCorr, 1)
        
    # Fonction qui place *fr* devant les lettres et mots de l'abécedaire de Albane Consigny
    def abeced_Consigny_es():
        print("Abécédaire Consigny ES")
        
        langue.set("ac")
        global global_lang
        global_lang = "ac"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        pays.set("ES")
        global global_pays
        global_pays = "ES"    # Mise dans une variable globale pour être conservée lors d'un changement de disposition
        
        global global_type
        global_type = 3      # Type d'information écrite dans le cadre de texte = Abécédaire Consigny
        
        # Actualiser le code QR si changement de langue - "None" nécessaire parce que la fonction n'est pas appelée par un événement ?
        global global_errCorr
        qr_actu(None, global_errCorr, 1) 


    ###### WIDGETS ######

    # ---------   Création de l'interface   ---------#

    # Création des cadres principaux
    # Cadre des champs et boutons
    frame_input = tk.Frame(root, background=coul_interface, bd=0)
    # Cadre réservé au code QR
    frame_qr = tk.Frame(root, background=color_mode[global_mode], bd=4, relief="sunken")
    
    # Méthode grid() qui dépend de la disposition choisie
    def disp_horiz():
        root.geometry(geom_horiz)   # Valeurs défines au début du programme
        frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
        frame_qr.grid(row=0, column=1, padx=2, pady=2)
        root.rowconfigure(0, weight=1, minsize=155)  # Row 0 avec taille minimale de 155 pixels
        root.columnconfigure(1, weight=1, minsize=155)  # Column 1 avec taille minimale de 155 pixels

    def disp_vertic():
        root.geometry(geom_verti)   # Valeurs défines au début du programme
        frame_input.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
        frame_qr.grid(row=1, column=0, padx=2, pady=2)
        root.rowconfigure(1, weight=1, minsize=155)  # Row 0 avec taille minimale de 155 pixels
        root.columnconfigure(0, weight=1, minsize=155)  # Column 1 avec taille minimale de 155 pixels

    if disp == "h":
        disp_horiz()
    if disp == "v":
        disp_vertic()

    # Création des frame secondaires
    frame_text = tk.Frame(frame_input, background=coul_interface, bd=0, relief="sunken")
    frame_size = tk.Frame(frame_input, background=coul_interface, bd=0, relief="sunken")

    frame_text.pack(expand=True, fill="both", ipadx=5, ipady=0, pady=0)
    frame_size.pack(expand=True, fill="both", ipadx=5, ipady=0)

    frame_lang = tk.Frame(frame_text, background=coul_interface, bd=0, relief="sunken")
    frame_data = tk.Frame(frame_text, background=coul_interface, bd=0, relief="sunken")

    frame_lang.pack(expand=True, fill="both", ipadx=0, ipady=0, pady=0, side=tk.LEFT)
    frame_data.pack(expand=True, fill="both", ipadx=0, ipady=0, pady=0, side=tk.LEFT)

    # Création de la barre des menu
    menuBar = tk.Menu(root)

    # ---------   Création fenêtre "toplevel" - Aide   ---------#

    def toplevel_aide():
        toplevel = tk.Toplevel(root)
        toplevel.title(f"Aide pour MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)  # Maintenir la fenêtre toujours au dessus
        toplevel.resizable(width=False, height=False)
        
        # Ajout d'une icône à la fenêtre
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('Medias/icon.png')))

        frame_Image = tk.Frame(toplevel, bd=20, bg=coul_interface)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
                
        restrictions_label = tk.Label(frame_Image,
                       text="Restrictions :"
                            + "\n- MAEL ne peut pas encore prononcer seuls, les mots formés du son d'une seule voyelle."
                            + "\nExemples : 'haut', 'ou', 'eau', 'un', 'on', 'haie', 'es', 'est'..."
                            + "\nCes mots doivent être accompagnés d'un contexte ou d'un déterminant."
                            + "\nPour prononcer des voyelles seules, utilisez les 'Sons Borel-Maisonny'"
                            + "\nMenu : Langues > Sprécial > Sons Borel-Maisonny",
                       font=("Arial", 10),
                       compound="left",
                       bg = coul_interface,
                       justify=tk.LEFT)
        
        restrictions_label.pack(side="bottom", pady=5)

        # Ajout du document png pour l'aide
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Aide-V4.png")))
        image_aide = tk.Label(frame_Image, image=img_png)
        image_aide.image = img_png
        image_aide.pack(side="bottom", fill="both", expand=tk.YES)

        if platform.system() == 'Linux':
            install_xclip = tk.Label(frame_Image,
                                   text="Sous Linux, installez \"xclip\" avant la première utilisation --> sudo apt-get install xclip",
                                   font=("Arial", 11),
                                   compound="left",
                                   justify=tk.LEFT)
            
            install_xclip.pack(side="bottom", fill="both", pady=5)



    # ---------   Création fenêtre "toplevel" - Informations   ---------#

    def toplevel_info():
        toplevel = tk.Toplevel(root)
        toplevel.title(f"À propos de MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)  # Maintenir la fenêtre toujours au dessus
        toplevel.resizable(width=False, height=False)
        
        # Ajout d'une icône à la fenêtre
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('Medias/icon.png')))

        frame_Image = tk.Frame(toplevel, bd=20, bg=coul_interface)
        frame_Texte = tk.Frame(toplevel, bd=20, bg=coul_interface)
        frame_Licence = tk.Frame(toplevel, bd=3, bg=coul_interface)

        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        frame_Texte.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        frame_Licence.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        # Ajout du texte
        img_text = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Infos-450px.png")))
        interf_MAELScan = tk.Label(frame_Image, image=img_text)
        interf_MAELScan.image = img_text
        interf_MAELScan.pack(side="left", fill="both", expand=tk.YES)

        # Ajout d'un screen shot de MAEL Scan
        img_screenShot = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Interface_MAEL_Scan_450px.png")))
        interf_MAELScan = tk.Label(frame_Image, image=img_screenShot)
        interf_MAELScan.image = img_screenShot
        interf_MAELScan.pack(side="left", fill="both", expand=tk.YES)
        
                # Spécification de la licence libre
        licence_label = tk.Label(frame_Licence,
                                 text="Logiciel sous licence GNU GPL v3",
                                 font=("Arial", 11),
                                 compound="center",
                                 justify=tk.LEFT)
        licence_label.pack(side="bottom", fill="both", pady=0)
        
        
    # ---------   Création fenêtre "toplevel" - Borel-Maisonny   ---------#

    def toplevel_BM():
        toplevel = tk.Toplevel(root)
        toplevel.title(f"Sons Borel-Maisonny - MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)  # Maintenir la fenêtre toujours au dessus
        toplevel.resizable(width=False, height=False)
        
        # Ajout d'une icône à la fenêtre
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('Medias/icon.png')))

        frame_Image = tk.Frame(toplevel, bd=10, bg=coul_interface)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Ajout du document png pour l'aide
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Borel-Maisonny.png")))
        image_BM = tk.Label(frame_Image, image=img_png)
        image_BM.image = img_png
        image_BM.pack(side="bottom", fill="both", expand=tk.YES)
        
    def toplevel_AC():
        toplevel = tk.Toplevel(root)
        toplevel.title(f"Abécédaire Consigny - MAEL Gen {qrgen_version}")
        toplevel.attributes('-topmost', 1)  # Maintenir la fenêtre toujours au dessus
        toplevel.resizable(width=False, height=False)
        
        # Ajout d'une icône à la fenêtre
        toplevel.iconphoto(False, tk.PhotoImage(file=resourcePath('Medias/icon.png')))

        frame_Image = tk.Frame(toplevel, bd=10, bg=coul_interface)
        frame_Image.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Ajout du document png pour l'aide
        img_png = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Abecedaire_Consigny.png")))
        image_BM = tk.Label(frame_Image, image=img_png)
        image_BM.image = img_png
        image_BM.pack(side="bottom", fill="both", expand=tk.YES)
        
    # ---------   Menu / sous-menus des langues   ---------#

    # Création du menu "Langues"
    menuLangue = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Langues", menu=menuLangue)

    # Création du menu "A" --> Va avoir des sous-menus
    menu_A = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="A", menu=menu_A)

    # Liste des langues inclues dans ce menu
    list_A = ["Afrikaans af-ZAF", "Allemand de-DEU", "Anglais en-AUS",
              "Anglais en-IND", "Anglais en-GBR", "Anglais en-USA",
              "Arabe ar-SAU"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_A:
        command = lambda n=name: extract_lang_pays(n)
        menu_A.add_command(label=name, command=command)

    # Création du menu "B-D" --> Va avoir des sous-menus
    menu_B_D = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="B-D", menu=menu_B_D)

    # Liste des langues inclues dans ce menu
    list_B_D = ["Basque eu-ESP", "Bengali bn-IND", "Bulgare bg-BGR", "Catalan ca-ESP",
                "Chinois zh-CHN", "Coréen ko-KOR", "Danois da-DNK"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_B_D:
        command = lambda n=name: extract_lang_pays(n)
        menu_B_D.add_command(label=name, command=command)

    # Création du menu "E-G" --> Va avoir des sous-menus
    menu_E_G = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="E-G", menu=menu_E_G)

    # Liste des langues inclues dans ce menu
    list_E_G = ["Espagnol es-ESP", "Espagnol es-USA", "Finnois fi-FIN", "Français fr-CAN",
                "Français fr-FRA", "Galicien gl-ESP", "Grec el-GRC", "Gujarati gu-IND"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_E_G:
        command = lambda n=name: extract_lang_pays(n)
        menu_E_G.add_command(label=name, command=command)

    # Création du menu "H-K" --> Va avoir des sous-menus
    menu_H_K = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="H-K", menu=menu_H_K)

    # Liste des langues inclues dans ce menu
    list_H_K = ["Hébreu he-ISR", "Hindi hi-IND", "Hongrois hu-HUN", "Indonésien id-IDN",
                "Islandais is-ISL", "Italien it-ITA", "Japonais ja-JPN"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_H_K:
        command = lambda n=name: extract_lang_pays(n)
        menu_H_K.add_command(label=name, command=command)

    # Création du menu "L-M" --> Va avoir des sous-menus
    menu_L_M = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="L-M", menu=menu_L_M)

    # Liste des langues inclues dans ce menu
    list_L_M = ["Kannada kn-IND", "Letton lv-LVA", "Lituanien lt-LTU", "Malais ms-MYS",
                "Malayalam ml-IND", "Marathi mr-IND"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_L_M:
        command = lambda n=name: extract_lang_pays(n)
        menu_L_M.add_command(label=name, command=command)

    # Création du menu "N-P" --> Va avoir des sous-menus
    menu_N_P = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="N-P", menu=menu_N_P)

    # Liste des langues inclues dans ce menu
    list_N_P = ["Néerlandais nl-BEL", "Néerlandais nl-NLD", "Norvégien nb-NOR", "Panjabi pa-IND",
                "Philippin tl-PHL", "Polonais pl-POL", "Portugais pt-BRA", "Portugais pt-PRT"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_N_P:
        command = lambda n=name: extract_lang_pays(n)
        menu_N_P.add_command(label=name, command=command)

    # Création du menu "Q-S" --> Va avoir des sous-menus
    menu_Q_S = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="Q-S", menu=menu_Q_S)

    # Liste des langues inclues dans ce menu
    list_Q_S = ["Roumain ro-ROU", "Russe ru-RUS", "Serbe sr-SRB", "Slovaque sk-SVK", "Suédois sv-SWE"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_Q_S:
        command = lambda n=name: extract_lang_pays(n)
        menu_Q_S.add_command(label=name, command=command)

    # Création du menu "T-Z" --> Va avoir des sous-menus
    menu_T_Z = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="T-Z", menu=menu_T_Z)

    # Liste des langues inclues dans ce menu
    list_T_Z = ["Tamoul ta-IND", "Tchèque cs-CZE", "Télougou te-IND", "Thaï th-THA",
                "Turc tr-TUR", "Ukrainien uk-UKR", "Vietnamien vi-VNM"]

    # Création d'un sous-menu pour chaque langue
    # Utilisation d'une lambda pour pouvoir entrer le titre du menu comme paramètre de la fonction à lancer
    for name in list_T_Z:
        command = lambda n=name: extract_lang_pays(n)
        menu_T_Z.add_command(label=name, command=command)
        
    # Création du menu "Spécial" --> Va avoir des sous-menus
    menu_Special = tk.Menu(menuBar, tearoff=0)
    menuLangue.add_cascade(label="Spécial", menu=menu_Special) 
    # Liste des options proposées dans ce menu
    menu_Special.add_command(label="Sons Borel-Maisonny", command=borel_Maisonny)
    menu_Special.add_command(label="Abécédaire Consigny FR", command=abeced_Consigny_fr)
    menu_Special.add_command(label="Abécédaire Consigny ES", command=abeced_Consigny_es)
    
    # ---------   Menu "Paramètres"   ---------#

    menuParam = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Paramètres", menu=menuParam)

    # ---------   Sous-menu "Robustesse"   ---------#

    # Création du menu "Robustesse" --> Va avoir des sous-menus
    menuRobust = tk.Menu(menuParam, tearoff=0)
    menuParam.add_cascade(label="Robustesse", menu=menuRobust)

    # ---------   Création des sous-sous-menus du taux de correction   ---------#

    # Variables recevant le texte qui sera celui des différents taux de correction
    txt_07 = "  7% : moins robuste - mois grand"
    txt_15 = " 15%"
    txt_25 = " 25%"
    txt_30 = " 30% : plus robuste - plus grand"

    # Ajouter une étoile lors du redémarrage pour garder un visuel du taux de correction en cours
    if global_errCorr == 1:    # 1 = qrcode.constants.ERROR_CORRECT_L
        txt_07 = f"*{txt_07}"
    elif global_errCorr == 0:  # 0 = qrcode.constants.ERROR_CORRECT_M
        txt_15 = f"*{txt_15}"
    elif global_errCorr == 2:  # 2 = qrcode.constants.ERROR_CORRECT_H
        txt_30 = f"*{txt_30}"
    else:
        txt_25 = f"*{txt_25}"  # 3 = qrcode.constants.ERROR_CORRECT_Q

    menuRobust.add_command(label=txt_07, command=Robust_Bas)
    menuRobust.add_command(label=txt_15, command=Robust_Moy)
    menuRobust.add_command(label=txt_25, command=Robust_Qua)  # Niveau de correction par défaut au démarrage
    menuRobust.add_command(label=txt_30, command=Robust_Haut)

    # ---------   Sous-menu "Vertical / Horizontal"   ---------#

    dp = disp

    if disp == "h":
        text_menu = "Disposition vertical"
    else:
        text_menu = "Disposition horizontal"

    # Fonction chargée de détruire la fenêtre principale pour la reconstruire dans la nouvelle disposition.

    def relaunch_new_disp_param(d=dp, txt=text_menu):
        nonlocal id_boucle  # Ajouter cette ligne pour indiquer que vous utilisez la variable globale
        id_boucle = None    # Réinitialiser la variable
        menuParam.entryconfigure(1, label=txt)

        if d == "h":
            d = "v"
        else:
            d = "h"

        if id_boucle is not None:
            root.after_cancel(id_boucle)
        root.destroy()
        application(d)

    
    menuParam.add_command(label=text_menu, command=relaunch_new_disp_param)

    # ---------   Sous-sous-menu "Modes dictée"   ---------#

    # Création du menu "Dicter - texte non visible" --> Va avoir des sous-menus
    
    menuDictee = tk.Menu(menuParam, tearoff=0)
    menuParam.add_cascade(label="Modes dictée", menu=menuDictee)


    # Fonction activée en cliquant sur le sous-sous-menu "Dicter - texte non visible"

    def actu_menu_dicter():
        menuParam.entryconfig(2, label="* Modes dictée")
        menuDictee.entryconfig(0, label="* Dicter (texte non visible)")
        menuDictee.entryconfig(1, label="Épeler (texte non visible)")
        menuParam.entryconfig(3, label="Mode Lecture")
        
        label_mode.config(text="Dict", fg=color_mode["dicter"],)           # Actualiser le label() du mode D/L
    

    def mode_dicter():
        global global_mode
        global_mode = "dicter"
        qr_actu(None, global_errCorr, 1)              # Actualiser le code QR (avec la nouvelle valeur de "global_mode"
        
        # Changer le texte du menu selon le mode en cours
        actu_menu_dicter()

    menuDictee.add_command(label="", command=mode_dicter)

        # ---------   Sous-sous-menu "Épeler"   ---------#

    # Fonction activée en cliquant sur le sous-sous-menu "Épeler - texte non visible"

    def actu_menu_epeler():
        menuParam.entryconfig(2, label="* Modes dictée")
        menuDictee.entryconfig(0, label="Dicter (texte non visible)")
        menuDictee.entryconfig(1, label="* Épeler (texte non visible)")
        menuParam.entryconfig(3, label="Mode Lecture")
        
        label_mode.config(text="Épel", fg=color_mode["epeler"],)           # Actualiser le label() du mode D/L
    

    def mode_epeler():
        global global_mode
        global_mode = "epeler"
        qr_actu(None, global_errCorr, 1)              # Actualiser le code QR (avec la nouvelle valeur de "global_mode"

        # Changer le texte du menu selon le mode en cours
        actu_menu_epeler()

    menuDictee.add_command(label="", command=mode_epeler)


    # ---------   Sous-menu "Lire"   ---------#

    # Fonction activée en cliquant sur le sous-menu "Lire"

    def actu_menu_lire():
        menuParam.entryconfig(2, label="Modes dictée")
        menuDictee.entryconfig(0, label="Dicter (texte non visible)")
        menuDictee.entryconfig(1, label="Épeler (texte non visible)")
        menuParam.entryconfig(3, label="* Mode Lecture")
        
        label_mode.config(text="Lect", fg=color_mode["lire"],)           # Actualiser le label() du mode D/L
    

    def mode_lire():
        global global_mode
        global_mode = "lire"
        qr_actu(None, global_errCorr, 1)              # Actualiser le code QR (avec la nouvelle valeur de "global_mode")

        # Changer le texte du menu selon le mode en cours
        actu_menu_lire()

    menuParam.add_command(label="", command=mode_lire)
        

    # ---------   Menu "Information"   ---------#

    # Création du menu 'Informations'
    menuInfos = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Informations", menu=menuInfos)
    menuInfos.add_command(label='Aide', command=toplevel_aide)
    menuInfos.add_command(label='Sons Borel-Maisonny', command=toplevel_BM)
    menuInfos.add_command(label='Abécédaire Consigny', command=toplevel_AC)
    menuInfos.add_command(label='À propos de "MAEL Gen"', command=toplevel_info)

    # Configuration de la barre des menus
    root.config(menu=menuBar)

    # ---------   Création d'un Label() pour afficher la langue et le pays   --------- #

    # Pour laisser de l'espace au dessus du Label() de la langue - Seulement en disposition horizontal
    if disp == "h":
        label_vide = tk.Label(frame_lang,
                              text="",
                              font=("Arial", 3),
                              compound="bottom",
                              bg=coul_interface)

        label_vide.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

    label_lang = tk.Label(frame_lang,
                          textvariable=langue,
                          font=("Arial", 10, "italic"),
                          compound="bottom",
                          fg="black",
                          bg=coul_interface)

    label_lang.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

    label_pay = tk.Label(frame_lang,
                         textvariable=pays,
                         font=("Arial", 8, "italic"),
                         compound="bottom",
                         fg="black",
                         bg=coul_interface)

    label_pay.pack(ipadx=0, ipady=0, pady=0, side=tk.TOP)

    # ---------   Création d'un Label() pour afficher mode dictée / lecture / épeler   --------- #


    label_mode = tk.Label(frame_lang,
                          text="",        # Ne rien afficher au début, juste après vient la configuration
                          font=("Arial", 10, "italic"),
                          compound="bottom",
                          fg="black",
                          bg=coul_interface)

    label_mode.pack(ipadx=0, ipady=2, pady=2, side=tk.TOP)


    # ---------   Une fois le champ de texte label_mode activé    ---------#

    if global_mode == "lire":
        actu_menu_lire()

    if global_mode == "dicter":
        actu_menu_dicter()

    if global_mode == "epeler":
        actu_menu_epeler()


    # ---------   Bouton pour copier le code QR    ---------#

    def copy_QR():
        copie_png(resourcePath("Medias/QR_Tempor.png"))

    # Créer un objet photoimage pour utiliser l'image
    photo_copy = tk.PhotoImage(file=resourcePath("Medias/Copy-20px-QR.png"))
        
    button_copy = tk.Button(frame_lang, 
                            image=photo_copy,
                            command=copy_QR,
                            bg=coul_interface
                            )
    button_copy.pack(ipadx=0, ipady=0, pady=1, side=tk.TOP)

    # ---------   Widget Text() pour recevoir le texte à mettre dans le code QR    ---------#

    text_saisi = tk.Text(frame_data, width=30, height=5, bg="white", fg="blue")
    text_saisi.pack(side=tk.LEFT)

    # Retrouver le début de la chaine de caractère envoyée par un collage du png
    # L'éffacer avec tout ce qui vient après
    def delete_png(event):
        string = "0x89 0x50"
        index = text_saisi.search(string, "1.0", "end")
        if index:
            text_saisi.delete(index, "end")

    # Fonction qui collera le texte du presse papier dans le cadre de texte
    def paste_text(event):
        text_saisi.delete("1.0", tk.END)
        text_saisi.event_generate('<<Paste>>')

        global global_errCorr
        qr_actu(event, global_errCorr, 1)  # actualiser le code QR

    text_saisi.bind("<Control-v>",
                    delete_png)  # Après le <Control-v>, enlever le texte correspondant au png (Pourquoi apparaît-il ???)
    text_saisi.bind("<KeyRelease>", lambda event: qr_actu(event, global_errCorr,
                                                          1))  # Quand des touches son lâchées : écriture ou <Control-v>, actualiser le code QR
    text_saisi.bind("<Button-3>", paste_text)  # Si simple "clic droit" --> coller le texte

    # ---------   Zone de choix de la taille du code QR   ---------#
    
    # Charger le logo dans une variable
    icon_logo = ImageTk.PhotoImage(Image.open(resourcePath("Medias/icon-20px.png")))
    # Créer le Label()
    label_logo = tk.Label(frame_size, 
                        image=icon_logo,
                        bg=coul_interface
                        )
    label_logo.pack(padx=ecart, side=tk.LEFT)

    # Label "Taille :"
    label_size = tk.Label(frame_size,
                          text="Taille :",
                          font=("Arial", 11),
                          compound="bottom",
                          bg=coul_interface)
    label_size.pack(padx=ecart, side=tk.LEFT)

    # Widget Entry() pour recevoir la valeur de la taille du code QR
    entry_size = tk.Entry(frame_size,
                          width = 5,
                          bg = coul_interface,
                          fg = "black")
    entry_size.insert(0, "150")
    entry_size.pack(side=tk.LEFT, pady=0, padx=ecart)

    # Actualiser le code QR si "Ctrl + v" ou "Clic droit" dans "entry_size"
    entry_size.bind("<Return>", lambda event: qr_actu(event, global_errCorr, 1))
    entry_size.bind("<KP_Enter>", lambda event: qr_actu(event, global_errCorr, 1))
    entry_size.bind("<Control-v>", lambda event: qr_actu(event, global_errCorr, 1))

    # ---------   Widget Scale() pour modifier la taille du code QR   ---------#

    # Création d'une fonction qui sera activée par le widget Scale()
    def syncho_size(value):
        nonlocal new_size_var  # Utiliser la variable de contrôle non locale "new_size_var"
        new_size_var.set(value)  # Y mettre la valeur de la valeur retournée par "scale_size"
        entry_size.delete(0, tk.END)  # Effacer le Widget "entry_size"
        entry_size.insert(0, str(new_size_var.get()))  # Actualiser "entry_size" avec la nouvelle valeur
        # print(f"Taille = {new_size_var.get()}")
        global global_errCorr

        if text_saisi.get("1.0", tk.END).strip() == "":
            new_img = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Bienvenue.png")))
            label_qr.config(image=new_img)  # Mettez à jour l'image du label
            label_qr.image = new_img  # Gardez une référence à la nouvelle image
        else:
            qr_actu(None, global_errCorr, 1)  # Actualiser le code QR avec la nouvelle taille

    # Création du widget Scale()
    scale_size = tk.Scale(frame_size,
                          variable=new_size_var,
                          from_=50,
                          to=150,
                          resolution=1,
                          orient=tk.HORIZONTAL,
                          command=syncho_size,
                          width=15,
                          length=90,
                          showvalue=0,
                          bg=coul_interface,
                          bd=2
                          )

    scale_size.set(150)  # Valeur initiale

    scale_size.pack(side=tk.LEFT, pady=0, padx=ecart)

    # ---------   Actualiser un icone mémoire de travail   ---------#

    # Charger l'image dans une variable
    icon_mem_str = ImageTk.PhotoImage(Image.open(resourcePath("Medias/PP-vid-20px.png")))
    # Créer le Label()
    label_mem = tk.Label(frame_size, 
                        image=icon_mem_str,
                        bg=coul_interface
                        )
    label_mem.pack(padx=7, side=tk.LEFT)

    def actu_icon_mem(mem):
        # Charger la nouvelle image
        icon_mem_png = ImageTk.PhotoImage(Image.open(resourcePath(f"Medias/PP-{mem}-20px.png")))
        # Mettre à jour l'image affichée dans le widget Label
        label_mem.configure(image=icon_mem_png)
        label_mem.image = icon_mem_png  # Mettre à jour la référence de l'image

    # Déterminer la nature du contenu du presse papier : png, vide ou texte pour adapter l'icône
    def scan_clipboard():

        # Pour ne pas commencer à mettre un PNG dans le presse papier dès le démarrage, qr_actu ne doit pas être lancée au premier démarrage
        try:
            # Obtenez le contenu du presse-papier pour vérifiez s'il est vide - Bug au démarrage si le presse papier est vide
            contenu = root.clipboard_get()

            if "0x89 0x50" in contenu:  # Vérifier si c'est un png, il commencera par "0x89 0x50" (trouvé empiriquement)
                actu_icon_mem("png")

            else:
                actu_icon_mem(
                    "str")  # Si c'est autre-chose qu'un png, afficher l'icône string. Je sais, c'est un peu faible, mais bon...

        except tk.TclError:
            actu_icon_mem("vid")  # Si la mémoire est vide, afficher l'icône mémoire vide

            if platform.system() == 'Windows' or "Darwin":
                actu_icon_mem("png")      # Actualiser l'icone du presse papier sous Windows

    # Fonction pour vérifier périodiquement le contenu du presse papier
    def periodic_scan_clipboard():
        global id_boucle
        scan_clipboard()
        id_boucle = root.after(500, periodic_scan_clipboard)  # Exécuter la fonction après une seconde (500 ms) et place l'id dans une variable
        # --> nécessaire pour pouvoir arrêter le processus proprement avant de fermer la fenêtre pincipale.

    # Lancer périodiquement la fonction grâce à une boucle after()
    periodic_scan_clipboard()

    # ---------   Label() recevant les images de codes QR   ---------#

    img_code = ImageTk.PhotoImage(Image.open(resourcePath("Medias/Bienvenue.png")))
    label_qr = tk.Label(frame_qr, image=img_code)
    label_qr.pack()

    # ---------   Fermer l'application avec "ctrl+q"   ---------#

    def quit_application(event):
        if id_boucle is not None:
            root.after_cancel(id_boucle)  # Annuler l'action périodique
        root.destroy()

    root.bind_all("<Control-q>", quit_application)

    ###### BOUCLE PRINCIPALE DE TKinter ######

    root.mainloop()


disp = "h"               # Commencer en mode horizontal
application(disp)        # Lancer la fonction principale


