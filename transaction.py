"""Info related to transactions already made that should be split."""

from dataclasses import dataclass
from typing import List
import datetime
import abc
import pandas as pd
import os


@dataclass
class Transaction:
    """A single transaction made on |date| of |amount| dollars."""
    amount: float
    date: datetime.date


class TransactionExtractor:
    """Interface of class that extracts transactions made"""

    @abc.abstractmethod
    def GetLatestPayment(self) -> Transaction:
        pass

    @abc.abstractmethod
    def GetAllPayments(self) -> List[Transaction]:
        pass

    @abc.abstractmethod
    def GetPaymentsWithinDateRange(self, start_date: datetime.date, end_date: datetime.date) -> List[Transaction]:
        pass



class OfflineCSVTransactionExtractor(TransactionExtractor):
    """Concrete implementation of TransactionExtractor that extracts payments
    from an input CSV file with a list of all payments made.
    Expects the following schema from the CSV:
        - Date, Amount.
    Expects the date string to be in ISO Format (YYYY-MM-DD)
    """

    def __init__(self, csv_filepath):
        self.csv = csv_filepath
        self.payments_df = pd.read_csv(csv_filepath)
        self._validate()
        self.payments_df['Date'] = self.payments_df['Date'].apply(lambda x : datetime.date.fromisoformat(x))

    def _validate(self):
        assert os.path.exists(self.csv)
        for col in ['Date', 'Amount']:
            assert col in self.payments_df.columns

    
    def _get_transaction_for_row(self, row):
        return Transaction(amount=row['Amount'], date=row['Date'])

    def _transform_df_to_transactions(self, df):
        res = []
        for i, row in df.iterrows():
            res.append(self._get_transaction_for_row(row))
        return res

    def GetLatestPayment(self) -> Transaction:
        print(self.payments_df)
        latest_payment_row = self.payments_df.sort_values(['Date']).iloc[-1]
        return self._get_transaction_for_row(latest_payment_row)

    def GetAllPayments(self) -> List[Transaction]:
        return self._transform_df_to_transactions(self.payments_df)
        

    def GetPaymentsWithinDateRange(self, start_date: datetime.date, end_date: datetime.date) -> List[Transaction]:
        filtered = self.payments_df[(self.payments_df['Date'] >= start_date) & (self.payments_df['Date'] <= end_date)]
        return self._transform_df_to_transactions(filtered)


