from enum import Enum


class Status(str, Enum):
    completed = "completed"
    in_progress = "in_progress"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    information = "information"