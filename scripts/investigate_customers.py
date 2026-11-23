
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_customers_dataset.csv")

df = pd.read_csv(file_path)

print("========== CUSTOMERS INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Exact duplicate records
print("\nExact duplicate records:", df.duplicated().sum())

# Duplicate customer IDs
print(
    "\nDuplicate customer IDs:",
    df["customer_id"].duplicated().sum()
)

# Duplicate customer unique IDs
print(
    "\nDuplicate customer unique IDs:",
    df["customer_unique_id"].duplicated().sum()
)

# Customer state distribution
print("\nCustomer state distribution:")
print(df["customer_state"].value_counts())

# Customer city statistics
print("\nNumber of unique customer cities:")
print(df["customer_city"].nunique())

# Customer ZIP code prefix
print("\nZIP code prefix statistics:")
print(df["customer_zip_code_prefix"].describe())

# Data types
print("\nData types:")
print(df.dtypes)
