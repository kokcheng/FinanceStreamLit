import streamlit as st

st.title("Page 1")
st.write("This is Page 1.")

df = st.session_state.stock_data
if df is not None:
    st.subheader("Stock Data")
    st.dataframe(df.tail())

