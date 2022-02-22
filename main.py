from typing import Dict, List, Optional
import pandas as pd


class Task:

    def __init__(self, activity: str, start: pd.Timestamp.time) -> None:
        self.activity: str = activity
        self.start: pd.Timestamp.time = start
        self.end: pd.Timestamp.time = None

    def end_task(self, end: pd.Timestamp.time):
        self.end = end

    def __str__(self) -> str:
        return f"Activity: {self.activity}| Start: {self.start}| End: {self.end}"


class Day:

    def __init__(self, actor: str, date: pd.Timestamp.date, tasks: Optional[List[Task]] = None) -> None:
        self.actor: str = actor
        self.date: pd.Timestamp.date = date
        self.tasks: List[Task] = tasks if tasks is not None else []

    def __str__(self) -> str:
        _str = [f"Actor: {self.actor}| Date: {self.date}| Tasks:"]
        for task in self.tasks:
            _str.append(f"\n\t{task}")
        return ''.join(_str)


def get_day(days: List[Day], actor: str, date: pd.Timestamp.date) -> Day:
    query_result = list(filter(lambda day: day.actor == actor and day.date == date, days))

    if len(query_result) == 0:
        day = Day(actor, date)
        days.append(day)
    else:
        day = query_result[0]
    
    return day


if __name__ == "__main__":
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
            day = get_day(days, row['actor'], row['Date-time'].date())
            day.tasks.append(task)

    for day in days:
        print(day)