# Import required libraries
import json  # Library for JSON operations

def load_records():
    """
    Load records from a JSON file.

    Returns:
        list: List of records.
    """
    try:
        with open('records.json', 'r') as file:
            records = json.load(file)  # Load JSON data from file
    except FileNotFoundError:
        records = []  # Create an empty list if file not found
    return records

def save_records(records):
    """
    Save records to a JSON file.

    Args:
        records (list): List of records.
    """
    with open('records.json', 'w') as file:
        json.dump(records, file, indent=4)  # Write JSON data to file with indentation

def add_record(records):
    """
    Add a new record to the HRIS.

    Args:
        records (list): List of records.
    """
    # Get input for each field of the record
    name = input("Enter the employee full name: ")
    date_of_birth = get_valid_date("Enter the employee's date of birth (DD-MM-YYYY): ")
    age = get_valid_input("Enter the employee's age (18 or above): ", int, lambda x: x >= 18)
    address = input("Enter the employee's address: ")
    email = get_valid_email("Enter the employee's email address: ")
    job_position = input("Enter the job position: ")
    department = input("Enter the department: ")
    salary = get_valid_input("Enter the employee's salary: ", float, lambda x: x >= 0)
    hire_date = get_valid_date("Enter the employee's hire date (DD-MM-YYYY): ")        

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