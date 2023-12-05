# Importing Libraries
import sqlite3
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import talib


from config import *
from helpers import *
from datetime import datetime, timedelta

# Database Connection
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Querying Strategy and Stocks
cursor.execute("""
               SELECT id FROM strategy WHERE name = 'bollinger_bands'
               """)

strategy_id = cursor.fetchone()['id']

cursor.execute("""
               SELECT symbol, name
               FROM stock
               JOIN stock_strategy ON stock_strategy.stock_id = stock.id
               WHERE stock_strategy.strategy_id = ?
               """, (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

# Alpaca API Connection
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Setting Historical Data Range
historical_data_days = 30
current_date =  datetime.now()
current_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")
start_date = current_date - pd.DateOffset(days=historical_data_days)
start_date = start_date.strftime("%Y-%m-%d")  # Format the date as a string

us_market_open_time = pd.Timestamp(f"{current_date} 09:30:00")

# Apply the time zone offset to get the start time in Belgrade's time zone
start_minute_bar_belgrade = us_market_open_time + pd.Timedelta(hours=6)

# Set the duration (15 minutes) and calculate the end time accordingly
duration = pd.Timedelta(minutes=15)
end_minute_bar_belgrade = start_minute_bar_belgrade + duration

messages=[]

# Check existing orders
orders = api.list_orders(status='all', after=current_date)  # Updated 'after' parameter
existing_order_symbols = [order.symbol for order in orders]

# Iterating Through Symbols
for symbol in symbols:
    # Download historical data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=current_date, interval='1m')

    # Calculate Bollinger Bands with a 20-minute time period
    data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Close'], timeperiod=20)

    current_candle = data.iloc[-1]
    previous_candle = data.iloc[-2]

    # Trading Logic
    if current_candle.close > data['lower_band'] and previous_candle.close < data['lower_band']:
            if symbol not in existing_order_symbols:
                limit_price = current_candle.close

                candle_range = current_candle.high - current_candle.low
                
                # Placing Long Order
                messages.append(f'Placing long order for {symbol} at {limit_price}')

                api.submit_order(
                    symbol=symbol,
                    side='buy',  # Change 'sell' to 'buy' for a long position
                    type='limit',
                    qty=calculate_quantity(limit_price),
                    time_in_force='day',
                    order_class='bracket',
                    limit_price=limit_price,
                    take_profit=dict(
                        limit_price=limit_price + (candle_range*3),  # Adjust for long position
                    ),
                    stop_loss=dict(
                        stop_price=previous_candle.high  # Adjust for long position
                    )
                )

            else:
                print(f'Already an order for {symbol}, skipping')
    # Printing Messages
    print(messages)