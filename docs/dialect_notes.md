# Dialect Notes: PostgreSQL First

This project has been explicitly designed for **PostgreSQL 15+** via Docker.

## Key Differences & Implementation details

### 1. Data Types
- `TIMESTAMP`: Utilized for all dates instead of `DATETIME2`.
- `NUMERIC`: Used natively instead of `DECIMAL`.
- `VARCHAR/TEXT`: Retained as standard.

### 2. Loading Strategy (psql \copy)
PostgreSQL client `psql` utilizes the `\copy` meta-command, which smoothly executes data ingestion from local client paths to the server natively. This is the simplest local approach and avoids server-side volume permission errors.

### 3. Date Math
Date extraction and differences calculation relies strictly on PostgreSQL native features rather than `DATEDIFF()`:
- **Elapsed time in days:** `EXTRACT(EPOCH FROM (end_date - start_date))/86400.0`
- **Elapsed time in months:** `EXTRACT(year FROM age(current, past)) * 12 + EXTRACT(month FROM age(current, past))`

### 4. Coalescing and Nulls
ANSI standard `COALESCE()` is retained as it remains strictly cross-compatible.
