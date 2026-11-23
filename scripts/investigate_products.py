
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_products_dataset.csv")

df = pd.read_csv(file_path)

print("========== PRODUCT DATA INVESTIGATION ==========")

# 1. Dataset overview
print("\nDataset shape:", df.shape)

# 2. Missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# 3. Check rows with missing product categories
missing_category = df[df["product_category_name"].isnull()]

print("\nProducts with missing category:")
print(len(missing_category))

print("\nSample missing-category products:")
print(missing_category.head())

# 4. Check whether all 610 rows have the same missing fields
print("\nMissing values pattern:")
print(
    df[df.isnull().any(axis=1)]
    .isnull()
    .sum(axis=1)
    .value_counts()
)

# 5. Check duplicate product IDs
print("\nDuplicate product IDs:")
print(df["product_id"].duplicated().sum())
