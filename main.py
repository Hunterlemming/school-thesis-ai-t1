from typing import Dict, List, Optional
import pandas as pd

from services.log_parser import parse_default_csv_to_days


def create_csv_1():
    raise NotImplementedError


if __name__ == "__main__":
    days = parse_default_csv_to_days()
    for day in days:
        print(day)