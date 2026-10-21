# Dictionnaires contenant les correspondances entre les lettres
# et la façon de les épeler.
# https://patorjk.com/software/taag


"""
  ______                         _
 |  ____|                       (_)
 | |__ _ __ __ _ _ __   ___ __ _ _ ___
 |  __| '__/ _` | '_ \ / __/ _` | / __|
 | |  | | | (_| | | | | (_| (_| | \__ \
 |_|  |_|  \__,_|_| |_|\___\__,_|_|___/
                        )_)
"""

epel_tts_fr = {
    # ==================================================================
    # 1. LETTRES ACCENTUÉES
    # ==================================================================
    "\u00c9": "e majuscule accent aigu",          # [É]
    "\u00e0": "a accent grave",                   # [à]
    "\u00c0": "a majuscule accent grave",         # [À]
    "\u00e8": "e accent grave",                   # [è]
    "\u00c8": "e majuscule accent grave",         # [È]
    "\u00f9": "u accent grave",                   # [ù]
    "\u00d9": "u majuscule accent grave",         # [Ù]
    "\u00e2": "a accent circonflexe",             # [â]
    "\u00c2": "a majuscule accent circonflexe",   # [Â]
    "\u00ea": "e accent circonflexe",             # [ê]
    "\u00ca": "e majuscule accent circonflexe",   # [Ê]
    "\u00ee": "i accent circonflexe",             # [î]
    "\u00ce": "i majuscule accent circonflexe",   # [Î]
    "\u00f4": "o accent circonflexe",             # [ô]
    "\u00d4": "o majuscule accent circonflexe",   # [Ô]
    "\u00fb": "u accent circonflexe",             # [û]
    "\u00db": "u majuscule accent circonflexe",   # [Û]
    "\u00eb": "e tréma",                          # [ë]
    "\u00cb": "e majuscule tréma",                # [Ë]
    "\u00ef": "i tréma",                          # [ï]
    "\u00cf": "i majuscule tréma",                # [Ï]
    "\u00fc": "u tréma",                          # [ü]
    "\u00dc": "u majuscule tréma",                # [Ü]
    "\u00ff": "i grec tréma",                     # [ÿ]
    "\u0178": "i grec majuscule tréma",           # [Ÿ]
    "\u00e7": "c cédille",                        # [ç]
    "\u00c7": "c cédille majuscule",              # [Ç]

    # ==================================================================
    # 2. LIGATURES ET LETTRES PARTICULIÈRES
    # ==================================================================
    "\u00e6": "e dans le a",                      # [æ]
    "\u00c6": "e dans le a majuscule",            # [Æ]
    "\u0153": "e dans le o",                      # [œ]
    "\u0152": "e dans le o majuscule",            # [Œ]
    "\u0079": "i grec",                           # [y]
    "\u0077": "double v",                         # [w]


    # ==================================================================
    # 3. LETTRES MAJUSCULES
    # ==================================================================
    "\u0041": "a majuscule",                      # [A]
    "\u0042": "b majuscule",                      # [B]
    "\u0043": "c majuscule",                     # [C]
    "\u0044": "d majuscule",                      # [D]
    "\u0045": "e majuscule",                      # [E]
    "\u0046": "f majuscule",                     # [F]
    "\u0047": "g majuscule",                      # [G]
    "\u0048": "h majuscule",                     # [H]
    "\u0049": "i majuscule",                     # [I]
    "\u004a": "j majuscule",                     # [J]
    "\u004b": "k majuscule",                     # [K]
    "\u004c": "l majuscule",                     # [L]
    "\u004d": "m majuscule",                     # [M]
    "\u004e": "n majuscule",                     # [N]
    "\u004f": "o majuscule",                     # [O]
    "\u0050": "p majuscule",                     # [P]
    "\u0051": "q majuscule",                     # [Q]
    "\u0052": "r majuscule",                     # [R]
    "\u0053": "s majuscule",                     # [S]
    "\u0054": "t majuscule",                     # [T]
    "\u0055": "u majuscule",                     # [U]
    "\u0056": "v majuscule",                     # [V]
    "\u0057": "double v majuscule",              # [W]
    "\u0058": "x majuscule",                     # [X]
    "\u0059": "i grec majuscule",                # [Y]
    "\u005a": "z majuscule",                     # [Z]

    # ==================================================================
    # 4. LETTRES MINUSCULES
    # ==================================================================
    "\u0061": "a",                               # [a]
    "\u0062": "b",                               # [b]
    "\u0063": "c",                               # [c]
    "\u0064": "d",                               # [d]
    "\u0065": "e",                               # [e]
    "\u0066": "f",                               # [f]
    "\u0067": "g",                               # [g]
    "\u0068": "h",                               # [h]
    "\u0069": "i",                               # [i]
    "\u006a": "j",                               # [j]
    "\u006b": "k",                               # [k]
    "\u006c": "l",                               # [l]
    "\u006d": "m",                               # [m]
    "\u006e": "n",                               # [n]
    "\u006f": "o",                               # [o]
    "\u0070": "p",                               # [p]
    "\u0071": "q",                               # [q]
    "\u0072": "r",                               # [r]
    "\u0073": "s",                               # [s]
    "\u0074": "t",                               # [t]
    "\u0075": "u",                               # [u]
    "\u0076": "v",                               # [v]
    "\u0077": "double v",                        # [w]
    "\u0078": "x",                               # [x]
    "\u0079": "i grec",                          # [y]
    "\u007a": "z",                               # [z]

    # ==================================================================
    # 5. PONCTUATION
    # ==================================================================
    "\u002c": "virgule",                         # [,]
    "\u002e": "point",                           # [.]
    "\u003b": "point-virgule",                   # [;]
    "\u003a": "deux points",                     # [:]
    "\u003f": "point d'interrogation",           # [?]
    "\u0021": "point d'exclamation",             # [!]
    "\u2026": "points de suspension",            # […]
    "\u0028": "parenthèse ouverte",              # [(]
    "\u0029": "parenthèse fermée",               # [)]
    "\u005b": "crochet ouvert",                  # [[]
    "\u005d": "crochet fermé",                   # []]
    "\u007b": "accolade ouverte",                # [{]
    "\u007d": "accolade fermée",                 # [}]
    "\u00b7": "point médian",                    # [·]
    "\u2030": "pour mille",                      # [‰]
    "\u00a4": "symbole monétaire",               # [¤]

    # ==================================================================
    # 6. APOSTROPHES
    # Les trois formes partagent la valeur "apostrophe" (même prononciation).
    # ==================================================================
    "\u0027": "apostrophe",                      # ['] apostrophe droite (touche 4)
    "\u2019": "apostrophe",                      # [’] typographique — comment. : même valeur
    "\u02bc": "apostrophe",                      # [ʼ] apostrophe lettre — comment. : même valeur
    "\u0060": "apostrophe",                      # [`] accent grave détourné — comment. : même valeur

    # ==================================================================
    # 7. GUILLEMETS (distinction ouvrant / fermant)
    # Chaque paire typographique partage sa valeur.
    # ==================================================================
    "\u00ab": "ouvrez les guillemets",               # [«] chevron
    "\u00bb": "fermez les guillemets",               # [»] chevron
    "\u201c": "ouvrez les guillemets",               # [“] double virgule haute
    "\u201d": "fermez les guillemets",               # [”] double virgule haute
    "\u201e": "ouvrez les guillemets",               # [„] double virgule basse
    "\u201f": "ouvrez les guillemets",               # [‟] double virgule haute renversée (rare)
    "\u0022": "guillemets",                          # ["] droit — comment. : ouvrant/fermant selon contexte
    "\u2018": "ouvrez les guillemets",               # [‘] simple virgule haute
    "\u201b": "ouvrez les guillemets",               # [‛] simple virgule haute renversée (rare)
    "\u201a": "virgule",                             # [‚] simple virgule basse
    "\u2039": "ouvrez les guillemets",               # [‹] chevron simple
    "\u203a": "fermez les guillemets",               # [›] chevron simple

    # ==================================================================
    # 8. TIRETS ET BARRES
    # Hyphen-minus est polyvalent : valeur "trait d'union" (usage dominant).
    # Demi-cadratin, cadratin et puces partagent la valeur "tiret".
    # ==================================================================
    "\u002d": "trait d'union",                   # [-] hyphen-minus (touche 6) — comment. : usage dominant
    "\u2010": "trait d'union",                   # [‐] — comment. : même valeur que la touche 6
    "\u2011": "trait d'union",                   # [‑] insécable — comment. : même valeur
    "\ufe63": "trait d'union",                   # [﹣] petite variante — comment. : même valeur
    "\uff0d": "trait d'union",                   # [－] pleine chasse — comment. : même valeur
    "\u2012": "tiret",                           # [‒] tiret chiffres
    "\u2013": "tiret",                           # [–] demi-cadratin
    "\u2014": "tiret",                           # [—] cadratin
    "\u2015": "tiret",                           # [―] barre horizontale
    "\u2212": "moins",                           # [−] signe moins mathématique
    "\u2022": "tiret",                           # [•] puce — comment. : lu comme un tiret de liste
    "\u2023": "tiret",                           # [‣] puce triangulaire — comment. : idem
    "\u002f": "barre oblique",                   # [/]
    "\u005c": "barre oblique inversée",          # [\]
    "\u007c": "barre verticale",                 # [|]
    "\u005f": "tiret bas",                       # [_]

    # ==================================================================
    # 9. SYMBOLES ET SIGNES
    # ==================================================================
    "\u20ac": "euro",                            # [€]
    "\u0024": "dollar",                          # [$]
    "\u00a3": "livre",                           # [£]
    "\u00a2": "cent",                            # [¢]
    "\u0023": "dièse",                          # [#]
    "\u002a": "astérisque",                      # [*]
    "\u0040": "arobase",                         # [@]
    "\u0026": "et commercial",                  # [&]
    "\u0025": "pour cent",                      # [%]
    "\u002b": "plus",                            # [+]
    "\u003d": "égal",                            # [=]
    "\u003c": "inférieur",                       # [<]
    "\u003e": "supérieur",                       # [>]
    "\u005e": "accent circonflexe",              # [^]
    "\u007e": "tilde",                           # [~]
    "\u00b0": "degré",                          # [°]
    "\u00a7": "paragraphe",                      # [§]
    "\u00b6": "paragraphe",                      # [¶] pied de mouche — comment. : même valeur que §
    "\u2020": "obèle",                           # [†]
    "\u2021": "double obèle",                    # [‡]
    "\u00a9": "copyright",                       # [©]
    "\u00ae": "marque déposée",                   # [®]
    "\u2122": "marque déposée",                  # [™] — comment. : même valeur que ®
    "\u00d7": "multiplié par",                   # [×]
    "\u00f7": "divisé par",                      # [÷]
    "\u2260": "différent de",                    # [≠]
    "\u2264": "inférieur ou égal",               # [≤]
    "\u2265": "supérieur ou égal",               # [≥]

    # ==================================================================
    # 10. ESPACES (catégorie Zs uniquement)
    # Toutes les largeurs partagent la valeur "espace" (même prononciation).
    # ==================================================================
    "\u0020": "espace",                          # [ ] espace ordinaire
    "\u00a0": "espace",                          # [ ] insécable — comment. : même valeur
    "\u202f": "espace",                          # [ ] fine insécable — comment. : même valeur
    "\u2009": "espace",                          # [ ] fine — comment. : même valeur
    "\u2007": "espace",                          # [ ] insécable chiffres — comment. : même valeur
    "\u2008": "espace",                          # [ ] de ponctuation — comment. : même valeur
    "\u200a": "espace",                          # [ ] ultrafine — comment. : même valeur

    # ==================================================================
    # 11. SPÉCIAL : catégories Zp, Zl et C (contrôle et format)
    # --> Pour tests : Incompatibles avec les codes QR
    # Zp = Paragraph Separator, Zl = Line Separator,
    # C  = Control (Cc), Format (Cf), Private Use (Co), Unassigned (Cn).
    # Ces caractères sont invisibles ou structurels : ils sont soit rendus
    # comme un espace/saut, soit ignorés (valeur vide).
    # ==================================================================
    # --- Zp et Zl (séparateurs de zone) ---
    "\u2029": "espace",                          # [ ] séparateur de paragraphe — comment. : rendu comme un espace
    "\u2028": "espace",                          # [ ] séparateur de ligne — comment. : rendu comme un espace

    # --- Cc : caractères de contrôle (ponctuels) ---
    "\u0009": "espace",                          # [ ] tabulation horizontale — comment. : rendu comme un espace
    "\u000a": "espace",                          # [ ] saut de ligne (LF) — comment. : rendu comme un espace
    "\u000b": "espace",                          # [ ] tabulation verticale — comment. : idem
    "\u000c": "espace",                          # [ ] saut de page (FF) — comment. : idem
    "\u000d": "espace",                          # [ ] retour chariot (CR) — comment. : idem
    "\u0000": "",                                # [ ] NUL — comment. : ignoré
    "\u0001": "",                                # [ ] SOH — comment. : ignoré
    "\u0002": "",                                # [ ] STX — comment. : ignoré
    "\u0003": "",                                # [ ] ETX — comment. : ignoré
    "\u0004": "",                                # [ ] EOT — comment. : ignoré
    "\u0005": "",                                # [ ] ENQ — comment. : ignoré
    "\u0006": "",                                # [ ] ACK — comment. : ignoré
    "\u0007": "",                                # [ ] BEL — comment. : ignoré
    "\u0008": "",                                # [ ] retour arrière (BS) — comment. : ignoré
    "\u000e": "",                                # [ ] Shift In — comment. : ignoré
    "\u000f": "",                                # [ ] Shift Out — comment. : ignoré
    "\u0010": "",                                # [ ] Data Link Escape — comment. : ignoré
    "\u0011": "",                                # [ ] Device Control 1 — comment. : ignoré
    "\u0012": "",                                # [ ] Device Control 2 — comment. : ignoré
    "\u0013": "",                                # [ ] Device Control 3 — comment. : ignoré
    "\u0014": "",                                # [ ] Device Control 4 — comment. : ignoré
    "\u0015": "",                                # [ ] Negative Ack — comment. : ignoré
    "\u0016": "",                                # [ ] Synchronous Idle — comment. : ignoré
    "\u0017": "",                                # [ ] End of Trans. Block — comment. : ignoré
    "\u0018": "",                                # [ ] Cancel — comment. : ignoré
    "\u0019": "",                                # [ ] End of Medium — comment. : ignoré
    "\u001a": "",                                # [ ] Substitute — comment. : ignoré
    "\u001b": "",                                # [ ] Escape — comment. : ignoré
    "\u001c": "",                                # [ ] File Separator — comment. : ignoré
    "\u001d": "",                                # [ ] Group Separator — comment. : ignoré
    "\u001e": "",                                # [ ] Record Separator — comment. : ignoré
    "\u001f": "",                                # [ ] Unit Separator — comment. : ignoré
    "\u007f": "",                                # [ ] DEL — comment. : ignoré

    # --- Cf : caractères de format (invisibles) ---
    "\u00ad": "",                                # [­] trait d'union conditionnel (SOFT HYPHEN) — comment. : ignoré (invisible hors césure)
    "\u200b": "",                                # [​] espace zéro largeur — comment. : ignoré
    "\u200c": "",                                # [‌] anti-liant (ZWNJ) — comment. : ignoré
    "\u200d": "",                                # [‍] liant (ZWJ) — comment. : ignoré
    "\u200e": "",                                # [‎] marque gauche-droite (LRM) — comment. : ignoré
    "\u200f": "",                                # [‏] marque droite-gauche (RLM) — comment. : ignoré
    "\u202a": "",                                # [‎] début LRE — comment. : ignoré
    "\u202b": "",                                # [‏] début RLE — comment. : ignoré
    "\u202c": "",                                # [‬] fin de directionnalité (PDF) — comment. : ignoré
    "\u202d": "",                                # [‎] début LRO — comment. : ignoré
    "\u202e": "",                                # [‏] début RLO — comment. : ignoré
    "\u2060": "",                                # [⁠] liant sans largeur (WJ) — comment. : ignoré
    "\ufeff": "",                                # [﻿] BOM / espace zéro insécable — comment. : ignoré

    # --- Co et Cn : usage privé et non assigné ---
    # Les plages Co (U+E000–U+F8FF) et Cn (non assignés) n'ont pas de
    # lecture possible : à traiter par défaut avec la chaîne vide dans
    # le code du TTS (fallback), sans énumération exhaustive ici.
}



