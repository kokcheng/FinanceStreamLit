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
def fetch_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.to_csv(DATA_FILE)
    return df

# Function to calculate RSI
def calculate_rsi(df, window=14):
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=window).rsi()
    return df

# Load stock data from file
def load_stock_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    return None

# Streamlit UI
st.title("Stock Analysis App")

# Sidebar for user input
st.sidebar.header("Stock Selection")
ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL")
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

    # Plot RSI
    st.subheader("RSI Indicator")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red")  # Overbought level
    ax.axhline(30, linestyle="--", color="green")  # Oversold level
    ax.set_ylabel("RSI Value")
    ax.legend()
    st.pyplot(fig)

else:
    st.warning("No stock data found. Please download stock data first.")

