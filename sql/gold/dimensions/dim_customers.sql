
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: dim_customers
-- Purpose: Store unique customer information
-- Source: staging.customers
-- =====================================================

-- Step 1: Create customer dimension

CREATE TABLE IF NOT EXISTS gold.dim_customers (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL UNIQUE,
    inconsistent_location_flag BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Load unique customers

INSERT INTO gold.dim_customers (
    customer_unique_id,
    inconsistent_location_flag
)
SELECT
    customer_unique_id,
    BOOL_OR(inconsistent_location_flag)
FROM staging.customers
GROUP BY customer_unique_id

ON CONFLICT (customer_unique_id)
DO UPDATE SET
    inconsistent_location_flag =
        EXCLUDED.inconsistent_location_flag;