# Générés avec Mistral --> à vérifier

"""
  ______                                   _
 |  ____|                                 | |
 | |__   ___ _ __   __ _  __ _ _ __   ___ | |
 |  __| / __| '_ \ / _` |/ _` | '_ \ / _ \| |
 | |____\__ \ |_) | (_| | (_| | | | | (_) | |
 |______|___/ .__/ \__,_|\__, |_| |_|\___/|_|
            | |           __/ |
            |_|          |___/
"""



epel_tts_es = {
    # ==================================================================
    # 1. LETRAS ACENTUADAS (MAYÚSCULAS)
    # El español usa la tilde aguda en vocales abiertas y cerradas.
    # ==================================================================
    "\u00c1": "a mayúscula con tilde",           # [Á]
    "\u00c9": "e mayúscula con tilde",           # [É]
    "\u00cd": "i mayúscula con tilde",           # [Í]
    "\u00d3": "o mayúscula con tilde",           # [Ó]
    "\u00da": "u mayúscula con tilde",           # [Ú]

    # ==================================================================
    # 2. LETRAS PARTICULARES DEL ESPAÑOL
    # La ñ (eñe) es la letra distintiva del español.
    # La ü solo aparece en las sílabas gue/gui (pingüino).
    # ==================================================================
    "\u00d1": "eñe mayúscula",                   # [Ñ]
    "\u00f1": "eñe",                             # [ñ] única minúscula especial incluida
    "\u00dc": "u mayúscula con diéresis",        # [Ü]
    "\u00fc": "u con diéresis",                  # [ü] única minúscula especial incluida

    # ==================================================================
    # 3. LETRAS MAYÚSCULAS
    # ==================================================================
    "\u0041": "a mayúscula",                     # [A]
    "\u0042": "b mayúscula",                     # [B]
    "\u0043": "c mayúscula",                     # [C]
    "\u0044": "d mayúscula",                     # [D]
    "\u0045": "e mayúscula",                     # [E]
    "\u0046": "f mayúscula",                     # [F]
    "\u0047": "g mayúscula",                     # [G]
    "\u0048": "h mayúscula",                     # [H]
    "\u0049": "i mayúscula",                     # [I]
    "\u004a": "j mayúscula",                     # [J]
    "\u004b": "k mayúscula",                     # [K]
    "\u004c": "l mayúscula",                     # [L]
    "\u004d": "m mayúscula",                     # [M]
    "\u004e": "n mayúscula",                     # [N]
    "\u004f": "o mayúscula",                     # [O]
    "\u0050": "p mayúscula",                     # [P]
    "\u0051": "q mayúscula",                     # [Q]
    "\u0052": "r mayúscula",                     # [R]
    "\u0053": "s mayúscula",                     # [S]
    "\u0054": "t mayúscula",                     # [T]
    "\u0055": "u mayúscula",                     # [U]
    "\u0056": "v mayúscula",                     # [V]
    "\u0057": "uve doble mayúscula",             # [W] — comment. : "uve doble" o "doble ve" según región
    "\u0058": "x mayúscula",                     # [X]
    "\u0059": "i griega mayúscula",              # [Y]
    "\u005a": "z mayúscula",                     # [Z]

    # ==================================================================
    # 4. LETRAS MINÚSCULAS
    # ==================================================================
    "\u0061": "a",                               # [a]
    "\u0062": "b",                               # [b]
    "\u0063": "c",                               # [c]
    "\u0064": "d",                               # [d]
    "\u0065": "e",                               # [e]
    "\u0066": "f",                               # [f]
    "\u0067": "g",                               # [g]
    "\u0068": "h",                               # [h]
    "\u0069": "i",                               # [i]
    "\u006a": "j",                               # [j]
    "\u006b": "k",                               # [k]
    "\u006c": "l",                               # [l]
    "\u006d": "m",                               # [m]
    "\u006e": "n",                               # [n]
    "\u006f": "o",                               # [o]
    "\u0070": "p",                               # [p]
    "\u0071": "q",                               # [q]
    "\u0072": "r",                               # [r]
    "\u0073": "s",                               # [s]
    "\u0074": "t",                               # [t]
    "\u0075": "u",                               # [u]
    "\u0076": "v",                               # [v]
    "\u0077": "uve doble",                       # [w]
    "\u0078": "x",                               # [x]
    "\u0079": "i griega",                        # [y]
    "\u007a": "z",                               # [z]

    # ==================================================================
    # 5. PUNTUACIÓN
    # Los signos ¿ y ¡ son exclusivos del español (y del gallego).
    # Se abren y se cierran: ¿...? ¡...!
    # ==================================================================
    "\u00bf": "signo de apertura de interrogación",  # [¿]
    "\u00a1": "signo de apertura de exclamación",    # [¡]
    "\u002c": "coma",                            # [,]
    "\u002e": "punto",                           # [.]
    "\u003b": "punto y coma",                    # [;]
    "\u003a": "dos puntos",                      # [:]
    "\u003f": "signo de cierre de interrogación",    # [?] — comment. : "cierra" la apertura ¿
    "\u0021": "signo de cierre de exclamación",      # [!] — comment. : "cierra" la apertura ¡
    "\u2026": "puntos suspensivos",              # […]
    "\u0028": "paréntesis de apertura",          # [(]
    "\u0029": "paréntesis de cierre",            # [)]
    "\u005b": "corchete de apertura",            # [[]]
    "\u005d": "corchete de cierre",              # []]
    "\u007b": "llave de apertura",               # [{]
    "\u007d": "llave de cierre",                 # [}]
    "\u00b7": "punto medio",                     # [·]
    "\u2030": "por mil",                         # [‰]
    "\u00a4": "símbolo monetario",                # [¤]

    # ==================================================================
    # 6. APÓSTROFOS Y COMILLAS
    # El español no usa apóstrofo en palabras propias, pero aparece
    # en extranjerismos y textos importados.
    # ==================================================================
    "\u0027": "apóstrofo",                       # ['] recto
    "\u2019": "apóstrofo",                       # [’] tipográfico — comment. : mismo valor
    "\u02bc": "apóstrofo",                       # [ʼ] apóstrofo letra — comment. : mismo valor
    "\u0060": "apóstrofo",                       # [`] acento grave — comment. : mismo valor

    # ==================================================================
    # 7. COMILLAS (distinción apertura / cierre)
    # Las comillas latinas «» (comillas angulares) son las tradicionales
    # del español; las inglesas “” son las más frecuentes hoy.
    # ==================================================================
    "\u00ab": "comillas de apertura",           # [«] comillas angulares
    "\u00bb": "comillas de cierre",              # [»]
    "\u201c": "comillas de apertura",           # [“] comillas inglesas
    "\u201d": "comillas de cierre",             # [”]
    "\u201e": "comillas de apertura",           # [„] comillas alemanas — comment. : raro en español
    "\u201f": "comillas de apertura",           # [‟] — comment. : raro
    "\u0022": "comillas de apertura",           # ["] rectas — comment. : apertura o cierre según contexto
    "\u2018": "comillas de apertura",          # [‘] comillas simples
    "\u201b": "comillas de apertura",           # [‛] — comment. : raro
    "\u201a": "comillas de apertura",           # [‚]
    "\u2039": "comillas de apertura",           # [‹] comillas angulares simples
    "\u203a": "comillas de cierre",             # [›]

    # ==================================================================
    # 8. GUIONES Y BARRAS
    # El guion (hyphen-minus) es polivalente : valor "guion" (uso dominante).
    # Rayas (—) y viñetas comparten el valor "raya".
    # ==================================================================
    "\u002d": "guion",                          # [-] guion-menos (teclado) — comment. : uso dominante
    "\u2010": "guion",                          # [‐] — comment. : mismo valor
    "\u2011": "guion",                          # [‑] guion de no separación — comment. : mismo valor
    "\ufe63": "guion",                          # [﹣] — comment. : mismo valor
    "\uff0d": "guion",                          # [－] ancho completo — comment. : mismo valor
    "\u2012": "raya",                           # [‒] guion de cifras
    "\u2013": "raya",                           # [–] raja o semirraya — comment. : "raya menor"
    "\u2014": "raya",                            # [—] raya
    "\u2015": "raya",                           # [―] barra horizontal
    "\u2212": "menos",                          # [−] signo menos matemático
    "\u2022": "raya",                           # [•] viñeta — comment. : leída como viñeta de lista
    "\u2023": "raya",                           # [‣] viñeta triangular — comment. : ídem
    "\u002f": "barra",                          # [/] barra oblicua
    "\u005c": "barra invertida",                # [\]
    "\u007c": "barra vertical",                 # [|]
    "\u005f": "guion bajo",                     # [_]

    # ==================================================================
    # 9. SÍMBOLOS Y SIGNOS
    # ==================================================================
    "\u20ac": "euro",                           # [€]
    "\u0024": "dólar",                          # [$]
    "\u00a3": "libra",                          # [£]
    "\u00a2": "centavo",                        # [¢]
    "\u0023": "almuadilla",                     # [#] — comment. : "almuadilla" (RAE) o "numeral"
    "\u002a": "asterisco",                      # [*]
    "\u0040": "arroba",                         # [@]
    "\u0026": "et",                             # [&] — comment. : "et" o "ampersand"
    "\u0025": "por ciento",                     # [%]
    "\u002b": "más",                            # [+]
    "\u003d": "igual",                          # [=]
    "\u003c": "menor que",                      # [<]
    "\u003e": "mayor que",                      # [>]
    "\u005e": "circunflejo",                    # [^]
    "\u007e": "virgulilla",                     # [~] — comment. : también "tilde de la ñ" en español
    "\u00b0": "grado",                          # [°]
    "\u00a7": "párrafo",                        # [§]
    "\u00b6": "párrafo",                        # [¶] calderón — comment. : mismo valor que §
    "\u2020": "obelisco",                       # [†]
    "\u2021": "doble obelisco",                 # [‡]
    "\u00a9": "copyright",                      # [©]
    "\u00ae": "marca registrada",               # [®]
    "\u2122": "marca registrada",               # [™] — comment. : mismo valor que ®
    "\u00d7": "multiplicado por",               # [×]
    "\u00f7": "dividido por",                   # [÷]
    "\u2260": "distinto de",                    # [≠]
    "\u2264": "menor o igual que",              # [≤]
    "\u2265": "mayor o igual que",              # [≥]

    # ==================================================================
    # 10. ESPACIOS (categoría Zs únicamente)
    # Todas las anchuras comparten el valor "espacio".
    # ==================================================================
    "\u0020": "espacio",                        # [ ] espacio normal
    "\u00a0": "espacio",                        # [ ] de no separación — comment. : mismo valor
    "\u202f": "espacio",                        # [ ] estrecho de no separación — comment. : mismo valor
    "\u2009": "espacio",                        # [ ] fino — comment. : mismo valor
    "\u2007": "espacio",                        # [ ] de no separación de cifras — comment. : mismo valor
    "\u2008": "espacio",                        # [ ] de puntuación — comment. : mismo valor
    "\u200a": "espacio",                        # [ ] extrafino — comment. : mismo valor

    # ==================================================================
    # 11. ESPECIAL : categorías Zp, Zl y C (control y formato)
    # Zp = separador de párrafo, Zl = separador de línea,
    # C  = control (Cc), formato (Cf), uso privado (Co), sin asignar (Cn).
    # ==================================================================
    # --- Zp y Zl ---
    "\u2029": "espacio",                        # [ ] separador de párrafo — comment. : leído como espacio
    "\u2028": "espacio",                        # [ ] separador de línea — comment. : leído como espacio

    # --- Cc : caracteres de control ---
    "\u0009": "espacio",                        # [ ] tabulación — comment. : leído como espacio
    "\u000a": "espacio",                        # [ ] salto de línea (LF) — comment. : leído como espacio
    "\u000b": "espacio",                        # [ ] tabulación vertical — comment. : ídem
    "\u000c": "espacio",                        # [ ] salto de página (FF) — comment. : ídem
    "\u000d": "espacio",                        # [ ] retorno de carro (CR) — comment. : ídem
    "\u0000": "",                              # [ ] NUL — comment. : ignorado
    "\u0001": "",                              # [ ] SOH — comment. : ignorado
    "\u0002": "",                              # [ ] STX — comment. : ignorado
    "\u0003": "",                              # [ ] ETX — comment. : ignorado
    "\u0004": "",                              # [ ] EOT — comment. : ignorado
    "\u0005": "",                              # [ ] ENQ — comment. : ignorado
    "\u0006": "",                              # [ ] ACK — comment. : ignorado
    "\u0007": "",                              # [ ] BEL — comment. : ignorado
    "\u0008": "",                              # [ ] retroceso (BS) — comment. : ignorado
    "\u000e": "",                              # [ ] Shift In — comment. : ignorado
    "\u000f": "",                              # [ ] Shift Out — comment. : ignorado
    "\u0010": "",                              # [ ] DLE — comment. : ignorado
    "\u0011": "",                              # [ ] DC1 — comment. : ignorado
    "\u0012": "",                              # [ ] DC2 — comment. : ignorado
    "\u0013": "",                              # [ ] DC3 — comment. : ignorado
    "\u0014": "",                              # [ ] DC4 — comment. : ignorado
    "\u0015": "",                              # [ ] NAK — comment. : ignorado
    "\u0016": "",                              # [ ] SYN — comment. : ignorado
    "\u0017": "",                              # [ ] ETB — comment. : ignorado
    "\u0018": "",                              # [ ] CAN — comment. : ignorado
    "\u0019": "",                              # [ ] EM — comment. : ignorado
    "\u001a": "",                              # [ ] SUB — comment. : ignorado
    "\u001b": "",                              # [ ] Escape — comment. : ignorado
    "\u001c": "",                              # [ ] separador de archivo — comment. : ignorado
    "\u001d": "",                              # [ ] separador de grupo — comment. : ignorado
    "\u001e": "",                              # [ ] separador de registro — comment. : ignorado
    "\u001f": "",                              # [ ] separador de unidad — comment. : ignorado
    "\u007f": "",                              # [ ] DEL — comment. : ignorado

    # --- Cf : caracteres de formato (invisibles) ---
    "\u00ad": "",                              # [­] guion suave (SOFT HYPHEN) — comment. : ignorado
    "\u200b": "",                              # [​] espacio de anchura cero — comment. : ignorado
    "\u200c": "",                              # [‌] ZWNJ — comment. : ignorado
    "\u200d": "",                              # [‍] ZWJ — comment. : ignorado
    "\u200e": "",                              # [‎] marca izquierda-derecha (LRM) — comment. : ignorado
    "\u200f": "",                              # [‏] marca derecha-izquierda (RLM) — comment. : ignorado
    "\u202a": "",                              # [‎] inicio LRE — comment. : ignorado
    "\u202b": "",                              # [‏] inicio RLE — comment. : ignorado
    "\u202c": "",                              # [‬] fin direccional (PDF) — comment. : ignorado
    "\u202d": "",                              # [‎] inicio LRO — comment. : ignorado
    "\u202e": "",                              # [‏] inicio RLO — comment. : ignorado
    "\u2060": "",                              # [⁠] ligadura de anchura cero (WJ) — comment. : ignorado
    "\ufeff": "",                              # [﻿] BOM — comment. : ignorado

    # --- Co y Cn : no enumerables, tratar con fallback
}
"""
                       _       _
     /\               | |     (_)
    /  \   _ __   __ _| | __ _ _ ___
   / /\ \ | '_ \ / _` | |/ _` | / __|
  / ____ \| | | | (_| | | (_| | \__ \
 /_/    \_\_| |_|\__, |_|\__,_|_|___/
                  __/ |
                 |___/
"""





