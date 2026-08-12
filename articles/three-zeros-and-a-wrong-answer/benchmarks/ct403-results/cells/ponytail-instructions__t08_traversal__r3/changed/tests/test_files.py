import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_path_stays_inside_upload_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = os.path.join(directory, "uploads")
            outside = os.path.join(directory, "outside")
            os.mkdir(root)
            os.mkdir(outside)
            os.symlink(outside, os.path.join(root, "link"))

            with patch("app.files.UPLOAD_ROOT", root):
                self.assertEqual(download_path("nested/file.txt"), os.path.join(root, "nested/file.txt"))
                for name in ("../secret.txt", "/etc/passwd", "link/secret.txt"):
                    with self.subTest(name=name), self.assertRaises(ValueError):
                        download_path(name)


if __name__ == "__main__":
    unittest.main()
