CREATE OR REPLACE VIEW staging.debug_business_partner_pl
AS WITH distinct_bp AS (
         SELECT DISTINCT profit_and_loss.business_partner_code,
            profit_and_loss.business_partner_name
           FROM staging.profit_and_loss
          WHERE profit_and_loss.business_partner_code IS NOT NULL 
        ), curent_bp AS (
         SELECT DISTINCT business_partner.business_partner_code
           FROM main.business_partner
        )
 SELECT db.business_partner_code,
    db.business_partner_name
   FROM distinct_bp db
     LEFT JOIN curent_bp r USING (business_partner_code)
  WHERE r.business_partner_code IS NULL;


CREATE OR REPLACE VIEW staging.debug_profit_center_pl
AS WITH distinct_profit_center AS (
         SELECT DISTINCT profit_and_loss.profit_center_code,
            profit_and_loss.profit_center_name
           FROM staging.profit_and_loss
          WHERE profit_and_loss.profit_center_code IS NOT NULL 
        )
 SELECT pc.profit_center_code,
    pc.profit_center_name
   FROM distinct_profit_center pc
     LEFT JOIN staging.profit_center_staging pcs ON pc.profit_center_code::text = pcs.raw_value::text
  WHERE pcs.raw_value IS NULL;



-- 2. Debug Document Type
CREATE OR REPLACE VIEW staging.debug_document_type AS
WITH distinct_doc_type AS (
    SELECT DISTINCT document_type_name 
    FROM staging.transactions
    WHERE document_type_name IS NOT NULL 
)
SELECT dt.document_type_name
FROM distinct_doc_type dt
LEFT JOIN staging.document_type_staging dts ON dt.document_type_name = dts.raw_value
WHERE dts.raw_value IS NULL;


-- 3. Debug Cost Center
CREATE OR REPLACE VIEW staging.debug_cost_center AS
WITH distinct_cost_center AS (
    SELECT DISTINCT cost_center_code 
    FROM staging.transactions
    WHERE cost_center_code IS NOT NULL
)
SELECT cc.cost_center_code
FROM distinct_cost_center cc
LEFT JOIN staging.cost_center_staging ccs ON cc.cost_center_code = ccs.raw_value
WHERE ccs.raw_value IS NULL;


CREATE OR REPLACE VIEW staging.debug_profit_center AS
WITH distinct_profit_center AS (
    SELECT DISTINCT profit_center_code 
    FROM staging.transactions
    WHERE profit_center_code IS NOT NULL 
)
SELECT pc.profit_center_code
FROM distinct_profit_center pc
LEFT JOIN staging.profit_center_staging pcs ON pc.profit_center_code = pcs.raw_value
WHERE pcs.raw_value IS NULL;


CREATE OR REPLACE VIEW staging.debug_warehouse AS
WITH distinct_warehouse AS (
    SELECT DISTINCT warehouse_code 
    FROM staging.transactions
    WHERE warehouse_code IS NOT NULL
)
SELECT w.warehouse_code
FROM distinct_warehouse w
LEFT JOIN staging.warehouse_staging ws ON w.warehouse_code = ws.raw_value
WHERE ws.raw_value IS NULL;


CREATE OR REPLACE VIEW staging.debug_return_type AS
WITH distinct_return_type AS (
    SELECT DISTINCT return_type_code 
    FROM staging.transactions
    WHERE return_type_code IS NOT NULL 
)
SELECT rt.return_type_code
FROM distinct_return_type rt
LEFT JOIN staging.return_type_staging rts ON rt.return_type_code = rts.raw_value
WHERE rts.raw_value IS NULL;


CREATE OR REPLACE VIEW staging.debug_uom AS
WITH distinct_uom AS (
    SELECT DISTINCT uom_name 
    FROM staging.transactions
    WHERE uom_name IS NOT NULL 
)
SELECT u.uom_name
FROM distinct_uom u
LEFT JOIN staging.uom_staging us ON u.uom_name = us.raw_value
WHERE us.raw_value IS NULL;


CREATE OR REPLACE VIEW staging.debug_product AS
WITH distinct_products AS (
    SELECT product_code AS raw_product_code FROM staging.transactions WHERE product_code IS NOT NULL
    UNION
    SELECT source_product_code AS raw_product_code FROM staging.transactions WHERE source_product_code IS NOT NULL
)
SELECT dp.raw_product_code
FROM distinct_products dp
LEFT JOIN main.product p ON dp.raw_product_code = p.product_code
WHERE p.product_code IS NULL;

CREATE OR REPLACE VIEW staging.debug_business_partner AS
WITH distinct_bp AS (
    SELECT DISTINCT business_partner_code FROM staging.transactions
)
SELECT db.business_partner_code
FROM distinct_bp db
LEFT JOIN main.business_partner bp ON db.business_partner_code = bp.business_partner_code 
                                  AND bp.is_current = true
WHERE bp.business_partner_code IS NULL;

CREATE MATERIALIZED VIEW main.view_unpivoted_transactions AS
SELECT
    t.business_partner_key,
    t.product_key,
    t.source_product_key,
    t.sell_type_key,
    t.warehouse_key,
    t.posting_date,
    u.metric_name,
    sum(u.value) AS value
FROM main.transactions t
JOIN main.business_partner bp USING (business_partner_key)
JOIN main.product p USING (product_key)
CROSS JOIN LATERAL (
    VALUES 
        ('weight', t.weight),
        ('uom_per_quantity', t.uom_per_quantity),
        ('uom_quantity', t.uom_quantity),
        ('quantity', t.quantity),
        ('quantity_packaging_uom', t.quantity_packaging_uom),
        ('box', t.box),
        ('base_price', t.base_price),
        ('discount_percent', t.discount_percent),
        ('discounted_price', t.discounted_price),
        ('discounted_price_tax', t.discounted_price_tax),
        ('sales_revenue', t.sales_revenue),
        ('sales_amount_fc', t.sales_amount_fc),
        ('tax_amount', t.tax_amount),
        ('tax_amount_fc', t.tax_amount_fc),
        ('sales_amount_tax', t.sales_amount_tax),
        ('sales_amount_fc_tax', t.sales_amount_fc_tax),
        ('return_quantity', t.return_quantity)
) AS u(metric_name, value)
WHERE 
    scenario_key = 1
    AND u.value <> 0 
    AND product_key <> 0
    AND (bp.team_key <> 0 AND p.product_category_key <> 0)
GROUP BY
    t.business_partner_key,
    t.product_key,
    t.source_product_key,
    t.sell_type_key,
    t.warehouse_key,
    t.posting_date,
    t.scenario_key,
    u.metric_name