import win32com.client as win32
from pathlib import Path
import time, questionary
from datetime import datetime
from shutil import copy 


class ReportRefresher:
    """
    Mở và làm mới dữ liệu trong các file mẫu (template_report) sau đó đổi tên và di chuyển sang thư mục kết quả (refreshed_report)
    """
    
    def __init__(self, report_folder: Path):
        self.template_path = Path(report_folder / "template_report") # Thư mục chứa file mẫu
        self.result_path = Path(report_folder / "refreshed_report") # Thư mục chứa file kết quả sau khi refresh file mẫu
    
    def run_process(self):
        file = self.file_selector()
        if file:
            self.process_file(
                selected_paths = file
            ) 
       
    def file_selector(self):
        """
        Chọn các file template, trả về một list các đường dẫn 
        """
        
        selected_report = questionary.checkbox(
            "Chọn báo cáo cần refresh dữ liệu",
            choices = [str(file) for file in self.template_path.glob("*.xlsx")]
        ).ask()

        if not selected_report:
            return
        
        # Lấy danh sách các file đã tạo trước đó trong thư mục result
        selected_file_name = [Path(file).stem for file in selected_report]
        refreshed_file_name = [file for file in self.result_path.glob("*")]

        if refreshed_file_name:
            for f in selected_file_name:
                for rf in refreshed_file_name:
                    if f in rf.stem:
                        print("Tìm thấy báo cáo cũ, đang xoá...")
                        rf.unlink()
        
        return selected_report

    def process_file(self, selected_paths: list):
        """
        Làm mới dữ liệu, đổi tên file theo ngày, giờ và di chuyển đến thư mục kết quả
        """
        
        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False 
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False
        excel.EnableEvents = False
        excel.AskToUpdateLinks = False

        for path in selected_paths:
            file_path = Path(path)
            if not file_path.is_file():
                print(f"Không tìm thấy đường dẫn {path}")
                continue

            print(f"Đang làm mới: {file_path}")

            # Làm mới dữ liệu
            try:
                wb = excel.Workbooks.Open(str(file_path))            

                time.sleep(3)  

                wb.RefreshAll()

                excel.CalculateUntilAsyncQueriesDone()
                wb.Save()

                # Lưu file với tên mới
                timestamp = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")

                dst = self.result_path / f"({timestamp}) {file_path.stem}{file_path.suffix}"
                copy(file_path, dst)
                print("Làm mới dữ liệu thành công!")

            except Exception as e:
                print(f"Xảy ra lỗi khi làm mới file: {e}")
                wb.Close()
                continue
        
        excel.Quit()