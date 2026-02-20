# Minimal Runbook

Ensure your terminal is at the project root (`sql-relational-analysis/`).

1. **Start PostgreSQL** (requires Docker installed)
   ```bash
   docker run --name olist_pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15-alpine
   ```

2. **Wait for DB readiness (approx 5 seconds)**

3. **Initialize DB & Connect**
   ```bash
   export PGPASSWORD=postgres
   psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE olist;"
   psql -h localhost -p 5432 -U postgres -d olist
   ```

4. **Execute all SQL Scripts in Order** (from within the `psql` prompt connected to `olist`):
   ```sql
   \i sql/ddl/01_create_schema.sql
   \i sql/ddl/02_create_tables.sql
   \i sql/load/01_bulk_insert_data.sql
   \i sql/ddl/03_add_constraints.sql
   \i sql/tests/01_validation_nulls_and_duplicates.sql
   \i sql/tests/02_validation_referential_integrity.sql
   \i sql/tests/03_validation_metric_sanity.sql
   \i sql/views/01_vw_order_fact.sql
   \i sql/views/02_vw_item_fact.sql
   \i sql/views/03_vw_customer_monthly_metrics.sql
   \i sql/views/04_vw_delivery_sla_metrics.sql
   \i sql/analysis/01_revenue_and_aov_behavior.sql
   \i sql/analysis/02_cohorts_and_retention.sql
   \i sql/analysis/03_delivery_sla_performance.sql
   \i sql/analysis/04_review_score_drivers.sql
   \i sql/analysis/05_payment_type_behavior.sql
   ```
