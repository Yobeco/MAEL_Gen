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

![](./readme_assets/MAEL_Gen.png)


## A- Description :eye:

Application de bureau multiplateforme (Linux, MacOS et Windows) qui permet aux enseignants de créer facilement des codes QR contenant du texte que leurs élèves peuvent écouter. 
Ils peuvent les intégrer à leurs différents supports pédagogiques, ajoutant ainsi une dimension audio à leurs documents papier.

Les codes QR seront scannés par les élèves à l'aide de l'application **MAEL Scan** :speaker: (disponible sur Android et bientôt sur iOS).

---

## B- Fonctionnalités :clipboard:

- **Mode "lecture"** : affiche et lit à haute voix le texte contenu dans le code QR.
- **Mode "dicter"** : n'affiche pas mais lit à haute voix le texte contenu dans le code QR.
- **Mode "épeler"** : lit à haute voix chaque lettre du texte contenu dans le code QR.
- **Mode "MP3"** : lit un fichier provenant de Google Drive.

---

## C- Principe de fonctionnement :gear:

*(Pour aider à la compréhension du code)*

---

**:one: Au premier démarrage**

Quand on écrit un texte dans l'entrée de texte, la langue par défault est "français" :fr: et le mode par défaut est "Lecture" :

1- Le texte subit d'abord un "encryptage" léger.

2- Un code QR contenant ce texte (utf-8) est généré.

*⟶ MAEL Scan comprendra qu'il est en mode lecture et utilisera la voix de synthèse française :fr:.*

---

**:two: Si vous changez _la langue_ du contenu par exemple _italien_ :**

1- Le texte reçoit un préfixe du type `<it>`

2- Le texte subit d'abord un "encryptage" léger.

3- Un code QR contenant ce texte (utf-8) est généré.

*⟶ __MAEL Scan__ comprendra qu'il est en __mode lecture__ et utilisera la voix de synthèse de voix __italienne__ :it:.*

---

**:three: Si vous choisissez le *mode dicter* :**

1- Le texte reçoit un préfixe du type `<it>`

2- Le texte reçoit un siffixe du type `#d`

2- Le texte subit d'abord un "encryptage" léger.

3- Un code QR contenant ce texte (utf-8) est généré.

*⟶ __MAEL Scan__ comprendra qu'il est en __mode dictée__ et utilisera la voix de synthèse de voix __italienne__ :it:.*

Les voix de synthèse sont celles générée oar le téléphone.

:eyes: Certaines langues (avec gtts) ont plusieurs voix possibles, par exemples :

| Voix | Préfixe |
| ----------- | ----------- |
| Portugais du portugal | `<ptPRT>` |
| Portugais du Bésil | `<ptBRA>` |

:bookmark_tabs: [Voir la liste des lagues de GTTS (Probablement à actualiser...)](./readme_assets/Langues_GTTS.pdf)

---

**:four: À chaque modification :**

Le fichier `.png` généré est automatiquement envoyé dans le presse-papier.
(Un petit icône indique si dans le presse-papier, il y a un code QR ou du texte)

⟶ Le professeur n'a plus qu'à faire `Coller` dans son éditeur personnel.

---

## D- Fonctionnalités à développer :rocket:

1- **Mode "dicter"**

- Le mode dictée actuelle va changer de nom et s'appeler "Mode caché".

- Le mode dictée reste une lecture sans montrer le texte, mais il faudrait :

    - ajouter l'oralisation de la ponctuation et
    - afficher le menu lecture-pause (avec barre de défilement)

2- **Mode "MP3"**

- Création d'un MAEL Cloud avec moins de limitations que Google Drive.

3- **Interface**

- Remplacement de TKinter par **TTKBootstrap**
- **Déplacer les boutons d'accès au changement de mode** du menu « Paramètres » à vers l'emplacement du curseur (qui sera supprimé).
- Gestion des langues s'écrivant de droite à gauche.

**:+1: Vous pouvez proposer votre aider pour developper ces fonctions**

4- **LibreOffice** <img src="https://cdn.simpleicons.org/react/61DAFB" width="24" height="24" style="vertical-align: middle;" />

Quand on crée un document contenant beaucoup de codes QR, il devient plus facile de se tromper. (Mettre deux fois le même code QR par exemple... :sweat_smile: )

*(Pour que le professeur puisse voir d'un seul coup d'oeil le mode du code QR, j'avais ajouté un petit carré de couleur en bas à droite.)*

De la même manière, pour pouvoir vérifier facilement le contenu du code QR, j'aurais voulu ajouter ce texte dans les méta-données du fichier .png pour que sous LibreOffice, dans une bulle apparaisse les métadonnées de l'image ou bien quelles soient visibles dans l'inspecteur (colonne à droite).


---

## E- Pour participer au développement :open_hands:

Écrivez moi ici :

### 📨 ***[mael@lvh.edu.ni](mailto:mael@lvh.edu.ni)***

---

## C- Installation

Pour essayer MAEL_Gen, exécutez le script :

    git clone https://github.com/Yobeco/MAEL_Gen.git
    cd MAEL_Gen
    python3 -m venv mael_venv
    source mael_venv/bin/activate     pip install -r requirements.txt
    python3 MAEL_V5.0.py


