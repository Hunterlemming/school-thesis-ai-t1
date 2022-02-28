from typing import Dict, List
import pandas as pd
from model.day import DEFAULT_DAY_INTERVALS, DaySummary
from model.log import LogSummary

from services.log_parser import parse_default_csv
from utils.time_utils import get_overlapping_time_in_seconds


def create_csv_1(log: LogSummary, actor: str) -> None:
    '''Writes actor's productivity during the days into a csv.'''
    rows: List[List[pd.Timestamp.date, float]] = []
    # Collecting data from each day, relevant to the actor
    actor_summaries: List[DaySummary] = []
    for day_sum in log.days.values():
        actor_summaries.append(day_sum[actor])
    # Creating dataframe for csv
    for day_sum in actor_summaries:
        rows.append([pd.to_datetime(day_sum.date, format='%Y-%m-%d'), day_sum.get_daily_product_per_hour_performance()])
    # Creating the csv
    df = pd.DataFrame(rows, columns=['timestamp', 'num of activity performed'])
    df.set_index('timestamp', inplace=True)
    df.to_csv('./data/generated/gen_1.csv', sep=';')


def create_csv_2(log: LogSummary, actor_m: str, *actor_os: str) -> None:
    '''Writes actor's productivity along with common worktime percentages (with other actors) into a csv.'''
    rows: List[List[pd.Timestamp.date, int, float]] = []    # This is *float for actor_os number of arguments
    if len(actor_os) == 0:
        actor_os = tuple(log.actors)
    # Looping through days
    for day in log.days.values():
        main_summary = day.get(actor_m)
        if main_summary is None:
            continue
        # Getting productivity and worktime for that day
        m_actor_productivity = main_summary.get_daily_product_per_hour_performance()
        m_actor_work_time = main_summary.get_daily_worktime()
        # Getting worktimes of other actors that day
        common_worktime_percent: Dict[str, float] = {}
        for other_actor in actor_os:
            if other_actor == actor_m:
                continue
            # Getting the section(s) where their worktimes overlap
            other_summary = day.get(other_actor)
            if other_summary is None:
                common_worktime_percent[other_actor] = 0
            else:
                common_time_in_seconds = get_overlapping_time_in_seconds(main_summary.tasks, other_summary.tasks)
                common_worktime_percent[other_actor] = round((common_time_in_seconds / m_actor_work_time) * 100, 2)
        # Adding row to dataframe
        row = [pd.to_datetime(main_summary.date, format='%Y-%m-%d'), round(m_actor_productivity, 3),
            *list(common_worktime_percent.values())]
        rows.append(row)
    # Creating csv
    df = pd.DataFrame(rows, columns=['timestamp', 'productivity', *actor_os])
    df.set_index('timestamp', inplace=True)
    df.to_csv('./data/generated/gen_2.csv', sep=';')


if __name__ == "__main__":
    summary = parse_default_csv()
    # print(summary)
    # print(summary.get_day_by_date('2022-02-18'))
    create_csv_1(summary, 'A1')
    create_csv_2(summary, summary.actors[0], summary.actors[1], summary.actors[2])
