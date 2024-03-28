import yfinance as yf
from tabulate import tabulate

def get_live_stock_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        live_price = stock.history(period='1d')['Close'][0]
        return live_price
    except Exception as e:
        print(f"Error fetching live stock price for {ticker_symbol}: {e}")
        return None

def get_52_week_high(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period='1y')
        high_52_week = hist['Close'].max()
        return high_52_week
    except Exception as e:
        print(f"Error fetching 52-week high for {ticker_symbol}: {e}")
        return None

def get_average_volume(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period='1y')
        avg_volume = hist['Volume'].mean() / 1e6  # Convert volume to millions
        return avg_volume
    except Exception as e:
        print(f"Error fetching average volume for {ticker_symbol}: {e}")
        return None

def get_today_volume(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period='1d')
        today_volume = hist['Volume'][0] / 1e6  # Convert volume to millions
        return today_volume
    except Exception as e:
        print(f"Error fetching today's volume for {ticker_symbol}: {e}")
        return None

def get_options_volume(ticker_symbol):
    try:
        options = yf.Ticker(ticker_symbol).option_chain(stock.info['optionable'])
        options_volume = options.calls.volume.sum() / 1e6  # Convert volume to millions
        return options_volume
    except Exception as e:
        print(f"Error fetching options volume for {ticker_symbol}: {e}")
        return None

def highlight_price(close_price, high_52_week):
    percent_difference = ((high_52_week - close_price) / high_52_week) * 100
    if percent_difference > 10:
        return "\033[92m" + f"${percent_difference:.2f}%" + "\033[0m"  # Display in green
    else:
        return "\033[91m" + f"${percent_difference:.2f}%" + "\033[0m"  # Display in red

def analyze_stocks(ticker_symbols):
    data = []
    headers = ["Symbol", "Live Price", "52-week High", "Difference", "Average Volume (Millions)",
               "Today's Volume (Millions)", "Options Volume (Millions)", "Within 10% of 52-week High"]
    for symbol in ticker_symbols:
        live_price = get_live_stock_price(symbol)
        high_52_week = get_52_week_high(symbol)
        avg_volume = get_average_volume(symbol)
        today_volume = get_today_volume(symbol)
        options_volume = get_options_volume(symbol)
        if live_price is not None and high_52_week is not None:
            difference = live_price - high_52_week
            within_10_percent = highlight_price(live_price, high_52_week)

            # Check if Today's Volume is greater than Average Volume
            if today_volume is not None and avg_volume is not None:
                if today_volume > avg_volume:
                    today_volume_text = "\033[92m" + f"{today_volume:.2f}" + "\033[0m"  # Display in green
                else:
                    today_volume_text = "\033[91m" + f"{today_volume:.2f}" + "\033[0m"  # Display in red
            else:
                today_volume_text = "N/A"

            data.append([symbol, f"${live_price:.2f}", f"${high_52_week:.2f}", f"${difference:.2f}",
                         f"{avg_volume:.2f}" if avg_volume is not None else "N/A", today_volume_text,
                         f"{options_volume:.2f}" if options_volume is not None else "N/A", within_10_percent])
    print(tabulate(data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    ticker_symbols = ["MSFT", "AAPL", "NVDA", "QQQ", "SPY", "AMZN", "GOOG", "META", "BRK.A", "LLY",
                      "TSM"]  # Updated list of ticker symbols
    analyze_stocks(ticker_symbols)
