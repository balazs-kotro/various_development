from trading.z_score_calculator.z_score_calculator import InputSeries, ZScoreCalculator
from trading.position_creator.position_object import Positions
import pandas as pd
import numpy as np
import uuid


class PositionGenerator:
    def __init__(
        self,
        asset_dataframe,
        z_score_data: pd.Series,
        asset_list: list,
        ratios,
        position_id,
        sum_trade_amount: float,
        static_upper_entrance_threshold: float,
        static_upper_exit_threshold: float,
        static_lower_entrance_threshold: float,
        static_lower_exit_threshold: float,
    ):

        self.z_score_data = z_score_data
        self.asset_dataframe = asset_dataframe
        self.asset_list = asset_list
        self.ratios = ratios
        self.position_id = position_id
        self.sum_trade_amount = sum_trade_amount
        self.static_upper_entrance_threshold = static_upper_entrance_threshold
        self.static_upper_exit_threshold = static_upper_exit_threshold
        self.static_lower_entrance_threshold = static_lower_entrance_threshold
        self.static_lower_exit_threshold = static_lower_exit_threshold

    def intermittent_trade(self) -> Positions:

        filtered_dataframe = self.asset_dataframe.astype(float)[list(self.asset_list)]
        date = self.asset_dataframe.index[-1]

        if (
            self.z_score_data.iloc[-2]
            < self.static_lower_exit_threshold and self.z_score_data.iloc[-1]
            >= self.static_lower_exit_threshold
        ) or (
            self.z_score_data.iloc[-2]
            > self.static_upper_exit_threshold and self.z_score_data.iloc[-1]
            <= self.static_upper_exit_threshold
        ):
            ratios =[-x for x in self.ratios]
            invested_amounts = ratios * filtered_dataframe.values[-1]

            return Positions(
                position_id=self.position_id,
                date=date,
                assets=self.asset_list,
                asset_ratios=ratios,
                invested_amounts=invested_amounts,
                weights=ratios
            )

    def initial_trade(self) -> Positions:

        assets = list(self.asset_list[0])
        weights = list(self.asset_list[1])
        date = self.asset_dataframe.index[-1]

        first_asset_amount = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[0][0]
        first_asset_ratio = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[1][0]

        second_asset_amount = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[0][1]
        second_asset_ratio = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[1][1]

        third_asset_amount = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[0][2]
        third_asset_ratio = calculate_ratio_to_invest_in_asset(
            initial_investment_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            time_series_matrix=self.asset_dataframe,
        )[1][2]

        if self.z_score_data.iloc[-1] >= self.static_upper_entrance_threshold:
            assets_and_position_list = position_aggregator(
                float_list=[
                    first_asset_amount,
                    second_asset_amount,
                    third_asset_amount,
                ],
                ratio_list=[
                    first_asset_ratio,
                    second_asset_ratio,
                    third_asset_ratio,
                ],
                asset_list=assets,
                weight_list=weights,
                threshold=5,
            )
            assets_and_position_list[0] = [
                -element for element in assets_and_position_list[0]
            ]
            return Positions(
                position_id=position_id,
                assets=assets_and_position_list[1],
                date=date,
                asset_ratios=assets_and_position_list[2],
                invested_amounts=assets_and_position_list[0],
                weights=weights,
            )

        elif self.z_score_data.iloc[-1] <= self.static_lower_entrance_threshold:

            assets_and_position_list = position_aggregator(
                float_list=[
                    first_asset_amount,
                    second_asset_amount,
                    third_asset_amount,
                ],
                ratio_list=[
                    first_asset_ratio,
                    second_asset_ratio,
                    third_asset_ratio,
                ],
                asset_list=assets,
                weight_list=weights,
                threshold=5,
            )

            position_id = uuid.uuid4()

            return Positions(
                position_id=position_id,
                assets=assets_and_position_list[1],
                date=date,
                asset_ratios=assets_and_position_list[2],
                invested_amounts=assets_and_position_list[0],
                weights=weights,
            )
        else:
            pass

    # def initial_trade(self):
    #     trade_on_a_and_b = self.trade_direction(
    #         self.z_score_data.input_time_series_a, self.z_score_data.input_time_series_b
    #     )
    #     trade_on_a_and_c = self.trade_direction(
    #         self.z_score_data.input_time_series_a, self.z_score_data.input_time_series_c
    #     )
    #     trade_on_b_and_c = self.trade_direction(
    #         self.z_score_data.input_time_series_b, self.z_score_data.input_time_series_c
    #     )

    #     return Trade.sum_instances(
    #         [trade_on_a_and_b, trade_on_a_and_c, trade_on_b_and_c]
    #     )


