# Import required libraries
import json  # Library for JSON operations
import re    # Library for regular expressions
import openpyxl # Import openpyxl library for working with Excel files
from openpyxl.styles import Font # Import Font class from openpyxl.styles module for styling Excel cells
import gspread # Import gspread library for accessing Google Sheets
from google.oauth2.service_account import Credentials  # Import Credentials class from google.oauth2.service_account module for authentication
from simple_term_menu import TerminalMenu # Import TerminalMenu class from simple_term_menu module for creating interactive menus in the terminal
import colorama # Import colorama library for terminal output coloring
from colorama import Fore, Style # Import Fore and Style classes from colorama module for text coloring
import os # Import os module for interacting with the operating system
import datetime # Import datetime module for working with dates and times

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json') # Load credentials from the service account file
SCOPED_CREDS = CREDS.with_scopes(SCOPE) # Load credentials from the service account file
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS) # Authorize the gspread client using the scoped credentials
SHEET = GSPREAD_CLIENT.open('pp3') # Open the Google Sheets document named 'pp3'

hris = SHEET.worksheet('hris') # Access the 'hris' worksheet within the Google Sheets document


def load_records():
    """
    Load records from Google Sheets.

    Returns:
        list: List of records.
    """
    records_data = hris.get_all_values()
    if not records_data:
        print("No records found in the worksheet.")
        return []

    fieldnames = [fieldname.lower() for fieldname in records_data[0]]
    records = [dict(zip(fieldnames, row)) for row in records_data[1:]]
    return records

def save_records(records):
    """
    Save records to Google Sheets.

    Args:
        records (list): List of records.
    """
    # Clear existing data in the worksheet
    hris.clear()

    # Write the fieldnames as column headers in uppercase
    fieldnames = list(records[0].keys())
    capitalized_fieldnames = [fieldname.upper() for fieldname in fieldnames]
    hris.insert_row(capitalized_fieldnames, 1)

    # Write the records to the worksheet
    for record in records:
        row_values = [record[fieldname] for fieldname in fieldnames]
        hris.append_row(row_values)

    print("Records saved to Google Sheets successfully!")

def add_record(records):
    """
    Add a new record to the HRIS.

    Args:
        records (list): List of records.
    """
    # Get input for each field of the record
    name = get_valid_name_input("Enter the employee full name: ", str, lambda x: True)
    date_of_birth = get_valid_dob_date("Enter the employee's date of birth (DD-MM-YYYY): ", min_age=18)
    
    # Calculate age from date of birth
    current_date = datetime.datetime.now().date()
    dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))

    # Check if the address is valid
    address = input("Enter the employee address: ")
    while not is_valid_address(address):
        print("Invalid address format! Please enter a valid address. The address should contain at least 5 characters.")
        address = input("Enter the employee address: ")

    email = get_valid_email("Enter the employee's email address: ")
    job_position = get_alphabetic_input("Enter the job position: ")
    department = get_alphabetic_input("Enter the department: ")
    salary = get_valid_input("Enter the employee's salary($): ", float, lambda x: x >= 0)
    # Calculate the minimum hire date (18 years after the date of birth)
    min_hire_date = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date() + datetime.timedelta(days=365 * 18)

    # Get the hire date
    hire_date = get_valid_hire_date("Enter the employee's hire date (DD-MM-YYYY): ", min_date=min_hire_date)

    # Create a record dictionary with the input values
    record = {
        'name': name,
        'date_of_birth': date_of_birth,
        'age': age,
        'address': address,
        'email': email,
        'job_position': job_position,
        'department': department,
        'salary': salary,
        'hire_date': hire_date
    }

    # Append the record to the list of records and save to file
    records.append(record)
    save_records(records)

