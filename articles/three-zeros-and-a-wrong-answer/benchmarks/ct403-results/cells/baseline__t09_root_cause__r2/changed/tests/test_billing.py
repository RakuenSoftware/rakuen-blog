import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class EndOfMonthTests(unittest.TestCase):
    def test_billing_period_in_january_has_31_days(self):
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)

    def test_end_of_month_handles_different_month_lengths(self):
        cases = (
            (datetime.date(2026, 4, 1), datetime.date(2026, 4, 30)),
            (datetime.date(2026, 2, 1), datetime.date(2026, 2, 28)),
            (datetime.date(2024, 2, 1), datetime.date(2024, 2, 29)),
        )

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(end_of_month(value), expected)


if __name__ == "__main__":
    unittest.main()
