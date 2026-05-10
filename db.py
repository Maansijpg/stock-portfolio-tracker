import mysql.connector
import pandas as pd

def run_query(sql): #gets data from MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Maansi@2707',
        database='portfolio_db'
    )
    df = pd.read_sql(sql, conn) #returns it as a table
    conn.close()
    return df