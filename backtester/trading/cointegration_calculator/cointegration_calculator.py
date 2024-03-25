import pandas as pd
import numpy as np
from itertools import combinations
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen


class CointegrationCalculator:
    def __init__(self, time_series_matrix: pd.DataFrame) -> None:
        self.time_series_matrix = time_series_matrix

    def find_cointegrated_assets(self) -> str:
        triplets = list(combinations(self.time_series_matrix.columns, 3))

        for triplet in triplets:
            cointegration_results =coint_johansen(
            pd.DataFrame({
            triplet[0]: self.time_series_matrix[triplet[0]].astype(float).values, 
            triplet[1]: self.time_series_matrix[triplet[1]].astype(float).values,
            triplet[2]: self.time_series_matrix[triplet[2]].astype(float).values}),
            det_order=0, k_ar_diff=1)


            critical_value = cointegration_results.cvt[:, 1]  # 1 corresponds to 95% confidence level

            trace_statistic = cointegration_results.lr1

            num_cointegrating_relationships = np.sum(trace_statistic > critical_value)

            if num_cointegrating_relationships == 3:
                print(triplet)
                print(cointegration_results.evec[:, 0] / cointegration_results.evec[:, 0][0])
