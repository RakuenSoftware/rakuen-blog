import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import download_path


class DownloadPathTests(unittest.TestCase):
    def setUp(self):
        self.root_dir = tempfile.TemporaryDirectory()
        self.root = self.root_dir.name
        self.root_patch = patch("app.files.UPLOAD_ROOT", self.root)
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.root_dir.cleanup()

    def test_returns_path_within_upload_root(self):
        expected = os.path.join(self.root, "images", "widget.png")
        self.assertEqual(download_path("images/widget.png"), expected)

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError):
            download_path("../secret.txt")

    def test_rejects_absolute_path_outside_root(self):
        with self.assertRaises(ValueError):
            download_path(os.path.join(os.path.dirname(self.root), "secret.txt"))

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            os.symlink(outside, os.path.join(self.root, "escape"))
            with self.assertRaises(ValueError):
                download_path("escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
