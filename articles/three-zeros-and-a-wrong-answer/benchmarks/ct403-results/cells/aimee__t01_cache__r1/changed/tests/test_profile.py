import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileCacheTests(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.db.users.clear()
        self.db.users["u1"] = {"id": "u1", "name": "before"}
        self.db.reset_counter()
        reset()

    def test_repeated_reads_use_cache(self):
        self.assertEqual("before", get_profile("u1")["name"])
        self.assertEqual("before", get_profile("u1")["name"])
        self.assertEqual(1, self.db.queries)

    def test_update_is_visible_on_next_read(self):
        get_profile("u1")

        update_profile("u1", {"name": "after"})

        self.assertEqual("after", get_profile("u1")["name"])
        self.assertEqual(3, self.db.queries)


if __name__ == "__main__":
    unittest.main()
