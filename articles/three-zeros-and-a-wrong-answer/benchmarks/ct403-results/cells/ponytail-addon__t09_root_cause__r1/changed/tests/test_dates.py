import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class DateTests(unittest.TestCase):
    def test_end_of_month(self):
        for day, expected in ((datetime.date(2026, 1, 1), 31),
                              (datetime.date(2026, 4, 1), 30),
                              (datetime.date(2024, 2, 1), 29)):
            self.assertEqual(end_of_month(day).day, expected)

        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)


if __name__ == "__main__":
    unittest.main()
