# stock-bot
This is the repo for the Twitter bot @stockbot42.
The bot, hosted on AWS Lambda, responds to tweets like '@stockbot42 AAPL' by giving useful summary info on the user's requested ticker. The market information is obtained via the yfinance library for Python, which pulls the data from Yahoo! Finance.