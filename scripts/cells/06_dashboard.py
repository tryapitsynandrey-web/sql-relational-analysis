# =============================================================================
# Dashboard 06 — Geographic Revenue & Delivery Risk Patterns
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Geographic Revenue & Delivery Risk Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

df_sorted_gmv   = df_geo.sort_values("gmv", ascending=False)
df_sorted_delay = df_geo.sort_values("delayed_rate_pct", ascending=False)

# ---------------------------------------------------------------------------
# Panel A (top, wide): GMV bar sorted descending — all states
# ---------------------------------------------------------------------------
ax_gmv = fig.add_subplot(3, 2, (1, 2))

norm = plt.Normalize(df_sorted_gmv["gmv"].min(), df_sorted_gmv["gmv"].max())
bar_colors_gmv = plt.cm.Blues(norm(df_sorted_gmv["gmv"]) * 0.65 + 0.25)

ax_gmv.bar(
    df_sorted_gmv["customer_state"],
    df_sorted_gmv["gmv"],
    color=bar_colors_gmv,
)

# Annotate GMV share on top 3
for _, row in df_sorted_gmv.head(3).iterrows():
    ax_gmv.annotate(
        f"{row['gmv_share_pct']:.1f}% of GMV",
        xy=(row["customer_state"], row["gmv"]),
        xytext=(0, 6), textcoords="offset points",
        ha="center", fontsize=8, color="#1565C0",
    )

ax_gmv.set_title("A  |  Total GMV by State (all delivered orders)", loc="left", pad=8)
ax_gmv.set_xlabel("Customer State")
ax_gmv.set_ylabel("GMV (BRL)")
ax_gmv.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
ax_gmv.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_gmv.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel B (middle-left): Delay rate by state — all states sorted
# ---------------------------------------------------------------------------
ax_delay = fig.add_subplot(3, 2, 3)

bar_cols_delay = [
    "#F44336" if r > median_delay else "#4CAF50"
    for r in df_sorted_delay["delayed_rate_pct"]
]
ax_delay.bar(
    df_sorted_delay["customer_state"],
    df_sorted_delay["delayed_rate_pct"],
    color=bar_cols_delay, width=0.7,
)
ax_delay.axhline(
    median_delay, color="#FF9800", linewidth=1.4, linestyle="--",
    label=f"Median: {median_delay:.1f}%",
)
ax_delay.set_title("B  |  Delay Rate by State  (red = above median)", loc="left", pad=8)
ax_delay.set_xlabel("State")
ax_delay.set_ylabel("Delayed Orders (%)")
ax_delay.legend(fontsize=9)
ax_delay.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_delay.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel C (middle-right): Delayed orders per 1,000 deliveries — normalised risk
# ---------------------------------------------------------------------------
ax_norm = fig.add_subplot(3, 2, 4)

df_geo["delay_per_1k"] = (
    df_geo["delayed_orders"] / df_geo["total_deliveries"] * 1000
).round(1)
df_norm_sorted = df_geo.sort_values("delay_per_1k", ascending=True)

ax_norm.barh(
    df_norm_sorted["customer_state"],
    df_norm_sorted["delay_per_1k"],
    color="#FF9800",
)
ax_norm.set_title("C  |  Delayed Orders per 1,000 Deliveries", loc="left", pad=8)
ax_norm.set_xlabel("Delayed Orders / 1,000")
ax_norm.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_norm.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel D (bottom-left): 2×2 Risk quadrant — GMV vs. Delay Rate
# ---------------------------------------------------------------------------
ax_quad = fig.add_subplot(3, 2, 5)

quadrant_colors = {
    "High GMV / High Delay": "#F44336",
    "High GMV / Low Delay":  "#4CAF50",
    "Low GMV / High Delay":  "#FF9800",
    "Low GMV / Low Delay":   "#90A4AE",
}
for q, grp in df_geo.groupby("quadrant"):
    ax_quad.scatter(
        grp["gmv"] / 1e6,
        grp["delayed_rate_pct"],
        label=q,
        color=quadrant_colors.get(q, "#607D8B"),
        s=70, zorder=3,
    )

# Label top-risk and top-value states
for _, row in df_geo.nlargest(3, "gmv").iterrows():
    ax_quad.annotate(row["customer_state"],
                     xy=(row["gmv"] / 1e6, row["delayed_rate_pct"]),
                     xytext=(4, 2), textcoords="offset points", fontsize=8)
for _, row in df_geo.nlargest(2, "delayed_rate_pct").iterrows():
    ax_quad.annotate(row["customer_state"],
                     xy=(row["gmv"] / 1e6, row["delayed_rate_pct"]),
                     xytext=(4, 2), textcoords="offset points", fontsize=8)

ax_quad.axhline(median_delay,  color="#FF9800", linewidth=1, linestyle="--", alpha=0.6)
ax_quad.axvline(median_gmv / 1e6, color="#2196F3", linewidth=1, linestyle="--", alpha=0.6)
ax_quad.set_title("D  |  GMV vs. Delay Rate Risk Quadrant", loc="left", pad=8)
ax_quad.set_xlabel("GMV (M BRL)")
ax_quad.set_ylabel("Delayed Rate (%)")
ax_quad.legend(fontsize=8, loc="upper right")
ax_quad.grid(True, linestyle="--", alpha=0.4)

# ---------------------------------------------------------------------------
# Panel E (bottom-right): Unique customers per state (top 10)
# ---------------------------------------------------------------------------
ax_cust = fig.add_subplot(3, 2, 6)

df_top_cust = df_geo.sort_values("unique_customers", ascending=True).tail(10)
ax_cust.barh(
    df_top_cust["customer_state"],
    df_top_cust["unique_customers"],
    color="#9C27B0",
)
ax_cust.set_title("E  |  Top 10 States by Unique Customer Count", loc="left", pad=8)
ax_cust.set_xlabel("Unique Customers")
ax_cust.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_cust.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_cust.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "06_geographic_dashboard.png")
plt.show()
