import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.users.clear()
        self.db.users["u1"] = {"id": "u1", "name": "before"}
        self.db.reset_counter()
        reset()

    def test_repeated_reads_use_cache(self):
        self.assertEqual(get_profile("u1")["name"], "before")
        self.assertEqual(get_profile("u1")["name"], "before")
        self.assertEqual(self.db.queries, 1)

    def test_update_invalidates_cached_profile(self):
        get_profile("u1")

        update_profile("u1", {"name": "after"})

        self.assertEqual(get_profile("u1")["name"], "after")
        self.assertEqual(self.db.queries, 3)


if __name__ == "__main__":
    unittest.main()
