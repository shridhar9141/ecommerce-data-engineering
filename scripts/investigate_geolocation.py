
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_geolocation_dataset.csv")

df = pd.read_csv(file_path)

print("========== GEOLOCATION INVESTIGATION ==========")

# 1. Exact duplicate rows
print("\nExact duplicate rows:")
print(df.duplicated().sum())

# 2. Display some exact duplicate rows
print("\nSample exact duplicate rows:")
print(df[df.duplicated(keep=False)].head(10))

# 3. Count repeated ZIP code prefixes
print("\nTotal unique ZIP code prefixes:")
print(df["geolocation_zip_code_prefix"].nunique())

print("\nRows with repeated ZIP code prefixes:")
print(
    df.duplicated(
        subset=["geolocation_zip_code_prefix"]
    ).sum()
)

# 4. Check different coordinates for the same ZIP prefix
coordinates_per_zip = (
    df.groupby("geolocation_zip_code_prefix")
    [["geolocation_lat", "geolocation_lng"]]
    .apply(lambda group: group.drop_duplicates().shape[0])
)

print("\nZIP prefixes with multiple coordinate pairs:")
print((coordinates_per_zip > 1).sum())
