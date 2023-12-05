# Importing Libraries
import backtrader, sqlite3, pandas
from datetime import date, datetime, time, timedelta
from config import *

# Strategy Definition
class OpeningRangeBreakout(backtrader.Strategy):
    pass
    params = dict(
        num_opening_bars=15
    )

    def __init__(self):
        # Step 2: Initializing Strategy
        self.opening_range_low = 0
        self.opening_range_high = 0
        self.opening_range = 0
        self.bought_today = False
        self.order = None

    def log(self, txt, dt=None):
        if dt is None:
            dt = self.datas[0].datetime.datetime()
        
        print('%s, %s' % (dt, txt))

    # Order Notification
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            order_details = f"{order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}"

            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order_details}")
            else:
                self.log(f"SELL EXECUTED, Price: {order_details}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    # Next Bar Calculation
    def next(self):
        current_bar_datetime = self.data.num2date(self.data.datetime[0])
        previous_bar_datetime = self.data.num2date(self.data.datetime[-1])

        if current_bar_datetime.date() != previous_bar_datetime.date():
            self.opening_range_low = self.data.low[0]
            self.opening_range_high = self.data.high[0]
            self.bought_today = False

        opening_range_start_time = time(9, 30, 0)
        dt = datetime.combine(date.today(), opening_range_start_time) + timedelta(minutes=self.p.num_opening_bars)
        opening_range_end_time = dt.time()

        if current_bar_datetime.time() >= opening_range_start_time \
                and current_bar_datetime.time() < opening_range_end_time:
            self.opening_range_high = max(self.data.high[0], self.opening_range_high)
            self.opening_range_low = min(self.data.low[0], self.opening_range_low)
            self.opening_range = self.opening_range_high - self.opening_range_low
        else:
            if self.order:
                return

            if self.position and (self.data.close[0] > (self.opening_range_high + self.opening_range)):
                self.close()

            if self.data.close[0] > self.opening_range_high and not self.position and not self.bought_today:
                self.order = self.buy()
                self.bought_today = True

            if self.position and (self.data.close[0] < (self.opening_range_high - self.opening_range)):
                self.order = self.close()

            if self.position and current_bar_datetime.time() >= time(15, 45, 0):
                self.log("RUNNING OUT OF THE - LIQUIDATION POSITION")
                self.close()

    # Stop Method
    def stop(self):
        self.log('(Num Opening Bars %2d) Ending Value %.2f' %
                 (self.params.num_opening_bars, self.broker.getvalue()))

        if self.broker.get_value() > 130000:
            self.flog("*** BIG WINNER ***")

        if self.broker.getvalue() < 70000:
            self.log("*** MAJOR LOSER ***")

# Script Execution
if __name__ == '__main__':
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT DISTINCT(stock_id) as stock_id FROM stock_price_minute
                   """)
    stocks = cursor.fetchall()

    for stock in stocks:
        cerebro = backtrader.Cerebro()
        cerebro.broker.set_cash(100000.0)
        cerebro.addsizer(backtrader.sizers.PercentSizer, percents=95)

        dataframe = pandas.read_sql("""
                                    SELECT datetime, open, high, close, volume
                                    FROM stock_price_minute
                                    WHERE stock_id = :stock_id
                                    AND strftime('%H:%M:%S', datetime) >= '09:30:00'
                                    AND strftime('%H:%M:%S', datetime) < '16:00:00'
                                    ORDER BY datetime ASC
                                    """, conn, params={"stock_id": stock['stock_id']}, index_col='datetime',
                                    parse_dates=['datetime'])

        data = backtrader.feeds.PandasData(dataname=dataframe)

        cerebro.adddata(data)
        cerebro.addstrategy(OpeningRangeBreakout)

        # Executes the backtes
        cerebro.run()
        cerebro.plot()

