from datetime import date
from colorama import Fore, Style, init

from habit_tracker.utils import logger
from habit_tracker.habit_crud import(add_habit, list_habits, edit_habit, delete_habit, mark_habit_done_for_date)
from habit_tracker.data_store import(load_habits)
from habit_tracker.utils.input_handler import(prompt_for_existing_habit)
from habit_tracker.analysis.statistics import(print_block_legend, show_habit_details, show_overview, show_current_streaks, show_best_streaks, show_weekly_summary)

# =========================
# Formatting helpers (UI)
# =========================

init(autoreset=True)

def title(text):
    print(Fore.CYAN + "\n" + "   " + ("-" * 20) + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.CYAN + f"   {text}" + Style.RESET_ALL)
    print(Fore.CYAN + "   " + ("-" * 20) + "\n" + Style.RESET_ALL)

def smalltitle(text):
    print(Fore.GREEN + "\n" + "   " + ("-" * 20) + Style.RESET_ALL)
    print(f"   {Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print(Fore.GREEN + "   " + ("-" * 20) + "\n" + Style.RESET_ALL)

def smallertitle(text):
    print(Fore.MAGENTA + "\n" + "   " + ("-" * 20) + Style.RESET_ALL)
    print(f"   {Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print(Fore.MAGENTA + "   " + ("-" * 20) + "\n" + Style.RESET_ALL)

def option(key, text):
    print(f"  {Fore.CYAN}{key}.{Style.RESET_ALL} {text}")

def prompt(text="\n   Choose an option: "):
    return input(f"  {Fore.BLUE}{text}{Style.RESET_ALL}").strip()


# =========================
# MAIN MENU
# =========================

def main():
    logger.debug("Habit Tracker started")
    
    while True:
        title("Habit Tracker")

        option("1", "Manage habits")
        option("2", "Track habits")
        option("3", "View Statistics")
        print("   " + ("-" * 20) + "\n")
        option("0", "Exit\n")
    
        choice = prompt()

        if choice == "1":
            manage_habits_menu()
        elif choice == "2":
            track_habits_menu()
        elif choice == "3":
            stats_menu()
        elif choice == "0":
            title("Goodbye!")
            logger.debug("Habit Tracker stopped")
            break
        else:
            logger.info(f"\nInvalid menu choice: {choice}. Try again.")

# =========================
# MANAGEMENT MENU
# =========================

def manage_habits_menu():
    while True:
        smalltitle("Manage Habits Menu")

        option("1", "List habits")
        option("2", "Add habit")
        option("3", "Edit habit")
        option("4", "Delete habit")
        print("   " + ("-" * 20) + "\n")
        option("0", "Back")

        choice = prompt()

        if choice == "1":
            data = load_habits()
            list_habits(data)
        elif choice == "2":
            add_habit()
        elif choice == "3":
            edit_habit()
        elif choice == "4":
            delete_habit()
        elif choice == "0":
            return
        else:
            logger.info(f"Invalid menu choice: {choice}. Try again.")

# =========================
# TRACKING MENU
# =========================

def track_habits_menu():
    while True:
        smalltitle("Track Habits Menu")

        option("1", "Mark habit done today")
        option("2", "Mark habit done another day")
        print("   " + ("-" * 20) + "\n")
        option("0", "Back")

        choice = prompt()

        if choice == "1":
            mark_habit_done_for_date(date.today().isoformat())
        elif choice == "2":
            mark_habit_done_for_date()
        elif choice == "0":
            return
        else:
            logger.info(f"Invalid menu choice: {choice}. Try again.")

# =========================
# STATISTICS MENU
# =========================

def stats_menu():
    while True:
        smalltitle("Habit Statistics")

        option("1", "Overview")
        option("2", "Habit Details")
        option("3", "Streaks")
        option("4", "Weekly Summary")
        option("5", "Full report (graphs)")
        print("   " + ("-" * 20) + "\n")
        option("0", "Back")

        choice = prompt()
        data = load_habits()

        if choice == "0":
            return

        if not data["habits"]:
            print("   No habits found.")
            continue

        elif choice == "1":
            title("Overview")
            show_overview(data)
            input("\n   Press Enter to continue...")

        elif choice == "2":
            title("Habit Details")
            show_habit_details_menu(data)

        elif choice == "3":
            smalltitle("Streaks")

            smallertitle("Current Streaks")
            show_current_streaks(data)

            smallertitle("Best Streaks")
            show_best_streaks(data)

            input("\n   Press Enter to continue...")
        
        elif choice == "4":
            title("Weekly Summary")
            show_weekly_summary(data)
            input("\n   Press Enter to continue...")

        elif choice == "5":
            title("Coming soon!")  # matplotlib / PDF later

        else:
            logger.info(f"Invalid menu choice: {choice}. Try again.")

# ----- Statistics Sub-Menu

def show_habit_details_menu(data):
    list_habits(data)
    print("   Choose a habit to view detailed progress.\n")
    habit = prompt_for_existing_habit(data, "   Enter habit ID (0 to go back): ")
    if not habit:
        return

    show_habit_details(habit)


def run():
    main()

if __name__ == "__main__":
    main()

