# Olist E-Commerce Analytics Pipeline: From Raw Data to Strategic Insights
A reproducible, zero-dependency SQL analytics pipeline built natively on PostgreSQL, delivering strategic insights from raw CSVs to localized executive reports in under 10 minutes.

### 🎥 Live Dashboard Demo / Architecture Run-through 
*(Link to video or dashboard GIF will be placed here)*

---

## 🚀 About the Project (STAR)
*   **Situation:** Olist, a Brazilian e-commerce integration platform, operates a complex marketplace connecting independent merchants to major consumer storefronts.
*   **Task:** The business needed to understand the core drivers of revenue, identify logistical bottlenecks (SLA failures), mitigate customer churn, and correlate seller performance to actual customer satisfaction scores.
*   **Action:** This project implements an end-to-end, SQL-first analytics engineering pipeline. It transforms raw transactional data into structured semantic views and programmatically outputs analytical visualizations.
*   **Result:** Stakeholders can make rapid, trustworthy decisions regarding logistics planning, payment option friction, and cohort marketing re-engagement based on verified metrics.

---

## 🏛 Architecture Overview
The pipeline enforces a strict separation of concerns across directory layers:
1.  **Data/DDL (`sql/ddl/`):** Instantiates the PostgreSQL target schema, assigns firm data types, and lays down performance indexes.
2.  **Load (`sql/load/`):** Utilizes native client-side `psql \copy` commands to stream raw flat files directly into memory.
3.  **Quality Tests (`sql/tests/`):** Automated SQL assertions validating referential integrity and metric boundaries to catch data corruption early.
4.  **Semantic Views (`sql/views/`):** The business logic layer. Abstracts normalized raw tables into cohesive fact and dimension virtual tables to prevent duplicated logic or fan-out errors in downstream queries.
5.  **Analysis Queries (`sql/analysis/`):** Pure SQL declarations explicitly answering fundamental business questions.
6.  **Insights Layer (`analysis/notebooks/`, `analysis/reports/`):** Programmatic execution of the SQL scripts via `psycopg2` and `pandas`, rendering output visually via `matplotlib` and summarizing findings in Markdown.

For an extensive architectural deep dive, mapping data flows and design trade-offs, review the **[Architecture Design Document](docs/architecture.md)**.

---

## 📂 Dataset Details
*   **Source:** The publicly available Olist Brazilian E-Commerce Dataset.
*   **Scale:** ~100,000 anonymized, real-world marketplace transactions executed between 2016 and 2018. Includes multifaceted dimensions such as order status, price, freight, customer location, sequential payment methods, physical product dimensions, and unstructured text reviews.
*   **Constraints:** Requires placing the raw `.csv` files inside `data/raw/olist/` prior to pipeline initialization. The datasets themselves are ignored via `.gitignore` to prevent repository bloat.

---

## ⭐ Key Features
| Feature | Implementation | Description |
| :--- | :--- | :--- |
| **Reproducible Runtime** | Docker (`Dockerfile`) | A minimal, ephemeral PostgreSQL container eliminating dependency conflicts. |
| **Strict Data Quality** | SQL Asserts (`sql/tests/`) | Pre-analysis execution blocks validating primary keys, orphan records, and time-travel logic. |
| **Virtualized Logic** | SQL Views (`sql/views/`) | Window functions and cohort math isolated into safe semantic views, preventing ad-hoc mapping errors. |
| **Programmatic Execution** | Python / Pandas | Pure SQL logic routed dynamically into executable scripts for data extraction and graphical rendering. |

---

## 🛠 Getting Started (Quick Start)
The entire pipeline is designed for a local turnaround time of less than 10 minutes.

**1. Spin up the Database Environment**
```bash
docker build -t olist-postgres .
docker run -d -p 5432:5432 --name olist_db olist-postgres
```

**2. Initialize the Pipeline**
Ensure your local `data/raw/olist/*.csv` files are populated. Execute the pipeline initialization steps (DDL, Data Load, Quality Tests, semantic views) as dictated in the **[Pipeline Runbook](docs/runbook.md)**.

**3. Run the Analytics**
Configure your local environment variables mimicking `.env.example`.
```bash
pip install pandas psycopg2-binary matplotlib jupyter python-dotenv
# Execute the analytical notebooks or scripts
jupyter notebook
```
> **Note:** A master execution script (e.g., `run_pipeline.sh`) is planned to fully automate step 2 and 3 sequentially for a single-click run.

---

