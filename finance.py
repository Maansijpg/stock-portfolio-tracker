import yfinance as yf
import mysql.connector
import pandas as pd
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Maansi@2707",
    database="portfolio_db"
)
cursor = conn.cursor()
tickers = ["AAPL", "MSFT", "INFY.NS", "HDFCBANK.NS", "ASIANPAINT.NS"]
stock_ids = [1, 2, 3, 4, 5]
for i in range(len(tickers)):
    ticker = tickers[i]
    stock_id = stock_ids[i]


    data = yf.download(ticker, period="1y", auto_adjust=True, progress=False) #gets ticker data from yf for 1 year
 
    data.reset_index(inplace=True) #gets the date as a column(yf saves it as a row)

    for j in range(len(data)):
        row = data.iloc[j] #goes through each row fetching data at a time
        date = pd.to_datetime(row["Date"].iloc[0]).strftime("%Y-%m-%d")
        price = round(float(row["Close"]), 2)
        vol = int(row["Volume"])
        
        
        sql = "INSERT IGNORE INTO price_history (stock_id, price_date, close_price, volume) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (stock_id, date, price, vol))
    print("Done with", ticker)

conn.commit()
print("All prices saved!")
cursor.close()
conn.close()
