# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

#sales = SHEET.worksheet('sales')
#data = sales.get_all_values()
#print(data)

def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a valid string of data from user via terminal
    which must be a string of 6 numbers separated by commas. The loop will
    repeatedly request data until it is valid.
    """
    while True:
        print('''
        
█░█░█ █▀█ █▀█ █░░ █▀▄   █▀▀ █░█ █▀█   ▀█ █▀█ ▀█ ▀█
▀▄▀▄▀ █▄█ █▀▄ █▄▄ █▄▀   █▄▄ █▄█ █▀▀   █▄ █▄█ █▄ █▄\n''')

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Examples: 10,11,12,13,14,15\n")
        
        data_str = input("Enter your data here:\n")
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data

def validate_data(values):
    """
    Converts string into integers.
    Raises ValueError if strings cant be converted into ints,
    of if there arent 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f'6 values required. You provided only {len(values)} values')
    except ValueError as e:
        print(f'Invalid data: {e}.\n')
        return False
    
    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted in a worksheet
    Update relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_update = SHEET.worksheet(worksheet)
    worksheet_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus with each item type.
    
    Surplus is defined as the sales figure subtracted from the stock:
    Positive equals waste.
    Negative equals extra made after stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries():
    """
    Collects columns of data from sales worksheet,
    collecting the last 5 entries for each sandwich and
    returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")
   
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock data for each item type, adding 10%
    """
    print("Calculating stock data...\n")

    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation!\n")
main()