import pytest
from copy import deepcopy
import unittest
from unittest.mock import patch
import pandas as pd
from trading.cointegration_calculator.cointegration_calculator import (
    CointegrationCalculator,
    likelihood_ratio_test,
)


def test_find_cointegrated_assets(mocker):
    mock_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    mocker.patch("pandas.DataFrame", return_value=mock_df)
    mock_result = (1.23, 4.56)
    mock_coint_johansen = mocker.patch("statsmodels.tsa.vector_ar.vecm.coint_johansen")
    mock_coint_johansen.return_value = mock_result

    expected_data1 = 1.0
    expected_data2 = 1

    mocker.patch(
        "trading.cointegration_calculator.cointegration_calculator.best_johansen_model_finder",
        return_value=(1.0, 1),
    )

    mocker.patch(
        "trading.cointegration_calculator.cointegration_calculator.list_cointegrated_assets",
        side_effect=[
            (["A", "B", "C"], [1.0, 1.0, 1.0], 1),
            (["A", "C", "B"], [1.0, 1.0, 1.0], 1),
            (["B", "A", "C"], [1.0, 1.0, 1.0], 1),
            (["B", "C", "A"], [1.0, 1.0, 1.0], 1),
            (["C", "A", "B"], [1.0, -1.0, 1.0], 1),
            (["C", "B", "A"], [1.0, 1.0, 1.0], 1),
            ]
    )

    cointegration_calculator = CointegrationCalculator(mock_df)

    actual_list = cointegration_calculator.find_cointegrated_assets()
    expected_list = [(['C', 'A', 'B'], [1.0, -1.0, 1.0], 2)]

    assert actual_list == expected_list


# def test_likelihood_ratio_test() -> None:
#     print("I am in test_likelihood_ratio_test")
#     likelihood_of_the_null_pypothesis = 1.0
#     likelihood_of_the_alternative_pypothesis = 1.0
#     degrees_of_freedom = 1

#     actual_likelihood_ratio_stat, actual_p_value = likelihood_ratio_test(
#         likelihood_of_the_null_pypothesis=likelihood_of_the_null_pypothesis,
#         likelihood_of_the_alternative_pypothesis=likelihood_of_the_alternative_pypothesis,
#         degrees_of_freedom=degrees_of_freedom,
#     )

#     expected_p_value = 1.0
#     expected_likelihood_ratio_stat = 0.0

    # assert actual_likelihood_ratio_stat == expected_likelihood_ratio_stat
    # assert actual_p_value == expected_p_value
