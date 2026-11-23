
import pandas as pd
from pathlib import Path

file_path = Path(
    "data/raw/product_category_name_translation.csv"
)

df = pd.read_csv(file_path)

print("========== CATEGORY TRANSLATION INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Display all records
print("\nCategory translation records:")
print(df.to_string(index=False))

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Exact duplicates
print("\nExact duplicate records:", df.duplicated().sum())

# Duplicate Portuguese category names
print(
    "\nDuplicate category names:",
    df["product_category_name"].duplicated().sum()
)

# Duplicate English category names
print(
    "\nDuplicate English translations:",
    df["product_category_name_english"].duplicated().sum()
)

# Unique categories
print(
    "\nUnique Portuguese categories:",
    df["product_category_name"].nunique()
)

print(
    "Unique English categories:",
    df["product_category_name_english"].nunique()
)

# Data types
print("\nData types:")
print(df.dtypes)
