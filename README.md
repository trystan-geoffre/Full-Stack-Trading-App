<h1 align="center">Full Stack Trading Platform</h1>

<br>

Welcome to my repository dedicated to explain the construction of a Trading Plartform!

<br>

<h2 align="center">🌅 Journey Highlights 🌅</h2>
<p>
Building the trading was a logique choice for me. I knew that I needed challenged on building, maintening   a dynamic database. Having previously developed a trading AI with TensorFlow (link to the project), the logical next step was to create an entire trading environment based on a custom database. As of now, the database consisting of five different tables, one of which has over 35 million rows.

<h1></h1>

<h3>💫 Quick platform review 💫 </h3>

The platform boasts 6 distinct trading strategies (3 for buying and 3 for shorting) applicable to over 11,000 different stocks, cryptocurrencies, and other assets. The list of tickers is updated daily, automated data download providing real-time updates on the website. Additionally, the website offers a TradingView chart.

*The code is complete, and the website functions locally. However, I acknowledge that the HTML code for the user interface does not meet the standards of a well-finished website. Despite website development not being my primary focus, I am committed to delivering quality work. I will share the link to the website as soon as I complete the necessary improvements. Thank you for your understanding*

<br>

<h3>📈 Trading Strategies Efficiency 📉</h3>
The trading strategies underwent two testing phases on paper trading (no real money). Initially, a 24-day evaluation (October 3rd to 27th) focused solely on the opening range strategies, resulting in a nominal loss of 1.5%. 

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

**Python:** Language used to structure the platform functionalities.

**SQLite:** To create, maintain a 5GB database with 5 different tables and +35 millions rows.

**HTML:** Used to create the Trading platform interface and website functionalities.

  <h3>Python Libraries & APIs</h3>
  
**SQLite3:** Python library that enables the use of SQLite within PythonLibrary permitting to use SQLite within python

**Alpaca_trade_api:** Python API that allows the utilization of Alpaca's functions, enabling real-time market trading for free, with a focus on algorithmic trading strategies.

**ta-lib:** A technical analysis library in Python, providing tools and functions for analyzing financial markets and making informed trading decisions based on technical indicators.

**Backtrader:** Python framework for developing and testing trading strategies, offering extensive functionality for backtesting and optimizing strategies before deploying them in live markets.

**FastAPI (Jinja2Templates):** FastAPI is a modern, fast web framework for building APIs with Python, and Jinja2Templates is a template engine used for creating dynamic HTML templates in conjunction with FastAPI.

**Uvicorn:** Serves as a lightweight and efficient way to run asynchronous web applications written in Python. It provides a fast and scalable solution for deploying and managing web servers

**Semantic-UI:** A user interface framework that utilizes HTML to create a responsive and visually appealing design for the trading platform.

**Crontab:** A time-based job scheduler, used in this context to schedule and automate periodic tasks within the trading platform.

**yfinance (yahoo finance):** Python library that grants access to real-time financial data from Yahoo Finance, facilitating the retrieval of market information for various assets at no cost.

**trading View:** A platform that provides advanced charting tools and analysis for financial markets, often integrated into trading applications to offer users a comprehensive view of market data and trends.

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
Utilize the scripts in this repository to manage the database. Begin with the "create_db" script  <a href=""> Code Link</a> to establish the five necessary tables. You also have drop_db <a href=""> Code Link</a> to drop all tables in app.db.


<h4>Populating Stock Information:</h4>
Execute the "populate_stocks.py" script <a href=""> Code Link</a> to populate the "stock" table with information for every stock, cryptocurrency, and asset available on Alpaca. The data includes the symbol/ticker, name, exchange, and a flag indicating whether shorting is permissible. Ensure that the data is successfully loaded using DB Browser for SQLite (or other), resulting in over 13,000 rows. To automatically add new stocks if there is any, create a Crontab code to run the script. I personally run it daily, after market closure.


