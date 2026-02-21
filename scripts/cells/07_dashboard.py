# =============================================================================
# Dashboard 07 — Time-Series Trends & Seasonality
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Revenue Time-Series: Trends, Momentum & Seasonality",
    fontsize=16, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Panel A (top, wide): Revenue vs. 3M rolling average — trend context
# ---------------------------------------------------------------------------
ax_trend = fig.add_subplot(3, 2, (1, 2))

ax_trend.fill_between(
    df_monthly["revenue_month"],
    df_monthly["total_revenue"],
    alpha=0.15, color="#2196F3",
)
ax_trend.plot(
    df_monthly["revenue_month"],
    df_monthly["total_revenue"],
    color="#2196F3", linewidth=1.8, label="Monthly Revenue",
)
ax_trend.plot(
    df_monthly["revenue_month"],
    df_monthly["revenue_rolling_3m"],
    color="#FF9800", linewidth=2.2, linestyle="--", label="3-Month Rolling Average",
)

# Annotate peak month
peak_idx = df_monthly["total_revenue"].idxmax()
peak_row = df_monthly.loc[peak_idx]
ax_trend.annotate(
    f"Peak: {peak_row['total_revenue']:,.0f}",
    xy=(peak_row["revenue_month"], peak_row["total_revenue"]),
    xytext=(0, 14), textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#555"),
    fontsize=9, color="#555",
)

ax_trend.set_title("A  |  Monthly Revenue vs. 3-Month Rolling Average", loc="left", pad=8)
ax_trend.set_xlabel("Month")
ax_trend.set_ylabel("Revenue (BRL)")
ax_trend.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.2f}M"))
ax_trend.legend(fontsize=9)
ax_trend.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel B (middle-left): Month-over-month revenue change %
# ---------------------------------------------------------------------------
ax_mom = fig.add_subplot(3, 2, 3)

mom_vals = df_monthly["revenue_mom_pct"].dropna()
mom_months = df_monthly.loc[mom_vals.index, "revenue_month"]
bar_cols_mom = ["#4CAF50" if v >= 0 else "#F44336" for v in mom_vals]

ax_mom.bar(mom_months, mom_vals, color=bar_cols_mom, width=20)
ax_mom.axhline(0, color="#333", linewidth=0.8)
ax_mom.set_title("B  |  Month-over-Month Revenue Change (%)", loc="left", pad=8)
ax_mom.set_xlabel("Month")
ax_mom.set_ylabel("MoM Change (%)")
ax_mom.tick_params(axis="x", rotation=45)
ax_mom.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel C (middle-right): MoM order volume change
# ---------------------------------------------------------------------------
ax_vol_mom = fig.add_subplot(3, 2, 4)

vol_mom_vals   = df_monthly["orders_mom_pct"].dropna()
vol_mom_months = df_monthly.loc[vol_mom_vals.index, "revenue_month"]
bar_cols_vol   = ["#4CAF50" if v >= 0 else "#F44336" for v in vol_mom_vals]

ax_vol_mom.bar(vol_mom_months, vol_mom_vals, color=bar_cols_vol, width=20)
ax_vol_mom.axhline(0, color="#333", linewidth=0.8)
ax_vol_mom.set_title("C  |  Month-over-Month Order Volume Change (%)", loc="left", pad=8)
ax_vol_mom.set_xlabel("Month")
ax_vol_mom.set_ylabel("MoM Change (%)")
ax_vol_mom.tick_params(axis="x", rotation=45)
ax_vol_mom.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D (bottom-left): Seasonality index by month
# ---------------------------------------------------------------------------
ax_season = fig.add_subplot(3, 2, 5)

si_clean = df_monthly.dropna(subset=["seasonality_index"])
bar_cols_si = [
    "#2196F3" if v >= 1 else "#90A4AE"
    for v in si_clean["seasonality_index"]
]
ax_season.bar(
    si_clean["revenue_month"],
    si_clean["seasonality_index"],
    color=bar_cols_si, width=20,
)
ax_season.axhline(1.0, color="#FF9800", linewidth=1.4, linestyle="--",
                  label="Index = 1.0 (neutral)")
ax_season.set_title("D  |  Seasonality Index (Revenue / 12M Rolling Mean)", loc="left", pad=8)
ax_season.set_xlabel("Month")
ax_season.set_ylabel("Seasonality Index")
ax_season.tick_params(axis="x", rotation=45)
ax_season.legend(fontsize=9)
ax_season.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_season.annotate(
    "Index > 1.0: above-average month  |  Index < 1.0: below average",
    xy=(0.01, 0.04), xycoords="axes fraction", fontsize=8.5, color="#555", style="italic",
)

# ---------------------------------------------------------------------------
# Panel E (bottom-right): Average revenue by month-of-year (calendar seasonality)
# ---------------------------------------------------------------------------
ax_cal = fig.add_subplot(3, 2, 6)

month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_avg = (
    df_monthly.groupby("month_of_year")["total_revenue"]
    .mean()
    .reindex(range(1, 13), fill_value=0)
)
overall_monthly_mean = monthly_avg.mean()

bar_cols_cal = [
    "#2196F3" if v >= overall_monthly_mean else "#90A4AE"
    for v in monthly_avg
]
ax_cal.bar(month_labels, monthly_avg, color=bar_cols_cal)
ax_cal.axhline(overall_monthly_mean, color="#FF9800", linewidth=1.4, linestyle="--",
               label=f"Overall avg: {overall_monthly_mean:,.0f}")
ax_cal.set_title("E  |  Avg Revenue by Calendar Month (all years)", loc="left", pad=8)
ax_cal.set_xlabel("Calendar Month")
ax_cal.set_ylabel("Avg Revenue (BRL)")
ax_cal.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.2f}M"))
ax_cal.legend(fontsize=9)
ax_cal.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_cal.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "07_time_series_dashboard.png")
plt.show()
