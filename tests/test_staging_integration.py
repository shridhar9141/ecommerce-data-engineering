
import csv
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# Expected datasets and row counts
DATASETS = {
    "customers": ("customers_cleaned.csv", 99441),
    "geolocation": ("geolocation_cleaned.csv", 738332),
    "orders": ("orders_cleaned.csv", 99441),
    "order_items": ("order_items_cleaned.csv", 112650),
    "payments": ("payments_cleaned.csv", 103886),
    "reviews": ("reviews_cleaned.csv", 99224),
    "products": ("products_cleaned.csv", 32951),
    "sellers": ("sellers_cleaned.csv", 3095),
    "category_translation": (
        "category_translation_cleaned.csv", 71
    ),
}


@pytest.fixture(scope="module")
def db_engine():
    """Create a PostgreSQL connection for integration tests."""

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
        pytest.skip(
            f"Missing database configuration: {missing_vars}"
        )

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(db_url, pool_pre_ping=True)

    try:
        yield engine
    finally:
        engine.dispose()


def count_csv_records(csv_path):
    """Count CSV records correctly, including multiline fields."""

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        return sum(1 for _ in reader)


@pytest.mark.parametrize(
    "table_name, dataset_info",
    DATASETS.items(),
)
def test_staging_table_row_count(
    db_engine, table_name, dataset_info
):
    """Compare cleaned CSV records with PostgreSQL records."""

    filename, expected_rows = dataset_info

    csv_path = (
        PROJECT_ROOT / "data" / "processed" / filename
    )

    assert csv_path.exists(), (
        f"Cleaned CSV not found: {csv_path}"
    )

    csv_rows = count_csv_records(csv_path)

    with db_engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM staging.{table_name}")
        )
        database_rows = result.scalar_one()

    assert csv_rows == expected_rows, (
        f"{table_name}: CSV expected {expected_rows}, "
        f"but found {csv_rows}"
    )

    assert database_rows == csv_rows, (
        f"{table_name}: CSV has {csv_rows} rows, "
        f"but PostgreSQL has {database_rows}"
    )
