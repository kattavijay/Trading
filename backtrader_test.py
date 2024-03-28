import backtrader as bt
import yfinance as yf

class StockData(bt.feeds.PandasData):
    params = (
        ('openinterest', None),
    )

def get_stock_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period='1y')
        hist = hist.reset_index()
        hist.columns = [col.lower() for col in hist.columns]
        return hist
    except Exception as e:
        print(f"Error fetching stock data for {ticker_symbol}: {e}")
        return None

def analyze_stocks(ticker_symbols):
    cerebro = bt.Cerebro()
    for symbol in ticker_symbols:
        stock_data = get_stock_data(symbol)
        if stock_data is not None:
            data = StockData(dataname=stock_data)
            cerebro.adddata(data, name=symbol)
    cerebro.run()
    cerebro.plot()

if __name__ == "__main__":
    ticker_symbols = ["MSFT", "AAPL", "NVDA", "QQQ", "SPY", "AMZN", "GOOG", "META", "BRK.A", "LLY", "TSM"]
    analyze_stocks(ticker_symbols)
