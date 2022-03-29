# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Examples: 10,11,12,13,14,15\n")
        
        data_str = input("Enter your data here: ")
        
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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data providede
    """
    print("Updating sales worksheet...")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

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

def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to Love Sandwiches Data Automation!\n")
main()