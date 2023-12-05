# Import Libraries
from config import *
from datetime import timedelta, date
import sqlite3
import yfinance as yf
import pandas as pd
import csv

# Get Date Range
today = date.today()  # Get the current date
start_date = today - timedelta(days=29)  # 29 days before today

# Connect to SQLite Database
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Read Stock Symbols from CSV
symbols = []
stock_ids = {}

with open('minute_stocks.csv') as f:
    reader = csv.reader(f)

    for line in reader:
        symbols.append(line[1])

print(symbols)
cursor.execute("""
    SELECT * FROM stock
""")

stocks = cursor.fetchall()

for stock in stocks:
    symbol = stock['yf_symbol']
    stock_ids[symbol] = stock['id']

print(symbol)

# Fetch historical data for each stock in the list
for symbol in symbols:
    end_date_range = start_date+timedelta(days=4)
    
    while start_date < end_date_range:
        end_date = start_date + timedelta(days=4)
        print(f"===Fetching minute bars {start_date}-{end_date} for {symbol}")

        try:
            # Corrected the stock symbol
            minutes = yf.download(symbol, start=start_date, end=end_date, interval="1m")
            
            # Set DatetimeIndex explicitly
            minutes.index = pd.to_datetime(minutes.index)
            
            # Resample and forward-fill missing values
            minutes_resampled = minutes.resample('1min').ffill()

            for index, row in minutes_resampled.iterrows():
                cursor.execute("""
                            INSERT INTO stock_price_minute (stock_id, datetime, open, high, low, close, volume)
                            VALUES (?,?,?,?,?,?,?)
                            """, (stock_ids[symbol], index.tz_localize(None).isoformat(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
                
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

        start_date = start_date + timedelta(days=7)

# Commit and Close Database Connection
connection.commit()
connection.close()




