from pathlib import Path
from sqlalchemy import create_engine 
from src.data_extractor import SalesDataExtractor
from src.database.client import DatabaseClient
from src.data_inspector import DebugViewInspector
from src.helper.result_writer import ResultWriter

BASE_PATH = Path().cwd()
file_paths = [file for file in Path("data/sales/daily").glob("*")]
sales_data_extractor = SalesDataExtractor(paths=file_paths)

engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")

data_client = DatabaseClient(engine)
view_debug = DebugViewInspector(
    engine=engine
)
result_writer = ResultWriter(BASE_PATH)

def sales_data_pipeline():
    result, has_error = sales_data_extractor.read_excel()
    if has_error:
        print("Có lỗi, đang dừng chương trình")
        return

    data_client.insert_dataframe(
        df=result,
        table_name="transactions",
        schema="staging"
    )

    # Kiểm tra các view debug có trả về lỗi hay không
    result, has_error = view_debug.view_inspector("staging")
    if has_error:
        print("Thiếu thông tin, vui lòng cập nhật")
        result_writer.write_result(result)
        return 
    
sales_data_pipeline()