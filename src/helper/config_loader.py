import json


class ConfigLoader:
    def __init__(self, config_path):
        with open(config_path, encoding="utf-8") as config_file:
            self.config_data: dict = json.load(config_file)

        self.col_req_dict = None
        self.col_exclusive_dict = None
        self.col_use = None
        self.rename_dict = None
        self.dtype_dict = None

        self.config_loader()

    def config_loader(self):

        self.col_req_dict = {
            col_name: data["raw_name"]
            for col_name, data in self.config_data.items()
        }

        self.col_exclusive_dict = {
            col_name: data["exclusive"]
            for col_name, data in self.config_data.items() if data.get("exclusive")
        }
            
        self.col_use = {
            col for dict_data in self.config_data.values() 
            for col in dict_data["raw_name"]
        }

        self.rename_dict = {
            raw_name: new_col_name 
            for new_col_name, data in self.config_data.items()
            for raw_name in data["raw_name"] 
        }

        self.dtype_dict = {col: dict_data["dtype"] for col, dict_data in self.config_data.items()}