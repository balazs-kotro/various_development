import pandas as pd
import numpy as np
from dataclasses import dataclass, fields


@dataclass
class InputSeries:
    input_time_series_a: pd.Series
    input_time_series_b: pd.Series
    input_time_series_c: pd.Series


class ZScoreCalculator:

    def __init__(self, input_data: pd.DataFrame, asset_list: list):
        self.input_data = input_data
        self.asset_list = asset_list

    def calculate_z_score(self, input_series: pd.Series) -> pd.Series:
        return (input_series - input_series.mean()) / np.std(input_series)

    def run(self):
        spread_series = calculate_spread(input_data= self.input_data, asset_list=self.asset_list )
        spread_time_series = self.calculate_z_score(spread_series)
        return spread_time_series


def calculate_spread(input_data: pd.DataFrame, asset_list: list) -> pd.Series:
    weights = asset_list[1]
    assets = asset_list[0]
    spread_time_series = (
        input_data[assets[0]].astype(float).values
        + weights[1] * input_data[assets[1]].astype(float).values
        + weights[2] * input_data[assets[2]].astype(float).values
    )

    return pd.Series(spread_time_series)
