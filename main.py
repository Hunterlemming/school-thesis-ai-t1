from typing import Dict, List, Optional
import pandas as pd

from services.csv_services import parse_default_csv_to_days


if __name__ == "__main__":
    days = parse_default_csv_to_days()
    for day in days:
        print(day)