import duckdb
import pandas as pd
import os

DATA_DIR = os.path.abspath("dataset")
DB_PATH = os.path.join(DATA_DIR, "analytics.duckdb")

# List of all your CSV files and table names
CSV_TABLES = {
    "categories": "categories.csv",
    "customers": "customers.csv",
    "employees": "employees.csv",
    "orders": "orders.csv",
    "order_details": "order_details.csv",
    "products": "products.csv",
    "shippers": "shippers.csv",
}


def initialize_database():
    # Create or connect to DuckDB file
    con = duckdb.connect(DB_PATH)

    # Clean old tables
    for table in CSV_TABLES:
        con.execute(f"DROP TABLE IF EXISTS {table};")

    for table_name, file_name in CSV_TABLES.items():
        print(f"Loading {file_name} into table '{table_name}'...")
        df = pd.read_csv(f"dataset/{file_name}", encoding="cp1252")
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

    con.close()
    print("✅ DuckDB initialized.")


def get_connection():
    return duckdb.connect(DB_PATH)


# Run when executed directly
if __name__ == "__main__":
    initialize_database()
