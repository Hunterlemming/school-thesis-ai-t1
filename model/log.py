from typing import Callable, Dict, List, Union

import pandas as pd

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


    def _filter_for_same_date_days(self, param_date: pd.Timestamp) -> List[DaySummary]:
        '''The core loop of both get_same_date_days functions I didn't want to duplicate.'''
        filtered_days: List[DaySummary] = []
        for day in self.days:
            current_dt = pd.to_datetime(str(day.date))
            if param_date == current_dt:
                filtered_days.append(day)
            if param_date < current_dt:
                break
        return filtered_days

    def get_same_date_days_with_date(self, date: Union[pd.Timestamp.date, str]) -> List[DaySummary]:
        '''Returns all the Day-s of all actors, who worked on the parameter date.'''
        param_dt = pd.to_datetime(str(date))
        same_date_days: List[DaySummary] = self._filter_for_same_date_days(param_dt)
        return same_date_days

    def get_same_date_days_with_index(self, index: int) -> List[DaySummary]:
        '''Same as get_same_date_days(), but instead of passing a date we pass a day index.'''
        if index > len(self.days) - 1:
            return []
        param_dt = pd.to_datetime(str(self.days[index].date))
        same_date_days: List[DaySummary] = self._filter_for_same_date_days(param_dt)
        return same_date_days

    def get_all_same_date_days(self):
        #TODO: This, you will probably need to refactor the class 2, to prevent double loop!
        pass


    def __str__(self) -> str:
        _str = [f"Actors: {', '.join([a for a in self.actors])}\n"]
        _str.append(f"Activities: {', '.join([a for a in self.activities])}\n")
        _str.append("Days:")
        for i, day in enumerate(self.days.values()):
            _str.append(f"\n{list(self.days.keys())[i]}")
            for summary in day.values():
                _str.append(f"\n{summary}")
        return ''.join(_str)
