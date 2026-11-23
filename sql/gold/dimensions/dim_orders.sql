
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: dim_orders
-- Purpose: Store order details and customer relationship
-- Source: staging.orders, gold.customer_records
-- =====================================================

-- Step 1: Create order dimension

CREATE TABLE IF NOT EXISTS gold.dim_orders (
    order_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,
    customer_key BIGINT NOT NULL,
    order_status VARCHAR(30),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    delivered_missing_delivery_date BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_key)
        REFERENCES gold.dim_customers(customer_key)
);

-- Step 2: Load order data

INSERT INTO gold.dim_orders (
    order_id,
    customer_key,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    delivered_missing_delivery_date
)
SELECT
    o.order_id,
    cr.customer_key,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    o.delivered_missing_delivery_date

FROM staging.orders o

JOIN gold.customer_records cr
    ON o.customer_id = cr.customer_id

ON CONFLICT (order_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    order_status = EXCLUDED.order_status,
    order_purchase_timestamp = EXCLUDED.order_purchase_timestamp,
    order_approved_at = EXCLUDED.order_approved_at,
    order_delivered_carrier_date = EXCLUDED.order_delivered_carrier_date,
    order_delivered_customer_date = EXCLUDED.order_delivered_customer_date,
    order_estimated_delivery_date = EXCLUDED.order_estimated_delivery_date,
    delivered_missing_delivery_date =
        EXCLUDED.delivered_missing_delivery_date;
