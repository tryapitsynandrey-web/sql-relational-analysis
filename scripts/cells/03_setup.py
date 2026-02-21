# Load SQL queries
sql_path = get_sql_path("sql/analysis/03_delivery_sla_performance.sql")
queries = load_queries(sql_path)

# Execute both SLA queries
with get_connection() as conn:
    df_sla_summary = pd.read_sql(queries[0], conn)
    df_delay_state = pd.read_sql(queries[1], conn)

_checks_03 = [
    ("SLA summary row returned",          len(df_sla_summary) == 1),
    ("Delay state rows > 0",             len(df_delay_state) > 0),
    ("Delay rate 0-100",                 df_delay_state["delayed_rate_pct"].between(0, 100).all()),
    ("Total deliveries > 0",             int(df_sla_summary["total_deliveries"].iloc[0]) > 0),
]
print("Notebook 03 — Data Validation")
for label, passed in _checks_03:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print()
display(df_sla_summary)
display(df_delay_state.head(15))
