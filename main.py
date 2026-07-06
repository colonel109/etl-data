from pathlib import Path

from src.processors.data_extractor import SalesDataExtractor

file_paths = [file for file in Path("data/sales/daily").glob("*")]
sales_data_extractor = SalesDataExtractor(paths=file_paths)
sales_data_extractor.read_excel()