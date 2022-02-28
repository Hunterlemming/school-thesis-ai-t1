from typing import Dict, List, Optional
import pandas as pd
from model.day import DEFAULT_DAY_INTERVALS, DaySummary
from model.log import LogSummary
from model.task import Task

from services.log_parser import parse_default_csv
from utils.time_utils import get_overlapping_time


def create_csv_1(log: LogSummary) -> None:
    '''A1 productivity during the days'''
    rows: List[List[pd.Timestamp.date, int]] = []
    # Collecting data from each day, relevant to the actor
    actor0_days = []
    for day in log.days.values():
        actor0_days.append(day[log.actors[0]])
    # Creating dataframe for csv
    for day in actor0_days:
        rows.append([pd.to_datetime(day.date, format='%Y-%m-%d'), day.get_daily_product_per_hour_performance()])
    df = pd.DataFrame(rows, columns=['timestamp', 'num of activity performed'])
    df.set_index('timestamp', inplace=True)
    df.to_csv('./data/generated/gen_1.csv', sep=';')


def create_csv_2(log: LogSummary) -> None:
    '''A1 productivity with A2'''
    rows: List[List[pd.Timestamp.date, int, float]] = []
    demo_actor: str = log.actors[0]
    # Looping through days
    for day in log.days.values():
        actor_day_summary = day.get(demo_actor)
        if actor_day_summary is not None:
            # Getting productivity and worktime for that day
            actor_productivity = actor_day_summary.get_daily_product_per_hour_performance()
            actor_work_time = actor_day_summary.get_daily_hours_worked()
            # Getting worktimes of other actors that day
            other_worktimes: Dict[str, float] = {}
            for other_actor in log.actors:
                if other_actor != demo_actor:
                    other_day_summary = day.get(other_actor)
                    if other_day_summary is None:
                        other_worktimes[other_actor] = 0
                    else:
                        # Getting the section(s) where their worktimes overlap
                        other_worktimes[other_actor] = get_overlapping_time(actor_day_summary.tasks, other_day_summary.tasks)


if __name__ == "__main__":
    summary = parse_default_csv()
    # print(summary)
    create_csv_1(summary)
    # print(summary.get_day_by_date('2022-02-18'))
    tasks1 = summary.get_day_by_index(0).get('A1').tasks
    tasks2 = summary.get_day_by_index(0).get('A5').tasks
    overlaps = get_overlapping_time(tasks1, tasks2)
    print(overlaps)
    
    # wh = summary.get_same_date_days_with_index(0)
    # for day in wh:
    #     print(day)
