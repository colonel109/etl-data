from pathlib import Path
from sqlalchemy import create_engine, text 
from src.data_extractor import SalesDataExtractor
from src.database.client import DatabaseClient
from src.data_inspector import DebugViewInspector
from src.helper.result_writer import ResultWriter

BASE_PATH = Path().cwd()
file_paths = [file for file in Path("data/sales/daily").glob("*")]
sales_data_extractor = SalesDataExtractor(paths=file_paths)

engine = create_engine("postgresql+psycopg://postgres:duong1234@localhost:5432/daesang_db_test")

data_client = DatabaseClient(engine)
view_debug = DebugViewInspector(
    engine=engine
)
result_writer = ResultWriter(BASE_PATH)

def sales_data_pipeline():
    result, has_error = sales_data_extractor.read_excel()
    if has_error:
        print("Có lỗi, đang dừng chương trình")
        return

    data_client.insert_dataframe(
        df=result,
        table_name="transactions",
        schema="staging"
    )

    # Kiểm tra các view debug có trả về lỗi hay không
    result, has_error = view_debug.view_inspector("staging")
    if has_error:
        print("Thiếu thông tin, vui lòng cập nhật")
        result_writer.write_result(result)
        return 
    
with engine.connect() as conn:
    conn.execute(
        text("""
        INSERT INTO main.transactions (
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
            COALESCE(bp.business_partner_key, 0) AS business_partner_key,
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
        LEFT JOIN main.business_partner bp 
            ON t.business_partner_code = bp.business_partner_code 
           AND (t.posting_date >= bp.valid_from AND (t.posting_date < bp.valid_to OR bp.valid_to IS NULL))
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
        """)
    )
    conn.commit()

sales_data_pipeline()