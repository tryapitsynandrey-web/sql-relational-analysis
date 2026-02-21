#!/usr/bin/env bash
# =============================================================================
# run_pipeline.sh — Olist Analytics Pipeline: Full Initialisation Script
#
# Executes the complete pipeline from schema creation through data quality
# validation and semantic view deployment, in the correct dependency order.
#
# USAGE
#   ./scripts/run_pipeline.sh
#
# PREREQUISITES
#   • Docker must be running.
#   • The PostgreSQL container must already be started (see README "Quick Start").
#   • Raw CSV files must be present in data/raw/olist/*.csv.
#   • The PGPASSWORD environment variable (or .env) must be set.
#
# ENVIRONMENT
#   DB_HOST       (default: localhost)
#   DB_PORT       (default: 5432)
#   DB_USER       (default: postgres)
#   DB_PASSWORD   (default: postgres)
#   DB_NAME       (default: olist)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve repository root regardless of where the script is called from.
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# ---------------------------------------------------------------------------
# Load .env if present (analysis/.env takes precedence over repo-root .env)
# ---------------------------------------------------------------------------
ENV_FILE="$REPO_ROOT/analysis/.env"
if [[ -f "$ENV_FILE" ]]; then
    # Export all non-comment, non-empty lines from the .env file.
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    echo "✓ Loaded environment from $ENV_FILE"
fi

# ---------------------------------------------------------------------------
# Connection parameters (with defaults matching Docker Compose defaults)
# ---------------------------------------------------------------------------
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-olist}"
export PGPASSWORD="${DB_PASSWORD:-postgres}"

PSQL="psql -h $DB_HOST -p $DB_PORT -U $DB_USER"

# ---------------------------------------------------------------------------
# Helper: print a section header
# ---------------------------------------------------------------------------
section() {
    echo ""
    echo "──────────────────────────────────────────────────────────"
    echo "  $1"
    echo "──────────────────────────────────────────────────────────"
}

# ---------------------------------------------------------------------------
# Helper: execute a SQL file against the olist database
# ---------------------------------------------------------------------------
run_sql() {
    local label="$1"
    local file="$2"
    echo "  → $label"
    $PSQL -d "$DB_NAME" -f "$REPO_ROOT/$file"
}

# ---------------------------------------------------------------------------
# Step 1: Ensure the target database exists
# ---------------------------------------------------------------------------
section "Step 1 of 5 — Database Initialisation"
echo "  → Creating database '$DB_NAME' (skipped if already exists)"
$PSQL -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1 \
    || $PSQL -c "CREATE DATABASE $DB_NAME;"
echo "  ✓ Database ready"

# ---------------------------------------------------------------------------
# Step 2: DDL — Schema, tables, constraints
# ---------------------------------------------------------------------------
section "Step 2 of 5 — DDL (Schema, Tables, Constraints)"
run_sql "Create schema"          "sql/ddl/01_create_schema.sql"
run_sql "Create tables"          "sql/ddl/02_create_tables.sql"

# ---------------------------------------------------------------------------
# Step 3: Data load
# ---------------------------------------------------------------------------
section "Step 3 of 5 — Data Load"
echo "  NOTE: Ensure data/raw/olist/*.csv files are present before this step."
run_sql "Bulk insert data"       "sql/load/01_bulk_insert_data.sql"

# Constraints after load to avoid per-row check overhead during bulk inserts.
run_sql "Add constraints"        "sql/ddl/03_add_constraints.sql"

# ---------------------------------------------------------------------------
# Step 4: Data Quality Validation
# ---------------------------------------------------------------------------
section "Step 4 of 5 — Data Quality Tests"
run_sql "Nulls & duplicates"     "sql/tests/01_validation_nulls_and_duplicates.sql"
run_sql "Referential integrity"  "sql/tests/02_validation_referential_integrity.sql"
run_sql "Metric sanity"          "sql/tests/03_validation_metric_sanity.sql"
echo "  ✓ All data quality assertions passed"

# ---------------------------------------------------------------------------
# Step 5: Semantic Layer (Views)
# ---------------------------------------------------------------------------
section "Step 5 of 5 — Semantic Views"
run_sql "vw_order_fact"              "sql/views/01_vw_order_fact.sql"
run_sql "vw_item_fact"               "sql/views/02_vw_item_fact.sql"
run_sql "vw_customer_monthly_metrics" "sql/views/03_vw_customer_monthly_metrics.sql"
run_sql "vw_delivery_sla_metrics"   "sql/views/04_vw_delivery_sla_metrics.sql"
echo "  ✓ Semantic layer deployed"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  Pipeline initialisation complete."
echo "  Open analysis/notebooks/ in Jupyter to run the analytics."
echo "══════════════════════════════════════════════════════════════"
