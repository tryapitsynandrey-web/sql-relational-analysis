# =============================================================================
# Dashboard 10 — Executive Synthesis Dashboard
# =============================================================================
fig = plt.figure(figsize=(18, 16))
fig.suptitle(
    "Olist E-Commerce — Executive Analytical Dashboard",
    fontsize=17, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Panel A (top, wide): Executive KPI scorecard (text table)
# ---------------------------------------------------------------------------
ax_kpi = fig.add_subplot(4, 2, (1, 2))
ax_kpi.axis("off")

kpi_rows = list(kpi_summary.items())
n_cols = 5
n_rows_kpi = 2

ax_kpi.text(0.0, 1.02, "A  |  Platform Performance Snapshot", transform=ax_kpi.transAxes,
            fontsize=12, fontweight="bold")

cell_w = 1.0 / n_cols
cell_h = 0.45

for col_i, (label, val) in enumerate(kpi_rows[:n_cols]):
    x = col_i * cell_w + cell_w / 2
    ax_kpi.text(x, 0.92, label, transform=ax_kpi.transAxes,
                ha="center", fontsize=8.5, color="#555")
    ax_kpi.text(x, 0.68, val, transform=ax_kpi.transAxes,
                ha="center", fontsize=14, fontweight="bold", color="#212121")

for col_i, (label, val) in enumerate(kpi_rows[n_cols:n_cols * 2]):
    x = col_i * cell_w + cell_w / 2
    is_risk = "Delay" in label or "Cancel" in label or "Gap" in label
    ax_kpi.text(x, 0.42, label, transform=ax_kpi.transAxes,
                ha="center", fontsize=8.5, color="#555")
    ax_kpi.text(x, 0.18, val, transform=ax_kpi.transAxes,
                ha="center", fontsize=14, fontweight="bold",
                color="#F44336" if is_risk else "#212121")

# ---------------------------------------------------------------------------
# Panel B (second row left): Revenue trend — high-level sparkline
# ---------------------------------------------------------------------------
ax_rev = fig.add_subplot(4, 2, 3)

ax_rev.fill_between(
    df_monthly["revenue_month"],
    df_monthly["total_revenue"],
    alpha=0.2, color="#2196F3",
)
ax_rev.plot(
    df_monthly["revenue_month"],
    df_monthly["total_revenue"],
    color="#2196F3", linewidth=2,
)
ax_rev.set_title("B  |  Monthly Revenue Trend", loc="left", pad=8)
ax_rev.set_ylabel("Revenue (BRL)")
ax_rev.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
ax_rev.set_xlabel("")
ax_rev.tick_params(axis="x", rotation=30)
ax_rev.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel C (second row right): SLA donut
# ---------------------------------------------------------------------------
ax_sla = fig.add_subplot(4, 2, 4)

total_del    = int(df_sla_exec["total_deliveries"].iloc[0])
total_delay  = int(df_sla_exec["total_delayed_orders"].iloc[0])

wedges, _, autotexts = ax_sla.pie(
    [total_del - total_delay, total_delay],
    labels=["On-Time", "Delayed"],
    autopct="%1.1f%%",
    colors=["#4CAF50", "#F44336"],
    startangle=90,
    wedgeprops=dict(width=0.52),
    textprops=dict(fontsize=10),
)
for at in autotexts:
    at.set_fontweight("bold")
centre_text = f"{delayed_rate_exec:.1f}%\nDelayed"
ax_sla.text(0, 0, centre_text, ha="center", va="center",
            fontsize=12, fontweight="bold", color="#F44336")
ax_sla.set_title("C  |  Delivery SLA Status", loc="left", pad=8)

# ---------------------------------------------------------------------------
# Panel D (third row left): Review score distribution (compact)
# ---------------------------------------------------------------------------
ax_rev_score = fig.add_subplot(4, 2, 5)

score_colors = {1: "#F44336", 2: "#FF7043", 3: "#FF9800", 4: "#8BC34A", 5: "#4CAF50"}
bar_cols = [score_colors.get(int(s), "#9E9E9E") for s in df_scores["review_score"]]
ax_rev_score.bar(
    df_scores["review_score"].astype(str),
    df_scores["pct_of_total"],
    color=bar_cols, width=0.6,
)
ax_rev_score.set_title("D  |  Review Score Distribution (%)", loc="left", pad=8)
ax_rev_score.set_xlabel("Score")
ax_rev_score.set_ylabel("% of Reviews")
ax_rev_score.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel E (third row right): Payment method revenue share
# ---------------------------------------------------------------------------
ax_pay = fig.add_subplot(4, 2, 6)

p_colors = {"credit_card": "#2196F3", "boleto": "#FF9800",
            "voucher": "#9C27B0", "debit_card": "#4CAF50"}
pie_cols = [p_colors.get(p, "#607D8B") for p in df_payments["payment_type"]]
ax_pay.pie(
    df_payments["total_payment_value"],
    labels=df_payments["payment_type"].str.replace("_", " ").str.title(),
    autopct="%1.1f%%",
    colors=pie_cols,
    startangle=90,
    textprops=dict(fontsize=9),
)
ax_pay.set_title("E  |  Revenue Share by Payment Method", loc="left", pad=8)

# ---------------------------------------------------------------------------
# Panel F (bottom, wide): Risk matrix — 5 themes × 2 dimensions
# ---------------------------------------------------------------------------
ax_risk = fig.add_subplot(4, 2, (7, 8))
ax_risk.axis("off")

risk_table = [
    # Theme, Lead KPI, Signal, Priority (1=High, 3=Low)
    ("Revenue & AOV",     f"AOV: {avg_aov:,.0f} BRL",       "Flat AOV — volume-driven growth only",              2),
    ("Retention & LTV",   f"M1 Ret: {avg_m1_ret:.1f}%" if avg_m1_ret else "M1 Ret: N/A",
                          "Below-avg retention for majority of cohorts",       1),
    ("Delivery SLA",      f"Delay: {delayed_rate_exec:.1f}%", "Systematic ETA underestimation across network",      1),
    ("Review Scores",     f"Score gap: {score_gap:.2f}" if score_gap else "Gap: N/A",
                          "Delayed orders drive 1-star reviews — recoverable", 1),
    ("Payment Risk",      f"CC share: {cc_share:.1f}%" if cc_share else "CC: N/A",
                          "Single-rail revenue concentration risk",             2),
]

ax_risk.text(0.5, 1.02, "F  |  Cross-Domain Risk Summary",
             transform=ax_risk.transAxes, ha="center",
             fontsize=12, fontweight="bold")

col_headers = ["Analytical Theme", "Lead KPI", "Key Risk Signal", "Priority"]
col_xs      = [0.0, 0.22, 0.44, 0.90]
header_y    = 0.90
ax_risk.text(col_xs[0], header_y, col_headers[0], transform=ax_risk.transAxes,
             fontsize=9, fontweight="bold", color="#333")
ax_risk.text(col_xs[1], header_y, col_headers[1], transform=ax_risk.transAxes,
             fontsize=9, fontweight="bold", color="#333")
ax_risk.text(col_xs[2], header_y, col_headers[2], transform=ax_risk.transAxes,
             fontsize=9, fontweight="bold", color="#333")
ax_risk.text(col_xs[3], header_y, col_headers[3], transform=ax_risk.transAxes,
             fontsize=9, fontweight="bold", color="#333", ha="center")

priority_color = {1: "#F44336", 2: "#FF9800", 3: "#4CAF50"}
priority_label = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}

for row_i, (theme, kpi_val, signal, priority) in enumerate(risk_table):
    y_row = 0.76 - row_i * 0.14
    ax_risk.text(col_xs[0], y_row, theme,     transform=ax_risk.transAxes, fontsize=9)
    ax_risk.text(col_xs[1], y_row, kpi_val,   transform=ax_risk.transAxes, fontsize=9, fontweight="bold")
    ax_risk.text(col_xs[2], y_row, signal,    transform=ax_risk.transAxes, fontsize=8.5, color="#444")
    ax_risk.text(col_xs[3], y_row, priority_label[priority],
                 transform=ax_risk.transAxes, fontsize=9, fontweight="bold",
                 color=priority_color[priority], ha="center")

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "10_executive_dashboard.png")
plt.show()
