import json
import pandas as pd
from pathlib import Path
from sqlalchemy import text


class SalesDataProcessor:
    """
    Hàm này chịu trách nhiệm đọc và lấy dữ liệu từ các một list các path
    """

    def __init__(self, engine):
        self.engine = engine
        
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
        
    def read_excel(self, file_path_list: list):
        """
        Đọc và xử lí dữ liệu của các file trong list các path được truyền vào 
        """

        completed_dfs = []
        has_error = False # Đánh dấu batch này có file bị lỗi không
        not_mapped_columns = [] # Lưu trữ danh sách các cột chưa được map

        if file_path_list:
            for file in file_path_list:
                # Đọc file
                file_name = file.stem
                suffix = Path(file).suffix

                file_type = self.check_file_type(file_name)
                
                # Đọc file excel
                print(f"Đang xử lí file {file_name}")
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
                                not_mapped_info = {
                                    "Tên file ": file.stem,
                                    "Tên cột chưa map": col_name
                                }
                                not_mapped_columns.append(not_mapped_info)
                                has_missing_col = True
                                
                        if has_missing_col:
                            has_error = True # Trả về lỗi chung, batch này sẽ không được import vào database
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
        
        if has_missing_col or has_error: 
            result = {"Cột còn thiếu": not_mapped_columns}
            return result, has_error
            
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
    
    def copy_to_main_table(self, target_table):
        """
        Lấy dữ liệu từ bảng staging trong database và import vào bảng đích
        """
        
        query = text(
            f"""
            INSERT INTO main.{target_table} (
                business_partner_key, product_key, source_product_key,
                document_type_key, sell_type_key,
                cost_center_key, profit_center_key,
                warehouse_key, return_type_key,
                uom_key, tax_key, posting_date, due_date,
                demand_date, final_delivery_date, document_no, tax_number,
                weight, uom_per_quantity, uom_quantity,
                quantity, quantity_packaging_uom, box,
                base_price, discount_percent, discounted_price,
                discounted_price_tax, sales_revenue, sales_amount_fc,
                tax_amount, tax_amount_fc, sales_amount_tax,
                sales_amount_fc_tax, return_quantity
            )
            SELECT
                business_partner_key,
                COALESCE(p.product_key, 0) AS product_key,
                COALESCE(pm.product_key, 0) AS source_product_key,
                COALESCE(dts.document_type_key, 0) AS document_type_key,
                COALESCE(sts.sell_type_key, 0) AS sell_type_key,
                COALESCE(ccs.cost_center_key, 0) AS cost_center_key,
                COALESCE(pcs.profit_center_key, 0) AS profit_center_key,
                COALESCE(ws.warehouse_key, 0) AS warehouse_key,
                COALESCE(rts.return_type_key, 0) AS return_type_key,
                COALESCE(us.uom_key, 0) AS uom_key,
                COALESCE(ts.tax_key, 0) AS tax_key,
                t.posting_date, t.due_date,
                t.demand_date, t.final_delivery_date,
                t.document_no, t.tax_number,
                t.weight, t.uom_per_quantity,
                t.uom_quantity, t.quantity,
                t.quantity_packaging_uom, t.box,
                t.base_price, t.discount_percent,
                t.discounted_price, t.discounted_price_tax,
                t.sales_revenue, t.sales_amount_fc,
                t.tax_amount, t.tax_amount_fc,
                t.sales_amount_tax, t.sales_amount_fc_tax,
                t.return_quantity
            FROM staging.transactions t
            JOIN main.business_partner bp 
                ON t.business_partner_code = bp.business_partner_code 
            AND (t.posting_date >= bp.valid_from AND (t.posting_date <= bp.valid_to OR bp.valid_to IS NULL))
            LEFT JOIN main.product p ON t.product_code = p.product_code 
            LEFT JOIN main.product pm ON t.source_product_code = pm.product_code
            LEFT JOIN staging.document_type_staging dts ON t.document_type_name = dts.raw_value
            LEFT JOIN staging.sell_type_staging sts ON t.sell_type_name = sts.raw_value
            LEFT JOIN staging.cost_center_staging ccs ON t.cost_center_code = ccs.raw_value
            LEFT JOIN staging.profit_center_staging pcs ON t.profit_center_code = pcs.raw_value
            LEFT JOIN staging.warehouse_staging ws ON t.warehouse_code = ws.raw_value
            LEFT JOIN staging.return_type_staging rts ON t.return_type_code = rts.raw_value
            LEFT JOIN staging.uom_staging us ON t.uom_name = us.raw_value
            LEFT JOIN staging.tax_staging ts ON t.tax_code = ts.raw_value;
            """
            )

        with self.engine.begin() as conn:
            conn.execute(query)