import unittest
from pathlib import Path

from wardoff import venv


class TestVenv(unittest.TestCase):
    def setUp(self):
        venv.create()

    def test_site_packages(self):
        self.assertTrue(venv.site_packages().is_dir())

    def test_create(self):
        self.assertTrue(venv.VENVDIR.is_dir())

    def test_pip_install(self):
        output = venv.pip_install("niet")
        lines = []
        for line in output.split("\n"):
            if line:
                lines.append(line)
        self.assertTrue(lines[-1].startswith("Successfully installed"))

    def test_pip_show(self):
        venv.pip_install("niet")
        info = venv.pip_show("niet")
        location = None
        for el in info:
            if not el.startswith("Location:"):
                continue
            location = el.replace("Location: ", "")
        self.assertTrue(Path(location).is_dir())

    def test_destroy(self):
        self.assertTrue(venv.VENVDIR.is_dir())
        venv.destroy()
        self.assertFalse(venv.VENVDIR.is_dir())
