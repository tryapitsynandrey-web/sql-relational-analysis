# =============================================================================
# Dashboard 00 — Data Quality Visual Report
# =============================================================================
# Build colour-coded test result matrix and null-rate profiles
# =============================================================================

# ---------------------------------------------------------------------------
# Panel layout
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 12))
fig.suptitle(
    "Olist Data Quality & Integrity Dashboard",
    fontsize=16, fontweight="bold", y=0.99,
)

# ---------------------------------------------------------------------------
# Panel A: Test suite pass/fail bar chart (left, tall)
# ---------------------------------------------------------------------------
ax_bar = fig.add_subplot(2, 2, 1)

suite_counts = df_summary.groupby(["Suite", "Status"]).size().unstack(fill_value=0)
suite_counts = suite_counts.reindex(columns=["PASS", "FAIL"], fill_value=0)

colors_bar = ["#4CAF50", "#F44336"]
suite_counts.plot(
    kind="barh", ax=ax_bar, color=colors_bar, width=0.55
)
ax_bar.set_title("A  |  Test Results by Suite", loc="left", pad=8)
ax_bar.set_xlabel("Number of Tests")
ax_bar.legend(loc="lower right", fontsize=9)
ax_bar.grid(True, axis="x", linestyle="--", alpha=0.5)
ax_bar.set_axisbelow(True)

# ---------------------------------------------------------------------------
# Panel B: Overall pass rate KPI scorecard (top-right)
# ---------------------------------------------------------------------------
ax_kpi = fig.add_subplot(2, 2, 2)
ax_kpi.axis("off")

pass_rate = passed_tests / total_tests * 100
kpi_items = [
    ("Total Checks Run",    str(total_tests)),
    ("Passed",              f"{passed_tests}  ({pass_rate:.0f}%)"),
    ("Failed",              f"{failed_tests}"),
    ("Suites Executed",     str(len(test_files))),
    ("View-level Checks",   str(len(view_checks))),
    ("View Checks Passed",  str(sum(c[2] for c in view_checks))),
]

ax_kpi.text(0.5, 1.02, "B  |  Quality Gate Summary",
            transform=ax_kpi.transAxes, ha="center",
            fontsize=11, fontweight="bold")
y = 0.88
for label, val in kpi_items:
    is_risk = "Failed" in label and val != "0"
    ax_kpi.text(0.05, y, label + ":", transform=ax_kpi.transAxes,
                ha="left", fontsize=10, color="#555")
    ax_kpi.text(0.95, y, val, transform=ax_kpi.transAxes,
                ha="right", fontsize=10, fontweight="bold",
                color="#F44336" if is_risk else "#212121")
    y -= 0.14

# ---------------------------------------------------------------------------
# Panel C: Null rate profile for vw_order_fact
# ---------------------------------------------------------------------------
ax_null_of = fig.add_subplot(2, 2, 3)

null_rates_of = (df_of.isnull().mean() * 100).sort_values(ascending=False)
null_rates_of = null_rates_of[null_rates_of > 0].head(12)

if len(null_rates_of) > 0:
    bar_cols = ["#F44336" if v > 5 else "#FF9800" for v in null_rates_of]
    ax_null_of.barh(null_rates_of.index, null_rates_of.values, color=bar_cols)
    ax_null_of.axvline(5, color="#FF9800", linewidth=1.2, linestyle="--",
                       label="5% threshold")
    ax_null_of.legend(fontsize=9)
else:
    ax_null_of.text(0.5, 0.5, "No nulls detected in\nvw_order_fact",
                    ha="center", va="center", transform=ax_null_of.transAxes,
                    fontsize=11, color="#4CAF50", fontweight="bold")

ax_null_of.set_title("C  |  Null Rate (%) — vw_order_fact", loc="left", pad=8)
ax_null_of.set_xlabel("Null Rate (%)")
ax_null_of.grid(True, axis="x", linestyle="--", alpha=0.5)

# ---------------------------------------------------------------------------
# Panel D: Null rate profile for vw_delivery_sla_metrics
# ---------------------------------------------------------------------------
ax_null_sla = fig.add_subplot(2, 2, 4)

null_rates_sla = (df_sla.isnull().mean() * 100).sort_values(ascending=False)
null_rates_sla = null_rates_sla[null_rates_sla > 0].head(12)

if len(null_rates_sla) > 0:
    bar_cols_sla = ["#F44336" if v > 5 else "#FF9800" for v in null_rates_sla]
    ax_null_sla.barh(null_rates_sla.index, null_rates_sla.values, color=bar_cols_sla)
    ax_null_sla.axvline(5, color="#FF9800", linewidth=1.2, linestyle="--",
                        label="5% threshold")
    ax_null_sla.legend(fontsize=9)
else:
    ax_null_sla.text(0.5, 0.5, "No nulls detected in\nvw_delivery_sla_metrics",
                     ha="center", va="center", transform=ax_null_sla.transAxes,
                     fontsize=11, color="#4CAF50", fontweight="bold")

ax_null_sla.set_title("D  |  Null Rate (%) — vw_delivery_sla_metrics", loc="left", pad=8)
ax_null_sla.set_xlabel("Null Rate (%)")
ax_null_sla.grid(True, axis="x", linestyle="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.97])
save_figure(fig, "00_data_quality_dashboard.png")
plt.show()
