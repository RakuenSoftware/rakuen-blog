import unittest

from app.models import User


class UserMigrationTests(unittest.TestCase):
    def test_serializes_split_and_legacy_names(self):
        user = User("u1", "Ada", "Lovelace", "ada@example.com")

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

    def test_loads_legacy_row(self):
        user = User.from_dict(
            {"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"}
        )

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))
        self.assertEqual(user.name, "Ada Lovelace")

    def test_loads_split_row(self):
        user = User.from_dict(
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            }
        )

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))

    def test_keeps_legacy_constructor_and_name_setter(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")
        user.name = "Grace Hopper"

        self.assertEqual((user.first_name, user.last_name), ("Grace", "Hopper"))
        self.assertEqual(user.email, "ada@example.com")

    def test_keeps_legacy_keyword_constructor(self):
        user = User(uid="u1", name="Prince", email="prince@example.com")

        self.assertEqual((user.first_name, user.last_name), ("Prince", ""))
        self.assertEqual(user.name, "Prince")


if __name__ == "__main__":
    unittest.main()
