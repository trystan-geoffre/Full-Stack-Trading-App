import alpaca_trade_api as tradeapi
from config import *

def connect(api_key, api_secret, base_url):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    try:
        account = api.get_account()
        print("Connected: Connected to Alpaca API")
        return api
    except Exception as e:
        print(f"Failed to connect to Alpaca API. Error: {str(e)}")
        return None

def close_outstanding_sell_orders(api):
    # Fetch all open orders
    open_orders = api.list_orders(status='open')

    # Filter open sell orders
    sell_orders = [order for order in open_orders if order.side == 'sell']

    # Close each outstanding sell order
    for order in sell_orders:
        try:
            api.cancel_order(order.id)
            print(f"Canceled sell order {order.id} for {order.symbol}")
        except Exception as e:
            print(f"Error canceling sell order {order.id}: {str(e)}")

def close_all_positions(api):
    # Fetch current positions
    positions = api.list_positions()

    # Close all positions
    for position in positions:
        symbol = position.symbol
        qty_to_close = int(position.qty)

        if qty_to_close > 0:
            try:
                response = api.close_position(symbol, qty=qty_to_close)
                print(f"Closed position for {symbol}: {response}")
            except Exception as e:
                print(f"Error closing position {symbol}: {str(e)}")

if __name__ == "__main__":
    api_key = API_KEY
    api_secret = SECRET_KEY
    base_url = BASE_URL
    api = connect(api_key, api_secret, base_url)

    if api:
        # Close outstanding sell orders
        close_outstanding_sell_orders(api)

        # Close all positions
        close_all_positions(api)
