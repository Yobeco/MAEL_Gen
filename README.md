![MAEL](https://github.com/Yobeco/MAEL_Phono_fouille/blob/main/readme_assets/Logo-MAEL-120.png "Logo du projet MAEL")

Une application associée au projet MAEL

# MAEL Gen

Copyright (c) 2025 Yonnel Bécognée

[![License: Libre Non Commerciale](https://img.shields.io/badge/license-GNU%20GENERAL%20PUBLIC%20LICENSE%20V3-white.svg)](./LICENSE)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=yellow)

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-009900.svg)](#contributing) [![Beginner friendly](https://img.shields.io/badge/Beginner%20friendly-8A2BE2)]()

[![Status: Active](https://img.shields.io/badge/status-active-009900.svg)]()

**Auteur** : Yonnel Bécognée   
**Année** : 2025

---

![](https://github.com/Yobeco/MAEL_Gen/blob/main/readme_assets/MAEL_Gen.png)


## A- Description

Application de bureau multiplateforme (Linux, MacOS et Windows) qui permet aux enseignants de créer facilement des codes QR contenant du texte que leurs élèves peuvent écouter. 
Ils peuvent les intégrer à leurs différents supports pédagogiques, ajoutant ainsi une dimension audio à leurs documents papier.

Les codes QR seront scannés par les élèves à l'aide de l'application **MAEL Scan** :speaker: (disponible sur Android et bientôt sur iOS).

---

## B- Fonctionnalités

- **Mode "lecture"** : affiche et lit à haute voix le texte contenu dans le code QR.
- **Mode "dicter"** : n'affiche pas mais lit à haute voix le texte contenu dans le code QR.
- **Mode "épeler"** : lit à haute voix chaque lettre du texte contenu dans le code QR.
- **Mode "MP3"** : fichier provenant de Google Drive

## 3- Fonctionnalités à développer

1- **Mode "dicter"**

- Ajout d'un suffixe au contenu du code QR qui permetrra à MAEL Gen :

    - d'ajouter la lecture à voix haute des signes de ponctuation et
    - d'afficher le menu lecture-pause (avec barre de défilement)

2- **Mode "MP3"**

- Création d'un MAEL Cloud avec moins de limitations que Google Drive.

3- **Interface**

- Remplacement de TKinter par **TTKBootstrap**
- **Déplacer les boutons d'accès au changement de mode** du menu « Paramètres » à vers l'emplacement du curseur (qui sera supprimé).

**:+1: Vous pouvez proposer votre aider pour developper ces fonctions**

## 4- Pour participer au développement

Écrivez moi à :

### 📨 ***[mael@lvh.edu.ni](mailto:mael@lvh.edu.ni)***

---

## C- Installation

Clonez ce dépôt et exécutez le script :

    git clone git://github.com/toncompte/MAEL_Gen.git
    cd phono-fouille
    python3 monscript.py