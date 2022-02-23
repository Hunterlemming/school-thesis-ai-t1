from typing import List, Optional, Tuple
import pandas as pd

from model.task import Task


DAY_INTERVALS: List[Tuple[str, str]] = [('08:00', '10:00'), ('10:00', '12:00'), ('12:00', '14:00'), ('14:00', '16:00')]


class Day:

    def __init__(self, actor: str, date: pd.Timestamp.date, tasks: Optional[List[Task]] = None) -> None:
        self.actor: str = actor
        self.date: pd.Timestamp.date = date
        self.tasks: List[Task] = tasks if tasks is not None else []


    def get_daily_all_number_of_products(self) -> int:
        '''Returns the daily number of products.'''
        return len(self.tasks)

    def get_daily_hours_worked(self) -> float:
        '''Returns the amount of hours worked this day (with 3 decimals).'''
        worktime: float = 0
        # Calculating the worktime in seconds
        for task in self.tasks:
            tasktime: pd.Timedelta = pd.to_datetime(str(task.end)) - pd.to_datetime(str(task.start))
            worktime += tasktime.seconds
        # Returning the worktime in hours (3 decimals)
        return round(worktime / 3600, 3)

    def get_daily_product_per_hour_performance(self) -> float:
        '''Returns the average number of products created in a workhour'''
        return self.get_daily_all_number_of_products() / self.get_daily_hours_worked()


    def get_interval_productivity(self, start: str, end: str) -> float:
        # TODO: this
        worktime: float = 0
        products: int = 0
        for task in self.tasks:
            pass

    def get_worktime_in_intervals(self) -> List[float]:
        pass

    def __str__(self) -> str:
        _str = [f"Actor: {self.actor}| Date: {self.date}| Tasks:"]
        for task in self.tasks:
            _str.append(f"\n\t{task}")
        return ''.join(_str)
