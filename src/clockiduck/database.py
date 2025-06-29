import duckdb
from datetime import datetime, timezone
from typing import Optional

DB_FILE = "clockiduck.db"


def get_connection() -> duckdb.DuckDBPyConnection:
    """Returns a connection to the DuckDB database."""
    return duckdb.connect(database=DB_FILE, read_only=False)


def init_db() -> None:
    """Initializes the database and creates tables if they don't exist."""
    with get_connection() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS time_entries (
                id VARCHAR PRIMARY KEY,
                description VARCHAR,
                user_id VARCHAR,
                project_id VARCHAR,
                task_id VARCHAR,
                start TIMESTAMPTZ,
                "end" TIMESTAMPTZ,
                duration_seconds INTEGER
            );
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                key VARCHAR PRIMARY KEY,
                value TIMESTAMPTZ
            );
        """)


def get_last_sync_time() -> Optional[datetime]:
    """Retrieves the last sync timestamp from the app_state table."""
    try:
        with get_connection() as con:
            result = con.execute("SELECT value FROM app_state WHERE key = 'last_sync'").fetchone()
            return result[0] if result else None
    except duckdb.CatalogException:
        # This can happen if the table or db doesn't exist yet on the very first run.
        return None


def update_last_sync_time(sync_time: datetime) -> None:
    """Updates the last sync timestamp in the app_state table."""
    with get_connection() as con:
        con.execute(
            "INSERT OR REPLACE INTO app_state (key, value) VALUES ('last_sync', ?)",
            [sync_time],
        )