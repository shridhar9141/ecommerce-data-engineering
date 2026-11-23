
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Staging
-- Table: reviews
-- Source: Olist reviews dataset
-- Purpose: Store cleaned customer review records
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score SMALLINT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    duplicate_review_id_flag BOOLEAN
);
