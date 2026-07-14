from pathlib import Path
import questionary

pipeline = {
    "Dữ liệu bán hàng": {
        "sales": {
            "Dữ liệu tháng": {"AR Invoice": "ar_invoice", "Order": "order"},
            "Dữ liệu ngày": "daily"
        }
    },
    "Dữ liệu lỗ lãi": "profit_and_loss",
}

class PipelineSelector:
    def __init__(self, base_path: Path, pipeline: dict):
        self.base_path = base_path
        self.pipeline = pipeline

    def pipeline_selector(self):
        # Lựa chọn pipeline
        pipeline_select = questionary.select(
            "Chọn self.pipeline cần xử lí:",
            choices=list(self.pipeline.keys())
        ).ask()

        print(self.pipeline[pipeline_select])

        selected_pipeline = self.pipeline[pipeline_select]

        # Chọn pipeline xử lí dữ liệu lỗ lãi
        if pipeline_select == "Dữ liệu lỗ lãi":
            return self.base_path / selected_pipeline

        # Chọn piple xử lí dữ liệu bán hàng
        if pipeline_select == "Dữ liệu bán hàng":
            report_type_dict = selected_pipeline["sales"]
            sales_type = questionary.select(
                "Chọn loại bảng cần import:",
                choices=list(report_type_dict.keys())
            ).ask()

            file_type_dict = report_type_dict[sales_type]
            if sales_type == "Dữ liệu ngày":
                return self.base_path / "sales" / file_type_dict
            
            if sales_type == "Dữ liệu tháng":
                file_type = questionary.checkbox(
                    "Chọn loại file cần xử lí",
                    choices = list(file_type_dict.keys())
                ).ask()

                path = [
                    self.base_path / "sales" / file_type_dict[item]
                    for item in file_type
                ]
                return path

pipeline_selector = PipelineSelector(
    base_path=Path(r"D:\Projects\etl-data\data"),
    pipeline=pipeline
)
path = pipeline_selector.pipeline_selector()
print(path)