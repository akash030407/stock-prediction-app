import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Prediction App", layout="wide")

st.title("📈 Stock Price Prediction Website")

st.write("Enter stock symbol (Example: AAPL, TSLA, TCS.NS)")

stock = st.text_input("Stock Symbol")

if stock:
    data = yf.download(stock, start="2020-01-01")

    st.subheader("Stock Data")
    st.write(data.tail())

    st.subheader("Closing Price Chart")

    fig, ax = plt.subplots()
    ax.plot(data["Close"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    st.pyplot(fig)