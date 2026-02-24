# Olist E-Commerce Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-%3E%3D1.24-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)

## Description
This repository contains an end-to-end data analytics pipeline and interactive Streamlit web dashboard for analyzing e-commerce data. It provides structured schema definitions, data ingestion scripts, semantic views, and automated data quality tests using PostgreSQL, alongside Jupyter notebooks for exploratory data analysis.

## Architecture Overview
The project is structurally aligned into a layered architecture:
- **Database Layer (`sql/`)**: Contains Data Definition Language (DDL) scripts, bulk data loading processes, and semantic views orchestrating a star/snowflake schema in PostgreSQL.
- **Testing Layer (`sql/tests/`)**: Automated SQL-based data quality and consistency assertions executed via a runner script.
- **Analytics Layer (`analysis/`)**: Jupyter notebooks tailored for granular reporting, alongside generated visualizations and local environment configurations.
- **Application Core (`src/core/`)**: Python data access modules bridging the database structure with the display logic securely.
- **User Interface (`src/ui/`, `src/main.py`)**: A Streamlit interface delivering analytical insights via Plotly visualizations, supported by a specialized entry-point wrapper `start_analysis.py`.
- **Infrastructure (`scripts/`, `Dockerfile`)**: Bash routines orchestrating Docker-based PostgreSQL setup, sequential DDL deployment, schema testing, and dataset validation.

## Features
- Complete reproducible PostgreSQL database initialisation (DDL, Data Loading, Semantic Views).
- Automated SQL data quality validation (referential integrity, metric sanity, null/duplicate checks).
- Interactive web-based metrics dashboard via Streamlit and Python.
- Containerized PostgreSQL 15 environment support.
- Configurable environment variable management (`.env`).
- Explanatory analytics generated via Jupyter Notebooks.

## Project Structure
```text
.
├── Dockerfile                  # PostgreSQL 15 database container setup
├── README.md                   # Project documentation
├── analysis/                   # Jupyter notebooks (.ipynb) and generated analytical reports
├── docs/                       # Auxiliary documentation
├── meta/                       # Project metadata
├── requirements.txt            # Python dependencies
├── scripts/                    # Shell and Python scripts for pipeline validation and execution
├── sql/                        # SQL scripts (DDL, load, tests, views) layer
├── src/                        # Dashboard python packages (core, ui) and runner code
└── start_analysis.py           # Launch script for the web dashboard app
```

## Installation
### Local
1. Ensure Python 3.x is installed.
2. Clone the repository and navigate to the project root.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the PostgreSQL database locally or ensure access to a running instance.

### Docker
1. The repository supports containerized PostgreSQL. Build and run the database container:
   `docker build -t olist-db .`
2. Follow local installation steps for the Python application environment.

## Usage
### CLI
- Internal pipelines and database orchestration are accessible via the `scripts/` directory. Run the initialization script (depends on valid `.env` config):
  `./scripts/run_pipeline.sh` 
- Data quality tests can be manually run explicitly:
  `python scripts/run_sql_tests.py`

### Web
- Launch the Streamlit analytic dashboard using the dedicated launch file:
  `python start_analysis.py`

## Data Storage
- **PostgreSQL 15**: Primary relational data storage and aggregations.
- **Raw CSV Files**: Source datasets are anticipated to be localized within `data/raw/olist/`.
- **Python / Streamlit Caching**: Volatile caching is managed in-memory on the application tier.

## Configuration
- Project configuration heavily leverages environment variables.
- An environment file must be located in `analysis/.env` mapping database secrets: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- The application automatically attempts to replicate `analysis/.env.example` to `analysis/.env` if missing.

## Development Notes
- `PGPASSWORD` is natively exposed inside pipeline shell scripts in favor of loaded `.env` bindings.
- Database load routines are hardcoded via SQL to depend on exact flat file system locations (`data/raw/olist/*.csv`).

## Limitations & Assumptions
- **Raw Data Presence**: It is assumed that raw data is manually positioned directly into `data/raw/olist/*.csv` as no specific automated fetching/downloading script was verified in the repository.
- **Python Version Limit**: While frameworks restrict downwards versions to relatively modern iterations (`pandas >= 2.0`), no firm base runtime Python requirement is explicitly documented or bound.
- **Docker Compose Constraints**: Although a `Dockerfile` exists strictly for a base PostgreSQL image, no `docker-compose.yml` natively chains the database and web app together, meaning orchestration remains manual.

## License
Not specified