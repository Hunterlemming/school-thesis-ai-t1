from typing import List, Optional
import pandas as pd

from model.task import Task


class Day:

    def __init__(self, actor: str, date: pd.Timestamp.date, tasks: Optional[List[Task]] = None) -> None:
        self.actor: str = actor
        self.date: pd.Timestamp.date = date
        self.tasks: List[Task] = tasks if tasks is not None else []

    def get_number_of_activities_performed(self):
        return len(self.tasks)

    def __str__(self) -> str:
        _str = [f"Actor: {self.actor}| Date: {self.date}| Tasks:"]
        for task in self.tasks:
            _str.append(f"\n\t{task}")
        return ''.join(_str)
