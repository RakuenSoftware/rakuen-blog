import unittest

from app.models import User


class UserMigrationTest(unittest.TestCase):
    def test_loads_legacy_row_and_keeps_legacy_api(self):
        user = User.from_dict({"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"})

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))
        self.assertEqual(user.to_dict()["name"], "Ada Lovelace")

    def test_round_trips_split_name(self):
        row = User("u1", "Ada", "Lovelace", "ada@example.com").to_dict()

        user = User.from_dict(row)
        self.assertEqual((user.first_name, user.last_name, user.name),
                         ("Ada", "Lovelace", "Ada Lovelace"))

    def test_legacy_constructor_and_name_assignment(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")
        user.name = "Grace Hopper"

        self.assertEqual((user.first_name, user.last_name), ("Grace", "Hopper"))


if __name__ == "__main__":
    unittest.main()
