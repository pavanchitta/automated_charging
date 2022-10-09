"""Unit tests for transaction.py"""

import unittest
import pandas as pd
import datetime
from transaction import OfflineCSVTransactionExtractor


class OfflineCSVTransactionExtractorTest(unittest.TestCase):

    def setUp(self):
        self.test_csv_path = 'test_payments.csv'
        # Check initialization doesn't fail
        self.extractor = OfflineCSVTransactionExtractor(self.test_csv_path)

    def test_get_latest_payment(self):
        latest_payment = self.extractor.GetLatestPayment()
        self.assertEqual(latest_payment.amount, 20)
        self.assertEqual(latest_payment.date, datetime.date.fromisoformat('2021-05-21'))

    def test_get_all_payments(self):
        all_payments = self.extractor.GetAllPayments()
        self.assertEqual(len(all_payments), 2)

    def test_get_payments_within_range(self):
        start_date = datetime.date.fromisoformat('2021-01-21')
        end_date = datetime.date.fromisoformat('2022-01-21')
        payments = self.extractor.GetPaymentsWithinDateRange(start_date, end_date)
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0].amount, 20)
        self.assertEqual(payments[0].date, datetime.date.fromisoformat('2021-05-21'))

        start_date = datetime.date.fromisoformat('2021-10-21') 
        payments = self.extractor.GetPaymentsWithinDateRange(start_date, end_date)
        self.assertEqual(len(payments), 0)





if __name__ == "__main__":
    unittest.main()