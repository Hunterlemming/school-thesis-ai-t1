from typing import Union
import pandas as pd


class Task:

    def __init__(self, activity: str, start: pd.Timestamp.time) -> None:
        self.activity: str = activity
        self.start: pd.Timestamp.time = start
        self.end: pd.Timestamp.time = None


    @staticmethod
    def _task_time_delta_in_seconds(start: Union[str, pd.Timestamp.time], end: Union[str, pd.Timestamp.time]) -> float:
        """
            Returns the difference between two timestamps in seconds.\n
            \tIf the **value > 0** the second event happened **after** the first.\n
            \tIf the **value < 0** the second event happened **before** the first.
        """
        delta: pd.Timedelta = pd.to_datetime(str(end)) - pd.to_datetime(str(start))
        return delta.seconds


    def end_task(self, end: pd.Timestamp.time):
        self.end = end


    def __str__(self) -> str:
        return f"Activity: {self.activity}| Start: {self.start}| End: {self.end}"
