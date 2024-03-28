import yfinance as yf
import tweepy


def get_live_stock_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        live_price = stock.history(period='1d')['Close'][0]
        return live_price
    except Exception as e:
        print(f"Error fetching live stock price for {ticker_symbol}: {e}")
        return None


def get_number_of_tweets(symbol):
    try:
        # Twitter API credentials
        consumer_key = "VTyy3wIpC0O8usOUkZjJuarKc"
        consumer_secret = "60yVfndK4x1aHF5EImnH45ZElmCugwSwMNVXTEmPcpwh69hJGB"
        access_token = "33452553-u2wfXnCxHY0BigF5yxVxflAXzqZWlpm0zEA5IuFRm"
        access_token_secret = "b2yencMvFJWo3FkLabntvytII70zOS1Uw9z7gSqruplv7"

        # Authenticate with Twitter API
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Search for tweets mentioning the symbol today
        today_tweets = api.search_tweets(q=f"${symbol}", count=100, result_type="recent", tweet_mode="extended")
        return len(today_tweets)
    except Exception as e:
        print(f"Error fetching tweets for {symbol}: {e}")
        return None


def analyze_stocks(ticker_symbols):
    for symbol in ticker_symbols:
        live_price = get_live_stock_price(symbol)
        if live_price is not None:
            tweets_count = get_number_of_tweets(symbol)
            print(f"Symbol: {symbol}, Live Price: {live_price:.2f}, Tweets Today: {tweets_count}")


if __name__ == "__main__":
    ticker_symbols = ["MSFT", "AAPL", "NVDA", "QQQ", "SPY", "AMZN", "GOOG", "META", "BRK.A", "LLY", "TSM"]
    analyze_stocks(ticker_symbols)