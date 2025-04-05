import streamlit as st
from util.stock_util import download_stock_data_list_v2

# function to plot the ticker given the dataframe in the following format
# index is the ticker, columns are the dates, and values are the closing prices
import matplotlib.pyplot as plt
def plot_stock_data(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    for ticker in data.index:
        ax.plot(data.columns, data.loc[ticker], label=ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title("Stock Prices")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


st.title("Watch List Page")
st.subheader("Local Banking Stocks")

# tickers for DBS, OCBC, UOB
tickers = ["D05.SI", "O39.SI", "U11.SI"]
data = download_stock_data_list_v2(tickers, period="3d", interval="1d")

# remove Open, High, Low
data = data.drop(columns=["Open", "High", "Low"])

# format the Date column to yyyy-MMM-dd
data.index = data.index.strftime("%Y-%b-%d")

# transform data such that the ticker is the row, the columns are the dates, and the values are the closing prices
data = data.transpose()
# add stock name for the ticker, for row with D05.SI, add a column with DBS
data = data.rename(index={"D05.SI": "DBS", "O39.SI": "OCBC", "U11.SI": "UOB"})

st.dataframe(data)
# remove row with index = 'Volume'
data = data.drop(index=["Volume"])

plot = plot_stock_data(data)
st.pyplot(plot)

# add a separator
st.write("---")

st.subheader("POEMS Unit Trust")

# tickers for DBS, OCBC, UOB
tickers = ["0P0001OO2D.SI", "0P0001OOJG.SI"]
data = download_stock_data_list_v2(tickers, period="7d", interval="1d")

# remove Open, High, Low
data = data.drop(columns=["Open", "High", "Low", "Volume"])

# format the Date column to yyyy-MMM-dd
data.index = data.index.strftime("%Y-%b-%d")

# transform data such that the ticker is the row, the columns are the dates, and the values are the closing prices
data = data.transpose()
# add stock name for the ticker, for row with D05.SI, add a column with DBS
data = data.rename(index={"0P0001OO2D.SI": "MSCI World", "0P0001OOJG.SI": "Prime USA"})

st.dataframe(data)

plot = plot_stock_data(data)
st.pyplot(plot)

# add a separator
st.write("---")

st.subheader("US Stocks")
# tickers for Nvidia, Tesla, Tiger
tickers = ["NVDA", "TSLA", "BABA"]
data = download_stock_data_list_v2(tickers, period="5d", interval="1d")
# remove Open, High, Low
data = data.drop(columns=["Open", "High", "Low"])
# format the Date column to yyyy-MMM-dd
data.index = data.index.strftime("%Y-%b-%d")
# transform data such that the ticker is the row, the columns are the dates, and the values are the closing prices
data = data.transpose()
# add stock name for the ticker, for row with D05.SI, add a column with DBS
data = data.rename(index={"NVDA": "Nvidia", "TSLA": "Tesla", "BABA": "Alibaba"})
st.dataframe(data)



# remove row with index = 'Volume'
data = data.drop(index=["Volume"])

plot = plot_stock_data(data)
st.pyplot(plot)
