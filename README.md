<h1 align="center">Full Stack Trading App</h1>

<br>

Welcome to my repository dedicated to explain the construction of a Trading app!

<br>

<h2 align="center">🌅 Journey Highlights 🌅</h2>
My initiation into the world of Deep Learning started with the enlightening 6.S191 MIT course by Alexander Amini. Building on this foundation, I expanded my knowledge by following the instructive courses curated by Josh Stamer. The hands-on experience in the practical application of Deep Learning with TensorFlow was facilitated by Aladdin Persson's tutorials, culminating in being certified TensorFlow Developer by Google.
I express my gratitude to these educators for providing excellent and free resources to the community.

<br>


The code is finished and the website function in local, nonetheless, the html code for the user interface is not. Even if building website is not a part of the data science fiel I want to finish it. I will publish the link to the website as soon as I finish it as of right now I do not judge the website's beauty and finition to ba at the same level as the the codes that makes it work. hence my motivation to not publish it yet. Thanks for your understanding. 


Before diving into the projects, you'll find a comprehensive list of the main libraries, APIs languages that have been used and a quick definition.

<details>
  <h2 align="center"> 📖 Libraries APIs & Languages 📖 </h2>
  
  <summary> 📖 Libraries APIs & Languages 📖</summary> 
<p>

  <h3>Languages</h3>

**Python:** Used to create the hole trading app, linking SQLite and HTML codes with the rest of it

**SQLite** To create, maintain and dynamicly maintain a 5GB data base with 5 different tables with one of +35 millions rows

11k stocks

**HTML:** Used to create the Trading app interface and functionalities.

  <h3>Python Libraries & APIs</h3>
  
**SQLite3** Library permitting to use SQLite within python

**Alpaca_trade_api** API in python that permits to use alpaca's functions to be able to trade real-time on the market for free

**yfinance (yahoo finance):** library that allow us to acces to financial data in real time for free

**ta-lib** 

**FastAPI (Jinja2Templates)**

**Backtrader**

</p>
  <br>
</details>

<br>

<h2 align="center">🔎 Repository Overview 🔍</h2>
<br>
This repository is a testament to .... the repository is divided in 5 parts:

<br>




^



To initialize the "app.db" database using SQLite3, begin by executing the command "sqlite3 app.db" in the terminal, creating the initial database file.

Afterwards, create a configuration file named "config.py" and input the necessary Alpaca API credentials (API_KEY, SECRET_KEY, BASE_URL), as well as the file location for your "app.db" (DB_FILE), and email configuration details (EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT).

Proceed to set up the required tables by executing the "create_db.py" script. This script encapsulates the code to create the five essential tables for the Full-Stack application. Running this command executes the Python script, establishing the foundational tables within the "app.db" database, laying the groundwork for the Full-Stack application.

Finally, utilize "populate_stocks.py" to populate the stock table with every stock available on Alpaca.

#######populate prices
This code is a Python script that connects to an SQLite database and updates stock price information, including technical indicators, by fetching data from Yahoo Finance. The primary steps are as follows:

Database Connection Setup:
Establish a connection to an SQLite database specified in the "config.py" file, and configure the database cursor.
Retrieve Stock Symbols from the Database:
Fetch stock symbols and related information from the 'stock' table in the SQLite database.
Define Date Range and Initialize Sets:
Define the end date for the data retrieval and create sets to keep track of processed symbols and those found in Yahoo Finance.
Iterate Through Symbols:
Loop through the stock symbols obtained from the database, replacing characters in the symbol name for compatibility with Yahoo Finance's API.
Check and Download Data from Yahoo Finance:
Check if the symbol has already been processed and, if not, attempt to download historical price data from Yahoo Finance using the yfinance library. The script handles cases where the 'max' period is not allowed by downloading data for a single day.
Handle Data and Update Database:
Process the downloaded data, calculate technical indicators such as Simple Moving Averages (SMA) and Relative Strength Index (RSI), and insert the data into the 'stock_price' table of the SQLite database.
Clean Up and Remove Symbols:
Close the database connection and remove symbols not found in Yahoo Finance from the 'stock' table in the SQLite database.
Reason for Using Yahoo Finance Over Alpaca API:

The code explains that the choice to retrieve data from Yahoo Finance instead of Alpaca API is due to changes in Alpaca's free data retrieval policy, making it no longer viable to obtain extensive data for free. This shift to Yahoo Finance simplifies the data retrieval process and aligns with the script's goal of updating stock price information.
Symbol Formatting Differences:

