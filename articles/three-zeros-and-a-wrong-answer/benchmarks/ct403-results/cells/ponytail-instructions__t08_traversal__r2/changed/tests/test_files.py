import os
import tempfile
import unittest
from unittest.mock import patch

from app.errors import AppError
from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_rejects_paths_outside_upload_root(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            for name in ("../secret", os.path.join(root, "..", "secret")):
                with self.subTest(name=name), self.assertRaises(AppError):
                    download_path(name)

    def test_allows_nested_paths_inside_upload_root(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            self.assertEqual(download_path("nested/file.txt"), os.path.join(root, "nested/file.txt"))

    def test_rejects_symlinks_outside_upload_root(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            os.symlink(outside, os.path.join(root, "link"))
            with patch("app.files.UPLOAD_ROOT", root), self.assertRaises(AppError):
                download_path("link/secret")


if __name__ == "__main__":
    unittest.main()
