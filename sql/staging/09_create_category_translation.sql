
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: category_translation
-- Source: Olist category translation dataset
-- Purpose: Store Portuguese-to-English category mappings
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.category_translation (
    product_category_name TEXT,
    product_category_name_english TEXT
);
