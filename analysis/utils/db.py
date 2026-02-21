"""
Database connection utilities for the Olist analytics pipeline.

Credentials are read exclusively from environment variables so that no
secrets are hard-coded in notebooks or source files.  A `.env` file
(copied from ``.env.example``) is the recommended way to supply these
values for local development.

Environment Variables
---------------------
DB_HOST       : Postgres host (default: localhost)
DB_PORT       : Postgres port (default: 5432)
DB_USER       : Postgres user (default: postgres)
DB_PASSWORD   : Postgres password (default: postgres)
DB_NAME       : Target database name (default: olist)
"""

from __future__ import annotations

import os

import psycopg2
import psycopg2.extensions

from dotenv import load_dotenv

# Load .env from the analysis/ directory (one level up from this utils/ package).
_ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=_ENV_PATH, override=False)


def _get_param(primary_key: str, fallback_key: str, default: str) -> str:
    """Return the first non-empty value among the two env keys, then the default."""
    return (
        os.environ.get(primary_key)
        or os.environ.get(fallback_key)
        or default
    )


def get_connection() -> psycopg2.extensions.connection:
    """
    Open and return a psycopg2 database connection using environment variables.

    The caller is responsible for closing the connection.  In notebooks,
    prefer the context-manager form::

        with get_connection() as conn:
            df = pd.read_sql(query, conn)

    Returns
    -------
    psycopg2.extensions.connection
        An open, autocommit-disabled connection to the configured database.

    Raises
    ------
    psycopg2.OperationalError
        Re-raised with an informative message if the connection attempt fails.
    """
    params = {
        "host": _get_param("DB_HOST", "POSTGRES_HOST", "localhost"),
        "port": _get_param("DB_PORT", "POSTGRES_PORT", "5432"),
        "user": _get_param("DB_USER", "POSTGRES_USER", "postgres"),
        "password": _get_param("DB_PASSWORD", "POSTGRES_PASSWORD", "postgres"),
        "dbname": _get_param("DB_NAME", "POSTGRES_DB", "olist"),
    }

    try:
        return psycopg2.connect(**params)
    except psycopg2.OperationalError as exc:
        raise psycopg2.OperationalError(
            f"Could not connect to PostgreSQL at {params['host']}:{params['port']} "
            f"(db={params['dbname']}, user={params['user']}). "
            "Check that the database is running and that your .env file is correct."
        ) from exc
