"""Tests unitaires de MaelController (sans écran ni dépendance audio)."""
import unittest

from mael_Scan_gui import MaelController


class FakeSetup:
    def __init__(self, to_show):
        self.to_show = to_show


class FakeScanService:
    def __init__(self):
        self.last_tts_setup = None
        self.calls = []
        self.next_setup = FakeSetup("Contenu à afficher")

    def scan(self):
        self.last_tts_setup = self.next_setup

    def repeat(self, slow=False):
        self.calls.append(slow)


class ControllerTests(unittest.TestCase):
    def test_repetition_inactive_before_scan(self):
        service = FakeScanService()
        controller = MaelController(service)
        self.assertFalse(controller.can_repeat)
        controller.on_repeat()
        self.assertEqual(service.calls, [])

    def test_scan_exposes_to_show_and_enables_repeat(self):
        controller = MaelController(FakeScanService())
        self.assertEqual(controller.on_scan(), "Contenu à afficher")
        self.assertTrue(controller.can_repeat)

    def test_repeat_normal_and_slow_delegate_to_scan_service(self):
        service = FakeScanService()
        controller = MaelController(service)
        controller.on_scan()
        controller.on_repeat()
        controller.on_repeat(slow=True)
        self.assertEqual(service.calls, [False, True])

    def test_scan_without_tts_setup_is_reported(self):
        service = FakeScanService()
        service.next_setup = None
        controller = MaelController(service)
        self.assertEqual(controller.on_scan(), "Aucun texte à lire pour ce scan.")
        self.assertFalse(controller.can_repeat)


if __name__ == "__main__":
    unittest.main()
