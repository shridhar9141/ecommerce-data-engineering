
import pandas as pd
from pathlib import Path

# Define raw data directory
DATA_DIR = Path("data/raw")

# Select the orders dataset
file_path = DATA_DIR / "olist_orders_dataset.csv"

# Read CSV file
df = pd.read_csv(file_path)

# Display basic information
print("\n========== DATASET OVERVIEW ==========")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())
