import json
import pandas as pd
from pathlib import Path


class SalesDataExtractor:
    """
    Hàm này chịu trách nhiệm đọc và lấy dữ liệu từ các một list các path
    """

    def __init__(self, paths: list):
        self.selected_file = paths # Lưu trữ đường dẫn
        self.rename_dict = {} # Lưu trữ từ điển đổi tên cột
        self.dtype_dict = None # Lưu trữ từ điển đổi dtype
        self.col_req_dict = {} # Lưu trữ từ điển các cột / tên cột gốc để so sánh với file thô
        self.col_use = None # Lưu trữ các cột bắt buộc

        self.config_loader()
        
    def config_loader(self):
        """
        Đọc file config và trích xuất thông tin cần thiết
        """
        
        with open('configs/sales_data_config.json') as config_file:
            config_data = json.load(config_file)
        
        # Dict dùng để phát hiện cột chưa được map trong file dữ liệu thô
        for col_name, dict_data in config_data.items():
            if dict_data["use"]:
                self.col_req_dict[col_name] = dict_data["raw_name"]
            
        # Danh sách cột bắt buộc phải có (chỉ sử dụng các cột này)
        self.col_use = {
            col for dict_data in config_data.values() 
            for col in dict_data["raw_name"] if dict_data["use"]
        }

        # Từ điển đổi tên cột
        for col_name, dict_data in config_data.items():
            for col_raw_name in dict_data["raw_name"]:
                self.rename_dict[col_raw_name]=col_name

        # Từ điển đổi dtype
        self.dtype_dict = {col: dict_data["dtype"] for col, dict_data in config_data.items() if dict_data["use"] }
        
    def read_excel(self):
        """
        Đọc và xử lí dữ liệu của các file trong list self.selected_file
        """

        completed_dfs = []
        has_error = False # Đánh dấu batch này có file bị lỗi không
        not_mapped_columns = [] # Lưu trữ danh sách các cột chưa được map

        if self.selected_file:
            for file in self.selected_file:
                # Đọc file
                print(f"Đang đọc file: {file.stem}")
                suffix = Path(file).suffix
                
                # Đọc file excel
                if suffix == ".xlsx":
                    try:
                        has_missing_col = False # Đánh dấu file có thiếu cột không
                        raw_col_list = pd.read_excel(file, nrows=0) # Lấy tên cột có trong file gốc

                        for col_name, raw_col_name_list in self.col_req_dict.items():
                            if not any(col in raw_col_name_list for col in raw_col_list): # Trường hợp không tìm thấy cột nào được map với tên cột trong file gốc
                                not_mapped_info = {col_name: file.stem}
                                not_mapped_columns.append(not_mapped_info)
                                has_missing_col = True

                        print(not_mapped_columns)

                        if has_missing_col:
                            has_error = True
                            continue

                        print("Đã map đủ tất cả các cột bắt buộc!")
                        df: pd.DataFrame = pd.read_excel(
                            file,
                            usecols=[col for col in self.col_use if col in raw_col_list], 
                            dtype="string", 
                            engine="openpyxl"
                        )

                        # Đổi tên cột
                        df = df.rename(columns=self.rename_dict)

                        # Chuyển định dạng
                        for col, dtype in self.dtype_dict.items():
                            if dtype == "numeric":
                                df[col] = pd.to_numeric(df[col], errors="coerce")

                            if dtype == "date":
                                df[col] = pd.to_datetime(df[col], errors="coerce", format="%d.%m.%Y")

                        if not df.empty:
                            completed_dfs.append(df)
                            print(completed_dfs)
                    except Exception as e:
                        print(e)
        
            if len(completed_dfs) == 0: 
                print("Không có kết quả")
                return None
            
        result = pd.concat(completed_dfs)
        return result, has_error

    def write_excel(self):
        pass