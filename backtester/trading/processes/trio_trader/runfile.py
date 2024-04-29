import pandas as pd
from trading.data_loader.data_loader import DataLoader
import trading.data_loader.panel_to_matrix_transformer as panel_to_matrix_transformer
from trading.data_writer.data_writer import DataWriter
from trading.cointegration_calculator.cointegration_calculator import (
    CointegrationCalculator,
)
from trading.z_score_calculator.z_score_calculator import ZScoreCalculator, InputSeries
from trading.position_creator.position_creator import PositionGenerator, Positions
from trading.position_creator.super_position_object import SuperPosition
import pickle
import uuid


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

        for i in range(0, 1):
            if aggregated_initial_trades is None:
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
                    z_score_spread = z_score_calculator.run()

                    position_generator = PositionGenerator(
                        time_series_matrix[0 : 500 + i],
                        z_score_spread,
                        cointegrated_asset_triplet,
                        None,
                        None,
                        50,
                        2.0,
                        0.4,
                        -2.5,
                        -0.4,
                    )
                    initial_trade = position_generator.initial_trade()
                    if pd.notnull(initial_trade):
                        initial_trade_list.append(initial_trade)
                        position_id = getattr(initial_trade, "position_id")
                        assets = getattr(initial_trade, "assets")
                        asset_ratios = getattr(initial_trade, "asset_ratios")
                        invested_amounts = getattr(initial_trade, "invested_amounts")
                        weights = getattr(initial_trade, "weights")
                        date = getattr(initial_trade, "date")

                        print(position_id)
                        print(assets)
                        print(asset_ratios)
                        print(invested_amounts)
                        print(weights)
                        print(date)

                        DataWriter(initial_trade).write_data_to_database()

                        super_position.add_class(initial_trade)

                aggregated_initial_trades = Positions.sum_instances(
                    initial_trade_list, parernt_id=parent_id
                )
                position_id = getattr(aggregated_initial_trades, "position_id")
                assets = getattr(aggregated_initial_trades, "assets")
                asset_ratios = getattr(aggregated_initial_trades, "asset_ratios")
                invested_amounts = getattr(
                    aggregated_initial_trades, "invested_amounts"
                )

            # print(position_id)
            # print(assets)
            # print(asset_ratios)
            # print(invested_amounts)
            # print(weights)

            else:
                cointegrated_assets_list = list(
                    getattr(aggregated_initial_trades, "assets")
                )

                classes = super_position.get_classes()

                for current_class in range(len(classes)):
                    cointegrated_asset_triplet = getattr(
                        classes[current_class], "assets"
                    )
                    weights = getattr(classes[current_class], "weights")
                    asset_ratios = getattr(classes[current_class], "asset_ratios")
                    z_score_calculator = ZScoreCalculator(
                        time_series_matrix[0 : 500 + i - 1],
                        list([cointegrated_asset_triplet, weights]),
                    )
                    z_score_spread = z_score_calculator.run()
                    position_generator = PositionGenerator(
                        time_series_matrix[0 : 500 + i - 1],
                        z_score_spread,
                        cointegrated_asset_triplet,
                        asset_ratios,
                        position_id,
                        50,
                        2.0,
                        0.5,
                        -2.5,
                        -1.0,
                    )

                    intermittent_trade = position_generator.intermittent_trade()

                    if pd.notnull(intermittent_trade):
                        position_id = getattr(intermittent_trade, "position_id")
                        assets = getattr(intermittent_trade, "assets")
                        asset_ratios = getattr(intermittent_trade, "asset_ratios")
                        date = getattr(intermittent_trade, "date")
                        invested_amounts = getattr(
                            intermittent_trade, "invested_amounts"
                        )
                        print(i)
                        print(position_id)
                        print(assets)
                        print(asset_ratios)
                        print(invested_amounts)
                        print(date)

                        DataWriter(intermittent_trade).write_data_to_database()

                        super_position.remove_class(classes[current_class])

        # data_writer_class = DataWriter()
        # stored_positions = data_writer_class.write_data_to_database()
        # print(stored_positions)


if __name__ == "__main__":
    data_instance = InputSeries(
        input_time_series_a=pd.Series([250, 255, 230], name="A_asset"),
        input_time_series_b=pd.Series([33, 30, 35], name="B_asset"),
        input_time_series_c=pd.Series([15, 18, 10], name="C_asset"),
    )

    trio_trader = TrioTrader(input_data=data_instance, run_cointegration=False)
    trio_trader.run()
