import datetime
import unittest

from app.billing import billing_period_days
from app.dates import end_of_month


class BillingPeriodTest(unittest.TestCase):
    def test_month_ends_and_billing_period(self):
        self.assertEqual(end_of_month(datetime.date(2026, 1, 1)), datetime.date(2026, 1, 31))
        self.assertEqual(end_of_month(datetime.date(2024, 2, 1)), datetime.date(2024, 2, 29))
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)


if __name__ == "__main__":
    unittest.main()
