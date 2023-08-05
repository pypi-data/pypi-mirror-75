import yfinance as yf

tickers = [
    yf.Ticker("AAPL"),
    # ................
    # ^^ add tickers of companies you want to follow here
    # you can find a ticker from a company name here https://www.marketwatch.com/tools/quotes/lookup.asp
]


# By default Seamless Cloud will execute the function `main` in the file `function.py`
# You can override this behaviour by using --entrypoint flag
def main():
    for ticker in tickers:
        print(f"Company: {ticker.info['longName']}")
        print(f"Stock Price: ${ticker.info['regularMarketPrice']}")
        # Let's look at 3 latest recommendations by stock analysts firms
        print("Latest 3 recommendations:")
        for date, row in ticker.recommendations.iloc[-3:].iterrows():
            print(f"{row['Firm']} recommendation dated {date.date()}: {row['To Grade']}")
        # ................
        # ^^ here you can send email or message in your favourite messenger if you want
