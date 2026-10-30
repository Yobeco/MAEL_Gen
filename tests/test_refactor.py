"""Tests sans réseau ni carte son pour la séparation des responsabilités audio."""
from __future__ import annotations

import importlib
import os
import sys
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent
SOURCE = Path("/mnt/user-data/uploads")
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT))


def _stub_module(name: str, attrs: dict | None = None) -> None:
    module = types.ModuleType(name)
    for key, value in (attrs or {}).items():
        setattr(module, key, value)
    sys.modules.setdefault(name, module)


# Modules purement matériels optionnels : leur import n'est pas nécessaire aux tests.
_stub_module("cv2")
_stub_module("zxingcpp")
_stub_module("miniaudio")
_stub_module("gtts", {"gTTS": object})


class FakeReader:
    def __init__(self):
        self.paths = []
        self.stops = 0
        self._playing = False
        self.wait_calls = 0
        self.started = threading.Event()
        self._done = threading.Event()
        self.auto_complete = True

    @property
    def is_playing(self):
        return self._playing

    def stop(self):
        self.stops += 1
        self._playing = False
        self._done.set()

    def play(self, path):
        self.paths.append(path)
        self._playing = True
        self.started.set()
        self._done.clear()
        if self.auto_complete:
            self._playing = False
            self._done.set()

    def wait(self, timeout=None):
        self.wait_calls += 1
        finished = self._done.wait(timeout)
        if finished:
            self._playing = False
        return finished


class FakeTts:
    def __init__(self):
        self.calls = []
        self.block_text = None
        self.entered = threading.Event()
        self.release = threading.Event()
        self.temp = tempfile.TemporaryDirectory()

    def synthesize(self, text, lang, slow=False):
        self.calls.append((text, lang, slow))
        if text == self.block_text:
            self.entered.set()
            self.release.wait(3)
        target = Path(self.temp.name) / f"{len(self.calls)}.mp3"
        target.write_bytes(b"mp3")
        return str(target)


class Scanner:
    def scan(self, source=None):
        return []


def make_item(mode="lire", text="bonjour"):
    from qr_dto import RawQr, TtsItem
    raw = RawQr(text=text, position=None, format="QRCode", ec_level=None)
    return TtsItem(raw=raw, original=text, text=text, lang="fr", mode=mode)


def make_setup(mode="lire", texts=("bonjour",), gds=()):
    from qr_dto import TtsSetup
    item = make_item(mode, " ".join(texts))
    return TtsSetup(item=item, mode=mode, lang="fr", to_pronounce=tuple(texts),
                    to_show="", list_gds=tuple(gds))


def wait_done(scan, timeout=3):
    thread = scan._thread
    if thread:
        thread.join(timeout)
    if thread and thread.is_alive():
        raise AssertionError("Le worker audio n'a pas terminé à temps")


