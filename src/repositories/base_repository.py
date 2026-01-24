"""
Base repository with common database operations.
"""

import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Optional

from ..db.connection import get_connection, row_to_dict, rows_to_dicts


class BaseRepository(ABC):
    """
    Abstract base class for repositories.

    Provides common database operations and connection management.
    """

    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize repository with optional connection.

        Args:
            conn: Optional database connection. Uses thread-local if not provided.
        """
        self._conn = conn

    @property
    def conn(self) -> sqlite3.Connection:
        """Get the database connection."""
        if self._conn is None:
            self._conn = get_connection()
        return self._conn

    def _execute(
        self,
        sql: str,
        params: tuple = (),
        commit: bool = True
    ) -> sqlite3.Cursor:
        """
        Execute a SQL statement.

        Args:
            sql: SQL statement to execute.
            params: Parameters for the SQL statement.
            commit: Whether to commit after execution.

        Returns:
            Cursor with results.
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        if commit:
            self.conn.commit()
        return cursor

    def _execute_many(
        self,
        sql: str,
        params_list: list[tuple],
        commit: bool = True
    ) -> None:
        """
        Execute a SQL statement with multiple parameter sets.

        Args:
            sql: SQL statement to execute.
            params_list: List of parameter tuples.
            commit: Whether to commit after execution.
        """
        cursor = self.conn.cursor()
        cursor.executemany(sql, params_list)
        if commit:
            self.conn.commit()
        cursor.close()

    def _fetch_one(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """
        Fetch a single row as a dictionary.

        Args:
            sql: SQL SELECT statement.
            params: Parameters for the query.

        Returns:
            Dictionary with column values or None.
        """
        cursor = self._execute(sql, params, commit=False)
        row = cursor.fetchone()
        cursor.close()
        return row_to_dict(row) if row else None

    def _fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        """
        Fetch all rows as dictionaries.

        Args:
            sql: SQL SELECT statement.
            params: Parameters for the query.

        Returns:
            List of dictionaries with column values.
        """
        cursor = self._execute(sql, params, commit=False)
        rows = cursor.fetchall()
        cursor.close()
        return rows_to_dicts(rows)

    def _insert(self, table: str, data: dict) -> int:
        """
        Insert a row into a table.

        Args:
            table: Table name.
            data: Dictionary of column: value pairs.

        Returns:
            ID of the inserted row.
        """
        columns = list(data.keys())
        placeholders = ", ".join("?" for _ in columns)
        col_str = ", ".join(columns)
        sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
        cursor = self._execute(sql, tuple(data.values()))
        row_id = cursor.lastrowid
        cursor.close()
        return row_id

    def _insert_many(self, table: str, columns: list[str], rows: list[tuple]) -> None:
        """
        Insert multiple rows into a table.

        Args:
            table: Table name.
            columns: List of column names.
            rows: List of value tuples.
        """
        if not rows:
            return
        placeholders = ", ".join("?" for _ in columns)
        col_str = ", ".join(columns)
        sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
        self._execute_many(sql, rows)

    def _update(self, table: str, data: dict, where: str, where_params: tuple) -> int:
        """
        Update rows in a table.

        Args:
            table: Table name.
            data: Dictionary of column: value pairs to update.
            where: WHERE clause (without 'WHERE' keyword).
            where_params: Parameters for the WHERE clause.

        Returns:
            Number of rows affected.
        """
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + where_params
        cursor = self._execute(sql, params)
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def _delete(self, table: str, where: str, where_params: tuple) -> int:
        """
        Delete rows from a table.

        Args:
            table: Table name.
            where: WHERE clause (without 'WHERE' keyword).
            where_params: Parameters for the WHERE clause.

        Returns:
            Number of rows deleted.
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        cursor = self._execute(sql, where_params)
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def _delete_all(self, table: str) -> int:
        """
        Delete all rows from a table.

        Args:
            table: Table name.

        Returns:
            Number of rows deleted.
        """
        sql = f"DELETE FROM {table}"
        cursor = self._execute(sql)
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def _count(self, table: str, where: str = None, where_params: tuple = ()) -> int:
        """
        Count rows in a table.

        Args:
            table: Table name.
            where: Optional WHERE clause.
            where_params: Parameters for the WHERE clause.

        Returns:
            Number of rows.
        """
        sql = f"SELECT COUNT(*) as count FROM {table}"
        if where:
            sql += f" WHERE {where}"
        result = self._fetch_one(sql, where_params)
        return result['count'] if result else 0

    def _exists(self, table: str, where: str, where_params: tuple) -> bool:
        """
        Check if rows exist in a table.

        Args:
            table: Table name.
            where: WHERE clause.
            where_params: Parameters for the WHERE clause.

        Returns:
            True if at least one row exists.
        """
        sql = f"SELECT 1 FROM {table} WHERE {where} LIMIT 1"
        result = self._fetch_one(sql, where_params)
        return result is not None

    def begin_transaction(self) -> None:
        """Begin a transaction."""
        self.conn.execute("BEGIN TRANSACTION")

    def commit(self) -> None:
        """Commit the current transaction."""
        self.conn.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self.conn.rollback()

    @abstractmethod
    def to_dict(self, id: int) -> Optional[dict]:
        """
        Export an entity as a YAML-compatible dictionary.

        Args:
            id: Entity ID.

        Returns:
            Dictionary representation suitable for YAML export.
        """
        pass
