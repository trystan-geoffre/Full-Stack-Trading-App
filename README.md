<h1 align="center">Full Stack Trading Platform</h1>

<br>

Welcome to my repository dedicated to explain the construction of a Trading Plartform!

<br>

<h2 align="center">🌅 Journey Highlights 🌅</h2>
<p>
Building the trading was a logical choice for me. I knew that I needed to be challenged on building and maintening a dynamic database. Having previously developed a Trading AI with TensorFlow <a href="https://github.com/trystan-geoffre/Trading-AI-TensorFlow/tree/master">(Project Link)</a>, the next step was to create an entire trading environment based on a custom database. As of now, the database consists of five different tables, one of which has over 35 million rows.
  I would like to express my gratitude to Part-Time Larry for providing essential concepts and foundations that facilitated the construction of this platform.

<h1></h1>

<h3>💫 Quick platform review 💫 </h3>

The platform boasts 6 distinct trading strategies (3 for buying and 3 for shorting), all applicable to over 11,000 different stocks, cryptocurrencies, and other assets. The list of tickers is updated daily, automated data download providing real-time updates on the website. Additionally, the website offers a TradingView chart.

*The code is complete, and the website functions locally. However, I acknowledge that the HTML code for the user interface does not meet the standards of a well-finished website. Despite website development not being my primary focus, I am committed to delivering quality work. I will share the link to the website as soon as I finish the necessary improvements. Thank you for your understanding*

<br>

<h3>📈 Trading Strategies Efficiency 📉</h3>
The trading strategies underwent two testing phases on paper trading (no real money). Initially, a 24-day evaluation (October 3rd to 27th) focused solely on the opening range strategies, resulting in a loss of 1.5%. 

Following iterative adjustments and the incorporation of new trading strategies, a subsequent 20-day test spanning from October 27th to November 16th yielded a notable **7.6% profit over 20days**. 

However, it's crucial to note that these strategies are yet to undergo evaluation over an extended period to comprehensively assess their long-term efficiency and robustness.

---

<h2 align="center">🔎 Repository Overview 🔍</h2>

<br>

Before diving into the projects, you'll find a comprehensive list of the main libraries, APIs and languages that have been used and a quick definition.
</p>

<details>
  <h2 align="center"> 📖 Libraries APIs & Languages 📖 </h2>
  
  <summary> 📖 Libraries APIs & Languages 📖</summary> 
<p>

  <h3>Languages</h3>

<h4> Python: </h4>
Language used to structure the platform functionalities.

<h4> SQLite: </h4>
To create, maintain a 5GB database with 5 different tables and +35 millions rows.

<h4> HTML: </h4>
Used to create the Trading platform interface and website functionalities.

<h1></h1>
  
<h3>Python Libraries & APIs</h3>
  
<h4> SQLite3: </h4>
Python library that enables the use of SQLite within PythonLibrary permitting to use SQLite within python

<h4> Alpaca_trade_api: </h4>
Python API that allows the utilization of Alpaca's functions, enabling real-time market trading for free, with a focus on algorithmic trading strategies.

<h4> Ta-lib: </h4>
A technical analysis library in Python, providing tools and functions for analyzing financial markets and making informed trading decisions based on technical indicators.

<h4> Backtrader: </h4>
Python framework for developing and testing trading strategies, offering extensive functionality for backtesting and optimizing strategies before deploying them in live markets.

<h4> FastAPI (Jinja2Templates): </h4>
FastAPI is a modern, fast web framework for building APIs with Python, and Jinja2Templates is a template engine used for creating dynamic HTML templates in conjunction with FastAPI.

<h4> Uvicorn: </h4>Serves as a lightweight and efficient way to run asynchronous web applications written in Python. It provides a fast and scalable solution for deploying and managing web servers


<h4> Semantic-UI: </h4>
A user interface framework that utilizes HTML to create a responsive and visually appealing design for the trading platform.

<h4> Crontab: </h4>
A time-based job scheduler, used in this context to schedule and automate periodic tasks within the trading platform.

<h4> Yfinance (yahoo finance): </h4>
Python library that grants access to real-time financial data from Yahoo Finance, facilitating the retrieval of market information for various assets at no cost.

<h4> Trading View: </h4>
A platform that provides advanced charting tools and analysis for financial markets, often integrated into trading applications to offer users a comprehensive view of market data and trends.

</p>
  <br>
</details>

<h1></h1>

<details>
  <h2 align="center">🌐 DataBase 🌐</h2>
  
  <summary> 🌐 DataBase 🌐 </summary> 

  <p>
<h4>Setting Up the Database:</h4>
To initiate the database creation process, first, generate the database named "app.db" using SQLite3. Execute the command "sqlite3 app.db" in the terminal to establish the initial database file. This step lays the foundation for subsequent configurations.


