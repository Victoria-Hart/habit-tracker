import json
from config import DATA_PATH
from models.habit import Habit
from utils.input_handler import(get_non_empty_string, get_optional_string, get_int)

# ----- JSON helpers ----- 

def load_habits():
    if not DATA_PATH.exists():
        return {"habits": []}
    
    with open(DATA_PATH, "r", encoding="UTF-8") as f:
        return json.load(f)

def save_habits(habits):
    with open(DATA_PATH, "w", encoding="UTF-8") as f:
        json.dump(habits, f, indent=2)

# ----- Features ----- 

### Generate new id ###

def get_new_id(habits):
    if not habits:
        return 1
    return max(h["id"] for h in habits) + 1

### Add a Habit ###

def add_habit():
    data = load_habits()
    new_id = get_new_id(data["habits"])

    try:
        name = get_non_empty_string("Habit name: ") #input_handler.py checks for valid input
        description = get_optional_string("Description (optional): ") #input_handler.py checks for valid input
    except ValueError as e:
        print(e)
        return

    new_habit = Habit(new_id, name, description)
    data["habits"].append(new_habit.to_dict())
    save_habits(data)

    print(f"Habit '{name}' added successfully!")

### List Habits ###

def list_habits(data):
    if not data["habits"]:
        print("No habits found.")
        return False
    
    print("\nYour habits:\n")
    print("(Unique ID: Habit Name - Description) \n")
    for habit in data["habits"]:
        print(f"{habit["id"]}: {habit["name"]} - {habit["description"]}\n")

### Edit Habit ###

def edit_habit():
    data = load_habits()
    list_habits(data)
    
    while True:
        try:
            habit_id = get_int("Enter habit ID to edit (0 to go back): ") #input_handler.py checks for valid input
        except ValueError as e:
            print(e)
            continue

        if habit_id == 0:
                return
        
        habit = next(
            (h for h in data["habits"] if int(h["id"]) == habit_id),
            None)
        
        if habit is None:
            print("Habit not found. Try again.")
            continue

        try:
            habit["name"] = get_non_empty_string("New name: ") #input_handler.py checks for valid input
            habit["description"] = get_optional_string("New description (optional): ") #input_handler.py checks for valid input
        except  ValueError as e:
                    print(e)
                    continue
                
        save_habits(data)
        print("Habit updated.")
        return
    
### Delete Habit ###

def delete_habit():
    data = load_habits()
    list_habits(data)

    while True:
        try:
            habit_id = get_int("Enter habit ID to delete (0 to go back): ") #input_handler.py checks for valid input
        except ValueError as e:
            print(e)
            continue  # ask again

        if habit_id == 0:
                return

        # Find habit
        habit = next(
            (h for h in data["habits"] if int(h["id"]) == habit_id),
            None
        )

        if habit is None:
            print("Habit not found. Try again.")
            continue  # ask again

        # Confirmation
        confirm = input(
            f"Are you sure you want to delete '{habit['name']}'? (YES/NO): "
        ).strip().upper()

        if confirm == "NO":
            print("Deletion cancelled.")
            return  # back to menu

        if confirm == "YES":
            data["habits"].remove(habit)
            save_habits(data)
            print(f"Habit {habit['name']} deleted.")
            return  # back to menu

        print("Please type YES or NO.")


# ----- MAIN MENU LOOP ----- 

def main():
    while True:
        print("\n Habit Tracker \n")
        print("1. Add habit")
        print("2. List habits")
        print("3. Edit habit")
        print("4. Delete habit")
        print("5. Exit\n")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

