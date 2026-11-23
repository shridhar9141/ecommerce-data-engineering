
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Analysis: Monthly Sales Performance
-- Layer: Gold
-- Purpose: Analyse monthly orders, sales and freight
-- =====================================================

SELECT
    d.year_number,
    d.month_number,
    d.month_name,

    -- Number of unique orders
    COUNT(DISTINCT o.order_id) AS total_orders,

    -- Total items sold
    COUNT(f.order_item_key) AS total_items_sold,

    -- Total product sales
    SUM(f.price) AS product_sales,

    -- Total shipping charges
    SUM(f.freight_value) AS total_freight,

    -- Product sales + freight
    SUM(f.price + f.freight_value) AS total_sales

FROM gold.fact_order_items f

JOIN gold.dim_orders o
    ON f.order_key = o.order_key

JOIN gold.dim_date d
    ON o.purchase_date_key = d.date_key

GROUP BY
    d.year_number,
    d.month_number,
    d.month_name

ORDER BY
    d.year_number,
    d.month_number;
