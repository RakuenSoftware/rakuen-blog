import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import InvalidDownloadPath, download_path


class DownloadPathTests(unittest.TestCase):
    def test_returns_canonical_path_below_upload_root(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            self.assertEqual(download_path("nested/file.txt"),
                             os.path.join(root, "nested", "file.txt"))

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            with self.assertRaises(InvalidDownloadPath):
                download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            with self.assertRaises(InvalidDownloadPath):
                download_path("/etc/passwd")

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            os.symlink(outside, os.path.join(root, "escape"))
            with patch("app.files.UPLOAD_ROOT", root):
                with self.assertRaises(InvalidDownloadPath):
                    download_path("escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
