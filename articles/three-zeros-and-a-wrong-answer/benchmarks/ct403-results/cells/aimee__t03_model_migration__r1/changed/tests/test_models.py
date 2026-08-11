import unittest

from app.models import User


class UserMigrationTests(unittest.TestCase):
    def test_serializes_split_and_legacy_names(self):
        user = User("u1", "Ada", "Lovelace", "ada@example.test")

        self.assertEqual(user.name, "Ada Lovelace")
        self.assertEqual(
            user.to_dict(),
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "name": "Ada Lovelace",
                "email": "ada@example.test",
            },
        )

    def test_loads_legacy_row(self):
        user = User.from_dict(
            {"id": "u1", "name": "Ada Lovelace", "email": "ada@example.test"}
        )

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))

    def test_loads_split_row(self):
        user = User.from_dict(
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.test",
            }
        )

        self.assertEqual(user.name, "Ada Lovelace")

    def test_keeps_legacy_constructor_and_name_assignment(self):
        user = User("u1", "Ada Lovelace", "ada@example.test")
        user.name = "Grace Hopper"

        self.assertEqual((user.first_name, user.last_name), ("Grace", "Hopper"))
        self.assertEqual(user.email, "ada@example.test")

    def test_loads_partially_migrated_row(self):
        user = User.from_dict(
            {
                "id": "u1",
                "first_name": "Ada",
                "name": "Ada Lovelace",
                "email": "ada@example.test",
            }
        )

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))


if __name__ == "__main__":
    unittest.main()
