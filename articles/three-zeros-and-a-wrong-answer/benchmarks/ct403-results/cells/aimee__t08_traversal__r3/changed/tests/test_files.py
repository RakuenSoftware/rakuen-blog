import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import download_path


class DownloadPathTests(unittest.TestCase):
    def test_returns_path_within_upload_root(self):
        with tempfile.TemporaryDirectory() as root:
            with patch("app.files.UPLOAD_ROOT", root):
                self.assertEqual(
                    download_path("images/widget.png"),
                    os.path.join(root, "images", "widget.png"),
                )

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as root:
            with patch("app.files.UPLOAD_ROOT", root):
                with self.assertRaises(ValueError):
                    download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with tempfile.TemporaryDirectory() as root:
            with patch("app.files.UPLOAD_ROOT", root):
                with self.assertRaises(ValueError):
                    download_path(os.path.join(os.path.sep, "etc", "passwd"))

    def test_rejects_symlink_outside_upload_root(self):
        with tempfile.TemporaryDirectory() as root:
            with tempfile.TemporaryDirectory() as outside:
                os.symlink(outside, os.path.join(root, "escape"))
                with patch("app.files.UPLOAD_ROOT", root):
                    with self.assertRaises(ValueError):
                        download_path("escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