<h4>Configuring Alpaca API, SQLite and Email:</h4>
Following the database creation, proceed to set up a configuration file named "config.py." Enter essential Alpaca API credentials (API_KEY, SECRET_KEY, BASE_URL), define the file location for "app.db" (DB_FILE), and provide email configuration details (EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT).

 
<h4>Database Initialization and Table Management:</h4>
Utilize the scripts in this repository to manage the database. Begin with the "create_db" script  <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/create_db.py"> Code Link</a> to establish the five necessary tables. You also have drop_db <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/drop_db.py"> Code Link</a> to drop all tables in app.db.


<h4>Populating Stock Information:</h4>
Execute the "populate_stocks.py" script <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/populate_stocks.py"> Code Link</a> to populate the "stock" table with information for every stock, cryptocurrency, and asset available on Alpaca. The data includes the symbol/ticker, name, exchange, and a flag indicating whether shorting is permissible. Ensure that the data is successfully loaded using DB Browser for SQLite (or other), resulting in over 13,000 rows. To automatically add new stocks if there is any, create a <a href="https://crontab.guru">Crontab</a> code to run the script. I personally run it daily, after market closure.


<h4>Fetching Historical Stock Prices:</h4>
The "populate_prices" script <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/populate_prices.py"> Code Link</a>. downloads data for all tickers in the "stock" table in the "stock_price" table, a process that may take some time due to the substantial volume of data.  Since some Alpaca functionalities are restricted or no longer free, Yahoo Finance is used as an alternative for obtaining free, extensive historical data.The script also addresses variations in ticker names, ensuring a match with Yahoo Finance or dropping unmatched tickers in "stock". After completion, the "stock" table is populated with over 11,000 tickers, the "stock_price" table featuring daily open, close, high, low, volume, and date information. Additionally, in "stock_price" the script calculates the Simple Moving Average (SMA) for 20 and 50 days and the Relative Strength Index (RSI) for 14 days using the Ta-lib analysis library.

  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center"> ♟️ Trading Strategies ♟️ </h2>
  
  <summary>♟️Trading Strategies♟️</summary> 

  <p>
The helpers.py code sets the amount to invest in each trade. You are encouraged to modify this amount according to your preferences or requirements. <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/helpers.py"> Code Link</a> 

<h4>Opening Range Breakdown:</h4>
This Python script is designed to automate the execution of a trading strategy, specifically the "opening range breakdown" strategy, using Alpaca API for real-time trading. The script connects to an SQLite database to retrieve stocks associated with the chosen strategy, then checks if the stock has already an order filled. For each stock, it downloads 15-minute interval historical data from Yahoo Finance, calculates the opening range, and determines if a breakdown has occurred after the opening range. If a breakout is detected and there is no existing filled order for the stock, a short order is placed on Alpaca with specified limit, take-profit, and stop-loss prices. The script logs messages for each action and is configured to run for a defined historical data range. <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/opening_range_breakdown.py"> Code Link</a>

<h4>Opening Range Breakout:</h4>
The Opening Range Breakout code is similar to the Opening Range Breakdown, with the key difference being the calculation of a breakout. Also, in this context, the code is designed to execute a buy order with a trailing stop instead of a traditional stop-loss and take-profit approach. The trailing stop dynamically adjusts the stop price based on the stock's price movement, enhancing adaptability to market fluctuations. Additionally, the bracket order setup incorporates a limit price, offering control over the maximum price paid for the stock during the buy order execution <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/opening_range_breakout.py"> Code Link</a>

<h4>Bollinger Bands Short:</h4>
This Python code is a trading script that utilizes the Alpaca API and Yahoo Finance to implement a Bollinger Bands strategy for a list of stocks. The script connects to a SQLite database, queries for stocks associated with the "bollinger_bands" strategy, and checks for existing orders. It then downloads historical price data, calculates Bollinger Bands, and executes a short order when specific trading conditions are met, incorporating limit prices, take-profit, and stop-loss parameters. The script is designed to automate trading decisions based on the Bollinger Bands indicator, providing a systematic approach to managing short positions in the stock market.<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/bollinger_bands_short.py "> Code Link</a>

<h4>Bollinger Bands Long:</h4>
This Bollinger Bands Long code mirrors the Bollinger Bands Short, with the only difference being in the calculation of upward movement and the execution of a buy order instead of a short order.<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/bollinger_bands_long.py"> Code Link</a>

To automatically execute the Bollinger Bands and Opening Range Breakout/Down strategies, I utilize Crontab. These scripts are scheduled to run every minute exclusively during the trading hours on trading days. This ensures that the strategies are consistently applied within the active market periods.

<h4>Daily Close:</h4>
This script is designed to automatically close all stock positions at the conclusion of the trading day. To automate its execution, you can implement a Crontab code. I typically schedule it to run 30 minutes before the market closes. The script begins by retrieving and canceling any active sell orders. Subsequently, it proceeds to close out all existing stock positions.
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/daily_close.py"> Code Link</a>
  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center"> 🏹 Main code 🏹</h2>
  
  <summary> 🏹 Main code 🏹 </summary> 

  <p>
