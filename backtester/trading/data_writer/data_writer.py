from sqlalchemy import create_engine, MetaData, Table, insert
from datetime import datetime
import pandas as pd


class DataWriter:
    def __init__(self, position_class) -> None:
        self.position_class = position_class

    def write_data_to_database(self):

        engine = create_engine("postgresql://postgres:asd@host.docker.internal:5432/postgres")
        conn = engine.connect()

        metadata = MetaData()
        existing_table = Table("profit_and_loss", metadata, autoload_with=engine)

        position_id = getattr(self.position_class, "position_id")
        assets = getattr(self.position_class, "assets")
        asset_ratios = getattr(self.position_class, "asset_ratios")
        invested_amounts = getattr(self.position_class, "invested_amounts")
        weights = getattr(self.position_class, "weights")
        date = getattr(self.position_class, "date")

        for i in range(len(assets)):
            data = {
                "parent_id": "parent_id_1",
                "trade_id": position_id,
                "date": date,
                "asset": assets[i],
                "direction": long_or_short(invested_amounts[i]),
                "asset_ratio": asset_ratios[i],
                "asset_weight": weights[i],
                "amount_invested": invested_amounts[i],
            }

            insert_stmt = insert(existing_table).values(**data)
            conn.execute(insert_stmt)
            conn.commit()

        conn.close()

def long_or_short(input_number: float):
    if input_number > 0:
        return "LONG"
    if input_number < 0:
        return "SHORT" 