import unittest

from app.models import User


class UserMigrationTest(unittest.TestCase):
    def test_reads_legacy_rows_and_writes_both_name_shapes(self):
        user = User.from_dict({"id": "u1", "name": "Ada Lovelace", "email": "ada@example.com"})

        self.assertEqual((user.first_name, user.last_name), ("Ada", "Lovelace"))
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
        self.assertEqual(User.from_dict(user.to_dict()).name, "Ada Lovelace")

    def test_legacy_constructor_still_works(self):
        user = User("u1", "Ada Lovelace", "ada@example.com")

        self.assertEqual((user.first_name, user.last_name, user.email), ("Ada", "Lovelace", "ada@example.com"))


if __name__ == "__main__":
    unittest.main()
