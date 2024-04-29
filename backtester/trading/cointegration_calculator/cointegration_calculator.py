import pandas as pd
import numpy as np
from itertools import combinations
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from scipy.stats import chi2
from typing import Tuple, List
from itertools import permutations


class CointegrationCalculator:
    def __init__(self, time_series_matrix: pd.DataFrame) -> None:
        self.time_series_matrix = time_series_matrix

    def dataframe_wrapper(self, asset_list: list) -> pd.DataFrame:
        asset_dataframe = pd.DataFrame(
            {
                asset_list[0]: self.time_series_matrix[asset_list[0]]
                .astype(float)
                .values,
                asset_list[1]: self.time_series_matrix[asset_list[1]]
                .astype(float)
                .values,
                asset_list[2]: self.time_series_matrix[asset_list[2]]
                .astype(float)
                .values,
            }
        )
        return asset_dataframe

    def find_cointegrated_assets(self) -> list:
        triplets = list(combinations(self.time_series_matrix.columns, 3))
        cointegrated_assets_list = []
        for triplet in triplets:

            asset_dataframe = self.dataframe_wrapper(asset_list=triplet)

            optimal_cointegration_results, optimal_lag = best_johansen_model_finder(
                asset_dataframe=asset_dataframe, max_lag=6
            )

            cointegrated_asset_specifications = list_cointegrated_assets(
                triplet=triplet,
                cointegration_results=optimal_cointegration_results,
                optimal_lag=optimal_lag,
            )
            if pd.isnull(
                cointegrated_asset_specifications
            ):
                continue
            else:
                cointegrated_assets_list.append(cointegrated_asset_specifications)

        filtered_list = cointegrated_assets_list
        return filtered_list


def likelihood_ratio_test(
    likelihood_of_the_null_pypothesis: float,
    likelihood_of_the_alternative_pypothesis: float,
    degrees_of_freedom: int,
):
    likelihood_ratio_stat = 2 * (
        likelihood_of_the_alternative_pypothesis - likelihood_of_the_null_pypothesis
    )
    p_value = 1 - chi2.cdf(likelihood_ratio_stat, degrees_of_freedom)
    return likelihood_ratio_stat, p_value


def best_johansen_model_finder(asset_dataframe: pd.DataFrame, max_lag: int):
    best_lag = None
    best_likelihood_ratio_stat = float("-inf")
    best_p_value = None
    best_cointegration_results = None

    for lag in range(1, max_lag):
        cointegration_results = coint_johansen(
            asset_dataframe, det_order=0, k_ar_diff=lag
        )

        likelihood_of_the_null_pypothesis = cointegration_results.lr1[0]
        likelihood_of_the_alternative_pypothesis = cointegration_results.lr1[1]
        degrees_of_freedom = lag - 1

        likelihood_ratio_stat, p_value = likelihood_ratio_test(
            likelihood_of_the_null_pypothesis,
            likelihood_of_the_alternative_pypothesis,
            degrees_of_freedom,
        )

        if likelihood_ratio_stat > best_likelihood_ratio_stat:
            best_lag = lag
            best_likelihood_ratio_stat = likelihood_ratio_stat
            best_p_value = p_value
            best_cointegration_results = cointegration_results

    return best_cointegration_results, best_lag


def list_cointegrated_assets(triplet, cointegration_results, optimal_lag) -> tuple:

    weights = cointegration_results.evec[:, 0] / cointegration_results.evec[:, 0][0]

    critical_value = cointegration_results.cvt[:, 1]
    trace_statistic = cointegration_results.lr1

    number_of_cointegrating_relationships = np.sum(trace_statistic > critical_value)

    if number_of_cointegrating_relationships == 3:
        return (triplet, weights, optimal_lag)


def check_if_all_element_is_larger_than_threshold(input_list: list, threshold: int):
    return all(element > threshold for element in input_list)

def check_if_all_element_is_smaller_than_threshold(input_list: list, threshold: int):
    absolute_list = [abs(element) for element in input_list]
    return any(element < threshold for element in absolute_list)
