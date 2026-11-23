
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: dim_sellers
-- Purpose: Store seller information
-- Source: staging.sellers
-- =====================================================

-- Step 1: Create seller dimension

CREATE TABLE IF NOT EXISTS gold.dim_sellers (
    seller_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL UNIQUE,
    seller_zip_code_prefix VARCHAR(10),
    seller_city TEXT,
    seller_state VARCHAR(5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Load seller data

INSERT INTO gold.dim_sellers (
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM staging.sellers

ON CONFLICT (seller_id)
DO UPDATE SET
    seller_zip_code_prefix = EXCLUDED.seller_zip_code_prefix,
    seller_city = EXCLUDED.seller_city,
    seller_state = EXCLUDED.seller_state;
