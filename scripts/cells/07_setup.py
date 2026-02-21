# =============================================================================
# Notebook 07 — Time-Series Trends & Seasonality
# Setup: load monthly revenue data and derive rolling metrics in Python
# =============================================================================

sql_path = get_sql_path("sql/analysis/01_revenue_and_aov_behavior.sql")
queries  = load_queries(sql_path)

with get_connection() as conn:
    df_monthly = pd.read_sql(queries[0], conn)   # Q1: monthly revenue, orders, AOV

# ---------------------------------------------------------------------------
# Type coercion and sorting
# ---------------------------------------------------------------------------
df_monthly["revenue_month"] = pd.to_datetime(df_monthly["revenue_month"])
df_monthly = df_monthly.sort_values("revenue_month").reset_index(drop=True)

# ---------------------------------------------------------------------------
# Derived time-series metrics (all computed from observed SQL columns only)
# ---------------------------------------------------------------------------

# Month-over-month % change in revenue
df_monthly["revenue_mom_pct"] = df_monthly["total_revenue"].pct_change() * 100

# Month-over-month % change in order volume
df_monthly["orders_mom_pct"] = df_monthly["total_orders"].pct_change() * 100

# 3-month rolling average revenue (centred — uses pandas .rolling)
df_monthly["revenue_rolling_3m"] = (
    df_monthly["total_revenue"].rolling(window=3, min_periods=2).mean()
)

# 3-month rolling average AOV
df_monthly["aov_rolling_3m"] = (
    df_monthly["average_order_value"].rolling(window=3, min_periods=2).mean()
)

# Seasonality index: monthly revenue / 12-month trailing mean
# Allows visual identification of above/below-average months
trailing_mean = df_monthly["total_revenue"].rolling(window=12, min_periods=6).mean()
df_monthly["seasonality_index"] = (df_monthly["total_revenue"] / trailing_mean).round(3)

# Calendar fields for grouping
df_monthly["month_of_year"] = df_monthly["revenue_month"].dt.month
df_monthly["year"]          = df_monthly["revenue_month"].dt.year

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
ts_checks = [
    ("Rows > 0",                      len(df_monthly) > 0),
    ("Sorted ascending by month",     df_monthly["revenue_month"].is_monotonic_increasing),
    ("No missing revenue values",     df_monthly["total_revenue"].notna().all()),
    ("All revenue values > 0",        (df_monthly["total_revenue"] > 0).all()),
    ("Seasonality index not all null",df_monthly["seasonality_index"].notna().any()),
]

print("Notebook 07 — Time-Series Data Validation")
print("=" * 50)
for label, passed in ts_checks:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")
print(f"\nTime range: {df_monthly['revenue_month'].min().date()} "
      f"to {df_monthly['revenue_month'].max().date()}  "
      f"({len(df_monthly)} months)")

display(df_monthly[["revenue_month","total_revenue","total_orders",
                     "average_order_value","revenue_mom_pct",
                     "revenue_rolling_3m","seasonality_index"]].head(10))
