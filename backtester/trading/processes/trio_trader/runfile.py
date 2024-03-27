import pandas as pd
from trading.data_loader.data_loader import DataLoader
import trading.data_loader.panel_to_matrix_transformer as panel_to_matrix_transformer
from trading.data_writer.data_writer import DataWriter
from trading.cointegration_calculator.cointegration_calculator import (
    CointegrationCalculator,
)
from trading.z_score_calculator.z_score_calculator import ZScoreCalculator, InputSeries
from trading.position_creator.position_creator import PositionGenerator
import pickle


class TrioTrader:

    def __init__(self, input_data, run_cointegration) -> None:
        self.input_data = input_data
        self.run_cointegration = run_cointegration

    def run(self) -> None:

        data_loader_class = DataLoader("assets")
        time_series_panel = data_loader_class.load_whole_table()
        time_series_matrix = panel_to_matrix_transformer.transform_panel_to_matrix(
            panel_data=time_series_panel, index="date", columns="asset", values="value"
        )

        if self.run_cointegration:
            cointegration_calculator = CointegrationCalculator(
                time_series_matrix[0:500]
            )
            cointegrated_assets_list = (
                cointegration_calculator.find_cointegrated_assets()
            )

            with open(
                "/app/trading/processes/trio_trader/cointegrated_assets_list.pkl", "wb"
            ) as file:
                pickle.dump(cointegrated_assets_list, file)
        else:
            with open(
                "/app/trading/processes/trio_trader/cointegrated_assets_list.pkl", "rb"
            ) as file:
                cointegrated_assets_list = pickle.load(file)

        z_score_calculator = ZScoreCalculator(
            time_series_matrix[0:500], cointegrated_assets_list
        )
        z_score_calculator.calculate_z_scores()

        # position_generator = PositionGenerator(dummy_z_score, 1.0, 1.0, 1.0, 1.0)
        # generated_positions = position_generator.generate_positions()
        # print(generated_positions)

        # data_writer_class = DataWriter()
        # stored_positions = data_writer_class.write_data_to_database()
        # print(stored_positions)


if __name__ == "__main__":
    data_instance = InputSeries(
        input_time_series_a=pd.Series([250, 255, 230], name="A_asset"),
        input_time_series_b=pd.Series([33, 30, 35], name="B_asset"),
        input_time_series_c=pd.Series([15, 18, 10], name="C_asset"),
    )

    trio_trader = TrioTrader(input_data=data_instance, run_cointegration=True)
    trio_trader.run()
