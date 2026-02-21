# Naming Conventions

## General SQL Rules
*   **Case format:** `snake_case` is strictly enforced for all schemas, tables, views, and columns. No CamelCase or PascalCase.
*   **Keywords:** SQL keywords (`SELECT`, `FROM`, `OVER`, `PARTITION BY`, `FILTER`) must be entirely UPPERCASE.
*   **Aliases:** Always use descriptive aliases (`c` for `customers`, `o` for `orders`). Computed columns must always be aliased explicitly with `as field_name`.

## Object Naming
*   Base tables accurately reflect plural entities (`orders`, `products`).
*   Views are prefixed with `vw_` to easily distinguish virtual layers from materialized tables.
*   Views acting as fact tables suffix `_fact` (e.g., `vw_order_fact`).
*   Views acting as aggregated metric tables suffix `_metrics` (e.g., `vw_delivery_sla_metrics`).

## Metric and Column Naming
Inferred or calculated metric columns must follow strictly typed suffixes/prefixes to self-document their intent and data type:
*   `total_` : Absolute summations (e.g., `total_revenue`, `total_orders`).
*   `avg_` : Mean averages (e.g., `avg_order_value`, `avg_review_score`).
*   `_pct` : Computed ratios representing percentages (0-100 scale, e.g., `retention_rate_pct`).
*   `_days` : Time duration metrics indicating the unit (e.g., `actual_delivery_days`).
*   `is_` : Boolean indicator flags (e.g., `is_delayed`).

## Consistency Rationale
Enforcing semantic suffixes (`_pct`, `_days`) guarantees downstream users (like the Python Insights Layer) can naturally infer how to format the data without constantly querying the `information_schema` or guessing if `delay` means milliseconds, days, or a raw timestamp. Utilizing `vw_` protects raw access and guarantees analysts are querying the standardized semantic layer.
