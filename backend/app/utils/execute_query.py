import duckdb
import pandas as pd


def execute_sql_query(db_path: str, query: str) -> pd.DataFrame:
    """
    Execute a SQL query on a DuckDB database and return the results as a DataFrame.

    :param db_path: Path to the DuckDB database file.
    :param query: The SQL query to execute.
    :return: Query results as a pandas DataFrame.
    """
    with duckdb.connect(db_path, read_only=True) as conn:
        return conn.execute(query).df()
