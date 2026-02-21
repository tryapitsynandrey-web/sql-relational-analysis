# Load SQL queries
sql_path = get_sql_path("sql/analysis/04_review_score_drivers.sql")
queries = load_queries(sql_path)

# Execute all three review-score queries
with get_connection() as conn:
    df_score_dist       = pd.read_sql(queries[0], conn)
    df_delivery_scores  = pd.read_sql(queries[1], conn)
    df_worst_categories = pd.read_sql(queries[2], conn)

_checks_04 = [
    ("Score dist rows > 0",               len(df_score_dist) > 0),
    ("Delivery score rows > 0",           len(df_delivery_scores) > 0),
    ("Worst category rows > 0",           len(df_worst_categories) > 0),
    ("Review scores in 1-5 range",        df_score_dist["review_score"].between(1, 5).all()),
    ("pct_of_total sums to ~100",         abs(df_score_dist["pct_of_total"].sum() - 100) < 1),
]
print("Notebook 04 — Data Validation")
for label, passed in _checks_04:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print()
display(df_score_dist)
display(df_delivery_scores)
display(df_worst_categories)
