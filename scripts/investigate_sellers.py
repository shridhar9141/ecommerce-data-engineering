
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_sellers_dataset.csv")

df = pd.read_csv(file_path)

print("========== SELLERS INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Exact duplicate records
print("\nExact duplicate records:", df.duplicated().sum())

# Duplicate seller IDs
print(
    "\nDuplicate seller IDs:",
    df["seller_id"].duplicated().sum()
)

# Unique sellers
print("\nUnique sellers:", df["seller_id"].nunique())

# Seller state distribution
print("\nSeller state distribution:")
print(df["seller_state"].value_counts())

# Unique seller cities
print("\nUnique seller cities:", df["seller_city"].nunique())

# ZIP code prefix statistics
print("\nZIP code prefix statistics:")
print(df["seller_zip_code_prefix"].describe())

# Data types
print("\nData types:")
print(df.dtypes)
