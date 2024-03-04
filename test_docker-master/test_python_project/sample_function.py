import pandas as pd



def first_function() -> pd.Series:
    first_series = pd.Series([0, 1])
    second_series = pd.Series([2, 3])

    return first_series[0] + second_series[0]
