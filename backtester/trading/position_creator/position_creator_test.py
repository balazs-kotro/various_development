from trading.position_creator.position_creator import (
    position_aggregator,
    calculate_ratio_to_invest_in_asset,
    asset_ratio_calculator,
)
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "input_list, expected_list",
    [
        ([[1.1, 1.8, -1.2], ["A", "B", "C"]], [[1.1, 1.8, -1.2], ["A", "B", "C"]]),
        ([[1.1, -1.8, -1.2], ["A", "B", "C"]], [[1.1, -1.8, -1.2], ["A", "B", "C"]]),
        ([[1.1, 1.8, 1.2], ["A", "B", "C"]], [[1.1, 1.8, 1.2], ["A", "B", "C"]]),
        ([[-1.1, -1.8, -1.2], ["A", "B", "C"]], [[-1.1, -1.8, -1.2], ["A", "B", "C"]]),
        ([[0.2, 1.8, -1.2], ["A", "B", "C"]], [[None, 2.0, -1.2], [None, "B", "C"]]),
        ([[1.2, 0.8, -1.2], ["A", "B", "C"]], [[2.0, None, -1.2], ["A", None, "C"]]),
        ([[-1.2, 1.8, -0.2], ["A", "B", "C"]], [[-1.4, 1.8, None], ["A", "B", None]]),
        ([[1.0, -1.8, -0.2], ["A", "B", "C"]], [[1.0, -2.0, None], ["A", "B", None]]),
        (
            [[0.8, -0.8, -0.2], ["A", "B", "C"]],
            [[None, None, None], [None, None, None]],
        ),
        ([[0.8, 0.8, -1.2], ["A", "B", "C"]], [[None, None, -1.2], [None, None, "C"]]),
        ([[1.8, -0.8, -0.2], ["A", "B", "C"]], [[1.8, None, None], ["A", None, None]]),
    ],
)
def test_position_aggregator(input_list, expected_list) -> None:
    threshold = 1.0
    actual_list = position_aggregator(
        float_list=input_list[0], asset_list=input_list[1], threshold=threshold
    )

    assert actual_list == expected_list


def test_calculate_ratio_to_invest_in_asset() -> None:
    input_list = [["BP", "NVTK", "SIBN"], [1, 0.61463125, -0.54752609]]
    input_dataframe = pd.DataFrame(
        {"BP": [490.25, 500.25], "NVTK": [134.89, 141.03], "SIBN": [111.01, 115.6]}
    )

    expected_list = [42.61570956044032, 7.384290439559675, -50.0]

    actual_list = calculate_ratio_to_invest_in_asset(
        asset_list=input_list,
        time_series_matrix=input_dataframe,
        initial_investment_amount=50.0,
    )


    assert expected_list == actual_list


def test_asset_ratio_calculator_for_positive_values() -> None:
    weights = [1, 0.61463125, -0.54752609]
    input_dataframe = pd.DataFrame(
        {"BP": [490.25, 500.25], "NVTK": [134.89, 141.03], "SIBN": [111.01, 115.6]}
    )
    initial_investment_amount = 50.0
    expected_asset_ratios = pd.Series(
        [0.085189, 0.052360], index=["BP", "NVTK"], name=1
    )
    positive_asset_ratios = asset_ratio_calculator(
        initial_investment_amount=initial_investment_amount,
        weights=weights,
        time_series_matrix=input_dataframe,
        indicator="positive",
    )
    pd.testing.assert_series_equal(expected_asset_ratios, positive_asset_ratios)


def test_asset_ratio_calculator_for_negative_values() -> None:
    weights = [1, 0.61463125, -0.54752609]
    input_dataframe = pd.DataFrame(
        {"BP": [490.25, 500.25], "NVTK": [134.89, 141.03], "SIBN": [111.01, 115.6]}
    )
    initial_investment_amount = 50.0
    expected_asset_ratios = pd.Series([0.432525952], index=["SIBN"], name=1)
    negative_asset_ratios = asset_ratio_calculator(
        initial_investment_amount=initial_investment_amount,
        weights=weights,
        time_series_matrix=input_dataframe,
        indicator="negative",
    )
    pd.testing.assert_series_equal(expected_asset_ratios, negative_asset_ratios)
