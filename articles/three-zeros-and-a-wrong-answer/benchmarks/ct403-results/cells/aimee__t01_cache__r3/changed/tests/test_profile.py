import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileCacheTest(unittest.TestCase):
    def setUp(self):
        reset()
        self.db = get_db()
        self.db.users.clear()
        self.db.reset_counter()
        self.db.users["u1"] = {"id": "u1", "name": "before"}

    def test_repeated_reads_only_query_once(self):
        self.assertEqual(get_profile("u1")["name"], "before")
        self.assertEqual(get_profile("u1")["name"], "before")

        self.assertEqual(self.db.queries, 1)

    def test_update_is_visible_on_next_read(self):
        get_profile("u1")

        update_profile("u1", {"name": "after"})

        self.assertEqual(get_profile("u1")["name"], "after")
        self.assertEqual(self.db.queries, 3)


if __name__ == "__main__":
    unittest.main()
