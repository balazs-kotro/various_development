from sqlalchemy import create_engine, MetaData, Table, select

class DataLoader:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def load_data_from_database(self) -> str:
        return "1 - DataLoader is called"

    def load_whole_table(self):
        from sqlalchemy import create_engine, MetaData, Table, select
        engine = create_engine('postgresql://postgres:asd@host.docker.internal:5432/postgres')
        connection = engine.connect() 

        metadata = MetaData()
        table_metadata= Table('assets', metadata, autoload_with=engine)

        execution = connection.execute(table_metadata.select())
        result = pd.DataFrame(execution.fetchall(), columns = table_metadata.columns.keys())
        conn.close()

        return result