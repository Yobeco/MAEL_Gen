"""Tests sans réseau ni périphérique audio du lecteur miniaudio local."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path

SOURCE = Path(__file__).with_name("mp3_read.py")


def load_reader_module():
    spec = importlib.util.spec_from_file_location("mp3_read_deadlock_under_test", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_miniaudio(reader_box):
    state = {"devices": [], "lock_checks": [], "auto_finish": False}
    module = types.ModuleType("miniaudio")

    def check_lock_free(operation):
        if not reader_box:
            return
        reader = reader_box[0]
        got = reader._lock.acquire(timeout=0.2)
        state["lock_checks"].append((operation, got))
        if got:
            reader._lock.release()
        else:
            raise AssertionError(f"_lock détenu pendant {operation}")

    class Samples:
        def __getitem__(self, _slice):
            check_lock_free("pcm callback")
            return self

        def tobytes(self):
            check_lock_free("pcm callback bytes")
            return b"\x01\x02\x03\x04"

    class Decoded:
        sample_format = "s16"
        nchannels = 2
        sample_rate = 44100
        num_frames = 8
        samples = Samples()

    def decode_file(path):
        check_lock_free("decode_file")
        if not Path(path).is_file():
            raise FileNotFoundError(path)
        return Decoded()

    class PlaybackDevice:
        def __init__(self, **kwargs):
            check_lock_free("PlaybackDevice.__init__")
            self.kwargs = kwargs
            self.start_entered = threading.Event()
            self.release_start = threading.Event()
            self.produced = []
            self.stopped = False
            self.closed = False
            state["devices"].append(self)

        def start(self, stream):
            check_lock_free("start")
            self.produced.append(stream.send(4))
            self.start_entered.set()
            if state["auto_finish"]:
                try:
                    while True:
                        self.produced.append(stream.send(4))
                except StopIteration:
                    return
            self.release_start.wait(2.0)

        def stop(self):
            check_lock_free("stop")
            self.stopped = True
            self.release_start.set()

        def close(self):
            check_lock_free("close")
            self.closed = True

    module.decode_file = decode_file
    module.PlaybackDevice = PlaybackDevice
    return module, state


class DeadlockRegressionTests(unittest.TestCase):
    def setUp(self):
        self.reader_box = []
        self.fake_miniaudio, self.state = make_miniaudio(self.reader_box)
        self.previous_miniaudio = sys.modules.get("miniaudio")
        sys.modules["miniaudio"] = self.fake_miniaudio
        self.module = load_reader_module()
        self.reader = self.module.MiniaudioMp3Reader()
        self.reader_box.append(self.reader)
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = Path(self.tempdir.name) / "local.mp3"
        self.path.write_bytes(b"not decoded by a real codec")

    def tearDown(self):
        self.reader.stop()
        self.tempdir.cleanup()
        sys.modules.pop("mp3_read_deadlock_under_test", None)
        if self.previous_miniaudio is None:
            sys.modules.pop("miniaudio", None)
        else:
            sys.modules["miniaudio"] = self.previous_miniaudio

    def _wait_for_device(self, count=1):
        deadline = time.monotonic() + 1.0
        while time.monotonic() < deadline:
            if len(self.state["devices"]) >= count and self.state["devices"][count - 1].start_entered.is_set():
                return self.state["devices"][count - 1]
            time.sleep(0.005)
        self.fail("PlaybackDevice.start() n'a pas été appelé.")

    def test_stop_under_one_second_wait_and_all_audio_calls_unlocked(self):
        self.reader.play(str(self.path))
        device = self._wait_for_device()
        self.assertEqual(device.produced, [b"\x01\x02\x03\x04"])
        self.assertTrue(self.reader.is_playing)

        started = time.monotonic()
        self.reader.stop()
        elapsed = time.monotonic() - started
        self.assertLess(elapsed, 1.0, f"stop() a pris {elapsed:.3f} s")
        self.assertTrue(device.stopped)
        self.assertTrue(self.reader.wait(0.2), "wait() n'a pas vu la fin après stop().")
        self.assertFalse(self.reader.is_playing)
        self.assertTrue(self.state["lock_checks"])
        self.assertTrue(all(ok for _, ok in self.state["lock_checks"]), self.state["lock_checks"])

    def test_replay_uses_new_events_and_callbacks_do_not_take_lock(self):
        for expected_device_count in (1, 2):
            self.reader.play(str(self.path))
            device = self._wait_for_device(expected_device_count)
            self.assertEqual(device.produced, [b"\x01\x02\x03\x04"])
            self.reader.stop()
            self.assertTrue(self.reader.wait(0.2))
        self.assertEqual(len(self.state["devices"]), 2)
        self.assertTrue(all(ok for _, ok in self.state["lock_checks"]), self.state["lock_checks"])

    def test_wait_reports_natural_end(self):
        self.state["auto_finish"] = True
        self.reader.play(str(self.path))
        self.assertTrue(self.reader.wait(1.0), "wait() n'a pas signalé la fin normale.")
        self.assertFalse(self.reader.is_playing)
        self.assertEqual(self.state["devices"][0].produced[-1], b"\x01\x02\x03\x04")
        self.assertTrue(all(ok for _, ok in self.state["lock_checks"]), self.state["lock_checks"])

    def test_rejects_remote_or_non_mp3_path(self):
        with self.assertRaises(ValueError):
            self.reader.play("https://example.invalid/audio.mp3")
        txt = Path(self.tempdir.name) / "local.txt"
        txt.write_text("no audio")
        with self.assertRaises(ValueError):
            self.reader.play(str(txt))


if __name__ == "__main__":
    unittest.main(verbosity=2)