def view_records(records):
    """
    View all records in the HRIS.

    Args:
        records (list): List of records.
    """
    if not records:
        print("No records found!")
    else:
        for idx, record in enumerate(records):
            print(f"\n{Fore.YELLOW}Record {idx + 1}:")
            print(f"{Fore.BLUE}Name: {Fore.GREEN}{record['name']}")
            print(f"{Fore.BLUE}Date of Birth: {Fore.GREEN}{record['date_of_birth']}")
            print(f"{Fore.BLUE}Age: {Fore.GREEN}{record['age']}")
            print(f"{Fore.BLUE}Address: {Fore.GREEN}{record['address']}")
            print(f"{Fore.BLUE}Email: {Fore.GREEN}{record['email']}")
            print(f"{Fore.BLUE}Job Position: {Fore.GREEN}{record['job_position']}")
            print(f"{Fore.BLUE}Department: {Fore.GREEN}{record['department']}")
            print(f"{Fore.BLUE}Salary: {Fore.GREEN}{record['salary']}")
            print(f"{Fore.BLUE}Hire Date: {Fore.GREEN}{record['hire_date']}")
            print(Style.RESET_ALL)

def update_record(records):
    """
    Update a record in the HRIS.

    Args:
        records (list): List of records.
    """
    if not records:
        print("No records available to update.")
        return

    # Display the existing records
    view_records(records)
    record_idx = get_valid_record_input("\nEnter the record number to update: ", int, lambda x: 1 <= x <= len(records)) - 1

    # Get the chosen record for updating
    record = records[record_idx]
    print(f"\nUpdating record {record_idx + 1}: {record['name']}")

    # Get updated input for each field of the record
    record['name'] = get_valid_name_input("Enter the employee full name: ", str, lambda x: True)
    record['date_of_birth'] = get_valid_dob_date("Enter the employee's date of birth (DD-MM-YYYY): ", min_age=18)
    date_of_birth = record['date_of_birth']
    # Calculate age from date of birth
    current_date = datetime.datetime.now().date()
    dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    record['age'] = age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    
    # Check if the address is valid
    address = input("Enter the employee address: ")
    while not is_valid_address(address):
        print("Invalid address format! Please enter a valid address. The address should contain at least 5 characters.")
        address = input("Enter the employee address: ")
    record['address'] = address
    record['email'] = get_valid_email("Enter the updated employee's email address: ")
    record['job_position'] = get_alphabetic_input("Enter the updated employee's job position: ")
    record['department'] = get_alphabetic_input("Enter the updated employee's department: ")
    record['salary'] = get_valid_input("Enter the updated employee's salary($): ", float, lambda x: x >= 0)

    # Calculate the minimum hire date (18 years after the date of birth)
    min_hire_date = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date() + datetime.timedelta(days=365 * 18)

    # Get the hire date
    hire_date = get_valid_hire_date("Enter the employee's hire date (DD-MM-YYYY): ", min_date=min_hire_date)

    # Save the updated records to file
    save_records(records)
    print("Record updated successfully!")

def delete_record(records):
    """
    Delete a record from the HRIS.

    Args:
        records (list): List of records.
    """
    if not records:
        print("No records available to delete.")
        return

    # Display the existing records
    view_records(records)
    record_idx = get_valid_record_input("\nEnter the record number to delete: ", int, lambda x: 1 <= x <= len(records)) - 1

    # Get the chosen record for deletion
    record = records[record_idx]
    print(f"\nDeleting record {record_idx + 1}: {record['name']}")
    confirm = get_confirmation_input("Are you sure you want to delete this record? (y/n): ")

    if confirm.lower() == 'y':
        # Delete the record from the list and save to file
        del records[record_idx]
        save_records(records)
        print("Record deleted successfully!")
    else: 
        print("Deletion cancelled.")
        print("Return to HRIS!")
        hris_menu(records)

def search_records(records):
    """
    Search records in the HRIS based on a search term.

    Args:
        records (list): List of records.
    """
    if not records:
        print("No records available to search.")
        return

    search_term = input("Enter the search term: ")
    found_records = []
    for record in records:
        # Search for records with a matching name
        if search_term.lower() in record['name'].lower():
            found_records.append(record)
    if found_records:
        view_records(found_records)
    else:
        print("No matching records found.")

