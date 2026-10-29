# -*- coding: utf-8 -*-
"""
test_list.py
============

Données purement statiques pour les tests / démonstrations.
AUCUN import (ni stdlib, ni métier) : ce module doit pouvoir
être chargé partout sans déclencher d'effet de bord.

Exposé
------
strings_to_obfus : tuple[str, ...]
    Tuple de 21 chaînes de caractères représentatives des
    contenus qui pourraient être stockés dans de vrais codes QR.
    Les deux entrées ``<es>`` et ``<en>`` utilisent les guillemets
    courbes (``“ ”``) explicites (U+201C / U+201D) — pas de
    guillemets typographiques ambigus.
"""

strings_to_obfus = (
    # "C'est ce que l'on dit...#d",
    # "/gd/1IHf9ayDGjCthJhKmzstr0ZUUvZVcJH8P",
    # "WIFI:T:WPA;S:CLARO1_F53E79;P:c024ZwRKpG;H:;;",
    # "C'est ce que l'on dit…#d",
    # "Ils aiment ça parce que c'est bon !#d",
    # "Où vas-tu Zaïn ?#d",
    # "Coucou tout le monde !#e",
    # "Ça va les élèves ?",
    # "Un maître à œil vif.#c",
    # "C’eût été drôle pour Æsius.#e",
    # "Une île",
    # "<frCH>À Noël, l'œuf est dans l'âtre contre le mûr de la façade.",
    # "<frBE>Est-ce que le caractère ~ est accepté ?#e",
    # "<frCA>El niño est fort à Managua.",
    # "Du maïs à Noël !",
    # "<es>« Qué lindo »",
    "<en>She says: “That's nice!”",
    # "<ko>안녕하세요! 제 이름은... 입니다. 만나서 반갑습니다.",
    # "<ko>입니다. 만나서  반갑습니다.#e",
    # "<ja>クレジットカードではらいます。",
    # "<zh>書左僕射燕國公張說 製若夫玉毫流照｡甘露灑于大千｡金鏡揚暉｡",
    # "<ru>У меня большая семья из шести человек: я, мама",
    # "<el>Τὴν εὐγενεστάτην ὄλυραν, ὅταν ὡς χρὴ",
)
