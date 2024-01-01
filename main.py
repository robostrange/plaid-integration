import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
import pandas as pd
from datetime import datetime
from plaid.model.transactions_get_request import TransactionsGetRequest
import openpyxl
from openpyxl import load_workbook, styles
from openpyxl.styles import NamedStyle

# Load environment variables
load_dotenv()

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_DEVELOPMENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Constants
HEADERS = ["TRANS_ID", "DATE", "DESCRIPTION", "INSTITUTION", "ACCOUNT TYPE", "CATEGORY", "AMOUNT", "STATUS"]

# Initialize Plaid client
def init_plaid_client():
    config = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={'clientId': PLAID_CLIENT_ID, 'secret': PLAID_SECRET}
    )
    return plaid_api.PlaidApi(plaid.ApiClient(config))

# Fetch transactions from Plaid
def get_transactions(client, access_token, start_date_str, end_date_str):
    try:
        # Convert string dates to datetime objects in format 'YYYY-MM-DD'
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Create a TransactionsGetRequest object with the date objects
        request = TransactionsGetRequest(access_token=access_token, start_date=start_date, end_date=end_date)
        response = client.transactions_get(request)
        return response['transactions']
    except plaid.ApiException as e:
        print(f"Error fetching transactions: {e}")
        return []

# Format transactions into DataFrame
def format_transactions(transactions):
    formatted = []
    for txn in transactions:
        formatted.append({
            "TRANS_ID": txn.get('transaction_id', ''),
            "DATE": txn.get('date', ''),
            "DESCRIPTION": txn.get('name', ''),
            "INSTITUTION": 'TBD',  # Placeholder for actual institution data
            "ACCOUNT TYPE": 'TBD',  # Placeholder for account type
            "CATEGORY": ' > '.join(txn.get('category', [])),
            "AMOUNT": txn.get('amount', 0),
            "STATUS": 'Pending' if txn.get('pending', False) else 'Completed'
        })
    return pd.DataFrame(formatted, columns=HEADERS)

# Update Excel workbook with transaction data
def update_workbook(df, path):
    if df.empty:
        print("No transactions to update.")
        return

    with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='Transactions', index=False)
        ws = writer.book['Transactions']
        apply_styles_to_sheet(ws)

# Apply styles to Excel sheet
def apply_styles_to_sheet(ws):
    set_column_widths(ws)
    currency_style = NamedStyle(name='currency', number_format='"$"#,##0.00')
    for row in ws.iter_rows(min_row=2):
        row[0].number_format = '@'  # TRANS_ID as text
        row[1].number_format = 'MM/DD/YYYY'  # DATE
        row[6].style = currency_style  # AMOUNT

def set_column_widths(ws):
    column_widths = {'A': 12, 'B': 11, 'C': 75, 'D': 13, 'E': 13, 'F': 38, 'G': 9, 'H': 9}
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

# Reorder sheets in workbook
def reorder_sheets(path, sheet_name, index):
    book = load_workbook(path)
    sheet = book[sheet_name]
    book.remove(sheet)
    book._sheets.insert(index, sheet)
    book.save(path)

# Script execution
if __name__ == "__main__":
    print("Starting script...")
    client = init_plaid_client()
    start_date = (datetime.now() - pd.DateOffset(months=2)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    transactions = get_transactions(client, ACCESS_TOKEN, start_date, end_date)
    formatted_data = format_transactions(transactions)
    update_workbook(formatted_data, 'finances-workbook.xlsx')
    if not formatted_data.empty:
        reorder_sheets('finances-workbook.xlsx', 'Transactions', 0)
    print("Script completed.")


