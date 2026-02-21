# =============================================================================
# Dashboard 08 — Rule-Based Outlier Detection
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Order-Level Outlier Detection Dashboard  (IQR Method)",
    fontsize=16, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
c_norm    = "#90A4AE"
c_outlier = "#F44336"

# ---------------------------------------------------------------------------
# Panel A (top-left): Revenue distribution with outlier fence
# ---------------------------------------------------------------------------
ax_hist_rev = fig.add_subplot(2, 3, 1)

# Cap x-axis at 99th percentile for readability; outliers still counted
p99_rev = df_merged["total_order_value"].quantile(0.99)
plot_rev = df_merged["total_order_value"].clip(upper=p99_rev)

ax_hist_rev.hist(
    plot_rev[~df_merged["is_revenue_outlier"]],
    bins=60, color=c_norm, alpha=0.8, label="Normal",
)
ax_hist_rev.hist(
    plot_rev[df_merged["is_revenue_outlier"]].clip(upper=p99_rev),
    bins=30, color=c_outlier, alpha=0.8, label=f"Outlier (>{rev_fence:,.0f})",
)
ax_hist_rev.axvline(rev_fence, color="#FF9800", linewidth=1.6, linestyle="--",
                    label=f"IQR fence: {rev_fence:,.0f}")
ax_hist_rev.set_title("A  |  Order Value Distribution with IQR Fence", loc="left", pad=8)
ax_hist_rev.set_xlabel("Order Value (BRL)  [capped at P99]")
ax_hist_rev.set_ylabel("Number of Orders")
ax_hist_rev.legend(fontsize=8)
ax_hist_rev.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# ---------------------------------------------------------------------------
# Panel B (top-centre): Revenue scatter — inliers vs. outliers
# ---------------------------------------------------------------------------
ax_scatter_rev = fig.add_subplot(2, 3, 2)

n_plot = min(5000, len(df_merged))
df_sample = df_merged.sample(n_plot, random_state=42)
colours_scatter = [c_outlier if o else c_norm
                   for o in df_sample["is_revenue_outlier"]]

ax_scatter_rev.scatter(
    range(len(df_sample)),
    df_sample["total_order_value"].clip(upper=p99_rev),
    c=colours_scatter, s=4, alpha=0.4, zorder=2,
)
ax_scatter_rev.axhline(rev_fence, color="#FF9800", linewidth=1.4,
                        linestyle="--", label="IQR fence")
ax_scatter_rev.set_title(
    f"B  |  Revenue Outlier Scatter  (sample n={n_plot:,})", loc="left", pad=8
)
ax_scatter_rev.set_xlabel("Order index (sampled)")
ax_scatter_rev.set_ylabel("Order Value (BRL)  [capped at P99]")
ax_scatter_rev.legend(fontsize=8)
ax_scatter_rev.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# ---------------------------------------------------------------------------
# Panel C (top-right): KPI scorecard
# ---------------------------------------------------------------------------
ax_kpi = fig.add_subplot(2, 3, 3)
ax_kpi.axis("off")

delay_fence_str = f"{delay_fence:.1f}d" if delay_fence is not None else "N/A"
kpi_items = [
    ("Total Orders Analysed",   f"{n_total:,}"),
    ("Revenue Outlier Fence",   f"{rev_fence:,.2f} BRL"),
    ("Revenue Outliers",        f"{n_rev_outliers:,}  ({n_rev_outliers/n_total*100:.2f}%)"),
    ("Delay Outlier Fence",     delay_fence_str),
    ("Delay Outliers",          f"{n_delay_outliers:,}  ({n_delay_outliers/n_total*100:.2f}%)"),
    ("Dual Outliers",           f"{n_dual_outliers:,}"),
]

ax_kpi.text(0.5, 1.0, "C  |  Outlier Summary",
            transform=ax_kpi.transAxes, ha="center",
            fontsize=11, fontweight="bold")
y = 0.88
for label, val in kpi_items:
    is_risk = "Outlier" in label or "Dual" in label
    ax_kpi.text(0.05, y, label + ":", transform=ax_kpi.transAxes,
                ha="left", fontsize=9.5, color="#555")
    ax_kpi.text(0.95, y, val, transform=ax_kpi.transAxes,
                ha="right", fontsize=9.5, fontweight="bold",
                color="#F44336" if is_risk else "#212121")
    y -= 0.15

# ---------------------------------------------------------------------------
# Panel D (bottom-left): Revenue outlier count by state
# ---------------------------------------------------------------------------
ax_state_rev = fig.add_subplot(2, 3, 4)

state_outliers = (
    df_merged.groupby("customer_state")["is_revenue_outlier"]
    .sum()
    .sort_values(ascending=True)
    .tail(15)
    .astype(int)
)
ax_state_rev.barh(
    state_outliers.index, state_outliers.values, color=c_outlier
)
ax_state_rev.set_title("D  |  Revenue Outlier Count by State (top 15)", loc="left", pad=8)
ax_state_rev.set_xlabel("Outlier Orders")
ax_state_rev.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_state_rev.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel E (bottom-centre): Delay distribution with fence (for delayed orders only)
# ---------------------------------------------------------------------------
ax_hist_delay = fig.add_subplot(2, 3, 5)

if delay_fence is not None and len(delayed_df) > 0:
    p99_delay = delayed_df["delay_days"].quantile(0.99)
    ax_hist_delay.hist(
        delayed_df.loc[~df_merged.loc[delayed_df.index, "is_delay_outlier"],
                       "delay_days"].clip(upper=p99_delay),
        bins=40, color=c_norm, alpha=0.8, label="Normal delay",
    )
    ax_hist_delay.hist(
        delayed_df.loc[df_merged.loc[delayed_df.index, "is_delay_outlier"],
                       "delay_days"].clip(upper=p99_delay),
        bins=20, color=c_outlier, alpha=0.8, label=f"Extreme delay (>{delay_fence:.0f}d)",
    )
    ax_hist_delay.axvline(delay_fence, color="#FF9800", linewidth=1.6, linestyle="--")
else:
    ax_hist_delay.text(0.5, 0.5, "No delay outlier data", ha="center", va="center",
                       transform=ax_hist_delay.transAxes)

ax_hist_delay.set_title("E  |  Delay Duration Distribution (delayed orders only)", loc="left", pad=8)
ax_hist_delay.set_xlabel("Delay Days  [capped at P99]")
ax_hist_delay.set_ylabel("Orders")
ax_hist_delay.legend(fontsize=8)

# ---------------------------------------------------------------------------
# Panel F (bottom-right): Outlier rate by state (revenue outliers / total)
# ---------------------------------------------------------------------------
ax_rate = fig.add_subplot(2, 3, 6)

state_totals = df_merged.groupby("customer_state").size().rename("total")
state_out_rate = (
    df_merged.groupby("customer_state")["is_revenue_outlier"]
    .mean()
    .mul(100)
    .sort_values(ascending=True)
    .tail(15)
)
overall_out_rate = n_rev_outliers / n_total * 100
ax_rate.barh(
    state_out_rate.index,
    state_out_rate.values,
    color=["#F44336" if v > overall_out_rate else "#90A4AE"
           for v in state_out_rate.values],
)
ax_rate.axvline(overall_out_rate, color="#FF9800", linewidth=1.4, linestyle="--",
                label=f"Overall: {overall_out_rate:.2f}%")
ax_rate.set_title("F  |  Revenue Outlier Rate by State (%)", loc="left", pad=8)
ax_rate.set_xlabel("Outlier Rate (%)")
ax_rate.legend(fontsize=8)
ax_rate.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_rate.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "08_outlier_dashboard.png")
plt.show()
