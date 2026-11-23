
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: payments
-- Source: Olist payments dataset
-- Purpose: Store cleaned payment records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.payments (
    order_id VARCHAR(50),
    payment_sequential INTEGER,
    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2),
    zero_installments_flag BOOLEAN
);
