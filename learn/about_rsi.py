import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def calculate_rsi(data, window=14):
    """Calculate RSI"""
    delta = data['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain.flatten()).rolling(window=window, min_periods=1).mean()
    avg_loss = pd.Series(loss.flatten()).rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Fetch stock data
ticker = "VWRA.L"  # Change to any stock
data = yf.download(ticker, period="6mo", interval="1d")

# Compute RSI
data['RSI'] = calculate_rsi(data)

# Generate Buy/Sell Signals
data['Buy Signal'] = (data['RSI'] < 30) & (data['RSI'].shift(1) >= 30)  # RSI crosses above 30
data['Sell Signal'] = (data['RSI'] > 70) & (data['RSI'].shift(1) <= 70)  # RSI crosses below 70

# Plot Closing Price with Buy/Sell Signals
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

ax1.plot(data.index, data['Close'], label="Closing Price", color='blue')
ax1.scatter(data.index[data['Buy Signal']], data['Close'][data['Buy Signal']], color='green', marker='^', label="Buy Signal", alpha=1)
ax1.scatter(data.index[data['Sell Signal']], data['Close'][data['Sell Signal']], color='red', marker='v', label="Sell Signal", alpha=1)
ax1.set_title(f"{ticker} Stock Price with Buy/Sell Signals")
ax1.legend()
ax1.grid()

# Plot RSI with Buy/Sell Markers
ax2.plot(data.index, data['RSI'], label="RSI", color='red')
ax2.axhline(70, linestyle='--', color='gray', label="Overbought (70)")
ax2.axhline(30, linestyle='--', color='gray', label="Oversold (30)")
ax2.scatter(data.index[data['Buy Signal']], data['RSI'][data['Buy Signal']], color='green', marker='^', label="Buy Signal", alpha=1)
ax2.scatter(data.index[data['Sell Signal']], data['RSI'][data['Sell Signal']], color='red', marker='v', label="Sell Signal", alpha=1)
ax2.set_title("RSI with Buy/Sell Signals")
ax2.legend()
ax2.grid()

plt.show()
