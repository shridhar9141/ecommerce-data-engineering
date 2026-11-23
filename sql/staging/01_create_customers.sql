
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: customers
-- Source: Olist customers dataset
-- Purpose: Store cleaned customer records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city TEXT,
    customer_state VARCHAR(5),
    inconsistent_location_flag BOOLEAN
);