def sort_records(records):
    """
    Sort records in the HRIS based on a sorting choice.

    Args:
        records (list): List of records.
    """
    if not records:
        print("No records available to sort.")
        return

    sort_choice = input("Sort records by (name/age/department): ").lower()
    if sort_choice == 'name':
        # Sort records by name
        records.sort(key=lambda x: x['name'])
    elif sort_choice == 'age':
        # Sort records by age
        records.sort(key=lambda x: x['age'])
    elif sort_choice == 'department':
        # Sort records by department
        records.sort(key=lambda x: x['department'])
    else:
        print("Invalid sorting choice!")
        return

    print("Records sorted successfully!")
    view_records(records)

def main_menu(records):
    """
    Main menu.

    Args:
        records (list): List of records.
    """
    print("*********************************************\n")
    print("Welcome to Human Resources Information System\n")
    print("*********************************************\n")
    print("Welcome to our secure and efficient employee data management application.")
    print("Our app is designed specifically to ensure the utmost security and organization of your company's valuable employee data.")
    print("With our powerful features and intuitive interface, you can confidently store and manage all necessary information with ease.\n") 
    print("----------------------------------------------------------------------------------------------------------------------------\n")
    while True:
        
        # Define menu options
        options = [
            "HRIS Menu",
            "Instructions"
        ]

        # Create menu object
        menu = TerminalMenu(options)

        # Display the menu and get user's choice
        menu_index = menu.show()

        if menu_index == 0:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Add a new record
            hris_menu(records)
        elif menu_index == 1:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # View all records
            print("Brief Application Instructions:\n")
            print("To utilize this application effectively, please follow these steps:\n")
            print("1. Navigation: Use the arrow keys to navigate through the menu options.\n")
            print("2. HRIS Menu: Within the HRIS Menu, you will find various features to manage employee data efficiently. These features include:\n")
            print("* Adding new employee data: Enter new employee information to store it securely.")
            print("* Viewing stored data: Access and review the existing employee data.")
            print("* Updating existing data: Modify and update employee records as required.")
            print("* Deleting stored data: Remove employee data that is no longer needed.")
            print("* Searching the data: Utilize search functionality to locate specific employee information.")
            print("* Sorting the data: Arrange employee data based on specific criteria for easier analysis.")
            print("\n")
            print("By following these instructions, you can effectively navigate and utilize the features provided by the HRIS application.\n")
            print("Navigate to HRIS MENU: Locate and select the 'HRIS MENU' option\n")

def hris_menu(records):
    """
    Human Resources Information System (HRIS) menu.

    Args:
        records (list): List of records.
    """   
    while True:
        # Define menu options
        options = [
            "Add Record",
            "View Records",
            "Update Record",
            "Delete Record",
            "Search Records",
            "Sort Records",
            "Exit"
        ]

        # Create menu object
        menu = TerminalMenu(options)

        # Display the menu and get user's choice       
        menu_index = menu.show()

        if menu_index == 0:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Add a new record
            add_record(records)
        elif menu_index == 1:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # View all records
            view_records(records)
        elif menu_index == 2:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Update a record
            update_record(records)
        elif menu_index == 3:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Delete a record
            delete_record(records)
        elif menu_index == 4:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Search for records
            search_records(records)
        elif menu_index == 5:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # Sort records
            sort_records(records)
        elif menu_index == 6:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            main_menu(records)
            
        else:
            print("Invalid choice! Please try again.")
        
def get_valid_name_input(prompt, data_type, condition):
    """
    Get valid user input based on data type and condition.

    Args:
        prompt (str): The input prompt message.
        data_type (type): The expected data type of the input.
        condition (callable): A condition function to validate the input.

    Returns:
        The validated user input.
    """
    while True:
        value = input(prompt)
        if len(value) >= 2 and not re.search(r'\d|\W', value):
            try:
                return data_type(value)
            except ValueError:
                print("Invalid input! Please enter a valid value.")
        else:
            print("Invalid input! Please enter at least 2 characters that are not numbers or special characters.")

def get_valid_input(prompt, data_type, condition):
    """
    Get valid user input based on data type and condition.

    Args:
        prompt (str): The input prompt message.
        data_type (type): The expected data type of the input.
        condition (callable): A condition function to validate the input.

    Returns:
        The validated user input.
    """
    while True:
        try:
            value = data_type(input(prompt))
            if condition(value):
                return value
            else:
                print("Invalid input! Enter a positive amount using only numbers(5000) and the decimal point '.' (e.g: 4500.80).")
        except ValueError:
            print("Invalid input! Enter a positive amount using only numbers(5000) and/or the decimal point '.' (e.g: 4500.80).")