<h4>Fetching Historical Stock Prices:</h4>
The "populate_prices" script <a href=""> Code Link</a>. downloads data for all tickers in the "stock" table in the "stock_price" table, a process that may take some time due to the substantial volume of data.  Since some Alpaca functionalities are restricted or no longer free, Yahoo Finance is used as an alternative for obtaining free, extensive historical data.The script also addresses variations in ticker names, ensuring a match with Yahoo Finance or dropping unmatched tickers in "stock". After completion, the "stock" table is populated with over 11,000 tickers, the "stock_price" table featuring daily open, close, high, low, volume, and date information. Additionally, in "stock_price" the script calculates the Simple Moving Average (SMA) for 20 and 50 days and the Relative Strength Index (RSI) for 14 days using the Ta-lib analysis library.

  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center"> ♟️ Trading Strategies ♟️ </h2>
  
  <summary>♟️Trading Strategies♟️</summary> 

  <p>

<h4>Opening Range Breakdown:</h4>
This Python script is designed to automate the execution of a trading strategy, specifically the "opening range breakdown" strategy, using Alpaca API for real-time trading. The script connects to an SQLite database to retrieve stocks associated with the chosen strategy, then checks if the stock has already an order filled. For each stock, it downloads 15-minute interval historical data from Yahoo Finance, calculates the opening range, and determines if a breakdown has occurred after the opening range. If a breakout is detected and there is no existing filled order for the stock, a short order is placed on Alpaca with specified limit, take-profit, and stop-loss prices. The script logs messages for each action and is configured to run for a defined historical data range. <a href=""> Code Link</a>

<h4>Opening Range Breakout:</h4>
The Opening Range Breakout code is similar to the Opening Range Breakdown, with the key difference being the calculation of a breakout. Also, in this context, the code is designed to execute a buy order with a trailing stop instead of a traditional stop-loss and take-profit approach. The trailing stop dynamically adjusts the stop price based on the stock's price movement, enhancing adaptability to market fluctuations. Additionally, the bracket order setup incorporates a limit price, offering control over the maximum price paid for the stock during the buy order execution <a href=""> Code Link</a>

<h4>Bollinger Bands Short:</h4>
This Python code is a trading script that utilizes the Alpaca API and Yahoo Finance to implement a Bollinger Bands strategy for a list of stocks. The script connects to a SQLite database, queries for stocks associated with the "bollinger_bands" strategy, and checks for existing orders. It then downloads historical price data, calculates Bollinger Bands, and executes a short order when specific trading conditions are met, incorporating limit prices, take-profit, and stop-loss parameters. The script is designed to automate trading decisions based on the Bollinger Bands indicator, providing a systematic approach to managing short positions in the stock market.

<h4>Bollinger Bands Long:</h4>
This Bollinger Bands Long code mirrors the Bollinger Bands Short, with the only difference being in the calculation of upward movement and the execution of a buy order instead of a short order.<a href=""> Code Link</a>

  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center"> 🏹 Main code 🏹</h2>
  
  <summary> 🏹 Main code 🏹 </summary> 

  <p>
This FastAPI application, run through Uvicorn, is a web-based stock analysis and trading platform. It utilizes SQLite for local data storage, Alpaca API for real-time stock data, and FastAPI for building the web interface. The application offers functionalities such as filtering stocks based on various criteria (e.g., new closing highs/lows, RSI overbought/oversold, above/below SMA), viewing detailed stock information, applying trading strategies, and monitoring orders. The routes handle HTTP requests, connect to the SQLite database to execute queries, and render HTML templates using Jinja2. Overall, the objective is to provide a user-friendly platform for stock analysis, strategy application, and order monitoring.

<a href=""> Code Link</a>
  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center">🔰 Templates HTML 🔰</h2>
  
  <summary> 🔰 Templates HTML 🔰</summary> 

  <p>


<a href=""> Code Link</a>
  </p>
  <br>
</details>

<br>

<details>
  <h2 align="center">🎯 Backtesting 🎯</h2>
  
  <summary> 🎯 Backtesting 🎯</summary> 

  <p>


<a href=""> Code Link</a>
  </p>
  <br>
</details>

<br>
