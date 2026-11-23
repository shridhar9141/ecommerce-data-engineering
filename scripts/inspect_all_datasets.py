
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

for file_path in DATA_DIR.glob("*.csv"):

    print("\n" + "=" * 60)
    print(f"DATASET: {file_path.name}")
    print("=" * 60)

    df = pd.read_csv(file_path)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Records:", df.duplicated().sum())
