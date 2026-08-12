import os
import tempfile
import unittest
from unittest.mock import patch

from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_rejects_paths_outside_upload_root(self):
        with tempfile.TemporaryDirectory() as root:
            with patch("app.files.UPLOAD_ROOT", root):
                self.assertEqual(download_path("nested/file.txt"), os.path.join(root, "nested/file.txt"))
                for name in ("../secret.txt", root + "-other/secret.txt", "/etc/passwd"):
                    with self.subTest(name=name), self.assertRaises(ValueError):
                        download_path(name)


if __name__ == "__main__":
    unittest.main()
