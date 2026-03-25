-- =========================================================
-- Online Retail Customer LTV Analysis (Starter SQL)
-- =========================================================
-- Purpose:
--   1) Clean transaction-level online retail data
--   2) Engineer revenue fields
--   3) Aggregate to customer-level LTV dataset
--   4) Produce KPI-ready outputs for Tableau
--
-- Notes:
--   - Adjust syntax for your SQL dialect if needed (PostgreSQL/Snowflake/BigQuery).
--   - Replace source table references with your environment tables.
-- =========================================================

-- 1) CLEAN TRANSACTIONS
WITH base_transactions AS (
    SELECT
        CAST(customer_id AS VARCHAR) AS customer_id,
        CAST(invoice_no AS VARCHAR) AS invoice_no,
        CAST(invoice_date AS TIMESTAMP) AS invoice_date,
        EXTRACT(YEAR FROM CAST(invoice_date AS TIMESTAMP)) AS invoice_year,
        CAST(quantity AS NUMERIC) AS quantity,
        CAST(unit_price AS NUMERIC) AS unit_price
    FROM data_raw.online_retail_transactions
),

cleaned_transactions AS (
    SELECT
        customer_id,
        invoice_no,
        invoice_date,
        invoice_year,
        quantity,
        unit_price,
        (quantity * unit_price) AS revenue,
        CASE
            WHEN customer_id IS NULL OR TRIM(customer_id) = '' THEN 0
            WHEN quantity <= 0 THEN 0
            WHEN unit_price <= 0 THEN 0
            -- Optional canceled invoice logic: uncomment if invoices are prefixed, e.g. 'C'
            -- WHEN invoice_no LIKE 'C%' THEN 0
            ELSE 1
        END AS is_valid_transaction
    FROM base_transactions
),

filtered_transactions AS (
    SELECT
        customer_id,
        invoice_no,
        invoice_date,
        invoice_year,
        quantity,
        unit_price,
        revenue
    FROM cleaned_transactions
    WHERE is_valid_transaction = 1
),

-- 2) CUSTOMER-LEVEL AGGREGATION
customer_ltv AS (
    SELECT
        customer_id,
        SUM(revenue) AS customer_ltv,
        COUNT(DISTINCT invoice_no) AS order_frequency,
        CASE
            WHEN COUNT(DISTINCT invoice_no) > 0
                THEN SUM(revenue) / COUNT(DISTINCT invoice_no)
            ELSE 0
        END AS avg_order_value,
        CASE
            WHEN COUNT(DISTINCT invoice_no) > 1 THEN 1
            ELSE 0
        END AS repeat_customer_flag
    FROM filtered_transactions
    GROUP BY customer_id
),

-- 3) LTV BINS FOR DISTRIBUTION
customer_ltv_binned AS (
    SELECT
        customer_id,
        customer_ltv,
        order_frequency,
        avg_order_value,
        repeat_customer_flag,
        CASE
            WHEN customer_ltv < 100 THEN '0-99'
            WHEN customer_ltv < 250 THEN '100-249'
            WHEN customer_ltv < 500 THEN '250-499'
            WHEN customer_ltv < 1000 THEN '500-999'
            WHEN customer_ltv < 2500 THEN '1000-2499'
            ELSE '2500+'
        END AS ltv_bin
    FROM customer_ltv
),

-- 4) KPI SNAPSHOT (OPTIONAL OUTPUT)
kpi_summary AS (
    SELECT
        COUNT(*) AS total_customers,
        AVG(customer_ltv) AS average_ltv,
        AVG(CASE WHEN repeat_customer_flag = 1 THEN customer_ltv END) AS average_repeat_ltv,
        SUM(CASE WHEN repeat_customer_flag = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS repeat_customer_pct
    FROM customer_ltv_binned
)

-- FINAL SELECTS
-- A) Use this for Tableau customer-level source
SELECT *
FROM customer_ltv_binned
ORDER BY customer_ltv DESC;

-- B) Optional: KPI table output
-- SELECT * FROM kpi_summary;
