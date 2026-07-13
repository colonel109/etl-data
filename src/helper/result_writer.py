import pandas as pd
from pathlib import Path

class ResultWriter:
    """
    Class này nhận một list các dict có dạng {"tên sheet": "dataframe"} và ghi vào dataframe
    """
    
    def __init__(self, base_path):
        self.base_path: Path = base_path

    def write_result(self, data):
        with pd.ExcelWriter(Path(self.base_path / "error_result.xlsx")) as writer:
            for sheet_name, dataframe in data.items():
                dataframe.to_excel(
                    excel_writer=writer,
                    sheet_name=sheet_name,
                    index=False 
                )