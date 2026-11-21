# End-to-End E-commerce Analytics for an Indian D2C Brand

**Stack:** Python · PostgreSQL · BigQuery SQL · Excel · Power BI · scikit-learn

A reproducible portfolio case study for a fictional Indian direct-to-consumer fashion brand, **Vastraa**. The project covers data generation, data quality, dimensional modelling, product and marketing analytics, experimentation, unit economics, predictive modelling and executive communication.

## Business context
Vastraa sells apparel through its own website and marketplaces. The CEO wants profitable growth; the CMO needs channel allocation; Product needs funnel and experiment evidence; Finance needs contribution economics; Operations needs lower COD/RTO losses.

All company and transaction data are synthetic. No real customer information is used.

## Quick start (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python python/generate_data.py --orders 60000 --seed 20261121
python python/run_analytics.py
```
Generated CSVs are written to `data/raw`, `data/processed` and `data/exports`; they are intentionally gitignored. The generator defaults to 60,000 orders across 18 months and creates a few hundred thousand GA4-style events.

## PostgreSQL
Create a database, then run:
```powershell
psql -U postgres -d vastraa_analytics -f sql/01_postgres_schema.sql
psql -U postgres -d vastraa_analytics -f sql/02_staging_transformations.sql
psql -U postgres -d vastraa_analytics -f sql/03_mart_models.sql
psql -U postgres -d vastraa_analytics -f sql/04_data_quality_tests.sql
psql -U postgres -d vastraa_analytics -f sql/05_reporting_views.sql
```
Load generated CSVs into `raw` tables using `\copy` (commands are in `docs/postgres_loading.md`). SQL files use PostgreSQL syntax. `sql/bigquery/` contains BigQuery-specific equivalents and partitioning guidance.

## Analysis and deliverables
- `python/run_analytics.py`: data quality profile, KPI outputs, funnel, cohorts, RFM/K-Means, attribution comparison, contribution margin, experiment readouts, repeat-purchase model and demand forecast.
- `notebooks/01_exploratory_data_analysis.ipynb`: runnable EDA notebook.
- `excel/unit_economics_scenario_model.xlsx`: editable COD-share scenario model with live formulas.
- `dashboards/`: Power BI build instructions and DAX.
- `docs/`: charter, stakeholders, questions, KPI and data dictionaries, ERD, ground truth and warehouse setup.
- `reports/`: stakeholder-ready written deliverables and presentation script.

## Important modelling conventions
- Revenue is GST-inclusive in source orders. Net sales exclude GST using the configured 5% blended illustrative GST rate; this is a simplifying assumption, not tax advice.
- A delivered order is an order with `order_status = 'delivered'`. Returns are reported separately and reduce net realised sales in the financial layer.
- CAC = attributable acquisition spend / new customers acquired. Attribution models are compared as sensitivity analyses; none is treated as causal truth.
- RTO is a failed delivery with `delivery_outcome = 'RTO'`. Tier-3 COD risk is deliberately higher in the synthetic data.
- Bot traffic and duplicate events are retained in raw data; staging removes known bot traffic and deduplicates event IDs.
- Experiment outcomes are simulated and are not real-world evidence.

## Suggested portfolio walkthrough
1. Explain the commercial problem and KPI tree.
2. Show reproducible generation and quality controls.
3. Demonstrate funnel, cohorts and channel attribution.
4. Explain COD/RTO and contribution margin.
5. Present experiment decisions and predictive outputs.
6. Close with recommendations and trade-offs.

## Reproducibility
Default seed: `20261121`. All generated tables are deterministic for a fixed seed and order count. Results can vary if you change the seed or date range.
