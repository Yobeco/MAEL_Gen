"""Construction des URL d’accès aux fichiers audio hébergés sur un cloud."""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

# Les fournisseurs non implémentés sont documentés en section B-2 du projet.
# Le format d’identifiant opaque et les URL publiques devront être confirmés
# avec l’instance NextCloud / La Suite retenue avant d’activer ces entrées.
FOURNISSEURS: dict[str, dict[str, str] | None] = {
    "gd": {"nom": "Google Drive", "url": "https://drive.google.com/uc?export=download&id={id}"},
    # "nc": None,  # NextCloud : URL directe dépendante de l’instance / partage.
    # "ls": None,  # La Suite : fournisseur et format d’URL à confirmer.
}


def build_url(cloud_item: Any) -> str:
    """Reconstruit l’URL du fichier à partir d’un CloudItem (`mode`, `id`).

    L’identifiant du QR est conservé opaque et encodé comme paramètre URL.
    """
    mode = getattr(cloud_item, "mode", None)
    opaque_id = getattr(cloud_item, "id", None)
    if not isinstance(mode, str) or not isinstance(opaque_id, str) or not opaque_id:
        raise ValueError("CloudItem invalide : mode et id non vides sont requis.")
    fournisseur = FOURNISSEURS.get(mode)
    if fournisseur is None:
        if mode in {"nc", "ls"}:
            raise NotImplementedError(f"Le fournisseur {mode!r} est réservé mais non configuré.")
        raise ValueError(f"Fournisseur cloud inconnu : {mode!r}")
    template = fournisseur["url"]
    # Utiliser urlencode pour préserver l’ID opaque dans le paramètre `id`.
    if "?" not in template:
        return template.format(id=opaque_id)
    base, query = template.split("?", 1)
    values = dict(part.split("=", 1) for part in query.split("&") if "=" in part)
    values["id"] = opaque_id
    return f"{base}?{urlencode(values)}"


# Alias francophone pratique, tout en conservant le nom public build_url.
construire_url = build_url
