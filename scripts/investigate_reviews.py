
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_order_reviews_dataset.csv")

df = pd.read_csv(file_path)

print("========== REVIEWS INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Exact duplicate records
print("\nExact duplicate records:", df.duplicated().sum())

# Duplicate review IDs
print("\nDuplicate review IDs:", df["review_id"].duplicated().sum())

# Review score distribution
print("\nReview score distribution:")
print(df["review_score"].value_counts().sort_index())

# Check invalid review scores
print("\nInvalid review scores:")
print(
    df[
        ~df["review_score"].between(1, 5)
    ][["review_id", "review_score"]]
)

# Review comment lengths
print("\nReview comment title lengths:")
print(df["review_comment_title"].str.len().describe())

print("\nReview comment message lengths:")
print(df["review_comment_message"].str.len().describe())

# Review creation and answer timestamps
print("\nReview timestamp data types:")
print(df[["review_creation_date", "review_answer_timestamp"]].dtypes)
