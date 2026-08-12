import datetime
import unittest

from app.billing import billing_period_days


class BillingPeriodDaysTest(unittest.TestCase):
    def test_uses_actual_month_length(self):
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)
        self.assertEqual(billing_period_days(datetime.date(2024, 2, 1)), 29)


if __name__ == "__main__":
    unittest.main()
