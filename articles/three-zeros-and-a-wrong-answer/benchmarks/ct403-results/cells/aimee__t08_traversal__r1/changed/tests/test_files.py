import os
import tempfile
import unittest

from app import files
from app.errors import AppError


class DownloadPathTests(unittest.TestCase):
    def setUp(self):
        self.upload_root = tempfile.TemporaryDirectory()
        self.original_upload_root = files.UPLOAD_ROOT
        files.UPLOAD_ROOT = self.upload_root.name

    def tearDown(self):
        files.UPLOAD_ROOT = self.original_upload_root
        self.upload_root.cleanup()

    def test_returns_canonical_path_inside_upload_root(self):
        expected = os.path.join(os.path.realpath(self.upload_root.name), "images", "widget.png")

        self.assertEqual(files.download_path("images/widget.png"), expected)

    def test_rejects_parent_directory_traversal(self):
        with self.assertRaises(AppError):
            files.download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with self.assertRaises(AppError):
            files.download_path(os.path.join(os.path.sep, "etc", "passwd"))

    def test_rejects_similar_directory_prefix(self):
        sibling = self.upload_root.name + "-private"

        with self.assertRaises(AppError):
            files.download_path(os.path.join("..", os.path.basename(sibling), "secret.txt"))

    def test_rejects_symlink_outside_upload_root(self):
        with tempfile.TemporaryDirectory() as outside:
            os.symlink(outside, os.path.join(self.upload_root.name, "escape"))

            with self.assertRaises(AppError):
                files.download_path("escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
