import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
import openpyxl
from openpyxl import Workbook
import pandas as pd
from datetime import datetime
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime


# Load environment variables from .env file
load_dotenv()
#Debugging measure to see if tokens are being sent correctly
print("Loaded Variables:")
print("PLAID_CLIENT_ID:", os.getenv('PLAID_CLIENT_ID'))
print("PLAID_SECRET:", os.getenv('PLAID_SANDBOX_SECRET'))
print("ACCESS_TOKEN:", os.getenv('ACCESS_TOKEN'))


# Define constants for Plaid's API keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SANDBOX_SECRET')  # Change to PLAID_DEVELOPMENT_SECRET for development
PLAID_ENVIRONMENT = 'sandbox'  # Change to 'development' for development environment
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN') # Temorary access token for testing purposes. Generated with token_retrieval.py

# Set up Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENVIRONMENT == 'sandbox' else plaid.Environment.Development,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Define a function to retrieve transactions from Plaid
from datetime import datetime

def get_transactions(access_token, start_date_str, end_date_str):
    try:
        # Convert string dates to datetime objects in the format 'YYYY-MM-DD'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Create a TransactionsGetRequest object
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )

        # Call the transactions_get method with the request object
        response = client.transactions_get(request)
        return response['transactions']
    except plaid.ApiException as e:
        print("Error fetching transactions:", e)
        return []


# Implement format_transactions function
def format_transactions(transactions):
    # Convert transactions to a DataFrame
    if transactions:
        df = pd.DataFrame(transactions)
        # TODO: Format the DataFrame as needed (e.g., rename columns, format dates)
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no transactions

# Implement update_workbook function
def update_workbook(transactions_df, workbook_path='finances-workbook.xlsx'):
    # Open the workbook and update it with transactions
    if not transactions_df.empty:
        # Load the workbook using openpyxl
        book = openpyxl.load_workbook(workbook_path)

        # If the 'Transactions' sheet exists, remove it
        if 'Transactions' in book.sheetnames:
            book.remove(book['Transactions'])
            book.save(workbook_path)  # Save the workbook after removing the sheet

        # Write transactions to a new 'Transactions' sheet using a fresh ExcelWriter
        with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a') as writer:
            transactions_df.to_excel(writer, sheet_name="Transactions", index=False)
            # No explicit save needed, as the context manager handles it

    else:
        print("No transactions to update.")


# Main logic for script execution
if __name__ == "__main__":
    print("Starting main script execution...")
    
    # Define date range for transactions
    start_date = (datetime.now() - pd.DateOffset(months=2)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    print(f"Fetching transactions from {start_date} to {end_date}...")
    
    # Retrieve and format transactions
    transactions = get_transactions(ACCESS_TOKEN, start_date, end_date)
    print(f"Retrieved {len(transactions)} transactions.")
    
    formatted_transactions = format_transactions(transactions)
    print("Transactions formatted.")

    # Path to the Excel workbook
    workbook_path = 'finances-workbook.xlsx'
    print(f"Updating workbook at {workbook_path}...")

    # Update the Excel workbook with new transactions
    update_workbook(formatted_transactions, workbook_path)
    print("Workbook updated.")

    print("Script execution complete.")


