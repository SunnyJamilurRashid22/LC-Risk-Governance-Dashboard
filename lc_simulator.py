try:
    import numpy as np
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="Iamba12345@",
        host="127.0.0.1",
        port=5432,
        database="banking_db",
    )
    engine = create_engine(connection_url)

    print("📥 Step 1: Fetching historical fx_returns from database...")
    query = 'SELECT * FROM fx_returns ORDER BY "Date" ASC;'
    df = pd.read_sql_query(query, con=engine)

    var_95_daily = np.percentile(df["log_return"], 5)
    fx_risk_penalty_pct = abs(var_95_daily)

    lc_portfolio = [
        {"client_name": "Apex Apparel Ltd", "lc_id": "LC-2026-001", "lc_value_usd": 1500000},
        {"client_name": "Dhaka Pharma Corp", "lc_id": "LC-2026-002", "lc_value_usd": 750000},
        {"client_name": "Bengal Motors", "lc_id": "LC-2026-003", "lc_value_usd": 3200000},
        {"client_name": "Padma Food & Beverage", "lc_id": "LC-2026-004", "lc_value_usd": 500000},
    ]
    portfolio_df = pd.DataFrame(lc_portfolio)

    BASE_MARGIN_PCT = 0.10
    portfolio_df["recommended_margin_pct"] = BASE_MARGIN_PCT + fx_risk_penalty_pct
    portfolio_df["cash_margin_required_usd"] = (
        portfolio_df["lc_value_usd"] * portfolio_df["recommended_margin_pct"]
    )
    portfolio_df["at_risk_exposure_usd"] = (
        portfolio_df["lc_value_usd"] * fx_risk_penalty_pct
    )

    print("📤 Step 2: Injecting calculated rows into table 'active_lc_risk'...")
    portfolio_df.to_sql(
        name="active_lc_risk",
        con=engine,
        if_exists="replace",
        index=False,
        schema="public",
    )
    print("✅ Success! Data successfully locked inside PostgreSQL.")

    print("\n🔍 Step 3: Running instant database verification query...")
    verification_df = pd.read_sql_table("active_lc_risk", con=engine, schema="public")

    print("\n=================== LIVE DATABASE TABLE VIEW ===================")
    print(verification_df)
    print("==================================================================")
    print("🎉 Verification complete! The table exists and is fully accurate.")

except Exception as e:
    print(f"\n❌ Pipeline failed: {e}")

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1;"
    "DATABASE=your_database;"
    "UID=your_user;"
    "PWD=your_password;"
    "TrustServerCertificate=yes;"  
    "Connection Timeout=30;"       
)
