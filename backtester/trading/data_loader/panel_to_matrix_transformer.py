import pandas as pd

def transform_panel_to_matrix(panel_data: pd.DataFrame, index: str, columns: str, values: str) -> pd.DataFrame:
    
    matrix_data = panel_data.pivot(index=index, columns=columns, values=values).reset_index()
    matrix_data.set_index(index, inplace=True)

    return matrix_data