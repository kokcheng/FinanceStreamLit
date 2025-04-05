import streamlit as st

# import the calculate_rsi function from the utility module
from util.rsi_util import calculate_rsi, plot_rsi, plot_rsi_with_signals, plot_rsi_divergence, plot_rsi_trendline

st.title("RSI")
st.write("""
#### RSI Formula
𝑅𝑆𝐼 = 100 − 100/(1 + 𝑅𝑆)
where\n
𝑅𝑆 = Average Gain over 𝑛 periods/Average Loss over 𝑛 periods
 
The default period n is 14. RSI values range from 0 to 100.

#### RSI Interpretation
- Above 70 → Overbought (possible price correction or reversal)
- Below 30 → Oversold (potential buying opportunity)
- Between 30-70 → Neutral zone (no clear trend)

#### Trading Strategies Using RSI
1) Overbought & Oversold Levels
- If RSI > 70, consider selling (price may drop).
- If RSI < 30, consider buying (price may rise).

2) Divergence
- Bullish Divergence: RSI rises while price falls → potential reversal upward.
- Bearish Divergence: RSI falls while price rises → potential reversal downward.

3) RSI Crossovers
- RSI crossing above 30 is a bullish signal.
- RSI crossing below 70 is a bearish signal.

4) RSI Trendline Breakout
- Draw a trendline on the RSI itself. If RSI breaks the trendline, it signals a potential change in trend.
""")

if "stock_data" not in st.session_state:
    st.session_state.stock_data = None
    st.write("No stock data loaded yet.")
else:
    df = st.session_state.stock_data
    st.write("Stock data loaded successfully.")
    if df is not None:

        st.subheader("Stock Data")
        df = calculate_rsi(df)
        st.dataframe(df.tail())

        st.subheader("RSI Plot")
        fig = plot_rsi(df)
        st.pyplot(fig)

        st.subheader("RSI with Buy/Sell Signals")
        fig2 = plot_rsi_with_signals(df)
        st.pyplot(fig2)

        st.subheader("RSI Divergence Plot")
        fig3 = plot_rsi_divergence(df)
        st.pyplot(fig3)

        st.subheader("RSI Trendline Plot")
        fig4 = plot_rsi_trendline(df)
        st.pyplot(fig4)