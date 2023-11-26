import alpaca_trade_api as tradeapi
import yfinance as yf
import talib

from config import *
from helpers import *

def connect(api_key, api_secret, base_url):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    try:
        account = api.get_account()
        print("Connected: Connected to Alpaca API")
        return api
    except Exception as e:
        print(f"Failed to connect to Alpaca API. Error: {str(e)}")
        return None

def place_market_order(api, symbol, qty, side):
    try:
        quote = api.get_last_quote(symbol)
        order = api.submit_order(
            symbol=symbol,
            qty=calculate_quantity(quote.bidprice),
            side=side,
            type='market',
            time_in_force='day',
        )
        return order
    except Exception as e:
        print(f"Error placing market order: {str(e)}")
        return None

def place_trailing_stop_order(api, symbol, qty, trail_percent, side):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='trailing_stop',
            trail_percent=trail_percent,
            time_in_force='gtc',
        )
        return order
    except Exception as e:
        print(f"Error placing trailing stop order: {str(e)}")
        return None

if __name__ == "__main__":
    api_key = API_KEY
    api_secret = SECRET_KEY
    base_url = BASE_URL
    api = connect(api_key, api_secret, base_url)

    if api:
        # Replace these values with your specific order details
        symbol = 'AAPL'  # Replace with the desired stock symbol
        qty = 10  # Replace with the desired quantity of shares
        trail_percent = 1.5  # Replace with the desired trailing stop percentage
        side = 'buy'  # Replace with 'buy' or 'sell'

        # Place a market order
        market_order = place_market_order(api, symbol, qty, side)

        # Place a trailing stop order if the market order is successfully placed
        if market_order:
            place_trailing_stop_order(api, symbol, qty, trail_percent, side)
