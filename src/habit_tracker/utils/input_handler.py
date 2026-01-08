from datetime import datetime
from habit_tracker.data_store import(find_habit_by_id)
from habit_tracker.utils import logger
from colorama import Fore, Style

def get_non_empty_string(prompt):
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty!")
    return value

def get_int(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("Please enter a valid number.")
    return int(value)
    
def get_optional_string(prompt):
    return input(prompt).strip()

def get_valid_date(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            parsed = datetime.strptime(user_input, "%Y-%m-%d")
            return parsed.date().isoformat()
        except ValueError:
            print("Please enter date as YYYY-MM-DD")

def prompt_for_existing_habit(data, prompt):
    """Prompt user for habit ID and return habit. Returns None if users choose 0 (Go back)"""
    while True:
        try:
            habit_id = get_int(prompt)
        except ValueError as e:
            print(e)
            logger.info("Invalid habit ID input.")
            continue

        if habit_id == 0:
            logger.debug("User chose to go back.")
            return None

        habit = find_habit_by_id(data, habit_id)
        if habit is None:
            print("Habit not found. Try again.")
            logger.info(f"Habit ID {habit_id} not found.")
            continue

        return habit
    
def prompt_for_frequency():
    while True:
        print("Frequency type:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")

        choice = input("Choose frequency type: ")

        if choice == "1":
            freq_type = "daily"
        elif choice == "2":
            freq_type = "weekly"
        elif choice == "3":
            freq_type = "monthly"
        else:
            print("Invalid choice. Try again.")
            continue

        try:
            times = get_int(f"How many times {freq_type} ?")
            if times < 1:
                raise ValueError
        except ValueError:
            logger.info("Invalid input for times")
            print("Please enter a number greater than 0.")
            continue
        
        return freq_type, times

def confirm_action(prompt):
    """Ask the user to confirm an action. Returns True for YES, False for NO. Keeps prompting until valid input is given."""
    while True:
        answer = input(f"\n   {Fore.RED}{Style.BRIGHT}ATTENTION!{Style.RESET_ALL} {prompt} (YES/NO): ").strip().upper()

        if answer == "YES":
            return True
        if answer == "NO":
            return False

        print("   Please type YES or NO.")
        logger.info(f"Invalid confirmation input: {answer}")