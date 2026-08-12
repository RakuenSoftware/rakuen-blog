import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class DateTests(unittest.TestCase):
    def test_end_of_month_and_billing_period(self):
        cases = [
            (datetime.date(2026, 1, 1), datetime.date(2026, 1, 31), 31),
            (datetime.date(2026, 2, 1), datetime.date(2026, 2, 28), 28),
            (datetime.date(2024, 2, 1), datetime.date(2024, 2, 29), 29),
            (datetime.date(2026, 4, 1), datetime.date(2026, 4, 30), 30),
        ]
        for start, end, days in cases:
            with self.subTest(start=start):
                self.assertEqual(end_of_month(start), end)
                self.assertEqual(billing_period_days(start), days)


if __name__ == "__main__":
    unittest.main()
