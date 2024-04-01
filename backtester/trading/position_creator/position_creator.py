from trading.z_score_calculator.z_score_calculator import InputSeries, ZScoreCalculator
from trading.position_creator.position_object import Positions
import pandas as pd
import numpy as np


class PositionGenerator:
    def __init__(
        self,
        asset_dataframe,
        z_score_data: pd.Series,
        asset_list: list,
        sum_trade_amount: float,
        static_upper_entrance_threshold: float,
        static_upper_exit_threshold: float,
        static_lower_entrance_threshold: float,
        static_lower_exit_threshold: float,
    ):

        self.z_score_data = z_score_data
        self.asset_dataframe = asset_dataframe
        self.asset_list = asset_list
        self.sum_trade_amount = sum_trade_amount
        self.static_upper_entrance_threshold = static_upper_entrance_threshold
        self.static_upper_exit_threshold = static_upper_exit_threshold
        self.static_lower_entrance_threshold = static_lower_entrance_threshold
        self.static_lower_exit_threshold = static_lower_exit_threshold

    def initial_trade(self) -> Positions:

        assets = self.asset_list[0]

        first_asset_amount = calculate_amount_to_invest_in_asset(
            trade_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            asset_number=0,
        )
        second_asset_amount = calculate_amount_to_invest_in_asset(
            trade_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            asset_number=1,
        )
        third_asset_amount = calculate_amount_to_invest_in_asset(
            trade_amount=self.sum_trade_amount,
            asset_list=self.asset_list,
            asset_number=2,
        )

        if self.z_score_data.iloc[-1] >= self.static_upper_entrance_threshold:
            return Positions(assets, (-first_asset_amount, -second_asset_amount, -third_asset_amount))
        elif self.z_score_data.iloc[-1] <= self.static_lower_entrance_threshold:
            return Positions(assets, (first_asset_amount, second_asset_amount, third_asset_amount))
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


def calculate_amount_to_invest_in_asset(
    trade_amount: float,
    asset_list: list,
    asset_number: int,
) -> float:
    original_amount_to_invest_in_one_asset = trade_amount / 2.0
    weights = asset_list[1]
    
    sum_weights = weights[1] + weights[2]
   
    
    second_weight_ratio =  weights[1] / abs(sum_weights)
    third_weight_ratio = weights[2] / abs(sum_weights)
    
    weight_ratio = [1, second_weight_ratio, third_weight_ratio]
    return (original_amount_to_invest_in_one_asset * weight_ratio[asset_number])

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

def add_positive_to_positive_and_negative_to_negative(float_list, asset_list, threshold):
    positive_sum = 0
    negative_sum = 0
    modified_float_list = float_list.copy()
    modified_asset_list = asset_list.copy()
    
    
    for num in float_list:
        if num > 0:
            positive_sum += num
        elif num < 0:
            negative_sum += num
    

    for num in range(len(float_list)):
        if float_list[num] > 0 and abs(float_list[num]) < threshold: 
            modified_asset_list[num] = None
            modified_float_list[num] = None
            if pd.notnull(first_positive_index(modified_float_list)):
                modified_float_list[first_positive_index(modified_float_list)] = positive_sum
        elif float_list[num] < 0 and abs(float_list[num]) < threshold:
            modified_asset_list[num] = None
            modified_float_list[num] = None
            if pd.notnull(first_negative_index(modified_float_list)):
                modified_float_list[first_negative_index(modified_float_list)] = negative_sum

    return [modified_float_list, modified_asset_list]