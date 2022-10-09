"""Main entry-point for making requests for pge payments."""

from absl import flags
from absl import app
import datetime

from typing import Optional

import venmo_client
import transaction as transaction_extract
import secrets
import transaction_adapter

FLAGS = flags.FLAGS

flags.DEFINE_string('payment_history_csv', None, 'The raw payment history CSV downloaded from pge.com')
flags.DEFINE_list('chargee_usernames', None, 'List of usernames to charge equally.')
flags.DEFINE_string('start_date', None, 'Optional start date of transactions')
flags.DEFINE_string('end_date', None, 'Optional end date of transactions')
flags.DEFINE_boolean('dry_run', True, 'If True, wont actually charge, will just print info.')
flags.DEFINE_string('base_description', 'PGE', 'Description prefix added to charge description.')

flags.mark_flags_as_required(['payment_history_csv', 'chargee_usernames'])

_TMP_CSV_PATH = 'data/pge_payment_history.csv'

def _get_date_bounds(start_date: Optional[datetime.date], end_date: Optional[datetime.date]):
    if start_date is None:
        start_date = datetime.date.min
    else:
        start_date = datetime.date.fromisoformat(start_date)
    if end_date is None:
        end_date = datetime.date.max
    else:
        end_date = datetime.date.fromisoformat(end_date)
    return start_date, end_date


def main(_):
    # Initialize venmo payment client.
    venmo = venmo_client.VenmoClient(secrets.ACCESS_TOKEN)
    user_ids = {}
    for username in FLAGS.chargee_usernames:
        user_ids[venmo.get_user_id_by_username(username)] = username

    # First adapt the raw input csv to a format that is ingestible by the transaction extractor.
    pge_transaction_adapter = transaction_adapter.PGECSVTransactionAdapter(FLAGS.payment_history_csv)
    pge_transaction_adapter.transform_to_csv(_TMP_CSV_PATH)

    start_date, end_date = _get_date_bounds(FLAGS.start_date, FLAGS.end_date)
    print(start_date, end_date)

    transaction_extractor = transaction_extract.OfflineCSVTransactionExtractor(_TMP_CSV_PATH)
    transactions = transaction_extractor.GetPaymentsWithinDateRange(start_date, end_date)

    for transaction in transactions:
        total_amount = transaction.amount
        indiv_amount = total_amount / (len(user_ids) + 1)
        description = f'{FLAGS.base_description} - {str(transaction.date)}'
        for user_id in user_ids:
            print(f'Requesting {indiv_amount} from {user_ids[user_id]} with description {description}.')
            if not FLAGS.dry_run:
                venmo.request_money(user_id, indiv_amount, description)
    
    

if __name__ == "__main__":
    app.run(main)