"""
Script to synchronize time entries from Clockify to the local DuckDB database.
"""

from datetime import datetime, timezone
import duckdb

from . import clockify_client
from . import database


def sync_clockify_to_db() -> None:
    """
    Fetches new time entries from Clockify and saves them to the database.
    """
    print("Initializing database...")
    database.init_db()

    last_sync_time = database.get_last_sync_time()
    if last_sync_time:
        print(f"Last sync was at {last_sync_time}. Fetching new entries since then.")
    else:
        print("No previous sync found. Fetching all time entries.")

    try:
        entries = clockify_client.client.get_time_entries(start=last_sync_time)
    except Exception as e:
        print(f"Error fetching data from Clockify: {e}")
        return

    if not entries:
        print("No new entries to sync.")
        # We still update the sync time to now to avoid re-checking empty periods
        database.update_last_sync_time(datetime.now(timezone.utc))
        return

    print(f"Found {len(entries)} new time entries to save.")

    data_to_insert = [
        (e.id, e.description, e.user_id, e.project_id, e.task_id, e.time_interval.start, e.time_interval.end, e.duration_seconds)
        for e in entries
    ]

    with database.get_connection() as con:
        try:
            con.executemany(
                "INSERT OR REPLACE INTO time_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                data_to_insert,
            )
            print(f"Successfully saved {len(data_to_insert)} entries to the database.")
            database.update_last_sync_time(datetime.now(timezone.utc))
        except duckdb.Error as e:
            print(f"Database error during insertion: {e}")