
# function download stock data from yfinance given a ticker
import yfinance as yf
import pandas as pd

# function to download stock data from yfinance given a list of tickers
def download_stock_data_list(tickers, period="6mo", interval="1d"):
    """
    Download stock data from yfinance given a list of tickers.

    Parameters:
    tickers (list): List of stock ticker symbols.
    period (str): Period for the stock data. Default is "6mo".
    interval (str): Interval for the stock data. Default is "1d".

    Returns:
    dict: Dictionary with ticker as key and DataFrame as value.
    """
    stock_data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            stock_data[ticker] = df
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
    return stock_data

# function to download stock data from yfinance given a ticker list, use the download function to download data without for loop
def download_stock_data_list_v2(tickers, period="6mo",interval="1d"):
    """
    Download stock data from yfinance given a list of tickers.

    Parameters:
    tickers (list): List of stock ticker symbols.
    period (str): Period for the stock data. Default is "6mo".
    interval (str): Interval for the stock data. Default is "1d".

    Returns:
    dict: Dictionary with ticker as key and DataFrame as value.
    """
    try:
        stock_data = yf.download(tickers, period=period, interval=interval)
        return stock_data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None


def download_stock_data(ticker, period="6mo", interval="1d"):
    """
    Download stock data from yfinance given a ticker.

    Parameters:
    ticker (str): Stock ticker symbol.
    period (str): Period for the stock data. Default is "6mo".
    interval (str): Interval for the stock data. Default is "1d".

    Returns:
    pd.DataFrame: DataFrame containing the stock data.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    data = download_stock_data(ticker, period="7d", interval="1d")
    if data is not None:
        print(data.head())
    else:
        print("Failed to download stock data.")

    # List of tickers
    tickers = ['AAPL', 'GOOG', 'MSFT', 'TSLA']
    data = download_stock_data_list(tickers, period="7d", interval="1d")
    if data is not None:
        for ticker, df in data.items():
            print(f"{ticker} data:")
            print(df.head())
    else:
        print("Failed to download stock data.")