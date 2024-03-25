import pandas as pd
import numpy as np
from itertools import combinations
from statsmodels.tsa.stattools import coint


class CointegrationCalculator:
    def __init__(self, time_series_matrix: pd.DataFrame) -> None:
        self.time_series_matrix = time_series_matrix

    def find_cointegrated_assets(self) -> str:
        triplets = list(combinations(self.time_series_matrix.columns, 3))

        cointegration_results = [(triplet, coint(df[triplet[0]], df[triplet[1]], df[triplet[2]])) for triplet in triplets]

        cointegrated_triplets = [(triplet, result) for triplet, result in cointegration_results if result[1] < 0.05]
        print("Cointegrated triplets:")
        for triplet in cointegrated_triplets:
            print(triplet)
