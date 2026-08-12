import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class BillingPeriodTests(unittest.TestCase):
    def test_january_billing_period_has_31_days(self):
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)

    def test_end_of_month_handles_leap_year(self):
        self.assertEqual(
            end_of_month(datetime.date(2024, 2, 1)),
            datetime.date(2024, 2, 29),
        )


if __name__ == "__main__":
    unittest.main()
