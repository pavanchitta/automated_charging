"""Interface and implementations for adapting specific transaction sources
to the CSV format required by OfflineCSVTransactionExtractor.
"""
import abc
import pandas as pd


class CSVTransactionAdapterInterface:

    @abc.abstractmethod
    def transform_to_csv(self, output_csv_path: str):
        """Generates a CSV that is of the format required by OfflineCSVTransactionExtractor
        and dumps to |output_csv_path|."""


class PGECSVTransactionAdapter(CSVTransactionAdapterInterface):

    def __init__(self, input_csv_path: str):
        self.input_csv_path = input_csv_path
        self.input_df = pd.read_csv(input_csv_path)

    def _transform_date(self, date):
        # Ex 10/06/22 -> 2022-06-10
        terms = date.split('/')
        day, month, year = terms[1], terms[0], f'20{terms[2]}'
        return f'{year}-{month}-{day}'

    def _transform_amount(self, amount):
        # Just get rid of dollar sign.
        # Ex $57.46 -> 57.46
        return float(amount[1:])

    def transform_to_csv(self, output_csv_path: str):
        df = self.input_df.copy()
        df = df[9:] # Get rid of initial rows
        cols = df.columns[1:4] # Get rid of the unnecessary columns
        df = df[cols]
        df.reset_index(drop=True, inplace=True)
        df.columns = ['Date', 'Type', 'Amount']
        df = df[df['Type'] == 'Bill']
        df['Date'] = df['Date'].apply(lambda x : self._transform_date(x))
        df['Amount'] = df['Amount'].apply(lambda x : self._transform_amount(x))
        df.to_csv(output_csv_path, index=False)
