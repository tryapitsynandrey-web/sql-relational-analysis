# =============================================================================
# Dashboard 04 — Review Score Drivers
# =============================================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "Olist Customer Review Score Driver Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Derived KPIs for annotations
# ---------------------------------------------------------------------------
score_1_series = df_score_dist.loc[df_score_dist["review_score"] == 1, "pct_of_total"]
pct_1_star     = float(score_1_series.values[0]) if len(score_1_series) else 0.0

score_5_series = df_score_dist.loc[df_score_dist["review_score"] == 5, "pct_of_total"]
pct_5_star     = float(score_5_series.values[0]) if len(score_5_series) else 0.0

delivery_idx   = df_delivery_scores.set_index("delivery_status")
score_on_time  = float(delivery_idx.loc["On-Time", "avg_review_score"]) if "On-Time" in delivery_idx.index else None
score_delayed  = float(delivery_idx.loc["Delayed", "avg_review_score"]) if "Delayed" in delivery_idx.index else None

# ---------------------------------------------------------------------------
# Panel A (top-left): Score distribution bar with % labels
# ---------------------------------------------------------------------------
ax_dist = fig.add_subplot(2, 3, 1)

score_colors = {1: "#F44336", 2: "#FF7043", 3: "#FF9800", 4: "#8BC34A", 5: "#4CAF50"}
bar_colors_dist = [score_colors.get(int(s), "#9E9E9E") for s in df_score_dist["review_score"]]

bars = ax_dist.bar(
    df_score_dist["review_score"].astype(str),
    df_score_dist["pct_of_total"],
    color=bar_colors_dist, width=0.6,
)

for bar, pct in zip(bars, df_score_dist["pct_of_total"]):
    ax_dist.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{pct:.1f}%",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
    )

ax_dist.set_title("A  |  Review Score Distribution (% of Total)", loc="left", pad=8)
ax_dist.set_xlabel("Review Score")
ax_dist.set_ylabel("Share of Reviews (%)")
ax_dist.set_ylim([0, df_score_dist["pct_of_total"].max() * 1.18])
ax_dist.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel B (top-centre): Delivery status vs. avg review score — gap highlighted
# ---------------------------------------------------------------------------
ax_del = fig.add_subplot(2, 3, 2)

del_colors = [
    "#4CAF50" if s == "On-Time" else "#F44336"
    for s in df_delivery_scores["delivery_status"]
]

bars_del = ax_del.bar(
    df_delivery_scores["delivery_status"],
    df_delivery_scores["avg_review_score"],
    color=del_colors, width=0.45,
)

for bar, val in zip(bars_del, df_delivery_scores["avg_review_score"]):
    ax_del.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.04,
        f"{val:.2f}",
        ha="center", va="bottom", fontsize=12, fontweight="bold",
    )

if score_on_time is not None and score_delayed is not None:
    gap = score_on_time - score_delayed
    mid_score = score_delayed + gap / 2 + 0.1
    ax_del.annotate(
        f"Gap: {gap:.2f} points",
        xy=(1, score_delayed), xytext=(0.5, mid_score),
        fontsize=9, color="#333", style="italic",
        arrowprops=dict(arrowstyle="-", color="#999"),
    )

ax_del.set_title("B  |  Avg Review Score: On-Time vs. Delayed", loc="left", pad=8)
ax_del.set_xlabel("Delivery Status")
ax_del.set_ylabel("Average Review Score (1-5)")
ax_del.set_ylim([0, 5.5])
ax_del.axhline(4.0, color="#999", linewidth=0.8, linestyle=":")
ax_del.grid(True, axis="y", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel C (top-right): KPI scorecard
# ---------------------------------------------------------------------------
ax_kpi = fig.add_subplot(2, 3, 3)
ax_kpi.axis("off")

total_reviews = int(df_score_dist["total_reviews"].sum())

if score_on_time is not None and score_delayed is not None:
    gap_str = f"{score_on_time - score_delayed:.2f} pts"
else:
    gap_str = "N/A"

kpi_lines = [
    ("Total Reviews",       f"{total_reviews:,}"),
    ("5-Star Share",        f"{pct_5_star:.1f}%"),
    ("1-Star Share",        f"{pct_1_star:.1f}%"),
    ("Avg Score (On-Time)", f"{score_on_time:.2f}" if score_on_time else "N/A"),
    ("Avg Score (Delayed)", f"{score_delayed:.2f}" if score_delayed else "N/A"),
    ("Delivery Score Gap",  gap_str),
]

ax_kpi.text(0.5, 1.0, "C  |  Review KPI Summary", transform=ax_kpi.transAxes,
            ha="center", fontsize=11, fontweight="bold")

y_pos = 0.88
for label, value in kpi_lines:
    is_risk = "1-Star" in label or "Delayed" in label or "Gap" in label
    ax_kpi.text(0.08, y_pos, label + ":", transform=ax_kpi.transAxes,
                ha="left", fontsize=10, color="#555")
    ax_kpi.text(0.95, y_pos, value, transform=ax_kpi.transAxes,
                ha="right", fontsize=10, fontweight="bold",
                color="#F44336" if is_risk else "#212121")
    y_pos -= 0.14

# ---------------------------------------------------------------------------
# Panel D (bottom, wide): Bottom 10 categories — horizontal bar with benchmark
# ---------------------------------------------------------------------------
ax_cat = fig.add_subplot(2, 3, (4, 6))

df_worst_sorted = df_worst_categories.sort_values("avg_review_score", ascending=True)
cat_colors = [
    "#F44336" if s < 3.5 else "#FF9800" if s < 4.0 else "#8BC34A"
    for s in df_worst_sorted["avg_review_score"]
]

bars_cat = ax_cat.barh(
    df_worst_sorted["category_english"].str.replace("_", " ").str.title(),
    df_worst_sorted["avg_review_score"],
    color=cat_colors, height=0.65,
)

for bar, (_, row) in zip(bars_cat, df_worst_sorted.iterrows()):
    label_text = f"{row['avg_review_score']:.2f}  ({int(row['total_orders']):,} orders)"
    ax_cat.text(
        row["avg_review_score"] + 0.02,
        bar.get_y() + bar.get_height() / 2,
        label_text,
        va="center", fontsize=9, color="#333",
    )

ax_cat.axvline(4.0, color="#2196F3", linewidth=1.4, linestyle="--",
               label="Score = 4.0 (benchmark)")
ax_cat.set_title(
    "D  |  Bottom 10 Product Categories by Avg Review Score  "
    "(red < 3.5 | amber < 4.0 | min 50 orders)",
    loc="left", pad=8,
)
ax_cat.set_xlabel("Average Review Score (1-5)")
ax_cat.set_xlim([1, 5.2])
ax_cat.legend(fontsize=9)
ax_cat.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_cat.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "04_review_dashboard.png")
plt.show()
