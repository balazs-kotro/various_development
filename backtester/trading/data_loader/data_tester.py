from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd


if __name__ == "__main__":
    from sqlalchemy import create_engine, MetaData, Table, select

    engine = create_engine(
        "postgresql://postgres:asd@host.docker.internal:5432/postgres"
    )
    conn = engine.connect()

    metadata = MetaData()
    division = Table("assets", metadata, autoload_with=engine)

    query = division.select()

    exe = conn.execute(query)
    result = pd.DataFrame(exe.fetchall(), columns=division.columns.keys())
    print(result)
