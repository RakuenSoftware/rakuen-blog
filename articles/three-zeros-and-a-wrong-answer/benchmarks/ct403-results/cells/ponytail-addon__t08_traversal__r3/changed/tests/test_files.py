import os
import tempfile
import unittest
from unittest.mock import patch

from app.errors import Forbidden
from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_stays_inside_upload_root(self):
        with tempfile.TemporaryDirectory() as root, patch("app.files.UPLOAD_ROOT", root):
            self.assertEqual(download_path("nested/file.txt"), os.path.join(root, "nested/file.txt"))
            os.symlink("/etc", os.path.join(root, "link"))
            for name in ("../secret.txt", "/etc/passwd", "link/passwd"):
                with self.assertRaises(Forbidden):
                    download_path(name)


if __name__ == "__main__":
    unittest.main()
