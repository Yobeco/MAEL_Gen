# Installation sous Debian

# Script d'installation Debian complet avec création de `requirements.txt`

Voici le script bash `install_mael.sh` qui installe les dépendances système **et** crée le fichier `requirements.txt` avec son contenu :

```bash
#!/usr/bin/env bash
# =====================================================================
# install_mael.sh — Installation de l'environnement MAEL sous Debian
# Cible : Python 3.13 (Debian Trixie) ou Python 3.11+ (Bookworm)
# Usage : bash install_mael.sh
# =====================================================================

set -euo pipefail

# ---------------------------------------------------------------------
# 1. Création du fichier requirements.txt
# ---------------------------------------------------------------------
echo "📝 Création du fichier requirements.txt..."

touch requirements.txt

cat > requirements.txt <<'EOF'
# =====================================================================
# requirements.txt — Équivalent Debian du shell.nix (environnement MAEL)
# Cible : Python 3.13 sous Debian (Bookworm / Trixie)
# Usage : python3.13 -m venv .venv && source .venv/bin/activate
#         pip install -r requirements.txt
# =====================================================================

# --- Interface graphique ---------------------------------------------
# NB : 'tkinter' n'est PAS installable via pip.
#      Il faut installer le paquet système : sudo apt install python3-tk
ttkbootstrap>=1.10.1
pillow>=10.3.0

# --- Génération de QR codes (MAEL_V6.0) ------------------------------
qrcode>=7.4.2

# --- Détection et annotation PDF (MAEL_Verif_PDF) --------------------
zxing-cpp>=2.2.0
opencv-python>=4.10.0.84
numpy>=1.26.0
fpdf2>=2.7.9
pypdfium2>=4.30.0
pypdf>=4.3.0

# --- Presse-papier (MAEL_V6.0) ---------------------------------------
# Équivalent du paquet Nix 'pyperclip'
pyperclip>=1.9.0

# --- Outils de développement (optionnels, comme dans shell.nix) ------
ipython>=8.27.0
pytest>=8.3.0
black>=24.8.0
ruff>=0.6.0
EOF

echo "✅ requirements.txt créé."

# ---------------------------------------------------------------------
# 2. Dépendances système (apt)
# ---------------------------------------------------------------------
echo "📦 Installation des dépendances système..."

sudo apt update
sudo apt install -y \
    python3 python3-venv python3-dev python3-tk \
    libgl1 libglib2.0-0 \
    libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev \
    libxcb1 libx11-6 libxext6 \
    xclip xsel wl-clipboard git

# ---------------------------------------------------------------------
# 3. Environnement virtuel Python
# ---------------------------------------------------------------------
echo "🐍 Création de l'environnement virtuel .venv..."

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

# ---------------------------------------------------------------------
# 4. Installation des dépendances Python
# ---------------------------------------------------------------------
echo "⬇️  Installation des paquets Python..."

pip install --upgrade pip
pip install -r requirements.txt

# ---------------------------------------------------------------------
# 5. Message final
# ---------------------------------------------------------------------
echo ""
echo "🚀 Environnement MAEL prêt."
echo "🐍 Python : $(python --version)"
echo "📦 Modules : tkinter, ttkbootstrap, qrcode, pillow, cv2,"
echo "             numpy, zxingcpp, fpdf, pypdf, pypdfium2, pyperclip"
echo "🖥️  Presse-papier : xclip, xsel, wl-clipboard"
echo ""
echo "Pour activer l'environnement dans un nouveau terminal :"
echo "  source .venv/bin/activate"
echo ""
echo "Pour lancer les applications :"
echo "  python MAEL_V6.0.py"
echo "  python MAEL_Verif_PDF.py <fichier.pdf>"
echo ""
```

---

## 🔍 Détails des commandes utilisées