def get_valid_dob_date(message, min_age=None):
    """
    Prompt the user to enter a valid date in the format (DD-MM-YYYY) with an optional minimum age constraint.

    Args:
        message (str): The message to display when prompting for input.
        min_age (int): The minimum age in years for the date. Defaults to None.

    Returns:
        str: The valid date string in the format (DD-MM-YYYY).
    """
    while True:
        date_str = input(message)
        try:
            # Check if the entered date is a valid date
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()

            # Check if the entered date is not in the future
            if date > datetime.datetime.now().date():
                print("Invalid date! Please enter a date before today.")
                continue

            # Check if the entered date is not older than 1970
            if date.year < 1970:
                print("Invalid date! Please enter a date after 1970.")
                continue

            # Check if the entered date satisfies the minimum age constraint
            if min_age is not None:
                min_age_date = datetime.datetime.now().date() - datetime.timedelta(days=365 * min_age)
                if date > min_age_date:
                    print("Invalid date! The employee does not meet the age requirement. The minimum age for employment is 18 years.")
                    continue

            return date_str
        except ValueError:
            print("Invalid date format! Please enter a valid date (DD-MM-YYYY).")

def get_valid_hire_date(message, min_date=None):
    """
    Prompt the user to enter a valid date in the format (DD-MM-YYYY) with an optional minimum date constraint.

    Args:
        message (str): The message to display when prompting for input.
        min_date (datetime.date): The minimum date constraint. Defaults to None.

    Returns:
        str: The valid date string in the format (DD-MM-YYYY).
    """
    while True:
        date_str = input(message)
        try:
            # Check if the entered date is a valid date
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()

            # Check if the entered date is not in the future
            if date > datetime.datetime.now().date():
                print("Invalid date! Please enter a date before today.")
                continue

            # Check if the entered date is not older than 1970
            if date.year < 1970:
                print("Invalid date! Please enter a date after 1970.")
                continue

            # Check if the entered date satisfies the minimum date constraint
            if min_date is not None and date < min_date:
                print("Invalid date! The employee does not meet the age requirement. The minimum age for employment is 18 years.")
                continue

            return date_str
        except ValueError:
            print("Invalid date format! Please enter a valid date (DD-MM-YYYY).")

def is_valid_address(address):
    # Regular expression pattern for address format validation
    pattern = r'^[a-zA-Z0-9\s.,#-]{5,}$'

    if re.match(pattern, address):
        return True
    else:
        return False

def get_alphabetic_input(prompt):
    while True:
        user_input = input(prompt)
        if re.match(r'^[a-zA-Z]{2,}$', user_input):
            return user_input
        else:
            print("Invalid input! Please enter a value consisting of at least 2 alphabetic characters only.")

def get_valid_email(prompt):
    """
    Get a valid email address input from the user.

    Args:
        prompt (str): The input prompt message.

    Returns:
        str: The validated email address.
    """
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    while True:
        email = input(prompt)
        if re.match(email_pattern, email):
            return email
        else:
            print("Invalid email address! Please enter a valid email address.")

def get_confirmation_input(prompt):
    while True:
        response = input(prompt)
        if response.lower() == 'y' or response.lower() == 'n':
            return response.lower()
        else:
            print("Invalid input! Please enter 'y' for Yes or 'n' for No.")

def get_valid_record_input(prompt, data_type, condition):
    """
    Get a valid record number input based on data type and condition.

    Args:
        prompt (str): The input prompt message.
        data_type (type): The expected data type of the input.
        condition (callable): A condition function to validate the input.

    Returns:
        The validated record number input.
    """
    while True:
        try:
            value = data_type(input(prompt))
            if condition(value):
                return value
            else:
                print("Invalid input! Please enter a valid record number.")
        except ValueError:
            print("Invalid input! Please enter a valid record number.")

# Load records from file
records = load_records()

# Clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# Run the HRIS
main_menu(records)
            