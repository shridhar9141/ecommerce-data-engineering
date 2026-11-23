
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: sellers
-- Source: Olist sellers dataset
-- Purpose: Store cleaned seller records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.sellers (
    seller_id VARCHAR(50),
    seller_zip_code_prefix VARCHAR(10),
    seller_city TEXT,
    seller_state VARCHAR(5)
);
