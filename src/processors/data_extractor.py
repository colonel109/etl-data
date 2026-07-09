import json
import pandas as pd
from pathlib import Path


class SalesDataExtractor:
    """
    Hàm này chịu trách nhiệm đọc và lấy dữ liệu từ các một list các path
    """

    def __init__(self, paths: list):
        self.selected_file = [Path(path) for path in paths] # Lưu trữ đường dẫn
        self.rename_dict = {} # Lưu trữ từ điển đổi tên cột
        self.dtype_dict = None # Lưu trữ từ điển đổi dtype
        self.col_req_dict = {} # Lưu trữ từ điển các cột / tên cột gốc để so sánh với file thô
        self.col_exclusive_dict = None # Lưu trữ các tên cột
        self.col_use = None # Lưu trữ các cột bắt buộc

        self.config_loader()
        
    def config_loader(self):
        """
        Đọc file config và trích xuất thông tin cần thiết
        """
        
        with open('configs/sales_data_config.json') as config_file:
            config_data: dict = json.load(config_file)
        
        # Dict dùng để phát hiện cột chưa được map trong file dữ liệu thô
        self.col_req_dict = {
            col_name: data["raw_name"]
            for col_name, data in config_data.items()
        }

        # Dict dùng để bỏ qua các cột chỉ nằm ở một loại file
        self.col_exclusive_dict = {
            col_name: data["exclusive"]
            for col_name, data in config_data.items() if data.get("exclusive")
        }
            
        # Dict chứa cột bắt buộc phải có (chỉ sử dụng các cột này)
        self.col_use = {
            col for dict_data in config_data.values() 
            for col in dict_data["raw_name"]
        }

        # Từ điển đổi tên cột
        self.rename_dict = {
            raw_name: new_col_name 
            for new_col_name, data in config_data.items()
            for raw_name in data["raw_name"] 
        }

        # Từ điển đổi dtype
        self.dtype_dict = {col: dict_data["dtype"] for col, dict_data in config_data.items()}
        
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
                file_name = file.stem
                suffix = Path(file).suffix

                file_type = self.check_file_type(file_name)
                
                # Đọc file excel
                if suffix == ".xlsx" and file_type:
                    try:
                        has_missing_col = False # Đánh dấu file có thiếu cột không
                        raw_col_list = pd.read_excel(file, nrows=0).columns.tolist() # Lấy tên cột có trong file gốc

                        for col_name, raw_col_name_list in self.col_req_dict.items():
                            # Trường hợp thiếu cột không nằm trong loại file order / ar_invoice
                            col_exclusive_compare = self.col_exclusive_dict.get(col_name)
                            if col_exclusive_compare and col_exclusive_compare != file_type:
                                continue 
                            
                            # Trường hợp không tìm thấy cột nào được map với tên cột trong file gốc
                            if not any(col in raw_col_name_list for col in raw_col_list): 
                                not_mapped_info = {col_name: file.stem}
                                not_mapped_columns.append(not_mapped_info)
                                has_missing_col = True
                                
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

                        # Drop dòng trống
                        df = df.dropna(subset=['business_partner_code'])

                        # Chuyển định dạng
                        for col, dtype in self.dtype_dict.items():
                            if col in df.columns:
                                if dtype == "numeric":
                                    df[col] = pd.to_numeric(df[col], errors="coerce")

                                if dtype == "date":
                                    df[col] = pd.to_datetime(df[col], errors="coerce", format="%d.%m.%Y")

                        if not df.empty:
                            df["source_file"] = file_name
                            df["scenario"] = file_type
                            completed_dfs.append(df)
                    except Exception as e:
                        print(e)
        
            if len(completed_dfs) == 0: 
                print("Không có kết quả")
                return None, has_error
            
        result = pd.concat(completed_dfs, ignore_index=True)
        return result, has_error
    
    def check_file_type(self, file_name):
        file_name_lower = file_name.lower()
        # Value của dict này cần quy định chính xác với value trong configs/sales_data_config.json
        dict_data= {
            "ar_invoice": ["ar", "invoice"],
            "order": ["order", "or"] 
        }

        for file_type, kw_list in dict_data.items():
            if any(kw in file_name_lower for kw in kw_list):
                return file_type
        return None