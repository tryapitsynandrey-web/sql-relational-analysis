# =============================================================================
# Notebook 06 — Geographic Patterns
# Setup: load state-grain revenue and SLA data, then cross-join in Python
# =============================================================================

# ---------------------------------------------------------------------------
# Load state-grain revenue data (Q3 of the revenue analysis)
# ---------------------------------------------------------------------------
sql_rev  = get_sql_path("sql/analysis/01_revenue_and_aov_behavior.sql")
q_states = load_queries(sql_rev)[2]   # Q3: GMV by state

# Load state-grain SLA data (Q2 of the SLA analysis)
sql_sla   = get_sql_path("sql/analysis/03_delivery_sla_performance.sql")
q_sla_agg = load_queries(sql_sla)[0]  # Q1: national totals
q_sla_geo = load_queries(sql_sla)[1]  # Q2: delay rate by state

# Load state-grain review score data (derived from review + delivery join)
sql_rev4  = get_sql_path("sql/analysis/04_review_score_drivers.sql")
q_del_score = load_queries(sql_rev4)[1]   # Q2: avg score by delivery status

with get_connection() as conn:
    df_gmv_state   = pd.read_sql(q_states,    conn)
    df_sla_summary = pd.read_sql(q_sla_agg,   conn)
    df_delay_state = pd.read_sql(q_sla_geo,   conn)

# ---------------------------------------------------------------------------
# Cross-join: merge revenue and SLA state-grain tables in Python
# SQL already computed both at state grain — this is presentation-layer join
# ---------------------------------------------------------------------------
df_geo = pd.merge(
    df_gmv_state,
    df_delay_state,
    on="customer_state",
    how="inner",
)

# Compute GMV share
total_gmv = df_geo["gmv"].sum()
df_geo["gmv_share_pct"] = (df_geo["gmv"] / total_gmv * 100).round(2)

# Classification: high delay = above median delayed_rate_pct
median_delay = df_geo["delayed_rate_pct"].median()
median_gmv   = df_geo["gmv"].median()
df_geo["delay_tier"]   = df_geo["delayed_rate_pct"].apply(
    lambda r: "High Delay"  if r > median_delay else "Low Delay"
)
df_geo["gmv_tier"] = df_geo["gmv"].apply(
    lambda g: "High GMV" if g > median_gmv else "Low GMV"
)
df_geo["quadrant"] = df_geo["gmv_tier"] + " / " + df_geo["delay_tier"]

# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------
geo_checks = [
    ("Merged rows > 0",             len(df_geo) > 0),
    ("No null customer_state",      df_geo["customer_state"].notna().all()),
    ("No null gmv",                 df_geo["gmv"].notna().all()),
    ("No null delayed_rate_pct",    df_geo["delayed_rate_pct"].notna().all()),
    ("GMV values >= 0",             (df_geo["gmv"] >= 0).all()),
    ("Delay rate 0-100",            df_geo["delayed_rate_pct"].between(0, 100).all()),
]

print("Notebook 06 — Geographic Data Validation")
print("=" * 50)
for label, passed in geo_checks:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}]  {label}")

print(f"\nStates in merged dataset: {len(df_geo)}")
display(df_geo.sort_values("gmv", ascending=False).head(10))
