
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: dim_products
-- Purpose: Store product and category information
-- Sources: staging.products, staging.category_translation
-- =====================================================

-- Step 1: Create product dimension

CREATE TABLE IF NOT EXISTS gold.dim_products (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_category_name VARCHAR(100),
    product_category_english VARCHAR(100),
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Load product data with category translation

INSERT INTO gold.dim_products (
    product_id,
    product_category_name,
    product_category_english,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
SELECT
    p.product_id,
    p.product_category_name,

    -- Use original category when translation is unavailable
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name
    ),

    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm

FROM staging.products p

LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name

ON CONFLICT (product_id)
DO UPDATE SET
    product_category_name = EXCLUDED.product_category_name,
    product_category_english = EXCLUDED.product_category_english,
    product_name_length = EXCLUDED.product_name_length,
    product_description_length = EXCLUDED.product_description_length,
    product_photos_qty = EXCLUDED.product_photos_qty,
    product_weight_g = EXCLUDED.product_weight_g,
    product_length_cm = EXCLUDED.product_length_cm,
    product_height_cm = EXCLUDED.product_height_cm,
    product_width_cm = EXCLUDED.product_width_cm;
