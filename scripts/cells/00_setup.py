# =============================================================================
# Notebook 00 — Data Quality & Integrity Validation
# Setup, SQL execution, and assertion layer
# =============================================================================

# ---------------------------------------------------------------------------
# Load and execute all SQL test suites
# ---------------------------------------------------------------------------
test_files = [
    "sql/tests/01_validation_nulls_and_duplicates.sql",
    "sql/tests/02_validation_referential_integrity.sql",
    "sql/tests/03_validation_metric_sanity.sql",
]

suite_labels = [
    "Null & Duplicate Checks",
    "Referential Integrity Checks",
    "Metric Sanity Checks",
]

# Expected row count for every test query: 0 means the assertion passes.
# A non-zero result means the test detected a data quality violation.
EXPECTED_ZERO_ROWS = True

results = []  # list of dicts: {suite, query_idx, label, rows, passed}

with get_connection() as conn:
    for suite_file, suite_label in zip(test_files, suite_labels):
        path   = get_sql_path(suite_file)
        queries = load_queries(path)
        for i, query in enumerate(queries):
            df     = pd.read_sql(query, conn)
            passed = len(df) == 0
            results.append({
                "suite":     suite_label,
                "test_num":  i + 1,
                "rows_returned": len(df),
                "passed":    passed,
                "detail_df": df,   # stored for display on failure
            })

# Build summary DataFrame
df_summary = pd.DataFrame([
    {
        "Suite":          r["suite"],
        "Test #":         r["test_num"],
        "Rows Returned":  r["rows_returned"],
        "Status":         "PASS" if r["passed"] else "FAIL",
    }
    for r in results
])

total_tests  = len(results)
passed_tests = sum(r["passed"] for r in results)
failed_tests = total_tests - passed_tests

print(f"Data Quality Suite Results  |  {passed_tests}/{total_tests} checks passed")
print("=" * 60)
display(df_summary)

# ---------------------------------------------------------------------------
# Show detail rows for any failed checks
# ---------------------------------------------------------------------------
if failed_tests > 0:
    print(f"\n⚠️  {failed_tests} check(s) returned unexpected rows:")
    for r in results:
        if not r["passed"]:
            print(f"\n  Suite: {r['suite']} | Test {r['test_num']}")
            display(r["detail_df"].head(20))
else:
    print("\n✅  All data quality checks passed. Dataset is safe to analyse.")

# ---------------------------------------------------------------------------
# Supplementary Python-level checks on core analytical views
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Supplementary view-level checks (Python assertions)")
print("=" * 60)

view_checks = []

with get_connection() as conn:
    # vw_order_fact — delivered orders only
    df_of = pd.read_sql(
        "SELECT * FROM olist.vw_order_fact WHERE order_status = 'delivered'", conn
    )
    view_checks.append(("vw_order_fact",          "Row count > 0",
                        len(df_of) > 0))
    view_checks.append(("vw_order_fact",          "total_order_value >= 0",
                        (df_of["total_order_value"] >= 0).all()))
    view_checks.append(("vw_order_fact",          "No null order_id",
                        df_of["order_id"].notna().all()))

    # vw_delivery_sla_metrics
    df_sla = pd.read_sql("SELECT * FROM olist.vw_delivery_sla_metrics", conn)
    view_checks.append(("vw_delivery_sla_metrics","Row count > 0",
                        len(df_sla) > 0))
    view_checks.append(("vw_delivery_sla_metrics","actual_delivery_days not all null",
                        df_sla["actual_delivery_days"].notna().any()))

    # vw_customer_monthly_metrics
    df_cm = pd.read_sql("SELECT * FROM olist.vw_customer_monthly_metrics", conn)
    view_checks.append(("vw_customer_monthly_metrics","Row count > 0",
                        len(df_cm) > 0))
    view_checks.append(("vw_customer_monthly_metrics","months_since_first_purchase >= 0",
                        (df_cm["months_since_first_purchase"] >= 0).all()))

df_view_checks = pd.DataFrame(view_checks, columns=["View", "Check", "Passed"])
df_view_checks["Status"] = df_view_checks["Passed"].map({True: "PASS", False: "FAIL"})
display(df_view_checks[["View", "Check", "Status"]])
