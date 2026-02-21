"""
Rebuilds all 11 analysis notebooks with a standardised 6-cell structure:

    Cell 0 [markdown]  Purpose & Business Question
    Cell 1 [markdown]  Data Sources & Grain
    Cell 2 [code]      Environment setup + SQL execution + validation
    Cell 3 [markdown]  Analytical Methodology
    Cell 4 [code]      Multi-panel dashboard
    Cell 5 [markdown]  Conclusions  (loaded from analysis/reports/)

Dashboard and setup code is stored in ``scripts/cells/<NN>_{setup,dashboard}.py``
as plain Python source files — no string-escaping issues, independently editable.
Conclusion markdown is stored in ``analysis/reports/<NN>_*.md`` — the single
source of truth for all structured findings, implications, and recommendations.

Run from the repository root:
    python scripts/rebuild_notebooks.py
"""

from __future__ import annotations

import json
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Directory constants
# ──────────────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).resolve().parent.parent
NB_DIR      = REPO_ROOT / "analysis" / "notebooks"
CELLS_DIR   = Path(__file__).resolve().parent / "cells"
REPORTS_DIR = REPO_ROOT / "analysis" / "reports"


# ──────────────────────────────────────────────────────────────────────────────
# Notebook JSON helpers
# ──────────────────────────────────────────────────────────────────────────────

def _code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def _markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
    }


def _notebook(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }


def _read_cell(filename: str) -> str:
    path = CELLS_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Cell source not found: {path}")
    return path.read_text(encoding="utf-8")


