from pathlib import Path
from sqlalchemy import create_engine 
from src.processors.data_extractor import SalesDataExtractor
from src.database.client import DatabaseClient

file_paths = [file for file in Path("data/sales/daily").glob("*")]
sales_data_extractor = SalesDataExtractor(paths=file_paths)

engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")

data_client = DatabaseClient(engine)

def process_and_import():
    result, has_error = sales_data_extractor.read_excel()
    if has_error:
        print("Có lỗi, đang dừng chương trình")
        return

    data_client.insert_dataframe(
        df=result,
        table_name="transactions",
        schema="staging",
    )

process_and_import()