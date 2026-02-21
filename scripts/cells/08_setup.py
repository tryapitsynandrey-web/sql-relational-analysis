# =============================================================================
# Notebook 08 — Rule-Based Outlier & Anomaly Detection
# Setup: load order-level data and apply IQR outlier rules in Python
# =============================================================================

# ---------------------------------------------------------------------------
# Load order-level data from existing views
# ---------------------------------------------------------------------------
with get_connection() as conn:
    # Order-level: total_order_value per delivered order
    df_orders = pd.read_sql(
        """
        SELECT order_id, customer_state, total_order_value,
               order_purchase_timestamp
        FROM olist.vw_order_fact
        WHERE order_status = 'delivered'
        """,
        conn,
    )

    # Delivery-level: delay duration per order
    df_delivery = pd.read_sql(
        """
        SELECT order_id, actual_delivery_days, estimated_delivery_days,
               delay_vs_estimate_days AS delay_days, is_delayed
        FROM olist.vw_delivery_sla_metrics
        """,
        conn,
    )

df_orders["order_purchase_timestamp"] = pd.to_datetime(
    df_orders["order_purchase_timestamp"]
)

# Merge for joint analysis
df_merged = pd.merge(df_orders, df_delivery, on="order_id", how="inner")

# ---------------------------------------------------------------------------
# IQR-based outlier rules (non-parametric, deterministic, no ML)
# Boundary: Q75 + 1.5 × IQR  (standard Tukey fence for right-skewed data)
# ---------------------------------------------------------------------------

def iqr_upper_fence(series: "pd.Series") -> float:
    """Return the upper Tukey fence for a numeric series."""
    q25, q75 = series.quantile([0.25, 0.75])
    return q75 + 1.5 * (q75 - q25)


# Revenue outliers
rev_fence = iqr_upper_fence(df_merged["total_order_value"])
df_merged["is_revenue_outlier"] = df_merged["total_order_value"] > rev_fence

# Delay outliers (only for delayed orders)
delayed_df = df_merged[df_merged["is_delayed"] == True].copy()
if len(delayed_df) > 0:
    delay_fence = iqr_upper_fence(delayed_df["delay_days"])
    df_merged["is_delay_outlier"] = (
        df_merged["is_delayed"] & (df_merged["delay_days"] > delay_fence)
    )
else:
    delay_fence = None
    df_merged["is_delay_outlier"] = False

# Combined: flag orders that are outliers on BOTH dimensions
df_merged["is_dual_outlier"] = (
    df_merged["is_revenue_outlier"] & df_merged["is_delay_outlier"]
)

# Summary statistics
n_rev_outliers   = int(df_merged["is_revenue_outlier"].sum())
n_delay_outliers = int(df_merged["is_delay_outlier"].sum())
n_dual_outliers  = int(df_merged["is_dual_outlier"].sum())
n_total          = len(df_merged)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
out_checks = [
    ("Merged rows > 0",                n_total > 0),
    ("Revenue fence > 0",              rev_fence > 0),
    ("Revenue outliers > 0",           n_rev_outliers > 0),
    ("Revenue outlier rate < 15%",     n_rev_outliers / n_total < 0.15),
    ("No null is_revenue_outlier",     df_merged["is_revenue_outlier"].notna().all()),
]

print("Notebook 08 — Outlier Detection Data Validation")
print("=" * 55)
for label, passed in out_checks:
    print(f"  [{'PASS' if passed else 'FAIL'}]  {label}")

print(f"\nTotal orders analysed : {n_total:,}")
print(f"Revenue outlier fence : {rev_fence:,.2f} BRL")
print(f"Revenue outliers      : {n_rev_outliers:,}  ({n_rev_outliers/n_total*100:.2f}%)")
if delay_fence is not None:
    print(f"Delay outlier fence   : {delay_fence:.1f} days")
    print(f"Delay outliers        : {n_delay_outliers:,}  ({n_delay_outliers/n_total*100:.2f}%)")
print(f"Dual outliers         : {n_dual_outliers:,}")
