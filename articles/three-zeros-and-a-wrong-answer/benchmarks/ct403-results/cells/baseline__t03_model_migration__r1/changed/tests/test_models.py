import unittest

from app.models import User


class UserMigrationTests(unittest.TestCase):
    def test_loads_legacy_row_and_serializes_both_name_formats(self):
        user = User.from_dict(
            {"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"}
        )

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

    def test_loads_migrated_row(self):
        user = User.from_dict(
            {
                "id": "u1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            }
        )

        self.assertEqual(user.name, "Ada Lovelace")

    def test_null_migrated_columns_fall_back_to_legacy_name(self):
        user = User.from_dict(
            {
                "id": "u1",
                "name": "Ada Lovelace",
                "first_name": None,
                "last_name": None,
                "email": "ada@example.com",
            }
        )

        self.assertEqual(user.first_name, "Ada")
        self.assertEqual(user.last_name, "Lovelace")

    def test_old_constructor_and_name_attribute_remain_compatible(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")
        user.name = "Grace Hopper"

        self.assertEqual(user.first_name, "Grace")
        self.assertEqual(user.last_name, "Hopper")
        self.assertEqual(user.email, "ada@example.com")


if __name__ == "__main__":
    unittest.main()
