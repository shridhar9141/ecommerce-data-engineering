
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Analysis: Payment Method Analysis
-- Layer: Gold
-- Purpose: Analyse payment methods and transaction value
-- =====================================================

SELECT
    payment_type,

    -- Total payment transactions
    COUNT(*) AS total_transactions,

    -- Number of unique orders
    COUNT(DISTINCT order_id) AS total_orders,

    -- Total amount collected through each method
    ROUND(SUM(payment_value), 2) AS total_payment_value,

    -- Average payment transaction value
    ROUND(AVG(payment_value), 2) AS average_payment_value

FROM gold.fact_payments

GROUP BY
    payment_type

ORDER BY
    total_payment_value DESC;
