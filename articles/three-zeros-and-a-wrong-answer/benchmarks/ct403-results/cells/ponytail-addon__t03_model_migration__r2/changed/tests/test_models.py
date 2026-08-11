import unittest

from app.models import User


class UserMigrationTest(unittest.TestCase):
    def test_old_and_new_rows_are_compatible(self):
        old = User.from_dict({"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"})
        new = User.from_dict(old.to_dict())

        self.assertEqual((old.first_name, old.last_name), ("Ada", "Lovelace"))
        self.assertEqual(new.to_dict(), old.to_dict())
        self.assertEqual(new.to_dict()["name"], "Ada Lovelace")

    def test_legacy_constructor_still_works(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")

        self.assertEqual((user.first_name, user.last_name, user.email),
                         ("Ada", "Lovelace", "ada@example.com"))


if __name__ == "__main__":
    unittest.main()
