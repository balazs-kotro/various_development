from trading.z_score_calculator.z_score_calculator import InputSeries, ZScoreCalculator
from trading.position_creator.position_object import Positions
import pandas as pd
import numpy as np


class PositionGenerator:
    def __init__(
        self,
        z_score_data: InputSeries,
        static_upper_entrance_threshold: float,
        static_upper_exit_threshold: float,
        static_lower_entrance_threshold: float,
        static_lower_exit_threshold: float,
    ):

        self.z_score_data = z_score_data
        self.static_upper_entrance_threshold = static_upper_entrance_threshold
        self.static_upper_exit_threshold = static_upper_exit_threshold
        self.static_lower_entrance_threshold = static_lower_entrance_threshold
        self.static_lower_exit_threshold = static_lower_exit_threshold

    def trade_direction(
        self, first_series: pd.Series, second_series: pd.Series
    ) -> Positions:
        series_difference = first_series.iloc[-1] - second_series.iloc[-1]
        print(series_difference)

        if series_difference >= self.static_upper_entrance_threshold:
            return Trade((first_series.name, second_series.name), (-1, 1))
        if series_difference <= self.static_lower_entrance_threshold:
            return Trade((first_series.name, second_series.name), (1, -1))
        else:
            return Trade((first_series.name, second_series.name), (0, 0))

    def initial_trade(self):
        trade_on_a_and_b = self.trade_direction(
            self.z_score_data.input_time_series_a, self.z_score_data.input_time_series_b
        )
        trade_on_a_and_c = self.trade_direction(
            self.z_score_data.input_time_series_a, self.z_score_data.input_time_series_c
        )
        trade_on_b_and_c = self.trade_direction(
            self.z_score_data.input_time_series_b, self.z_score_data.input_time_series_c
        )

        return Trade.sum_instances(
            [trade_on_a_and_b, trade_on_a_and_c, trade_on_b_and_c]
        )

    def generate_positions(self) -> str:
        return "4 - PositionGenerator is called"
