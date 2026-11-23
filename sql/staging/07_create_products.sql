
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: products
-- Source: Olist products dataset
-- Purpose: Store cleaned product records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(50),
    product_category_name TEXT,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER
);
