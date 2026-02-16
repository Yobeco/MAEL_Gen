
![MAEL](./readme_assets/Logo-MAEL-120.png "MAEL project logo")

# MAEL Gen

*An application belonging to the [__MAEL project__](https://github.com/Yobeco/MAEL_Project)*   

Copyright (c) 2022 Yonnel Bécognée

[![License: Libre Non Commerciale](https://img.shields.io/badge/license-GNU%20GENERAL%20PUBLIC%20LICENSE%20V3-white.svg)](./LICENSE)

[![Python](https://img.shields.io/badge/Python-V3.10%2B-blue?logo=python&logoColor=yellow)](https://www.python.org/)

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-009900.svg)](#contributing) [![Beginner friendly](https://img.shields.io/badge/Beginner%20friendly-FF8000)]()

[![Status: Active](https://img.shields.io/badge/status-active-009900.svg)]()

## :fr: [Français](https://github.com/Yobeco/MAEL_Gen/blob/main/README.fr.md) | :es: [Español](https://github.com/Yobeco/MAEL_Gen/blob/main/README.es.md) | :gb: English

---

![ScreenShot](https://raw.githubusercontent.com/Yobeco/MAEL_Project/refs/heads/main/readme_assets/MAEL_Gen.png)

## A- Description :eye:

:computer: **Cross-platform desktop application** (Linux, macOS, and Windows) that allows teachers to easily create QR codes containing text that their students can listen to.  

They can integrate them into their various teaching materials, thus adding an **audio dimension** :ear: to their paper documents.

The QR codes will be scanned by students using the **MAEL Scan** application :speaker: (available on Android <img src="https://cdn.simpleicons.org/android/808080" width="24" height="24" style="vertical-align: middle;" /> and soon on iOS <img src="https://cdn.simpleicons.org/apple/808080" width="24" height="24" style="vertical-align: middle;" />).

---

## B- Features :clipboard:

- **"Read" mode**: displays and reads aloud the text contained in the QR code.

- **"Dictate" mode**: does not display the text but reads aloud the text contained in the QR code.

- **"Spell" mode**: reads aloud each letter of the text contained in the QR code.

- **"MP3" mode**: plays a file from Google Drive.

- **Special MP3 sounds**: these are sounds from the Borel-Maisonny method and the Consigny Alphabet Book (created by the AMLA Nort area).

- **55 supported languages** (except for the "spell" mode for the moment).

:fr: :gb: :es: :portugal: :brazil: :it: :de: :ru: :jp: :cn: :kr: ...

## C- How to use MAEL Gen? :blush:

### 1- Use a synthetic voice :speaking_head:

1. Launch **MAEL Gen**

2. Enter the text you want to be spoken in the text field (type it, or use `Ctrl + v`, or simply `right-click`)

3. Choose the language (menu `Language`) of your text.

4. Choose the mode (menu `Settings`) according to your objective.

5. Adjust the size of the QR code (field `Size` or slider)

6. Paste it into your document: LibreOffice Writer <img src="https://cdn.simpleicons.org/libreofficewriter/808080" width="24" height="24" style="vertical-align: middle;" />, Draw <img src="https://cdn.simpleicons.org/libreofficedraw/808080" width="24" height="24" style="vertical-align: middle;" />, or any other editor...

*⟶ The student will then only have to scan this code with __MAEL Scan__ to listen to the content :headphones:...*

### 2- Use an MP3 file

1. Upload an .mp3 file :microphone: to your Google Drive account <img src="https://cdn.simpleicons.org/googledrive/808080" width="24" height="24" style="vertical-align: middle;" />

2. **Share** the folder containing the .mp3 file **with anyone who has the link**.

3. Retrieve the sharing link.

4. Paste this link into MAEL Gen.

5. Adjust the size (field `Size` or slider).

*⟶ The student will then only have to scan this code with __MAEL Scan__ to listen to the MP3 file :headphones:: a poem, a dialogue...*

More information:

![](./readme_assets/Aide-V4.png)

---

## D- Operating principle :gear:

*(To help understand the code)*

---

**:one: On first launch**

When writing in the text input, the default language is "French" :fr: and the default mode is "Read":

1- The text first undergoes light "encryption".

2- A QR code containing this text (`utf-8`) is generated.

*⟶ By default, __MAEL Scan__ will understand that it is in __read mode__ and will use the French synthetic voice :fr:.*

---

**:two: If you change the _language_ of the content, for example _Italian_ :it:** :

1- The text to be placed in the QR code receives a prefix such as `<it>`

2- The text (with its prefix) first undergoes light "encryption".

3- A QR code containing this text (`utf-8`) is generated.

*⟶ __MAEL Scan__ remains in __read mode__ but will this time use the __Italian__ synthetic voice :it:.*

---

**:three: If you switch to *dictate mode* :**

1- The text keeps its prefix such as `<it>`

2- The text receives a suffix such as `#d`

2- The text (with its prefix and suffix) first undergoes light "encryption".

3- A QR code containing this text (`utf-8`) is generated.

*⟶ __MAEL Scan__ will this time understand that it is in __dictate mode__ and will use the __Italian__ synthetic voice :it:.*

---

:speaking_head: The synthetic voices are those generated by the phone. (`GTTS` on Android)

:warning: Some languages have several possible voices. The prefix will then be longer. For example:

| Voice | Prefix |
| ----------- | ----------- |
| Portuguese from Portugal :portugal: | `<ptPRT>` |
| Portuguese from Brazil :brazil: | `<ptBRA>` |

:bookmark_tabs: [See the list of GTTS languages (Probably needs updating...)](./readme_assets/Langues_GTTS.pdf)

---

**:four: On each modification:**

A `.png` file corresponding to the QR code is generated and automatically sent to the clipboard. :clipboard:

(A small icon indicates whether there is a QR code or text in the clipboard)

*⟶ The teacher only has to `Paste` it into their personal editor.*

---

## E- Features to be developed :rocket:

1- **"Dictate" mode**

- The current _**"Dictate mode"**_ (speaking the text without displaying it) will change its name and be called **"Hide mode"**. :arrows_counterclockwise:

- The new _**"Dictate mode"**_ will include:

    - reading the text without displaying it,
    - speaking the punctuation, and
    - displaying the play-pause menu :play_or_pause_button: (with scroll bar).

2- **"MP3" mode**

- Creation of a **MAEL Cloud** :cloud: with fewer limitations than Google Drive (hosted with the **MAEL Phrase** platform).

- Addition of an option (suffix) that will indicate to **MAEL Scan** that it must keep the MP3 file :inbox_tray: so as not to have to re-download it if it is scanned again.

3- **Interface**

- Replacement of TKinter with **TTKBootstrap**

- **Moving the 4 mode-switch buttons** from the “Settings” menu to the location of the size slider (which will be removed).

- Management of right-to-left languages :arrow_left: such as Arabic or Hebrew.

4- **Batch verification of QR codes**

When creating a document containing several QR codes, it becomes easier to make mistakes (for example, placing the same QR code twice... :sweat_smile: ).

I therefore started creating a quick QR code verification function.

1. Will propose taking a screenshot of the document to be checked

2. Will detect the QR codes in the captured image

3. Will add to the image the text of each QR code found

I started with **TKinter** for the interface to select the area to capture (already used by MAEL Gen), **mss** for the capture itself, and possibly **OpenCV** for detecting and reading QR codes.

### :+1: Offer your help to develop one of these features :smile:

---

# F- :open_hands: Take part in the MAEL project <img src="https://raw.githubusercontent.com/Yobeco/MAEL_Project/refs/heads/main/readme_assets/MAEL.svg" alt="MAEL Logo" width="40" height="40" /> !

:ring_buoy: To **get help** regarding the use of **MAEL Gen** or to **participate in development** :computer:, write to me here:

### :mailbox_with_mail: ***[mael@lvh.edu.ni](mailto:mael@lvh.edu.ni)***

### :star2: Contributors

Many thanks to all the people who will contribute to this project!

| Avatar | Name               | GitHub                          | Role                     |
|--------|--------------------|---------------------------------|--------------------------|
| [<img src="https://github.com/YoBeco.png" width="50" style="border-radius: 50%;">](https://github.com/YoBeco) | Bécognée Yonnel | [@Yobeco](https://github.com/Yobeco) | Maintainer |
| [<img src="https://github.com/Nail-yk.png" width="50" style="border-radius: 50%;">](https://github.com/Nail-yk) | Padawan         | [@Nail-yk](https://github.com/Nail-yk) | Documentation translation |
| ... | ... | ... | Python developer |

---

## G- Installation :arrow_heading_down:

To try **MAEL Gen**, run the script:

```bash
git clone https://github.com/Yobeco/MAEL_Gen.git
cd MAEL_Gen
python3 -m venv mael_venv
source mael_venv/bin/activate
pip install -r requirements.txt
python3 MAEL_V5.0.py
```