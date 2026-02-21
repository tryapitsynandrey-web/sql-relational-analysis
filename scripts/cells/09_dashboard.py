# =============================================================================
# Dashboard 09 — Rule-Based Customer Segmentation (Spend Tiers)
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Customer Spend-Tier Segmentation Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

colors_list = [tier_colors.get(t, "#607D8B") for t in df_seg_base["ltv_tier"]]

# ---------------------------------------------------------------------------
# Panel A (top-left): Cohort count per tier — shows tier distribution
# ---------------------------------------------------------------------------
ax_count = fig.add_subplot(2, 3, 1)

tier_counts = df_seg_base["ltv_tier"].value_counts().reindex(tier_order)
ax_count.bar(
    tier_counts.index,
    tier_counts.values,
    color=[tier_colors[t] for t in tier_counts.index],
    width=0.55,
)
for i, (tier, cnt) in enumerate(tier_counts.items()):
    ax_count.text(i, cnt + 0.1, str(cnt), ha="center", va="bottom",
                  fontsize=11, fontweight="bold")

ax_count.set_title("A  |  Cohort Count by Spend Tier", loc="left", pad=8)
ax_count.set_ylabel("Number of Cohorts")
ax_count.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel B (top-centre): Average peak LTV by tier
# ---------------------------------------------------------------------------
ax_ltv_tier = fig.add_subplot(2, 3, 2)

avg_ltv_by_tier = (
    df_seg_base.groupby("ltv_tier")["peak_avg_ltv"]
    .mean()
    .reindex(tier_order)
)
bars_ltv = ax_ltv_tier.bar(
    avg_ltv_by_tier.index,
    avg_ltv_by_tier.values,
    color=[tier_colors[t] for t in avg_ltv_by_tier.index],
    width=0.55,
)
for bar, val in zip(bars_ltv, avg_ltv_by_tier.values):
    ax_ltv_tier.text(
        bar.get_x() + bar.get_width() / 2, val + 1,
        f"{val:,.0f}", ha="center", va="bottom",
        fontsize=11, fontweight="bold",
    )
ax_ltv_tier.set_title("B  |  Average Peak LTV by Tier (BRL)", loc="left", pad=8)
ax_ltv_tier.set_ylabel("Avg Peak Cumulative LTV (BRL)")
ax_ltv_tier.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_ltv_tier.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel C (top-right): Average month-1 retention by tier
# ---------------------------------------------------------------------------
ax_ret_tier = fig.add_subplot(2, 3, 3)

avg_ret_by_tier = (
    df_seg_base.groupby("ltv_tier")["month1_retention_pct"]
    .mean()
    .reindex(tier_order)
)
bars_ret = ax_ret_tier.bar(
    avg_ret_by_tier.index,
    avg_ret_by_tier.values,
    color=[tier_colors[t] for t in avg_ret_by_tier.index],
    width=0.55,
)
for bar, val in zip(bars_ret, avg_ret_by_tier.values):
    ax_ret_tier.text(
        bar.get_x() + bar.get_width() / 2, val + 0.1,
        f"{val:.1f}%", ha="center", va="bottom",
        fontsize=11, fontweight="bold",
    )
ax_ret_tier.set_title("C  |  Avg Month-1 Retention Rate by Tier (%)", loc="left", pad=8)
ax_ret_tier.set_ylabel("Month-1 Retention Rate (%)")
ax_ret_tier.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D (bottom-left, wide): LTV scatter coloured by tier — over time
# ---------------------------------------------------------------------------
ax_scatter = fig.add_subplot(2, 3, (4, 5))

for tier in tier_order:
    grp = df_seg_base[df_seg_base["ltv_tier"] == tier]
    ax_scatter.scatter(
        grp["cohort_month"],
        grp["peak_avg_ltv"],
        color=tier_colors[tier],
        label=tier,
        s=80, zorder=3,
    )

ax_scatter.set_title(
    "D  |  Peak Avg Cumulative LTV by Cohort Month (coloured by tier)", loc="left", pad=8
)
ax_scatter.set_xlabel("Cohort Month")
ax_scatter.set_ylabel("Peak Avg LTV (BRL)")
ax_scatter.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_scatter.legend(fontsize=9)
ax_scatter.grid(True, linestyle="--", alpha=0.4)

# ---------------------------------------------------------------------------
# Panel E (bottom-right): Cohort size by tier (total customers per tier)
# ---------------------------------------------------------------------------
ax_size = fig.add_subplot(2, 3, 6)

total_size_by_tier = (
    df_seg_base.groupby("ltv_tier")["cohort_size"]
    .sum()
    .reindex(tier_order)
)
ax_size.bar(
    total_size_by_tier.index,
    total_size_by_tier.values,
    color=[tier_colors[t] for t in total_size_by_tier.index],
    width=0.55,
)
for i, (tier, val) in enumerate(total_size_by_tier.items()):
    ax_size.text(i, val + 10, f"{int(val):,}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")

ax_size.set_title("E  |  Total Cohort Size by Tier", loc="left", pad=8)
ax_size.set_ylabel("Total Customers")
ax_size.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_size.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_size.annotate(
    "Tier boundaries: P33 and P67 of observed peak LTV distribution.",
    xy=(0.01, 0.02), xycoords="axes fraction",
    fontsize=8.5, color="#666", style="italic",
)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "09_segmentation_dashboard.png")
plt.show()
