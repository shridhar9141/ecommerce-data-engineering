
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: geolocation
-- Source: Olist geolocation dataset
-- Purpose: Store cleaned geolocation records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.geolocation (
    geolocation_zip_code_prefix VARCHAR(10),
    geolocation_lat NUMERIC,
    geolocation_lng NUMERIC,
    geolocation_city TEXT,
    geolocation_state VARCHAR(5)
);
