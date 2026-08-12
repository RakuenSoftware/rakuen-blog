import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class BillingPeriodTests(unittest.TestCase):
    def test_january_billing_period_has_31_days(self):
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)

    def test_end_of_month_handles_month_lengths_and_leap_years(self):
        cases = (
            (datetime.date(2026, 4, 1), datetime.date(2026, 4, 30)),
            (datetime.date(2026, 2, 1), datetime.date(2026, 2, 28)),
            (datetime.date(2024, 2, 1), datetime.date(2024, 2, 29)),
        )
        for start, expected in cases:
            with self.subTest(start=start):
                self.assertEqual(end_of_month(start), expected)


if __name__ == "__main__":
    unittest.main()