### `touch requirements.txt`
Crée un fichier **vide** s'il n'existe pas (et met à jour son horodatage s'il existe déjà). Utile pour garantir la présence du fichier avant l'écriture.

### `cat > requirements.txt <<'EOF' ... EOF`
Redirige le contenu du *here-document* vers le fichier. Les quotes simples autour de `EOF` (`<<'EOF'`) empêchent l'interprétation des variables et caractères spéciaux (`$`, backticks) — important ici puisqu'il y a des `$` potentiels dans les commentaires.

> 💡 **Alternative** : on pourrait se passer de `touch` puisque `cat >` crée le fichier s'il n'existe pas. Mais comme demandé, on garde le `touch` explicite — c'est aussi une bonne pratique si l'on veut vérifier les permissions d'écriture avant.

---

## 🚀 Utilisation

```bash
# 1. Rendre le script exécutable
chmod +x install_mael.sh

# 2. Lancer l'installation
./install_mael.sh

# 3. Activer le venv (dans chaque nouveau terminal)
source .venv/bin/activate

# 4. Lancer les scripts
python MAEL_V6.0.py
python MAEL_Verif_PDF.py <fichier.pdf>
```

---

## ⚙️ Variantes possibles

### Si tu veux forcer Python 3.13 explicitement

Remplace dans la section 3 :

```bash
python3 -m venv .venv
```

par :

```bash
python3.13 -m venv .venv
```

et dans la section 2, adapte les paquets :

```bash
sudo apt install -y python3.13 python3.13-venv python3.13-dev python3-tk ...
```

### Si tu es sur un serveur sans écran

Remplace dans `requirements.txt` :

```txt
opencv-python>=4.10.0.84
```

par :

```txt
opencv-python-headless>=4.10.0.84
```

### Pour un venv sans les outils de dev

Supprime simplement les 4 dernières lignes de `requirements.txt` (`ipython`, `pytest`, `black`, `ruff`).



---

# `set -euo pipefail` — Le "mode strict" du shell

Cette ligne est une **combinaison de quatre options** de Bash qui rendent un script beaucoup plus **robuste** et **prévisible**. Sans elle, un script Bash continue silencieusement même après une erreur, ce qui peut produire des comportements catastrophiques (suppression de fichiers, installations incomplètes, etc.).

Décomposons chaque partie :

---

## 🔹 `set -e` → *errexit*

**Le script s'arrête immédiatement dès qu'une commande retourne un code de sortie non nul** (c'est-à-dire une erreur).

### Sans `-e` :

```bash
#!/usr/bin/env bash
cd /dossier/qui/nexiste/pas   # échoue silencieusement
rm -rf *                       # ⚠️ s'exécute quand même dans le mauvais dossier !
```

### Avec `-e` :

```bash
#!/usr/bin/env bash
set -e
cd /dossier/qui/nexiste/pas   # ❌ échec → le script s'arrête ICI
rm -rf *                       # jamais atteint → pas de catastrophe
```

> ⚠️ **Exceptions** : `-e` est ignoré dans certains contextes :
> - commandes dans un `if`, `while`, `until`
> - commandes précédées de `!`
> - commandes dans un `&&` ou `||` (sauf la dernière)
> - commandes dont le code retour est explicitement testé

---

## 🔹 `set -u` → *nounset*

**Toute utilisation d'une variable non définie provoque une erreur** et arrête le script.

### Sans `-u` :

```bash
#!/usr/bin/env bash
echo "Bonjour $UTILISATEUR"    # UTILISATEUR non défini → affiche "Bonjour " (silencieux)
rm -rf "$DOSSIER"/*             # DOSSIER vide → rm -rf /* 💀
```

### Avec `-u` :

```bash
#!/usr/bin/env bash
set -u
echo "Bonjour $UTILISATEUR"
# ❌ bash: UTILISATEUR: unbound variable
```

C'est une protection **vitale** contre les fautes de frappe (`$DOSSIER` au lieu de `$DOSSIERS`) et les variables oubliées.

> 💡 **Astuce** : si tu veux autoriser une variable optionnelle, utilise la syntaxe `${VAR:-valeur_par_défaut}` ou `${VAR:-}`.

---

## 🔹 `set -o pipefail` → *pipefail*

**Dans un pipeline `cmd1 | cmd2 | cmd3`, le code de retour du pipeline est celui de la dernière commande qui a échoué** (au lieu du code de la dernière commande uniquement).

### Sans `pipefail` :

```bash
#!/usr/bin/env bash
set -e
false | true                    # code retour = 0 (celui de `true`)
echo "on continue..."           # ✅ s'affiche → l'erreur de `false` est masquée
```

### Avec `pipefail` :

```bash
#!/usr/bin/env bash
set -eo pipefail
false | true                    # code retour = 1 (celui de `false`)
echo "on continue..."           # ❌ jamais atteint
```

### Cas concret — pourquoi c'est crucial :

```bash
# Sans pipefail : détecte seulement l'échec de `tee`
curl https://exemple.com/data | tee data.txt

# Avec pipefail : détecte l'échec de `curl` OU de `tee`
set -o pipefail
curl https://exemple.com/data | tee data.txt
```

Sans `pipefail`, si `curl` échoue (réseau coupé), `tee` réussit quand même → le pipeline retourne 0 → **l'erreur réseau passe inaperçue**.

---

## 🔹 Combinaison `-euo` + `pipefail`

On peut écrire les trois options courtes d'un coup :

```bash
set -euo pipefail
```

C'est équivalent à :

```bash
set -e
set -u
set -o pipefail
```

`-euo` regroupe `-e`, `-u`, `-o`... mais attention : `-o pipefail` ne peut **pas** être abrégé en `-op` car `pipefail` est le *nom* de l'option, pas une lettre. C'est pourquoi on écrit `set -euo pipefail` et non `set -eup`.

---

## 🎯 Résumé visuel

| Option        | Nom        | Effet                                         | Danger évité                          |
| ------------- | ---------- | --------------------------------------------- | ------------------------------------- |
| `-e`          | `errexit`  | Stoppe à la 1ʳᵉ erreur                        | `rm -rf` après un `cd` raté           |
| `-u`          | `nounset`  | Erreur si variable non définie                | `rm -rf $VAR` avec `VAR` vide         |
| `-o pipefail` | `pipefail` | Le pipeline échoue si **une** commande échoue | Erreur masquée par le dernier maillon |

---

## 🛡️ Bonnes pratiques associées

### 1. `IFS` — souvent ajouté en complément

```bash
set -euo pipefail
IFS=$'\n\t'
```

Cela évite les mauvaises surprises avec les espaces dans les noms de fichiers lors des boucles `for`.

### 2. `set -x` — pour déboguer

```bash
set -euo pipefail
set -x    # affiche chaque commande avant exécution
```

Utile temporairement pour voir où ça coince, à retirer en production.

### 3. Ne pas mettre `set -e` dans un `.bashrc`

Dans un shell interactif, `set -e` est **dangereux** : la moindre commande qui échoue (par ex. `grep` sans résultat) fermerait ton terminal. À réserver aux **scripts**.

---

## ⚠️ Pièges courants avec `set -e`

### Piège 1 — `grep` qui ne trouve rien

```bash
set -e
grep "motif" fichier.txt    # ❌ si rien trouvé → exit 1 → script stoppé
```

**Solution** :

```bash
grep "motif" fichier.txt || true
# ou
if grep -q "motif" fichier.txt; then
    echo "trouvé"
fi
```

### Piège 2 — Lecture dans une boucle

```bash
set -e
while read -r ligne; do
    echo "$ligne"
done < fichier.txt          # ❌ le dernier read renvoie 1 (EOF) → script stoppé
```

**Solution** :

```bash
while read -r ligne; do
    echo "$ligne"
done < fichier.txt || true
```

### Piège 3 — `-u` avec `$@` ou `$1`

```bash
set -u
echo "$1"                    # ❌ erreur si aucun argument fourni
```

**Solution** :

```bash
echo "${1:-}"                # OK, valeur vide par défaut
```

---

## 🧠 En résumé

`set -euo pipefail` transforme Bash d'un langage **permissif** (qui continue malgré les erreurs) en un langage **strict** (qui s'arrête à la première anomalie).

C'est **la première ligne à mettre dans tout script Bash sérieux** — sauf raison particulière de ne pas le faire. Dans notre script `install_mael.sh`, elle garantit par exemple que :

- Si `sudo apt install` échoue → on **n'exécute pas** `python3 -m venv` dans un environnement bancal.
- Si `pip install -r requirements.txt` échoue → on **n'affiche pas** le message final "🚀 Environnement MAEL prêt" (ce qui serait mensonger).
- Si `curl` ou tout autre outil échoue dans un pipeline → on le sait immédiatement.
