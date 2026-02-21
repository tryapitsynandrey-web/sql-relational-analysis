# =============================================================================
# Dashboard 01 — Revenue, AOV & Geographic GMV
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Revenue & AOV Dashboard",
    fontsize=16, fontweight="bold", y=0.98,
)

# ---------------------------------------------------------------------------
# Panel A (top, wide): Monthly Revenue Trend with AOV overlay
# ---------------------------------------------------------------------------
ax_rev   = fig.add_subplot(3, 2, (1, 2))   # spans both columns

color_rev = "#2196F3"
color_aov = "#FF9800"

ax_rev.fill_between(
    df_monthly_revenue["revenue_month"],
    df_monthly_revenue["total_revenue"],
    alpha=0.18, color=color_rev,
)
ax_rev.plot(
    df_monthly_revenue["revenue_month"],
    df_monthly_revenue["total_revenue"],
    marker="o", color=color_rev, linewidth=2, label="Total Revenue (BRL)",
)
ax_rev.set_title("A  |  Monthly Revenue Trend with Average Order Value (AOV)", loc="left", pad=8)
ax_rev.set_xlabel("Month")
ax_rev.set_ylabel("Total Revenue (BRL)", color=color_rev)
ax_rev.tick_params(axis="y", labelcolor=color_rev)
ax_rev.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# Overlay AOV on a secondary y-axis
ax_aov = ax_rev.twinx()
ax_aov.plot(
    df_monthly_revenue["revenue_month"],
    df_monthly_revenue["average_order_value"],
    marker="s", linestyle="--", color=color_aov, linewidth=1.8, label="AOV (BRL)",
)
ax_aov.set_ylabel("Average Order Value (BRL)", color=color_aov)
ax_aov.tick_params(axis="y", labelcolor=color_aov)
ax_aov.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# Annotate overall revenue peak
peak_idx = df_monthly_revenue["total_revenue"].idxmax()
peak_row = df_monthly_revenue.loc[peak_idx]
ax_rev.annotate(
    f"Peak: {peak_row['total_revenue']:,.0f}",
    xy=(peak_row["revenue_month"], peak_row["total_revenue"]),
    xytext=(0, 18), textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#555"),
    fontsize=9, color="#555",
)

# Combined legend
lines1, labels1 = ax_rev.get_legend_handles_labels()
lines2, labels2 = ax_aov.get_legend_handles_labels()
ax_rev.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
ax_rev.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_aov.grid(False)

# ---------------------------------------------------------------------------
# Panel B (middle, wide): Top 10 Categories by Revenue — horizontal bar
# ---------------------------------------------------------------------------
ax_cat = fig.add_subplot(3, 2, (3, 4))

df_cat_sorted = df_top_categories.sort_values("total_revenue", ascending=True)
bars = ax_cat.barh(
    df_cat_sorted["category_english"].str.replace("_", " ").str.title(),
    df_cat_sorted["total_revenue"],
    color="#2196F3",
)
ax_cat.set_title("B  |  Top 10 Product Categories by Revenue (Delivered Orders)", loc="left", pad=8)
ax_cat.set_xlabel("Total Revenue (BRL)")
ax_cat.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))

# Annotate the top bar with its revenue value
top_val = df_cat_sorted["total_revenue"].iloc[-1]
ax_cat.text(
    top_val * 0.98,
    len(df_cat_sorted) - 1,
    f"  {top_val/1e6:.2f}M",
    va="center", ha="right", fontsize=9, color="white", fontweight="bold",
)
ax_cat.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_cat.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel C (bottom-left): Monthly Order Volume — captures seasonality signal
# ---------------------------------------------------------------------------
ax_vol = fig.add_subplot(3, 2, 5)
ax_vol.bar(
    df_monthly_revenue["revenue_month"],
    df_monthly_revenue["total_orders"],
    color="#9C27B0", width=20,
)
ax_vol.set_title("C  |  Monthly Order Volume", loc="left", pad=8)
ax_vol.set_xlabel("Month")
ax_vol.set_ylabel("Orders")
ax_vol.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_vol.tick_params(axis="x", rotation=45)
ax_vol.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D (bottom-right): GMV by State — gradient intensity colouring
# ---------------------------------------------------------------------------
ax_state = fig.add_subplot(3, 2, 6)

df_state_sorted = df_top_states.sort_values("gmv", ascending=False).head(10)
gmv_vals = df_state_sorted["gmv"]

# Colour bars by GMV intensity using a single-hue gradient
norm = plt.Normalize(gmv_vals.min(), gmv_vals.max())
colors_state = plt.cm.Blues(norm(gmv_vals) * 0.6 + 0.35)

ax_state.bar(df_state_sorted["customer_state"], gmv_vals, color=colors_state)
ax_state.set_title("D  |  Top 10 States by GMV", loc="left", pad=8)
ax_state.set_xlabel("State")
ax_state.set_ylabel("GMV (BRL)")
ax_state.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
ax_state.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_state.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "01_revenue_dashboard.png")
plt.show()
