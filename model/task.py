from typing import Optional, Union
import pandas as pd

from utils.logger import log_error


class Task:

    def __init__(self, activity: str, start: pd.Timestamp.time, end: Optional[pd.Timestamp.time] = None) -> None:
        self.activity: str = activity
        self.start: pd.Timestamp.time = start
        self.end: pd.Timestamp.time = end


    @staticmethod
    def _task_time_delta_in_seconds(start: Union[str, pd.Timestamp.time], end: Union[str, pd.Timestamp.time]) -> float:
        """
            Returns the difference between two timestamps in seconds.\n
            \tIf the **value > 0** the second event happened **after** the first.\n
            \tIf the **value < 0** the second event happened **before** the first.
        """
        start_date, end_date = pd.to_datetime(str(start)), pd.to_datetime(str(end))
        delta: pd.Timedelta = end_date - start_date
        # Adding the (passed days * number of seconds in a day) to the equation. If start < end 
        # it adds 0, otherwise we add -1 days to a positive amount of seconds to get the result.
        delta_seconds = delta.seconds + delta.days * 86400
        return delta_seconds


    def end_task(self, end: pd.Timestamp.time) -> None:
        self.end = end

    def get_task_time_in_seconds(self) -> float:
        if self.end is None:
            log_error("Time requested in an open task!", f"\tActivity:{self.activity}\n\tStart:{self.start}")
            return 0
        return Task._task_time_delta_in_seconds(self.start, self.end)


    def __str__(self) -> str:
        return f"Activity: {self.activity}| Start: {self.start}| End: {self.end}"
