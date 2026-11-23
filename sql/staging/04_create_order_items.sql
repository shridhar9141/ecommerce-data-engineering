
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: order_items
-- Source: Olist order_items dataset
-- Purpose: Store cleaned order item records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.order_items (
    order_id VARCHAR(50),
    order_item_id INTEGER,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(12,2),
    freight_value NUMERIC(12,2)
);
