"""
 ██████   ██████   █████████   ██████████ █████
▒▒██████ ██████   ███▒▒▒▒▒███ ▒▒███▒▒▒▒▒█▒▒███
 ▒███▒█████▒███  ▒███    ▒███  ▒███  █ ▒  ▒███
 ▒███▒▒███ ▒███  ▒███████████  ▒██████    ▒███
 ▒███ ▒▒▒  ▒███  ▒███▒▒▒▒▒███  ▒███▒▒█    ▒███
 ▒███      ▒███  ▒███    ▒███  ▒███ ▒   █ ▒███      █
 █████     █████ █████   █████ ██████████ ███████████
▒▒▒▒▒     ▒▒▒▒▒ ▒▒▒▒▒   ▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒

     ███████    █████        ██████
   ███▒▒▒▒▒███ ▒▒███        ███▒▒███
  ███     ▒▒███ ▒███████   ▒███ ▒▒▒  █████ ████  █████
▒███      ▒███ ▒███▒▒███ ███████   ▒▒███ ▒███  ███▒▒
▒███      ▒███ ▒███ ▒███▒▒▒███▒     ▒███ ▒███ ▒▒█████
▒▒███     ███  ▒███ ▒███  ▒███      ▒███ ▒███  ▒▒▒▒███
 ▒▒▒███████▒   ████████   █████     ▒▒████████ ██████
   ▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒   ▒▒▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒


V 6.1

https://patorjk.com/software/taag
2026-09-16

"""

########################################################################
#   Classe qui permet de cacher (obfusquer) et de retrouver (désobfusquer)
#   des chaînes de caractères.
########################################################################

import unicodedata


# ----------------------------------------------------------------------
# Petits outils pour savoir si un caractère peut aller dans un QR code
# ----------------------------------------------------------------------

# Catégories Unicode autorisées, écrites en entier.
# Zs = espace qui sépare deux mots (par exemple l'espace normal).
_ALLOWED_EXACT = frozenset({"Zs"})

# Familles de catégories autorisées (on regarde la première lettre) :
#   L = lettre, M = marque d'accent, N = chiffre,
#   P = ponctuation, S = symbole.
_ALLOWED_PREFIXES = frozenset({"L", "M", "N", "P", "S"})

# Limites du domaine Unicode.
_UNICODE_MIN = 0x0000
_UNICODE_MAX = 0x10FFFF

# Zone des "surrogates" : des codes réservés qui ne peuvent pas
# être écrits correctement en UTF-8. On les refuse toujours.
_SURROGATE_MIN = 0xD800
_SURROGATE_MAX = 0xDFFF


def _category_of(cp):
    """Renvoie la catégorie Unicode du code (un nombre entier).

    On suppose que le code est déjà valide (pas un surrogate) :
    c'est _is_qr_safe_codepoint qui fait ce tri avant.
    """
    return unicodedata.category(chr(cp))


def _is_qr_safe_codepoint(cp):
    """Renvoie True si ce code peut être écrit dans un QR code.

    On accepte : L, M, N, P, S et Zs.
    On refuse : Zl (séparateur de ligne), Zp (séparateur de paragraphe),
    Cc (contrôle), Cf (format), Cs (surrogate), Co (usage privé),
    Cn (non attribué).

    Les surrogates sont refusés exprès : Python sait les créer avec chr(),
    mais le texte obtenu ne peut pas être enregistré en UTF-8.
    """
    if cp < _UNICODE_MIN or cp > _UNICODE_MAX:
        return False
    if _SURROGATE_MIN <= cp <= _SURROGATE_MAX:
        return False
    cat = unicodedata.category(chr(cp))
    if cat in _ALLOWED_EXACT:
        return True
    return cat[0] in _ALLOWED_PREFIXES


