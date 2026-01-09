from habit_tracker.utils import logger
from colorama import Fore, Style

from habit_tracker.models.habit import Habit
from habit_tracker.utils.input_handler import(get_non_empty_string, get_optional_string, get_valid_date, prompt_for_existing_habit, prompt_for_frequency, confirm_action)
from habit_tracker.data_store import(load_habits, get_new_id, save_habits)
from habit_tracker.utils import logger

"""handles basic CRUD functions for instances of habits"""

### Add a Habit ###

def add_habit():
    data = load_habits()
    new_id = get_new_id(data)

    try:
        name = get_non_empty_string("   Habit name: ")                     #input_handler.py checks for valid input
        description = get_optional_string("   Description (optional): ")   #input_handler.py checks for valid input
    except ValueError as e:
        print(e)
        return

    frequency_type, frequency_times = prompt_for_frequency()

    new_habit = Habit(new_id, name, description, frequency_type, frequency_times)

    data["habits"].append(new_habit.to_dict())
    save_habits(data)

    logger.info(f"Habit '{name}' added successfully.")

### List Habits ###

def list_habits(data):
    if not data["habits"]:
        print("No habits found.")
        return False
    
    print("\n")
    print(Fore.MAGENTA + "   " + ("-" * 20) + Style.RESET_ALL)
    print(f"   {Fore.MAGENTA}{Style.BRIGHT}Your habits{Style.RESET_ALL}")
    print(Fore.MAGENTA + "   " + ("-" * 20) + "\n" + Style.RESET_ALL)

    print(
    f"   {Fore.YELLOW}Unique ID{Style.RESET_ALL}: "
    f"{Fore.LIGHTMAGENTA_EX}Habit Name{Style.RESET_ALL} - {Fore.LIGHTRED_EX}Description{Style.RESET_ALL} "
    f"{Fore.CYAN}(Frequency){Style.RESET_ALL}"
    )
    print("   " + ("-"*47) + "\n")

    for habit in data["habits"]:
        freq = habit["frequency"]

        print(
            f"   {Fore.YELLOW}{habit['id']}{Style.RESET_ALL}: "
            f"{Fore.LIGHTMAGENTA_EX}{habit['name']}{Style.RESET_ALL} - {Fore.LIGHTRED_EX}{habit['description']}{Style.RESET_ALL} "
            f"{Fore.CYAN}({freq['times']}x {freq['type']}){Style.RESET_ALL}\n"
        )

    return True

### Edit Habit ###

def edit_habit():
    data = load_habits()
    list_habits(data)
    logger.debug("User entered edit-habit menu.")

    if not data['habits']:
        print("   No habits in list.")
        return

    habit = prompt_for_existing_habit(data, "   Enter habit ID to edit (0 to go back): ")
    if habit is None:
        return

    try:
        habit["name"] = get_non_empty_string("   New name: ")                              #input_handler.py checks for valid input
        habit["description"] = get_optional_string("   New description (optional): ")      #input_handler.py checks for valid input
    except ValueError as e:
        print(e)
        logger.info("Invalid input while editing habit.")
        return

    save_habits(data)
    logger.info(f"Habit '{habit['name']}' updated.")                                    ### Logger INFO example
    logger.debug("User exited edit-habit menu.")
    return

### Mark Habit Done ###

def mark_habit_done_for_date(target_date=None):
    data = load_habits()
    list_habits(data)
    logger.debug("User entered mark-habit-done menu.")

    habit = prompt_for_existing_habit(data, "Enter habit ID to mark as done (0 to go back): ")
    if habit is None:
        logger.debug("User exited mark-habit-done menu.")
        return

    if target_date is None:
        target_date = get_valid_date("Enter date (YYYY-MM-DD): ")

    if target_date in habit["completed_days"]:
        logger.info(
            f"Habit '{habit['name']}' was already marked as done on {target_date}."
        )
        return

    habit["completed_days"].append(target_date)
    save_habits(data)

    logger.info(f"Habit '{habit['name']}' marked done on {target_date}.")

### Delete Habit ###

def delete_habit():
    data = load_habits()
    list_habits(data)
    logger.debug("User entered delete-habit menu.")

    habit = prompt_for_existing_habit(data, "   Enter habit ID to delete (0 to go back): ")
    if habit is None:
        logger.debug("User exited delete-habit menu.")
        return

    # Confirmation
    if confirm_action(f"   Are you sure you want to delete '{habit['name']}'"):
        data["habits"].remove(habit)
        save_habits(data)
        logger.info(f"Habit '{habit['name']}' deleted.")
    else:
        logger.info(f"Deletion cancelled for habit '{habit['name']}'.")

