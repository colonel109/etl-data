import pandas as pd
from pathlib import Path

class ResultWriter:
    """
    Class này nhận một list các dict có dạng {"tên sheet": "dataframe"} và ghi vào dataframe
    """
    
    def __init__(self, base_path):
        self.base_path: Path = base_path

    def write_result(self, data_list=None, data_single=None):
        """
        Hàm này phụ trách viết file excel từ dữ liệu được nhập vào
        - data_list: list các từ điển có dạng [{tên sheet: dataframe}, ....]
        - data_single: {tên sheet: {tên cột1: giá trị1, tên cột2: giá trị2}}
        """
        print(data_list)
        with pd.ExcelWriter(Path(self.base_path / "error_result.xlsx")) as writer:
            if data_list:
                for sheet_name, dataframe in data_list.items():
                    dataframe.to_excel(
                        excel_writer=writer,
                        sheet_name=sheet_name,
                        index=False 
                    )
            
            if data_single:
                print(data_single)
                for sheet_name, data in data_single.items():
                    df = pd.DataFrame(data)
                    df.to_excel(
                        excel_writer=writer,
                        sheet_name=sheet_name,
                        index=False
                    )