def _next_safe_codepoint(cp):
    """Renvoie le plus petit code autorisé qui est >= cp.

    On avance tant qu'on tombe sur un code interdit.
    Si on dépasse la fin d'Unicode, on lève une erreur.
    """
    while cp <= _UNICODE_MAX:
        if _is_qr_safe_codepoint(cp):
            return cp
        cp += 1
    raise ValueError(
        f"Aucun code autorisé trouvé en avançant depuis {cp:#x} "
        "(on a dépassé la fin d'Unicode)."
    )


def _prev_safe_codepoint(cp):
    """Renvoie le plus grand code autorisé qui est <= cp.

    On recule tant qu'on tombe sur un code interdit.
    Si on descend sous zéro, on lève une erreur.
    """
    while cp >= _UNICODE_MIN:
        if _is_qr_safe_codepoint(cp):
            return cp
        cp -= 1
    raise ValueError(
        f"Aucun code autorisé trouvé en reculant depuis {cp:#x} "
        "(on est descendu sous zéro)."
    )


class Obfus:

    # Ancien dictionnaire d'exceptions, gardé vide pour ne rien casser
    # si un autre bout de code y fait encore référence.
    enobfus_excl_dict = {}

    # Constructeur de la classe.
    # Aucun attribut à créer : on n'a pas besoin de garder de données
    # quand on fabrique un objet Obfus().
    def __init__(self):
        pass

    # # # # # # # # # # # # # # # # # # # # #
    #   Décalage d'un caractère à l'autre   #
    # # # # # # # # # # # # # # # # # # # # #

    def codepoint_shifter(self, word, shift_value):
        """Décale chaque caractère de la chaîne de `shift_value` (+1 ou -1).

        Pour cacher (shift = +1) :
            On ajoute 1 au code du caractère. Si le résultat tombe sur
            une catégorie interdite, on ajoute encore 1, et ainsi de
            suite, jusqu'à trouver un caractère autorisé.

        Pour retrouver (shift = -1) :
            Même chose, mais en enlevant 1 à chaque fois.

        Grâce au filtre d'entrée (dans enobfus et deobfus), la chaîne
        reçue ne contient que des caractères autorisés. Du coup,
        l'aller-retour redonne toujours la chaîne de départ :
            deobfus(enobfus(s)) == s   pour toute chaîne valide.
        """
        if shift_value not in (1, -1):
            raise ValueError("shift_value doit être +1 ou -1")

        out = []
        for letter in word:
            cp = ord(letter)

            if shift_value == 1:
                # On avance jusqu'au prochain caractère autorisé.
                target = _next_safe_codepoint(cp + 1)
            else:
                # On recule jusqu'au précédent caractère autorisé.
                target = _prev_safe_codepoint(cp - 1)

            out.append(chr(target))

        return "".join(out)


    # # # # # # # # # # # # # # # # # # # # #
    #          Mélange des lettres          #
    # # # # # # # # # # # # # # # # # # # # #

    def shuffler(self, mot_a_enobfus):
        # On va ranger les lettres mélangées dans cette liste.
        local_mixed_word = []

        # On prend d'abord une lettre sur deux (positions impaires).
        i = 1
        while i < len(mot_a_enobfus):
            local_mixed_word.append(mot_a_enobfus[i])
            i = i + 2

        # Puis on ajoute les autres (positions paires).
        i = 0
        while i < len(mot_a_enobfus):
            local_mixed_word.append(mot_a_enobfus[i])
            i = i + 2

        # On retourne la liste pour finir le mélange.
        local_mixed_word.reverse()

        # On recolle le tout en une seule chaîne.
        local_mixed_word_str = "".join(local_mixed_word)

        # On renvoie la chaîne mélangée, prête pour le QR code.
        return local_mixed_word_str



    # # # # # # # # # # # # # # # # # # # # #
    #        Dé-mélange des lettres         #
    # # # # # # # # # # # # # # # # # # # # #


    def unshuffler(self, mot_a_deobfus):
        # On va ranger les lettres remises dans l'ordre dans cette liste.
        unmixed_word_list = []

        # Moitié de la longueur (division entière) : utile pour retrouver
        # où chaque lettre a été rangée par le mélange.
        half_len = len(mot_a_deobfus) // 2

        # Cas 1 : la longueur est paire.
        if not len(mot_a_deobfus) % 2:
            i = half_len - 1
            while i >= 0:
                unmixed_word_list.append(mot_a_deobfus[i])
                unmixed_word_list.append(mot_a_deobfus[i + half_len])
                i -= 1

        # Cas 2 : la longueur est impaire.
        else:
            # On parcourt les deux moitiés en alternant :
            #   - la première moitié, lue à l'envers
            #   - la seconde moitié, lue à l'envers aussi
            # et on ajoute la lettre du milieu à la fin.
            i = half_len
            while i >= 0:
                unmixed_word_list.append(mot_a_deobfus[i])
                if i > 0:
                    unmixed_word_list.append(mot_a_deobfus[half_len + i])
                i -= 1

        # On recolle le tout en une seule chaîne.
        unmixed_word_str = "".join(unmixed_word_list)

        # On renvoie la chaîne remise dans l'ordre.
        return unmixed_word_str


    # # # # # # # # # # # # # # # # # # # # #
    #    Filtre d'entrée (catégories)       #
    # # # # # # # # # # # # # # # # # # # # #

    def _check_input(self, word):
        """Vérifie que la chaîne ne contient que des caractères autorisés.

        Dès qu'un caractère interdit (Zl, Zp, Cc, Cf, Cs, Co, Cn) est
        trouvé, on lève une erreur en précisant sa position et sa catégorie.
        """
        for idx, letter in enumerate(word):
            cp = ord(letter)
            if not _is_qr_safe_codepoint(cp):
                cat = unicodedata.category(letter)
                raise ValueError(
                    f"Caractère interdit à la position {idx} : "
                    f"{letter!r} (U+{cp:04X}, catégorie {cat}). "
                    "Seules les catégories L, M, N, P, S, Zs sont autorisées."
                )


    # Cacher une chaîne de caractères.
    def enobfus(self, word):
        self._check_input(word)
        shifted_word = self.codepoint_shifter(word, 1)
        enobfused_word = self.shuffler(shifted_word)
        return enobfused_word

    # Retrouver la chaîne de caractères d'origine.
    def deobfus(self, word):
        self._check_input(word)
        unshifted_word = self.codepoint_shifter(word, -1)
        deobfused_word = self.unshuffler(unshifted_word)
        return deobfused_word

