# =============================================================================
# Dashboard 05 — Payment Type Behavior & Cancellation Risk
# =============================================================================
import matplotlib.patches as mpatches  # Required for legend patch labels in panel E
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Payment Method Behavior & Cancellation Risk Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

payment_colors = {
    "credit_card": "#2196F3",
    "boleto":      "#FF9800",
    "voucher":     "#9C27B0",
    "debit_card":  "#4CAF50",
}
default_color = "#607D8B"


def _pcolors(df, col="payment_type"):
    """Map payment type strings to their designated colours."""
    return [payment_colors.get(p, default_color) for p in df[col]]


# ---------------------------------------------------------------------------
# Panel A (top-left): Order volume — horizontal bar, sorted descending
# ---------------------------------------------------------------------------
ax_vol = fig.add_subplot(3, 2, 1)

df_vol_sorted = df_payment_usage.sort_values("total_orders_used", ascending=True)
ax_vol.barh(
    df_vol_sorted["payment_type"].str.replace("_", " ").str.title(),
    df_vol_sorted["total_orders_used"],
    color=_pcolors(df_vol_sorted),
    height=0.55,
)
ax_vol.set_title("A  |  Order Volume by Payment Method", loc="left", pad=8)
ax_vol.set_xlabel("Number of Orders")
ax_vol.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_vol.grid(True, axis="x", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel B (top-right): Revenue share — pie chart
# ---------------------------------------------------------------------------
ax_pie = fig.add_subplot(3, 2, 2)

pie_colors = _pcolors(df_payment_usage)
wedges, texts, autotexts = ax_pie.pie(
    df_payment_usage["total_payment_value"],
    labels=df_payment_usage["payment_type"].str.replace("_", " ").str.title(),
    autopct="%1.1f%%",
    colors=pie_colors,
    startangle=90,
    textprops=dict(fontsize=9),
)
for at in autotexts:
    at.set_fontweight("bold")
ax_pie.set_title("B  |  Revenue Share by Payment Method", loc="left", pad=8)

# ---------------------------------------------------------------------------
# Panel C (middle-left): Average transaction value with overall average reference
# ---------------------------------------------------------------------------
ax_atv = fig.add_subplot(3, 2, 3)

df_atv = df_payment_usage.sort_values("avg_transaction_value", ascending=False)
bars_atv = ax_atv.bar(
    df_atv["payment_type"].str.replace("_", " ").str.title(),
    df_atv["avg_transaction_value"],
    color=_pcolors(df_atv), width=0.5,
)

overall_atv = (
    df_payment_usage["total_payment_value"].sum()
    / df_payment_usage["total_orders_used"].sum()
)
ax_atv.axhline(overall_atv, color="#FF9800", linewidth=1.4, linestyle="--",
               label=f"Overall avg: {overall_atv:.0f} BRL")

for bar, val in zip(bars_atv, df_atv["avg_transaction_value"]):
    ax_atv.text(
        bar.get_x() + bar.get_width() / 2,
        val + 1,
        f"{val:.0f}",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
    )

ax_atv.set_title("C  |  Avg Transaction Value by Payment Method (BRL)", loc="left", pad=8)
ax_atv.set_ylabel("Avg Transaction Value (BRL)")
ax_atv.legend(fontsize=9)
ax_atv.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D (middle-right): Average installments per payment type
# ---------------------------------------------------------------------------
ax_inst = fig.add_subplot(3, 2, 4)

df_inst = df_payment_usage.sort_values("avg_installments", ascending=False)
bars_inst = ax_inst.bar(
    df_inst["payment_type"].str.replace("_", " ").str.title(),
    df_inst["avg_installments"],
    color=_pcolors(df_inst), width=0.5,
)

for bar, val in zip(bars_inst, df_inst["avg_installments"]):
    ax_inst.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.05,
        f"{val:.1f}x",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
    )

ax_inst.set_title("D  |  Avg Installment Count by Payment Method", loc="left", pad=8)
ax_inst.set_ylabel("Avg Installments")
ax_inst.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel E (bottom, wide): Cancellation rate with risk zone shading
# ---------------------------------------------------------------------------
ax_cancel = fig.add_subplot(3, 2, (5, 6))

df_cancel_sorted = df_cancellations.sort_values("cancellation_rate_pct", ascending=False)
overall_cancel = (
    df_cancel_sorted["canceled_orders"].sum()
    / df_cancel_sorted["total_orders"].sum() * 100
)

cancel_bar_colors = [
    "#F44336" if r > overall_cancel * 1.25 else
    "#FF9800" if r > overall_cancel else
    "#4CAF50"
    for r in df_cancel_sorted["cancellation_rate_pct"]
]

bars_cancel = ax_cancel.bar(
    df_cancel_sorted["payment_type"].str.replace("_", " ").str.title(),
    df_cancel_sorted["cancellation_rate_pct"],
    color=cancel_bar_colors, width=0.5,
)

for bar, val, n in zip(
    bars_cancel,
    df_cancel_sorted["cancellation_rate_pct"],
    df_cancel_sorted["total_orders"],
):
    label_text = f"{val:.2f}%  ({n:,} orders)"
    ax_cancel.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.02,
        label_text,
        ha="center", va="bottom", fontsize=9,
    )

ax_cancel.axhline(overall_cancel, color="#FF9800", linewidth=1.4, linestyle="--",
                  label=f"Weighted avg: {overall_cancel:.2f}%")

max_cancel_rate = df_cancel_sorted["cancellation_rate_pct"].max()
ax_cancel.axhspan(
    overall_cancel * 1.25, max_cancel_rate * 1.15,
    alpha=0.07, color="#F44336",
)

red_patch   = mpatches.Patch(color="#F44336", label=">125% of avg (High Risk)")
amber_patch = mpatches.Patch(color="#FF9800", label=">100% of avg (Elevated)")
green_patch = mpatches.Patch(color="#4CAF50", label="Below avg (Healthy)")
ax_cancel.legend(handles=[red_patch, amber_patch, green_patch], fontsize=9, loc="upper right")

ax_cancel.set_title(
    "E  |  Cancellation Rate by Payment Type  (red = high risk | amber = elevated | green = healthy)",
    loc="left", pad=8,
)
ax_cancel.set_xlabel("Payment Method")
ax_cancel.set_ylabel("Cancellation Rate (%)")
ax_cancel.grid(True, axis="y", linestyle="--", alpha=0.5)
ax_cancel.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "05_payment_dashboard.png")
plt.show()
