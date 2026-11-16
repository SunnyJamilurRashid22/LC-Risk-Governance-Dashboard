import pandas as pd
import yfinance as yf
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

print("Fetching market data...")
ticker = "USDBDT=X"
data = yf.download(ticker, start="2025-01-01", end="2026-11-01")
df = data[['Close']].copy()
df.columns = ['close_price']
df['log_return'] = np.log(df['close_price'] / df['close_price'].shift(1))
df = df.dropna()
final_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Iamba12345@",  
    host="127.0.0.1",
    port=5432,
    database="banking_db"
)
engine = create_engine(final_url)
print("Exporting pipeline data to PostgreSQL...")
df.to_sql(name='fx_returns', con=engine, if_exists='replace', index=True)
print("Success! Data successfully written to the 'fx_returns' table.")