epel_tts_en = {
    # ==================================================================
    # 1. ACCENTED LETTERS
    # English orthography uses no accented letters. This section is
    # intentionally empty: keep the structure, add nothing.
    # ==================================================================

    # ==================================================================
    # 2. SPECIAL LETTERS
    # English has no ñ, no ligatures in native spelling. Rare names
    # keep æ/œ (encyclopædia, cœur borrowed); included for coverage.
    # ==================================================================
    "\u00e6": "ash",                             # [æ] — comment. : ligature, foreign/legacy words only
    "\u00c6": "capital ash",                     # [Æ] — comment. : same coverage
    "\u0153": "ethel",                           # [œ] — comment. : foreign words only
    "\u0152": "capital ethel",                   # [Œ] — comment. : same coverage

    # ==================================================================
    # 3. CAPITAL LETTERS
    # Spoken spelling: "capital A", "capital B", etc.
    # ==================================================================
    "\u0041": "capital a",                       # [A]
    "\u0042": "capital b",                       # [B]
    "\u0043": "capital c",                       # [C]
    "\u0044": "capital d",                       # [D]
    "\u0045": "capital e",                       # [E]
    "\u0046": "capital f",                       # [F]
    "\u0047": "capital g",                       # [G]
    "\u0048": "capital h",                       # [H]
    "\u0049": "capital i",                       # [I]
    "\u004a": "capital j",                       # [J]
    "\u004b": "capital k",                       # [K]
    "\u004c": "capital l",                       # [L]
    "\u0058": "capital x",                       # [X]
    "\u004d": "capital m",                       # [M]
    "\u004e": "capital n",                       # [N]
    "\u004f": "capital o",                       # [O]
    "\u0050": "capital p",                       # [P]
    "\u0051": "capital q",                       # [Q]
    "\u0052": "capital r",                       # [R]
    "\u0053": "capital s",                       # [S]
    "\u0054": "capital t",                       # [T]
    "\u0055": "capital u",                       # [U]
    "\u0056": "capital v",                       # [V]
    "\u0057": "capital double u",                # [W] — comment. : on épelle "capital double-u"
    "\u0059": "capital y",                       # [Y]
    "\u005a": "capital z",                       # [Z] — comment. : "zed" (UK) / "zee" (US)

    # ==================================================================
    # 4. LOWERCASE LETTERS
    # Spoken spelling: just the letter name, no "lowercase" prefix.
    # ==================================================================
    "\u0061": "a",                               # [a]
    "\u0062": "b",                               # [b]
    "\u0063": "c",                               # [c]
    "\u0064": "d",                               # [d]
    "\u0065": "e",                               # [e]
    "\u0066": "f",                               # [f]
    "\u0067": "g",                               # [g]
    "\u0068": "h",                               # [h]
    "\u0069": "i",                               # [i]
    "\u006a": "j",                               # [j]
    "\u006b": "k",                               # [k]
    "\u006c": "l",                               # [l]
    "\u006d": "m",                               # [m]
    "\u006e": "n",                               # [n]
    "\u006f": "o",                               # [o]
    "\u0070": "p",                               # [p]
    "\u0071": "q",                               # [q]
    "\u0072": "r",                               # [r]
    "\u0073": "s",                               # [s]
    "\u0074": "t",                               # [t]
    "\u0075": "u",                               # [u]
    "\u0076": "v",                               # [v]
    "\u0077": "double u",                        # [w]
    "\u0078": "x",                               # [x]
    "\u0079": "y",                               # [y]
    "\u007a": "z",                               # [z] — comment. : "zed" (UK) / "zee" (US)

    # ==================================================================
    # 5. PUNCTUATION
    # English uses no inverted opening signs: ? and ! open directly.
    # ==================================================================
    "\u002c": "comma",                            # [,]
    "\u002e": "full stop",                        # [.]
    "\u003b": "semicolon",                        # [;]
    "\u003a": "colon",                            # [:]
    "\u003f": "question mark",                    # [?]
    "\u0021": "exclamation mark",                 # [!]
    "\u2026": "ellipsis",                         # […]
    "\u0028": "open parenthesis",                 # [(]
    "\u0029": "close parenthesis",                # [)]
    "\u005b": "open bracket",                      # [[]]
    "\u005d": "close bracket",                    # []]
    "\u007b": "open brace",                       # [{]
    "\u007d": "close brace",                      # [}]
    "\u00b7": "middle dot",                       # [·]
    "\u2030": "per mille",                        # [‰]
    "\u00a4": "currency sign",                    # [¤]

    # ==================================================================
    # 6. APOSTROPHES
    # The apostrophe is essential in English (contractions, possessives).
    # All three forms share the value "apostrophe".
    # ==================================================================
    "\u0027": "apostrophe",                       # ['] straight (keyboard)
    "\u2019": "apostrophe",                       # [’] typographic — comment. : same value
    "\u02bc": "apostrophe",                       # [ʼ] letter apostrophe — comment. : same value
    "\u0060": "apostrophe",                       # [`] backtick misused — comment. : same value

    # ==================================================================
    # 7. QUOTATION MARKS (opening / closing distinction)
    # “ ” are the standard English pair; « » appear in UK typography.
    # ==================================================================
    "\u201c": "open quotation mark",              # [“] double, opening
    "\u201d": "close quotation mark",             # [”] double, closing
    "\u2018": "open quotation mark",              # [‘] single, opening
    "\u2019": "close quotation mark",             # [’] — comment. : same codepoint as the apostrophe; also closes single quotes
    "\u0022": "open quotation mark",              # ["] straight — comment. : opening or closing depending on context
    "\u00ab": "open quotation mark",              # [«] guillemets — comment. : used in some UK styles, same value
    "\u00bb": "close quotation mark",             # [»] — comment. : same value
    "\u201e": "open quotation mark",              # [„] — comment. : rare, imported
    "\u201f": "open quotation mark",              # [‟] — comment. : rare
    "\u201b": "open quotation mark",              # [‛] — comment. : rare
    "\u201a": "open quotation mark",              # [‚] — comment. : rare
    "\u2039": "open quotation mark",              # [‹] single guillemet — comment. : rare
    "\u203a": "close quotation mark",             # [›] single guillemet — comment. : same value

    # ==================================================================
    # 8. DASHES AND BARS
    # The keyboard hyphen-minus is polyvalent: value "hyphen" (dominant use).
    # En dash, em dash and bullets share the value "dash".
    # ==================================================================
    "\u002d": "hyphen",                           # [-] hyphen-minus (keyboard) — comment. : dominant use
    "\u2010": "hyphen",                          # [‐] true hyphen — comment. : same value
    "\u2011": "hyphen",                          # [‑] non-breaking hyphen — comment. : same value
    "\ufe63": "hyphen",                          # [﹣] small variant — comment. : same value
    "\uff0d": "hyphen",                          # [－] fullwidth — comment. : same value
    "\u2012": "dash",                            # [‒] figure dash
    "\u2013": "dash",                            # [–] en dash
    "\u2014": "dash",                            # [—] em dash
    "\u2015": "dash",                            # [―] horizontal bar
    "\u2212": "minus",                           # [−] mathematical minus sign
    "\u2022": "dash",                            # [•] bullet — comment. : read as a list dash
    "\u2023": "dash",                            # [‣] triangular bullet — comment. : same value
    "\u002f": "slash",                           # [/] — comment. : "slash" (UK: "oblique", "stroke")
    "\u005c": "backslash",                       # [\]
    "\u007c": "vertical bar",                    # [|] — comment. : also "pipe"
    "\u005f": "underscore",                      # [_]

    # ==================================================================
    # 9. SYMBOLS AND SIGNS
    # ==================================================================
    "\u0024": "dollar sign",                      # [$]
    "\u00a3": "pound sign",                      # [£]
    "\u20ac": "euro sign",                       # [€]
    "\u00a2": "cent sign",                        # [¢]
    "\u0023": "hash sign",                       # [#] — comment. : "hash" (UK) / "pound" / "number sign" (US)
    "\u002a": "asterisk",                         # [*]
    "\u0040": "at sign",                          # [@]
    "\u0026": "ampersand",                       # [&]
    "\u0025": "percent sign",                     # [%]
    "\u002b": "plus sign",                       # [+]
    "\u003d": "equals sign",                      # [=]
    "\u003c": "less-than sign",                  # [<]
    "\u003e": "greater-than sign",               # [>]
    "\u005e": "caret",                            # [^]
    "\u007e": "tilde",                           # [~]
    "\u00b0": "degree sign",                     # [°]
    "\u00a7": "section sign",                    # [§]
    "\u00b6": "pilcrow",                         # [¶] — comment. : same function as §, distinct name in English
    "\u2020": "dagger",                          # [†]
    "\u2021": "double dagger",                   # [‡]
    "\u00a9": "copyright sign",                  # [©]
    "\u00ae": "registered sign",                 # [®]
    "\u2122": "trademark sign",                  # [™] — comment. : same function as ®
    "\u00d7": "multiplication sign",             # [×]
    "\u00f7": "division sign",                   # [÷]
    "\u2260": "not equal to",                     # [≠]
    "\u2264": "less than or equal to",            # [≤]
    "\u2265": "greater than or equal to",         # [≥]

    # ==================================================================
    # 10. SPACES (Zs category only)
    # All widths share the value "space".
    # ==================================================================
    "\u0020": "space",                            # [ ] ordinary space
    "\u00a0": "space",                            # [ ] no-break space — comment. : same value
    "\u202f": "space",                            # [ ] narrow no-break space — comment. : same value
    "\u2009": "space",                            # [ ] thin space — comment. : same value
    "\u2007": "space",                            # [ ] figure space — comment. : same value
    "\u2008": "space",                            # [ ] punctuation space — comment. : same value
    "\u200a": "space",                            # [ ] hair space — comment. : same value

    # ==================================================================
    # 11. SPECIAL: Zp, Zl and C categories (control and format)
    # Zp = paragraph separator, Zl = line separator,
    # C  = control (Cc), format (Cf), private use (Co), unassigned (Cn).
    # ==================================================================
    # --- Zp and Zl ---
    "\u2029": "space",                            # [ ] paragraph separator — comment. : read as a space
    "\u2028": "space",                            # [ ] line separator — comment. : read as a space

    # --- Cc: control characters ---
    "\u0009": "space",                            # [ ] tab — comment. : read as a space
    "\u000a": "space",                            # [ ] line feed (LF) — comment. : read as a space
    "\u000b": "space",                            # [ ] vertical tab — comment. : same value
    "\u000c": "space",                            # [ ] form feed (FF) — comment. : same value
    "\u000d": "space",                            # [ ] carriage return (CR) — comment. : same value
    "\u0000": "",                                 # [ ] NUL — comment. : ignored
    "\u0001": "",                                 # [ ] SOH — comment. : ignored
    "\u0002": "",                                 # [ ] STX — comment. : ignored
    "\u0003": "",                                 # [ ] ETX — comment. : ignored
    "\u0004": "",                                 # [ ] EOT — comment. : ignored
    "\u0005": "",                                 # [ ] ENQ — comment. : ignored
    "\u0006": "",                                 # [ ] ACK — comment. : ignored
    "\u0007": "",                                 # [ ] BEL — comment. : ignored
    "\u0008": "",                                 # [ ] backspace (BS) — comment. : ignored
    "\u000e": "",                                 # [ ] Shift In — comment. : ignored
    "\u000f": "",                                 # [ ] Shift Out — comment. : ignored
    "\u0010": "",                                 # [ ] DLE — comment. : ignored
    "\u0011": "",                                 # [ ] DC1 — comment. : ignored
    "\u0012": "",                                 # [ ] DC2 — comment. : ignored
    "\u0013": "",                                 # [ ] DC3 — comment. : ignored
    "\u0014": "",                                 # [ ] DC4 — comment. : ignored
    "\u0015": "",                                 # [ ] NAK — comment. : ignored
    "\u0016": "",                                 # [ ] SYN — comment. : ignored
    "\u0017": "",                                 # [ ] ETB — comment. : ignored
    "\u0018": "",                                 # [ ] CAN — comment. : ignored
    "\u0019": "",                                 # [ ] EM — comment. : ignored
    "\u001a": "",                                 # [ ] SUB — comment. : ignored
    "\u001b": "",                                 # [ ] Escape — comment. : ignored
    "\u001c": "",                                 # [ ] file separator — comment. : ignored
    "\u001d": "",                                 # [ ] group separator — comment. : ignored
    "\u001e": "",                                 # [ ] record separator — comment. : ignored
    "\u001f": "",                                 # [ ] unit separator — comment. : ignored
    "\u007f": "",                                 # [ ] DEL — comment. : ignored

    # --- Cf: format characters (invisible) ---
    "\u00ad": "",                                 # [­] soft hyphen — comment. : ignored
    "\u200b": "",                                 # [​] zero-width space — comment. : ignored
    "\u200c": "",                                 # [‌] ZWNJ — comment. : ignored
    "\u200d": "",                                 # [‍] ZWJ — comment. : ignored
    "\u200e": "",                                 # [‎] LRM — comment. : ignored
    "\u200f": "",                                 # [‏] RLM — comment. : ignored
    "\u202a": "",                                 # [‎] LRE — comment. : ignored
    "\u202b": "",                                 # [‏] RLE — comment. : ignored
    "\u202c": "",                                 # [‬] PDF — comment. : ignored
    "\u202d": "",                                 # [‎] LRO — comment. : ignored
    "\u202e": "",                                 # [‏] RLO — comment. : ignored
    "\u2060": "",                                 # [⁠] word joiner — comment. : ignored
    "\ufeff": "",                                 # [﻿] BOM — comment. : ignored

    # --- Co and Cn: not enumerable, handle with fallback
}


