import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import run_query
from charts import chart1, chart2, chart3
from ml_signal import get_signals, train
import subprocess

st.set_page_config(page_title="Portfolio Tracker", layout="wide")


with st.sidebar:
    st.title("Portfolio Tracker")
    page = st.radio("Navigation", ["Dashboard", "ML Signals", "Transactions", "Price History"])

    if st.button("Refresh Prices"):
        subprocess.run(["/opt/anaconda3/bin/python", "/Users/maansibr/Desktop/stock mysql/finance.py"])
        st.success("Prices refreshed!")

    if st.button("Retrain Model"):
        with st.spinner("Training..."):
            train()
        st.success("Model retrained!")

st.title("Portfolio Tracker")


if page == "Dashboard":
    st.subheader("Dashboard")

    fig1 = chart1()
    st.pyplot(fig1)
    plt.close()

    fig2 = chart2()
    st.pyplot(fig2)
    plt.close()

    fig3 = chart3()
    st.pyplot(fig3)
    plt.close()


elif page == "ML Signals":
    st.subheader("ML Signal — Today's Recommendation")
    st.caption("Buy if +1% in 10 days, Sell if -1%, else Hold | Accuracy: 42%")    
    signals = get_signals()

    def color_signal(val):
        if val == 'BUY':
            return 'font-weight: bold'
        elif val == 'SELL':
            return 'font-weight: bold'
        else:
            return 'font-weight: bold'

    styled = signals.style.map(color_signal, subset=['Signal'])    
    st.dataframe(styled, use_container_width=True)


    st.divider()
    st.caption(
        " This is a student project — not financial advice. "
        "The model learns historical patterns that may not repeat. "
        "Accuracy is limited by 1 year of data and 5 stocks."
    )


elif page == "Transactions":
    st.subheader("Transactions")
    df = run_query("SELECT * FROM transactions")
    st.dataframe(df)



elif page == "Price History":
    st.subheader("Price History")
    fig3 = chart3()
    st.pyplot(fig3)
    plt.close()
