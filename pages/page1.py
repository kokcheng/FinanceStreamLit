import streamlit as st

st.title("Page 1")
st.write("This is Page 1.")



if "stock_data" not in st.session_state:
    #st.session_state.stock_data = None
    st.write("No stock data loaded yet.")
else:
    st.write("Stock data loaded successfully.")
    df = st.session_state.stock_data

    st.subheader("Stock Data")
    st.dataframe(df.tail())

# write new line
st.write("## Example of RSI Calculation")
st.write("""
tst
         """)

# different text formatting
st.write("**Bold Text**")
st.write("*Italic Text*")
st.write("`Inline Code`")
st.write("```python\n# Code Block\nprint('Hello, World!')\n```")
st.write("### Subheader")
st.write("#### Sub-subheader")
st.write("1. Numbered List")
st.write("- Bullet List")
st.write("[Link to Streamlit Documentation](https://docs.streamlit.io/library/)")
st.write("![Image](https://www.example.com/image.png)")
st.write("## Conclusion")
