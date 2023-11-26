# Importing Libraries
import sqlite3
from config import *

# Establish Database Connection
connection = sqlite3.connect(DB_FILE)

# Create a Cursor
cursor = connection.cursor()

# Create 'stock' Table
cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock(
               id INTEGER PRIMARY KEY, 
               symbol TEXT NOT NULL UNIQUE,
               yf_symbol TEXT UNIQUE ,
               name TEXT NOT NULL,
               exchange TEXT NOT NULL,
               shortable BOOLEAN NOT NULL,
               last_download_date DATE
            )
        """)

# Create 'stock_price' Table
cursor.execute("""
            CREATE TABLE stock_price (
               id INTEGER,
               stock_id INTEGER,
               date NOT NULL,
               open NOT NULL,
               high NOT NULL,
               low NOT NULL,
               close NOT NULL,
               volume NOT NULL,
               sma_20,
               sma_50,
               rsi_14,
               FOREIGN KEY (stock_id) REFERENCES stock (id)
            )
        """)

# Create 'stock_price_minute' Table
cursor.execute("""
            CREATE TABLE stock_price_minute (
               id INTEGER PRIMARY KEY,
               stock_id INTEGER,
               datetime NOT NULL,
               open NOT NULL,
               high NOT NULL,
               low NOT NULL,
               close NOT NULL,
               volume NOT NULL,
               FOREIGN KEY (stock_id) REFERENCES stock (id)
            )
        """)

# Create 'strategy' Table
cursor.execute("""
               CREATE TABLE IF NOT EXISTS strategy (
               id INTEGER PRIMARY KEY,
               name NOT NULL
               )
                """)

# Create 'stock_strategy' Table
cursor.execute("""
               CREATE TABLE IF NOT EXISTS stock_strategy (
               stock_id INTEGER NOT NULL,
               strategy_id INTEGER NOT NULL,
               FOREIGN KEY (stock_id) REFERENCES stock (id)
               FOREIGN KEY (strategy_id) REFERENCES strategy (id)
               )
               """)

# Define Strategies and Insert into 'strategy' Table
strategies = ['opening_range_breakout', 'opening_range_breakdown']

for strategy in strategies:
    cursor.execute("""
        INSERT INTO strategy (name) VALUES (?)
    """, (strategy,))

# Commit Changes to the Database
connection.commit()