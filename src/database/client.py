import pandas as pd
from sqlalchemy import create_engine, text
from src.database.structure import Base, TransactionsStaging


class DatabaseClient:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
    
    def create_table(self):
        Base.metadata.create_all(
            bind=self.engine, 
            tables=[TransactionsStaging.__table__]
        )
        
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, schema: str, chunksize: int = 10000):
        if df.empty:
            return
        
        with self.engine.connect() as conn:
            sql = text("TRUNCATE TABLE staging.transactions RESTART IDENTITY")
            conn.execute(sql)
            conn.commit()

        df.to_sql(
            name=table_name,
            con=self.engine,
            schema=schema,
            if_exists="append",
            index=False,
            chunksize=chunksize,
            method=self._psql_insert_copy
        )
    
    @staticmethod
    def _psql_insert_copy(table, conn, keys, data_iter):
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            columns = ", ".join([f'"{k}"' for k in keys])
            table_name = f'"{table.schema}"."{table.name}"' if table.schema else f'"{table.name}"'
            with cur.copy(f"COPY {table_name} ({columns}) FROM STDIN") as copy:
                for row in data_iter:
                    copy.write_row(row)