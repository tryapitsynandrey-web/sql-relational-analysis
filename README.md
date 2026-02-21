# Olist E-Commerce Analytics: From Data to Strategy 📊

A professional Streamlit-powered analytics application that transforms raw transactional data from Brazilian e-commerce into interactive business intelligence.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.0+-orange.svg)](https://plotly.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

---

## 🚀 Executive Summary (STAR Method)

- **Situation:** Olist operates a massive marketplace in Brazil, managing high-volume transactions, logistics, and customer feedback. Stakeholders lacked a unified, interactive tool to visualize performance drivers and identify operational risks.
- **Task:** Transition from static, script-based analysis to a professional web-based dashboard that provides real-time KPIs, interactive visualizations, and dynamic business recommendations.
- **Action:** Developed a layered architecture (PostgreSQL -> Core Data Layer -> Streamlit UI). Refactored SQL logic into a cached data provider and implemented interactive charts using Plotly Express for drill-down capabilities.
- **Result:** Delivered a decision-ready executive dashboard that highlights revenue peaks, categories with the highest growth, and regional logistics bottlenecks, enabling data-driven strategic planning for the C-suite.

---

## ⚙️ Quick Start

### 1. Prerequisite Setup
Ensure your local environment is configured with PostgreSQL and the Olist dataset:
```bash
# Clone the repo and install dependencies
pip install -r requirements.txt

# Configure your database env
cp analysis/.env.example analysis/.env
```

### 2. Seed Data
If you haven't run the pipeline yet, initialize the database:
```bash
./scripts/run_pipeline.sh
```

### 3. One-Click Launch
Start the web application directly from the root:
```bash
python start_analysis.py
```

---

## 🏛 Technical Architecture

The project follows a strict three-tier architecture to ensure maintainability and separation of concerns:

```mermaid
graph TD
    subgraph UI_Layer[Streamlit UI Layer]
        Main[src/main.py] --> Dashboard[src/ui/dashboard.py]
    end
    
    subgraph Core_Layer[Business Logic Layer]
        Dashboard --> DP[src/core/data_provider.py]
        DP -- "st.cache_data" --> Logic[SQL Logic]
    end
    
    subgraph Data_Layer[Data Infrastructure]
        DP --> DB[src/core/db_client.py]
        DB --> Postgres[(PostgreSQL)]
    end
```

- **Persistence Layer**: Raw data ingestion into PostgreSQL.
- **Logic Layer**: Python-based data provider utilizing `st.cache_data` to minimize DB overhead.
- **Presentation Layer**: Modular Streamlit components and Plotly charts.

---

## 🛠 Features

- **Dynamic KPI Cards**: Instant tracking of Revenue, AOV, and Order Volume with period-over-period deltas.
- **Interactive Visualizations**: Zoomable revenue trends and regional GMV distribution maps.
- **Executive Summary**: Real-time business insights generated via dynamic Python logic.
- **One-Click Deployment**: Simplified launch sequence for developers and analysts.

---

## ✉️ Author
**Andrew Shwarts**  
[LinkedIn](https://linkedin.com/in/andrewshwarts) | [Portfolio](https://example.com)