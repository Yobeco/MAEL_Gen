"""Affichage provisoire des paramètres Wi-Fi MAEL, sans configuration système."""

from __future__ import annotations

import platform
from pathlib import Path

from qr_dto import WifiItem


class WifiSetup:
    """Reçoit les paramètres Wifi; l'application réseau reste à implémenter."""

    def __init__(self) -> None:
        self.is_raspberry_pi = self._detect_raspberry_pi()

    @staticmethod
    def _detect_raspberry_pi() -> bool:
        """Détecte un Raspberry Pi à partir du modèle exposé par Linux."""
        if platform.system() != "Linux":
            return False
        for model_path in (
            Path("/proc/device-tree/model"),
            Path("/sys/firmware/devicetree/base/model"),
        ):
            try:
                model = model_path.read_text(errors="ignore").replace("\x00", "")
            except OSError:
                continue
            if "raspberry pi" in model.lower():
                return True
        return False

    def apply(self, item: WifiItem) -> None:
        """Trace les champs non sensibles; ne change jamais le réseau sur PC."""
        # Même si une valeur non-secrète contient par accident le mot de passe,
        # on le masque pour garantir son absence de la sortie console.
        def safe(value: object) -> str:
            rendered = str(value)
            if item.password:
                rendered = rendered.replace(item.password, "[masqué]")
            return rendered

        print(
            "WifiSetup (Raspberry Pi)" if self.is_raspberry_pi else "WifiSetup (PC)",
            f"ssid={safe(item.ssid)}",
            f"type={safe(item.type)}",
            f"hide={safe(item.hide)}",
        )

        if self.is_raspberry_pi:
            # TODO: implémenter la configuration via nmcli selon la distribution.
            # TODO: prévoir une alternative wpa_supplicant pour les systèmes adaptés.
            pass
        # Sur PC, cette classe est strictement en lecture seule: aucune commande
        # système ni écriture de configuration n'est exécutée.
