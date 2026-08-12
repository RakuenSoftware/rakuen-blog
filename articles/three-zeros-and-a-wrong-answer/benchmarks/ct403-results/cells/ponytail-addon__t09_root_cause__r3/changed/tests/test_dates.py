import datetime
import unittest

from app.billing import billing_period_days


class BillingDatesTest(unittest.TestCase):
    def test_january_billing_period(self):
        self.assertEqual(billing_period_days(datetime.date(2026, 1, 1)), 31)


if __name__ == "__main__":
    unittest.main()