def _read_report(filename: str) -> str:
    path = REPORTS_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Report not found: {path}")
    return path.read_text(encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────────────
# Shared import / setup header (prepended to every code cell 2)
# ──────────────────────────────────────────────────────────────────────────────
_SETUP_HEADER = """\
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from IPython.display import display

_REPO_ROOT = Path().resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from analysis.utils.db import get_connection
from analysis.utils.sql_loader import get_sql_path, load_queries
from analysis.utils.plotting import apply_style, save_figure

apply_style()
"""


# ──────────────────────────────────────────────────────────────────────────────
# Per-notebook specifications
# ──────────────────────────────────────────────────────────────────────────────
NOTEBOOKS: list[dict] = [
    # ── 00 ── Data Quality ───────────────────────────────────────────────────
    {
        "filename": "00_data_quality.ipynb",
        "cell0_body": """\
# Data Quality & Integrity Validation

**Role:** Data trust layer — this notebook must pass before any analytical findings are considered valid.

**Business question:** Does the Olist dataset meet the structural and referential integrity requirements necessary for quantitative analysis?

**Why this matters:** Analytical conclusions are only as reliable as the data they are derived from. This notebook formalises data quality as a first-class analytical step, not an afterthought.
""",
        "cell1_body": """\
## Data Sources

| Source | Description |
|---|---|
| `sql/tests/01_validation_nulls_and_duplicates.sql` | Duplicate order/item checks + null checks on critical fields |
| `sql/tests/02_validation_referential_integrity.sql` | Foreign-key orphan checks (orders → customers, items → orders, etc.) |
| `sql/tests/03_validation_metric_sanity.sql` | Negative price/payment checks + time-travel delivery detection + review score range |
| `olist.vw_order_fact` | Order-level view used for supplementary Python null-rate checks |
| `olist.vw_delivery_sla_metrics` | Delivery view used for supplementary null-rate checks |
| `olist.vw_customer_monthly_metrics` | Customer monthly view used for supplementary row-count and range checks |

**Grain:** One row per test assertion. Expected result for every SQL test query: 0 rows returned (assertion passes).
""",
        "cell3_body": """\
## Analytical Methodology

**Method:** SQL assertion testing + Python supplementary checks.

Each SQL test query is designed to return **0 rows** if the data quality condition is satisfied. A non-zero row count constitutes a test failure and indicates a specific data quality violation.

This method was chosen because:
- It requires no statistical assumptions.
- It produces fully deterministic, binary results (pass / fail).
- The same queries can be run in any SQL client or CI/CD pipeline without modification.

Python supplementary checks extend this to view-level properties (null rates, monotonicity, value ranges) that are more naturally expressed in pandas than in SQL.

**Validation hierarchy:**
1. SQL structural tests (uniqueness, referential integrity, value bounds)
2. Python view-level null rate profiles
3. Python range and consistency checks on derived views
""",
        "setup_file":      "00_setup.py",
        "dashboard_file":  "00_dashboard.py",
        "conclusion_file": "00_data_quality.md",
    },

    # ── 01 ── Revenue & AOV ───────────────────────────────────────────────────
    {
        "filename": "01_revenue_and_aov.ipynb",
        "cell0_body": """\
# Revenue, AOV & Geographic GMV Analysis

**Business question:** Where is revenue coming from — by time, product category, and geography — and how is average order value evolving?

**Decisions supported:**
- Revenue planning and forecasting
- Category investment prioritisation
- Geographic logistics and marketing resource allocation
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1: Monthly revenue & AOV | `vw_order_fact` — delivered orders only | One row per calendar month |
| Q2: Top 10 categories | `vw_item_fact` — delivered orders only | One row per category |
| Q3: GMV by state | `vw_order_fact` — delivered orders only | One row per customer state |

**Key columns used:** `revenue_month`, `total_revenue`, `total_orders`, `average_order_value`, `category_english`, `total_item_value`, `customer_state`, `gmv`, `unique_customers`

**Filter:** All queries restrict to `order_status = 'delivered'`. Cancelled, unavailable, and in-transit orders are excluded.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Time-series line chart** for revenue trend (panel A): chosen because it preserves the temporal sequence and allows the eye to track directional change.
- **Dual-axis overlay** for AOV on the same time axis: allows simultaneous comparison of two metrics on different scales without a separate chart.
- **Horizontal bar chart** for category ranking (panel B): the horizontal orientation accommodates long category labels without rotation.
- **Bar chart** for order volume seasonality (panel C): discrete monthly bars are more legible than a continuous line for volume counts.
- **Gradient-coloured bar chart** for state GMV (panel D): single-hue gradient encodes magnitude without introducing false categorical distinctions.

**Why this method:** Revenue, AOV, and geographic concentration are descriptive metrics best conveyed by rank-ordered comparisons and time-series trend lines. No statistical modeling is required or appropriate for descriptive GMV analysis.
""",
        "setup_file":      "01_setup.py",
        "dashboard_file":  "01_dashboard.py",
        "conclusion_file": "01_revenue_and_aov.md",
    },

    # ── 02 ── Cohorts & Retention ─────────────────────────────────────────────
    {
        "filename": "02_cohorts_and_retention.ipynb",
        "cell0_body": """\
# Customer Cohort Retention & Lifetime Value Analysis

**Business question:** Do customers return after their first purchase, and how does lifetime spend accumulate across cohorts?

**Decisions supported:**
- Whether to invest in retention versus acquisition
- When in the customer lifecycle to intervene
- How to evaluate acquisition channel quality beyond volume metrics
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1: Cohort retention matrix | `vw_customer_monthly_metrics` — non-cancelled orders | One row per cohort month × months since first purchase |
| Q2: Cumulative LTV by cohort | `vw_customer_monthly_metrics` — non-cancelled orders | One row per cohort month × months since first purchase |

**Key columns used:** `cohort_month`, `months_since_first_purchase`, `retention_rate_pct`, `returned_customers`, `avg_cumulative_ltv`

**Filter:** Cancelled orders excluded at the view definition level. Cohort month is defined as the truncated calendar month of a customer's first qualifying purchase.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Cohort bar chart** for month-1 retention (panel A): each bar represents one acquisition cohort. Red/blue colour encoding relative to the cross-cohort average immediately highlights underperforming cohorts.
- **Decay curve** (panel B): a line chart with shaded fill conveys the rate of customer loss over months. The steepest slope identifies the most actionable intervention window.
- **LTV growth curve** (panel C): cumulative LTV by month gives a clearer picture of the monetisation arc than snapshot LTV alone.
- **Cohort size bar** (panel D): separates the acquisition volume trend from the per-customer value trend, preventing conflation.
- **Scatter plot** (panel E): cohort size vs. peak LTV directly tests whether more customers per cohort predicts higher spend — a hypothesis with direct implications for acquisition strategy.

**Why this method:** Cohort analysis is the standard approach for measuring retention in a marketplace setting because it controls for time, allowing comparison of customers acquired under different conditions. No statistical inference is required — the analysis is descriptive and the patterns are observable directly.
""",
        "setup_file":      "02_setup.py",
        "dashboard_file":  "02_dashboard.py",
        "conclusion_file": "02_cohorts_and_retention.md",
    },

    # ── 03 ── Delivery SLA ────────────────────────────────────────────────────
    {
        "filename": "03_delivery_sla_performance.ipynb",
        "cell0_body": """\
# Delivery SLA Performance & Geographic Delay Analysis

**Business question:** What proportion of deliveries miss their SLA estimate, and which geographies carry the highest delay risk?

**Decisions supported:**
- Carrier contract negotiation and regional logistics partner review
- Customer-facing ETA calibration
- Proactive delay communication policy
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1: National SLA summary | `vw_delivery_sla_metrics` + `customers` | One row (national totals) |
| Q2: Delay by state | `vw_delivery_sla_metrics` + `customers` | One row per customer state |

**Key columns used:** `total_deliveries`, `total_delayed_orders`, `delayed_rate_pct`, `avg_actual_delivery_days`, `avg_estimated_delivery_days`, `customer_state`, `delayed_orders`, `avg_delay_days_when_delayed`

**Filter:** `vw_delivery_sla_metrics` excludes cancelled and unavailable orders by definition. Only orders with non-null actual delivery timestamps are included.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Donut chart** (panel A): the hollow centre is used for a summary KPI label (overall delayed %). Donut charts are appropriate for a single proportion comparison — on-time vs. delayed.
- **Bar chart with benchmark** (panel B): actual vs. estimated delivery days shown as side-by-side bars with a gap annotation. This directly quantifies the ETA calibration error.
- **KPI scorecard** (panel C): a text layout for 6 scalar KPIs that don't lend themselves to chart encoding. Used to anchor the executive at a glance before regional detail.
- **Full-state bar chart** (panel D): all states shown in a single chart, colour-coded against the national average. Allows immediate identification of above/below-average states.
- **Horizontal bar** (panel E): absolute delayed order counts for the worst-rate states. Separates the rate analysis from the volume analysis.
- **Bubble scatter** (panel F): delivery volume vs. delay rate, with bubble size encoding absolute delayed count. This 3-variable encoding identifies the true high-impact states.

**Why this method:** SLA analysis is fundamentally about rates and volumes across two dimensions (time and geography). The combination of rate analysis (panel D) and absolute volume analysis (panel E) is necessary because high-rate and high-volume states require different interventions.
""",
        "setup_file":      "03_setup.py",
        "dashboard_file":  "03_dashboard.py",
        "conclusion_file": "03_delivery_sla_performance.md",
    },

    # ── 04 ── Review Score Drivers ────────────────────────────────────────────
    {
        "filename": "04_review_score_drivers.ipynb",
        "cell0_body": """\
# Customer Review Score Drivers Analysis

**Business question:** What drives 1-star reviews — delivery performance, specific product categories, or both?

**Decisions supported:**
- Prioritisation of operational vs. product quality improvements for review score uplift
- Seller governance and product category exit criteria
- Customer satisfaction intervention timing
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1: Score distribution | `order_reviews` | One row per review score (1–5) |
| Q2: Score by delivery status | `order_reviews` + `vw_delivery_sla_metrics` | One row per delivery status (On-Time / Delayed) |
| Q3: Bottom 10 categories | `order_reviews` + `vw_item_fact` + `vw_delivery_sla_metrics` | One row per product category (min 50 orders) |

**Key columns used:** `review_score`, `total_reviews`, `pct_of_total`, `delivery_status`, `avg_review_score`, `category_english`, `total_orders`

**Filter:** Q3 applies a minimum of 50 orders per category to exclude categories with insufficient volume for stable average score calculation.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Colour-coded bar chart** (panel A): each score value (1–5) is assigned a semantic colour from red to green. Percentage labels above each bar allow immediate comparison without relying on axis reading.
- **Grouped bar chart** (panel B): two bars (On-Time, Delayed) with a gap annotation showing the score differential. This isolates the delivery effect on review score as a single, quantifiable number.
- **KPI scorecard** (panel C): scalar summary of review KPIs for executive context before the category-level detail.
- **3-tier colour horizontal bar** (panel D): three colours encode criticality — red (< 3.5), amber (3.5–4.0), green (≥ 4.0) — against a reference line at score = 4.0. Bar labels show both the score and the order volume, preventing misinterpretation of low scores from small samples.

**Why this method:** The analytical question has two parts — overall score distribution and causal drivers. Separating these into distinct panels (A for distribution, B for delivery effect, D for category effect) prevents conflation and allows each driver to be evaluated independently.
""",
        "setup_file":      "04_setup.py",
        "dashboard_file":  "04_dashboard.py",
        "conclusion_file": "04_review_score_drivers.md",
    },

    # ── 05 ── Payment Behaviour ───────────────────────────────────────────────
    {
        "filename": "05_payment_type_behavior.ipynb",
        "cell0_body": """\
# Payment Method Behavior & Cancellation Risk Analysis

**Business question:** Which payment methods generate the most revenue, and do certain payment types correlate with higher order cancellation rates?

**Decisions supported:**
- Payment gateway infrastructure investment and redundancy planning
- Boleto conversion rate improvement strategy
- Instalment product design for higher-AOV categories
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1: Payment usage & value | `order_payments` | One row per payment type |
| Q2: Cancellation by method | `orders` + `order_payments` | One row per payment type (min 100 orders) |

**Key columns used:** `payment_type`, `total_orders_used`, `total_payment_value`, `avg_transaction_value`, `avg_installments`, `canceled_orders`, `total_orders`, `cancellation_rate_pct`

**Filter:** Q2 restricts to payment types with at least 100 total orders to avoid unstable cancellation rate estimates from low-volume methods.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Horizontal bar chart** (panel A): volume ranking with a shared payment-type colour palette. Horizontal orientation handles label length.
- **Pie chart** (panel B): used only for revenue share — a single-level, parts-of-a-whole comparison where the interest is in proportional dominance (credit card vs. all others). Pie charts are appropriate in this context because the analysis is about concentration, not ranking.
- **Bar chart with reference line** (panel C): average transaction value by method with an overall-average benchmark. The benchmark line converts an absolute comparison into a relative one.
- **Bar chart** (panel D): installment count by method. No colour semantic needed as the data is ordinal, not binary.
- **3-tier colour bar with risk-zone shading** (panel E): cancellation rate bars coloured by risk tier (red / amber / green) against the weighted average. An `axhspan` shading zone highlights the high-risk region for visual emphasis.

**Why this method:** Payment behaviour analysis involves both volume/revenue metrics (descriptive) and cancellation risk (diagnostic). Separating these into panels prevents the revenue story from obscuring the operational risk signal.
""",
        "setup_file":      "05_setup.py",
        "dashboard_file":  "05_dashboard.py",
        "conclusion_file": "05_payment_type_behavior.md",
    },

    # ── 06 ── Geographic Patterns ─────────────────────────────────────────────
    {
        "filename": "06_geographic_patterns.ipynb",
        "cell0_body": """\
# Geographic Revenue & Delivery Risk Patterns

**Business question:** How do revenue concentration and delivery risk correlate across customer states, and which states represent the highest compound operational risk?

**Decisions supported:**
- Geographic resource allocation for logistics and support
- State-level SLA target differentiation
- Regional carrier contract prioritisation
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q3 of NB-01 | GMV, unique customers, total orders by state | One row per customer state |
| Q2 of NB-03 | Delay rate, delayed orders, total deliveries by state | One row per customer state |

**Cross-join:** The two state-grain tables are merged in Python on `customer_state`. No new SQL is introduced — this is a presentation-layer join of two existing aggregations.

**Derived columns (Python only, no SQL modification):**
- `gmv_share_pct`: state GMV as % of platform total
- `delay_tier`: above/below median delay rate
- `gmv_tier`: above/below median GMV
- `quadrant`: 2×2 composite (GMV tier × delay tier)
- `delay_per_1k`: delayed orders per 1,000 deliveries (normalised risk)
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Gradient bar chart** (panel A): all-state GMV ranking with a single-hue gradient encoding magnitude — avoids false categorical distinction while preserving rank order.
- **Colour-coded bar chart** (panel B): delay rate coloured red/green relative to the national median. Median is more robust than mean for threshold benchmarking in right-skewed distributions.
- **Normalised horizontal bar** (panel C): delayed orders per 1,000 deliveries — this rate is independent of state size and more comparable across states of different volume.
- **2×2 scatter quadrant** (panel D): the most analytically dense panel. Four combinations of GMV tier and delay tier define four strategic situations requiring different interventions. State labels annotate the most important outliers.
- **Horizontal bar** (panel E): unique customer count by state — confirms whether GMV concentration and customer concentration are geographically aligned.

**Why this method:** Geographic analysis requires simultaneous evaluation of absolute scale (GMV, order counts) and relative risk (delay rate, normalised exposure). No single chart captures all dimensions — the quadrant scatter is the synthesis, with the other panels providing supporting detail.
""",
        "setup_file":      "06_setup.py",
        "dashboard_file":  "06_dashboard.py",
        "conclusion_file": "06_geographic_patterns.md",
    },

    # ── 07 ── Time-Series Trends ──────────────────────────────────────────────
    {
        "filename": "07_time_series_trends.ipynb",
        "cell0_body": """\
# Time-Series Revenue Trends & Seasonality Analysis

**Business question:** Is revenue growth sustainable, what is the underlying trend beneath monthly volatility, and are there repeatable seasonal patterns that can inform operational planning?

**Decisions supported:**
- Revenue planning baseline methodology (rolling average vs. monthly actuals)
- Logistics capacity pre-allocation for seasonal peaks
- AOV intervention timing within the seasonal calendar
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1 of NB-01 | Monthly revenue, order count, AOV | One row per calendar month |

**Derived metrics (Python only — no SQL modification):**

| Metric | Formula | Purpose |
|---|---|---|
| `revenue_mom_pct` | `total_revenue.pct_change() * 100` | Measures directional momentum |
| `orders_mom_pct` | `total_orders.pct_change() * 100` | Compares volume and revenue momentum |
| `revenue_rolling_3m` | `total_revenue.rolling(3, min_periods=2).mean()` | Smooths short-term volatility |
| `aov_rolling_3m` | `average_order_value.rolling(3, min_periods=2).mean()` | AOV trend without month-to-month noise |
| `seasonality_index` | `total_revenue / trailing_12m_mean` | Identifies above/below-average months |

All derived metrics are computed from the observed `total_revenue`, `total_orders`, and `average_order_value` columns returned by Q1. No external data or statistical model is used.
""",
        "cell3_body": """\
## Analytical Methodology

**Methods applied:**
- **Shaded area + line chart with rolling average overlay** (panel A): the raw monthly series is shown as a shaded area for context; the smoothed rolling average is shown as the primary trend line. This combination is the standard approach for distinguishing trend from noise.
- **Bi-colour bar chart** (panel B & C): green/red MoM change bars immediately communicate whether a given month accelerated or decelerated, without requiring the reader to compute the change from the trend line.
- **Seasonality index bar with reference line** (panel D): bars above 1.0 are coloured distinctly to separate above-trend from below-trend months. The index is normalised to the trailing mean, making it comparable across years.
- **Calendar-month average bar** (panel E): collapses all years into a single 12-month view to reveal the repeatable within-year seasonal pattern. The standard year-average is more stable than any single year.

**Why this method:** Time-series revenue analysis requires separating three signals: long-term trend, short-term momentum, and repeatable seasonality. Each panel addresses exactly one of these three questions. Using a single chart for all three would produce an unreadable superposition.
""",
        "setup_file":      "07_setup.py",
        "dashboard_file":  "07_dashboard.py",
        "conclusion_file": "07_time_series_trends.md",
    },

    # ── 08 ── Outlier Detection ───────────────────────────────────────────────
    {
        "filename": "08_outlier_detection.ipynb",
        "cell0_body": """\
# Rule-Based Order-Level Outlier & Anomaly Detection

**Business question:** Which orders deviate significantly from the typical value and delivery experience — and what do these outliers reveal about operational risk?

**Decisions supported:**
- Whether to use mean or median for AOV reporting
- High-value order operational differentiation (priority routing, proactive communication)
- Extreme delay monitoring and escalation thresholds
""",
        "cell1_body": """\
## Data Sources

| Source | Description | Grain |
|---|---|---|
| `olist.vw_order_fact` | Order-level revenue — delivered orders only | One row per order |
| `olist.vw_delivery_sla_metrics` | Delivery timing and delay — all non-cancelled orders | One row per order |

**Merged on:** `order_id` (inner join — orders present in both views)

**Outlier method:** Standard Tukey IQR upper fence
- Formula: `Q75 + 1.5 × (Q75 − Q25)`
- Applied independently to `total_order_value` and `delay_days`
- The delay fence is computed only over delayed orders (`is_delayed = True`)
- No statistical assumptions about the underlying distribution are required

**Derived boolean flags:** `is_revenue_outlier`, `is_delay_outlier`, `is_dual_outlier`
""",
        "cell3_body": """\
## Analytical Methodology

**Method:** Tukey IQR fence (non-parametric rule-based outlier detection).

The IQR method was chosen because:
- It makes no assumption about the distribution (does not require normality).
- It is deterministic and reproducible — the same data always produces the same flags.
- It is the industry standard for initial outlier identification in right-skewed distributions (which order values and delay durations typically are).
- It requires no model training, no hyperparameters, and no external data.

**Alternative considered and rejected:** Z-score based outlier detection. Rejected because the order value distribution is heavily right-skewed; Z-scores perform poorly on non-normal distributions and would produce inconsistent results across dataset snapshots.

**Panels:**
- Histogram (A): distribution shape with fence vertical line — confirms the fence is placed at a visually sensible location.
- Scatter (B): individual order visibility — confirms outliers are not data entry errors (they are spread across the timeline).
- KPI scorecard (C): scalar summary for executive context.
- State-level bar (D & F): concentration and rate of outliers by geography — identifies whether outliers are geographically skewed.
- Delay distribution (E): same IQR logic applied to delay duration, restricted to delayed orders.
""",
        "setup_file":      "08_setup.py",
        "dashboard_file":  "08_dashboard.py",
        "conclusion_file": "08_outlier_detection.md",
    },

    # ── 09 ── Customer Segmentation ───────────────────────────────────────────
    {
        "filename": "09_customer_segmentation.ipynb",
        "cell0_body": """\
# Rule-Based Customer Spend-Tier Segmentation

**Business question:** Can customers be meaningfully segmented into distinct spend tiers using only observed LTV data — and does tier membership correlate with early retention behaviour?

**Decisions supported:**
- LTV-weighted retention investment allocation
- Acquisition channel evaluation beyond volume metrics
- CRM and re-engagement campaign targeting
""",
        "cell1_body": """\
## Data Sources

| Query | Description | Grain |
|---|---|---|
| Q1 of NB-02 | Cohort retention matrix | One row per cohort month × months since first purchase |
| Q2 of NB-02 | Cumulative LTV by cohort | One row per cohort month × months since first purchase |

**Aggregated to cohort grain (Python):**
- `peak_avg_ltv`: maximum observed `avg_cumulative_ltv` per cohort (final observed period per cohort)
- `cohort_size`: `returned_customers` at `months_since_first_purchase = 0`
- `month1_retention_pct`: `retention_rate_pct` at `months_since_first_purchase = 1`

**Tier assignment rule (percentile cut — data-driven, no assumed thresholds):**

| Tier | Condition | Rationale |
|---|---|---|
| High-Value | `peak_avg_ltv >= P67` | Top third of cohorts by observed peak LTV |
| Mid-Value | `P33 <= peak_avg_ltv < P67` | Middle third |
| Single-Purchase | `peak_avg_ltv < P33` | Bottom third — lowest observed cumulative spend |

P33 and P67 are computed from the dataset each time the notebook runs. No external thresholds are assumed.
""",
        "cell3_body": """\
## Analytical Methodology

**Method:** Percentile-cut spend tier segmentation (rule-based, non-parametric).

This method was chosen because:
- It is fully deterministic: the same data always produces the same tier boundaries.
- It requires no model training, no distance metrics, and no hyperparameter tuning.
- It is directly explainable to non-technical stakeholders: "this cohort is in the top third by cumulative spend."
- The tier boundaries are derived from the observed data distribution, not assumed in advance — making them accurate representations of the actual population structure.

**Alternative considered and rejected:** K-means clustering. Rejected because: (1) it is a ML method, which is outside the project constraints; (2) cluster assignments are sensitive to random initialisation and are not reproducible without fixing the seed; (3) the analytical question is about spend levels, which maps naturally to an ordered rank — a problem well-suited to percentile cuts.

**Panels:**
- Count bar (A): confirms all three tiers are populated and shows relative cohort distribution.
- LTV bar (B): confirms tiers have meaningfully different average LTV — validates the segmentation is non-trivial.
- Retention bar (C): tests the hypothesis that tier correlates with early engagement — the key business insight.
- Temporal scatter (D): shows whether tier quality changed over time (campaign effects, seasonal acquisition).
- Cohort size bar (E): confirms whether tiers have different acquisition scales — tests whether volume predicts quality.
""",
        "setup_file":      "09_setup.py",
        "dashboard_file":  "09_dashboard.py",
        "conclusion_file": "09_customer_segmentation.md",
    },

    # ── 10 ── Executive Dashboard ─────────────────────────────────────────────
    {
        "filename": "10_executive_dashboard.ipynb",
        "cell0_body": """\
# Executive Analytical Dashboard & Synthesis

**Role:** Cross-domain synthesis — this notebook aggregates the most decision-relevant findings from all five analytical themes into a single executive-level view.

**Business question:** What is the current state of the business across revenue, retention, operations, satisfaction, and payments — and where are the highest-priority risks?

**Audience:** Executive leadership, business stakeholders, and portfolio reviewers requiring a single starting point for the analysis.
""",
        "cell1_body": """\
## Data Sources

This notebook re-executes all five analytical query sets (Q1 from each) and aggregates the results into a unified KPI table. No new SQL queries are introduced.

| Theme | SQL File | Key Metrics |
|---|---|---|
| Revenue & AOV | `01_revenue_and_aov_behavior.sql` | Total GMV, total orders, avg AOV |
| Cohorts & LTV | `02_cohorts_and_retention.sql` | Avg month-1 retention, peak LTV |
| Delivery SLA | `03_delivery_sla_performance.sql` | Delay rate, ETA overshoot |
| Review Scores | `04_review_score_drivers.sql` | Score gap (on-time vs. delayed) |
| Payment Types | `05_payment_type_behavior.sql` | Credit card GMV share, cancel rate |

**Grain:** One row per business theme in the risk matrix. Scalar KPIs extracted from the first row of each summary query result.
""",
        "cell3_body": """\
## Analytical Methodology

**Method:** Cross-domain KPI aggregation and risk matrix synthesis.

The executive dashboard does not introduce new analytical methods — it applies the findings from notebooks 01–09 in a unified summary view. The design follows a top-down logic:

1. **Overall performance snapshot** (KPI scorecard, panel A) — establishes baseline before showing drivers.
2. **Most critical time-series signal** (revenue trend, panel B) — the single most-watched operational metric.
3. **Most critical operational risk** (SLA donut, panel C) — the highest-impact operational improvement lever.
4. **Most critical satisfaction signal** (review score distribution, panel D) — reflects the customer experience outcome of all operational decisions.
5. **Most critical financial risk** (payment share, panel E) — revenue concentration and cancellation risk.
6. **Prioritised risk summary table** (panel F) — synthesises all themes into a single decision-support matrix with explicit priority ratings.

**Priority ratings** (High / Medium / Low) are derived from the cross-domain findings in notebooks 01–09. They reflect the combination of financial impact, operational controllability, and finding strength — not subjective judgment.
""",
        "setup_file":      "10_setup.py",
        "dashboard_file":  "10_dashboard.py",
        "conclusion_file": "10_executive_dashboard.md",
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Build and write notebooks
# ──────────────────────────────────────────────────────────────────────────────

def build_notebook(spec: dict) -> None:
    """Assemble a 6-cell notebook from its spec and write it to disk."""
    setup_src      = _SETUP_HEADER + "\n" + _read_cell(spec["setup_file"])
    dashboard_src  = _read_cell(spec["dashboard_file"])
    conclusion_src = _read_report(spec["conclusion_file"])

    cells = [
        _markdown_cell(spec["cell0_body"]),   # 0 — Purpose & Business Question
        _markdown_cell(spec["cell1_body"]),   # 1 — Data Sources & Grain
        _code_cell(setup_src),                # 2 — Setup + SQL + Validation
        _markdown_cell(spec["cell3_body"]),   # 3 — Analytical Methodology
        _code_cell(dashboard_src),            # 4 — Dashboard
        _markdown_cell(conclusion_src),       # 5 — Conclusions (from reports/)
    ]

    nb_path = NB_DIR / spec["filename"]
    nb_path.write_text(json.dumps(_notebook(cells), indent=1), encoding="utf-8")
    print(f"  Written: {nb_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    print(f"Rebuilding {len(NOTEBOOKS)} analysis notebooks …")
    for spec in NOTEBOOKS:
        build_notebook(spec)
    print("Done.")
