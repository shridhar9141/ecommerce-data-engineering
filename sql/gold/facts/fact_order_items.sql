
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: fact_order_items
-- Purpose: Store order item sales transactions
-- Sources: staging.order_items and Gold dimensions
-- Grain: One row per order_id and order_item_id
-- =====================================================

-- Step 1: Create order items fact table

CREATE TABLE IF NOT EXISTS gold.fact_order_items (
    order_item_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    seller_key BIGINT NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    order_item_id INTEGER NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    freight_value NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_order_item
        UNIQUE (order_id, order_item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_key)
        REFERENCES gold.dim_orders(order_key),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_key)
        REFERENCES gold.dim_products(product_key),

    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_key)
        REFERENCES gold.dim_sellers(seller_key)
);

-- Step 2: Load order item transactions

INSERT INTO gold.fact_order_items (
    order_key,
    product_key,
    seller_key,
    order_id,
    order_item_id,
    price,
    freight_value
)
SELECT
    o.order_key,
    p.product_key,
    s.seller_key,
    oi.order_id,
    oi.order_item_id,
    oi.price,
    oi.freight_value

FROM staging.order_items oi

JOIN gold.dim_orders o
    ON oi.order_id = o.order_id

JOIN gold.dim_products p
    ON oi.product_id = p.product_id

JOIN gold.dim_sellers s
    ON oi.seller_id = s.seller_id

ON CONFLICT (order_id, order_item_id)
DO UPDATE SET
    order_key = EXCLUDED.order_key,
    product_key = EXCLUDED.product_key,
    seller_key = EXCLUDED.seller_key,
    price = EXCLUDED.price,
    freight_value = EXCLUDED.freight_value;
