import unittest

from app.models import User


class UserMigrationTest(unittest.TestCase):
    def test_old_and_new_rows_share_compatible_serialization(self):
        old = User.from_dict({"id": "u1", "name": "Ada Lovelace", "email": "a@example.com"})
        new = User.from_dict(
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "a@example.com",
            }
        )

        self.assertEqual(old.to_dict(), new.to_dict())
        self.assertEqual(old.to_dict()["name"], "Ada Lovelace")
        self.assertEqual((old.first_name, old.last_name), ("Ada", "Lovelace"))

        old_with_new_columns = User.from_dict(
            {
                "id": "u1",
                "name": "Ada Lovelace",
                "first_name": None,
                "last_name": None,
                "email": "a@example.com",
            }
        )
        self.assertEqual(old_with_new_columns.to_dict(), new.to_dict())


if __name__ == "__main__":
    unittest.main()
