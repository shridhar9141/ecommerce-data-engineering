# End-to-End E-Commerce Data Engineering Platform

An end-to-end data engineering project built using Python, Pandas, PostgreSQL, and SQL to process and analyze Brazilian e-commerce data.

## Project Overview

This project implements a data pipeline using the Brazilian E-Commerce Public Dataset by Olist.

The pipeline processes raw e-commerce data, performs data cleaning and quality checks, loads the cleaned datasets into PostgreSQL, and transforms them into analytical fact and dimension tables.

The final data model supports business analysis through SQL queries.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.13 |
| Data Processing | Pandas |
| Database | PostgreSQL |
| Database Connectivity | SQLAlchemy, psycopg2 |
| Query Language | SQL |
| Testing | pytest |
| Version Control | Git, GitHub |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shridhar9141/ecommerce-data-engineering.git
cd ecommerce-data-engineering
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the Dataset

Download the [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Extract the nine CSV files into:

```text
data/raw/
```

### 5. Configure PostgreSQL

Install PostgreSQL and create a database named:

```sql
CREATE DATABASE ecommerce_dw;
```

Create a `.env` file in the project root with your local database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

**Important:** Never commit your `.env` file or share database credentials publicly.

### 6. Prepare the Database

First, execute the SQL scripts in `sql/staging/` to create the staging schema and its nine tables.

After loading the cleaned datasets into the staging tables, execute the SQL scripts in `sql/gold/` to create the Gold schema, dimension tables, and fact tables.

Follow the numbered SQL scripts and their table dependencies.

### 7. Run the Data Pipeline

First, run the nine cleaning scripts to generate cleaned CSV files in `data/processed/`.

Then load customer records:

```bash
python ingestion/load_customers.py
```

Load the remaining eight datasets:

```bash
python ingestion/load_all_datasets.py
```

### 8. Run Automated Tests

```bash
python -m pytest -v
```

The test suite validates data quality rules and checks row counts in PostgreSQL staging and Gold tables.

## Architecture

**Current implementation:**

1. **Data Source:** Olist Brazilian E-Commerce Public Dataset.
2. **Ingestion:** Read raw CSV datasets using Python.
3. **Data Cleaning:** Clean, validate, and prepare datasets using Pandas.
4. **Staging Layer:** Load cleaned datasets into PostgreSQL staging tables.
5. **Gold Layer:** Create analytical fact and dimension tables.
6. **Analytics:** Execute SQL queries to generate business insights.
7. **Testing:** Validate data quality and database table row counts.

## Data Model

### Staging Layer

Stores the cleaned source datasets in PostgreSQL.

- Customers
- Geolocation
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Category Translation

### Gold Layer

Contains analytical tables:

**Dimension tables**
- dim_customers
- dim_products
- dim_sellers
- dim_orders
- dim_date
- customer_records

**Fact tables**
- fact_order_items
- fact_payments
- fact_reviews

## Key Features

- Ingestion of nine Olist datasets.
- Data cleaning and validation using Pandas.
- Duplicate detection and handling.
- Missing-value validation.
- Data type conversion and consistency checks.
- PostgreSQL staging and Gold layers.
- Fact and dimension table modeling.
- SQL-based business analytics.
- Automated unit and integration tests.

## Analytics

The project includes five SQL analytics queries:

1. Monthly Sales Analysis
2. Top Product Categories
3. Payment Method Analysis
4. Customer Review Analysis
5. Delivery Performance Analysis

## Data Quality and Testing

The project includes automated tests using pytest.

Current test coverage includes:

- Data cleaning and validation rules.
- Duplicate and missing-value handling.
- Staging table row-count validation.
- Gold table row-count validation.

**Latest test result:** 85 passed.

## Dataset

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains information about customers, orders, products, sellers, payments, reviews, and geolocation.

Download the dataset from Kaggle and place the original CSV files inside `data/raw/`.

ecommerce-data-engineering/
|
+-- data/
|   +-- raw/
|   +-- processed/
|
+-- ingestion/
|   +-- clean_*.py
|   +-- load_all_datasets.py
|   +-- load_customers.py
|   +-- __init__.py
|
+-- scripts/
|   +-- inspect_*.py
|   +-- investigate_*.py
|   +-- test_connection.py
|
+-- sql/
|   +-- staging/
|   +-- gold/
|   |   +-- dimensions/
|   |   +-- facts/
|   +-- analytics/
|
+-- tests/
|   +-- test_data_quality.py
|   +-- test_staging_integration.py
|   +-- test_gold_integration.py
|
+-- airflow/
+-- dashboard/
+-- docs/
+-- transformations/
|
+-- .gitignore
+-- README.md
+-- requirements.txt


## Future Enhancements

- Apache Airflow for workflow orchestration.
- dbt for modular SQL transformations and testing.
- Docker for containerization.
- Power BI for interactive dashboards.

## Author

**Shridhar**

GitHub: [@shridhar9141](https://github.com/shridhar9141)

Project Repository: [ecommerce-data-engineering](https://github.com/shridhar9141/ecommerce-data-engineering)
