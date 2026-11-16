import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

DEFAULT_DATABASE_URL = "postgresql://bms:bms@127.0.0.1:5432/bms"

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


def database_url() -> str:
    """Return the configured PostgreSQL connection string."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def connect(url: str | None = None) -> Connection:
    """Open a new PostgreSQL connection that returns rows as dictionaries."""
    return psycopg.connect(url or database_url(), row_factory=dict_row)


@contextmanager
def get_connection() -> Iterator[Connection]:
    """Yield a connection, committing on success and rolling back on error."""
    with connect() as connection:
        yield connection


def _schema_statements() -> list[str]:
    statements = (statement.strip() for statement in SCHEMA_FILE.read_text().split(";"))
    return [statement for statement in statements if statement]


def init_schema() -> None:
    """Create every table and index the application needs, if missing."""
    with get_connection() as connection:
        for statement in _schema_statements():
            connection.execute(statement)


def truncate_departments() -> None:
    """Remove every department and its benefits."""
    with get_connection() as connection:
        connection.execute(
            "TRUNCATE department_benefits, departments RESTART IDENTITY CASCADE"
        )


def truncate_all() -> None:
    """Remove every row from every application table."""
    with get_connection() as connection:
        connection.execute(
            "TRUNCATE department_benefits, departments, users RESTART IDENTITY CASCADE"
        )
