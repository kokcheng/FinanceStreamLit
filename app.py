import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import os
import ta  # Technical Analysis Library
import matplotlib.pyplot as plt

# File to save stock data
DATA_FILE = "stock_data.csv"

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

# Streamlit UI
st.title("Stock Analysis")

# Sidebar for user input
st.sidebar.header("Stock Selection")
ticker = st.sidebar.selectbox("Select Stock Ticker:", ["VWRA.L", "AAPL", "CFA.SI"])

period = st.sidebar.selectbox("Select Data Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

if st.sidebar.button("Download Data"):
    df = fetch_stock_data(ticker, period)
    st.sidebar.success(f"Data for {ticker} downloaded and saved!")

# Load saved stock data
df = load_stock_data()
if df is not None:
    st.subheader("Stock Data")
    st.dataframe(df.tail())

    # RSI Calculation
    df = calculate_rsi(df)

    df = calculate_macd(df)

    df = calculate_bollinger_bands(df)

    # Plot RSI
    st.subheader("RSI/ MACD")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red")  # Overbought level
    ax.axhline(30, linestyle="--", color="green")  # Oversold level
    ax.set_ylabel("RSI Value")
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(df.index, df["MACD"], label="MACD", color="purple")
    ax2.plot(df.index, df["Signal_Line"], label="Signal Line", color="orange")
    ax2.set_ylabel("MACD Value")
    ax2.legend()
    st.pyplot(fig)
    # Indicate buy/sell signals
    st.subheader("Buy/ Sell Signals")

    # buy/sell signals based on RSI only
    buy_signals = (df["RSI"] < 30)
    sell_signals = (df["RSI"] > 70)
    '''
    buy_signals = (df["RSI"] < 30) & (df["MACD"] > df["Signal_Line"])
    sell_signals = (df["RSI"] > 70) & (df["MACD"] < df["Signal_Line"])
    '''
    df["Buy_Signal"] = np.where(buy_signals, 1, 0)
    df["Sell_Signal"] = np.where(sell_signals, 1, 0)

    # create a new figure for buy/sell signals
    fig2, ax = plt.subplots()
    ax.plot(df.index, df["Close"], label="Close Price", color="black")
    ax.scatter(df.index, df["Buy_Signal"] * df["Close"], label="Buy Signal", marker="^", color="green")
    ax.scatter(df.index, df["Sell_Signal"] * df["Close"], label="Sell Signal", marker="v", color="red")
    ax.set_ylabel("Close Price")
    ax.legend()

    st.pyplot(fig2)



else:
    st.warning("No stock data found. Please download stock data first.")

