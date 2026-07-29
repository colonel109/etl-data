from pathlib import Path
from sqlalchemy import create_engine
from src.data_processor import SalesDataProcessor, ProfitAndLossProcessor
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
        self.pl_data_processor = ProfitAndLossProcessor(self.engine)
        self.result_writer = ResultWriter(base_path)
        self.pipeline = PipelineSelector(data_path)

    def process_data(self):
        """
        Chọn file, xử lí dữ liệu, import vào database và làm mới dữ liệu của view theo từng pipeline
        """
        # Lấy các file path, tên pipeline, bảng đích (đối với pipeline dữ liệu bán hàng)
        path, selected_pipeline, target_table  = self.pipeline.select_pipeline()
        file_paths = self.pipeline.select_file(path=path)

        if not file_paths:
            return

        if selected_pipeline == "sales": 
            # Đọc dữ liệu và viết lỗi liên quan đến đọc file
            result, has_error = self.sales_data_processor.read_excel(file_path_list=file_paths)
            if has_error:
                self.result_writer.write_result(data_single=result)
                print("Có lỗi, đang dừng chương trình")
                return
            
            # Xoá dữ liệu cũ ở bảng transactions staging
            self.database_controller.truncate_table(
                target_table="transactions",
                target_schema="staging"
            )

            # Luôn xoá bảng daily để tránh việc dup dữ liệu khi import dữ liệu tháng 
            self.database_controller.truncate_table(
                target_table="transactions_daily",
                target_schema="main"
            )

            # Insert data vào staging
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
            
            # Copy dữ liệu từ staging vào bảng đích (daily và monthy đối với dữ liệu bán hàng)
            self.sales_data_processor.copy_to_main_table(target_table)

            # Làm mới dữ liệu của view
            self.database_controller.refresh_view(
                target_schema="main",
                target_view="view_unpivoted_transactions"
            )
        
        elif selected_pipeline == "profit_and_loss":
            # Đọc dữ liệu và viết lỗi liên quan đến đọc file
            result, has_error = self.pl_data_processor.read_excel(file_path_list=file_paths)
            if has_error:
                self.result_writer.write_result(data_single=result)
                print("Có lỗi, đang dừng chương trình")
                return
            
            # Xoá dữ liệu cũ ở bảng transactions staging
            self.database_controller.truncate_table(
                target_table="profit_and_loss",
                target_schema="staging"
            )

            # Insert data vào staging
            self.database_controller.insert_dataframe(
                df=result,
                table_name="profit_and_loss",
                schema="staging"
            )

            # Kiểm tra các view debug có trả về lỗi hay không
            result, has_error = self.view_debugger.view_inspector("staging", "_pl") # Chỉ lọc các view có hậu tố _pl
            if has_error:
                print("Thiếu thông tin, vui lòng cập nhật")
                self.result_writer.write_result(data_list=result)
                return 
            
            # Copy dữ liệu từ staging vào bảng chính, đối với pl chỉ có 1 bảng đích
            self.pl_data_processor.copy_to_main_table()

            # Làm mới dữ liệu của view
            self.database_controller.refresh_view(
                target_schema="main",
                target_view="view_unpivoted_transactions"
            )


BASE_PATH = Path().cwd()
DATA_PATH = BASE_PATH / "data"

if __name__ == "__main__":    
    main_pipeline = MainPipeline(
        base_path=BASE_PATH,
        data_path=DATA_PATH,
        engine=create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")
    )

    main_pipeline.process_data()