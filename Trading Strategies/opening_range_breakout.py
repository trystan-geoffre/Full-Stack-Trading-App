# Import Libraries
import sqlite3
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import *
from helpers import *
from datetime import datetime

# Database Connection Setup
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Retrieve Strategy ID
cursor.execute("""
               SELECT id FROM strategy WHERE name = 'opening_range_breakout'
               """)

strategy_id = cursor.fetchone()['id']

# Retrieve Stocks Associated with the Strategy
cursor.execute("""
               SELECT symbol, name
               FROM stock
               JOIN stock_strategy ON stock_strategy.stock_id = stock.id
               WHERE stock_strategy.strategy_id = ?
               """, (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

# Alpaca API Connection
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)


messages = []

# Define the number of days for the historical data range
historical_data_days = 30

#Define Time Range
current_date =  datetime.now()
current_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")
start_date = current_date - pd.DateOffset(days=historical_data_days)
start_date = start_date.strftime("%Y-%m-%d")  # Format the date as a string

# Set the time of the US market open (New York, EDT)
us_market_open_time = pd.Timestamp(f"{current_date} 09:30:00")

# Apply the time zone offset to get the start time in Belgrade's time zone
start_minute_bar_belgrade = us_market_open_time + pd.Timedelta(hours=6)

# Set the duration (15 minutes) and calculate the end time accordingly
duration = pd.Timedelta(minutes=15)
end_minute_bar_belgrade = start_minute_bar_belgrade + duration


# Check existing orders
orders = api.list_orders(status='all', after=current_date)  # Updated 'after' parameter
existing_order_symbols = [order.symbol for order in orders]

# Loop Through Symbols
for symbol in symbols:
    # Download minute-level historical data from Yahoo Finance
    minute_bars = yf.download(symbol, start=start_date, end=current_date, interval="15m")

    if minute_bars.empty:
        print(f"No data found for symbol {symbol}")
    else:
        minute_bars.index = minute_bars.index.tz_localize(None)
        start_minute_bar = start_minute_bar_belgrade.tz_localize(None)
        end_minute_bar = end_minute_bar_belgrade.tz_localize(None)
        
        print(minute_bars.index)
        print(start_minute_bar)
        print(end_minute_bar)
        
        # Calculate Opening Range
        opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
        opening_range_bars = minute_bars.loc[opening_range_mask]
        opening_range_low = opening_range_bars['Low'].min()
        opening_range_high = opening_range_bars['High'].max()
        opening_range = opening_range_high - opening_range_low

        print(opening_range_low)
        print(opening_range_high)
        print(opening_range)

        # Check for Breakout
        after_opening_range_mask = minute_bars.index >= end_minute_bar
        after_opening_range_bars = minute_bars.loc[after_opening_range_mask]

        after_opening_range_breakout = after_opening_range_bars[after_opening_range_bars['Close'] > opening_range_high]

        if not after_opening_range_breakout.empty:
            if symbol not in existing_order_symbols:
                limit_price = after_opening_range_breakout.iloc[0]['Close']

                # Print and Store Messages
                messages.append(
                    f'placing order for {symbol} at {limit_price}, closed above {opening_range_high} \n\n {after_opening_range_breakout.iloc[0]}\n\n ')
                print(
                    f'placing order for {symbol} at {limit_price}, closed above {opening_range_high} at {after_opening_range_breakout.iloc[0]} ')

                # Place Alpaca Orders
                api.submit_order(
                    symbol=symbol,
                    side='buy',
                    type='trailing_stop', # Type of order: Trailing Stop
                    trail_percent=1.5, # Trail the price by 1.5%
                    qty=calculate_quantity(limit_price), # Quantity of shares to buy
                    time_in_force='day', # Order is valid for the trading day
                    order_class='bracket', # Use bracket order
                    limit_price=limit_price, # Set the limit price for the order
                )
                    
            else:
                print(f'Already an order for {symbol}, skipping')

print(messages)

