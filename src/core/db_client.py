"""
Database client for the Olist Streamlit application.
Refactored from analysis/utils/db.py for better integration.
"""

import os
import psycopg2
import psycopg2.extensions
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Load env vars
_REPO_ROOT = Path(__file__).resolve().parents[2]
_ENV_PATH = _REPO_ROOT / "analysis" / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

def _get_param(primary_key: str, fallback_key: str, default: str) -> str:
    return os.environ.get(primary_key) or os.environ.get(fallback_key) or default

@st.cache_resource
def get_connection():
    """
    Returns a cached database connection. 
    Using @st.cache_resource ensures we don't reconnect on every rerun.
    """
    params = {
        "host": _get_param("DB_HOST", "POSTGRES_HOST", "localhost"),
        "port": _get_param("DB_PORT", "POSTGRES_PORT", "5432"),
        "user": _get_param("DB_USER", "POSTGRES_USER", "postgres"),
        "password": _get_param("DB_PASSWORD", "POSTGRES_PASSWORD", "postgres"),
        "dbname": _get_param("DB_NAME", "POSTGRES_DB", "olist"),
    }
    
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        return conn
    except psycopg2.OperationalError as exc:
        st.error(f"Database connection failed: {exc}")
        return None
