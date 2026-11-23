
-- =====================================================
-- Project: E-Commerce Data Engineering Platform
-- Analysis: Customer Review Analysis
-- Layer: Gold
-- Purpose: Analyse customer satisfaction by review score
-- =====================================================

SELECT
    review_score,

    -- Number of reviews for each score
    COUNT(*) AS total_reviews,

    -- Percentage of reviews for each score
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS review_percentage

FROM gold.fact_reviews

GROUP BY
    review_score

ORDER BY
    review_score;