class RefactorTests(unittest.TestCase):
    def test_imports_all_python_modules(self):
        # Les fichiers refactorisés des livrables prennent priorité sur les sources.
        sys.path.remove(str(ROOT))
        sys.path.insert(0, str(ROOT))
        changed = {"mael_scan", "mp3_fetch", "mp3_read", "tts_player", "tts_player_gtts"}
        for name in changed:
            sys.modules.pop(name, None)
        for name in changed:
            self.assertEqual(importlib.import_module(name).__file__, str(ROOT / f"{name}.py"))
        # Importer aussi les autres modules du dépôt, leurs dépendances matériel étant stubées.
        for path in SOURCE.glob("*.py"):
            if path.stem in changed or path.stem == "audio_" + "control":
                continue
            importlib.import_module(path.stem)

    def test_mp3_fetch_returns_file_without_playing(self):
        from mp3_fetch import Mp3Fetch
        from qr_dto import CloudItem, RawQr

        class Response:
            headers = {"Content-Length": "7"}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, size=-1):
                if hasattr(self, "sent"):
                    return b""
                self.sent = True
                return b"fake mp3"

        raw = RawQr(text="/gd/id", position=None, format="QRCode", ec_level=None)
        item = CloudItem(raw=raw, mode="gd", id="id", text="id")
        fetch = Mp3Fetch(opener=lambda *a, **k: Response())
        path = fetch.fetch(item)
        self.assertTrue(Path(path).is_file())
        self.assertEqual(Path(path).read_bytes(), b"fake mp3")
        self.assertFalse(hasattr(fetch, "mp3_read"))
        Path(path).unlink()

    def test_new_scan_interrupts_current_reader(self):
        import mael_scan
        reader, tts = FakeReader(), FakeTts()
        reader.auto_complete = False
        subject = mael_scan.MaelScan(tts, scanner=Scanner(), reader=reader)
        with patch("qr_parse.parse_all", side_effect=[[make_item()], []]):
            subject.scan()
            self.assertTrue(reader.started.wait(1))
            old_event = subject._cancel
            subject.scan()
        wait_done(subject)
        self.assertTrue(old_event.is_set())
        self.assertGreaterEqual(reader.stops, 1)
        self.assertFalse(reader.is_playing)
        tts.temp.cleanup()

    def test_slow_synthesis_result_is_discarded_after_new_scan(self):
        import mael_scan
        reader, tts = FakeReader(), FakeTts()
        tts.block_text = "bloque"
        subject = mael_scan.MaelScan(tts, scanner=Scanner(), reader=reader)
        old = make_setup(texts=("bloque",))
        subject._new_request()
        old_generation, old_event = subject._generation, subject._cancel
        worker = threading.Thread(target=subject._run_actions,
                                  args=([("tts", old)], old_generation, old_event))
        worker.start()
        self.assertTrue(tts.entered.wait(1))
        subject._new_request()
        tts.release.set()
        worker.join(2)
        self.assertEqual(reader.paths, [])
        tts.temp.cleanup()

    def test_repeat_and_slow_repeat(self):
        import mael_scan
        reader, tts = FakeReader(), FakeTts()
        subject = mael_scan.MaelScan(tts, scanner=Scanner(), reader=reader)
        subject.last_tts_setup = make_setup(texts=("encore",))
        subject.repeat()
        wait_done(subject)
        subject.repeat_slow()
        wait_done(subject)
        self.assertEqual(tts.calls, [("encore", "fr", False), ("encore", "fr", True)])
        tts.temp.cleanup()

    def test_dicter_chains_groups_with_pauses(self):
        import mael_scan
        reader, tts = FakeReader(), FakeTts()
        subject = mael_scan.MaelScan(tts, scanner=Scanner(), reader=reader)
        subject.PAUSE_FACT_NORMAL = 0.001
        subject.PAUSE_MIN = 0.01
        setup = make_setup("dicter", ("un", "deux"), ("un", "deux"))
        started = time.monotonic()
        subject._new_request()
        subject._run_actions([("tts", setup)], subject._generation, subject._cancel)
        elapsed = time.monotonic() - started
        self.assertEqual([call[0] for call in tts.calls], ["un", "deux"])
        self.assertEqual(len(reader.paths), 2)
        self.assertGreaterEqual(elapsed, 0.015)
        tts.temp.cleanup()

    def test_slow_dicter_repeats_each_gds_slowly(self):
        import mael_scan
        reader, tts = FakeReader(), FakeTts()
        subject = mael_scan.MaelScan(tts, scanner=Scanner(), reader=reader)
        subject.PAUSE_REPEAT = 0.001
        subject.PAUSE_FACT_SLOW = 0.001
        subject.PAUSE_MIN = 0.001
        setup = make_setup("dicter", ("un", "deux"), ("un", "deux"))
        subject._new_request()
        subject._run_actions([("tts", setup)], subject._generation, subject._cancel, True)
        self.assertEqual(tts.calls, [("un", "fr", False), ("un", "fr", True),
                                     ("deux", "fr", False), ("deux", "fr", True)])
        self.assertEqual(len(reader.paths), 4)
        tts.temp.cleanup()


if __name__ == "__main__":
    unittest.main()
