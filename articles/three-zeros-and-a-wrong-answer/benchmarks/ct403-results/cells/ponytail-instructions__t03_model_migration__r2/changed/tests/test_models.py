import unittest

from app.models import User


class UserMigrationTest(unittest.TestCase):
    def test_loads_legacy_row_and_serializes_both_name_shapes(self):
        user = User.from_dict({"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"})

        self.assertEqual(user.first_name, "Ada")
        self.assertEqual(user.last_name, "Lovelace")
        self.assertEqual(
            user.to_dict(),
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "name": "Ada Lovelace",
                "email": "ada@example.com",
            },
        )

    def test_loads_split_row(self):
        user = User.from_dict(
            {"id": "u1", "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"}
        )

        self.assertEqual(user.name, "Ada Lovelace")

    def test_keeps_legacy_constructor(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))

        blank = User.from_dict({"id": "u2", "name": "", "email": None})
        self.assertEqual((blank.first_name, blank.last_name, blank.email), ("", "", None))


if __name__ == "__main__":
    unittest.main()
