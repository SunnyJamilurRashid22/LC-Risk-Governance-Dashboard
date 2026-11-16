# LC Risk Governance Dashboard

An automated end-to-end trade finance risk analytics pipeline integrating **Python**, **PostgreSQL**, and **Power BI** to monitor Letter of Credit (LC) collateral exposure and foreign exchange volatility.

![Dashboard Preview](dashboard_preview.png)

## Architecture & Tech Stack
* **Database (`PostgreSQL`):** Stores transactional LC risk records (`active_lc_risk`) and historical currency returns (`fx_returns`) inside `banking_db`.
* **Data Pipeline (`Python`):** Uses `pandas`, `numpy`, `yfinance`, and `SQLAlchemy` (`psycopg2`) to compute vectorized log returns, 95% Historical Daily Value at Risk (VaR), and cash margin breach flags.
* **Incremental Refresh (`Power Query M`):** Parameter-driven date filtering (`RangeStart` / `RangeEnd`) for scalable data ingestion.
* **Governance UI (`Power BI & DAX`):** Star-schema data model with dynamic conditional formatting (`#8B0000` Deep Crimson alerts) for immediate limit-breach detection.

## Key Modules
* `app.py` / `lc_simulator.py`: Simulates active Letter of Credit portfolios, calculates required cash margin cushions, and writes risk tables to PostgreSQL.
* `risk_analysis.py`: Fetches historical currency pairs, computes annualized FX volatility and 95% daily VaR, and audits compliance thresholds.
* `check_db.py`: Verifies database table integrity and row counts prior to dashboard refresh.
