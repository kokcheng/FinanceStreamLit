import streamlit as st

st.title("Info Page")

# what are the different types of text formatting in Streamlit?
st.header("MACD Indicator")
st.write("The MACD Histogram (MACD Hist) is a visual representation of the difference between the MACD Line and the Signal Line in the Moving Average Convergence Divergence (MACD) indicator. It helps traders identify trends, momentum, and potential buy/sell signals.")

st.write("MACD Histogram = MACD Line − Signal Line")
st.write("- MACD Line = 12-period EMA - 26-period EMA")
st.write("- Signal Line = 9-period EMA of the MACD Line")

st.write('''
**Positive Histogram (Above Zero Line):**

When the MACD Line is above the Signal Line, the histogram is positive.
- Indicates bullish momentum (uptrend).
- If the bars are increasing, it suggests strengthening bullish momentum.
- If the bars start decreasing, it signals a potential trend reversal.

**Negative Histogram (Below Zero Line):**

When the MACD Line is below the Signal Line, the histogram is negative.
- Indicates bearish momentum (downtrend).
- If the bars are increasing in the negative zone, it suggests weakening bearish momentum.
- If the bars start decreasing, it signals a potential bullish reversal.

**Zero Crossovers:**
- When the histogram crosses above zero → Bullish signal (MACD Line crosses above Signal Line).
- When the histogram crosses below zero → Bearish signal (MACD Line crosses below Signal Line).
''')

st.code("st.write('This is a Streamlit app.')")


