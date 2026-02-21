# =============================================================================
# Dashboard 02 — Cohort Retention & Lifetime Value
# =============================================================================
fig = plt.figure(figsize=(18, 16))
fig.suptitle(
    "Olist Cohort Retention & LTV Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Panel A (top, wide): Month-1 Retention Rate across all cohorts
# ---------------------------------------------------------------------------
ax_ret = fig.add_subplot(3, 2, (1, 2))

month_1 = df_retention[df_retention["months_since_first_purchase"] == 1].copy()
month_1 = month_1.sort_values("cohort_month")

avg_ret = month_1["retention_rate_pct"].mean()

ax_ret.bar(
    month_1["cohort_month"].dt.strftime("%Y-%m"),
    month_1["retention_rate_pct"],
    color=[
        "#F44336" if r < avg_ret else "#2196F3"
        for r in month_1["retention_rate_pct"]
    ],
    width=0.7,
)
ax_ret.axhline(avg_ret, color="#FF9800", linewidth=1.5, linestyle="--",
               label=f"Average: {avg_ret:.1f}%")
ax_ret.set_title("A  |  Month-1 Retention Rate by Acquisition Cohort", loc="left", pad=8)
ax_ret.set_xlabel("Cohort (First Purchase Month)")
ax_ret.set_ylabel("Month-1 Retention Rate (%)")
ax_ret.tick_params(axis="x", rotation=45)
ax_ret.legend()
ax_ret.annotate(
    "Bars below average (orange line) indicate cohorts with weaker early re-engagement.",
    xy=(0.01, 0.05), xycoords="axes fraction", fontsize=8.5, color="#666",
    style="italic",
)
ax_ret.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel B (middle-left): Retention decay curve (months 0–6, all cohorts pooled)
# ---------------------------------------------------------------------------
ax_decay = fig.add_subplot(3, 2, 3)

decay = (
    df_retention[df_retention["months_since_first_purchase"] <= 6]
    .groupby("months_since_first_purchase")["retention_rate_pct"]
    .mean()
    .reset_index()
)

ax_decay.plot(
    decay["months_since_first_purchase"],
    decay["retention_rate_pct"],
    marker="o", color="#2196F3", linewidth=2,
)
ax_decay.fill_between(
    decay["months_since_first_purchase"],
    decay["retention_rate_pct"],
    alpha=0.15, color="#2196F3",
)
ax_decay.set_title("B  |  Avg Retention Decay Curve (Months 0-6)", loc="left", pad=8)
ax_decay.set_xlabel("Months Since First Purchase")
ax_decay.set_ylabel("Avg Retention Rate (%)")
ax_decay.set_xticks(range(0, 7))
ax_decay.grid(True, axis="y", linestyle="--", alpha=0.5)

# Annotate the sharpest drop
if len(decay) >= 2:
    drops = decay["retention_rate_pct"].diff().iloc[1:]
    worst_month = int(drops.idxmin())
    steepest_label = f"Steepest drop at month {worst_month}"
    ax_decay.annotate(
        steepest_label,
        xy=(worst_month, decay.loc[worst_month, "retention_rate_pct"]),
        xytext=(worst_month + 0.3, decay.loc[worst_month, "retention_rate_pct"] + 3),
        arrowprops=dict(arrowstyle="->", color="#555"),
        fontsize=8.5, color="#555",
    )

# ---------------------------------------------------------------------------
# Panel C (middle-right): Average cohort LTV growth curve (all cohorts pooled)
# ---------------------------------------------------------------------------
ax_ltv = fig.add_subplot(3, 2, 4)

ltv_trend = (
    df_ltv.groupby("months_since_first_purchase")["avg_cumulative_ltv"]
    .mean()
    .reset_index()
    .sort_values("months_since_first_purchase")
)

ax_ltv.plot(
    ltv_trend["months_since_first_purchase"],
    ltv_trend["avg_cumulative_ltv"],
    marker="x", color="#4CAF50", linewidth=2,
)
ax_ltv.fill_between(
    ltv_trend["months_since_first_purchase"],
    ltv_trend["avg_cumulative_ltv"],
    alpha=0.12, color="#4CAF50",
)
ax_ltv.set_title("C  |  Avg Cumulative LTV Over Time (All Cohorts)", loc="left", pad=8)
ax_ltv.set_xlabel("Months Since First Purchase")
ax_ltv.set_ylabel("Avg Cumulative LTV (BRL)")
ax_ltv.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_ltv.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D (bottom-left): Cohort size (number of new customers per cohort)
# ---------------------------------------------------------------------------
ax_size = fig.add_subplot(3, 2, 5)

cohort_sizes = (
    df_retention[df_retention["months_since_first_purchase"] == 0]
    .sort_values("cohort_month")[["cohort_month", "returned_customers"]]
    .rename(columns={"returned_customers": "cohort_size"})
)

ax_size.bar(
    cohort_sizes["cohort_month"].dt.strftime("%Y-%m"),
    cohort_sizes["cohort_size"],
    color="#9C27B0", width=0.7,
)
ax_size.set_title("D  |  New Customer Acquisition by Cohort Month", loc="left", pad=8)
ax_size.set_xlabel("Cohort Month")
ax_size.set_ylabel("New Customers")
ax_size.tick_params(axis="x", rotation=45)
ax_size.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_size.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel E (bottom-right): LTV vs. cohort size scatter
# ---------------------------------------------------------------------------
ax_scatter = fig.add_subplot(3, 2, 6)

# Join cohort size with peak LTV per cohort
ltv_by_cohort = (
    df_ltv.groupby("cohort_month")["avg_cumulative_ltv"]
    .max()
    .reset_index()
    .rename(columns={"avg_cumulative_ltv": "peak_ltv"})
)
cohort_sizes_m = cohort_sizes.copy()
cohort_sizes_m["cohort_month"] = pd.to_datetime(cohort_sizes_m["cohort_month"])

merged = pd.merge(cohort_sizes_m, ltv_by_cohort, on="cohort_month", how="inner")

ax_scatter.scatter(
    merged["cohort_size"], merged["peak_ltv"],
    color="#FF9800", edgecolors="#E65100", linewidth=0.8, s=60, zorder=3,
)
ax_scatter.set_title("E  |  Cohort Size vs. Peak Cumulative LTV", loc="left", pad=8)
ax_scatter.set_xlabel("Cohort Size (New Customers)")
ax_scatter.set_ylabel("Peak Avg Cumulative LTV (BRL)")
ax_scatter.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_scatter.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_scatter.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.98])
save_figure(fig, "02_cohort_dashboard.png")
plt.show()
