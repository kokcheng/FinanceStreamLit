import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import os
import ta  # Technical Analysis Library
import matplotlib.pyplot as plt

from util.stock_util import get_stock_info
from util.stock_util import plot_stock_data


# File to save stock data
DATA_FILE = "stock_data.csv"

def get_stock_selection():
    # read stock selection from an excel file with two columns: stock_ticker and stock_name
    #stock_selection = pd.read_excel("stock_selection.xlsx")
    stock_selection = pd.DataFrame({
        "stock_ticker": ["VWRA.L", "CFA.SI", "AAPL", "NVDA", "AMZN", "D05.SI", "O39.SI", "U11.SI"],
        "stock_name": ["Vanguard FTSE All-World UCITS ET", "NikkoAM-StraitsTrading Asia ex Japan REIT ETF", "Apple Inc", "NVIDIA Corporation", "Amazon.com Inc", "DBS Group Holdings Ltd", "Oversea-Chinese Banking Corporation Limited", "United Overseas Bank Limited"]
    })
    return stock_selection

# Function to fetch stock data
def fetch_stock_data(ticker, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.to_csv(DATA_FILE)
    return df

# Function to calculate RSI
def calculate_rsi(df, window=14):
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=window).rsi()
    return df

def calculate_macd(df):
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["Signal_Line"] = macd.macd_signal()
    df["MACD_Hist"] = macd.macd_diff()
    return df

def calculate_bollinger_bands(df):
    df["BB_High"], df["BB_Mid"], df["BB_Low"] = ta.volatility.bollinger_hband(df["Close"]), ta.volatility.bollinger_mavg(df["Close"]), ta.volatility.bollinger_lband(df["Close"])
    return df

# Load stock data from file
def load_stock_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    return None


def plot_bollinger_bands(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["Close"], label="Close Price", color="black")
    ax.plot(df.index, df["BB_High"], label="BB High", color="red")
    ax.plot(df.index, df["BB_Mid"], label="BB Mid", color="blue")
    ax.plot(df.index, df["BB_Low"], label="BB Low", color="green")
    ax.set_ylabel("Close Price")
    ax.legend()
    return fig


# Streamlit UI

# Sidebar for user input
st.sidebar.write("v1.0.0")
st.sidebar.header("Stock Selection")

# Load stock selection
stock_selection = get_stock_selection()
stock_tickers = stock_selection["stock_ticker"].tolist()
stock_names = stock_selection["stock_name"].tolist()

# Select stock ticker
ticker = st.sidebar.selectbox("Select Stock Ticker:", stock_tickers, index=0)
# display stock name
stock_name = stock_names[stock_tickers.index(ticker)]

st.title(f"Stock Name: {stock_name}")

period = st.sidebar.selectbox("Select Data Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

if st.sidebar.button("Download Data"):
    df = fetch_stock_data(ticker, period)
    st.sidebar.success(f"Data for {ticker} downloaded and saved!")

# Load saved stock data
df = load_stock_data()
info = get_stock_info(ticker)
if info is not None:
    # Display stock information
    st.subheader("Stock Information")
    st.write(f"**Fifty Week Range:** {info['fiftyTwoWeekRange']}")
    if "yield" in info:
        st.write(f"**Dividend Yield:** {info['yield']}")

    st.write(f"**Trailing PE:** {info['trailingPE']}")
    # format the volume to be in millions
    if "volume" in info:
        info["volume"] = info["volume"] / 1_000_000
        info["volume"] = f"{info['volume']:.2f}M"
    else:
        info["volume"] = "N/A"
    st.write(f"**Volume:** {info['volume']}")
    st.write(f"**200 days average:** {info['twoHundredDayAverage']}")
else:
    st.sidebar.warning("No stock information found. Please check the ticker.")

if df is not None:
    # check if the stock data is already in session state or data changed
    if "stock_data" in st.session_state:
        st.write("add stock data to session state")
        st.session_state.stock_data = df
        st.session_state.stock_name = stock_name


    st.subheader("Last 10 days of stock data")
    # last 10 rows of stock data in reverse order
    st.dataframe(df.tail(10)[::-1])

    # plot a candle stick chart
    st.subheader("Stock Price Chart")
    # plot only the Close price
    df = df[["Close"]]
    fig = plot_stock_data(df)
    st.pyplot(fig)

    df = calculate_bollinger_bands(df)
    st.subheader("Bollinger Bands")
    # plot the Bollinger Bands
    fig = plot_bollinger_bands(df)
    st.pyplot(fig)

else:
    st.warning("No stock data found. Please download stock data first.")

