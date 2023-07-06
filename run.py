# Import required libraries

import gspread  # Import gspread library for accessing Google Sheets
from google.oauth2.service_account import Credentials  # Import Credentials
from simple_term_menu import TerminalMenu  # Import TerminalMenu class
from colorama import Fore, Style  # Import Fore and Style - text coloring
import os  # Import os module for interacting with the operating system
import datetime  # Import datetime module for working with dates and times
import time  # Import time module
from validation_functions import get_valid_name_input
from validation_functions import get_valid_input
from validation_functions import get_valid_dob_date
from validation_functions import get_valid_hire_date
from validation_functions import is_valid_address
from validation_functions import get_valid_email
from validation_functions import get_confirmation_input
from validation_functions import get_valid_record_input
from validation_functions import get_job_input
from validation_functions import get_department_input
from print_record import print_record

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the service account file
CREDS = Credentials.from_service_account_file('creds.json')
# Load credentials from the service account file
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Authorize the gspread client using the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Open the Google Sheets document named 'pp3'
SHEET = GSPREAD_CLIENT.open('pp3')
# Access the 'hris' worksheet within the Google Sheets document
hris = SHEET.worksheet('hris')

red_color = Fore.RED
reset_style = Style.RESET_ALL


def load_records():
    """
    Load records from Google Sheets.

    Returns:
        list: List of records.
    """
    records_data = hris.get_all_values()
    if not records_data:
        print(red_color + "No records found in the worksheet.")
        print(reset_style)
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

    if len(records) >= 1:
        # Write the fieldnames as column headers in uppercase
        fieldnames = list(records[0].keys())
        capitalized_fieldnames = [
            fieldname.upper() for fieldname in fieldnames
        ]
        hris.insert_row(capitalized_fieldnames, 1)

    # Write the records to the worksheet
    for record in records:
        row_values = [record[key] for key in record.keys()]
        hris.append_row(row_values)

    print("\n")  # Add whitespace above the progress update

    for i in range(1, 101):
        print(f"{Fore.LIGHTRED_EX}Saving progress: {i}%", end="\r")
        time.sleep(0.025)

    print("\n")  # Add whitespace below the progress update

    print(
        Fore.LIGHTGREEN_EX +
        "\nRecords saved to Google Sheets successfully!\n"
    )


