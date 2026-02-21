# Load SQL queries
sql_path = get_sql_path("sql/analysis/05_payment_type_behavior.sql")
queries = load_queries(sql_path)

# Execute both payment-type queries
with get_connection() as conn:
    df_payment_usage = pd.read_sql(queries[0], conn)
    df_cancellations = pd.read_sql(queries[1], conn)

_checks_05 = [
    ("Payment usage rows > 0",            len(df_payment_usage) > 0),
    ("Cancellation rows > 0",             len(df_cancellations) > 0),
    ("No null payment_type",              df_payment_usage["payment_type"].notna().all()),
    ("Avg transaction value > 0",         (df_payment_usage["avg_transaction_value"] > 0).all()),
    ("Cancellation rate 0-100",           df_cancellations["cancellation_rate_pct"].between(0, 100).all()),
]
print("Notebook 05 — Data Validation")
for label, passed in _checks_05:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print()
display(df_payment_usage)
display(df_cancellations)
