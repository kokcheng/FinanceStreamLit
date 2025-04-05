import ta
from matplotlib import pyplot as plt


# function to calculate the RSI given a DataFrame
# Function to calculate RSI
def calculate_rsi(df, window=14):
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=window).rsi()
    return df

def plot_rsi(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red", label="Overbought (70)")
    ax.axhline(30, linestyle="--", color="green", label="Oversold (30)")
    ax.set_ylabel("RSI")
    ax.legend()
    return fig

def plot_rsi_with_signals(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red", label="Overbought (70)")
    ax.axhline(30, linestyle="--", color="green", label="Oversold (30)")
    ax.set_ylabel("RSI")
    ax.legend()

    # Indicate buy/sell signals
    buy_signals = (df["RSI"] < 30)
    sell_signals = (df["RSI"] > 70)

    ax.scatter(df.index[buy_signals], df["RSI"][buy_signals], marker="^", color="green", label="Buy Signal")
    ax.scatter(df.index[sell_signals], df["RSI"][sell_signals], marker="v", color="red", label="Sell Signal")

    return fig

# plot the RSI to show bullish and bearish divergence
def plot_rsi_divergence(df):
    fig, ax = plt.subplots()

    # plot the close price on the second y-axis


    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red", label="Overbought (70)")
    ax.axhline(30, linestyle="--", color="green", label="Oversold (30)")
    ax.set_ylabel("RSI")
    ax.legend()

    # Indicate bullish and bearish divergence
    # More accurate divergence conditions
    bullish_divergence = (
            (df["RSI"] < 30) &  # RSI in oversold territory
            (df["Close"] < df["Close"].shift(1)) &  # Price making lower lows
            (df["RSI"] > df["RSI"].shift(1))  # RSI making higher lows
    )

    bearish_divergence = (
            (df["RSI"] > 70) &  # RSI in overbought territory
            (df["Close"] > df["Close"].shift(1)) &  # Price making higher highs
            (df["RSI"] < df["RSI"].shift(1))  # RSI making lower highs
    )
    ax.scatter(df.index[bullish_divergence], df["RSI"][bullish_divergence], marker="^", color="green", label="Bullish Divergence")
    ax.scatter(df.index[bearish_divergence], df["RSI"][bearish_divergence], marker="v", color="red", label="Bearish Divergence")

    ax2 = ax.twinx()
    ax2.plot(df.index, df["Close"], label="Close Price", color="black", alpha=0.5)
    ax2.set_ylabel("Close Price")
    return fig

# plot trendlines on the RSI
def plot_rsi_trendline(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["RSI"], label="RSI", color="blue")
    ax.axhline(70, linestyle="--", color="red", label="Overbought (70)")
    ax.axhline(30, linestyle="--", color="green", label="Oversold (30)")
    ax.set_ylabel("RSI")
    ax.legend()

    # Draw trendlines
    # Example trendlines (you can replace these with actual calculations)
    ax.plot([df.index[0], df.index[-1]], [30, 70], linestyle='--', color='orange', label='Trendline')
    return fig