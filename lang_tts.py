"""
Listes (fusionnées) des langues proposées par les TTS utilisables par MAEL

Structure des entrées du dictionnaire :
"Code MAEL": ["Référence","Code gTTS","Code BCP 47 Android","iOS Apple Voices","MAEL TTS ?"]

-------------------------------------------+

À développer plus tard :

Les modes "Dicter" et "Epeler" seront les même pour les langages "ideo"

Types d'écritures :

"ideo" --> Les systèmes logographiques ou idéophonographiques

Chaque caractère représente un mot ou une idée.
• Logogrammes / Idéogrammes : Un symbole correspond à un mot ou à un concept.
 - Exemples : Les caractères chinois (hanzi), les anciens hiéroglyphes égyptiens ou l'écriture maya. Dans l'écriture chinoise, on trouve des idéogrammes simples, composés (ex: soleil + lune = clarté) ou des idéo-phonogrammes.
• Pictogrammes : Dessins schématiques représentant directement un objet ou un être vivant.

"alpha" --> Les systèmes phonographiques

Les signes représentent des sons de la langue parlée (avec un nombre restreint de symboles de base).
• L'écriture syllabique (syllabaire) : Chaque caractère représente une syllabe complète.
 - Exemples : Les kana japonais (hiragana et katakana), le syllabaire cherokee ou l'éthiopien.
• L'alphabet (vocalique) : Chaque symbole représente un phonème individuel, distinguant nettement les voyelles et les consonnes.
 - Exemples : L'alphabet latin (utilisé pour le français, l'espagnol, l'anglais, etc.), l'alphabet grec ou cyrillique.
• L'abjad (alphabet consonantique) : Les signes notent principalement les consonnes, les voyelles étant souvent sous-entendues ou indiquées par des signes diacritiques facultatifs.
 - Exemples : L'arabe et l'hébreu.
• L'abugida (syllabo-alphabétique) : Les caractères représentent une consonne porteuse d'une voyelle inhérente, qui peut être modifiée par des signes secondaires attachés.
 - Exemples : Les écritures de l'Inde (dévanagari) et de l'Asie du Sud-Est

Structure des entrées du dictionnaire sera modifiée ainsi :
"Code MAEL": ["Type d'écriture", "Référence","Code gTTS","Code BCP 47 Android","iOS Apple Voices","MAEL TTS ?"]
À confirmer

"""


