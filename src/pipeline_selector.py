from pathlib import Path
import questionary


class PipelineSelector:
    """
    Chọn pipeline, file cần xử lí. Trả về danh sách các file, bảng cần import
    """

    def __init__(self, data_path: Path):
        self.data_path = data_path

    def select_pipeline(self):
        """
        Trả về tên pipeline, đường dẫn tới file và bảng đích để phục vụ việc import vào database
        """
        
        pipeline = {
            "Dữ liệu bán hàng": {
                "sales": {
                    "Dữ liệu tháng": {"AR Invoice": "ar_invoice", "Order": "order"},
                    "Dữ liệu ngày": "daily"
                }
            },
            "Dữ liệu lỗ lãi": "profit_and_loss",
        }

        # Lựa chọn pipeline
        pipeline_select = questionary.select(
            "Chọn pipeline cần xử lí:",
            choices=list(pipeline.keys())
        ).ask()

        selected_pipeline = pipeline[pipeline_select]
        target_pipeline = str(list(selected_pipeline.keys())[0]) # Lấy trên của pipeline đó

        # Chọn pipeline xử lí dữ liệu lỗ lãi
        if pipeline_select == "Dữ liệu lỗ lãi":
            
            path = self.data_path / selected_pipeline
            return path, selected_pipeline, target_table

        # Chọn piple xử lí dữ liệu bán hàng
        if pipeline_select == "Dữ liệu bán hàng":
            report_type_dict = selected_pipeline["sales"]
            sales_type = questionary.select(
                "Chọn loại bảng cần import:",
                choices=list(report_type_dict.keys())
            ).ask()

            file_type_dict = report_type_dict[sales_type]
            if sales_type == "Dữ liệu ngày":
                target_table = "transactions_daily" 
                path = [self.data_path / "sales" / file_type_dict] # chuyển sang list để khớp với đầu vào của hàm đọc file
                return path, target_pipeline, target_table 
            
            if sales_type == "Dữ liệu tháng":
                target_table = "transactions"
                file_type = questionary.checkbox(
                    "Chọn loại file cần xử lí",
                    choices = list(file_type_dict.keys())
                ).ask()

                path = [
                    self.data_path / "sales" / file_type_dict[item]
                    for item in file_type
                ]
                return path, target_pipeline, target_table
    
    def select_file(self, folder_paths: list | Path):
        """
        Lấy các path của các file được chọn từ danh sách folder được truyển vào
        """
        
        selected_files = []
        folders = folder_paths

        if folders:
            for folder in folders:
                if not folder.exists():
                    continue

                files = [f for f in folder.iterdir() if f.is_file()]

                if not files:
                    continue

                file_map = {f.name: f for f in files}

                chosen_names = questionary.checkbox(
                    f"Chọn các file trong thư mục [{folder.name}]:",
                    choices=list(file_map.keys()),
                ).ask()

                if chosen_names:
                    for name in chosen_names:
                        selected_files.append(file_map[name])
        
        return selected_files