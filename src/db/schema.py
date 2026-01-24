"""
Schema creation and management for ResumAI database.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from .connection import get_connection, execute_script


# Path to schema SQL file
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def create_schema(conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Create the database schema from schema.sql.

    Uses IF NOT EXISTS, so it's safe to call multiple times.

    Args:
        conn: Optional connection. Uses thread-local connection if not provided.
    """
    if conn is None:
        conn = get_connection()

    schema_sql = SCHEMA_PATH.read_text()
    execute_script(schema_sql, conn)


def drop_schema(conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Drop all tables in the database.

    WARNING: This destroys all data!

    Args:
        conn: Optional connection. Uses thread-local connection if not provided.
    """
    if conn is None:
        conn = get_connection()

    # Tables in reverse dependency order
    tables = [
        # Support tables
        "job_errors",
        "job_logs",
        "job_artifacts",

        # Subcontent tables (deepest first)
        "job_subcontent_bullet_tags",
        "job_subcontent_bullets",
        "job_subcontent_roles",
        "job_subcontent_company_urls",
        "job_subcontent_companies",
        "job_subcontent_coverletter",
        "job_subcontent_awards",
        "job_subcontent_education",
        "job_subcontent_highlights",
        "job_subcontent_skills",
        "job_subcontent_summary",
        "job_subcontent_contacts",

        # Job tables
        "job_subcontent_events",
        "job_tags",
        "job_files",
        "jobs",

        # Resume tables (deepest first)
        "resume_bullet_tags",
        "resume_bullets",
        "resume_roles",
        "resume_company_urls",
        "resume_companies",
        "resume_enjoys",
        "resume_passions",
        "resume_awards",
        "resume_education",
        "resume_skills",
        "resume_contacts",
        "resumes",
    ]

    cursor = conn.cursor()
    try:
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        conn.commit()
    finally:
        cursor.close()


def get_schema_version(conn: Optional[sqlite3.Connection] = None) -> int:
    """
    Get the current schema version.

    Returns 0 if schema_version table doesn't exist.

    Args:
        conn: Optional connection.

    Returns:
        Current schema version number.
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
        )
        if cursor.fetchone() is None:
            return 0

        cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        cursor.close()


def table_exists(table_name: str, conn: Optional[sqlite3.Connection] = None) -> bool:
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check.
        conn: Optional connection.

    Returns:
        True if table exists, False otherwise.
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def get_table_count(table_name: str, conn: Optional[sqlite3.Connection] = None) -> int:
    """
    Get the row count for a table.

    Args:
        table_name: Name of the table.
        conn: Optional connection.

    Returns:
        Number of rows in the table.
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    finally:
        cursor.close()


def get_all_tables(conn: Optional[sqlite3.Connection] = None) -> list[str]:
    """
    Get a list of all tables in the database.

    Args:
        conn: Optional connection.

    Returns:
        List of table names.
    """
    if conn is None:
        conn = get_connection()

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()


def get_database_stats(conn: Optional[sqlite3.Connection] = None) -> dict:
    """
    Get statistics about the database.

    Args:
        conn: Optional connection.

    Returns:
        Dictionary with table counts.
    """
    if conn is None:
        conn = get_connection()

    tables = get_all_tables(conn)
    stats = {}
    for table in tables:
        stats[table] = get_table_count(table, conn)
    return stats
