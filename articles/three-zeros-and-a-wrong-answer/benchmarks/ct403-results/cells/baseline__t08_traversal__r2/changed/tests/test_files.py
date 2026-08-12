import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import download_path


class DownloadPathTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.upload_root = os.path.join(self.tempdir.name, "uploads")
        os.mkdir(self.upload_root)
        self.root_patch = patch("app.files.UPLOAD_ROOT", self.upload_root)
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.tempdir.cleanup()

    def test_returns_path_below_upload_root(self):
        self.assertEqual(
            download_path("user/avatar.png"),
            os.path.join(self.upload_root, "user", "avatar.png"),
        )

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError):
            download_path("../secret.txt")

    def test_rejects_absolute_path(self):
        with self.assertRaises(ValueError):
            download_path(os.path.join(self.tempdir.name, "secret.txt"))

    def test_rejects_symlink_escape(self):
        outside = os.path.join(self.tempdir.name, "outside")
        os.mkdir(outside)
        os.symlink(outside, os.path.join(self.upload_root, "linked"))

        with self.assertRaises(ValueError):
            download_path("linked/secret.txt")


if __name__ == "__main__":
    unittest.main()
