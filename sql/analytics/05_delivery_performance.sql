
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Analysis: Order Delivery Performance
-- Layer: Gold
-- Purpose: Measure delivery time and late deliveries
-- =====================================================

SELECT
    COUNT(*) AS total_orders,

    -- Orders with an actual delivery date
    COUNT(order_delivered_customer_date) AS delivered_orders,

    -- Average time from purchase to customer delivery
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_delivered_customer_date -
                order_purchase_timestamp
            )) / 86400
        )::NUMERIC,
        2
    ) AS avg_delivery_days,

    -- Orders delivered after the estimated date
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date >
              order_estimated_delivery_date
    ) AS late_deliveries

FROM gold.dim_orders

WHERE order_status = 'delivered';
