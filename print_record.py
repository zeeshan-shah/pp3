from colorama import Fore, Style  # Import Fore and Style - text coloring


def print_record(records):
    for idx, record in enumerate(records):
        print(f"\n{Fore.YELLOW}Record {idx + 1}:")
        print(f"{Fore.BLUE}First Name: "
              f"{Fore.GREEN}{record['first_name']}")
        print(f"{Fore.BLUE}Last Name: "
              f"{Fore.GREEN}{record['last_name']}")
        print(f"{Fore.BLUE}Date of Birth: "
              f"{Fore.GREEN}{record['date_of_birth']}")
        print(f"{Fore.BLUE}Age: "
              f"{Fore.GREEN}{record['age']}")
        print(f"{Fore.BLUE}Address: "
              f"{Fore.GREEN}{record['address']}")
        print(f"{Fore.BLUE}Email: "
              f"{Fore.GREEN}{record['email']}")
        print(f"{Fore.BLUE}Job Position: "
              f"{Fore.GREEN}{record['job_position']}")
        print(f"{Fore.BLUE}Department: "
              f"{Fore.GREEN}{record['department']}")
        print(f"{Fore.BLUE}Salary: "
              f"{Fore.GREEN}{record['salary']}")
        print(f"{Fore.BLUE}Hire Date: "
              f"{Fore.GREEN}{record['hire_date']}")
        print(Style.RESET_ALL)
