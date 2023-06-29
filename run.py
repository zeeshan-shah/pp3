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