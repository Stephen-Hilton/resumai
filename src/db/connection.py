"""
Database connection management for ResumAI.
"""

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

# Thread-local storage for connections
_local = threading.local()

# Hardcoded database path: src/db/resumai.db
DB_PATH = Path(__file__).parent / "resumai.db"


def get_db_path() -> Path:
    """Get the hardcoded database path."""
    return DB_PATH


def _get_thread_connection() -> Optional[sqlite3.Connection]:
    """Get the connection for the current thread."""
    return getattr(_local, 'connection', None)


def _set_thread_connection(conn: Optional[sqlite3.Connection]) -> None:
    """Set the connection for the current thread."""
    _local.connection = conn


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Get or create a database connection for the current thread.

    Uses thread-local storage to maintain one connection per thread.
    Enables foreign keys and returns rows as Row objects for dict-like access.

    Args:
        db_path: Optional path to database file. Uses default if not provided.

    Returns:
        SQLite connection object.
    """
    conn = _get_thread_connection()

    if conn is None:
        path = db_path or get_db_path()
        conn = sqlite3.connect(str(path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        _set_thread_connection(conn)

    return conn


def close_connection() -> None:
    """Close the connection for the current thread."""
    conn = _get_thread_connection()
    if conn is not None:
        conn.close()
        _set_thread_connection(None)


def init_db(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Initialize the database, creating it if it doesn't exist.

    Args:
        db_path: Optional path to database file.

    Returns:
        SQLite connection object.
    """
    from .schema import create_schema

    # Close any existing connection
    close_connection()

    path = db_path or get_db_path()

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Get new connection and create schema
    conn = get_connection(path)
    create_schema(conn)

    return conn


@contextmanager
def transaction(conn: Optional[sqlite3.Connection] = None):
    """
    Context manager for database transactions.

    Automatically commits on success or rolls back on exception.

    Args:
        conn: Optional connection. Uses thread-local connection if not provided.

    Yields:
        Database cursor.

    Example:
        with transaction() as cursor:
            cursor.execute("INSERT INTO ...")
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


@contextmanager
def read_only(conn: Optional[sqlite3.Connection] = None):
    """
    Context manager for read-only database operations.

    Does not commit changes.

    Args:
        conn: Optional connection. Uses thread-local connection if not provided.

    Yields:
        Database cursor.

    Example:
        with read_only() as cursor:
            cursor.execute("SELECT ...")
            rows = cursor.fetchall()
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def execute_script(sql: str, conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Execute a multi-statement SQL script.

    Args:
        sql: SQL script with multiple statements.
        conn: Optional connection.
    """
    if conn is None:
        conn = get_connection()

    conn.executescript(sql)
    conn.commit()


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a dictionary."""
    return dict(zip(row.keys(), row))


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    """Convert a list of sqlite3.Row objects to a list of dictionaries."""
    return [row_to_dict(row) for row in rows]
