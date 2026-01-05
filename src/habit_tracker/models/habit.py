# describes the structure of the Habit class 
    
class Habit:
    def __init__(self, id, name, description="", frequency_type="daily", frequency_times=1):
        self.id = id
        self.name = name
        self.description = description
        self.frequency = {
            "type": frequency_type,
            "times": frequency_times
        }
        self.completed_days = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "completed_days": self.completed_days
        }