"""
  _____           _                     _
 |  __ \         | |                   (_)
 | |__) |__  _ __| |_ _   _  __ _  __ _ _ ___
 |  ___/ _ \| '__| __| | | |/ _` |/ _` | / __|
 | |  | (_) | |  | |_| |_| | (_| | (_| | \__ \
 |_|   \___/|_|   \__|\__,_|\__, |\__,_|_|___/
                             __/ |
                            |___/
"""


epel_tts_pt = {
    # ==================================================================
    # 1. LETRAS ACENTUADAS (minúsculas e maiúsculas)
    # ==================================================================
    "\u00e1": "a minúsculo com acento agudo",          # [á]
    "\u00c1": "a maiúsculo com acento agudo",          # [Á]
    "\u00e0": "a minúsculo com acento grave",          # [à]
    "\u00c0": "a maiúsculo com acento grave",          # [À]
    "\u00e2": "a minúsculo com acento circunflexo",    # [â]
    "\u00c2": "a maiúsculo com acento circunflexo",    # [Â]
    "\u00e3": "a minúsculo com til",                   # [ã]
    "\u00c3": "a maiúsculo com til",                   # [Ã]
    "\u00e9": "e minúsculo com acento agudo",          # [é]
    "\u00c9": "e maiúsculo com acento agudo",          # [É]
    "\u00ea": "e minúsculo com acento circunflexo",    # [ê]
    "\u00ca": "e maiúsculo com acento circunflexo",    # [Ê]
    "\u00ed": "i minúsculo com acento agudo",          # [í]
    "\u00cd": "i maiúsculo com acento agudo",          # [Í]
    "\u00f3": "o minúsculo com acento agudo",          # [ó]
    "\u00d3": "o maiúsculo com acento agudo",          # [Ó]
    "\u00f4": "o minúsculo com acento circunflexo",    # [ô]
    "\u00d4": "o maiúsculo com acento circunflexo",    # [Ô]
    "\u00f5": "o minúsculo com til",                   # [õ]
    "\u00d5": "o maiúsculo com til",                   # [Õ]
    "\u00fa": "u minúsculo com acento agudo",          # [ú]
    "\u00da": "u maiúsculo com acento agudo",          # [Ú]
    "\u00fc": "u minúsculo com trema",                 # [ü]
    "\u00dc": "u maiúsculo com trema",                 # [Ü]
    "\u00e7": "c cedilha minúsculo",                   # [ç]
    "\u00c7": "c cedilha maiúsculo",                   # [Ç]

    # ==================================================================
    # 2. LETRAS MAIÚSCULAS (básicas)
    # ==================================================================
    "\u0041": "a maiúsculo",                           # [A]
    "\u0042": "bê maiúsculo",                          # [B]
    "\u0043": "cê maiúsculo",                          # [C]
    "\u0044": "dê maiúsculo",                          # [D]
    "\u0045": "e maiúsculo",                           # [E]
    "\u0046": "efe maiúsculo",                         # [F]
    "\u0047": "gê maiúsculo",                          # [G]
    "\u0048": "agá maiúsculo",                         # [H]
    "\u0049": "i maiúsculo",                           # [I]
    "\u004a": "jota maiúsculo",                        # [J]
    "\u004b": "cá maiúsculo",                          # [K]
    "\u004c": "ele maiúsculo",                         # [L]
    "\u004d": "eme maiúsculo",                         # [M]
    "\u004e": "ene maiúsculo",                         # [N]
    "\u004f": "o maiúsculo",                           # [O]
    "\u0050": "pê maiúsculo",                          # [P]
    "\u0051": "quê maiúsculo",                         # [Q]
    "\u0052": "erre maiúsculo",                        # [R]
    "\u0053": "esse maiúsculo",                        # [S]
    "\u0054": "tê maiúsculo",                          # [T]
    "\u0055": "u maiúsculo",                           # [U]
    "\u0056": "vê maiúsculo",                          # [V]
    "\u0057": "dáblio maiúsculo",                      # [W]
    "\u0058": "xis maiúsculo",                         # [X]
    "\u0059": "ípsilon maiúsculo",                     # [Y]
    "\u005a": "zê maiúsculo",                          # [Z]

    # ==================================================================
    # 3. LETRAS MINÚSCULAS (básicas)
    # ==================================================================
    "\u0061": "a",                                     # [a]
    "\u0062": "bê",                                    # [b]
    "\u0063": "cê",                                    # [c]
    "\u0064": "dê",                                    # [d]
    "\u0065": "e",                                     # [e]
    "\u0066": "efe",                                   # [f]
    "\u0067": "gê",                                    # [g]
    "\u0068": "agá",                                   # [h]
    "\u0069": "i",                                     # [i]
    "\u006a": "jota",                                  # [j]
    "\u006b": "cá",                                    # [k]
    "\u006c": "ele",                                   # [l]
    "\u006d": "eme",                                   # [m]
    "\u006e": "ene",                                   # [n]
    "\u006f": "o",                                     # [o]
    "\u0070": "pê",                                    # [p]
    "\u0071": "quê",                                   # [q]
    "\u0072": "erre",                                  # [r]
    "\u0073": "esse",                                  # [s]
    "\u0074": "tê",                                    # [t]
    "\u0075": "u",                                     # [u]
    "\u0076": "vê",                                    # [v]
    "\u0077": "dáblio",                                # [w]
    "\u0078": "xis",                                   # [x]
    "\u0079": "ípsilon",                               # [y]
    "\u007a": "zê",                                    # [z]

    # ==================================================================
    # 4. PONTUAÇÃO
    # ==================================================================
    "\u002c": "vírgula",                               # [,]
    "\u002e": "ponto",                                 # [.]
    "\u003b": "ponto e vírgula",                        # [;]
    "\u003a": "dois pontos",                            # [:]
    "\u003f": "ponto de interrogação",                  # [?]
    "\u0021": "ponto de exclamação",                   # [!]
    "\u2026": "reticências",                           # […]  (reticências = points de suspension)
    "\u0028": "abre parênteses",                       # [(]
    "\u0029": "fecha parênteses",                      # [)]
    "\u005b": "abre colchetes",                        # [[]
    "\u005d": "fecha colchetes",                       # []]
    "\u007b": "abre chaves",                           # [{]
    "\u007d": "fecha chaves",                          # [}]
    "\u00b7": "ponto médio",                           # [·]
    "\u2030": "por mil",                               # [‰]
    "\u00a1": "ponto de exclamação invertido",         # [¡]
    "\u00bf": "ponto de interrogação invertido",       # [¿]

    # ==================================================================
    # 5. APÓSTROFOS
    # As quatro formas partilham o valor "apóstrofo" (mesma pronúncia).
    # ==================================================================
    "\u0027": "apóstrofo",                             # ['] apóstrofo reto (tecla)
    "\u2019": "apóstrofo",                             # [’] tipográfico — mesmo valor
    "\u02bc": "apóstrofo",                             # [ʼ] apóstrofo letra — mesmo valor
    "\u0060": "apóstrofo",                             # [`] acento grave desviado — mesmo valor

    # ==================================================================
    # 6. ASPAS / GUILLEMETS (distinção abre / fecha)
    # Cada par tipográfico partilha o seu valor.
    # ==================================================================
    "\u00ab": "abre aspas",                            # [«] chevron — aspas angulares
    "\u00bb": "fecha aspas",                           # [»]
    "\u201c": "abre aspas",                            # [“] vírgula dupla alta
    "\u201d": "fecha aspas",                           # [”]
    "\u201e": "abre aspas",                            # [„] vírgula dupla baixa
    "\u201f": "abre aspas",                            # [‟] vírgula dupla alta invertida (raro)
    "\u0022": "aspas",                                 # ["] reto — abre/fecha conforme contexto
    "\u2018": "abre aspas",                            # [‘] vírgula simples alta
    "\u201b": "abre aspas",                            # [‛] vírgula simples alta invertida (raro)
    "\u201a": "vírgula",                               # [‚] vírgula simples baixa
    "\u2039": "abre aspas",                            # [‹] chevron simples
    "\u203a": "fecha aspas",                           # [›]

    # ==================================================================
    # 7. TRAÇOS E BARRAS
    # Hífen é polivalente: valor "hífen" (uso dominante).
    # Meia-quadratina, quadratina e marcadores partilham o valor "traço".
    # ==================================================================
    "\u002d": "hífen",                                 # [-] hífen (tecla) — uso dominante
    "\u2010": "hífen",                                 # [‐] — mesmo valor
    "\u2011": "hífen",                                 # [‑] hífen não quebrável — mesmo valor
    "\ufe63": "hífen",                                 # [﹣] pequena variante — mesmo valor
    "\uff0d": "hífen",                                 # [－] largura total — mesmo valor
    "\u2012": "traço",                                 # [‒] traço de algarismos
    "\u2013": "traço",                                 # [–] meia-quadratina (travessão curto)
    "\u2014": "traço",                                 # [—] quadratina (travessão longo)
    "\u2015": "traço",                                 # [―] barra horizontal
    "\u2212": "sinal de menos",                        # [−] sinal matemático de menos
    "\u2022": "traço",                                 # [•] marcador — lido como traço de lista
    "\u2023": "traço",                                 # [‣] marcador triangular — idem
    "\u002f": "barra",                                 # [/]
    "\u005c": "barra invertida",                       # [\]
    "\u007c": "barra vertical",                        # [|]
    "\u005f": "traço baixo",                           # [_]  (sublinhado / underscore)

    # ==================================================================
    # 8. SÍMBOLOS E SIGNOS
    # ==================================================================
    "\u20ac": "euro",                                  # [€]
    "\u0024": "dólar",                                 # [$]
    "\u00a3": "libra",                                 # [£]
    "\u00a2": "centavo",                               # [¢]
    "\u0023": "cerquilha",                             # [#]  (tralha / cardinal / cerquilha)
    "\u002a": "asterisco",                             # [*]
    "\u0040": "arroba",                                # [@]
    "\u0026": "e comercial",                           # [&]
    "\u0025": "por cento",                             # [%]
    "\u002b": "mais",                                  # [+]
    "\u003d": "igual",                                 # [=]
    "\u003c": "menor que",                              # [<]
    "\u003e": "maior que",                              # [>]
    "\u005e": "acento circunflexo",                    # [^]
    "\u007e": "til",                                   # [~]
    "\u00b0": "grau",                                  # [°]
    "\u00a7": "parágrafo",                             # [§]
    "\u00b6": "parágrafo",                             # [¶]  (parágrafo / pilcrow — mesmo valor que §)
    "\u2020": "obelisco",                              # [†]  (adaga / obelisco)
    "\u2021": "obelisco duplo",                        # [‡]
    "\u00a9": "direitos de autor",                     # [©]  (copyright)
    "\u00ae": "marca registada",                       # [®]
    "\u2122": "marca registada",                       # [™]  — mesmo valor que ®
    "\u00d7": "vezes",                                 # [×]  (multiplicado por)
    "\u00f7": "dividido por",                          # [÷]
    "\u2260": "diferente de",                          # [≠]
    "\u2264": "menor ou igual",                        # [≤]
    "\u2265": "maior ou igual",                        # [≥]

    # ==================================================================
    # 9. ESPAÇOS (categoria Zs apenas)
    # Todas as larguras partilham o valor "espaço" (mesma pronúncia).
    # ==================================================================
    "\u0020": "espaço",                                # [ ] espaço normal
    "\u00a0": "espaço",                                # [ ] espaço não quebrável — mesmo valor
    "\u202f": "espaço",                                # [ ] espaço fino não quebrável — mesmo valor
    "\u2009": "espaço",                                # [ ] espaço fino — mesmo valor
    "\u2007": "espaço",                                # [ ] espaço não quebrável de algarismos — mesmo valor
    "\u2008": "espaço",                                # [ ] espaço de pontuação — mesmo valor
    "\u200a": "espaço",                                # [ ] espaço ultrafino — mesmo valor

    # ==================================================================
    # 10. ESPECIAL: categorias Zp, Zl e C (controlo e formato)
    # --> Para testes: Incompatíveis com códigos QR
    # Zp = Paragraph Separator, Zl = Line Separator,
    # C  = Control (Cc), Format (Cf), Private Use (Co), Unassigned (Cn).
    # Estes caracteres são invisíveis ou estruturais: ou são
    # renderizados como um espaço/salto, ou ignorados (valor vazio).
    # ==================================================================
    # --- Zp e Zl (separadores de zona) ---
    "\u2029": "espaço",                                # [ ] separador de parágrafo — renderizado como espaço
    "\u2028": "espaço",                                # [ ] separador de linha — renderizado como espaço

    # --- Cc : caracteres de controlo (pontuais) ---
    "\u0009": "espaço",                                # [ ] tabulação horizontal — renderizado como espaço
    "\u000a": "espaço",                                # [ ] mudança de linha (LF) — renderizado como espaço
    "\u000b": "espaço",                                # [ ] tabulação vertical — idem
    "\u000c": "espaço",                                # [ ] mudança de página (FF) — idem
    "\u000d": "espaço",                                # [ ] retorno de carro (CR) — idem
    "\u0000": "",                                      # [ ] NUL — ignorado
    "\u0001": "",                                      # [ ] SOH — ignorado
    "\u0002": "",                                      # [ ] STX — ignorado
    "\u0003": "",                                      # [ ] ETX — ignorado
    "\u0004": "",                                      # [ ] EOT — ignorado
    "\u0005": "",                                      # [ ] ENQ — ignorado
    "\u0006": "",                                      # [ ] ACK — ignorado
    "\u0007": "",                                      # [ ] BEL — ignorado
    "\u0008": "",                                      # [ ] backspace (BS) — ignorado
    "\u000e": "",                                      # [ ] Shift In — ignorado
    "\u000f": "",                                      # [ ] Shift Out — ignorado
    "\u0010": "",                                      # [ ] Data Link Escape — ignorado
    "\u0011": "",                                      # [ ] Device Control 1 — ignorado
    "\u0012": "",                                      # [ ] Device Control 2 — ignorado
    "\u0013": "",                                      # [ ] Device Control 3 — ignorado
    "\u0014": "",                                      # [ ] Device Control 4 — ignorado
    "\u0015": "",                                      # [ ] Negative Ack — ignorado
    "\u0016": "",                                      # [ ] Synchronous Idle — ignorado
    "\u0017": "",                                      # [ ] End of Trans. Block — ignorado
    "\u0018": "",                                      # [ ] Cancel — ignorado
    "\u0019": "",                                      # [ ] End of Medium — ignorado
    "\u001a": "",                                      # [ ] Substitute — ignorado
    "\u001b": "",                                      # [ ] Escape — ignorado
    "\u001c": "",                                      # [ ] File Separator — ignorado
    "\u001d": "",                                      # [ ] Group Separator — ignorado
    "\u001e": "",                                      # [ ] Record Separator — ignorado
    "\u001f": "",                                      # [ ] Unit Separator — ignorado
    "\u007f": "",                                      # [ ] DEL — ignorado

    # --- Cf : caracteres de formato (invisíveis) ---
    "\u00ad": "",                                      # [­] hífen condicional (SOFT HYPHEN) — ignorado (invisível fora de corte)
    "\u200b": "",                                      # [​] espaço de largura zero — ignorado
    "\u200c": "",                                      # [‌] não-ligador (ZWNJ) — ignorado
    "\u200d": "",                                      # [‍] ligador (ZWJ) — ignorado
    "\u200e": "",                                      # [‎] marca esquerda-direita (LRM) — ignorado
    "\u200f": "",                                      # [‏] marca direita-esquerda (RLM) — ignorado
    "\u202a": "",                                      # [‎] início LRE — ignorado
    "\u202b": "",                                      # [‏] início RLE — ignorado
    "\u202c": "",                                      # [‬] fim de direccionalidade (PDF) — ignorado
    "\u202d": "",                                      # [‎] início LRO — ignorado
    "\u202e": "",                                      # [‏] início RLO — ignorado
    "\u2060": "",                                      # [⁠] ligador sem largura (WJ) — ignorado
    "\ufeff": "",                                      # [﻿] BOM / espaço não quebrável de largura zero — ignorado

    # --- Co e Cn : uso privado e não atribuído ---
    # As gamas Co (U+E000–U+F8FF) e Cn (não atribuídos) não têm
    # leitura possível: a tratar por defeito com a cadeia vazia no
    # código do TTS (fallback), sem enumeração exaustiva aqui.
}

