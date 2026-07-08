import pandas as pd
from sqlalchemy import create_engine, text
from src.database.structure import Base, TransactionsStaging


class DatabaseClient:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
    
    def create_table(self):
        with self.engine.begin() as conn:
            conn.execute(text("DROP SCHEMA IF EXISTS main CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS staging CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS temp_schema CASCADE;"))
            
            conn.execute(text("CREATE SCHEMA main;"))
            conn.execute(text("CREATE SCHEMA staging;"))
            conn.execute(text("CREATE SCHEMA temp_schema;"))

        Base.metadata.create_all(self.engine)

        with self.engine.begin() as conn:
            setup_sql = text("""
                -- Seed dữ liệu giá trị 0
                INSERT INTO main.dept VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.channel VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.branch VALUES (0, 'NA', 0, 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.team VALUES (0, 'NA', 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.cost_center VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.profit_center VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.kpi_group VALUES (0, 'NA', 'NA', 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.product_category VALUES (0, 'NA', '0') ON CONFLICT DO NOTHING;
                INSERT INTO main.market VALUES (0, 'NA', 'NA', 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.document_type VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.sell_type VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.uom VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.warehouse VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.province VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.return_type VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.business_partner_type VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.business_partner_group VALUES (0, 'NA', 0) ON CONFLICT DO NOTHING;
            """)
            conn.execute(setup_sql)

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