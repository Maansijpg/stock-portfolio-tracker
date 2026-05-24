import mysql.connector
import pandas as pd

<<<<<<< HEAD
def run_query(sql):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
=======
def run_query(sql): #gets data from MySQL
    conn = mysql.connector.connect(
        host='localhost',
>>>>>>> 0ce5f6d5f9d567f81d5c70237f6b236ecfb89988
        user='root',
        password='Maansi@2707',
        database='portfolio_db'
    )
<<<<<<< HEAD
    df = pd.read_sql(sql, conn)
=======
    df = pd.read_sql(sql, conn) #returns it as a table
>>>>>>> 0ce5f6d5f9d567f81d5c70237f6b236ecfb89988
    conn.close()
    return df