# Import Libraries
import sqlite3
from config import *

# Database Connection
connection = sqlite3.connect(DB_FILE)

# Cursor Initialization
cursor = connection.cursor()

# Dropping Tables
cursor.execute("""
               DROP TABLE stock
               """)

cursor.execute("""
               DROP TABLE stock_price
               """)

cursor.execute("""
               DROP TABLE stock_price_minute
               """)

cursor.execute("""
               DROP TABLE stock_strategy
               """)
cursor.execute("""
               DROP TABLE strategy
               """)

# Committing Changes
connection.commit()