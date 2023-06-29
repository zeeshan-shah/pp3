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

        