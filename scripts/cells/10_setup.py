# =============================================================================
# Notebook 10 — Executive Summary Dashboard
# Setup: re-execute all 5 analytical query sets; build cross-notebook KPI table
# =============================================================================

# ---------------------------------------------------------------------------
# Load all 5 analysis query sets
# ---------------------------------------------------------------------------
sql_files = {
    "revenue":  "sql/analysis/01_revenue_and_aov_behavior.sql",
    "cohorts":  "sql/analysis/02_cohorts_and_retention.sql",
    "sla":      "sql/analysis/03_delivery_sla_performance.sql",
    "reviews":  "sql/analysis/04_review_score_drivers.sql",
    "payments": "sql/analysis/05_payment_type_behavior.sql",
}

with get_connection() as conn:
    # Revenue & AOV
    q_rev = load_queries(get_sql_path(sql_files["revenue"]))
    df_monthly = pd.read_sql(q_rev[0], conn)
    df_cats    = pd.read_sql(q_rev[1], conn)

    # Cohorts
    q_coh = load_queries(get_sql_path(sql_files["cohorts"]))
    df_retention = pd.read_sql(q_coh[0], conn)
    df_ltv_exec  = pd.read_sql(q_coh[1], conn)

    # SLA
    q_sla = load_queries(get_sql_path(sql_files["sla"]))
    df_sla_exec  = pd.read_sql(q_sla[0], conn)
    df_delay_geo = pd.read_sql(q_sla[1], conn)

    # Reviews
    q_rev4 = load_queries(get_sql_path(sql_files["reviews"]))
    df_scores      = pd.read_sql(q_rev4[0], conn)
    df_del_scores  = pd.read_sql(q_rev4[1], conn)
    df_worst_cats  = pd.read_sql(q_rev4[2], conn)

    # Payments
    q_pay = load_queries(get_sql_path(sql_files["payments"]))
    df_payments = pd.read_sql(q_pay[0], conn)
    df_cancels  = pd.read_sql(q_pay[1], conn)

df_monthly["revenue_month"] = pd.to_datetime(df_monthly["revenue_month"])
df_retention["cohort_month"] = pd.to_datetime(df_retention["cohort_month"])

# ---------------------------------------------------------------------------
# Extract scalar KPIs for the executive scorecard
# ---------------------------------------------------------------------------

# Revenue
total_gmv_exec    = df_monthly["total_revenue"].sum()
total_orders_exec = df_monthly["total_orders"].sum()
avg_aov           = df_monthly["average_order_value"].mean()

# Retention
m1_ret_df   = df_retention[df_retention["months_since_first_purchase"] == 1]
avg_m1_ret  = m1_ret_df["retention_rate_pct"].mean() if len(m1_ret_df) > 0 else None
peak_ltv    = df_ltv_exec["avg_cumulative_ltv"].max()

# SLA
delayed_rate_exec = float(df_sla_exec["delayed_rate_pct"].iloc[0])
avg_overshot_days = (
    float(df_sla_exec["avg_actual_delivery_days"].iloc[0])
    - float(df_sla_exec["avg_estimated_delivery_days"].iloc[0])
)

# Reviews
score_on_time = None
score_delayed = None
del_idx = df_del_scores.set_index("delivery_status")
if "On-Time" in del_idx.index:
    score_on_time = float(del_idx.loc["On-Time", "avg_review_score"])
if "Delayed" in del_idx.index:
    score_delayed = float(del_idx.loc["Delayed", "avg_review_score"])
score_gap = (score_on_time - score_delayed) if (score_on_time and score_delayed) else None

# Payments
cc_share = None
if len(df_payments) > 0:
    total_pay_val = df_payments["total_payment_value"].sum()
    cc_pay_val    = df_payments.loc[
        df_payments["payment_type"] == "credit_card", "total_payment_value"
    ]
    cc_share = float(cc_pay_val.values[0]) / total_pay_val * 100 if len(cc_pay_val) > 0 else None

cancel_weighted = (
    df_cancels["canceled_orders"].sum()
    / df_cancels["total_orders"].sum() * 100
)

print("Executive KPI Table")
print("=" * 60)
kpi_summary = {
    "Total Platform GMV (BRL)":       f"{total_gmv_exec:,.0f}",
    "Total Delivered Orders":         f"{total_orders_exec:,.0f}",
    "Average Order Value (BRL)":      f"{avg_aov:,.2f}",
    "Avg Month-1 Retention (%)":      f"{avg_m1_ret:.1f}" if avg_m1_ret else "N/A",
    "Peak Avg Cumulative LTV (BRL)":  f"{peak_ltv:,.2f}",
    "Overall Delay Rate (%)":         f"{delayed_rate_exec:.2f}",
    "Avg ETA Overshoot (days)":       f"{avg_overshot_days:+.1f}",
    "Score Gap (On-Time vs Delayed)": f"{score_gap:.2f}" if score_gap else "N/A",
    "Credit Card Revenue Share (%)":  f"{cc_share:.1f}" if cc_share else "N/A",
    "Weighted Cancel Rate (%)":       f"{cancel_weighted:.2f}",
}
for k, v in kpi_summary.items():
    print(f"  {k:45s}  {v}")
