import json
from habit_tracker.config import DATA_PATH
from habit_tracker.utils import logger

# Data access and persistence layer. #

# ----- JSON / Data helpers ----- 

def load_habits():
    if not DATA_PATH.exists():
        logger.warning("Habits file not found. Creating new file.")

        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        initial_data = {"next_id": 1, "habits": []}
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2)

        return initial_data
    
    try:
        if DATA_PATH.stat().st_size == 0:
            logger.warning("Habits file is empty. Reinitializing.")

            initial_data = {"next_id": 1, "habits": []}
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

            return initial_data

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            logger.debug(f"Loaded habits data: {json_data}")

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
        # Ensure data directory exists
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        logger.debug(f"Saving habits to {DATA_PATH}")
        logger.debug(f"Data to save: {data}")

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info("Habits saved successfully.")

    except Exception as e:
        logger.error(f"Failed to save habits: {e}")
        raise

# ----- ID Management -----

def get_new_id(data):
    new_id = data["next_id"]
    data["next_id"] += 1
    return new_id

# ----- Lookup Helper -----

def find_habit_by_id(data, habit_id):
    """Return habit dictionary with matching ID if found, or None if it doesn't exist."""
    for habit in data['habits']:
        if habit['id'] == habit_id:
            return habit
    return None