# ----------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # On fabrique un objet Obfus pour faire les tests.
    obfusor = Obfus()

    strings_to_obfus = [
        'Coucou tout le monde !',
        "Ça va les élèves ?",
        "Un maître à œil vif.",
        "C’eût été drôle pour Æsius.",
        "Une île",
        "Du maïs Noël !",
        "안녕하세요! 제 이름은... 입니다. 만나서 and 반갑습니다.",
        "El niño est fort à Managua.",
        "クレジットカードではらいます。",
        "書左僕射燕國公張說 製若夫玉毫流照｡甘露灑于大千｡金鏡揚暉｡",
        "У меня большая семья из шести человек: я, мама",
        "Τὴν εὐγενεστάτην ὄλυραν, ὅταν ὡς χρὴ",
        "À Noël, l'œuf est dans l'âtre contre le mûr de la façade.",
        "Est-ce que le caractère ~ est accepté ?"
    ]

    for string_to_obfus in strings_to_obfus:
        print(f"La chaîne de caractères à cacher : {string_to_obfus!r}")

        # On cache la chaîne.
        obfused_word = obfusor.enobfus(string_to_obfus)
        print(f"La chaîne une fois cachée est : {obfused_word!r}")

        # On la retrouve.
        deobfused_word = obfusor.deobfus(obfused_word)
        print(f"La chaîne une fois retrouvée est : {deobfused_word!r}")

        print(f"  -> Identique à l'original ? {deobfused_word == string_to_obfus}")
        print("")
        print(".'" * 40)
        print("")