def add_record(records):
    """
    Add a new record to the HRIS.

    Args:
        records (list): List of records.
    """
    # Get input for each field of the record
    first_name = get_valid_name_input(
        "Enter the employee first name: ",
        str,
        lambda x: True
    )
    last_name = get_valid_name_input(
        "Enter the employee last name: ",
        str,
        lambda x: True
    )
    date_of_birth = get_valid_dob_date(
        "Enter the employee's date of birth (DD-MM-YYYY): ",
        min_age=18
    )

    # Calculate age from date of birth
    current_date = datetime.datetime.now().date()
    dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    age = (
        current_date.year - dob.year
        - ((current_date.month, current_date.day) < (dob.month, dob.day))
    )

    # Check if the address is valid
    address = input("Enter the employee address: ")
    while not is_valid_address(address):
        print(
            red_color +
            "Invalid address format! Please enter a valid address."
        )
        print("The address should contain at least 5 characters.")
        print(reset_style)
        address = input("Enter the employee address: ")

    email = get_valid_email("Enter the employee's email address: ")
    job_position = get_job_input("Enter the job position: ")
    department = get_department_input("Enter the department: ")
    salary = get_valid_input(
        "Enter the employee's salary($): ",
        float, lambda x: x >= 0
    )
    # Calculate the minimum hire date (18 years after the date of birth)
    min_hire_date = (
        datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date() +
        datetime.timedelta(days=365 * 18)
    )

    # Get the hire date
    hire_date = get_valid_hire_date(
        "Enter the employee's hire date (DD-MM-YYYY): ",
        min_date=min_hire_date
    )

    # Create a record dictionary with the input values
    record = {
        'first_name': first_name,
        'last_name': last_name,
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
        print(red_color + "No records found!")
        print(reset_style)
    else:
        print_record(records)


def update_record(records):
    """
    Update a record in the HRIS.

    Args:
        records (list): List of records.
    """
    if not records:
        print(red_color + "No records available to update.")
        print(reset_style)
        return

    # Display the existing records
    view_records(records)
    record_idx = get_valid_record_input(
        "\nEnter the record number to update: ",
        int,
        lambda x: 1 <= x <= len(records)
    ) - 1

    # Get the chosen record for updating
    record = records[record_idx]
    print(f"\nUpdating record {record_idx + 1}: {record['first_name']} "
          f"{record['last_name']}")

    # Get updated input for each field of the record
    record['first_name'] = get_valid_name_input(
        "Enter the employee first name: ",
        str,
        lambda x: True
    )
    record['last_name'] = get_valid_name_input(
        "Enter the employee last name: ",
        str,
        lambda x: True
    )
    record['date_of_birth'] = get_valid_dob_date(
        "Enter the employee's date of birth (DD-MM-YYYY): ",
        min_age=18
    )
    date_of_birth = record['date_of_birth']
    # Calculate age from date of birth
    current_date = datetime.datetime.now().date()
    dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    age = (
        current_date.year - dob.year -
        ((current_date.month, current_date.day) < (dob.month, dob.day))
    )
    record['age'] = age

    # Check if the address is valid
    address = input("Enter the employee address: ")
    while not is_valid_address(address):
        print(
            red_color +
            "Invalid address format! Please enter a valid address. " +
            "The address should contain at least 5 characters."
        )
        print(reset_style)
        address = input("Enter the employee address: ")
    record['address'] = address
    record['email'] = get_valid_email(
        "Enter the updated employee's email address: "
    )
    record['job_position'] = get_job_input(
        "Enter the updated employee's job position: "
    )
    record['department'] = get_department_input(
        "Enter the updated employee's department: "
    )
    record['salary'] = get_valid_input(
        "Enter the updated employee's salary($): ",
        float,
        lambda x: x >= 0
    )

    # Calculate the minimum hire date (18 years after the date of birth)
    min_hire_date = (
        datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date() +
        datetime.timedelta(days=365 * 18)
    )

    # Get the hire date
    hire_date = get_valid_hire_date(
        "Enter the employee's hire date (DD-MM-YYYY): ",
        min_date=min_hire_date)
    record['hire_date'] = hire_date

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
        print(red_color + "No records available to delete.")
        print(reset_style)
        return

    # Display the existing records
    view_records(records)
    record_idx = get_valid_record_input(
        "\nEnter the record number to delete: ",
        int,
        lambda x: 1 <= x <= len(records)
    ) - 1

    # Get the chosen record for deletion
    record = records[record_idx]
    print(
        f"\nDeleting record {record_idx + 1}: "
        f"{record['first_name']} {record['last_name']}"
    )
    confirm = get_confirmation_input(
        Fore.YELLOW +
        "Are you sure you want to delete this record? (y/n): "
    )
    print(reset_style)

    if confirm.lower() == 'y':
        # Delete the record from the list and save to file
        del records[record_idx]
        print(Fore.GREEN + "Record deleted successfully!")
        save_records(records)
    else:
        print(red_color + "Deletion cancelled.")
        print(reset_style)
        print("Return to HRIS!")
        hris_menu(records)


def search_records(records):
    """
    Search records in the HRIS based on a search term.

    Args:
        records (list): List of records.
    """
    if not records:
        print(red_color + "No records available to search.")
        print(reset_style)
        return

    search_term = input("Enter the search term(first-/lastname): ")
    found_records = []
    for record in records:
        # Search for records with a matching name
        if (search_term.lower() in record['first_name'].lower() or
           search_term.lower() in record['last_name'].lower()):
            found_records.append(record)
    if found_records:
        view_records(found_records)
    else:
        print(red_color + "No matching records found.")
        print(reset_style)


def sort_records(records):
    """
    Sort records in the HRIS based on a sorting choice.

    Args:
        records (list): List of records.
    """
    if not records:
        print(red_color + "No records available to sort.")
        print(reset_style)
        return

    sort_choice = input("Sort records by (first name/last name/age/"
                        "department): ").lower()
    if sort_choice == 'first name':
        # Sort records by first name
        records.sort(key=lambda x: x['first_name'])
    elif sort_choice == 'last name':
        # Sort records by last name
        records.sort(key=lambda x: x['last_name'])
    elif sort_choice == 'age':
        # Sort records by age
        records.sort(key=lambda x: x['age'])
    elif sort_choice == 'department':
        # Sort records by department
        records.sort(key=lambda x: x['department'])
    else:
        print(red_color + "Invalid sorting choice!")
        print(reset_style)
        return

    print(Fore.GREEN + "Records sorted successfully!")
    view_records(records)
    save_records(records)


def main_menu(records):
    """
    Main menu.

    Args:
        records (list): List of records.
    """
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "*********************************************")
    print(Fore.BLUE + "Welcome to Human Resources Information System\n")
    print(Fore.GREEN + "*********************************************")
    print(Style.RESET_ALL)
    print("Welcome to our secure and efficient employee\ndata management "
          "application.\n")
    print("Our app is designed specifically to ensure the\nutmost security "
          "and organization of your\ncompany's valuable employee data. "
          "With our\npowerful features and intuitive interface, you\ncan "
          "confidently store andmanage all\nnecessary information with ease."
          )
    print("--------------------------------------------------\n")
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
            print(Fore.YELLOW + "Brief Application Instructions:\n")
            print(Style.RESET_ALL)
            print(
                "To utilize this application effectively, "
                "please follow these steps:\n"
                "1. Navigation: Use the arrow keys to "
                "navigate through the menu options.\n"
                "2. HRIS Menu: Within the HRIS Menu, you will "
                "find various features to manage employee data efficiently. "
                "These features include:\n"
                "\n"
                "* Adding new employee data: Enter new employee " +
                "information to store it securely.\n"
                "* Viewing stored data: Access and review " +
                "the existing employee data.\n"
                "* Updating existing data: Modify and update " +
                "employee records as required.\n"
                "* Deleting stored data: Remove employee data " +
                "that is no longer needed.\n"
                "* Searching the data: Utilize search functionality " +
                "to locate specific employee information.\n"
                "* Sorting the data: Arrange employee data based on " +
                "specific criteria for easier analysis."
            )
            print("\n")
            print(
                "By following these instructions, you can effectively "
                "navigate and utilize the features provided by "
                "the HRIS application.\n"
            )
            print(
                Fore.BLUE +
                "Navigate to HRIS MENU: Locate and "
                "select the 'Main MENU' option\n"
            )
            # Update options list to show only "HRIS Menu"
            options = ["Main Menu"]
            # Create update menu object without Instructions option
            menu = TerminalMenu(options)

            # Display the updated menu
            menu_index = menu.show()

            if menu_index == 0:
                main_menu(records)


def hris_menu(records):
    """
    Human Resources Information System (HRIS) menu.

    Args:
        records (list): List of records.
    """
    while True:
        print(Fore.YELLOW + "=============================")
        print("      HRIS MENU")
        print("   Select an Option:")
        print("=============================" + Fore.RESET)

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
            print(red_color + "Invalid choice! Please try again.")
            print(reset_style)


# Load records from file
records = load_records()

# Clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# Run the HRIS
main_menu(records)
