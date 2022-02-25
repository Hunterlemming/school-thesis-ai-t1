from typing import Union

import pandas as pd


def later_of(t1: Union[str, pd.Timestamp.time], t2: Union[str, pd.Timestamp.time]) -> Union[str, pd.Timestamp.time]:
    '''Returns the time-string of the later time parameter.'''
    t1_date, t2_date = pd.to_datetime(str(t1)), pd.to_datetime(str(t2))
    return t1 if t1_date >= t2_date else t2

def earlier_of(t1: Union[str, pd.Timestamp.time], t2: Union[str, pd.Timestamp.time]) -> Union[str, pd.Timestamp.time]:
    '''Returns the time-string of the earlier time parameter.'''
    t1_date, t2_date = pd.to_datetime(str(t1)), pd.to_datetime(str(t2))
    return t1 if t1_date <= t2_date else t2