def calculate_ratio_to_invest_in_asset(
    initial_investment_amount: float, asset_list: list, time_series_matrix: pd.DataFrame
):
    assets = asset_list[0]
    weights = asset_list[1]
    filtered_dataframe = time_series_matrix.astype(float)[list(assets)]

    positive_indices = find_positive_or_negative_indices_in_list(
        input_list=weights, indicator="positive"
    )
    negative_indices = find_positive_or_negative_indices_in_list(
        input_list=weights, indicator="negative"
    )

    positive_asset_ratios = asset_ratio_calculator(
        initial_investment_amount=initial_investment_amount,
        weights=weights,
        time_series_matrix=filtered_dataframe,
        indicator="positive",
    )

    negative_asset_ratios = asset_ratio_calculator(
        initial_investment_amount=initial_investment_amount,
        weights=weights,
        time_series_matrix=filtered_dataframe,
        indicator="negative",
    )

    result_list = [None, None, None]

    for element in range(len(positive_asset_ratios)):
        proper_index = positive_indices[element]
        result_list[proper_index] = positive_asset_ratios.iloc[element]

    for element in range(len(negative_asset_ratios)):
        proper_index = negative_indices[element]
        result_list[proper_index] = -negative_asset_ratios.iloc[element]

    return (list(result_list * filtered_dataframe.values[-1]), result_list)


def first_positive_index(lst):
    for i, num in enumerate(lst):
        if num is not None and num > 0:
            return i
    return None


def first_negative_index(lst):
    for i, num in enumerate(lst):
        if num is not None and num < 0:
            return i
    return None


def position_aggregator(float_list, asset_list, weight_list, ratio_list, threshold):
    positive_sum = 0
    negative_sum = 0
    positive_ratio_sum = 0
    negative_ratio_sum = 0
    modified_float_list = float_list.copy()
    modified_asset_list = asset_list.copy()
    modified_ratio_list = ratio_list.copy()
    modified_weight_list = ratio_list.copy()

    for num in float_list:
        if num > 0:
            positive_sum += num
        elif num < 0:
            negative_sum += num

    for num in ratio_list:
        if num > 0:
            positive_ratio_sum += num
        elif num < 0:
            negative_ratio_sum += num

    for num in range(len(float_list)):
        if float_list[num] > 0 and abs(float_list[num]) < threshold:
            modified_asset_list[num] = None
            modified_float_list[num] = None
            modified_ratio_list[num] = None
            modified_weight_list[num] = None
            if pd.notnull(first_positive_index(modified_float_list)):
                modified_float_list[first_positive_index(modified_float_list)] = (
                    positive_sum
                )
        elif float_list[num] < 0 and abs(float_list[num]) < threshold:
            modified_asset_list[num] = None
            modified_float_list[num] = None
            modified_ratio_list[num] = None
            modified_weight_list[num] = None
            if pd.notnull(first_negative_index(modified_float_list)):
                modified_float_list[first_negative_index(modified_float_list)] = (
                    negative_sum
                )

    return [
        modified_float_list,
        modified_asset_list,
        modified_ratio_list,
        modified_weight_list,
    ]


def find_positive_or_negative_indices_in_list(input_list: list, indicator: str):
    if indicator == "positive":
        indices = [i for i, num in enumerate(input_list) if num > 0]
    if indicator == "negative":
        indices = [i for i, num in enumerate(input_list) if num < 0]
    return indices


def asset_ratio_calculator(
    initial_investment_amount: float,
    weights: list,
    time_series_matrix: pd.DataFrame,
    indicator: str,
):
    asset_weights = find_positive_or_negative_indices_in_list(
        input_list=weights, indicator=indicator
    )
    asset_weight_values = [weights[i] for i in asset_weights]
    assets = time_series_matrix.iloc[:, asset_weights]
    assets_last_values = assets.iloc[-1, :]
    weighted_amounts = assets_last_values * asset_weight_values
    artificial_time_series_latest_positive_value = sum(
        assets_last_values * asset_weight_values
    )
    money_allocation_ratio = (
        weighted_amounts / artificial_time_series_latest_positive_value
    )
    money_allocation = money_allocation_ratio * initial_investment_amount
    asset_allocation = pd.Series(money_allocation) / pd.Series(assets_last_values)
    return asset_allocation
