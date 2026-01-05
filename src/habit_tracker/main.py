import json
from datetime import date

from habit_tracker.config import DATA_PATH
from habit_tracker.models.habit import Habit
from habit_tracker.utils import logger
from habit_tracker.utils.input_handler import(get_non_empty_string, get_optional_string, get_int, get_valid_date)

# ----- JSON / Data helpers ----- 

def load_habits():
    # File does not exist yet
    if not DATA_PATH.exists():
        logger.warning("Habits file not found. Creating new file.")     ### Logger WARNING example - missing file ### 
        return {"next_id": 1, "habits": []}

    try:
        # Handle empty file
        if DATA_PATH.stat().st_size == 0:
            logger.warning("Habits file is empty. Reinitializing.")
            return {"next_id": 1, "habits": []}
        
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            logger.debug(f"Loaded habits data: {json_data}")            ### Logger DEBUG example ###

        # ----- Backward compatibility -----
        if "habits" not in json_data:
            json_data["habits"] = []
            logger.warning("Missing 'habits' key. Initialized empty list.")

        if "next_id" not in json_data:
            max_id = max((h["id"] for h in json_data.get("habits", [])), default=0)
            json_data["next_id"] = max_id + 1
            logger.debug(f"Added missing next_id field (starting at {json_data['next_id']})")

        return json_data

    except json.JSONDecodeError as e:
        logger.error(f"Habits file is corrupted: {e}")                  ### Logger ERROR example - corrupted file ###
        raise
    
def save_habits(data):
    try:
        logger.debug(f"Saving habits to {DATA_PATH}")                   ### Logger DEBUG example ###
        logger.debug(f"Data to save: {data}")                         ### Logger DEBUG example ###

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            logger.info("Habits saved successfully.")                   ### Logger INFO example ###
    except Exception as e:
        logger.error(f"Failed to save habits: {e}")                     ### Logger ERROR example ###
        raise

def get_new_id(data):
    new_id = data["next_id"]
    data["next_id"] += 1
    return new_id

def find_habit_by_id(data, habit_id):
    """Return habit dictionary with matching ID if found, or None if it doesn't exist."""
    for habit in data['habits']:
        if habit['id'] == habit_id:
            return habit
    return None

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
            times = get_int(f"How many times {freq_type}?")
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
        answer = input(f"{prompt} (YES/NO): ").strip().upper()

        if answer == "YES":
            return True
        if answer == "NO":
            return False

        print("Please type YES or NO.")
        logger.info(f"Invalid confirmation input: {answer}")

# ----- Features ----- 

### Add a Habit ###

def add_habit():
    data = load_habits()
    new_id = get_new_id(data)

    try:
        name = get_non_empty_string("Habit name: ")                     #input_handler.py checks for valid input
        description = get_optional_string("Description (optional): ")   #input_handler.py checks for valid input
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
    
    print("\nYour habits:\n")
    print("(Unique ID: Habit Name - Description) \n")

    for habit in data["habits"]:
        freq = habit["frequency"]
        print(
        f"{habit['id']}: {habit['name']} "
        f"- {habit['description']} "
        f"({freq['times']}x {freq['type']})\n")
    return True

### Edit Habit ###

def edit_habit():
    data = load_habits()
    list_habits(data)
    logger.debug("User entered edit-habit menu.")

    if not data['habits']:
        print("No habits in list.")
        return

    habit = prompt_for_existing_habit(data, "Enter habit ID to edit (0 to go back): ")
    if habit is None:
        return

    try:
        habit["name"] = get_non_empty_string("New name: ")                              #input_handler.py checks for valid input
        habit["description"] = get_optional_string("New description (optional): ")      #input_handler.py checks for valid input
    except ValueError as e:
        print(e)
        logger.info("Invalid input while editing habit.")
        return

    save_habits(data)
    logger.info(f"Habit '{habit['name']}' updated.")                                    ### Logger INFO example
    logger.debug("User exited edit-habit menu.")
    return

### Delete Habit ###

def delete_habit():
    data = load_habits()
    list_habits(data)
    logger.debug("User entered delete-habit menu.")

    habit = prompt_for_existing_habit(data, "Enter habit ID to delete (0 to go back): ")
    if habit is None:
        logger.debug("User exited delete-habit menu.")
        return

    # Confirmation
    if confirm_action(f"Are you sure you want to delete '{habit['name']}'"):
        data["habits"].remove(habit)
        save_habits(data)
        logger.info(f"Habit '{habit['name']}' deleted.")
    else:
        logger.info(f"Deletion cancelled for habit '{habit['name']}'.")

### Mark Habit Done ###

def mark_habit_done_for_date(target_date=None):
    data = load_habits()
    list_habits(data)
    logger.debug("User entered mark-habit-done menu.")

    habit = prompt_for_existing_habit(
        data, "Enter habit ID to mark as done (0 to go back): "
    )
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

    
    
# ----- MAIN MENU LOOP ----- 

def main():
    logger.debug("Habit Tracker started")
    
    while True:
        print("\n Habit Tracker \n")
        print("1. Add habit")
        print("2. List habits")
        print("3. Edit habit")
        print("4. Delete habit")
        print("5. Mark habit done today")
        print("6. Mark habit done another day")
        print("7. Exit\n")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_habit()
        elif choice == "2":
            data = load_habits()
            list_habits(data)
        elif choice == "3":
            edit_habit()
        elif choice == "4":
            delete_habit()
        elif choice == "5":
            mark_habit_done_for_date(date.today().isoformat())
        elif choice == "6":
            mark_habit_done_for_date()
        elif choice == "7":
            print("Goodbye!")
            logger.debug("Habit Tracker stopped")
            break
        else:
            logger.info(f"Invalid menu choice: {choice}. Try again.")

def run():
    main()

if __name__ == "__main__":
    main()

