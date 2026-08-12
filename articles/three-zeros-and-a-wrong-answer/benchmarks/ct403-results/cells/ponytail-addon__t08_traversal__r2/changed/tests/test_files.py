import os
import tempfile
import unittest
from unittest.mock import patch

from app.errors import Forbidden
from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_stays_within_upload_root(self):
        with tempfile.TemporaryDirectory() as parent:
            root = os.path.join(parent, "uploads")
            outside = os.path.join(parent, "outside")
            os.mkdir(root)
            os.mkdir(outside)
            os.symlink(outside, os.path.join(root, "link"))

            with patch("app.files.UPLOAD_ROOT", root):
                self.assertEqual(download_path("folder/file.txt"), os.path.join(root, "folder/file.txt"))
                for name in ("../secret.txt", "/etc/passwd", "link/secret.txt"):
                    with self.subTest(name=name), self.assertRaises(Forbidden):
                        download_path(name)


if __name__ == "__main__":
    unittest.main()
