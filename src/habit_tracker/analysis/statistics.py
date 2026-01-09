from datetime import date, timedelta
from colorama import Fore, Style
from collections import Counter
from calendar import month_name, monthcalendar

from habit_tracker.habit_crud import list_habits
from habit_tracker.utils.input_handler import prompt_for_existing_habit


# =========================
# OVERVIEW
# =========================

def show_overview(data):
    stats = overview(data)

    print(f"   Total habits: {stats['total_habits']}")
    print(f"   Total completions: {stats['total_completions']}")

    if stats["most_completed_habit"]:
        print(f"   Most completed habit: {stats['most_completed_habit']}")
        print(f"   Least completed habit: {stats['least_completed_habit']}")

def overview(data):
    habits = data["habits"]

    total_habits = len(habits)
    total_completions = sum(len(h["completed_days"]) for h in habits)

    if not habits:
        return{
            "total_habits": 0,
            "total_completions": 0,
            "most_completed_habit": None,
            "least_completed_habit": None,
        }
    
    sorted_habits = sorted(habits, key=lambda h: len(h["completed_days"]))

    return {
        "total_habits": total_habits,
        "total_completions": total_completions,
        "most_completed_habit": sorted_habits[-1]["name"],
        "least_completed_habit": sorted_habits[0]["name"],
    }

# =========================
# STREAKS
# =========================

def show_current_streaks(data):
    for habit in data["habits"]:
        streak = current_streak(habit)
        label = streak_label(habit, streak)
        print(f"   {habit['name']}: {label}")

def current_streak(habit):
    if habit["frequency"]["type"] == "daily":
        return daily_streak(habit)
    elif habit["frequency"]["type"] == "weekly":
        return weekly_streak(habit)
    elif habit["frequency"]["type"] == "monthly":
        return monthly_streak(habit)

def daily_streak(habit):
    times_required = habit["frequency"]["times"]

    if not habit["completed_days"]:
        return 0

    counts = Counter(date.fromisoformat(d) for d in habit["completed_days"])

    current = max(counts)   # ← start from last completed day
    streak = 0

    while counts.get(current, 0) >= times_required:
        streak += 1
        current -= timedelta(days=1)

    return streak

def weekly_streak(habit):
    times_required = habit["frequency"]["times"]

    if not habit["completed_days"]:
        return 0

    weeks = Counter(
        date.fromisoformat(d).isocalendar()[:2]
        for d in habit["completed_days"]
    )

    current_year, current_week = max(weeks)
    streak = 0

    while weeks.get((current_year, current_week), 0) >= times_required:
        streak += 1
        current_week -= 1

        if current_week == 0:
            current_year -= 1
            current_week = date(current_year, 12, 28).isocalendar()[1]

    return streak

def monthly_streak(habit):
    times_required = habit["frequency"]["times"]

    if not habit["completed_days"]:
        return 0

    months = Counter(
        (date.fromisoformat(d).year, date.fromisoformat(d).month)
        for d in habit["completed_days"]
    )

    year, month = max(months)
    streak = 0

    while months.get((year, month), 0) >= times_required:
        streak += 1
        month -= 1

        if month == 0:
            month = 12
            year -= 1

    return streak

def streak_label(habit, streak):
    freq = habit["frequency"]

    unit = {
        "daily": "day",
        "weekly": "week",
        "monthly": "month"
    }[freq["type"]]

    plural = "" if streak == 1 else "s"

    return f"{streak} {unit}{plural} ({freq['times']}x {freq['type']})"

def best_streak(habit):
    #convert iso strings to date objects in chronological order
    dates = sorted(date.fromisoformat(d) for d in habit["completed_days"])
    if not dates:
        return 0
    
    best = 1
    current = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):        # check if day is the day before
            current += 1
            best = max(best, current)
        else:
            current = 1                                         # streak breaks

    return best

# ----- Best Streaks

def show_best_streaks(data):
    for habit in data["habits"]:
        best = best_streak(habit)
        label = streak_label(habit, best)
        print(f"   {habit['name']}: {label}")

def best_streak(habit):
    freq_type = habit["frequency"]["type"]

    if freq_type == "daily":
        return best_daily_streak(habit)
    elif freq_type == "weekly":
        return best_weekly_streak(habit)
    elif freq_type == "monthly":
        return best_monthly_streak(habit)
    
def best_daily_streak(habit):
    times_required = habit["frequency"]["times"]

    if not habit["completed_days"]:
        return 0

    counts = Counter(date.fromisoformat(d) for d in habit["completed_days"])

    valid_days = sorted(
        day for day, count in counts.items()
        if count >= times_required
    )

    best = current = 1

    for i in range(1, len(valid_days)):
        if valid_days[i] == valid_days[i - 1] + timedelta(days=1):
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best

def best_weekly_streak(habit):
    times_required = habit["frequency"]["times"]

    weeks = Counter(
        date.fromisoformat(d).isocalendar()[:2]
        for d in habit["completed_days"]
    )

    valid_weeks = sorted(
        (year, week) for (year, week), count in weeks.items()
        if count >= times_required
    )

    best = current = 1

    for i in range(1, len(valid_weeks)):
        y1, w1 = valid_weeks[i - 1]
        y2, w2 = valid_weeks[i]

        # handle ISO week rollover
        if (y2, w2) == next_week(y1, w1):
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best

