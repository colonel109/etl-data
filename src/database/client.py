import pandas as pd
from sqlalchemy import create_engine, text
from src.database.structure import Base, TransactionsStaging


class DatabaseClient:
    def __init__(self, engine):
        self.engine = engine 
    
    def create_table(self):
        with self.engine.begin() as conn:
            conn.execute(text("DROP SCHEMA IF EXISTS main CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS staging CASCADE;"))
            conn.execute(text("DROP SCHEMA IF EXISTS temp_schema CASCADE;"))
            
            conn.execute(text("CREATE SCHEMA main;"))
            conn.execute(text("CREATE SCHEMA staging;"))
            conn.execute(text("CREATE SCHEMA temp_schema;"))

        Base.metadata.create_all(self.engine)

        with self.engine.begin() as conn:
            setup_sql = text("""
                -- Seed dữ liệu giá trị 0
                INSERT INTO main.dept VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.channel VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.branch VALUES (0, 'NA', 0, 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.team VALUES (0, 'NA', 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.cost_center VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.profit_center VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.kpi_group VALUES (0, 'NA', 'NA', 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.product_category VALUES (0, 'NA', '0') ON CONFLICT DO NOTHING;
                INSERT INTO main.market VALUES (0, 'NA', 'NA', 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.document_type VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.sell_type VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.uom VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.warehouse VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.province VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.return_type VALUES (0, 'NA', 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.business_partner_type VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.business_partner_group VALUES (0, 'NA', 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.msg_group VALUES (0, 'NA', 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.ducviet_category_group VALUES (0, 'NA') ON CONFLICT DO NOTHING;
                INSERT INTO main.product VALUES (0, 'NA', 'NA', 'NA', 0, 0, 0, 0) ON CONFLICT DO NOTHING;
                INSERT INTO main.tax VALUES (0, 'NA') ON CONFLICT DO NOTHING;
            """)
            conn.execute(setup_sql)

        statements = [
                "CREATE EXTENSION IF NOT EXISTS postgres_fdw SCHEMA temp_schema;",
                
                """
                CREATE SERVER IF NOT EXISTS db_b_server
                FOREIGN DATA WRAPPER postgres_fdw
                OPTIONS (
                    host 'localhost',
                    port '5432',
                    dbname 'daesang_db'
                );
                """,
                
                """
                CREATE USER MAPPING IF NOT EXISTS FOR current_user
                SERVER db_b_server
                OPTIONS (
                    user 'postgres',
                    password 'duong1234'
                );
                """,
                
                "CREATE SCHEMA IF NOT EXISTS temp_schema;",
                "CREATE SCHEMA IF NOT EXISTS staging;",
                "CREATE SCHEMA IF NOT EXISTS main;",
                
                """
                IMPORT FOREIGN SCHEMA sales
                FROM SERVER db_b_server
                INTO temp_schema;
                """
            ]

        with self.engine.begin() as conn:
            for stmt in statements:
                conn.execute(text(stmt))
        
        with self.engine.begin() as conn:
            setup_sql = text("""
                INSERT INTO main.dept(dept_name)
                SELECT dept_name FROM temp_schema.dept
                WHERE dept_name ILIKE '%miền%';


                INSERT INTO main.channel(channel_name)
                SELECT channel_name FROM temp_schema.channel
                WHERE channel_key <> 0;

                --TRUNCATE TABLE main.branch RESTART IDENTITY CASCADE;

                INSERT INTO main.branch(branch_name, dept_key, channel_key)
                SELECT branch_name,
                CASE
                    WHEN branch_name ILIKE '%bắc%' THEN 1
                    WHEN branch_name ILIKE '%trung%' THEN 2
                    WHEN branch_name ILIKE '%nam%' THEN 3
                    ELSE 0
                END AS dept_key,
                CASE
                    WHEN branch_key = 0 THEN 0
                    WHEN branch_name ILIKE '%catering%' THEN 3
                    WHEN branch_name ILIKE '%đặc biệt%' THEN 1
                    ELSE 2
                END AS branch_key
                FROM temp_schema.branch 
                WHERE branch_name NOT ILIKE '%không%';

                INSERT INTO main.team(team_name, branch_key)
                WITH old_team_data AS (
                    SELECT 
                        team_name, t.branch_key, branch_name
                    FROM temp_schema.team t
                    LEFT JOIN temp_schema.branch b ON t.branch_key = b.branch_key 
                    WHERE branch_name NOT ILIKE '%không%'
                    ORDER BY team_name
                )
                SELECT 
                team_name, b.branch_key 
                FROM old_team_data otd
                LEFT JOIN main.branch b USING (branch_name)
                ORDER BY team_name;


                INSERT INTO main.province(province_name_old, province_name_new)
                SELECT province_name_old, province_name_new
                FROM temp_schema.province;

                INSERT INTO main.business_partner_type(bp_type_name)
                SELECT bp_type_name
                FROM temp_schema.business_partner_type
                WHERE bp_type_key <> 0;

                INSERT INTO main.business_partner_group(bp_group_name, bp_type_key)
                WITH temp_data AS (
                    SELECT 
                    bp_group_name,
                    bp_type_name
                    FROM temp_schema.business_partner_group
                    LEFT JOIN temp_schema.business_partner_type USING (bp_type_key)
                )
                SELECT bp_group_name, bp_type_key FROM temp_data
                LEFT JOIN main.business_partner_type USING (bp_type_name)
                WHERE bp_type_key IS NOT NULL
                AND bp_group_name NOT ILIKE '%không sử dụng%';

                INSERT INTO main.cost_center(cost_center_code, cost_center_name)
                SELECT cost_center_code, cost_center_name
                FROM temp_schema.cost_center;

                INSERT INTO main.profit_center (profit_center_code, profit_center_name)
                SELECT profit_center_code, profit_center_name
                FROM temp_schema.profit_center;

                INSERT INTO main.document_type (document_type_name)
                SELECT document_type_name
                FROM temp_schema.document_type;

                INSERT INTO main.market(market_type_name, country_name_eng, country_shortname_a2, country_name_vi)
                SELECT market_type, country_name_eng, country_shortname_a2, country_name_vi
                FROM temp_schema.market
                WHERE market_key <> 0
                ORDER BY market_type ASC;

                INSERT INTO main.kpi_group(sub_kpi_1, sub_kpi_2, sub_kpi_3, sub_kpi_0)
                SELECT sub_kpi_1, sub_kpi_2, sub_kpi_3, sub_kpi_0
                FROM temp_schema.kpi_group
                WHERE sub_kpi_1 NOT ILIKE '%không sử dụng%';

                INSERT INTO main.product_category(product_category_name, kpi_group_key)
                WITH category_data AS (
                SELECT
                product_category_name,
                sub_kpi_3
                FROM temp_schema.product_category
                LEFT JOIN temp_schema.kpi_group USING (kpi_group_key)
                )
                SELECT product_category_name, kg.kpi_group_key FROM category_data
                INNER JOIN main.kpi_group kg USING (sub_kpi_3)
                ORDER BY product_category_name;

                INSERT INTO main.return_type(return_type_code, return_type_name)
                SELECT return_code, return_type_name
                FROM temp_schema.return_type;

                INSERT INTO main.sell_type(sell_type_name)
                SELECT sell_type_name FROM temp_schema.sell_type;

                INSERT INTO main.warehouse(warehouse_code, warehouse_name)
                SELECT warehouse_code, warehouse_rname FROM temp_schema.warehouse;

                INSERT INTO main.ducviet_category_group (ducviet_category_name)
                SELECT ducviet_category_name
                FROM temp_schema.ducviet_category;

                INSERT INTO main.msg_group(msg_group_name, msg_group_size)
                SELECT msg_group_name, msg_size_group
                FROM temp_schema.msg_group;

                INSERT INTO main.uom(uom_name)
                SELECT sales_uom_name FROM temp_schema.sales_uom;

                INSERT INTO main.tax(tax_code)
                SELECT tax_code FROM temp_schema.tax_code;

                INSERT INTO main.product (product_code, product_name, product_name_eng, product_category_key, market_key, msg_group_key, ducviet_category_key)
                WITH data_temp AS (
                SELECT 
                product_code,
                product_name,
                product_name_eng,
                product_category_name,
                m.country_name_eng,
                mg.msg_group_name,
                dc.ducviet_category_name
                FROM temp_schema.product p
                LEFT JOIN temp_schema.product_category pc USING (product_category_key)
                LEFT JOIN temp_schema.market m USING (market_key)
                LEFT JOIN temp_schema.msg_group mg USING(msg_group_key)
                LEFT JOIN temp_schema.ducviet_category dc USING (ducviet_category_key)
                )
                SELECT 
                product_code,
                product_name,
                product_name_eng,
                COALESCE(pc.product_category_key, 0) AS product_category_key,
                COALESCE(m.market_key, 0) AS market_key,
                COALESCE(mg.msg_group_key, 0) AS msg_group_key,
                COALESCE(dcg.ducviet_category_key, 0) AS ducviet_category_key
                FROM data_temp 
                LEFT JOIN main.product_category pc USING (product_category_name)
                LEFT JOIN main.market m USING (country_name_eng)
                LEFT JOIN main.ducviet_category_group dcg USING (ducviet_category_name)
                LEFT JOIN main.msg_group mg USING (msg_group_name);

                SELECT * FROM temp_schema.business_partner;

                INSERT INTO main.business_partner(business_partner_code, business_partner_name, bp_group_key, team_key, province_key,
                creation_date, import_date, valid_from, valid_to, is_current)
                WITH temp_data AS (
                    SELECT
                        bp.business_partner_code,
                        bp.business_partner_name,
                        bpg.bp_group_name,
                        t.team_name,
                        p.province_name_old,
                        bp.creation_date,
                        bp.import_date,
                        bp.valid_from,
                        bp.valid_to,
                        bp.is_current
                    FROM temp_schema.business_partner bp
                    LEFT JOIN temp_schema.business_partner_group bpg USING (bp_group_key)
                    LEFT JOIN temp_schema.team t USING (team_key)
                    LEFT JOIN temp_schema.province p USING (province_key)
                )
                SELECT 
                    td.business_partner_code,
                    td.business_partner_name,
                    COALESCE(bpg.bp_group_key, 0) AS bp_group_key,
                    COALESCE(t.team_key, 0) AS team_key,
                    COALESCE(p.province_key, 0) AS province_key,
                    td.creation_date,
                    NOW()::date,
                    td.valid_from,
                    td.valid_to,
                    td.is_current
                FROM temp_data td
                LEFT JOIN main.business_partner_group bpg ON td.bp_group_name = bpg.bp_group_name
                LEFT JOIN main.team t ON td.team_name = t.team_name
                LEFT JOIN main.province p ON td.province_name_old = p.province_name_old;
            """)
            conn.execute(setup_sql)        

    def insert_dataframe(self, df: pd.DataFrame, table_name: str, schema: str, chunksize: int = 10000):
        if df.empty:
            return
        
        with self.engine.connect() as conn:
            sql = text("TRUNCATE TABLE staging.transactions RESTART IDENTITY")
            conn.execute(sql)
            conn.commit()

        df.to_sql(
            name=table_name,
            con=self.engine,
            schema=schema,
            if_exists="append",
            index=False,
            chunksize=chunksize,
            method=self._psql_insert_copy
        )
    
    @staticmethod
    def _psql_insert_copy(table, conn, keys, data_iter):
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            columns = ", ".join([f'"{k}"' for k in keys])
            table_name = f'"{table.schema}"."{table.name}"' if table.schema else f'"{table.name}"'
            with cur.copy(f"COPY {table_name} ({columns}) FROM STDIN") as copy:
                for row in data_iter:
                    copy.write_row(row)