lang_tts = {
    # Afrikaans
    "af": ["Afrikaans", "af", "af-ZA", None, None],

    # Amharique
    "am": ["Amharique", "am", "am-ET", None, None],

    # Arabe
    "ar":   ["Arabe", "ar", "ar-SA", "ar-SA", None],      # Arabie Saoudite [Réf.]
    "arEG": ["Arabe", "ar", "ar-EG", None, None],         # Égypte
    "arAE": ["Arabe", "ar", "ar-AE", None, None],         # Émirats Arabes Unis
    "arIQ": ["Arabe", "ar", "ar-IQ", None, None],         # Irak
    "arJO": ["Arabe", "ar", "ar-JO", None, None],         # Jordanie
    "arKW": ["Arabe", "ar", "ar-KW", None, None],         # Koweït
    "arLB": ["Arabe", "ar", "ar-LB", None, None],         # Liban
    "arMA": ["Arabe", "ar", "ar-MA", None, None],         # Maroc
    "arQA": ["Arabe", "ar", "ar-QA", None, None],         # Qatar

    # Bengali
    "bn":   ["Bengali", "bn", "bn-IN", "bn-IN", None],    # Inde [Réf.]
    "bnBD": ["Bengali", "bn", "bn-BD", None, None],       # Bangladesh

    # Bosniaque
    "bs": ["Bosniaque", "bs", "bs-BA", None, None],

    # Bulgare
    "bg": ["Bulgare", "bg", "bg-BG", "bg-BG", None],

    # Catalan
    "ca": ["Catalan", "ca", "ca-ES", "ca-ES", None],

    # Chinois
    "zh":   ["Chinois", "zh-CN", "zh-CN", "zh-CN", None], # Simplifié - Chine [Réf.]
    "zhTW": ["Chinois", "zh-TW", "zh-TW", "zh-TW", None], # Traditionnel - Taïwan
    "zhHK": ["Chinois", "yue", "zh-HK", "zh-HK", None],   # Cantonais - Hong Kong

    # Croate
    "hr": ["Croate", "hr", "hr-HR", "hr-HR", None],

    # Tchèque
    "cs": ["Tchèque", "cs", "cs-CZ", "cs-CZ", None],

    # Danois
    "da": ["Danois", "da", "da-DK", "da-DK", None],

    # Néerlandais
    "nl":   ["Néerlandais", "nl", "nl-NL", "nl-NL", None], # Pays-Bas [Réf.]
    "nlBE": ["Néerlandais", "nl", "nl-BE", "nl-BE", None], # Belgique

    # Anglais
    "en":   ["Anglais", "en", "en-GB", "en-GB", None],     # Royaume-Uni  [Réf.]
    "enUS": ["Anglais", "en", "en-US", "en-US", None],     # États-Unis
    "enAU": ["Anglais", "en", "en-AU", "en-AU", None],     # Australie
    "enIN": ["Anglais", "en", "en-IN", "en-IN", None],     # Inde
    "enCA": ["Anglais", "en", "en-CA", None, None],        # Canada
    "enNG": ["Anglais", "en", "en-NG", None, None],        # Nigéria
    "enZA": ["Anglais", "en", "en-ZA", "en-ZA", None],     # Afrique du Sud
    "enIE": ["Anglais", "en", "en-IE", "en-IE", None],     # Irlande
    "enNZ": ["Anglais", "en", "en-NZ", None, None],        # Nouvelle-Zélande
    "enPH": ["Anglais", "en", "en-PH", None, None],        # Philippines
    "enSG": ["Anglais", "en", "en-SG", None, None],        # Singapour

    # Estonien
    "et": ["Estonien", "et", "et-EE", None, None],

    # Filipino
    "tl": ["Filipino", "tl", "fil-PH", None, None],

    # Finnois
    "fi": ["Finnois", "fi", "fi-FI", "fi-FI", None],

    # Français
    "fr":   ["Français", "fr", "fr-FR", "fr-FR", None],    # France [Réf.]
    "frCA": ["Français", "fr-CA", "fr-CA", "fr-CA", None], # Canada
    "frBE": ["Français", "fr", "fr-BE", "fr-BE", None],    # Belgique
    "frCH": ["Français", "fr", "fr-CH", None, None],       # Suisse

    # Galicien
    "gl": ["Galicien", "gl", "gl-ES", "gl-ES", None],

    # Allemand
    "de":   ["Allemand", "de", "de-DE", "de-DE", None],    # Allemagne [Réf.]
    "deAT": ["Allemand", "de", "de-AT", None, None],       # Autriche
    "deCH": ["Allemand", "de", "de-CH", None, None],       # Suisse

    # Grec
    "el": ["Grec", "el", "el-GR", "el-GR", None],

    # Gujarati
    "gu": ["Gujarati", "gu", "gu-IN", "gu-IN", None],

    # Hausa
    "ha": ["Hausa", "ha", "ha-NG", None, None],

    # Hébreu
    "he": ["Hébreu", "iw", "he-IL", "he-IL", None],

    # Hindi
    "hi": ["Hindi", "hi", "hi-IN", "hi-IN", None],

    # Hongrois
    "hu": ["Hongrois", "hu", "hu-HU", "hu-HU", None],

    # Islandais
    "is": ["Islandais", "is", "is-IS", None, None],

    # Indonésien
    "id": ["Indonésien", "id", "id-ID", "id-ID", None],

    # Italien
    "it":   ["Italien", "it", "it-IT", "it-IT", None],     # Italie [Réf.]
    "itCH": ["Italien", "it", "it-CH", None, None],        # Suisse

    # Japonais
    "ja": ["Japonais", "ja", "ja-JP", "ja-JP", None],

    # Javanais
    "jv": ["Javanais", "jw", "jv-ID", None, None],

    # Kannada
    "kn": ["Kannada", "kn", "kn-IN", "kn-IN", None],

    # Khmer
    "km": ["Khmer", "km", "km-KH", None, None],

    # Coréen
    "ko": ["Coréen", "ko", "ko-KR", "ko-KR", None],

    # Letton
    "lv": ["Letton", "lv", "lv-LV", None, None],

    # Lituanien
    "lt": ["Lituanien", "lt", "lt-LT", "lt-LT", None],

    # Malais
    "ms": ["Malais", "ms", "ms-MY", "ms-MY", None],

    # Malayalam
    "ml": ["Malayalam", "ml", "ml-IN", "ml-IN", None],

    # Marathi
    "mr": ["Marathi", "mr", "mr-IN", "mr-IN", None],

    # Birman
    "my": ["Birman", "my", "my-MM", None, None],

    # Népalais
    "ne": ["Népalais", "ne", "ne-NP", "ne-NP", None],

    # Norvégien
    "no": ["Norvégien", "no", "no-NO", "no-NO", None],

    # Polonais
    "pl": ["Polonais", "pl", "pl-PL", "pl-PL", None],

    # Portugais
    "pt":   ["Portugais", "pt-PT", "pt-PT", "pt-PT", None], # Portugal [Réf.]
    "ptBR": ["Portugais", "pt", "pt-BR", "pt-BR", None],    # Brésil

    # Pendjabi
    "pa": ["Pendjabi", "pa", "pa-IN", None, None],

    # Roumain
    "ro": ["Roumain", "ro", "ro-RO", "ro-RO", None],

    # Russe
    "ru": ["Russe", "ru", "ru-RU", "ru-RU", None],

    # Serbe
    "sr": ["Serbe", "sr", "sr-RS", None, None],

    # Cingalais
    "si": ["Cingalais", "si", "si-LK", None, None],

    # Slovaque
    "sk": ["Slovaque", "sk", "sk-SK", "sk-SK", None],

    # Espagnol
    "es":   ["Espagnol", "es", "es-ES", "es-ES", None],    # Espagne [Réf.]
    "esUS": ["Espagnol", "es", "es-US", None, None],       # États-Unis
    "esMX": ["Espagnol", "es", "es-MX", "es-MX", None],    # Mexique
    "esAR": ["Espagnol", "es", "es-AR", "es-AR", None],    # Argentine
    "esCO": ["Espagnol", "es", "es-CO", "es-CO", None],    # Colombie
    "esCL": ["Espagnol", "es", "es-CL", "es-CL", None],    # Chili
    "esPE": ["Espagnol", "es", "es-PE", None, None],       # Pérou
    "esVE": ["Espagnol", "es", "es-VE", None, None],       # Venezuela

    # Soundanais
    "su": ["Soundanais", "su", "su-ID", None, None],

    # Suédois
    "sv": ["Suédois", "sv", "sv-SE", "sv-SE", None],

    # Swahili
    "sw":   ["Swahili", "sw", "sw-KE", None, None],        # Kenya [Réf.]
    "swTZ": ["Swahili", "sw", "sw-TZ", None, None],        # Tanzanie

    # Tamoul
    "ta":   ["Tamoul", "ta", "ta-IN", "ta-IN", None],      # Inde [Réf.]
    "taSG": ["Tamoul", "ta", "ta-SG", None, None],         # Singapour
    "taLK": ["Tamoul", "ta", "ta-LK", None, None],         # Sri Lanka
    "taMY": ["Tamoul", "ta", "ta-MY", None, None],         # Malaisie

    # Télougou
    "te": ["Télougou", "te", "te-IN", "te-IN", None],

    # Thaï
    "th": ["Thaï", "th", "th-TH", "th-TH", None],

    # Turc
    "tr": ["Turc", "tr", "tr-TR", "tr-TR", None],

    # Ukrainien
    "uk": ["Ukrainien", "uk", "uk-UA", "uk-UA", None],

    # Ourdou
    "ur":   ["Ourdou", "ur", "ur-PK", None, None],         # Pakistan [Réf.]
    "urIN": ["Ourdou", "ur", "ur-IN", None, None],         # Inde

    # Vietnamien
    "vi": ["Vietnamien", "vi", "vi-VN", "vi-VN", None],

    # Gallois
    "cy": ["Gallois", "cy", "cy-GB", None, None],
}


