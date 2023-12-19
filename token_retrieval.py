import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Plaid credentials from .env file
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SANDBOX_SECRET = os.getenv('PLAID_SANDBOX_SECRET')

def create_link_token():
    """
    Creates a link token using the Plaid API.
    """
    response = requests.post(
        'https://sandbox.plaid.com/link/token/create',
        json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SANDBOX_SECRET,
            'client_name': "Your App Name",
            'country_codes': ['US'],
            'language': 'en',
            'user': {'client_user_id': 'unique_user_id'},
            'products': ['transactions']
        }
    )
    return response.json().get('link_token')

def exchange_public_token(public_token):
    """
    Exchanges a public token for an access token using the Plaid API.
    """
    response = requests.post(
        'https://sandbox.plaid.com/item/public_token/exchange',
        json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SANDBOX_SECRET,
            'public_token': public_token
        }
    )
    return response.json().get('access_token')

def create_sandbox_public_token():
    """
    Creates a sandbox public token directly using the Plaid Sandbox API.
    """
    response = requests.post(
        'https://sandbox.plaid.com/sandbox/public_token/create',
        json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SANDBOX_SECRET,
            'institution_id': 'ins_1',
            'initial_products': ['transactions']
        }
    )
    return response.json().get('public_token')

if __name__ == "__main__":
    use_sandbox_api = input("Use Sandbox API to create public token? (y/n): ")
    public_token = create_sandbox_public_token() if use_sandbox_api.lower() == 'y' else input("Enter the public token: ")

    if public_token:
        access_token = exchange_public_token(public_token)
        print("Access token:", access_token)
    else:
        print("No valid public token provided.")
