from pathlib import Path
from sqlalchemy import create_engine
from src.data_processor import SalesDataProcessor
from src.database.controller import DatabaseController
from src.data_inspector import DebugViewInspector
from src.helper.result_writer import ResultWriter
from src.pipeline_selector import PipelineSelector


class MainPipeline:
    def __init__(self, base_path, data_path, engine):
        self.base_path = base_path
        self.engine = engine
        self.database_controller = DatabaseController(self.engine)
        self.view_debugger = DebugViewInspector(self.engine)
        self.sales_data_processor= SalesDataProcessor(self.engine)
        self.result_writer = ResultWriter(base_path)
        self.pipeline = PipelineSelector(data_path)
    
    def select_file_path(self):
        folder_list = self.pipeline.select_folder()
        file_paths = self.pipeline.select_file(folder_paths=folder_list)
        return file_paths
        
    def process_file(self, file_paths):
        """
        Xử lí dữ liệu và import vào database
        """
        
        result, has_error = self.sales_data_processor.read_excel(file_path_list=file_paths)
        if has_error:
            self.result_writer.write_result(data_single=result)
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
            self.result_writer.write_result(data_list=result)
            return 
        
        self.sales_data_processor.main_table_importer()

BASE_PATH = Path().cwd()
DATA_PATH = BASE_PATH / "data"

if __name__ == "__main__":    
    main_pipeline = MainPipeline(
        base_path=BASE_PATH,
        data_path=DATA_PATH,
        engine=create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
    )

    file_paths = main_pipeline.select_file_path()

    if file_paths:
        main_pipeline.process_file(
            file_paths=file_paths
        )