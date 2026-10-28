# -*- coding: utf-8 -*-
"""
mode_msg.py
===========

Traductions des **messages courts** affichés à l'écran par la couche
``TtsSetupBuilder``.

Les clés internes (``"Mode cacher"``, ``"Mode dicter"``, ``"Mode Epeler"``,
``"Mode épeler indisponible"``, ``"Mode épeler émojis"``) sont consommées
par la fonction utilitaire :func:`get_mode_message` (mode, langue) qui
renvoie le texte traduit, avec un repli français en cas de langue ou
de clé inconnue.

Conventions
-----------

* Les clés de premier niveau sont des codes langue courts ISO 639-1
  (deux lettres minuscules, par ex. ``"fr"``, ``"es"``). Cela reste
  aligné avec la résolution de langue effectuée par ``TtsSetupBuilder``
  (clé racine ``"fr"``, ``"es"``, etc.).
* Les langues non couvertes retombent toujours sur le français.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Mapping des noms de langue « humain » -> code court 2 lettres.
# Utile pour rebrancher facilement un texte d'origine en clair.
# 60 langues de référence en octobre 2026
# ----------------------------------------------------------------------

_LANG_NAMES = {
    "Afrikaans": "af",
    "Allemand": "de",
    "Amharique": "am",
    "Anglais": "en",
    "Arabe": "ar",
    "Bengali": "bn",
    "Birman": "my",
    "Bosniaque": "bs",
    "Bulgare": "bg",
    "Catalan": "ca",
    "Chinois": "zh",
    "Cingalais": "si",
    "Coréen": "ko",
    "Croate": "hr",
    "Danois": "da",
    "Espagnol": "es",
    "Estonien": "et",
    "Filipino": "tl",
    "Finnois": "fi",
    "Français": "fr",
    "Galicien": "gl",
    "Gallois": "cy",
    "Grec": "el",
    "Gujarati": "gu",
    "Haoussa": "ha",
    "Hébreu": "he",
    "Hindi": "hi",
    "Hongrois": "hu",
    "Indonésien": "id",
    "Islandais": "is",
    "Italien": "it",
    "Japonais": "ja",
    "Javanais": "jv",
    "Kannada": "kn",
    "Khmer": "km",
    "Letton": "lv",
    "Lituanien": "lt",
    "Malais": "ms",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Néerlandais": "nl",
    "Népalais": "ne",
    "Norvégien": "no",
    "Ourdou": "ur",
    "Pendjabi": "pa",
    "Polonais": "pl",
    "Portugais": "pt",
    "Roumain": "ro",
    "Russe": "ru",
    "Serbe": "sr",
    "Slovaque": "sk",
    "Soundanais": "su",
    "Suédois": "sv",
    "Swahili": "sw",
    "Tamoul": "ta",
    "Tchèque": "cs",
    "Télougou": "te",
    "Thaï": "th",
    "Turc": "tr",
    "Ukrainien": "uk",
    "Vietnamien": "vi",
}

# ----------------------------------------------------------------------
# Table des traductions
# ----------------------------------------------------------------------
# On distingue trois familles de clés :
#   * ``"Mode cacher"`` / ``"Mode dicter"`` / ``"Mode Epeler"`` :
#     messages de succès affichés à l'écran lors du lancement de
#     chaque mode (équivalent de « Écoute bien. »).
#   * ``"Mode epeler non implemente"`` : message d'erreur pour les
#     langues dont le dictionnaire ``epel_tts_xx`` est absent
#     (coréen, japonais, chinois, russe, grec...).
#   * ``"Mode epeler emoji"`` : message d'erreur lorsqu'un caractère
#     du payload relève d'une séquence émoji (ZWJ, sélecteurs de
#     teint, indicateurs régionaux, etc.).
# ----------------------------------------------------------------------
traductions = {
    # Afrikaans
    "af": {
        "Mode cacher": "Luister goed.",
        "Mode dicter": "Skryf die diktee neer.",
        "Mode Epeler": "Luister na die letters.",
        "Mode epeler non implemente":
            "Spelmodus nog nie in hierdie taal geïmplementeer nie",
        "Mode epeler emoji":
            "MAEL verwerk nie emoji's nie",
        "Mode mp3 telechargement ":
            "Klank aflaai...",
        "Mode mp3 erreur ":
            "Aflaai fout...",
    },
    # Amharique
    "am": {
        "Mode cacher": "በደንብ አዳምጥ።",
        "Mode dicter": "አይስሙለትን ጻፍ።",
        "Mode Epeler": "ፊደላቱን አዳምጥ።",
        "Mode epeler non implemente":
            "የፊደል አጻጻፍ ሁነታ በዚህ ቋንቋ ገና አልተተገበረም",
        "Mode epeler emoji":
            "MAEL ኢሞጂዎችን አያስኬድም",
        "Mode mp3 telechargement ":
            "ድምጽ በማውረድ ላይ...",
        "Mode mp3 erreur ":
            "የማውረድ ስህተት...",
    },
    # Arabe
    "ar": {
        "Mode cacher": "استمع جيدًا.",
        "Mode dicter": "اكتب الإملاء.",
        "Mode Epeler": "استمع إلى الحروف.",
        "Mode epeler non implemente":
            "وضع التهجئة لم يتم تنفيذه بعد في هذه اللغة",
        "Mode epeler emoji":
            "MAEL لا يعالج الرموز التعبيرية",
        "Mode mp3 telechargement ":
            "جارٍ تنزيل الصوت...",
        "Mode mp3 erreur ":
            "خطأ في التنزيل...",
    },
    # Bengali
    "bn": {
        "Mode cacher": "ভালো করে শোনো।",
        "Mode dicter": "শ্রুতিলেখটি লেখো।",
        "Mode Epeler": "অক্ষরগুলো শোনো।",
        "Mode epeler non implemente":
            "এই ভাষায় বানান মোড এখনও প্রয়োগ করা হয়নি",
        "Mode epeler emoji":
            "MAEL ইমোজি প্রক্রিয়া করে না",
        "Mode mp3 telechargement ":
            "অডিও ডাউনলোড হচ্ছে...",
        "Mode mp3 erreur ":
            "ডাউনলোড ত্রুটি...",
    },
    # Bosniaque
    "bs": {
        "Mode cacher": "Slušaj pažljivo.",
        "Mode dicter": "Napiši diktat.",
        "Mode Epeler": "Slušaj slova.",
        "Mode epeler non implemente":
            "Način sricanja još nije implementiran na ovom jeziku",
        "Mode epeler emoji":
            "MAEL ne obrađuje emodžije",
        "Mode mp3 telechargement ":
            "Preuzimanje zvuka...",
        "Mode mp3 erreur ":
            "Greška pri preuzimanju...",
    },
    # Bulgare
    "bg": {
        "Mode cacher": "Слушай внимателно.",
        "Mode dicter": "Напиши диктовката.",
        "Mode Epeler": "Слушай буквите.",
        "Mode epeler non implemente":
            "Режимът за правопис все още не е внедрен на този език",
        "Mode epeler emoji":
            "MAEL не обработва емоджита",
        "Mode mp3 telechargement ":
            "Изтегляне на аудио...",
        "Mode mp3 erreur ":
            "Грешка при изтегляне...",
    },
    # Catalan
    "ca": {
        "Mode cacher": "Escolta bé.",
        "Mode dicter": "Escriu el dictat.",
        "Mode Epeler": "Escolta les lletres.",
        "Mode epeler non implemente":
            "El mode de lletrejar encara no està implementat en aquest idioma",
        "Mode epeler emoji":
            "MAEL no processa els emojis",
        "Mode mp3 telechargement ":
            "Descarregant àudio...",
        "Mode mp3 erreur ":
            "Error de descàrrega...",
    },
    # Chinois
    "zh": {
        "Mode cacher": "仔细听。",
        "Mode dicter": "写下听写内容。",
        "Mode Epeler": "听字母。",
        "Mode epeler non implemente":
            "该语言尚未实现拼写模式",
        "Mode epeler emoji":
            "MAEL 不处理表情符号",
        "Mode mp3 telechargement ":
            "正在下载音频...",
        "Mode mp3 erreur ":
            "下载错误...",
    },
    # Croate
    "hr": {
        "Mode cacher": "Slušaj pažljivo.",
        "Mode dicter": "Napiši diktat.",
        "Mode Epeler": "Slušaj slova.",
        "Mode epeler non implemente":
            "Način sricanja još nije implementiran na ovom jeziku",
        "Mode epeler emoji":
            "MAEL ne obrađuje emoji znakove",
        "Mode mp3 telechargement ":
            "Preuzimanje zvuka...",
        "Mode mp3 erreur ":
            "Pogreška pri preuzimanju...",
    },
    # Tchèque
    "cs": {
        "Mode cacher": "Poslouchej pozorně.",
        "Mode dicter": "Napiš diktát.",
        "Mode Epeler": "Poslouchej písmena.",
        "Mode epeler non implemente":
            "Režim hláskování zatím není v tomto jazyce implementován",
        "Mode epeler emoji":
            "MAEL nezpracovává emoji",
        "Mode mp3 telechargement ":
            "Stahování zvuku...",
        "Mode mp3 erreur ":
            "Chyba stahování...",
    },
    # Danois
    "da": {
        "Mode cacher": "Lyt godt efter.",
        "Mode dicter": "Skriv diktaten.",
        "Mode Epeler": "Lyt til bogstaverne.",
        "Mode epeler non implemente":
            "Stavemåde er endnu ikke implementeret på dette sprog",
        "Mode epeler emoji":
            "MAEL behandler ikke emojis",
        "Mode mp3 telechargement ":
            "Downloader lyd...",
        "Mode mp3 erreur ":
            "Downloadfejl...",
    },
    # Néerlandais
    "nl": {
        "Mode cacher": "Luister goed.",
        "Mode dicter": "Schrijf het dictee op.",
        "Mode Epeler": "Luister naar de letters.",
        "Mode epeler non implemente":
            "Spelmodus is nog niet geïmplementeerd in deze taal",
        "Mode epeler emoji":
            "MAEL verwerkt geen emoji's",
        "Mode mp3 telechargement ":
            "Audio downloaden...",
        "Mode mp3 erreur ":
            "Downloadfout...",
    },
    # Anglais
    "en": {
        "Mode cacher": "Listen carefully.",
        "Mode dicter": "Write down the dictation.",
        "Mode Epeler": "Listen to the letters.",
        "Mode epeler non implemente":
            "Spelling mode not yet implemented in this language",
        "Mode epeler emoji":
            "MAEL does not process emojis",
        "Mode mp3 telechargement ":
            "Audio downloading...",
        "Mode mp3 erreur ":
            "Download Error...",
    },
    # Estonien
    "et": {
        "Mode cacher": "Kuula hoolikalt.",
        "Mode dicter": "Kirjuta etteütlus üles.",
        "Mode Epeler": "Kuula tähti.",
        "Mode epeler non implemente":
            "Õigekirjarežiim pole selles keeles veel rakendatud",
        "Mode epeler emoji":
            "MAEL ei töötle emotikone",
        "Mode mp3 telechargement ":
            "Heli allalaadimine...",
        "Mode mp3 erreur ":
            "Allalaadimise viga...",
    },
    # Filipino
    "tl": {
        "Mode cacher": "Makinig nang mabuti.",
        "Mode dicter": "Isulat ang dictation.",
        "Mode Epeler": "Makinig sa mga titik.",
        "Mode epeler non implemente":
            "Ang spelling mode ay hindi pa naipapatupad sa wikang ito",
        "Mode epeler emoji":
            "Hindi pinoproseso ng MAEL ang mga emoji",
        "Mode mp3 telechargement ":
            "Nagda-download ng audio...",
        "Mode mp3 erreur ":
            "Error sa pag-download...",
    },
    # Finnois
    "fi": {
        "Mode cacher": "Kuuntele tarkasti.",
        "Mode dicter": "Kirjoita sanelu ylös.",
        "Mode Epeler": "Kuuntele kirjaimia.",
        "Mode epeler non implemente":
            "Tavausmoodia ei ole vielä toteutettu tällä kielellä",
        "Mode epeler emoji":
            "MAEL ei käsittele emojeita",
        "Mode mp3 telechargement ":
            "Ladataan ääntä...",
        "Mode mp3 erreur ":
            "Latausvirhe...",
    },
    # Français
    "fr": {
        "Mode cacher": "Écoute bien.",
        "Mode dicter": "Écris la dictée.",
        "Mode Epeler": "Écoute les lettres.",
        "Mode epeler non implemente":
            "Mode épeler pas encore implémenté dans cette langue",
        "Mode epeler emoji":
            "MAEL ne traite pas les émojis",
        "Mode mp3 telechargement ":
            "Téléchargement de l'audio...",
        "Mode mp3 erreur ":
            "Erreur de téléchargement...",
    },
    # Galicien
    "gl": {
        "Mode cacher": "Escoita ben.",
        "Mode dicter": "Escribe o ditado.",
        "Mode Epeler": "Escoita as letras.",
        "Mode epeler non implemente":
            "O modo de deletrear aínda non está implementado neste idioma",
        "Mode epeler emoji":
            "MAEL non procesa os emojis",
        "Mode mp3 telechargement ":
            "Descargando o audio...",
        "Mode mp3 erreur ":
            "Erro de descarga...",
    },
    # Allemand
    "de": {
        "Mode cacher": "Hör gut zu.",
        "Mode dicter": "Schreib das Diktat auf.",
        "Mode Epeler": "Hör dir die Buchstaben an.",
        "Mode epeler non implemente":
            "Buchstabiermodus in dieser Sprache noch nicht implementiert",
        "Mode epeler emoji":
            "MAEL verarbeitet keine Emojis",
        "Mode mp3 telechargement ":
            "Audio wird heruntergeladen...",
        "Mode mp3 erreur ":
            "Download-Fehler...",
    },
    # Grec
    "el": {
        "Mode cacher": "Άκου προσεκτικά.",
        "Mode dicter": "Γράψε την υπαγόρευση.",
        "Mode Epeler": "Άκου τα γράμματα.",
        "Mode epeler non implemente":
            "Η λειτουργία συλλαβισμού δεν έχει ακόμη υλοποιηθεί σε αυτή τη γλώσσα",
        "Mode epeler emoji":
            "Το MAEL δεν επεξεργάζεται emoji",
        "Mode mp3 telechargement ":
            "Λήψη ήχου...",
        "Mode mp3 erreur ":
            "Σφάλμα λήψης...",
    },
    # Gujarati
    "gu": {
        "Mode cacher": "ધ્યાનથી સાંભળો.",
        "Mode dicter": "શ્રુતલેખ લખો.",
        "Mode Epeler": "અક્ષરો સાંભળો.",
        "Mode epeler non implemente":
            "આ ભાષામાં જોડણી મોડ હજી લાગુ કરવામાં આવ્યો નથી",
        "Mode epeler emoji":
            "MAEL ઇમોજી પ્રક્રિયા કરતું નથી",
        "Mode mp3 telechargement ":
            "ઓડિયો ડાઉનલોડ થઈ રહ્યું છે...",
        "Mode mp3 erreur ":
            "ડાઉનલોડ ભૂલ...",
    },
    # Haoussa
    "ha": {
        "Mode cacher": "Saurara da kyau.",
        "Mode dicter": "Rubuta dictation ɗin.",
        "Mode Epeler": "Saurari haruffan.",
        "Mode epeler non implemente":
            "Ba a aiwatar da yanayin rubutu a wannan harshe ba tukuna",
        "Mode epeler emoji":
            "MAEL baya sarrafa emoji",
        "Mode mp3 telechargement ":
            "Ana sauke sauti...",
        "Mode mp3 erreur ":
            "Kuskuren saukewa...",
    },
    # Hébreu
    "he": {
        "Mode cacher": "הקשב היטב.",
        "Mode dicter": "כתוב את ההכתבה.",
        "Mode Epeler": "הקשב לאותיות.",
        "Mode epeler non implemente":
            "מצב איות עדיין לא מיושם בשפה זו",
        "Mode epeler emoji":
            "MAEL לא מעבד אימוג'ים",
        "Mode mp3 telechargement ":
            "מוריד שמע...",
        "Mode mp3 erreur ":
            "שגיאת הורדה...",
    },
    # Hindi
    "hi": {
        "Mode cacher": "ध्यान से सुनो।",
        "Mode dicter": "श्रुतलेख लिखो।",
        "Mode Epeler": "अक्षरों को सुनो।",
        "Mode epeler non implemente":
            "इस भाषा में वर्तनी मोड अभी लागू नहीं किया गया है",
        "Mode epeler emoji":
            "MAEL इमोजी को प्रोसेस नहीं करता",
        "Mode mp3 telechargement ":
            "ऑडियो डाउनलोड हो रहा है...",
        "Mode mp3 erreur ":
            "डाउनलोड त्रुटि...",
    },
    # Hongrois
    "hu": {
        "Mode cacher": "Figyelj jól.",
        "Mode dicter": "Írd le a diktálást.",
        "Mode Epeler": "Hallgasd a betűket.",
        "Mode epeler non implemente":
            "A betűzési mód még nincs megvalósítva ezen a nyelven",
        "Mode epeler emoji":
            "A MAEL nem dolgoz fel emojikat",
        "Mode mp3 telechargement ":
            "Hang letöltése...",
        "Mode mp3 erreur ":
            "Letöltési hiba...",
    },
    # Islandais
    "is": {
        "Mode cacher": "Hlustaðu vel.",
        "Mode dicter": "Skrifaðu upp lesturinn.",
        "Mode Epeler": "Hlustaðu á stafina.",
        "Mode epeler non implemente":
            "Stafsetningahamur hefur ekki verið útfærður á þessu tungumáli ennþá",
        "Mode epeler emoji":
            "MAEL vinnur ekki með emoji",
        "Mode mp3 telechargement ":
            "Hleð niður hljóði...",
        "Mode mp3 erreur ":
            "Niðurhalsvilla...",
    },
    # Indonésien
    "id": {
        "Mode cacher": "Dengarkan dengan baik.",
        "Mode dicter": "Tulis dikte itu.",
        "Mode Epeler": "Dengarkan huruf-hurufnya.",
        "Mode epeler non implemente":
            "Mode ejaan belum diterapkan dalam bahasa ini",
        "Mode epeler emoji":
            "MAEL tidak memproses emoji",
        "Mode mp3 telechargement ":
            "Mengunduh audio...",
        "Mode mp3 erreur ":
            "Kesalahan unduhan...",
    },
    # Italien
    "it": {
        "Mode cacher": "Ascolta bene.",
        "Mode dicter": "Scrivi il dettato.",
        "Mode Epeler": "Ascolta le lettere.",
        "Mode epeler non implemente":
            "Modalità spelling non ancora implementata in questa lingua",
        "Mode epeler emoji":
            "MAEL non gestisce le emoji",
        "Mode mp3 telechargement ":
            "Download dell'audio in corso...",
        "Mode mp3 erreur ":
            "Errore di download...",
    },
    # Japonais
    "ja": {
        "Mode cacher": "よく聞いてください。",
        "Mode dicter": "書き取りを書いてください。",
        "Mode Epeler": "文字を聞いてください。",
        "Mode epeler non implemente":
            "この言語ではスペルモードはまだ実装されていません",
        "Mode epeler emoji":
            "MAELは絵文字を処理しません",
        "Mode mp3 telechargement ":
            "音声をダウンロード中...",
        "Mode mp3 erreur ":
            "ダウンロードエラー...",
    },
    # Javanais
    "jv": {
        "Mode cacher": "Rungokna kanthi becik.",
        "Mode dicter": "Tulisen diktene.",
        "Mode Epeler": "Rungokna aksarane.",
        "Mode epeler non implemente":
            "Mode ejaan durung ditrapake ing basa iki",
        "Mode epeler emoji":
            "MAEL ora ngolah emoji",
        "Mode mp3 telechargement ":
            "Ngundhuh audio...",
        "Mode mp3 erreur ":
            "Kesalahan undhuhan...",
    },
    # Kannada
    "kn": {
        "Mode cacher": "ಚೆನ್ನಾಗಿ ಕೇಳಿ.",
        "Mode dicter": "ಆಲೇಖನವನ್ನು ಬರೆಯಿರಿ.",
        "Mode Epeler": "ಅಕ್ಷರಗಳನ್ನು ಕೇಳಿ.",
        "Mode epeler non implemente":
            "ಈ ಭಾಷೆಯಲ್ಲಿ ಕಾಗುಣಿತ ಮೋಡ್ ಇನ್ನೂ ಜಾರಿಗೆ ಬಂದಿಲ್ಲ",
        "Mode epeler emoji":
            "MAEL ಎಮೋಜಿಗಳನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುವುದಿಲ್ಲ",
        "Mode mp3 telechargement ":
            "ಆಡಿಯೋ ಡೌನ್‌ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
        "Mode mp3 erreur ":
            "ಡೌನ್‌ಲೋಡ್ ದೋಷ...",
    },
    # Khmer
    "km": {
        "Mode cacher": "ស្តាប់ឱ្យបានល្អ។",
        "Mode dicter": "សរសេរតាមអាន។",
        "Mode Epeler": "ស្តាប់អក្សរ។",
        "Mode epeler non implemente":
            "របៀបប្រកបមិនទាន់ត្រូវបានអនុវត្តនៅក្នុងភាសានេះទេ",
        "Mode epeler emoji":
            "MAEL មិនដំណើរការអេម៉ូជីទេ",
        "Mode mp3 telechargement ":
            "កំពុងទាញយកសំឡេង...",
        "Mode mp3 erreur ":
            "កំហុសក្នុងការទាញយក...",
    },
    # Coréen
    "ko": {
        "Mode cacher": "잘 들어보세요.",
        "Mode dicter": "받아쓰기를 쓰세요.",
        "Mode Epeler": "글자를 들어보세요.",
        "Mode epeler non implemente":
            "이 언어에서는 철자 모드가 아직 구현되지 않았습니다",
        "Mode epeler emoji":
            "MAEL은 이모지를 처리하지 않습니다",
        "Mode mp3 telechargement ":
            "오디오 다운로드 중...",
        "Mode mp3 erreur ":
            "다운로드 오류...",
    },
    # Letton
    "lv": {
        "Mode cacher": "Klausies uzmanīgi.",
        "Mode dicter": "Uzraksti diktātu.",
        "Mode Epeler": "Klausies burtus.",
        "Mode epeler non implemente":
            "Pareizrakstības režīms šajā valodā vēl nav ieviests",
        "Mode epeler emoji":
            "MAEL neapstrādā emocijzīmes",
        "Mode mp3 telechargement ":
            "Lejupielādē audio...",
        "Mode mp3 erreur ":
            "Lejupielādes kļūda...",
    },
    # Lituanien
    "lt": {
        "Mode cacher": "Klausykis atidžiai.",
        "Mode dicter": "Užrašyk diktantą.",
        "Mode Epeler": "Klausykis raidžių.",
        "Mode epeler non implemente":
            "Rašybos režimas šioje kalboje dar neįdiegtas",
        "Mode epeler emoji":
            "MAEL neapdoroja jaustukų",
        "Mode mp3 telechargement ":
            "Atsisiunčiamas garsas...",
        "Mode mp3 erreur ":
            "Atsisiuntimo klaida...",
    },
    # Malais
    "ms": {
        "Mode cacher": "Dengar dengan teliti.",
        "Mode dicter": "Tulis imlak itu.",
        "Mode Epeler": "Dengar huruf-hurufnya.",
        "Mode epeler non implemente":
            "Mod ejaan belum dilaksanakan dalam bahasa ini",
        "Mode epeler emoji":
            "MAEL tidak memproses emoji",
        "Mode mp3 telechargement ":
            "Memuat turun audio...",
        "Mode mp3 erreur ":
            "Ralat muat turun...",
    },
    # Malayalam
    "ml": {
        "Mode cacher": "ശ്രദ്ധയോടെ കേൾക്കുക.",
        "Mode dicter": "ഡിക്റ്റേഷൻ എഴുതുക.",
        "Mode Epeler": "അക്ഷരങ്ങൾ കേൾക്കുക.",
        "Mode epeler non implemente":
            "ഈ ഭാഷയിൽ അക്ഷരവിന്യാസ മോഡ് ഇതുവരെ നടപ്പിലാക്കിയിട്ടില്ല",
        "Mode epeler emoji":
            "MAEL ഇമോജികൾ പ്രോസസ്സ് ചെയ്യുന്നില്ല",
        "Mode mp3 telechargement ":
            "ഓഡിയോ ഡൗൺലോഡ് ചെയ്യുന്നു...",
        "Mode mp3 erreur ":
            "ഡൗൺലോഡ് പിശക്...",
    },
    # Marathi
    "mr": {
        "Mode cacher": "लक्ष देऊन ऐका.",
        "Mode dicter": "श्रुतलेख लिहा.",
        "Mode Epeler": "अक्षरे ऐका.",
        "Mode epeler non implemente":
            "या भाषेत स्पेलिंग मोड अद्याप लागू केलेला नाही",
        "Mode epeler emoji":
            "MAEL इमोजी प्रक्रिया करत नाही",
        "Mode mp3 telechargement ":
            "ऑडिओ डाउनलोड होत आहे...",
        "Mode mp3 erreur ":
            "डाउनलोड त्रुटी...",
    },
    # Birman
    "my": {
        "Mode cacher": "သေချာနားထောင်ပါ။",
        "Mode dicter": "ဓာတ်စက်ရိုက်ထားသည်ကို ရေးပါ။",
        "Mode Epeler": "အက္ခရာများကို နားထောင်ပါ။",
        "Mode epeler non implemente":
            "ဤဘာသာစကားတွင် စာလုံးပေါင်းမုဒ်ကို မအကောင်အထည်ဖော်ရသေးပါ",
        "Mode epeler emoji":
            "MAEL သည် အီမိုဂျီများကို မလုပ်ဆောင်ပါ",
        "Mode mp3 telechargement ":
            "အသံဒေါင်းလုဒ်လုပ်နေသည်...",
        "Mode mp3 erreur ":
            "ဒေါင်းလုဒ်အမှား...",
    },
    # Népalais
    "ne": {
        "Mode cacher": "ध्यान दिएर सुन्नुहोस्।",
        "Mode dicter": "श्रुतलेख लेख्नुहोस्।",
        "Mode Epeler": "अक्षरहरू सुन्नुहोस्।",
        "Mode epeler non implemente":
            "यो भाषामा हिज्जे मोड अझै लागू गरिएको छैन",
        "Mode epeler emoji":
            "MAEL ले इमोजी प्रशोधन गर्दैन",
        "Mode mp3 telechargement ":
            "अडियो डाउनलोड हुँदैछ...",
        "Mode mp3 erreur ":
            "डाउनलोड त्रुटि...",
    },
    # Norvégien
    "no": {
        "Mode cacher": "Lytt godt.",
        "Mode dicter": "Skriv ned diktatet.",
        "Mode Epeler": "Lytt til bokstavene.",
        "Mode epeler non implemente":
            "Stavemodus er ennå ikke implementert på dette språket",
        "Mode epeler emoji":
            "MAEL behandler ikke emojier",
        "Mode mp3 telechargement ":
            "Laster ned lyd...",
        "Mode mp3 erreur ":
            "Nedlastingsfeil...",
    },
    # Polonais
    "pl": {
        "Mode cacher": "Słuchaj uważnie.",
        "Mode dicter": "Zapisz dyktando.",
        "Mode Epeler": "Słuchaj liter.",
        "Mode epeler non implemente":
            "Tryb literowania nie został jeszcze zaimplementowany w tym języku",
        "Mode epeler emoji":
            "MAEL nie przetwarza emoji",
        "Mode mp3 telechargement ":
            "Pobieranie dźwięku...",
        "Mode mp3 erreur ":
            "Błąd pobierania...",
    },
    # Portugais
    "pt": {
        "Mode cacher": "Escuta bem.",
        "Mode dicter": "Escreve o ditado.",
        "Mode Epeler": "Escuta as letras.",
        "Mode epeler non implemente":
            "Modo soletrar ainda não implementado neste idioma",
        "Mode epeler emoji":
            "O MAEL não processa emojis",
        "Mode mp3 telechargement ":
            "Baixando áudio...",
        "Mode mp3 erreur ":
            "Erro de download...",
    },
    # Pendjabi
    "pa": {
        "Mode cacher": "ਧਿਆਨ ਨਾਲ ਸੁਣੋ।",
        "Mode dicter": "ਸ਼੍ਰੁਤਲੇਖ ਲਿਖੋ।",
        "Mode Epeler": "ਅੱਖਰ ਸੁਣੋ।",
        "Mode epeler non implemente":
            "ਇਸ ਭਾਸ਼ਾ ਵਿੱਚ ਸਪੈਲਿੰਗ ਮੋਡ ਅਜੇ ਲਾਗੂ ਨਹੀਂ ਕੀਤਾ ਗਿਆ",
        "Mode epeler emoji":
            "MAEL ਇਮੋਜੀ ਨੂੰ ਪ੍ਰੋਸੈਸ ਨਹੀਂ ਕਰਦਾ",
        "Mode mp3 telechargement ":
            "ਆਡੀਓ ਡਾਊਨਲੋਡ ਹੋ ਰਿਹਾ ਹੈ...",
        "Mode mp3 erreur ":
            "ਡਾਊਨਲੋਡ ਗਲਤੀ...",
    },
    # Roumain
    "ro": {
        "Mode cacher": "Ascultă bine.",
        "Mode dicter": "Scrie dictarea.",
        "Mode Epeler": "Ascultă literele.",
        "Mode epeler non implemente":
            "Modul de silabisire nu este încă implementat în această limbă",
        "Mode epeler emoji":
            "MAEL nu procesează emoji",
        "Mode mp3 telechargement ":
            "Se descarcă audio...",
        "Mode mp3 erreur ":
            "Eroare de descărcare...",
    },
    # Russe
    "ru": {
        "Mode cacher": "Слушай внимательно.",
        "Mode dicter": "Запиши диктант.",
        "Mode Epeler": "Слушай буквы.",
        "Mode epeler non implemente":
            "Режим произношения по буквам ещё не реализован в этом языке",
        "Mode epeler emoji":
            "MAEL не обрабатывает эмодзи",
        "Mode mp3 telechargement ":
            "Загрузка аудио...",
        "Mode mp3 erreur ":
            "Ошибка загрузки...",
    },
    # Serbe
    "sr": {
        "Mode cacher": "Slušaj pažljivo.",
        "Mode dicter": "Napiši diktat.",
        "Mode Epeler": "Slušaj slova.",
        "Mode epeler non implemente":
            "Način sricanja još nije implementiran na ovom jeziku",
        "Mode epeler emoji":
            "MAEL ne obrađuje emodžije",
        "Mode mp3 telechargement ":
            "Preuzimanje zvuka...",
        "Mode mp3 erreur ":
            "Greška pri preuzimanju...",
    },
    # Cingalais
    "si": {
        "Mode cacher": "හොඳින් සවන් දෙන්න.",
        "Mode dicter": "අක්ෂර වින්‍යාසය ලියන්න.",
        "Mode Epeler": "අකුරුවලට සවන් දෙන්න.",
        "Mode epeler non implemente":
            "මෙම භාෂාවේ අක්ෂර වින්‍යාස මාදිලිය තවම ක්‍රියාත්මක කර නැත",
        "Mode epeler emoji":
            "MAEL ඉමෝජි සකසයන්නේ නැත",
        "Mode mp3 telechargement ":
            "ශ්‍රව්‍ය බාගත වෙමින්...",
        "Mode mp3 erreur ":
            "බාගැනීමේ දෝෂය...",
    },
    # Slovaque
    "sk": {
        "Mode cacher": "Počúvaj pozorne.",
        "Mode dicter": "Napíš diktát.",
        "Mode Epeler": "Počúvaj písmená.",
        "Mode epeler non implemente":
            "Režim hláskovania zatiaľ nie je v tomto jazyku implementovaný",
        "Mode epeler emoji":
            "MAEL nespracúva emoji",
        "Mode mp3 telechargement ":
            "Sťahovanie zvuku...",
        "Mode mp3 erreur ":
            "Chyba sťahovania...",
    },
    # Espagnol
    "es": {
        "Mode cacher": "Escucha bien.",
        "Mode dicter": "Escribe el dictado.",
        "Mode Epeler": "Escucha las letras.",
        "Mode epeler non implemente":
            "Modo deletrear aún no implementado en este idioma",
        "Mode epeler emoji":
            "MAEL no procesa los emojis",
        "Mode mp3 telechargement ":
            "Descargando audio...",
        "Mode mp3 erreur ":
            "Error de descarga...",
    },
    # Soundanais
    "su": {
        "Mode cacher": "Dangukeun saé.",
        "Mode dicter": "Tulis dikteuna.",
        "Mode Epeler": "Dangukeun hurup-hurupna.",
        "Mode epeler non implemente":
            "Mode éjahan can digunakeun dina ieu basa",
        "Mode epeler emoji":
            "MAEL henteu ngolah emoji",
        "Mode mp3 telechargement ":
            "Ngundeur audio...",
        "Mode mp3 erreur ":
            "Kasalahan undeuran...",
    },
    # Suédois
    "sv": {
        "Mode cacher": "Lyssna noga.",
        "Mode dicter": "Skriv ner diktamen.",
        "Mode Epeler": "Lyssna på bokstäverna.",
        "Mode epeler non implemente":
            "Stavningsläget är ännu inte implementerat på detta språk",
        "Mode epeler emoji":
            "MAEL bearbetar inte emojier",
        "Mode mp3 telechargement ":
            "Laddar ner ljud...",
        "Mode mp3 erreur ":
            "Nedladdningsfel...",
    },
    # Swahili
    "sw": {
        "Mode cacher": "Sikiliza vizuri.",
        "Mode dicter": "Andika imla.",
        "Mode Epeler": "Sikiliza herufi.",
        "Mode epeler non implemente":
            "Hali ya tahajia bado haijatekelezwa katika lugha hii",
        "Mode epeler emoji":
            "MAEL haichakati emoji",
        "Mode mp3 telechargement ":
            "Inapakua sauti...",
        "Mode mp3 erreur ":
            "Hitilafu ya upakuaji...",
    },
    # Tamoul
    "ta": {
        "Mode cacher": "நன்றாகக் கேள்.",
        "Mode dicter": "எழுத்துப்பிழை எழுது.",
        "Mode Epeler": "எழுத்துக்களைக் கேள்.",
        "Mode epeler non implemente":
            "இந்த மொழியில் எழுத்துப்பிழை பயன்முறை இன்னும் செயல்படுத்தப்படவில்லை",
        "Mode epeler emoji":
            "MAEL வரைபடக்குறியீடுகளை செயலாக்குவதில்லை",
        "Mode mp3 telechargement ":
            "ஒலி பதிவிறக்கப்படுகிறது...",
        "Mode mp3 erreur ":
            "பதிவிறக்கப் பிழை...",
    },
    # Télougou
    "te": {
        "Mode cacher": "జాగ్రత్తగా వినండి.",
        "Mode dicter": "డిక్టేషన్ రాయండి.",
        "Mode Epeler": "అక్షరాలను వినండి.",
        "Mode epeler non implemente":
            "ఈ భాషలో స్పెల్లింగ్ మోడ్ ఇంకా అమలు చేయబడలేదు",
        "Mode epeler emoji":
            "MAEL ఎమోజీలను ప్రాసెస్ చేయదు",
        "Mode mp3 telechargement ":
            "ఆడియో డౌన్‌లోడ్ అవుతోంది...",
        "Mode mp3 erreur ":
            "డౌన్‌లోడ్ లోపం...",
    },
    # Thaï
    "th": {
        "Mode cacher": "ฟังให้ดี",
        "Mode dicter": "เขียนตามคำบอก",
        "Mode Epeler": "ฟังตัวอักษร",
        "Mode epeler non implemente":
            "โหมดการสะกดยังไม่ได้ใช้งานในภาษานี้",
        "Mode epeler emoji":
            "MAEL ไม่ประมวลผลอีโมจิ",
        "Mode mp3 telechargement ":
            "กำลังดาวน์โหลดเสียง...",
        "Mode mp3 erreur ":
            "ข้อผิดพลาดในการดาวน์โหลด...",
    },
    # Turc
    "tr": {
        "Mode cacher": "Dikkatle dinle.",
        "Mode dicter": "Dikteyi yaz.",
        "Mode Epeler": "Harfleri dinle.",
        "Mode epeler non implemente":
            "Heceleme modu bu dilde henüz uygulanmadı",
        "Mode epeler emoji":
            "MAEL emojileri işlemez",
        "Mode mp3 telechargement ":
            "Ses indiriliyor...",
        "Mode mp3 erreur ":
            "İndirme hatası...",
    },
    # Ukrainien
    "uk": {
        "Mode cacher": "Слухай уважно.",
        "Mode dicter": "Запиши диктант.",
        "Mode Epeler": "Слухай літери.",
        "Mode epeler non implemente":
            "Режим промовляння по літерах ще не реалізовано в цій мові",
        "Mode epeler emoji":
            "MAEL не обробляє емодзі",
        "Mode mp3 telechargement ":
            "Завантаження аудіо...",
        "Mode mp3 erreur ":
            "Помилка завантаження...",
    },
    # Ourdou
    "ur": {
        "Mode cacher": "غور سے سنو۔",
        "Mode dicter": "املا لکھو۔",
        "Mode Epeler": "حروف سنو۔",
        "Mode epeler non implemente":
            "اس زبان میں ہجے کا موڈ ابھی نافذ نہیں کیا گیا",
        "Mode epeler emoji":
            "MAEL ایموجی پر کارروائی نہیں کرتا",
        "Mode mp3 telechargement ":
            "آڈیو ڈاؤن لوڈ ہو رہی ہے...",
        "Mode mp3 erreur ":
            "ڈاؤن لوڈ کی خرابی...",
    },
    # Vietnamien
    "vi": {
        "Mode cacher": "Hãy nghe kỹ.",
        "Mode dicter": "Viết chính tả.",
        "Mode Epeler": "Nghe các chữ cái.",
        "Mode epeler non implemente":
            "Chế độ đánh vần chưa được triển khai trong ngôn ngữ này",
        "Mode epeler emoji":
            "MAEL không xử lý emoji",
        "Mode mp3 telechargement ":
            "Đang tải âm thanh...",
        "Mode mp3 erreur ":
            "Lỗi tải xuống...",
    },
    # Gallois
    "cy": {
        "Mode cacher": "Gwrando'n ofalus.",
        "Mode dicter": "Ysgrifenna'r ddyfarniad.",
        "Mode Epeler": "Gwrando ar y llythyren.",
        "Mode epeler non implemente":
            "Nid yw'r modd sillafu wedi'i weithredu yn yr iaith hon eto",
        "Mode epeler emoji":
            "Nid yw MAEL yn prosesu emojis",
        "Mode mp3 telechargement ":
            "Yn llwytho sain i lawr...",
        "Mode mp3 erreur ":
            "Gwall llwytho i lawr...",
    },
}


def get_mode_message(mode_key: str, lang: str | None) -> str:
    """
    Retourne le message localisé associé à ``mode_key`` pour la langue ``lang``.

    Paramètres
    ----------
    mode_key : str
        Clé interne du message, par ex. ``"Mode cacher"``,
        ``"Mode dicter"``, ``"Mode Epeler"``, ``"Mode epeler non
        implemente"`` ou ``"Mode epeler emoji"``.
    lang : str | None
        Code langue ou variante (par ex. ``"fr"``, ``"frCH"``,
        ``"es"``). La fonction normalise en extrayant les deux
        premières lettres en minuscules.

    Retour
    ------
    str
        Le texte traduit. Si la langue ou la clé est absente du
        dictionnaire, repli sur le français (``"fr"``).
    """
    # Langue absente ou None : repli direct.
    if not lang:
        lang_short = "fr"
    else:
        # ``"frCH"`` -> ``"fr"``, ``"EN"`` -> ``"en"``, ``"es"`` -> ``"es"``.
        lang_short = lang[:2].lower() if len(lang) >= 2 else lang.lower()

    # Recherche dans la langue demandée, sinon repli français.
    table = traductions.get(lang_short, traductions.get("fr", {}))
    if mode_key in table:
        return table[mode_key]

    # Repli français global.
    fallback = traductions.get("fr", {})
    if mode_key in fallback:
        return fallback[mode_key]

    # Dernier recours : on retourne la clé brute plutôt que None.
    return mode_key