if __name__ == "__main__":
    from collections import Counter

    def print_stats(data: dict) -> None:
        """
        Affiche des statistiques globales sur le dictionnaire lang_tts.
        """
        total = len(data)
        # Langues génériques distinctes (nom_générique)
        generic = len({v[0] for v in data.values()})

        # --- Support par TTS ---
        # gTTS
        gtts_entries = sum(1 for v in data.values() if v[1] is not None)
        gtts_codes_unique = len({v[1] for v in data.values() if v[1] is not None})
        # Android
        android_entries = sum(1 for v in data.values() if v[2] is not None)
        android_codes_unique = len({v[2] for v in data.values() if v[2] is not None})
        # Apple
        apple_entries = sum(1 for v in data.values() if v[3] is not None)
        apple_codes_unique = len({v[3] for v in data.values() if v[3] is not None})

        print("=" * 60)
        print("STATISTIQUES GLOBALES DU DICTIONNAIRE lang_tts")
        print("=" * 60)
        print(f"Nombre total d'entrées                     : {total}")
        print(f"Nombre de langues génériques distinctes    : {generic}")
        print()

        print("--- Support par moteur TTS ---")
        print(f"{'':20} {'gTTS':>8} {'Android':>8} {'Apple':>8}")
        print(f"{'Entrées supportées':20} {gtts_entries:>8} {android_entries:>8} {apple_entries:>8}")
        print(f"{'Codes uniques':20} {gtts_codes_unique:>8} {android_codes_unique:>8} {apple_codes_unique:>8}")
        print()

        # Chevauchement : pour chaque entrée, on vérifie présence gTTS/Android/Apple
        # Comptons combien d'entrées sont supportées par les trois, par deux, par un seul...
        counter = Counter()
        for v in data.values():
            has_g = v[1] is not None
            has_a = v[2] is not None
            has_ap = v[3] is not None
            support_tuple = (has_g, has_a, has_ap)
            counter[support_tuple] += 1

        print("--- Chevauchement des supports (par entrée) ---")
        labels = {
            (True, True, True):   "gTTS + Android + Apple",
            (True, True, False):  "gTTS + Android (pas Apple)",
            (True, False, True):  "gTTS + Apple (pas Android)",
            (False, True, True):  "Android + Apple (pas gTTS)",
            (True, False, False): "gTTS seul",
            (False, True, False): "Android seul",
            (False, False, True): "Apple seul",
            (False, False, False): "Aucun support",
        }
        for support, count in sorted(counter.items()):
            label = labels.get(support, str(support))
            print(f"  {label:40} : {count}")
        print()

        # Langues avec le plus de variantes (top 5)
        generic_counter = Counter(v[0] for v in data.values())
        most_common = generic_counter.most_common(5)
        print("--- Top 5 des langues génériques avec le plus de variantes ---")
        for name, cnt in most_common:
            print(f"  {name:20} : {cnt} entrées")
        print()

        # Diverses curiosités
        # Entrées où le code Android diffère du code Apple (quand les deux existent)
        diff_codes = []
        for k, v in data.items():
            if v[2] is not None and v[3] is not None and v[2] != v[3]:
                diff_codes.append((k, v[0], v[2], v[3]))
        if diff_codes:
            print("--- Entrées où le code Android et Apple diffèrent (alors que les deux existent) ---")
            for k, name, andr, apl in diff_codes:
                print(f"  {k}: Android={andr} Apple={apl} ({name})")
        else:
            print("--- Codes Android et Apple : ils sont tous identiques quand les deux existent. ---")

        # Entrées où gTTS a un code unique différent du préfixe de langue ? (par ex. "yue" pour zhHK)
        # On peut les signaler
        unusual_gtts = []
        for k, v in data.items():
            gtts = v[1]
            # Comparer avec la partie "langue" de l'Android ou de la clé
            if gtts and not gtts.startswith(k[:2]):  # approximation : la clé commence par un code 2 lettres
                unusual_gtts.append((k, gtts, v[0]))
        if unusual_gtts:
            print()
            print("--- Codes gTTS inhabituels (différents du préfixe de la clé) ---")
            for k, gtts, name in unusual_gtts:
                print(f"  {k:6} -> gTTS={gtts} ({name})")
        print("=" * 60)

    print_stats(lang_tts)
