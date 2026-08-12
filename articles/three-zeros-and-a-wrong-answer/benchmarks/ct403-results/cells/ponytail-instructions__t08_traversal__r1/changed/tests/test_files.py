import unittest

from app.errors import Forbidden
from app.files import download_path


class DownloadPathTest(unittest.TestCase):
    def test_stays_inside_upload_root(self):
        self.assertEqual(download_path("users/u1.txt"), "/srv/uploads/users/u1.txt")
        with self.assertRaises(Forbidden):
            download_path("../secrets.txt")


if __name__ == "__main__":
    unittest.main()
