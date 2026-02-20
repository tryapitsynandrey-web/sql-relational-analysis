# Skill to Certification Mapping

This document maps the technical skills and methodologies demonstrated in the `sql-relational-analysis` repository directly to industry-standard data analytics and data science certifications. 

### 1. Google Data Analytics Professional Certificate
*   **Overview:** Focuses on foundational data analysis tasks including data cleaning, problem-solving, SQL queries, and basic visualization.
*   **Core Skills Claimed:** Data cleaning, SQL (aggregation, filtering), data visualization, analytical problem-solving.
*   **Evidence in Project:**
    *   `sql/tests/*.sql`: Demonstrates data quality checks, null handling, and referential integrity testing typical of the data cleaning phase.
    *   `sql/analysis/*.sql`: Demonstrates foundational SQL including JOINs, GROUP BY, aggregations, and conditional logic.
    *   `analysis/notebooks/*.ipynb`: Demonstrates data visualization and charting using Matplotlib and pandas, fulfilling presentation requirements.
*   **Gaps:** The certification leverages Tableau or R for visualization. This project relies entirely on Python (pandas/matplotlib) and lacks a dedicated proprietary dashboarding tool.

### 2. Google Advanced Data Analytics Professional Certificate
*   **Overview:** Emphasizes advanced Python programming, working with Jupyter notebooks, statistical analysis, and exploratory data analysis (EDA).
*   **Core Skills Claimed:** Python programming, Jupyter notebooks, EDA, statistical summarization.
*   **Evidence in Project:**
    *   `analysis/notebooks/*.ipynb`: Extensive use of Python and pandas for dynamic dataframe manipulation and exploratory data analysis.
    *   `analysis/reports/*.md`: Translation of EDA into structured executive summaries, outlining key findings and actionable insights.
*   **Gaps:** The certification heavily features predictive modeling, regression, and machine learning (via scikit-learn). This project is strictly relational/historical analytics and lacks predictive models.

### 3. IBM Data Analyst Professional Certificate
*   **Overview:** Focuses on Python, SQL, data visualization, and the construction of data analysis pipelines.
*   **Core Skills Claimed:** Python (pandas), SQL (relational database concepts), Data Visualization, Data Pipelines.
*   **Evidence in Project:**
    *   `sql/ddl/*.sql` & `sql/load/*.sql`: Demonstrates relational database construction, schema creation, and ETL/bulk data ingestion pipelines.
    *   `sql/views/*.sql`: Demonstrates intermediate SQL and semantic business-logic layer virtualization.
    *   `analysis/notebooks/*.ipynb`: Fully covers the Python/pandas data manipulation and visualization curriculum requirements.
*   **Gaps:** The certification includes Excel basics and IBM Cognos Analytics, neither of which are utilized in this strictly code-first environment.

### 4. IBM Data Science Professional Certificate
*   **Overview:** A rigorous program covering Python, SQL, data analysis methodology, and data-wrangling for data science.
*   **Core Skills Claimed:** Python for Data Science, SQL data extraction, Data Analysis methodology.
*   **Evidence in Project:**
    *   `docs/assumptions_and_next_steps.md` & `meta/*.md`: Reflects rigorous data science methodology by explicitly documenting data grains, constraints, limitations, and testing assumptions before analysis.
    *   `sql/analysis/02_cohorts_and_retention.sql`: Demonstrates complex data wrangling (cohort matrix generation, window functions, time-deltas) typical of the preliminary data science feature-engineering phase.
*   **Gaps:** Lacks the explicit Machine Learning (classification, clustering) and geospatial mapping (e.g., Folium) components of the IBM Data Science track.

### 5. Microsoft Power BI Data Analyst (PL-300)
*   **Overview:** Focuses on preparing data, modeling data, and visualizing data to answer business questions.
*   **Core Skills Claimed:** Data preparation, relational data modeling, analytical reporting.
*   **Evidence in Project:**
    *   `sql/ddl/03_add_constraints.sql` & `sql/views/*.sql`: Directly maps to the "Data Modeling" curriculum. Demonstrates establishing primary/foreign key relationships and abstracting raw tables into star-schema-like fact/dimension views.
    *   `analysis/reports/*.md`: Maps to the analytical interpretation of reports and the generation of actionable business metrics.
*   **Gaps:** This is a code-first repository. It completely lacks the proprietary Power BI interface, DAX (Data Analysis Expressions), and Power Query (M) skills required by the certification. Addressed by shifting the visualization burden to pure Python.

### 6. Microsoft SQL / Business Analyst
*   **Overview:** Focuses on querying data with robust SQL logic and translating business needs into data solutions.
*   **Core Skills Claimed:** Advanced SQL querying, business requirements translation.
*   **Evidence in Project:**
    *   `sql/analysis/*.sql`: Demonstrates proficiency in advanced SQL concepts, including CTEs, Window Functions (`OVER`, `PARTITION BY`, `ROWS BETWEEN`), and native aggregate pushdowns (`FILTER (WHERE...)`).
    *   `docs/recommendations.md` & `README.md`: Demonstrates direct translation of complex SQL outputs into concrete, prioritized business strategies based on effort and impact.
*   **Gaps:** Explicitly utilizes PostgreSQL 15+ instead of Microsoft SQL Server (T-SQL). While standard ANSI SQL applies universally, T-SQL specific syntax and SQL Server Management Studio (SSMS) are not demonstrated here.
