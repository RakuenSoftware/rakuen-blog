import unittest

from app.cache import reset
from app.db import get_db
from app.profile import get_profile, update_profile


class ProfileTest(unittest.TestCase):
    def test_reads_are_cached_and_updates_invalidate(self):
        reset()
        db = get_db()
        db.users.clear()
        db.users["u1"] = {"name": "before"}
        db.reset_counter()

        self.assertEqual(get_profile("u1")["name"], "before")
        self.assertEqual(get_profile("u1")["name"], "before")
        self.assertEqual(db.queries, 1)

        update_profile("u1", {"name": "after"})
        self.assertEqual(get_profile("u1")["name"], "after")
        self.assertEqual(db.queries, 3)


if __name__ == "__main__":
    unittest.main()
