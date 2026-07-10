from sqlalchemy import inspect, create_engine, text
import pandas as pd
from pathlib import Path

class DebugViewInspector:
    """
    Kiểm tra xem các view debug trong bảng staging có dữ liệu không
    """
    def __init__(self, engine, base_path):
        self.engine = engine
        self.has_error = False
        self.base_path = base_path

    def view_inspector(self, schema_name):
        inspector = inspect(self.engine)

        view_names = inspector.get_view_names(schema=schema_name)
        
        # Lấy danh sách các view có lỗi
        view_has_error = []
        with self.engine.connect() as conn:
            for view in view_names:
                target_view = f"{schema_name}.{view}"
                stmt = text(f"SELECT COUNT(*) FROM {target_view}")
                row_count = (conn.execute(stmt)).scalar()

                if row_count == 0:
                    continue 

                view_has_error.append(target_view)
        
            print(view_has_error) 
            if not view_has_error:
                return
            
            for view in view_has_error:
                with pd.ExcelWriter(f"{Path(self.base_path/ "result")}.xlsx", engine="openpyxl") as writer:
                    self.has_error = True

                    stmt = text(f"SELECT * FROM {view}")
                    df = pd.read_sql_query(stmt, con=conn)

                    df.to_excel(
                        excel_writer=writer, 
                        sheet_name=view,
                        index=False
                    )