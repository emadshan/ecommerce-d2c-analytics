# Vastraa — End-to-End E-commerce Analytics

**A data analytics portfolio project focused on profitable growth for a fictional Indian D2C fashion brand.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=flat&logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)

**Tools:** Python · PostgreSQL · BigQuery SQL · Excel · Power BI · scikit-learn

---

## 1. Project Overview

Vastraa is a fictional Indian direct-to-consumer fashion brand selling apparel through its own website and online marketplaces.

The objective of this project is to build an end-to-end analytics workflow that helps business stakeholders understand performance, identify growth opportunities, and evaluate profitability.

The project covers the analytics lifecycle:

- Synthetic data generation and validation
- Data cleaning and transformation
- Relational data modelling and SQL analytics
- Marketing attribution and customer segmentation
- Product funnel and cohort analysis
- Unit economics and COD/RTO analysis
- Experimentation and predictive modelling
- Executive reporting and business recommendations

> **Data disclaimer:** All company, customer, order, event, and experiment data in this project are synthetic. No real customer information is used. Experiment outcomes are simulated, not real-world evidence.

## 2. Business Problem

The business has different stakeholders with different questions:

| Stakeholder | Business question |
|---|---|
| CEO | Is the business growing profitably? |
| CMO | Which acquisition channels deserve more budget? |
| Product | Where are customers dropping out of the purchase funnel? |
| Finance | What drives contribution economics and profitability? |
| Operations | How can COD and return-to-origin losses be reduced? |

The analysis is designed to translate these questions into measurable KPIs, analytical outputs, and business decisions.

## 3. Technical Architecture

```text
Synthetic Data Generation
          |
          v
   Raw CSV Datasets
          |
          v
 Data Quality & Cleaning
          |
          v
 PostgreSQL / BigQuery
          |
          v
 Analytics & Data Models
          |
          +------------------+
          |         |        |
          v         v        v
       Python    Excel    Power BI
          |
          v
 Predictive & Experiment Analysis
          |
          v
 Stakeholder Reports
```

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, cleaning, analysis and automation |
| Pandas / NumPy | Data manipulation and numerical analysis |
| PostgreSQL | Relational storage, transformations and analytical queries |
| BigQuery SQL | Warehouse setup and partitioning examples |
| Excel | Unit economics and scenario modelling |
| Power BI | Business performance dashboards and KPI reporting |
| scikit-learn | Customer segmentation and predictive modelling |
| Jupyter Notebook | Exploratory data analysis |

## 5. Dataset

The data generator creates a reproducible synthetic dataset with a default of **60,000 orders across 18 months**, along with customers, products, order items, marketing and GA4-style event data.

The generator uses a configurable random seed so that the dataset can be recreated consistently.

Generated files are written to:

- `data/raw/`
- `data/processed/`
- `data/exports/`

These generated datasets are intentionally excluded from Git tracking.

## 6. Analytics Workstreams

### Data quality and preparation
- Profile source datasets.
- Identify missing values and duplicates.
- Retain raw data and apply cleaning rules in staging.
- Validate analytical outputs.

### Marketing analytics
- Compare marketing attribution approaches.
- Evaluate channel economics and acquisition spend.
- Calculate customer acquisition cost (CAC).
- Support channel budget allocation decisions.

### Product analytics
- Analyze the customer purchase funnel.
- Examine device-level conversion patterns.
- Build customer cohort and retention analyses.

### Customer analytics
- Apply RFM segmentation.
- Use K-Means clustering for customer grouping.
- Develop repeat-purchase modelling outputs.

### Unit economics and operations
- Evaluate contribution margin.
- Model COD-share scenarios.
- Analyze return-to-origin (RTO) patterns and delivery outcomes.

### Experimentation and forecasting
- Produce experiment readouts.
- Build a repeat-purchase model.
- Generate monthly demand forecasts.

## 7. Project Deliverables

| Folder | Contents |
|---|---|
| `python/` | Data generation, quality checks and analytics scripts |
| `sql/` | PostgreSQL schema, transformations, marts, tests and reporting views |
| `sql/bigquery/` | BigQuery-specific SQL and partitioning example |
| `notebooks/` | Exploratory data analysis notebook |
| `dashboards/` | Power BI dashboard, DAX measures and build guide |
| `excel/` | Unit economics scenario model |
| `docs/` | Project charter, business questions, KPI dictionary, data dictionary, ERD and setup guides |
| `reports/` | CEO, CFO, CMO and product insights reports, experiment readouts and walkthrough materials |

## 8. Getting Started

### Requirements
- Python
- PostgreSQL
- Power BI Desktop (to inspect the dashboard)
- Git

### Run locally on Windows PowerShell

```powershell
git clone https://github.com/emadshan/ecommerce-d2c-analytics.git
cd ecommerce-d2c-analytics

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python python/generate_data.py --orders 60000 --seed 20261121

python python/run_analytics.py
```

Generated CSV outputs are stored in the `data/` directories and are not committed to the repository.

### PostgreSQL setup

Create a database named `vastraa_analytics`, then execute:

```powershell
psql -U postgres -d vastraa_analytics -f sql/01_postgres_schema.sql
psql -U postgres -d vastraa_analytics -f sql/02_staging_transformations.sql
psql -U postgres -d vastraa_analytics -f sql/03_mart_models.sql
psql -U postgres -d vastraa_analytics -f sql/04_data_quality_tests.sql
psql -U postgres -d vastraa_analytics -f sql/05_reporting_views.sql
```

Load generated CSV files into the raw tables using the instructions in `docs/postgres_loading.md`.

## 9. Important Modelling Assumptions

- Source order revenue is GST-inclusive. Net sales exclude GST using an illustrative blended GST rate of 5%; this is a simplifying assumption, not tax advice.
- Delivered orders are identified by `order_status = 'delivered'`.
- Returns are reported separately and reduce net realised sales in the financial layer.
- CAC is calculated as attributable acquisition spend divided by new customers acquired.
- Attribution models are compared as sensitivity analyses and are not treated as causal truth.
- RTO is identified using `delivery_outcome = 'RTO'`.
- Tier-3 COD risk is deliberately higher in the synthetic dataset.
- Raw event data retains bot traffic and duplicate events; staging removes known bot traffic and deduplicates event IDs.
- Experiment results are simulated and should not be interpreted as actual business evidence.

## 10. Suggested Project Walkthrough

1. Introduce the business context and stakeholder questions.
2. Explain the data generation process and quality checks.
3. Demonstrate the SQL data model and transformations.
4. Present marketing attribution, funnel and cohort findings.
5. Explain customer segmentation and COD/RTO economics.
6. Walk through experimentation and predictive outputs.
7. Conclude with business recommendations and trade-offs.

## 11. Reproducibility

Default random seed: `20261121`.

Generated tables are deterministic for a fixed seed and order count. Results may change when the seed or date range is changed.

---

## Repository

**GitHub:** https://github.com/emadshan/ecommerce-d2c-analytics

*Built as a hands-on portfolio case study demonstrating end-to-end data analytics, SQL, Python, business intelligence, and business problem-solving.*

## Connect

I'm interested in Data Analyst, Business Analyst and Analytics Engineer opportunities.

- **LinkedIn:** [Emad Shanavas](https://www.linkedin.com/in/emadshan/)
- **GitHub:** [emadshan](https://github.com/emadshan)
- **Email:** [emadshanavasmk@gmail.com](mailto:emadshanavasmk@gmail.com)
