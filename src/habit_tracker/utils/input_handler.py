from habit_tracker.config import DATA_PATH
from datetime import datetime

def get_non_empty_string(prompt):
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty!")
    return value
    
def get_optional_string(prompt):
    return input(prompt).strip()

def get_int(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("Please enter a valid number.")
    return int(value)

def get_valid_date(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            parsed = datetime.strptime(user_input, "%Y-%m-%d")
            return parsed.date().isoformat()
        except ValueError:
            print("Please enter date as YYYY-MM-DD")