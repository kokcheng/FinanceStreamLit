import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import os
import ta  # Technical Analysis Library
import matplotlib.pyplot as plt



# File to save stock data
DATA_FILE = "stock_data.csv"

def get_stock_selection():
    # read stock selection from an excel file with two columns: stock_ticker and stock_name
    #stock_selection = pd.read_excel("stock_selection.xlsx")
    stock_selection = pd.DataFrame({
        "stock_ticker": ["VWRA.L", "CFA.SI", "AAPL"],
        "stock_name": ["Vanguard FTSE All-World UCITS ET", "NikkoAM-StraitsTrading Asia ex Japan REIT ETF", "Apple Inc"]
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
if df is not None:
    # check if the stock data is already in session state or data changed
    if "stock_data" in st.session_state:
        st.write("add stock data to session state")
        st.session_state.stock_data = df


    st.subheader("Last 10 days of stock data")
    # last 10 rows of stock data in reverse order
    st.dataframe(df.tail(10)[::-1])
    '''
    # RSI Calculation
    df = calculate_rsi(df)

    df = calculate_macd(df)

    df = calculate_bollinger_bands(df)

    # display RSI value in table
    st.subheader("RSI Value")
    st.dataframe(df[["RSI", "MACD", "Signal_Line", "MACD_Hist"]].tail(5))

    # plot the MACD Histogram
    st.subheader("MACD Histogram")
    st.write("Positive Histogram implies bullish momentum, while Negative Histogram implies bearish momentum.")
    
    fig1, ax = plt.subplots()
    ax.bar(df.index, df["MACD_Hist"], label="MACD Histogram", color="grey")
    ax.axhline(0, linestyle="--", color="black")
    ax.set_ylabel("MACD Histogram")
    ax.legend()
    st.pyplot(fig1)

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
    #buy_signals = (df["RSI"] < 30) & (df["MACD"] > df["Signal_Line"])
    #sell_signals = (df["RSI"] > 70) & (df["MACD"] < df["Signal_Line"])
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

    st.subheader("Bollinger Bands")
    st.text("Bollinger Bands are a type of statistical chart characterizing the prices and volatility over time of a financial instrument or commodity, using a formulaic method propounded by John Bollinger in the 1980s.")

    fig3 = plot_bollinger_bands(df)
    st.pyplot(fig3)
    '''
else:
    st.warning("No stock data found. Please download stock data first.")

