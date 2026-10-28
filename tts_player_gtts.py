"""Moteur gTTS produisant des fichiers MP3, sans gestion de lecture."""

from __future__ import annotations

import hashlib
import os
import tempfile
import threading
from pathlib import Path

from tts_player import TtsPlayer


class GttsPlayer(TtsPlayer):
    """Synthèse gTTS avec cache persistant sur disque."""

    def __init__(self, cache_dir: str | os.PathLike[str] | None = None) -> None:
        self.cache_dir = Path(cache_dir or (Path(tempfile.gettempdir()) / "mael_gtts_cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[tuple[str, str, bool], str] = {}
        self._lock = threading.RLock()

    def synthesize(self, text: str, lang: str, slow: bool = False) -> str:
        """Synthétise le texte et renvoie le chemin du MP3 mis en cache."""
        if not isinstance(text, str) or not isinstance(lang, str) or not lang:
            raise ValueError("Un texte et un code de langue sont requis.")
        key = (text, lang, bool(slow))
        with self._lock:
            cached = self._cache.get(key)
            if cached and Path(cached).is_file():
                return cached
            digest = hashlib.sha256(
                (lang + "\0" + str(bool(slow)) + "\0" + text).encode("utf-8")
            ).hexdigest()
            target = self.cache_dir / f"{digest}.mp3"
            if not target.is_file():
                from gtts import gTTS
                fd, temporary = tempfile.mkstemp(prefix=".mael-", suffix=".mp3", dir=self.cache_dir)
                os.close(fd)
                try:
                    gTTS(text=text, lang=lang, slow=bool(slow)).save(temporary)
                    os.replace(temporary, target)
                finally:
                    if os.path.exists(temporary):
                        os.unlink(temporary)
            self._cache[key] = str(target)
            return str(target)
