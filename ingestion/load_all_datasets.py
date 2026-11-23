
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL


# 1. Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


# 2. Database configuration
required_vars = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

missing_vars = [
    var for var in required_vars if not os.getenv(var)
]

if missing_vars:
    raise ValueError(
        f"Missing environment variables: {missing_vars}"
    )


# 3. Create PostgreSQL connection
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(db_url, pool_pre_ping=True)


# 4. Dataset configuration
datasets = {
    "geolocation": "geolocation_cleaned.csv",
    "products": "products_cleaned.csv",
    "orders": "orders_cleaned.csv",
    "order_items": "order_items_cleaned.csv",
    "payments": "payments_cleaned.csv",
    "reviews": "reviews_cleaned.csv",
    "sellers": "sellers_cleaned.csv",
    "category_translation": "category_translation_cleaned.csv",
}


# 5. Load datasets
print("========== E-COMMERCE DATA LOADING ==========")

try:

    total_datasets = len(datasets)
    successful_datasets = 0

    for table_name, filename in datasets.items():

        print(f"\nLoading: {table_name}")

        # Build CSV file path
        csv_path = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / filename
        )

        # Check whether CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {csv_path}"
            )

        # Read cleaned CSV
        df = pd.read_csv(csv_path)

        # Check whether dataset is empty
        if df.empty:
            raise ValueError(
                f"Dataset is empty: {csv_path}"
            )

        csv_rows = len(df)

        print("CSV rows:", csv_rows)

        # Load data inside a transaction
        with engine.begin() as connection:

            # Clear existing records
            connection.execute(
                text(f"TRUNCATE TABLE staging.{table_name}")
            )

            # Insert records into PostgreSQL
            df.to_sql(
                name=table_name,
                schema="staging",
                con=connection,
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi",
            )

            # Verify database row count
            result = connection.execute(
                text(
                    f"SELECT COUNT(*) "
                    f"FROM staging.{table_name}"
                )
            )

            database_rows = result.scalar_one()

            # Validate before transaction commits
            if database_rows != csv_rows:
                raise ValueError(
                    f"Row count mismatch for {table_name}: "
                    f"CSV={csv_rows}, DB={database_rows}"
                )

        # Transaction committed successfully
        successful_datasets += 1

        print("Database rows:", database_rows)
        print("Status: SUCCESS")

    print("\n========== LOADING SUMMARY ==========")
    print(f"Total datasets: {total_datasets}")
    print(f"Successfully loaded: {successful_datasets}")
    print("All eight datasets loaded successfully!")


except Exception as error:

    print("\n========== LOADING FAILED ==========")
    print("Error:", error)

    # Preserve the original exception
    raise


finally:

    # Release database resources
    engine.dispose()

    print("\nDatabase connection resources released.")
