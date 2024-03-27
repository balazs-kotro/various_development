import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from scipy.stats import chi2





if __name__ == "__main__":




    # Generate sample data
    nobs = 100
    x = np.random.randn(nobs, 2)
    y = np.random.randn(nobs, 3)

    # Concatenate variables
    data = np.concatenate((x, y), axis=1)


    result_with_constant = coint_johansen(y, det_order=1, k_ar_diff=2)


    cointegration_vector = result_with_constant.evec

# Calculate weights
    weights = cointegration_vector / cointegration_vector[0]  # Normalize by the first element

    print("Weights:", cointegration_vector)