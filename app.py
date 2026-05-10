import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from db import run_query

from charts import chart1, chart2, chart3

import subprocess

st.set_page_config(page_title="Portfolio Tracker", layout="wide")

with st.sidebar:
    st.title("Portfolio Tracker")
    page = st.radio("Navigation", ["Dashboard", "Transactions", "Price History"])

    if st.button("Refresh Prices"):
        subprocess.run(["/opt/anaconda3/bin/python", "/Users/maansibr/Desktop/stock mysql/finance.py"])

    st.title("Portfolio Tracker")
if page == "Dashboard":
    st.title("Dashboard")
    fig1 = chart1()
    st.pyplot(fig1)
    plt.close()

elif page == "Transactions":
    st.title("Transactions")
    df = run_query("SELECT * FROM transactions")
    st.dataframe(df)

elif page == "Price History":
    st.title("Price history")
    fig3 = chart3()
    st.pyplot(fig3)
    plt.close()

