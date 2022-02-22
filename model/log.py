from typing import List

from model.day import Day


class LogSummary:
    
    def __init__(self, actors: List[str], activities: List[str], days: List[Day]) -> None:
        self.actors: List[str] = actors
        self.activities: List[str] = activities
        self.days: List[Day] = days

    def __str__(self) -> str:
        _str = [f"Actors: {', '.join([a for a in self.actors])}\n"]
        _str.append(f"Activities: {', '.join([a for a in self.activities])}\n")
        _str.append("Days:")
        for day in self.days:
            _str.append(f"\n{day}")
        return ''.join(_str)
