import sample_function
import pandas as pd


def test_first_function() -> None:

    actual_value = sample_function.first_function()
    expected_value = 2

    assert actual_value == expected_value
