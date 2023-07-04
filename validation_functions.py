import re  # Library for regular expressions
from colorama import Fore, Style  # Import Fore and Style - text coloring
import datetime  # Import datetime module for working with dates and times

red_color = Fore.RED
reset_style = Style.RESET_ALL


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
                print(red_color + "Invalid input! Please enter a valid value.")
                print(reset_style)
        else:
            print(
                red_color +
                "Invalid input! Please enter at least 2 characters " +
                "that are not numbers or special characters."
            )
            print(reset_style)


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
                print(
                    red_color +
                    "Invalid input! Enter a positive amount using "
                    "only numbers and the decimal point (e.g., 4500.80)."
                )
                print(reset_style)
        except ValueError:
            print(
                red_color +
                "Invalid input! Enter a positive amount using only "
                "numbers(5000) and/or the decimal point '.' (e.g: 4500.80)."
            )
            print(reset_style)


def get_valid_dob_date(message, min_age=None):
    """
    Prompt the user to enter a valid date in the format (DD-MM-YYYY)
    with an optional minimum age constraint.

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
                print(
                    red_color +
                    "Invalid date! Please enter a date before today."
                )
                print(reset_style)
                continue

            # Check if the entered date is not older than 1970
            if date.year < 1970:
                print(
                    red_color +
                    "Invalid date! Please enter a date after 1970."
                )
                print(reset_style)
                continue

            # Check if the entered date satisfies the minimum age constraint
            if min_age is not None:
                min_age_date = datetime.datetime.now().date() - \
                               datetime.timedelta(days=365 * min_age)
                if date > min_age_date:
                    print(
                        red_color +
                        "Invalid date! The employee does not meet "
                        "the age requirement. The minimum age for employment "
                        "is 18 years."
                    )
                    print(reset_style)
                    continue

            return date_str
        except ValueError:
            print(
                red_color +
                "Invalid date format! "
                "Please enter a valid date (DD-MM-YYYY)."
            )
            print(reset_style)


def get_valid_hire_date(message, min_date=None):
    """
    Prompt the user to enter a valid date in the format (DD-MM-YYYY)
     with an optional minimum date constraint.

    Args:
        message (str): The message to display when prompting for input.
        min_date (datetime.date): The minimum date constraint.
        Defaults to None.

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
                print(
                    red_color +
                    "Invalid date! Please enter a date before today."
                )
                print(reset_style)
                continue

            # Check if the entered date is not older than 1970
            if date.year < 1970:
                print(
                    red_color +
                    "Invalid date! Please enter a date after 1970."
                )
                print(reset_style)
                continue

            # Check if the entered date satisfies the minimum date constraint
            if min_date is not None and date < min_date:
                print(
                    red_color +
                    "Invalid date! The employee does not meet the "
                    "age requirement. The minimum age for employment "
                    "is 18 years."
                )
                print(reset_style)
                continue

            return date_str
        except ValueError:
            print(
                red_color +
                "Invalid date format! "
                "Please enter a valid date (DD-MM-YYYY)."
            )
            print(reset_style)


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
            print(
                red_color +
                "Invalid input! "
                "Please enter a value consisting of at least "
                "2 alphabetic characters only."
            )
            print(reset_style)


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
            print(
                red_color +
                "Invalid email address! "
                "Please enter a valid email address."
            )
            print(reset_style)


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
                print(
                    red_color +
                    "Invalid input! "
                    "Please enter a valid record number."
                )
                print(reset_style)
        except ValueError:
            print(
                red_color +
                "Invalid input! "
                "Please enter a valid record number.")
            print(reset_style)
