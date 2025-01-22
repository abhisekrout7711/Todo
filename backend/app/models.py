from enum import Enum

class TaskStatus(Enum):
    Pending = "Pending"
    Completed = "Completed"
    InProgress = "In Progress"
    Overdue = "Overdue"

class TaskPriority(Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"