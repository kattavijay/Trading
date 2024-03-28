import yfinance as yf
import pandas as pd


def get_current_price_and_52_week_high(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period='1y')
        current_price = stock.history(period='1d')['Close'][0]
        high_52_week = hist['Close'].max()
        return current_price, high_52_week
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None, None


def count_stocks_within_10_percent_of_52_week_high(ticker_symbols):
    count = 0
    for symbol in ticker_symbols:
        current_price, high_52_week = get_current_price_and_52_week_high(symbol)
        if current_price is not None and high_52_week is not None:
            if (high_52_week - current_price) / high_52_week <= 0.10:
                count += 1
    return count


def get_sp500_tickers():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        sp500_df = tables[0]
        sp500_tickers = sp500_df['Symbol'].tolist()
        return sp500_tickers
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []


if __name__ == "__main__":
    try:
        sp500_tickers = get_sp500_tickers()
        if not sp500_tickers:
            print("Failed to retrieve S&P 500 tickers. Exiting program.")
            exit(1)

        num_stocks_within_10_percent = count_stocks_within_10_percent_of_52_week_high(sp500_tickers)
        print(
            f"The number of S&P 500 stocks whose current price is within 10% of the 52-week high: {num_stocks_within_10_percent}")
    except Exception as e:
        print(f"An error occurred: {e}")
