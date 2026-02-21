# Pipeline Runbook

Step-by-step instructions for initialising the Olist analytics environment from a clean state.

> **Quick version:** From the repository root, run `./scripts/run_pipeline.sh` to execute steps 2–5 automatically.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Docker | Used to run the PostgreSQL instance |
| Python ≥ 3.10 | Required by the notebook layer |
| Raw CSV files | Place the Olist dataset files inside `data/raw/olist/` |

---

## Step 1 — Configure your environment

Copy the environment template and fill in your credentials:

```bash
cp analysis/.env.example analysis/.env
# Edit analysis/.env if your credentials differ from the defaults (postgres/postgres)
```

---

## Step 2 — Start the PostgreSQL container

```bash
docker run \
  --name olist_pg \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=olist \
  -p 5432:5432 \
  -d postgres:15-alpine
```

Wait approximately 5 seconds for the container to be ready before proceeding.

---

## Step 3 — Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 4 — Run the full initialisation pipeline

```bash
./scripts/run_pipeline.sh
```

This script executes the following SQL files in dependency order:

| Stage | File |
|---|---|
| Schema | `sql/ddl/01_create_schema.sql` |
| Tables | `sql/ddl/02_create_tables.sql` |
| Data Load | `sql/load/01_bulk_insert_data.sql` |
| Constraints | `sql/ddl/03_add_constraints.sql` |
| Quality Test 1 | `sql/tests/01_validation_nulls_and_duplicates.sql` |
| Quality Test 2 | `sql/tests/02_validation_referential_integrity.sql` |
| Quality Test 3 | `sql/tests/03_validation_metric_sanity.sql` |
| View | `sql/views/01_vw_order_fact.sql` |
| View | `sql/views/02_vw_item_fact.sql` |
| View | `sql/views/03_vw_customer_monthly_metrics.sql` |
| View | `sql/views/04_vw_delivery_sla_metrics.sql` |

If any quality test assertion fails, the script exits immediately — no downstream analysis will run on corrupted data.

---

## Step 5 — Run the analytics notebooks

```bash
jupyter notebook analysis/notebooks/
```

Open each notebook in order and run all cells. Rendered charts are saved to `analysis/figures/`.

---

## Manual execution (alternative to the shell script)

If you prefer to run the SQL files yourself, connect to the database first:

```bash
export PGPASSWORD=postgres
psql -h localhost -p 5432 -U postgres -d olist
```

Then execute each file in the order listed in step 4 above using `\i <file>` from the `psql` prompt.
