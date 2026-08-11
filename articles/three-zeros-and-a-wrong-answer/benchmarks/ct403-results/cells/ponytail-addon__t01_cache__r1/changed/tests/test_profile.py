import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileCacheTest(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.users.clear()
        self.db.users["u1"] = {"name": "before"}
        self.db.reset_counter()
        reset()

    def test_reads_are_cached_and_updates_are_visible(self):
        self.assertEqual(get_profile("u1"), {"name": "before"})
        self.assertEqual(get_profile("u1"), {"name": "before"})
        self.assertEqual(self.db.queries, 1)

        update_profile("u1", {"name": "after"})

        self.assertEqual(get_profile("u1"), {"name": "after"})
        self.assertEqual(self.db.queries, 3)


if __name__ == "__main__":
    unittest.main()
