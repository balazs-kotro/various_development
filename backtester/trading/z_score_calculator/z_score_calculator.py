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
        z_score_list = []
        series = fields(self.input_data)
        for i in series:
            current_series = getattr(self.input_data, i.name)
            z_score = self.calculate_z_score(current_series)
            z_score_list.append(z_score)

        return InputSeries(*z_score_list)

    def calculate_z_scores(self):
        print(self.asset_list)
