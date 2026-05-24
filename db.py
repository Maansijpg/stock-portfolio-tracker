import mysql.connector
import pandas as pd

def run_query(sql):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='Maansi@2707',
        database='portfolio_db'
    )
    df = pd.read_sql(sql, conn)
    conn.close()
    return df