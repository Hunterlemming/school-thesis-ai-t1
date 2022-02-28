from typing import Dict, List
import pandas as pd

from model.day import DaySummary
from model.log import LogSummary
from model.task import Task


def get_or_create_day(days: Dict[str, Dict[str, DaySummary]], actor: str, date: pd.Timestamp.date) -> DaySummary:
    '''Returns the DaySummary with the given actor and date if it exists, otherwise creates a new one.'''
    date_str = str(date)
    new_summary = DaySummary(actor, date)
    if date_str in days.keys(): 
        if actor in days[date_str].keys():
            return days[date_str][actor]        # Returning already existing DaySummary
        days[date_str][actor] = new_summary
        return new_summary                      # Adding a new actor's DaySummary to a stored date_str
    days[date_str] = {actor: new_summary}
    return new_summary                          # Adding a brand new day, if necessary


def parse_default_csv() -> LogSummary:
    '''Parsing the thesis's default csv format.'''
    # Accessing csv
    input_csv = pd.read_csv('./data/raw_input.csv', sep=';', parse_dates=['Date-time'])
    # Initializing variables
    actors: List[str] = []
    activities: List[str] = [] 
    days: Dict[str, Dict[str, DaySummary]] = {}
    unfinished_tasks: Dict[str, Task] = {}
    # Iterating over the rows of the csv
    for index, row in input_csv.iterrows():
        task = None
        actor = row['actor']
        activity = row['activity']
        timestamp = row['Date-time']
        # Parsing the row
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
            # Adding a finished task to its DaySummary
            day = get_or_create_day(days, actor, timestamp.date())
            day.tasks.append(task)
    # Returning the parsed log
    return LogSummary(actors, activities, days)
