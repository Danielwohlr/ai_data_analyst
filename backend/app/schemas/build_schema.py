import duckdb


def build_duckdb_schema(db_path: str) -> str:
    """
    Extract schema information from a DuckDB database and format it as a string.

    :param db_path: Path to the DuckDB database file.
    :return: Formatted schema string like 'table(column1: type, column2: type, ...)'
    """
    with duckdb.connect(db_path, read_only=True) as conn:
        tables = [table[0] for table in conn.execute("SHOW TABLES").fetchall()]
        schema_lines = []

        for table in tables:
            columns = conn.execute(f"DESCRIBE {table}").fetchall()
            col_defs = ", ".join(
                f"{col_name}: {col_type}" for col_name, col_type, *_ in columns
            )
            schema_lines.append(f"{table}({col_defs})")

        return "\n".join(schema_lines)
