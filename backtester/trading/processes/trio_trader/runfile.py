import pandas as pd
from trading.data_loader.data_loader import DataLoader
import trading.data_loader.panel_to_matrix_transformer as panel_to_matrix_transformer
from trading.data_writer.data_writer import DataWriter
from trading.cointegration_calculator.cointegration_calculator import (
    CointegrationCalculator,
)
from trading.z_score_calculator.z_score_calculator import ZScoreCalculator, InputSeries
from trading.position_creator.position_creator import PositionGenerator, Positions
from trading.position_creator.portfolio_creator import (
    PortfolioGenerator,
    scaled_initial_trade,
    intermittent_trades,
)
from trading.position_creator.super_position_object import SuperPosition
import pickle
import uuid
import copy


class TrioTrader:

    def __init__(self, input_data, run_cointegration) -> None:
        self.input_data = input_data
        self.run_cointegration = run_cointegration

    def run(self) -> None:

        aggregated_initial_trades = None
        super_position = SuperPosition()
        initial_trade_list = []

        data_loader_class = DataLoader("assets")
        time_series_panel = data_loader_class.load_whole_table()
        time_series_matrix = panel_to_matrix_transformer.transform_panel_to_matrix(
            panel_data=time_series_panel, index="date", columns="asset", values="value"
        )

        parent_id = uuid.uuid4()

        latest_range_point = 200

        for i in range(0, latest_range_point):
            if len(initial_trade_list) == 0:
                if self.run_cointegration:
                    cointegration_calculator = CointegrationCalculator(
                        time_series_matrix[0:500]
                    )
                    cointegrated_assets_list = (
                        cointegration_calculator.find_cointegrated_assets()
                    )

                    with open(
                        "/app/trading/processes/trio_trader/cointegrated_assets_list.pkl",
                        "wb",
                    ) as file:
                        pickle.dump(cointegrated_assets_list, file)
                else:
                    with open(
                        "/app/trading/processes/trio_trader/cointegrated_assets_list.pkl",
                        "rb",
                    ) as file:
                        cointegrated_assets_list = pickle.load(file)

                for cointegrated_asset_triplet in cointegrated_assets_list:
                    z_score_calculator = ZScoreCalculator(
                        time_series_matrix[0 : 500 + i], cointegrated_asset_triplet
                    )
                    spread, z_score_spread = z_score_calculator.run()

                    position_generator = PortfolioGenerator(
                        time_series_matrix[0 : 500 + i],
                        spread,
                        z_score_spread,
                        cointegrated_asset_triplet,
                        None,
                        None,
                        100,
                        0.4,
                        0.0,
                        -0.4,
                        0.0,
                    )
                    initial_trade = position_generator.initial_trade()
                    if pd.notnull(initial_trade):
                        initial_trade_list.append(initial_trade)
                        # position_id = getattr(initial_trade, "position_id")
                        # assets = getattr(initial_trade, "assets")
                        # scaling_factor = getattr(initial_trade, "scaling_factor")
                        # invested_amounts = getattr(initial_trade, "invested_amounts")
                        # date = getattr(initial_trade, "date")

                scaled_initial_trade(initial_trade_list, 100.0)

                for trade in initial_trade_list:
                    super_position.add_class(trade)
                    DataWriter(trade).write_data_to_database()

            else:
                print(i)

                classes = super_position.get_classes()

                for current_class in range(len(classes)):
                    cointegrated_asset_triplet = getattr(
                        classes[current_class], "assets"
                    )
                    regression_weights = getattr(
                        classes[current_class], "regression_weights"
                    )
                    z_score_calculator = ZScoreCalculator(
                        time_series_matrix[0 : 500 + i],
                        list([cointegrated_asset_triplet, regression_weights]),
                    )
                    spread, z_score_spread = z_score_calculator.run()
                    position_generator = PortfolioGenerator(
                        time_series_matrix[0 : 500 + i],
                        spread,
                        z_score_spread,
                        cointegrated_asset_triplet,
                        None,
                        None,
                        100,
                        0.4,
                        0.0,
                        -0.4,
                        0.0,
                    )
                    if i == latest_range_point-1:
                        intermittent_trade = intermittent_trades(
                            asset_dataframe=time_series_matrix[0 : 500 + i],
                            asset_list=cointegrated_asset_triplet,
                            z_score_data=pd.Series([-1,0]),
                            static_lower_exit_threshold=0.0,
                            static_upper_exit_threshold=0.0,
                            position_class=classes[current_class],
                        )
                    else:
                        intermittent_trade = intermittent_trades(
                            asset_dataframe=time_series_matrix[0 : 500 + i],
                            asset_list=cointegrated_asset_triplet,
                            z_score_data=z_score_spread,
                            static_lower_exit_threshold=0.0,
                            static_upper_exit_threshold=0.0,
                            position_class=classes[current_class],
                        )

                    if pd.notnull(intermittent_trade):
                        position_id = getattr(intermittent_trade, "position_id")
                        assets = getattr(intermittent_trade, "assets")
                        date = getattr(intermittent_trade, "date")
                        invested_amounts = getattr(
                            intermittent_trade, "invested_amounts"
                        )

                        DataWriter(intermittent_trade).write_data_to_database()

                        setattr(classes[current_class], "assets", [None, None, None])
                    else:
                        if i == latest_range_point-1:
                            print("things are here")

                    super_position.remove_classes_with_none_attribute()
                    print(len(classes))


if __name__ == "__main__":
    data_instance = InputSeries(
        input_time_series_a=pd.Series([250, 255, 230], name="A_asset"),
        input_time_series_b=pd.Series([33, 30, 35], name="B_asset"),
        input_time_series_c=pd.Series([15, 18, 10], name="C_asset"),
    )

    trio_trader = TrioTrader(input_data=data_instance, run_cointegration=False)
    trio_trader.run()
