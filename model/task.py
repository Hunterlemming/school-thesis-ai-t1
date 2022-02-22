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