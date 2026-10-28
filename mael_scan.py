"""Orchestrateur minimal du flux MAEL Scan (acquisition, analyse, aiguillage)."""
from __future__ import annotations

from typing import Any

from qr_dto import CloudItem, TtsItem, TtsSetup, WifiItem
from wifi_setup import WifiSetup
from tts_setup import TtsSetupBuilder
import audio_control


class MaelScan:
    """Coordonne le scanner virtuel ou image, qr_parse et les sorties métier."""

    def __init__(self, tts_player: Any, wifi_setup: WifiSetup | None = None,
                 scanner: Any | None = None, mp3_fetch: Any | None = None,
                 on_audio_status: Any | None = None) -> None:
        self.tts_player = tts_player
        self.wifi_setup = wifi_setup or WifiSetup()
        self.scanner = scanner
        self.mp3_fetch = mp3_fetch
        self.on_audio_status = on_audio_status
        self.tts_setup_builder = TtsSetupBuilder()
        self.last_tts_item: TtsItem | None = None
        self.last_tts_setup: TtsSetup | None = None

    def scan(self, source: object | None = None) -> list[TtsItem | CloudItem | WifiItem]:
        """Scanne, parse tous les résultats, puis aiguille les DTO reconnus."""
        audio_control.stop_all()
        if self.scanner is None:
            from scanner_factory import create_scanner
            self.scanner = create_scanner("pc_pdf" if source is not None else None)
        raws = self.scanner.scan(source)
        from qr_parse import MODE_LIRE, parse_all
        items = parse_all(raws)
        for item in items:
            if isinstance(item, TtsItem):
                self.last_tts_item = item
                self.last_tts_setup = self.tts_setup_builder.build(item)
                self.tts_player.play(self.last_tts_setup)
            elif isinstance(item, WifiItem):
                wifi_tts_item = TtsItem(
                    raw=item.raw, original=item.raw.text, text="Code QR Wifi",
                    lang="fr", mode=MODE_LIRE,
                )
                from dataclasses import replace
                self.last_tts_setup = replace(
                    self.tts_setup_builder.build(wifi_tts_item),
                    mode=MODE_LIRE, lang="fr", list_gds=("Code QR Wifi",),
                    to_pronounce=("Code QR Wifi",), to_show="Code QR Wifi",
                )
                self.tts_player.play(self.last_tts_setup)
                self.wifi_setup.apply(item)
            elif isinstance(item, CloudItem):
                # Le lecteur est construit à la demande pour ne rien charger côté audio.
                from dataclasses import replace
                from qr_parse import MODE_LIRE
                status_item = TtsItem(
                    raw=item.raw, original=item.text, text=item.text, lang="fr", mode=MODE_LIRE
                )
                base_setup = self.tts_setup_builder.build(status_item)
                # TtsSetup n'a pas de champ to_say : to_pronounce vide garantit
                # une sortie uniquement visuelle via to_show, sans déclencher de TTS.
                def download_start() -> None:
                    if self.on_audio_status:
                        self.on_audio_status(replace(
                            base_setup, to_pronounce=(), to_show="Audio en téléchargement..."
                        ))
                def download_end() -> None:
                    if self.on_audio_status:
                        self.on_audio_status(replace(base_setup, to_pronounce=(), to_show=""))
                if self.mp3_fetch is None:
                    from mp3_fetch import Mp3Fetch
                    self.mp3_fetch = Mp3Fetch(
                        on_download_start=download_start, on_download_end=download_end
                    )
                else:
                    reader = getattr(self.mp3_fetch, "mp3_read", None)
                    if reader is not None:
                        reader.on_download_start = download_start
                        reader.on_download_end = download_end
                self.mp3_fetch.fetch(item)
        return items

    def repeat(self, slow: bool = False) -> None:
        """Rejoue le dernier TtsSetup (à vitesse normale ou lente)."""
        if self.last_tts_setup is not None:
            self.tts_player.play(self.last_tts_setup, slow=slow)

    def repeat_slow(self) -> None:
        """Relit le dernier TtsSetup à vitesse lente."""
        self.repeat(slow=True)


def scan(tts_player: Any, source: object | None = None,
         wifi_setup: WifiSetup | None = None,
         scanner: Any | None = None,
         mp3_fetch: Any | None = None) -> list[TtsItem | CloudItem | WifiItem]:
    """Point d'entrée fonctionnel pratique pour un scan ponctuel."""
    return MaelScan(
        tts_player, wifi_setup=wifi_setup, scanner=scanner, mp3_fetch=mp3_fetch
    ).scan(source)