"""
           _ _                                _
     /\   | | |                              | |
    /  \  | | | ___ _ __ ___   __ _ _ __   __| |
   / /\ \ | | |/ _ \ '_ ` _ \ / _` | '_ \ / _` |
  / ____ \| | |  __/ | | | | | (_| | | | | (_| |
 /_/    \_\_|_|\___|_| |_| |_|\__,_|_| |_|\__,_|

"""


epel_tts_de = {
    # ==================================================================
    # 1. BUCHSTABEN MIT UMLAUT UND SCHARFEM S
    # Deutsch verwendet ä, ö, ü (Umlaute) und ß (Eszett/scharfes S).
    # ==================================================================
    "\u00c4": "a mit umlaut gross",              # [Ä]
    "\u00e4": "a mit umlaut",                    # [ä]
    "\u00d6": "o mit umlaut gross",              # [Ö]
    "\u00f6": "o mit umlaut",                    # [ö]
    "\u00dc": "u mit umlaut gross",              # [Ü]
    "\u00fc": "u mit umlaut",                    # [ü]
    "\u00df": "eszett",                          # [ß] — comment. : "scharfes s", keine Grossbuchstabe (bis 2017: ẞ als Ausnahme)

    # ==================================================================
    # 2. BESONDERE BUCHSTABEN UND LIGATUREN
    # Ä, ö, ü sind bereits in Sektion 1. Hier: seltene Zeichen.
    # ==================================================================
    "\u00e6": "ae ligatur",                      # [æ] — comment. : Fremdwort (z. B. Enzyklopädie alt)
    "\u00c6": "ae ligatur gross",                # [Æ]
    "\u0153": "oe ligatur",                      # [œ] — comment. : Fremdwort
    "\u0152": "oe ligatur gross",                # [Œ]

    # ==================================================================
    # 3. GROSSBUCHSTABEN
    # Aussprache: "grosses A", "grosses B", usw.
    # ==================================================================
    "\u0041": "grosses a",                       # [A]
    "\u0042": "grosses b",                       # [B]
    "\u0043": "grosses c",                       # [C]
    "\u0044": "grosses d",                       # [D]
    "\u0045": "grosses e",                       # [E]
    "\u0046": "grosses f",                       # [F]
    "\u0047": "grosses g",                       # [G]
    "\u0048": "grosses h",                       # [H]
    "\u0049": "grosses i",                       # [I]
    "\u004a": "grosses j",                       # [J]
    "\u004b": "grosses k",                       # [K]
    "\u004c": "grosses l",                       # [L]
    "\u004d": "grosses m",                       # [M]
    "\u004e": "grosses n",                       # [N]
    "\u004f": "grosses o",                       # [O]
    "\u0050": "grosses p",                       # [P]
    "\u0051": "grosses q",                       # [Q]
    "\u0052": "grosses r",                       # [R]
    "\u0053": "grosses s",                       # [S]
    "\u0054": "grosses t",                       # [T]
    "\u0055": "grosses u",                       # [U]
    "\u0056": "grosses v",                       # [V]
    "\u0057": "grosses w",                       # [W]
    "\u0058": "grosses x",                       # [X]
    "\u0059": "grosses y",                       # [Y]
    "\u005a": "grosses z",                       # [Z]

    # ==================================================================
    # 4. KLEINBUCHSTABEN
    # Aussprache: nur der Buchstabe, ohne "kleines" davor.
    # ==================================================================
    "\u0061": "a",                               # [a]
    "\u0062": "b",                               # [b]
    "\u0063": "c",                               # [c]
    "\u0064": "d",                               # [d]
    "\u0065": "e",                               # [e]
    "\u0066": "f",                               # [f]
    "\u0067": "g",                               # [g]
    "\u0068": "h",                               # [h]
    "\u0069": "i",                               # [i]
    "\u006a": "j",                               # [j]
    "\u006b": "k",                               # [k]
    "\u006c": "l",                               # [l]
    "\u006d": "m",                               # [m]
    "\u006e": "n",                               # [n]
    "\u006f": "o",                               # [o]
    "\u0070": "p",                               # [p]
    "\u0071": "q",                               # [q]
    "\u0072": "r",                               # [r]
    "\u0073": "s",                               # [s]
    "\u0074": "t",                               # [t]
    "\u0075": "u",                               # [u]
    "\u0076": "v",                               # [v]
    "\u0077": "w",                               # [w]
    "\u0078": "x",                               # [x]
    "\u0079": "y",                               # [y]
    "\u007a": "z",                               # [z]

    # ==================================================================
    # 5. SATZZEICHEN
    # Deutsch verwendet keine umgekehrten Satzzeichen am Anfang.
    # ==================================================================
    "\u002c": "komma",                           # [,]
    "\u002e": "punkt",                           # [.]
    "\u003b": "semikolon",                        # [;]
    "\u003a": "doppelpunkt",                      # [:]
    "\u003f": "fragezeichen",                     # [?]
    "\u0021": "ausrufezeichen",                  # [!]
    "\u2026": "auslassungspunkte",                # […] — comment. : auch "ellipsis" oder "punkte"
    "\u0028": "klammer auf",                     # [(]
    "\u0029": "klammer zu",                      # [)]
    "\u005b": "eckige klammer auf",              # [[]
    "\u005d": "eckige klammer zu",               # []]
    "\u007b": "geschweifte klammer auf",         # [{]
    "\u007d": "geschweifte klammer zu",          # [}]
    "\u00b7": "mittelpunkt",                     # [·]
    "\u2030": "promille",                        # [‰]
    "\u00a4": "währungszeichen",                 # [¤]

    # ==================================================================
    # 6. APOSTROphe UND ANFÜHRUNGSZEICHEN
    # Das Apostroph ist im Deutschen selten (Fremdwörter, Auslassungen).
    # ==================================================================
    "\u0027": "apostroph",                       # ['] — comment. : auch "auslassungszeichen"
    "\u2019": "apostroph",                       # [’] — comment. : typografisch, gleicher wert
    "\u02bc": "apostroph",                       # [ʼ] — comment. : buchstaben-apostroph
    "\u0060": "apostroph",                       # [`] — comment. : akzentzeichen, gleicher wert

    # ==================================================================
    # 7. ANFÜHRUNGSZEICHEN (unterscheidung auf/zu)
    # Deutsche Anführungszeichen: „…" (unten-oben) oder »…« (innen-außen).
    # Englische "…" werden zunehmend verwendet.
    # ==================================================================
    "\u201e": "anführungszeichen auf",           # [„] — comment. : deutsches öffnen, unten
    "\u201c": "anführungszeichen auf",           # [“] — comment. : englisches öffnen, oben
    "\u201c": "anführungszeichen auf",           # [“] — comment. : gleiches zeichen, siehe oben
    "\u201d": "anführungszeichen zu",            # [”] — comment. : englisches schliessen, oben
    "\u201e": "anführungszeichen auf",           # [„] — comment. : deutsches öffnen
    "\u201f": "anführungszeichen zu",            # [‟] — comment. : selten
    "\u00bb": "anführungszeichen auf",           # [»] — comment. : französisches/deutsches innen-öffnen
    "\u00ab": "anführungszeichen zu",            # [«] — comment. : französisches/deutsches innen-schliessen
    "\u0022": "anführungszeichen",               # ["] — comment. : gerade, kontextabhängig auf/zu
    "\u2018": "anführungszeichen auf",           # [‘] — comment. : einfaches öffnen
    "\u2019": "anführungszeichen zu",            # [’] — comment. : einfaches schliessen, gleiches zeichen wie apostroph
    "\u201a": "anführungszeichen auf",           # [‚] — comment. : einfach, unten
    "\u201b": "anführungszeichen zu",            # [‛] — comment. : selten
    "\u2039": "anführungszeichen auf",           # [‹] — comment. : einfach, innen-öffnen
    "\u203a": "anführungszeichen zu",            # [›] — comment. : einfach, innen-schliessen

    # ==================================================================
    # 8. STRICHE UND LINIEN
    # Der Bindestrich (hyphen-minus) ist vielseitig: wert "bindestrich".
    # Gedankenstrich, Halbgeviertstrich und Aufzählungszeichen: "gedankenstrich".
    # ==================================================================
    "\u002d": "bindestrich",                     # [-] — comment. : hyphen-minus, hauptverwendung
    "\u2010": "bindestrich",                     # [‐] — comment. : echter bindestrich
    "\u2011": "bindestrich",                     # [‑] — comment. : geschützter bindestrich
    "\ufe63": "bindestrich",                     # [﹣] — comment. : kleine variante
    "\uff0d": "bindestrich",                     # [－] — comment. : vollbreite
    "\u2012": "gedankenstrich",                  # [‒] — comment. : zahlenstrich
    "\u2013": "gedankenstrich",                  # [–] — comment. : halbgeviertstrich (en dash)
    "\u2014": "gedankenstrich",                  # [—] — comment. : geviertstrich (em dash)
    "\u2015": "gedankenstrich",                  # [―] — comment. : horizontale linie
    "\u2212": "minuszeichen",                    # [−] — comment. : mathematisches minus
    "\u2022": "gedankenstrich",                  # [•] — comment. : aufzählungszeichen, als strich gelesen
    "\u2023": "gedankenstrich",                  # [‣] — comment. : dreieckiges aufzählungszeichen
    "\u002f": "schrägstrich",                    # [/] — comment. : "slash"
    "\u005c": "umgekehrter schrägstrich",         # [\] — comment. : "backslash"
    "\u007c": "senkrechter strich",              # [|] — comment. : auch "pipe"
    "\u005f": "unterstrich",                     # [_] — comment. : "underscore"

    # ==================================================================
    # 9. SYMBOLE UND ZEICHEN
    # ==================================================================
    "\u20ac": "eurozeichen",                     # [€]
    "\u0024": "dollarzeichen",                   # [$]
    "\u00a3": "pfundzeichen",                    # [£]
    "\u00a2": "centzeichen",                     # [¢]
    "\u0023": "raute",                           # [#] — comment. : "raute", "kreuz", "nummernzeichen"
    "\u002a": "sternchen",                       # [*] — comment. : auch "asterisk"
    "\u0040": "at-zeichen",                      # [@] — comment. : "klammeraffe", "at"
    "\u0026": "kaufmanns-und",                   # [&] — comment. : "et", "ampersand", "und-zeichen"
    "\u0025": "prozentzeichen",                  # [%]
    "\u002b": "pluszeichen",                    # [+]
    "\u003d": "gleichheitszeichen",               # [=]
    "\u003c": "kleiner-als",                      # [<]
    "\u003e": "grösser-als",                      # [>]
    "\u005e": "dachzeichen",                     # [^] — comment. : "zirkumflex", "dach"
    "\u007e": "tilde",                           # [~] — comment. : "schlange", "wellenlinie"
    "\u00b0": "gradzeichen",                     # [°]
    "\u00a7": "paragraphzeichen",                # [§] — comment. : "paragraf"
    "\u00b6": "absatzzeichen",                   # [¶] — comment. : "pilcrow", gleiche funktion wie §
    "\u2020": "kreuz",                           # [†] — comment. : "dagger", "obelisk"
    "\u2021": "doppelkreuz",                     # [‡] — comment. : "double dagger"
    "\u00a9": "copyrightzeichen",                # [©]
    "\u00ae": "registered-zeichen",              # [®] — comment. : "eingetragenes warenzeichen"
    "\u2122": "trademark-zeichen",               # [™] — comment. : gleiche funktion wie ®
    "\u00d7": "multiplikationszeichen",          # [×]
    "\u00f7": "divisionszeichen",                # [÷]
    "\u2260": "ungleich",                        # [≠]
    "\u2264": "kleiner-gleich",                  # [≤]
    "\u2265": "grösser-gleich",                  # [≥]

    # ==================================================================
    # 10. LEERZEICHEN (nur kategorie Zs)
    # Alle breiten teilen den wert "leerzeichen" oder "zwischenraum".
    # ==================================================================
    "\u0020": "leerzeichen",                     # [ ] — comment. : normales leerzeichen
    "\u00a0": "leerzeichen",                     # [ ] — comment. : geschütztes leerzeichen
    "\u202f": "leerzeichen",                     # [ ] — comment. : schmales geschütztes leerzeichen
    "\u2009": "leerzeichen",                     # [ ] — comment. : dünnes leerzeichen
    "\u2007": "leerzeichen",                     # [ ] — comment. : zahlenleerzeichen
    "\u2008": "leerzeichen",                     # [ ] — comment. : punktierungsleerzeichen
    "\u200a": "leerzeichen",                     # [ ] — comment. : haarleerzeichen

    # ==================================================================
    # 11. SPEZIELL: kategorien Zp, Zl und C (steuerung und format)
    # Zp = absatztrennzeichen, Zl = zeilentrennzeichen,
    # C  = steuerung (Cc), format (Cf), privater bereich (Co), nicht zugewiesen (Cn).
    # ==================================================================
    # --- Zp und Zl ---
    "\u2029": "leerzeichen",                     # [ ] — comment. : absatztrennzeichen, als leerzeichen gelesen
    "\u2028": "leerzeichen",                     # [ ] — comment. : zeilentrennzeichen, als leerzeichen gelesen

    # --- Cc: steuerzeichen ---
    "\u0009": "leerzeichen",                     # [ ] — comment. : tabulator, als leerzeichen gelesen
    "\u000a": "leerzeichen",                     # [ ] — comment. : zeilenvorschub (LF), als leerzeichen gelesen
    "\u000b": "leerzeichen",                     # [ ] — comment. : vertikaler tabulator
    "\u000c": "leerzeichen",                     # [ ] — comment. : seitenvorschub (FF)
    "\u000d": "leerzeichen",                     # [ ] — comment. : wagenrücklauf (CR)
    "\u0000": "",                                # [ ] — comment. : NUL, ignoriert
    "\u0001": "",                                # [ ] — comment. : SOH, ignoriert
    "\u0002": "",                                # [ ] — comment. : STX, ignoriert
    "\u0003": "",                                # [ ] — comment. : ETX, ignoriert
    "\u0004": "",                                # [ ] — comment. : EOT, ignoriert
    "\u0005": "",                                # [ ] — comment. : ENQ, ignoriert
    "\u0006": "",                                # [ ] — comment. : ACK, ignoriert
    "\u0007": "",                                # [ ] — comment. : BEL, ignoriert
    "\u0008": "",                                # [ ] — comment. : rückschritt (BS), ignoriert
    "\u000e": "",                                # [ ] — comment. : Shift In, ignoriert
    "\u000f": "",                                # [ ] — comment. : Shift Out, ignoriert
    "\u0010": "",                                # [ ] — comment. : DLE, ignoriert
    "\u0011": "",                                # [ ] — comment. : DC1, ignoriert
    "\u0012": "",                                # [ ] — comment. : DC2, ignoriert
    "\u0013": "",                                # [ ] — comment. : DC3, ignoriert
    "\u0014": "",                                # [ ] — comment. : DC4, ignoriert
    "\u0015": "",                                # [ ] — comment. : NAK, ignoriert
    "\u0016": "",                                # [ ] — comment. : SYN, ignoriert
    "\u0017": "",                                # [ ] — comment. : ETB, ignoriert
    "\u0018": "",                                # [ ] — comment. : CAN, ignoriert
    "\u0019": "",                                # [ ] — comment. : EM, ignoriert
    "\u001a": "",                                # [ ] — comment. : SUB, ignoriert
    "\u001b": "",                                # [ ] — comment. : Escape, ignoriert
    "\u001c": "",                                # [ ] — comment. : dateitrennzeichen, ignoriert
    "\u001d": "",                                # [ ] — comment. : gruppentrennzeichen, ignoriert
    "\u001e": "",                                # [ ] — comment. : datensatztrennzeichen, ignoriert
    "\u001f": "",                                # [ ] — comment. : einheitentrennzeichen, ignoriert
    "\u007f": "",                                # [ ] — comment. : DEL, ignoriert

    # --- Cf: formatzeichen (unsichtbar) ---
    "\u00ad": "",                                # [­] — comment. : bedingter trennstrich (SOFT HYPHEN), ignoriert
    "\u200b": "",                                # [​] — comment. : nullbreitenleerzeichen, ignoriert
    "\u200c": "",                                # [‌] — comment. : ZWNJ, ignoriert
    "\u200d": "",                                # [‍] — comment. : ZWJ, ignoriert
    "\u200e": "",                                # [‎] — comment. : LRM, ignoriert
    "\u200f": "",                                # [‏] — comment. : RLM, ignoriert
    "\u202a": "",                                # [‎] — comment. : LRE, ignoriert
    "\u202b": "",                                # [‏] — comment. : RLE, ignoriert
    "\u202c": "",                                # [‬] — comment. : PDF, ignoriert
    "\u202d": "",                                # [‎] — comment. : LRO, ignoriert
    "\u202e": "",                                # [‏] — comment. : RLO, ignoriert
    "\u2060": "",                                # [⁠] — comment. : wortverbinder (WJ), ignoriert
    "\ufeff": "",                                # [﻿] — comment. : BOM, ignoriert

    # --- Co und Cn: nicht aufzählbar, mit fallback behandeln ---
    # Die bereiche Co (U+E000–U+F8FF) und Cn (nicht zugewiesen) haben keine
    # aussprache: im TTS-code mit leerer zeichenkette als fallback behandeln.
}




