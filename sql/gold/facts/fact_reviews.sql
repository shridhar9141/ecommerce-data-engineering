
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Layer: Gold
-- Table: fact_reviews
-- Purpose: Store customer reviews and ratings
-- Sources: staging.reviews, gold.dim_orders
-- Grain: One row per source review record
-- =====================================================

-- Step 1: Create reviews fact table

CREATE TABLE IF NOT EXISTS gold.fact_reviews (
    review_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_key BIGINT NOT NULL,
    review_id VARCHAR(50),
    order_id VARCHAR(50) NOT NULL,
    review_score INTEGER NOT NULL,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    duplicate_review_id_flag BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_order
        FOREIGN KEY (order_key)
        REFERENCES gold.dim_orders(order_key),

    CONSTRAINT chk_review_score
        CHECK (review_score BETWEEN 1 AND 5)
);

-- Step 2: Load review records

INSERT INTO gold.fact_reviews (
    order_key,
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date,
    review_answer_timestamp,
    duplicate_review_id_flag
)
SELECT
    o.order_key,
    r.review_id,
    r.order_id,
    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp,
    r.duplicate_review_id_flag

FROM staging.reviews r

JOIN gold.dim_orders o
    ON r.order_id = o.order_id;
