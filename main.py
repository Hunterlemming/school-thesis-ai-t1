from typing import List
import pandas as pd
from model.day import DEFAULT_DAY_INTERVALS
from model.log import LogSummary

from services.log_parser import parse_default_csv


def create_csv_1(log: LogSummary):
    rows: List[List[pd.Timestamp.date, int]] = []

    actor0_days = []
    for day in log.days.values():
        actor0_days.append(day[log.actors[0]])

    
    for day in actor0_days:
        rows.append([pd.to_datetime(day.date, format='%Y-%m-%d'), day.get_daily_all_number_of_products()])
    df = pd.DataFrame(rows, columns=['timestamp', 'num of activity performed'])
    df.set_index('timestamp', inplace=True)
    df.to_csv('./data/generated/gen_1.csv', sep=';')


if __name__ == "__main__":
    summary = parse_default_csv()
    print(summary)
    create_csv_1(summary)
    print(summary.get_day_by_date('2022-02-18'))
    # wh = summary.get_same_date_days_with_index(0)
    # for day in wh:
    #     print(day)
