
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: customer_records
-- Purpose: Map customer records to unique customers
-- Source: staging.customers, gold.dim_customers
-- =====================================================

-- Step 1: Create customer records mapping table

CREATE TABLE IF NOT EXISTS gold.customer_records (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_key BIGINT NOT NULL
        REFERENCES gold.dim_customers(customer_key),
    customer_zip_code_prefix VARCHAR(10),
    customer_city TEXT,
    customer_state VARCHAR(5)
);

-- Step 2: Load customer records

INSERT INTO gold.customer_records (
    customer_id,
    customer_key,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
SELECT
    s.customer_id,
    d.customer_key,
    s.customer_zip_code_prefix,
    s.customer_city,
    s.customer_state
FROM staging.customers s
JOIN gold.dim_customers d
    ON s.customer_unique_id = d.customer_unique_id

ON CONFLICT (customer_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    customer_zip_code_prefix = EXCLUDED.customer_zip_code_prefix,
    customer_city = EXCLUDED.customer_city,
    customer_state = EXCLUDED.customer_state;
