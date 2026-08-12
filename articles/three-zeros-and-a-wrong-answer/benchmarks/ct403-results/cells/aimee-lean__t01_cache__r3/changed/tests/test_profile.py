import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileCacheTest(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.users.clear()
        self.db.users["u1"] = {"id": "u1", "name": "Old name"}
        self.db.reset_counter()
        reset()

    def test_repeated_reads_use_cache(self):
        self.assertEqual(get_profile("u1")["name"], "Old name")
        self.assertEqual(get_profile("u1")["name"], "Old name")

        self.assertEqual(self.db.queries, 1)

    def test_update_is_visible_after_profile_was_cached(self):
        get_profile("u1")

        update_profile("u1", {"name": "New name"})

        self.assertEqual(get_profile("u1")["name"], "New name")
        self.assertEqual(self.db.queries, 3)


if __name__ == "__main__":
    unittest.main()
