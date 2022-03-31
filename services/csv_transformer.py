from typing import Dict, List, Optional, Tuple
import pandas as pd
from model.day import DEFAULT_DAY_INTERVALS, DaySummary
from model.log import LogSummary

from utils.time_utils import get_overlapping_time_in_seconds


def create_type_1_csv(log: LogSummary, actor: str, daily: bool, 
    intervals: Optional[List[Tuple[str, str]]] = None, file_name: str = 'gen_1.csv') -> None:
    '''Writes actor's productivity and activity in the given timeframes during the days into a csv.'''
    rows: List[List[pd.Timestamp.date, float]] = []     # This is *float for len(intervals) number of arguments
    # Collecting data from each day, relevant to the actor
    actor_summaries: List[DaySummary] = []
    for day_sum in log.days.values():
        actor_sum = day_sum.get(actor)
        if actor_sum is not None:
            actor_summaries.append(actor_sum)
    # Creating dataframe for csv
    if daily:
        # Daily interval
        for day_sum in actor_summaries:
            rows.append([pd.to_datetime(day_sum.date, format='%Y-%m-%d'), day_sum.get_daily_product_per_hour_performance()])
        df = pd.DataFrame(rows, columns=['timestamp', 'productivity'])
    else:
        # Specific timeframe(s)
        for day_sum in actor_summaries:
            productivities_in_intervals = day_sum.get_multiple_interval_productivities(intervals)
            rows.append([pd.to_datetime(day_sum.date, format='%Y-%m-%d'), *productivities_in_intervals])
        # Creating headers
        if intervals is None:
            intervals = DEFAULT_DAY_INTERVALS
        int_headers = [i[0] + '-' + i[1] for i in intervals]
        df = pd.DataFrame(rows, columns=['timestamp', *int_headers])
    # Creating the csv
    df.set_index('timestamp', inplace=True)
    df.to_csv(f'./data/generated/{file_name}', sep=';')


def create_type_2_csv(log: LogSummary, actor_m: str, actor_os: List[str] = None, file_name: str = 'gen_2.csv') -> None:
    '''Writes actor's productivity along with common worktime percentages (with other actors) during the days into a csv.'''
    rows: List[List[pd.Timestamp.date, float, float]] = []    # The second is *float for len(actor_os) number of arguments
    if actor_os is None or len(actor_os) == 0:
        actor_os = tuple(filter(lambda a : a != actor_m, log.actors))
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
        row = [pd.to_datetime(main_summary.date, format='%Y-%m-%d'), m_actor_productivity,
            *list(common_worktime_percent.values())]
        rows.append(row)
    # Creating csv
    df = pd.DataFrame(rows, columns=['timestamp', 'productivity', *actor_os])
    df.set_index('timestamp', inplace=True)
    df.to_csv(f'./data/generated/{file_name}', sep=';')
