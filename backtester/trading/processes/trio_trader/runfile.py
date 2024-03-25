import pandas as pd
from trading.data_loader.data_loader import DataLoader
import trading.data_loader.panel_to_matrix_transformer as panel_to_matrix_transformer
from trading.data_writer.data_writer import DataWriter
from trading.cointegration_calculator.cointegration_calculator import CointegrationCalculator
from trading.z_score_calculator.z_score_calculator import ZScoreCalculator, InputSeries
from trading.position_creator.position_creator import PositionGenerator


class TrioTrader:

    def __init__(self, input_data) -> None:
        self.input_data = input_data
        self.dummy = "dummy_string"

    def run(self) -> None:

        data_loader_class = DataLoader("assets")
        time_series_panel = data_loader_class.load_whole_table()
        time_series_matrix = panel_to_matrix_transformer.transform_panel_to_matrix(panel_data=time_series_panel, index="date", columns="asset", values="value")
       
        cointegration_calculator = CointegrationCalculator()
        cointegrated_series = cointegration_calculator.find_cointegrated_assets()
        print(cointegrated_series)

        z_score_calculator = ZScoreCalculator(self.input_data)
        z_scores, dummy_z_score = z_score_calculator.calculate_z_scores()
        print(z_scores)

        posiiton_generator = PositionGenerator(dummy_z_score, 1.0, 1.0, 1.0, 1.0)
        generated_positions = posiiton_generator.generate_positions()
        print(generated_positions)

        data_writer_class = DataWriter()
        stored_positions = data_writer_class.write_data_to_database()
        print(stored_positions)


if __name__ == "__main__":
    data_instance = InputSeries(
        input_time_series_a=pd.Series([250, 255, 230], name="A_asset"),
        input_time_series_b=pd.Series([33, 30, 35], name="B_asset"),
        input_time_series_c=pd.Series([15, 18, 10], name="C_asset"),
    )

    trio_trader = TrioTrader(data_instance)
    trio_trader.run()
