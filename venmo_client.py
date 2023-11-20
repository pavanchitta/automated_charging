"""Client class for interfacing with the Venmo API."""

# Need to have a Venmo Client class which supports basic functionality.
# - Need to be able to MakeCharge(Amount, PersonId, description)
# - Need to figure out how to manage all the credentials / env variables that give
#   sufficient permissions for this.

import venmo_api
import secrets

class VenmoClient:
    def __init__(self, access_token):
        self.client = venmo_api.Client(access_token=access_token)

    def get_user_id_by_username(self, username):
        user = self.client.user.get_user_by_username(username=username)
        if (user):
            return user.id
        else:
            raise ValueError("ERROR: user did not comeback. Check username.")

    def request_money(self, id, amount, description, callback = None):
        # Returns a boolean: true if successfully requested
        return self.client.payment.request_money(amount, description, id, venmo_api.PaymentPrivacy.PUBLIC, None, callback)