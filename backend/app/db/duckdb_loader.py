import duckdb
import os

DATA_DIR = os.path.abspath("backend/dataset")
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
        con.execute(f"DROP TABLE IF EXISTS {table}")

    # Load each CSV with normalized column names and proper encoding
    for table_name, file_name in CSV_TABLES.items():
        csv_path = os.path.join(DATA_DIR, file_name)
        print(f"Loading {file_name} into table '{table_name}'...")
        print(f"CSV path: {csv_path}")

        con.execute(
            f"""
            CREATE TABLE {table_name} AS 
            SELECT * FROM read_csv_auto(
                '{csv_path}',
                delim=',',
                encoding='UTF-8',
                normalize_names=true,
                all_varchar=true
            )
        """
        )

    con.close()
    print("✅ DuckDB initialized.")


def get_connection():
    return duckdb.connect(DB_PATH)


# Run when executed directly
if __name__ == "__main__":
    initialize_database()
