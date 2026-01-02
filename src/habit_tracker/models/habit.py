# describes the structure of the Habit class 

class Habit:
    def __init__(self, habit_id, name, description=""): 
        self.id = habit_id
        self.name = name
        self.description = description
        self.completed_days = []

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "completed_days": self.completed_days,
        }