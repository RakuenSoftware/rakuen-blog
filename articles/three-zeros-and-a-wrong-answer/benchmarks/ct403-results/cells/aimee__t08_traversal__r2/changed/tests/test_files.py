import os
import tempfile
import unittest
from unittest.mock import patch

from app.errors import Forbidden
from app.files import download_path


class DownloadPathTests(unittest.TestCase):
    def test_returns_nested_path_within_upload_root(self):
        with tempfile.TemporaryDirectory() as upload_root:
            with patch("app.files.UPLOAD_ROOT", upload_root):
                self.assertEqual(
                    download_path("users/avatar.png"),
                    os.path.join(upload_root, "users", "avatar.png"),
                )

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as upload_root:
            with patch("app.files.UPLOAD_ROOT", upload_root):
                with self.assertRaises(Forbidden):
                    download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with self.assertRaises(Forbidden):
            download_path("/etc/passwd")

    def test_rejects_upload_root_prefix_collision(self):
        with tempfile.TemporaryDirectory() as parent:
            upload_root = os.path.join(parent, "uploads")
            os.mkdir(upload_root)
            with patch("app.files.UPLOAD_ROOT", upload_root):
                with self.assertRaises(Forbidden):
                    download_path("../uploads-private/secret.txt")

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as parent:
            upload_root = os.path.join(parent, "uploads")
            outside = os.path.join(parent, "outside")
            os.mkdir(upload_root)
            os.mkdir(outside)
            os.symlink(outside, os.path.join(upload_root, "escape"))
            with patch("app.files.UPLOAD_ROOT", upload_root):
                with self.assertRaises(Forbidden):
                    download_path("escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
