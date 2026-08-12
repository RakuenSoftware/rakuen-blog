import os
import tempfile
import unittest
from unittest.mock import patch

from app.errors import Forbidden
from app.files import download_path


class DownloadPathTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.upload_root = os.path.join(self.temporary_directory.name, "uploads")
        os.mkdir(self.upload_root)

        root_patch = patch("app.files.UPLOAD_ROOT", self.upload_root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_returns_path_inside_upload_root(self):
        expected = os.path.join(self.upload_root, "users", "avatar.png")

        self.assertEqual(download_path("users/avatar.png"), expected)

    def test_rejects_parent_traversal(self):
        with self.assertRaises(Forbidden):
            download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with self.assertRaises(Forbidden):
            download_path(os.path.join(self.temporary_directory.name, "secret.txt"))

    def test_rejects_symlink_outside_upload_root(self):
        outside = os.path.join(self.temporary_directory.name, "outside")
        os.mkdir(outside)
        os.symlink(outside, os.path.join(self.upload_root, "shared"))

        with self.assertRaises(Forbidden):
            download_path("shared/secret.txt")


if __name__ == "__main__":
    unittest.main()
