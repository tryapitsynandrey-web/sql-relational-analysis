# Load SQL queries
sql_path = get_sql_path("sql/analysis/01_revenue_and_aov_behavior.sql")
queries = load_queries(sql_path)

# Execute all three queries against the database
with get_connection() as conn:
    df_monthly_revenue = pd.read_sql(queries[0], conn)
    df_top_categories  = pd.read_sql(queries[1], conn)
    df_top_states      = pd.read_sql(queries[2], conn)

# Ensure datetime dtype for the time axis
df_monthly_revenue["revenue_month"] = pd.to_datetime(df_monthly_revenue["revenue_month"])

# ---------------------------------------------------------------------------
# Inline data validation
# ---------------------------------------------------------------------------
_checks_01 = [
    ("Monthly revenue rows > 0",         len(df_monthly_revenue) > 0),
    ("No null revenue values",           df_monthly_revenue["total_revenue"].notna().all()),
    ("All revenue values > 0",           (df_monthly_revenue["total_revenue"] > 0).all()),
    ("Top-categories rows > 0",          len(df_top_categories) > 0),
    ("Top-states rows > 0",              len(df_top_states) > 0),
    ("GMV values non-negative",          (df_top_states["gmv"] >= 0).all()),
]
print("Notebook 01 — Data Validation")
for label, passed in _checks_01:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print()
display(df_monthly_revenue.head(6))
display(df_top_categories)
display(df_top_states)
