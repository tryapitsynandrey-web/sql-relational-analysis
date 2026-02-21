# Olist Analytics System — Start Here

This repository contains a **structured, end-to-end analytical system** built on the Olist Brazilian e-commerce dataset. The analysis is SQL-first, decision-oriented, and designed to serve both analytics professionals and executive stakeholders.

---

## Analytical Philosophy

- **SQL is the single source of truth.** All metric definitions, joins, and aggregations live in SQL views and query files. Python is used only to validate, visualise, and interpret.
- **Every chart answers one analytical question.** Visualisations are not decorative — each panel is designed to support a specific operational or commercial decision.
- **All findings are grounded in observed data.** No metrics are invented, no assumptions are introduced, and no models are used.
- **Reproducibility is non-negotiable.** All notebooks can be re-executed end-to-end against a live database connection to reproduce the same outputs deterministically.

---

## How to Run the Analysis

### Prerequisites
```
1. A running PostgreSQL instance with the Olist schema loaded
   (see docs/runbook.md for database setup instructions)
2. Python environment with all dependencies installed:
   pip install -r requirements.txt
3. A .env file at analysis/.env containing:
   DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
```

### Recommended Execution Order
Run notebooks in sequence. Each notebook builds on the data trust established by the preceding one.

```bash
cd analysis/notebooks/
# Open in Jupyter and execute in order 00 → 10
jupyter notebook
```

To regenerate all notebook files from source (after editing cell scripts or reports):
```bash
python scripts/rebuild_notebooks.py
```

---

## Notebook System Map

| # | Notebook | Role | Audience |
|---|---|---|---|
| **00** | `00_data_quality.ipynb` | **Data Trust Layer** — SQL integrity tests + Python assertions. Establishes dataset is clean before any analysis begins. | Analysts, Engineers |
| **01** | `01_revenue_and_aov.ipynb` | **Revenue & Unit Economics** — Monthly GMV, AOV trends, category and geographic concentration. | All |
| **02** | `02_cohorts_and_retention.ipynb` | **Customer Retention & LTV** — Cohort retention matrix, LTV accumulation, acquisition volume trends. | Analytics, Product |
| **03** | `03_delivery_sla_performance.ipynb` | **Operational SLA** — Delay rate, ETA accuracy, state-level geographic risk. | Operations, Logistics |
| **04** | `04_review_score_drivers.ipynb` | **Satisfaction Drivers** — Score distribution, delivery impact on scores, category-level risk. | Product, CX |
| **05** | `05_payment_type_behavior.ipynb` | **Payment Behaviour** — Method usage, revenue share, installment patterns, cancellation risk. | Finance, Product |
| **06** | `06_geographic_patterns.ipynb` | **Geographic Cross-Analysis** — GMV vs. delay risk quadrant, state-level normalised exposure, customer density. | Operations, Strategy |
| **07** | `07_time_series_trends.ipynb` | **Trends & Seasonality** — MoM change, rolling averages, seasonality index, calendar-month patterns. | Analytics, Planning |
| **08** | `08_outlier_detection.ipynb` | **Outlier Detection** — IQR-based flags on order value and delivery delay, state-level outlier concentration. | Analytics, Operations |
| **09** | `09_customer_segmentation.ipynb` | **Customer Segmentation** — Rule-based spend tiers (P33/P67 LTV cuts), retention by tier, cohort composition. | CRM, Marketing |
| **10** | `10_executive_dashboard.ipynb` | **Executive Synthesis** — Cross-domain KPI scorecard, revenue trend, SLA status, payment share, risk matrix. | Executives, Leadership |

---

## Where to Find the Outputs

| Type | Location |
|---|---|
| Structured conclusions (Findings / Implications / Recommendations) | `analysis/reports/*.md` |
| Dashboard images (saved on notebook execution) | `analysis/figures/*.png` |
| SQL query logic | `sql/analysis/*.sql` |
| SQL view definitions | `sql/views/*.sql` |
| Data quality test queries | `sql/tests/*.sql` |
| Notebook cell source files | `scripts/cells/*.py` |

---

## Analytical Progression

```
data trust          descriptive         diagnostics         synthesis
───────────────────────────────────────────────────────────────────────
00_data_quality  →  01_revenue       →  06_geographic   \
                    02_cohorts       →  07_time_series    →  10_executive
                    03_sla           →  08_outliers      /
                    04_reviews       →  09_segments     /
                    05_payments
```

---

*For database setup, environment configuration, and full pipeline execution, see [`docs/runbook.md`](../docs/runbook.md).*
