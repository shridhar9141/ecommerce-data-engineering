
import pandas as pd
from pathlib import Path


def clean_reviews(df):
    """
    Convert review data types, validate required fields,
    and flag duplicate review IDs without removing records.
    """

    df = df.copy()

    # Convert data types
    df["review_score"] = df["review_score"].astype("int64")

    df["review_creation_date"] = pd.to_datetime(
        df["review_creation_date"],
        errors="raise"
    )

    df["review_answer_timestamp"] = pd.to_datetime(
        df["review_answer_timestamp"],
        errors="raise"
    )

    # Flag all rows with duplicate review IDs
    df["duplicate_review_id_flag"] = df.duplicated(
        subset=["review_id"],
        keep=False
    )

    # Validate required fields
    if df["review_id"].isna().any():
        raise ValueError("Missing review IDs found")

    if df["order_id"].isna().any():
        raise ValueError("Missing order IDs found")

    if not df["review_score"].between(1, 5).all():
        raise ValueError("Review scores must be between 1 and 5")

    # Validate timestamps
    if df["review_creation_date"].isna().any():
        raise ValueError("Missing review creation dates found")

    if df["review_answer_timestamp"].isna().any():
        raise ValueError("Missing review answer timestamps found")

    return df


def main():
    input_path = Path("data/raw/olist_order_reviews_dataset.csv")
    output_path = Path("data/processed/reviews_cleaned.csv")

    print("========== REVIEWS CLEANING ==========")

    df = pd.read_csv(input_path)
    original_rows = len(df)

    cleaned_df = clean_reviews(df)

    print("\nOriginal rows:", original_rows)
    print("Final rows:", len(cleaned_df))

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    print("\nDuplicate review IDs:")
    print(cleaned_df["review_id"].duplicated().sum())

    print("\nRows flagged for duplicate review IDs:")
    print(cleaned_df["duplicate_review_id_flag"].sum())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)


if __name__ == "__main__":
    main()
