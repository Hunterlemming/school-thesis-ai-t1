from typing import Dict, List
import pandas as pd

from model.day import Day
from model.log import LogSummary
from model.task import Task


def get_or_create_day(days: List[Day], actor: str, date: pd.Timestamp.date) -> Day:
    query_result = list(filter(lambda day: day.actor == actor and day.date == date, days))

    if len(query_result) == 0:
        day = Day(actor, date)
        days.append(day)
    else:
        day = query_result[0]
    
    return day


def parse_default_csv() -> LogSummary:
    input_csv = pd.read_csv('./data/raw_input.csv', sep=';', parse_dates=['Date-time'])
    
    actors: List[str] = []
    activities: List[str] = [] 
    days: List[Day] = []

    unfinished_tasks: Dict[str, Task] = {}

    for index, row in input_csv.iterrows():
        task = None
        
        actor = row['actor']
        activity = row['activity']
        timestamp = row['Date-time']

        if row['state'] == "start":
            # Starting a new task (unfinished)
            unfinished_tasks[actor] = Task(activity, timestamp.time())
        elif row['state'] == "end":
            # Finishing unfinished task
            task = unfinished_tasks[actor]
            task.end_task(timestamp.time())
            # Adding the actor and the activity to the log-summary
            if actor not in actors:
                actors.append(actor)
            if activity not in activities:
                activities.append(activity)
            # Removing task from the unfinished tasks
            unfinished_tasks.pop(actor)
        if task is not None:
            # Adding a finished task to its day
            day = get_or_create_day(days, actor, timestamp.date())
            day.tasks.append(task)

    return LogSummary(actors, activities, days)
