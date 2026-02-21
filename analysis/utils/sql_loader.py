"""
SQL file loading and statement-splitting utilities.

The analysis SQL files in ``sql/analysis/`` follow a consistent convention:
each statement is prefixed by a numbered comment delimiter of the form::

    -- 1. Query description here
    SELECT ...;

    -- 2. Next query description
    SELECT ...;

``load_queries`` reads any such file and returns a list of ready-to-execute
statement strings in declaration order, suitable for passing directly to
``pandas.read_sql``.
"""

from __future__ import annotations

import re
from pathlib import Path


# Matches numbered comment headers: "-- 1.", "-- 12.", etc. (the delimiter).
_QUERY_HEADER = re.compile(r"--\s*\d+\.\s+.*")

# Root of the repository, resolved relative to this file's location.
# Structure: repo_root/analysis/utils/sql_loader.py → repo_root three levels up.
_REPO_ROOT = Path(__file__).resolve().parents[2]


def get_sql_path(relative_path: str) -> Path:
    """
    Resolve a SQL file path relative to the repository root.

    Parameters
    ----------
    relative_path : str
        Path to the SQL file relative to the repository root,
        e.g. ``"sql/analysis/01_revenue_and_aov_behavior.sql"``.

    Returns
    -------
    Path
        Absolute path to the SQL file.

    Raises
    ------
    FileNotFoundError
        If the resolved path does not point to an existing file.
    """
    path = _REPO_ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(
            f"SQL file not found: {path}\n"
            f"(Resolved from repo root: {_REPO_ROOT})"
        )
    return path


def load_queries(sql_path: str | Path) -> list[str]:
    """
    Read a SQL file and return its numbered statements as a list of strings.

    Statements are identified by their ``-- N. Description`` prefix comment.
    Each returned string contains only the SQL body (no comment header),
    stripped of leading/trailing whitespace, and terminated with a single
    semicolon so it can be passed directly to ``pandas.read_sql``.

    Parameters
    ----------
    sql_path : str or Path
        Path to the ``.sql`` file to read.  Prefer an absolute path constructed
        via :func:`get_sql_path`.

    Returns
    -------
    list[str]
        SQL statement strings in declaration order.

    Raises
    ------
    FileNotFoundError
        If ``sql_path`` does not exist.
    ValueError
        If the file contains no recognisable ``-- N.`` delimiters.

    Examples
    --------
    >>> from analysis.utils.sql_loader import get_sql_path, load_queries
    >>> path = get_sql_path("sql/analysis/01_revenue_and_aov_behavior.sql")
    >>> queries = load_queries(path)
    >>> len(queries)
    3
    """
    sql_path = Path(sql_path)
    if not sql_path.is_file():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    raw_text = sql_path.read_text(encoding="utf-8")
    statements: list[str] = []

    # Walk through the file line by line, collecting SQL lines that follow
    # each numbered header and discarding everything else (FileName comments,
    # blank lines before the first header, etc.).
    current_lines: list[str] = []
    inside_query = False

    for line in raw_text.splitlines():
        if _QUERY_HEADER.match(line.strip()):
            # Flush the previous statement if one is in progress.
            if inside_query and current_lines:
                sql_body = "\n".join(current_lines).strip().rstrip(";")
                if sql_body:
                    statements.append(sql_body + ";")
            current_lines = []
            inside_query = True
        elif inside_query:
            current_lines.append(line)

    # Flush the final statement.
    if inside_query and current_lines:
        sql_body = "\n".join(current_lines).strip().rstrip(";")
        if sql_body:
            statements.append(sql_body + ";")

    if not statements:
        raise ValueError(
            f"No SQL statements found in {sql_path}. "
            "Ensure statements are prefixed with '-- N. Description' headers."
        )

    return statements
