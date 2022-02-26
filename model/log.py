from typing import Dict, List, Union

from model.day import DaySummary


class LogSummary:
    
    def __init__(self, actors: List[str], activities: List[str], days: Dict[str, Dict[str, DaySummary]]) -> None:
        self.actors: List[str] = actors
        self.activities: List[str] = activities
        self.days: Dict[str, Dict[str, DaySummary]] = days

    """
    LogSummary.days = {
        'day_date_str' : {
            'actor' : DaySummary
        }
    }
    """

    def get_day_by_index(self, index: int) -> Union[Dict[str, DaySummary], None]:
        if index < 0 or index > len(self.days.keys()):
            return None
        return self.days[list(self.days.keys())[index]]

    def get_day_by_date(self, date_str: str) -> Union[Dict[str, DaySummary], None]:
        if date_str not in self.days.keys():
            return None
        return self.days[date_str]


    def __str__(self) -> str:
        _str = [f"Actors: {', '.join([a for a in self.actors])}\n"]
        _str.append(f"Activities: {', '.join([a for a in self.activities])}\n")
        _str.append("Days:")
        for i, day in enumerate(self.days.values()):
            _str.append(f"\n{list(self.days.keys())[i]}")
            for summary in day.values():
                _str.append(f"\n{summary}")
        return ''.join(_str)
