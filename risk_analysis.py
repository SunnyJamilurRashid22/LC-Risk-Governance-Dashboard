import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from scipy.stats import norm

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Iamba12345@",  
    host="127.0.0.1",
    port=5432,
    database="banking_db"
)
engine = create_engine(connection_url)
print("📥 Fetching fx_returns data from PostgreSQL...")
query = "SELECT * FROM fx_returns ORDER BY \"Date\" ASC;"
df = pd.read_sql_query(query, con=engine, parse_dates=['Date'])
df.set_index('Date', inplace=True)

daily_vol = df['log_return'].std()
annualized_vol = daily_vol * np.sqrt(252)
var_95_historical = np.percentile(df['log_return'], 5)

print("\n================ RISK DASHBOARD METRICS ================")
print(f"✅ Total Observations Analyzed : {len(df)} days")
print(f"📉 Daily Log Return Volatility  : {daily_vol:.6f}")
print(f"⚡ Annualized FX Volatility    : {annualized_vol:.4%}")
print(f"🛡️ 95% Historical Daily VaR   : {var_95_historical:.4%}")
print("========================================================")