## 📈 Analytics & Insights
This repository explicitly targets five core business domains:
1.  **Gross Revenue & AOV Trends** (`01_revenue_and_aov.sql`)
2.  **Cohort Analysis & Retention Rates** (`02_cohorts_and_retention.sql`)
3.  **Logistics SLA Delays by Geography** (`03_delivery_sla_performance.sql`)
4.  **Drivers of 1-Star Customer Reviews** (`04_review_score_drivers.sql`)
5.  **Payment Method Cancellations** (`05_payment_type_behavior.sql`)

Executable analytical SQL is isolated in `sql/analysis/`. Statistical plotting occurs dynamically within `analysis/notebooks/*.ipynb`. Final business strategy recommendations and executive executive summaries are curated in `analysis/reports/*.md`.

---

## 🛡️ Data Quality & Testing
Before analytical queries are authorized, the pipeline executes `sql/tests/*.sql`.
*   **Guarantees:** Asserts against duplicate rows, validates strict referential integrity (no orphan keys), and enforces metric sanity (e.g., negative prices, delivery dates preceding purchase dates).
*   **Known Risks:** The ingestion pipeline deliberately utilizes raw `psql \copy` to maximize speed. Unplanned schema modifications inside the vendor's source CSV files will intentionally and safely crash the pipeline rather than implicitly logging corrupted data.

---

## 📝 Architecture Decisions
*   **Under-the-Hood SQL Modeling:** I intentionally built a back-to-basics, bare-metal SQL pipeline to demonstrate a fundamental, under-the-hood understanding of data modeling, testing, and semantic abstraction. Building these patterns from scratch highlights structural comprehension of what modern tools do abstraction-wise.
*   **Zero-Dependency Setup:** Eschewing complex orchestration guarantees seamless `<10 minute` verifiability by independent reviewers via simple local execution.
*   **Limitations:** True NET profitability remains a complete blindspot due to missing COGS (Cost of Goods Sold) and marketing overhead datasets.
*   **Further Reading:** See **[Assumptions & Next Steps](docs/assumptions_and_next_steps.md)** for detailed risk assessments, or review `meta/naming_conventions.md` and `meta/data_grain.md` for explicit documentation on calculation methodologies.

---

## 🏅 Skills Demonstrated
*   **Relational Database Design:** Normalization, Constraint mapping, Primary/Foreign Key Indexing.
*   **Analytics Engineering:** Virtualized semantic layer construction (`VIEWS`), isolating raw data from presentation facts.
*   **Advanced SQL Operations:** Common Table Expressions (CTEs), Window Functions, and PG-native `FILTER (WHERE...)` aggregate pushdowns.
*   **Data Quality Assurance:** Writing declarative data validation tests entirely in SQL.
*   **Data Visualization & Reporting:** Bridging SQL analytics into Python dataframes for charting (`matplotlib`) and communicating strategies (`markdown`).

---

## 🌲 Repository Structure
```text
.
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── analysis/
│   ├── figures/                # Exported PNG visualizations 
│   ├── notebooks/              # Jupyter analytical execution
│   └── reports/                # Markdown business strategy write-ups
├── data/                       
│   └── raw/                    # [Ignored] Source CSV files
├── docs/                       # Architecture, Assumptions, Runbook
├── meta/                       # Data Grains, Naming Conventions
└── sql/                        
    ├── analysis/               # Core business queries
    ├── ddl/                    # Schema, Tables, Constraints
    ├── load/                   # Ingestion logic
    ├── tests/                  # Integrity validations
    └── views/                  # Denormalized semantic layer
```

---

## 🔮 Scaling Roadmap
*   **Data Transformation Automation (`dbt`):** Migrate the bare-metal SQL testing logic and manual semantic views into a structured `dbt` project for documentation, lineage tracking, and macro-based testing at scale.
*   **Workflow Orchestration:** Wrap the ingestion, transformation, and reporting sequences into a DAG-based orchestrator (Airflow or Prefect) to handle retries and dependency gating.
*   **Cloud Data Warehouse Target:** Adapt the PostgreSQL core into a true OLAP system like Snowflake or BigQuery to separate compute/storage and enable PB-scale analytics.
*   **Geospatial Integration:** Utilize PostGIS to dynamically map logistical SLA failures beyond aggregate state buckets directly into localized bounding boxes.

---

## ✉️ Author & Contact
Designed and implemented as a Zero-Dependency SQL Analytics Pipeline.

*   **Author:** Andrew Shwarts
*   **Email:** [ashwarts@example.com] *(Update before publishing)*
*   **LinkedIn:** [linkedin.com/in/andrewshwarts] *(Update before publishing)*
*   **Location:** Authorized to work globally.