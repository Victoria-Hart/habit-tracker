# Habit Tracker

A command-line Habit Tracker written in Python.
The program allows users to create habits, track completions, and view statistics such as streaks, weekly summaries, and visual calendar-style progress directly in the terminal.

Habits can be tracked daily, weekly, or monthly with configurable frequency (e.g. 3x weekly, 1x monthly).
All data is stored locally in a JSON file.

The project focuses on clear project structure, modular code, version control, and use of a virtual environment.

---

## Features

* Add, edit, list, and delete habits
* Track habit completions by date
* Daily, weekly, and monthly habits with frequency requirements
* Statistics:

  * Overview
  * Current and best streaks
  * Weekly summaries
  * Visual habit details using block-based calendars

---

## Requirements

* Python 3.x
* colorama

(All dependencies are listed in `requirements.txt`)

---

## Installation and running the project

1. Clone the repository
2. Navigate to the project folder
3. Create and activate a virtual environment
4. Install dependencies:
   pip install -r requirements.txt  
5. Run the program:
   habit-tracker

## Demo data (optional)

The file `data/habits_demo.json` contains example habits and completion data
used to demonstrate the statistics and visualization features.

To use it, replace `data/habits.json` with `data/habits_demo.json` in `config.py` before running
the program.

## Assignment Mapping (Pythonprojekt)

**Projektstruktur**

* Flera paket:
  `habit_tracker/`, `models/`, `utils/`, `analysis/`
* Minst 5 moduler, t.ex.:
  `main.py`, `config.py`, `habit_crud.py`, `statistics.py`, `data_store.py`, `logger.py`

**Funktionella krav**

* Läsa data: `data_store.py`
* Bearbeta data: `analysis/statistics.py`
* Skriva ut resultat: `main.py`, `analysis/statistics.py`
* Klass: `Habit` i `models/habit.py`
* Funktioner i separata moduler
* Config-fil för pathing: `config.py`
* Custom logger: `utils/logger.py`
* Säker input-hantering: `utils/input_handler.py`

**Versionshantering**

* Git och feature-branches används

**Miljö och beroenden**

* Virtuell miljö (`venv`)
* Beroenden listade i `requirements.txt`
