from typing import Dict, List, Optional
import pandas as pd
from model.log import LogSummary

from services.log_parser import parse_default_csv


def create_csv_1(log: LogSummary):
    rows: List[List[pd.Timestamp.date, int]] = []

    actor0_days = filter(lambda day: day.actor == log.actors[0], log.days)

    for day in actor0_days:
        rows.append([day.date, day.get_number_of_activities_performed()])
    df = pd.DataFrame(rows, columns=['timestamp', 'num of activity performed'])
    print(rows)
    df.set_index('timestamp')
    print(df)
    # TODO: We need to set the first column as index
    df.to_csv('./data/gen_1.csv', sep=';')


if __name__ == "__main__":
    summary = parse_default_csv()
    create_csv_1(summary)
