"""
Database module for ResumAI SQLite storage.
"""

from .connection import get_connection, get_db_path, init_db, close_connection
from .schema import create_schema, drop_schema

__all__ = [
    'get_connection',
    'get_db_path',
    'init_db',
    'close_connection',
    'create_schema',
    'drop_schema',
]
