import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
import openpyxl
import pandas as pd
from datetime import datetime
from plaid.model.transactions_get_request import TransactionsGetRequest

# Load environment variables from .env file
load_dotenv()

# Debugging measure to check if tokens are being loaded correctly
print("Loaded Variables:")
print("PLAID_CLIENT_ID:", os.getenv('PLAID_CLIENT_ID'))
print("PLAID_SECRET:", os.getenv('PLAID_SANDBOX_SECRET'))
print("ACCESS_TOKEN:", os.getenv('ACCESS_TOKEN'))

# Define constants for Plaid's API keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SANDBOX_SECRET')  # Change for development
PLAID_ENVIRONMENT = 'sandbox'  # Change for development
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # Temporary access token

# Set up Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENVIRONMENT == 'sandbox' else plaid.Environment.Development,
    api_key={'clientId': PLAID_CLIENT_ID, 'secret': PLAID_SECRET}
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Function to retrieve transactions from Plaid
def get_transactions(access_token, start_date_str, end_date_str):
    try:
        # Convert string dates to datetime objects in format 'YYYY-MM-DD'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Create a TransactionsGetRequest object
        request = TransactionsGetRequest(access_token=access_token, start_date=start_date, end_date=end_date)
        response = client.transactions_get(request)
        return response['transactions']
    except plaid.ApiException as e:
        print("Error fetching transactions:", e)
        return []

# Function to format transactions into a DataFrame
def format_transactions(transactions):
    if transactions:
        df = pd.DataFrame(transactions)
        # TODO: Format DataFrame as needed (e.g., rename columns, format dates)
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no transactions

# Function to update the workbook with transactions
def update_workbook(transactions_df, workbook_path='finances-workbook.xlsx'):
    if not transactions_df.empty:
        with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a') as writer:
            # Check if 'Transactions' sheet exists and remove it
            if 'Transactions' in writer.book.sheetnames:
                std = writer.book['Transactions']
                writer.book.remove(std)

            # Write transactions to a new 'Transactions' sheet
            transactions_df.to_excel(writer, sheet_name="Transactions", index=False)

    else:
        print("No transactions to update.")

# Function to reorder sheets in the workbook
def reorder_sheets(workbook_path, sheet_name, desired_index):
    book = openpyxl.load_workbook(workbook_path)
    if sheet_name in book.sheetnames:
        sheet = book[sheet_name]
        book.remove(sheet)
        book._sheets.insert(desired_index, sheet)
        book.save(workbook_path)

# Main script execution
if __name__ == "__main__":
    print("Starting main script execution...")
    start_date = (datetime.now() - pd.DateOffset(months=2)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    print(f"Fetching transactions from {start_date} to {end_date}...")
    transactions = get_transactions(ACCESS_TOKEN, start_date, end_date)
    print(f"Retrieved {len(transactions)} transactions.")

    formatted_transactions = format_transactions(transactions)
    print("Transactions formatted.")

    workbook_path = 'finances-workbook.xlsx'
    print(f"Updating workbook at {workbook_path}...")
    update_workbook(formatted_transactions, workbook_path)
    reorder_sheets('finances-workbook.xlsx', 'Transactions', 2)  # Adjust index as needed
    print("Workbook updated.")
    print("Script execution complete.")

# TODO: Add detailed comments and docstrings.
# TODO: Implement robust error handling and logging.
# TODO: Enhance data formatting in format_transactions function.
