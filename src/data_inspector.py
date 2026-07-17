from sqlalchemy import inspect, text
import pandas as pd


class DebugViewInspector:
    """
    Kiểm tra xem các view debug trong bảng staging có dữ liệu không
    """
    def __init__(self, engine):
        self.engine = engine

    def view_inspector(self, schema_name: str, keyword: str = None):
        """
        Kiểm tra các view debug, trả về lỗi nếu có dữ liệu
        """
        
        inspector = inspect(self.engine)

        view_names = [
            view for view in
            inspector.get_view_names(schema=schema_name)
            if ("debug" in view and keyword in view)
        ]
        
        has_error = False
        view_has_error = []
        result: dict = {}
        with self.engine.connect() as conn:
            for view in view_names:
                target_view = f"{schema_name}.{view}"
                stmt = text(f"SELECT COUNT(*) FROM {target_view}")
                row_count = (conn.execute(stmt)).scalar()

                if row_count == 0:
                    continue 

                has_error=True
                view_has_error.append(target_view)
        
            if not view_has_error:
                print("Tất cả bảng đều được map foreign key")
                return {}, has_error
            
            for view in view_has_error:
                stmt = text(f"SELECT * FROM {view}")
                df = pd.read_sql_query(stmt, con=conn)
                result[view] = df 

            return result, has_error