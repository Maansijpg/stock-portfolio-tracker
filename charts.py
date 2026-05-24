import matplotlib.pyplot as plt
from db import run_query
def chart1():
    df1 = run_query("""
        SELECT s.ticker,
            ROUND(t.shares * t.buy_price, 2) AS amount_invested,
            ROUND(t.shares * ph.close_price, 2) AS current_value
        FROM transactions t
        JOIN stocks s ON t.stock_id = s.stock_id
        JOIN price_history ph ON t.stock_id = ph.stock_id
        WHERE t.portfolio_id = 1
        AND ph.price_date = (SELECT MAX(price_date) FROM price_history)
""")
    plt.bar(df1['ticker'], df1['amount_invested'], label='Invested')
    plt.bar(df1['ticker'], df1['current_value'], label='Current Value')
    plt.title('Invested vs Current Value')
    plt.legend()
    return plt.gcf() 
def chart2():
    df2 = run_query("""
        SELECT s.ticker,
            ROUND((ph.close_price - t.buy_price) / t.buy_price * 100, 2) AS gain_pct
        FROM transactions t
        JOIN stocks s ON t.stock_id = s.stock_id
        JOIN price_history ph ON t.stock_id = ph.stock_id
        WHERE t.portfolio_id = 1
        AND ph.price_date = (SELECT MAX(price_date) FROM price_history)
""")
    plt.bar(df2['ticker'], df2['gain_pct'])
    plt.title('Gain % per Stock')
    return plt.gcf()
def chart3():
    df3 = run_query("""
        SELECT ROUND(SUM(t.shares * t.buy_price), 2) AS total_invested,
            ROUND(SUM(t.shares * ph.close_price), 2) AS total_value_today
        FROM transactions t
        JOIN price_history ph ON t.stock_id = ph.stock_id
        WHERE t.portfolio_id = 1
        AND ph.price_date = (SELECT MAX(price_date) FROM price_history)
""")
    invested = float(df3['total_invested'][0])
    current = float(df3['total_value_today'][0])
    gain = round(current - invested, 2)
    plt.bar(['Invested', 'Current Value', 'Gain'], [invested, current, gain])
    plt.title('Portfolio Summary')
    return plt.gcf()
print("Done! Check chart1.png, chart2.png, chart3.png")