This Python code defines a FastAPI application that run through Uvicorn and serves as a web interface for stock trading strategies. It establishes routes for displaying a list of stocks with various filtering options based on financial indicators such as closing highs, closing lows, RSI overbought/sold, and SMA crossovers. The application also provides detailed views for individual stocks, strategies, and a summary of active orders. Users can apply strategies to specific stocks, view existing strategies, and monitor their trading orders through the web interface. The code utilizes SQLite for database management and Alpaca API for retrieving real-time financial data and managing trading orders. 

To launch the website locally, execute the command "uvicorn main:app --reload" in your terminal. You can access the website through the link provided in the following line of the console output: "INFO: Uvicorn running on http://****** (Press CTRL+C to quit)." <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/main.py"> Code Link</a>

  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center">🔰 Templates HTML (work in progress) 🔰</h2>
  
  <summary> 🔰 Templates HTML 🔰</summary> 

  <p>
<h4>Layout:</h4>
This HTML code defines a basic web page structure for a stocks-related application. It includes a navigation menu with links to the "Stocks," "Strategies," and "Order History" sections, and a "Logout" option on the right side. The content of the page is expected to be filled dynamically, allowing for flexible rendering based on specific sections or views. The page is styled using the Semantic UI library.<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/layout.html"> Code Link</a>

<h4>Index:</h4>
This HTML template, extending a base layout, is designed for rendering a dynamic stock list page. It includes a form with a dropdown menu allowing users to filter stocks based on various criteria such as new closing highs/lows, RSI (Relative Strength Index) overbought/oversold, and positions relative to SMA (Simple Moving Average) values. The template displays a table with stock details, including symbol, name, price, RSI 14, SMA 20, and SMA 50, dynamically populated with data fetched from the server. The table entries link to individual stock detail pages. <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/index.html"> Code Link</a>

<h4>Stock detail:</h4>
This HTML template, extending a base layout, is designed for rendering individual stock detail pages. It includes a heading displaying the stock's name and symbol, a TradingView widget for visualizing stock data, a form allowing users to apply trading strategies to the stock, and a table displaying historical price information. The TradingView widget dynamically fetches and displays real-time stock data, and the form enables users to apply various strategies to the selected stock. The historical price table presents key data such as open, high, low, close, and volume for each date. 
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/stock_detail.html"> Code Link</a>

<h4>Strategies:</h4>
This HTML template, extending a base layout, is designed for rendering a page that displays a list of available trading strategies. It includes a heading "Strategies" and a table with each row representing a strategy. Each strategy is a clickable link leading to a detailed view of that specific strategy.
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/strategies.html"> Code Link</a>

<h4>Strategy:</h4>
This HTML template, extending a base layout, is designed for rendering a page that displays a list of stocks associated with a specific trading strategy. It includes a heading that navigates back to the main stocks page, indicating the selected strategy's name. The table below lists each stock's symbol and name.
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/strategy.html"> Code Link</a>

<h4>Orders:</h4>
This HTML template, extending a base layout, is designed for rendering a page that displays a list of trading orders. It includes a heading "Orders" and a table with each row representing an order. The table provides details such as the order creation timestamp, side (buy/sell), quantity, symbol, filled price, and order status. 
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/templates%20html/orders.html"> Code Link</a>
  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center">🎯 Backtesting 🎯</h2>
  
  <summary> 🎯 Backtesting 🎯</summary> 

  <p>
You can find the Stocks' tickers I have used for the Backtesting in minute_stocks.csv  <a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/minute_stocks.csv"> Code Link</a>

<h4>Populate Minute Data:</h4>
This Python script imports necessary libraries and connects to an SQLite database. It reads stock symbols from a CSV file, retrieves historical minute-level price data using Yahoo Finance API for each stock, and inserts the data into the database. The script iterates through a specified date range, resamples the data to 1-minute intervals, and handles missing values.<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/populate_minute_data.py"> Code Link</a>

<h4>Backtesting:</h4>
  The provided Python code leverages the Backtrader library for backtesting the trading strategy Opening Range Breakout. The script iterates over distinct stocks, initializes the backtesting engine, fetches minute-level price data from a SQLite database, and executes the backtest using the defined strategy. The results are printed, and a plot is generated for visual analysis. This approach allows for evaluating the strategy's performance across different stocks, providing insights into its effectiveness in various market conditions.
<a href="https://github.com/trystan-geoffre/Full-Stack-Trading-App/blob/master2/backtest.py"> Code Link</a>
  </p>
  <br>
</details>

<br>

This marks the conclusion of the repository on a Full Stack Trading App. For those interested in exploring another complex project within the realm of Trading, I would invite you to visit the repository <a href="https://github.com/trystan-geoffre/Trading-AI-TensorFlow/tree/master"> Trading AI using TensorFlow</a> to witness the application of Deep Learning in stock prediction.
