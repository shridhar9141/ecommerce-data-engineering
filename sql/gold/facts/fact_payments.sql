
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: fact_payments
-- Purpose: Store customer payment transactions
-- Sources: staging.payments, gold.dim_orders
-- Grain: One row per order_id and payment_sequential
-- =====================================================

-- Step 1: Create payments fact table

CREATE TABLE IF NOT EXISTS gold.fact_payments (
    payment_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_key BIGINT NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2) NOT NULL,
    zero_installments_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_payment
        UNIQUE (order_id, payment_sequential),

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_key)
        REFERENCES gold.dim_orders(order_key)
);

-- Step 2: Load payment transactions

INSERT INTO gold.fact_payments (
    order_key,
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value,
    zero_installments_flag
)
SELECT
    o.order_key,
    p.order_id,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value,
    p.zero_installments_flag

FROM staging.payments p

JOIN gold.dim_orders o
    ON p.order_id = o.order_id

ON CONFLICT (order_id, payment_sequential)
DO UPDATE SET
    order_key = EXCLUDED.order_key,
    payment_type = EXCLUDED.payment_type,
    payment_installments = EXCLUDED.payment_installments,
    payment_value = EXCLUDED.payment_value,
    zero_installments_flag = EXCLUDED.zero_installments_flag;
