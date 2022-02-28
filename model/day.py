from typing import List, Optional, Tuple, Union
import pandas as pd

from model.task import Task
from utils.logger import log_warning
from utils.time_utils import earlier_of, later_of


DEFAULT_DAY_INTERVALS: List[Tuple[str, str]] = [('08:00', '10:00'), ('10:00', '12:00'), ('12:00', '14:00'), ('14:00', '16:00')]


class DaySummary:

    def __init__(self, actor: str, date: pd.Timestamp.date, tasks: Optional[List[Task]] = None) -> None:
        self.actor: str = actor
        self.date: pd.Timestamp.date = date
        self.tasks: List[Task] = tasks if tasks is not None else []


    def get_daily_all_number_of_products(self) -> int:
        '''Returns the daily number of products.'''
        return len(self.tasks)

    def get_daily_worktime(self, scale: str = 's', dec: int = 0) -> float:
        '''Returns the worktime this day. (default: seconds, 0 decimals)'''
        worktime: float = 0
        # Calculating the worktime in seconds
        for task in self.tasks:
            worktime += Task._task_time_delta_in_seconds(task.start, task.end)
        # Returning the worktime in preferred format
        if scale == 's':
            return worktime
        if scale == 'm':
            return round(worktime / 60, dec)
        if scale == 'h':
            return round(worktime / 3600, dec)

    def get_daily_product_per_hour_performance(self, dec: int = 3) -> float:
        '''Returns the average number of products created in a workhour. (default: 3 decimals)'''
        return round(self.get_daily_all_number_of_products() / self.get_daily_worktime('h',3), dec)


    def get_tasks_in_interval(
        self, int_start: Union[str, pd.Timestamp.time], int_end: Union[str, pd.Timestamp.time]) -> List[Task]:
        '''Returns the tasks in a certain timeframe.'''
        task_time_delta = Task._task_time_delta_in_seconds
        int_tasks: List[Task] = []
        for task in self.tasks:
            debug_pg: int = 0
            # If the task's start is later than the interval, break the loop!
            if task_time_delta(task.start, int_end) < 0:
                break
            # If the task's end is earlier than the interval, continue until we reach it!
            if task_time_delta(task.end, int_start) > 0:
                continue
            # Otherwise
            task_time_before_interval = task_time_delta(task.start, int_start)
            task_time_in_interval = task_time_delta(later_of(task.start, int_start), earlier_of(task.end, int_end))
            task_time_after_interval = task_time_delta(int_end, task.end)
            # If the task begins earlier but ends in the interval:
            if task_time_before_interval > 0:
                if task_time_in_interval >= task_time_before_interval:
                    int_tasks.append(task)
                    debug_pg += 1
            # If the task starts in the interval but ends later:
            if task_time_after_interval > 0:
                if task_time_in_interval > task_time_after_interval:
                    int_tasks.append(task)
                    debug_pg += 1
            # If the entire task is in the interval:
            if task_time_after_interval <= 0 and task_time_before_interval <= 0:
                    int_tasks.append(task)
                    debug_pg += 1
            # We log an error if we passed a too narrow interval (this might mess up the output)
            if debug_pg > 1:
                log_warning("INTERVAL TOO NARROW", f"Interval: {int_start}-{int_end}\n\
                    Day:\n\tActor{self.actor},\n\tDate:{self.date}\n\
                        Task:\n\t{task}")
        return int_tasks

    def get_multiple_interval_productivities(self, intervals: Optional[List[Tuple[str, str]]] = None) -> List[float]:
        '''Calculates the productivity in a list of intervals. (default: DEFAULT_DAY_INTERVALS)'''
        global DEFAULT_DAY_INTERVALS
        productivities: List[float] = []
        if intervals is None:
            intervals = DEFAULT_DAY_INTERVALS
        # Calculating individual interval productivities
        for interval in intervals:
            worktime_seconds: float = 0
            tasks_in_interval: List[Task] = self.get_tasks_in_interval(*interval)
            for task in tasks_in_interval:
                worktime_seconds += task.get_task_time_in_seconds()
            # Productivity = tasks done / worktime in hours
            productivities.append(len(tasks_in_interval) / (worktime_seconds / 3600) if worktime_seconds > 0 else 0)
        return productivities


    def __str__(self) -> str:
        _str = [f"Actor: {self.actor}| Date: {self.date}| Tasks:"]
        for task in self.tasks:
            _str.append(f"\n\t{task}")
        return ''.join(_str)
