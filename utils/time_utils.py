from typing import List, Optional, Union

import pandas as pd

from model.task import Task


def later_of(t1: Union[str, pd.Timestamp.time], t2: Union[str, pd.Timestamp.time]) -> Union[str, pd.Timestamp.time]:
    '''Returns the time-string of the later time parameter.'''
    t1_date, t2_date = pd.to_datetime(str(t1)), pd.to_datetime(str(t2))
    return t1 if t1_date >= t2_date else t2

def earlier_of(t1: Union[str, pd.Timestamp.time], t2: Union[str, pd.Timestamp.time]) -> Union[str, pd.Timestamp.time]:
    '''Returns the time-string of the earlier time parameter.'''
    t1_date, t2_date = pd.to_datetime(str(t1)), pd.to_datetime(str(t2))
    return t1 if t1_date <= t2_date else t2

def equal_to(t1: Union[str, pd.Timestamp.time], t2: Union[str, pd.Timestamp.time]) -> bool:
    '''Returns whether the two datetimes are the same.'''
    t1_date, t2_date = pd.to_datetime(str(t1)), pd.to_datetime(str(t2))
    return t1_date == t2_date

def get_overlapping_time(main_tasks: List[Task], other_tasks: List[Task], overlapping_time: Optional[float] = 0) -> float:
    '''Returns the overlapping time (in seconds) between two lists of tasks.'''
    if main_tasks is None or other_tasks is None:
        return 0
    task_time_delta = Task._task_time_delta_in_seconds
    # Checking for overlaps
    new_tasks: List[Task] = []
    for m_task in main_tasks:
        for o_task in other_tasks:
            # The other is before the main
            if task_time_delta(o_task.end, m_task.start) >= 0:
                continue
            # The other is after the main
            if task_time_delta(m_task.end, o_task.start) >= 0:
                break
            # The other task overlaps the main
            end_point: pd.Timestamp.time = earlier_of(m_task.end, o_task.end)
            inner_overlap: float = task_time_delta(later_of(m_task.start, o_task.start), end_point)
            overlapping_time += inner_overlap
            # Adding a new task with the rest of the other's time
            if not equal_to(end_point, o_task.end):
                remaining_o_task = Task(o_task.activity, m_task.end, o_task.end)
                new_tasks.append(remaining_o_task)
    if len(new_tasks) == 0:
        return overlapping_time
    return get_overlapping_time(main_tasks, new_tasks, overlapping_time)