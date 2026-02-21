# =============================================================================
# Notebook 09 — Rule-Based Customer Segmentation
# Setup: load customer-monthly metrics and assign spend tiers via percentile cuts
# =============================================================================

sql_path = get_sql_path("sql/analysis/02_cohorts_and_retention.sql")
queries  = load_queries(sql_path)

with get_connection() as conn:
    df_cohorts = pd.read_sql(queries[0], conn)   # retention matrix
    df_ltv     = pd.read_sql(queries[1], conn)   # cumulative LTV by cohort

df_cohorts["cohort_month"] = pd.to_datetime(df_cohorts["cohort_month"])
df_ltv["cohort_month"]     = pd.to_datetime(df_ltv["cohort_month"])

# ---------------------------------------------------------------------------
# Build customer-grain LTV snapshot: peak cumulative LTV per cohort-month
# (Each cohort_month × customer represented as avg_cumulative_ltv)
# ---------------------------------------------------------------------------
# Take the maximum LTV value per cohort (final observed period)
df_peak_ltv = (
    df_ltv.groupby("cohort_month")["avg_cumulative_ltv"]
    .max()
    .reset_index()
    .rename(columns={"avg_cumulative_ltv": "peak_avg_ltv"})
)

# Merge cohort size (from retention table at month 0)
df_cohort_size = (
    df_cohorts[df_cohorts["months_since_first_purchase"] == 0]
    [["cohort_month", "returned_customers"]]
    .rename(columns={"returned_customers": "cohort_size"})
)
df_seg_base = pd.merge(df_peak_ltv, df_cohort_size, on="cohort_month", how="inner")

# Merge month-1 retention rate
df_m1_ret = (
    df_cohorts[df_cohorts["months_since_first_purchase"] == 1]
    [["cohort_month", "retention_rate_pct"]]
    .rename(columns={"retention_rate_pct": "month1_retention_pct"})
)
df_seg_base = pd.merge(df_seg_base, df_m1_ret, on="cohort_month", how="left")

# ---------------------------------------------------------------------------
# Tier assignment: percentile-cut rules on peak_avg_ltv
# Tiers are computed from the data distribution — not pre-assumed thresholds
# ---------------------------------------------------------------------------
p33 = df_seg_base["peak_avg_ltv"].quantile(0.33)
p67 = df_seg_base["peak_avg_ltv"].quantile(0.67)

def assign_tier(ltv: float) -> str:
    if ltv >= p67:
        return "High-Value"
    elif ltv >= p33:
        return "Mid-Value"
    else:
        return "Single-Purchase"

df_seg_base["ltv_tier"]    = df_seg_base["peak_avg_ltv"].apply(assign_tier)
df_seg_base["cohort_year"] = df_seg_base["cohort_month"].dt.year

tier_order  = ["Single-Purchase", "Mid-Value", "High-Value"]
tier_colors = {"Single-Purchase": "#F44336", "Mid-Value": "#FF9800", "High-Value": "#4CAF50"}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
seg_checks = [
    ("Rows in seg_base > 0",             len(df_seg_base) > 0),
    ("No null peak_avg_ltv",             df_seg_base["peak_avg_ltv"].notna().all()),
    ("All three tiers represented",      set(df_seg_base["ltv_tier"]) == set(tier_order)),
    ("p33 < p67",                        p33 < p67),
    ("Cohort size all positive",         (df_seg_base["cohort_size"] > 0).all()),
]

print("Notebook 09 — Customer Segmentation Data Validation")
print("=" * 55)
for label, passed in seg_checks:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print(f"\nTier boundaries:  P33 = {p33:,.2f} BRL  |  P67 = {p67:,.2f} BRL")
print(f"Cohorts in dataset: {len(df_seg_base)}")
print("\nTier distribution:")
display(df_seg_base.groupby("ltv_tier")["cohort_size"].agg(["count","sum","mean"]).round(1))
display(df_seg_base.sort_values("cohort_month").head(10))
