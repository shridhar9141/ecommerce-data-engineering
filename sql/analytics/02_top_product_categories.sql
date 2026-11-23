
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Analysis: Top 10 Product Categories
-- Layer: Gold
-- Purpose: Identify the highest-revenue categories
-- =====================================================

SELECT
    p.product_category_english,

    -- Total items sold in each category
    COUNT(f.order_item_key) AS total_items_sold,

    -- Number of unique orders
    COUNT(DISTINCT f.order_id) AS total_orders,

    -- Revenue from product prices
    ROUND(SUM(f.price), 2) AS product_revenue,

    -- Total shipping charges
    ROUND(SUM(f.freight_value), 2) AS total_freight,

    -- Product revenue + freight
    ROUND(
        SUM(f.price + f.freight_value), 2
    ) AS total_revenue

FROM gold.fact_order_items f

JOIN gold.dim_products p
    ON f.product_key = p.product_key

GROUP BY
    p.product_category_english

ORDER BY
    total_revenue DESC

LIMIT 10;
