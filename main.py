from pathlib import Path
from sqlalchemy import create_engine
from src.data_processor import SalesDataProcessor
from src.database.controller import DatabaseController
from src.data_inspector import DebugViewInspector
from src.helper.result_writer import ResultWriter


class MainPipeline:
    def __init__(self, base_path, engine):
        self.base_path = base_path
        self.engine = engine
        self.database_controller = DatabaseController(self.engine)
        self.view_debugger = DebugViewInspector(self.engine)
        self.sales_data_processor= SalesDataProcessor(self.engine)
        self.result_writer = ResultWriter(base_path)
        
    def sales_data_pipeline(self, file_paths):
        """
        Pipeline xử lí dữ liệu bán hàng
        """
        
        result, has_error = self.sales_data_processor.read_excel(file_path_list=file_paths)
        if has_error:
            print("Có lỗi, đang dừng chương trình")
            return

        self.database_controller.insert_dataframe(
            df=result,
            table_name="transactions",
            schema="staging"
        )

        # Kiểm tra các view debug có trả về lỗi hay không
        result, has_error = self.view_debugger.view_inspector("staging")
        if has_error:
            print("Thiếu thông tin, vui lòng cập nhật")
            self.result_writer.write_result(result)
            return 
        
        self.sales_data_processor.main_table_importer()
        
main_pipeline = MainPipeline(
    base_path=Path().cwd(),
    engine=create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
)

main_pipeline.sales_data_pipeline(file_paths = [file for file in Path("data/sales/daily").glob("*")])