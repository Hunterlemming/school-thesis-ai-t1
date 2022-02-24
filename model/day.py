from typing import List, Optional, Tuple, Union
import pandas as pd

from model.task import Task
from utils.logger import log_warning


DEFAULT_DAY_INTERVALS: List[Tuple[str, str]] = [('08:00', '10:00'), ('10:00', '12:00'), ('12:00', '14:00'), ('14:00', '16:00')]


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
            worktime += Task._task_time_delta_in_seconds(task.start, task.end)
        # Returning the worktime in hours (3 decimals)
        return round(worktime / 3600, 3)

    def get_daily_product_per_hour_performance(self) -> float:
        '''Returns the average number of products created in a workhour.'''
        return self.get_daily_all_number_of_products() / self.get_daily_hours_worked()


    def get_single_interval_productivity(
        self, int_start: Union[str, pd.Timestamp.time], int_end: Union[str, pd.Timestamp.time]) -> float:
        '''Returns the created number of products divided by their summed up worktime in a certain timeframe.'''
        worktime: float = 0
        products: int = 0
        for task in self.tasks:
            debug_pg: int = 0
            # If the task's start is later than the interval, break the loop!
            if Task._task_time_delta_in_seconds(task.start, int_end) < 0:
                break
            # If the task's end is earlier than the interval, continue until we reach it!
            if Task._task_time_delta_in_seconds(task.end, int_start) > 0:
                continue
            # Otherwise
            task_time_full = Task._task_time_delta_in_seconds(task.start, task.end)
            task_time_before_interval = Task._task_time_delta_in_seconds(task.start, int_start)
            task_time_in_interval = Task._task_time_delta_in_seconds(max(task.start, int_start), min(task.end, int_end))
            task_time_after_interval = Task._task_time_delta_in_seconds(int_end, task.end)
            # If the task begins earlier but ends in the interval:
            if task_time_before_interval > 0:
                if task_time_in_interval >= task_time_before_interval:
                    worktime += task_time_full
                    products += 1
                    debug_pg += 1
            # If the task starts in the interval but ends later:
            if task_time_after_interval > 0:
                if task_time_in_interval > task_time_after_interval:
                    worktime += task_time_full
                    products += 1
                    debug_pg += 1
            # If the entire task is in the interval:
            if task_time_after_interval <= 0 and task_time_before_interval <= 0:
                    worktime += task_time_full
                    products += 1
                    debug_pg += 1
            # We log an error if we passed a too narrow interval (this might mess up the output)
            if debug_pg > 1:
                log_warning(f"WARNING: INTERVAL TOO NARROW\nInterval: {int_start}-{int_end}\n\
                    Day:\n\tActor{self.actor},\n\tDate:{self.date}\n\
                        Task:\n\t{task}")
        # TODO: Somehow we do not calculate worktime. Need to debug!!!
        return products / worktime

    def get_multiple_interval_productivities(self, intervals: Optional[List[Tuple[str, str]]] = None) -> List[float]:
        '''Using the single_interval_productivity function on a list of intervals (default: DEFAULT_DAY_INTERVALS).'''
        global DEFAULT_DAY_INTERVALS
        productivities: List[float] = []
        if intervals is None:
            intervals = DEFAULT_DAY_INTERVALS
        # Calculating individual interval productivities
        for interval in intervals:
            prod = self.get_single_interval_productivity(*interval)
            productivities.append(prod)
        return productivities


    def __str__(self) -> str:
        _str = [f"Actor: {self.actor}| Date: {self.date}| Tasks:"]
        for task in self.tasks:
            _str.append(f"\n\t{task}")
        return ''.join(_str)
