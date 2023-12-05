# Importing Libraries
import sqlite3
import alpaca_trade_api as tradeapi
from config import *

# Establish Database Connection
connection = sqlite3.connect(DB_FILE)
connection.row_factory=sqlite3.Row

# Create a Cursor
cursor = connection.cursor()

# Step 1: Retrieve Existing Symbols from the 'stock' Table
cursor.execute("""
               SELECT symbol, name FROM stock
               """)

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

# Step 2: Connect to the Alpaca API
def connect(api_key, api_secret, base_url):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    try:
        account = api.get_account()
        print("Connected: Connected to Alpaca API")
        return api
    except Exception as e:
        print(f"Failed to connect to Alpaca API. Error: {str(e)}")
        return None

api_key = API_KEY
api_secret = SECRET_KEY
base_url = BASE_URL
api = connect(api_key, api_secret, base_url)

# Step 3: Check if a Stock is Shortable and Update Database
def is_stock_shortable(api, symbol):
    asset = api.get_asset(symbol)
    return asset.easy_to_borrow

# Step 4: Retrieve All Assets from Alpaca
assets = api.list_assets()

# Step 5: Loop Through Alpaca Assets and Update Database
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            # Print and Insert New Stock
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?,?,?)",(asset.symbol, asset.name, asset.exchange))

            # Check if Stock is Shortable and Update Database
            shortable = 1 if is_stock_shortable(api, asset.symbol) else 0
            cursor.execute("UPDATE stock SET shortable = ? WHERE symbol = ?", (shortable, asset.symbol))

    except Exception as e:
        # Print Symbol and Error in Case of Exception
        print(asset.symbol)
        print(e)
connection.commit()