"""
Data provider layer for the Olist Streamlit application.
Handles SQL execution and Streamlit-side caching.
Uses the existing analysis.utils.sql_loader for proven SQL parsing.
"""

import sys
import os
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure repo root is on sys.path so analysis.utils imports work
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analysis.utils.sql_loader import get_sql_path, load_queries
from src.core.db_client import get_connection


@st.cache_data(ttl=3600)
def get_revenue_metrics():
    """Fetches monthly revenue, order volume, and AOV."""
    conn = get_connection()
    if not conn:
        return None, None, None

    queries = load_queries(get_sql_path("sql/analysis/01_revenue_and_aov_behavior.sql"))

    df_trend = pd.read_sql(queries[0], conn)
    df_trend["revenue_month"] = pd.to_datetime(df_trend["revenue_month"])

    df_cat = pd.read_sql(queries[1], conn)
    df_state = pd.read_sql(queries[2], conn)

    return df_trend, df_cat, df_state


@st.cache_data(ttl=3600)
def get_logistics_metrics():
    """Fetches delivery SLA metrics."""
    conn = get_connection()
    if not conn:
        return None

    try:
        queries = load_queries(get_sql_path("sql/analysis/03_delivery_sla_performance.sql"))
        return pd.read_sql(queries[0], conn)
    except Exception:
        return None


@st.cache_data(ttl=3600)
def get_customer_satisfaction():
    """Fetches review score driver data."""
    conn = get_connection()
    if not conn:
        return None

    try:
        queries = load_queries(get_sql_path("sql/analysis/04_review_score_drivers.sql"))
        return pd.read_sql(queries[0], conn)
    except Exception:
        return None