def best_monthly_streak(habit):
    times_required = habit["frequency"]["times"]

    months = Counter(
        (date.fromisoformat(d).year, date.fromisoformat(d).month)
        for d in habit["completed_days"]
    )

    valid_months = sorted(
        (y, m) for (y, m), count in months.items()
        if count >= times_required
    )

    best = current = 1

    for i in range(1, len(valid_months)):
        y1, m1 = valid_months[i - 1]
        y2, m2 = valid_months[i]

        if (y2, m2) == next_month(y1, m1):
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best

# =========================
# HELPERS
# =========================

def next_week(year, week):
    if week < date(year, 12, 28).isocalendar()[1]:
        return year, week + 1
    return year + 1, 1


def next_month(year, month):
    if month < 12:
        return year, month + 1
    return year + 1, 1


# =========================
# WEEKLY SUMMARY
# =========================

def weekly_summary(data):
    habits = [h["name"] for h in data["habits"]]
    summary = {}

    # First pass: find all weeks
    for habit in data["habits"]:
        for d in habit["completed_days"]:
            dt = date.fromisoformat(d)
            year, week, _ = dt.isocalendar()
            week_key = f"{year}-W{week:02d}"

            if week_key not in summary:
                summary[week_key] = {name: 0 for name in habits}

            summary[week_key][habit["name"]] += 1

    return summary


def show_weekly_summary(data):
    summary = weekly_summary(data)

    print("   Shows only weeks with activity. Weeks start on Monday.\n")

    if not summary:
        print("   No data yet.")
        return

    for week, habits in sorted(summary.items()):
        print(f"\n   {week}")
        for habit, count in habits.items():
            print(f"     • {habit}: {count}")


# =========================
# HABIT DETAILS
# =========================

BLOCK_FILLED = "█"
BLOCK_EMPTY = "░"

def render_day_block(day, habit, today, start):
    completed_days = {date.fromisoformat(d) for d in habit["completed_days"]}

    # OUTSIDE SELECTED RANGE
    if day < start:
        return Fore.LIGHTBLACK_EX + "░" + Style.RESET_ALL           

    # FUTURE
    if day > today:
        return Fore.LIGHTBLACK_EX + "░" + Style.RESET_ALL           

    # TODAY
    if day == today:
        return Fore.YELLOW + "█" + Style.RESET_ALL                  

    # DONE
    if day in completed_days:
        return Fore.GREEN + "█" + Style.RESET_ALL                   

    # MISSED (in range, past, not completed)
    return Fore.RED + "░" + Style.RESET_ALL


def habit_blocks(habit, months=3):
    today = date.today()
    completed_days = {
        date.fromisoformat(d) for d in habit["completed_days"]
    }

    # figure out which months to show
    shown_months = []
    y, m = today.year, today.month
    for _ in range(months):
        shown_months.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1

    shown_months.reverse()  # oldest → newest

    for year, month in shown_months:
        print(f"\n   {month_name[month]} {year}")
        print("   M T W T F S S")

        cal = monthcalendar(year, month)

        for week in cal:
            row = []
            for day in week:
                if day == 0:
                    row.append(Fore.LIGHTBLACK_EX + "░" + Style.RESET_ALL)
                else:
                    d = date(year, month, day)

                    if d > today:
                        row.append(Fore.LIGHTBLACK_EX + "░" + Style.RESET_ALL)
                    elif d == today:
                        row.append(Fore.YELLOW + "█" + Style.RESET_ALL)
                    elif d in completed_days:
                        row.append(Fore.GREEN + "█" + Style.RESET_ALL)
                    else:
                        row.append(Fore.RED + "█" + Style.RESET_ALL)

            print("   " + " ".join(row))


def print_block_legend():
    print(f"   Legend: {Fore.GREEN}█{Style.RESET_ALL} completed   {Fore.RED}█{Style.RESET_ALL} missed   {Fore.YELLOW}█{Style.RESET_ALL} today\n")


def show_habit_details(habit):
    print(f"\n   {Style.BRIGHT}{Fore.CYAN}{habit['name']}{Style.RESET_ALL}")
    freq = habit["frequency"]
    print(f"   {Style.BRIGHT}{Fore.CYAN}Frequency: {freq['times']}x {freq['type']}{Style.RESET_ALL}")

    while True:
        print(f"\n   {Fore.CYAN}Show:{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}1{Style.RESET_ALL}. Last month")
        print(f"   {Fore.CYAN}2{Style.RESET_ALL}. Last 2 months")
        print(f"   {Fore.CYAN}3{Style.RESET_ALL}. Last 3 months")
        print("   " + ("-" * 20) + "\n")
        print(f"   {Fore.CYAN}0{Style.RESET_ALL}. Back\n")

        choice = input(f"   {Fore.CYAN}Choose:{Style.RESET_ALL} ").strip()

        if choice == "1":
            print_block_legend()
            habit_blocks(habit, months=1)
            input("\n   Press Enter to continue...")
        elif choice == "2":
            print_block_legend()
            habit_blocks(habit, months=2)
            input("\n   Press Enter to continue...")
        elif choice == "3":
            print_block_legend()
            habit_blocks(habit, months=3)
            input("\n   Press Enter to continue...")
        elif choice == "0":
            return
        else:
            print("   Invalid choice.")



# =========================
# REPORTS?
# =========================

