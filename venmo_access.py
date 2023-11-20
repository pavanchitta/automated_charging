"""
Some access keys
"""
import venmo_api

VENMO_ACCESS_TOKEN_KEY = "VENMO_ACCESS_TOKEN_KEY"


def get_access_token(username, password):
    """Get access token."""
    access_token = venmo_api.Client.get_access_token(username=username,
                                            password=password)
    return access_token