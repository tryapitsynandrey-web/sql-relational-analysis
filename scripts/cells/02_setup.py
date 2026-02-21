# Load SQL queries
sql_path = get_sql_path("sql/analysis/02_cohorts_and_retention.sql")
queries = load_queries(sql_path)

# Execute both cohort queries
with get_connection() as conn:
    df_retention = pd.read_sql(queries[0], conn)
    df_ltv       = pd.read_sql(queries[1], conn)

# Coerce cohort_month to datetime
df_retention["cohort_month"] = pd.to_datetime(df_retention["cohort_month"])
df_ltv["cohort_month"]       = pd.to_datetime(df_ltv["cohort_month"])

# ---------------------------------------------------------------------------
# Inline data validation
# ---------------------------------------------------------------------------
_checks_02 = [
    ("Retention rows > 0",                len(df_retention) > 0),
    ("LTV rows > 0",                      len(df_ltv) > 0),
    ("No null cohort_month",              df_retention["cohort_month"].notna().all()),
    ("Retention rate 0-100",              df_retention["retention_rate_pct"].between(0, 100).all()),
    ("Cumulative LTV non-negative",       (df_ltv["avg_cumulative_ltv"] >= 0).all()),
]
print("Notebook 02 — Data Validation")
for label, passed in _checks_02:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print()
display(df_retention.head(10))
display(df_ltv.head(10))
