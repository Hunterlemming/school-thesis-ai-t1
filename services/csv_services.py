from typing import Dict, List
import pandas as pd

from model.day import Day
from model.task import Task


def get_or_create_day(days: List[Day], actor: str, date: pd.Timestamp.date) -> Day:
    query_result = list(filter(lambda day: day.actor == actor and day.date == date, days))

    if len(query_result) == 0:
        day = Day(actor, date)
        days.append(day)
    else:
        day = query_result[0]
    
    return day


def parse_default_csv_to_days() -> List[Day]:
    input_csv = pd.read_csv('./data/raw_input.csv', sep=';', parse_dates=['Date-time'])
    
    days: List[Day] = []
    unfinished_tasks: Dict[str, Task] = {}

    for index, row in input_csv.iterrows():
        task = None
        if row['state'] == "start":
            unfinished_tasks[row['actor']] = Task(row['activity'], row['Date-time'].time())
        elif row['state'] == "end":
            task = unfinished_tasks[row['actor']]
            task.end_task(row['Date-time'].time())
            unfinished_tasks.pop(row['actor'])
        if task is not None:
            day = get_or_create_day(days, row['actor'], row['Date-time'].date())
            day.tasks.append(task)

    return days