The script highlights the need to replace certain characters in the stock symbols for compatibility between Alpaca and Yahoo Finance. This substitution ensures that symbols, when used as part of URLs or filenames, conform to the requirements of the respective APIs. Specifically, slashes ('/') and periods ('.') in the symbols are replaced with hyphens ('-'). This step facilitates a seamless transition between the different symbol formats used by Alpaca and Yahoo Finance.
#######populate prices




#Opening range breakdown
Summary:

The goal of this script is to automate the identification and execution of trading strategies, specifically targeting opening range breakouts, for a set of stocks. It utilizes historical minute-level data obtained from Yahoo Finance and interacts with the Alpaca API to place buy orders when certain conditions are met.

Key Components and Steps:

Database Connection:
Connects to an SQLite database containing information about stocks, strategies, and related data.
Retrieve Strategy and Stock Information:
Retrieves the ID of the 'opening_range_breakout' strategy and gathers symbols associated with this strategy from the database.
Alpaca API Connection:
Establishes a connection to the Alpaca API using the provided credentials.
Define Time Range:
Defines the historical data range, typically the last 30 days, and sets the current date.
Check Existing Orders:
Fetches existing orders from Alpaca API after the current date to avoid redundant orders.
Loop Through Symbols:
Iterates through each stock symbol associated with the strategy.
Download Historical Data:
Downloads minute-level historical data from Yahoo Finance for each stock.
Calculate Opening Range:
Calculates the opening range (high - low) for the first 15 minutes of the market open.
Identify Breakout:
Identifies bars that close above the opening range high after the initial 15 minutes, signaling a potential breakout.
Place Alpaca Orders:
If a breakout is identified and there is no existing order for the symbol, a buy order is placed on Alpaca.
The order is set as a limit order with a take-profit order and a stop-loss order, creating a bracket order.
Print and Store Messages:
Prints and stores messages about the placed orders, providing information on the stock, limit price, and breakout details.
Summary Output:
Prints the final set of messages containing information about the executed orders.
Purpose and Significance:

The script automates the process of identifying opening range breakout opportunities, reducing manual effort and potential errors.
Historical data from Yahoo Finance is used due to the constraints on retrieving large datasets from the Alpaca API.
The Alpaca API is employed to execute trading orders based on the identified breakout conditions, facilitating an automated trading strategy.
Note:

The script incorporates modular functions from external files (helpers.py) for improved organization and readability.
The overall goal is to enhance the efficiency of executing a specific trading strategy by leveraging historical data analysis and algorithmic trading through the Alpaca platform.

#breakout
This code is used to submit a buy order with a trailing stop, ensuring that the stop price adjusts dynamically based on the stock's price movement. The bracket order setup further includes a limit price, which helps control the maximum price paid for the stock.

#Main
This FastAPI application, run through Uvicorn, is a web-based stock analysis and trading platform. It utilizes SQLite for local data storage, Alpaca API for real-time stock data, and FastAPI for building the web interface. The application offers functionalities such as filtering stocks based on various criteria (e.g., new closing highs/lows, RSI overbought/oversold, above/below SMA), viewing detailed stock information, applying trading strategies, and monitoring orders. The routes handle HTTP requests, connect to the SQLite database to execute queries, and render HTML templates using Jinja2. Overall, the objective is to provide a user-friendly platform for stock analysis, strategy application, and order monitoring.




#populate minute bars
This Python script performs the following operations:

Import Libraries:
Imports necessary libraries including configuration parameters, date handling, SQLite for database operations, Yahoo Finance API for stock data, Pandas for data manipulation, and CSV for reading a CSV file.
Get Date Range:
Retrieves the current date and sets a start date 29 days before that. This date range is used for fetching historical stock data.
Connect to SQLite Database:
Establishes a connection to the SQLite database using parameters from the configuration file.
Read Stock Symbols from CSV:
Reads stock symbols from a CSV file named 'minute_stocks.csv' and stores them in a list. Initializes an empty dictionary to store stock IDs.
Fetch Stock Information from Database:
Retrieves stock information, including Yahoo Finance symbols and IDs, from the database. Stores this information in a dictionary for easy access.
Fetch Historical Data for Each Stock:
For each stock symbol, fetches minute bars for a specified date range, resamples the data to 1-minute intervals, and inserts it into the 'stock_price_minute' table in the database.
Commit and Close Database Connection:
Commits the changes to the database and closes the connection.
In summary, this script automates the process of fetching minute-level historical stock price data from Yahoo Finance for a list of stocks, resampling the data, and storing it in an SQLite database.









HTML
