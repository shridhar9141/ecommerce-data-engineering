
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_order_reviews_dataset.csv")

df = pd.read_csv(file_path)

print("========== DUPLICATE REVIEW INVESTIGATION ==========")

# Find duplicated review IDs
duplicate_reviews = df[
    df.duplicated(subset=["review_id"], keep=False)
].sort_values("review_id")

print("\nTotal rows with duplicate review IDs:")
print(len(duplicate_reviews))

print("\nNumber of duplicated review IDs:")
print(duplicate_reviews["review_id"].nunique())

# Display sample duplicate records
print("\nSample duplicate review records:")
print(duplicate_reviews.head(20).to_string(index=False))

# Check whether duplicate review IDs belong to different orders
orders_per_review = (
    duplicate_reviews.groupby("review_id")["order_id"].nunique()
)

print("\nReview IDs associated with multiple orders:")
print((orders_per_review > 1).sum())

# Check duplicate order IDs
print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())

# Check whether duplicate IDs have different scores
scores_per_review = (
    duplicate_reviews.groupby("review_id")["review_score"].nunique()
)

print("\nReview IDs with different scores:")
print((scores_per_review > 1).sum())

# Check timestamp parsing
print("\nTimestamp conversion check:")

for column in ["review_creation_date", "review_answer_timestamp"]:
    converted = pd.to_datetime(df[column], errors="coerce")

    print(
        column,
        "| Invalid timestamps:",
        converted.isna().sum()
    )
