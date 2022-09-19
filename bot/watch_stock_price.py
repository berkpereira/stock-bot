import yfinance as yf

# Still only experimenting with yfinance Yahoo API library

# watch and update stock price every minute
# at this point, simulated using last trading day data
apple = yf.Ticker("AAPL")
day_prices = apple.history(period="1d", interval="1m")