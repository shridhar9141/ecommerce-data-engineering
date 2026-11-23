
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Purpose: Create the staging schema
-- Database: PostgreSQL
-- =====================================================

-- Create staging schema if it does not exist

CREATE SCHEMA IF NOT EXISTS staging;

-- Verify schema creation

SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'staging';
