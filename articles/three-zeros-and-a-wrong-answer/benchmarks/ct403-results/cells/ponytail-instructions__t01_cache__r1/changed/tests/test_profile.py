import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileCacheTest(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.users.clear()
        self.db.reset_counter()
        reset()

    def test_reads_are_cached_and_updates_are_immediately_visible(self):
        self.db.users["u1"] = {"id": "u1", "name": "old"}

        self.assertEqual(get_profile("u1")["name"], "old")
        self.assertEqual(get_profile("u1")["name"], "old")
        self.assertEqual(self.db.queries, 1)

        update_profile("u1", {"name": "new"})

        self.assertEqual(get_profile("u1")["name"], "new")
        self.assertEqual(self.db.queries, 3)


if __name__ == "__main__":
    unittest.main()
