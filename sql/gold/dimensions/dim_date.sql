
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: dim_date
-- Purpose: Create a calendar dimension for time analysis
-- Source: staging.orders
-- =====================================================

-- Step 1: Create date dimension

CREATE TABLE IF NOT EXISTS gold.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INTEGER,
    day_name VARCHAR(15),
    day_of_week INTEGER,
    week_number INTEGER,
    month_number INTEGER,
    month_name VARCHAR(15),
    quarter_number INTEGER,
    year_number INTEGER,
    is_weekend BOOLEAN
);

-- Step 2: Generate calendar dates
-- Covers the minimum and maximum order purchase dates.

INSERT INTO gold.dim_date (
    date_key,
    full_date,
    day_number,
    day_name,
    day_of_week,
    week_number,
    month_number,
    month_name,
    quarter_number,
    year_number,
    is_weekend
)
SELECT
    TO_CHAR(calendar_date, 'YYYYMMDD')::INTEGER,
    calendar_date::DATE,
    EXTRACT(DAY FROM calendar_date)::INTEGER,
    TO_CHAR(calendar_date, 'Day'),
    EXTRACT(ISODOW FROM calendar_date)::INTEGER,
    EXTRACT(WEEK FROM calendar_date)::INTEGER,
    EXTRACT(MONTH FROM calendar_date)::INTEGER,
    TO_CHAR(calendar_date, 'Month'),
    EXTRACT(QUARTER FROM calendar_date)::INTEGER,
    EXTRACT(YEAR FROM calendar_date)::INTEGER,
    EXTRACT(ISODOW FROM calendar_date) IN (6, 7)

FROM GENERATE_SERIES(
    (
        SELECT MIN(order_purchase_timestamp)::DATE
        FROM staging.orders
    ),
    (
        SELECT MAX(order_purchase_timestamp)::DATE
        FROM staging.orders
    ),
    INTERVAL '1 day'
) AS calendar_date

ON CONFLICT (date_key) DO NOTHING;

-- Step 3: Add purchase date key to orders

ALTER TABLE gold.dim_orders
ADD COLUMN IF NOT EXISTS purchase_date_key INTEGER;

-- Step 4: Map purchase timestamps to date keys

UPDATE gold.dim_orders o
SET purchase_date_key = d.date_key
FROM gold.dim_date d
WHERE o.order_purchase_timestamp::DATE = d.full_date;

-- Step 5: Add foreign key relationship

ALTER TABLE gold.dim_orders
ADD CONSTRAINT fk_orders_purchase_date
FOREIGN KEY (purchase_date_key)
REFERENCES gold.dim_date(date_key);
