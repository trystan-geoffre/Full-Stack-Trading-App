# Import Libraries
import yfinance as yf
import sqlite3
from config import *
from datetime import datetime
import talib

# Connect to your SQLite database
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Retrieve Stock Symbols from the Database
cursor.execute("""
               SELECT id, symbol, name, last_download_date FROM stock
               """)
stocks = cursor.fetchall()

# Define the date range
end_date = datetime.now().strftime("%Y-%m-%d")

# Create a set to keep track of symbols already processed
processed_symbols = set()

# Create a set to store symbols found in Yahoo Finance
symbols_in_yahoo_finance = set()

# Iterate through symbols in the database
for stock in stocks:
    symbol = stock['symbol']
    stock_id = stock['id']
    last_download_date = stock['last_download_date'] #'2023-01-01' for the first download
    symbol_for_download = symbol.replace('/', '-').replace('.', '-')

    # Check if this symbol has already been processed in a previous run
    if symbol_for_download not in processed_symbols:
        if last_download_date is None or last_download_date < end_date:
            try:
                # Attempt to download data with the "max" period
                data = yf.download(symbol_for_download, start=last_download_date, end=end_date)
            except Exception as e:
                if "Period 'max' is invalid" in str(e):
                    # "max" period is invalid, download data for 1 day
                    data = yf.download(symbol_for_download, period="1d")
                else:
                    raise  # Re-raise the exception if it's not the expected one

            if data.empty:
                # No data found for this symbol
                print(f"No data found for symbol {symbol}")
            else:
                # Mark this symbol as processed
                processed_symbols.add(symbol_for_download)
                symbols_in_yahoo_finance.add(symbol_for_download)

                # Check if a symbol with the same name already exists in the database stock
                cursor.execute("SELECT id FROM stock WHERE name = ?", (symbol,))
                existing_stock = cursor.fetchone()
                if existing_stock:
                    # Symbol with the same name exists, remove it
                    cursor.execute("DELETE FROM stock WHERE id = ?", (existing_stock['id'],))
                
                # Calculate the SMA (Simple Moving Averages) for 20 and 50
                data['SMA_20'] = talib.SMA(data['Close'], timeperiod=20)
                data['SMA_50'] = talib.SMA(data['Close'], timeperiod=50)
                
                # Calculate the RSI (Relative Strength Index) for 14
                data['RSI_14'] = talib.RSI(data['Close'], timeperiod=14)
                                
                # Insert data into the database
                for index, row in data.iterrows():
                    cursor.execute(
                        "INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (stock_id, index.date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['SMA_20'], row['SMA_50'], row['RSI_14'])
                    )

                # Update the last download date for the symbol
                cursor.execute("UPDATE stock SET last_download_date = ? WHERE id = ?", (end_date, stock_id))
                cursor.execute("UPDATE stock SET yf_symbol = ? WHERE id = ?", (symbol_for_download, stock_id))
# Close the database connection
connection.commit()
connection.close() 


# Remove symbols not found in Yahoo Finance from the database (outside of the primary loop)
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()
cursor.execute("SELECT id, symbol FROM stock")
db_symbols = cursor.fetchall()

for db_symbol in db_symbols:
    symbol = db_symbol[1]  # Access the symbol by index (1) in the tuple
    if symbol not in symbols_in_yahoo_finance:
        cursor.execute("DELETE FROM stock WHERE id = ?", (db_symbol[0],))  # Access the id by index (0) in the tuple

# Commit chnages and close the database connection
connection.commit()
connection.close() 