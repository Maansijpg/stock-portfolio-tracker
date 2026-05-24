# Stock Portfolio Tracker

A relational database project that tracks a stock portfolio, stores real market price data, and runs SQL analytics to calculate profit/loss, portfolio value, and sector allocation — visualized with Python charts.

Built as a DBMS course project using MySQL and Python.

---

## What it does

- Stores stock holdings and buy transactions in a normalized MySQL database
- Automatically downloads 1 year of real daily price data from Yahoo Finance
- Answers three core questions with SQL:
  - What is my portfolio worth today?
  - Am I making or losing money on each stock?
  - How is my money spread across sectors?
- Generates three charts: P&L bar chart, sector pie chart, price history line chart

---

## Database schema

Four tables connected through primary and foreign keys:

```
stocks          — companies you can invest in
portfolios      — your investment account
transactions    — every stock purchase (references stocks + portfolios)
price_history   — daily closing price for each stock (references stocks)
```

**Relationships:**
- `transactions.stock_id` → `stocks.stock_id`
- `transactions.portfolio_id` → `portfolios.portfolio_id`
- `price_history.stock_id` → `stocks.stock_id`

---

## Tech stack

| Tool | Purpose |
|------|---------|
| MySQL | Database engine |
| MySQL Workbench | Writing and testing SQL queries |
| Python 3 | Data loading and visualization |
| yfinance | Downloading real stock price data |
| pandas | Handling query results as DataFrames |
| matplotlib | Drawing charts |
| mysql-connector-python | Connecting Python to MySQL |

---

## Project structure

```
portfolio-tracker/
│
├── create_tables.sql    # Creates all 4 tables in MySQL
├── insert_data.sql      # Inserts stocks, portfolio, and transactions
├── load_prices.py       # Downloads real prices into price_history
├── db.py                # Reusable MySQL connection function
├── charts.py            # Runs analytics queries and draws 3 charts
└── README.md
```

---

## How to run

### 1. Set up the database

Open MySQL Workbench and run these files in order:

```
create_tables.sql
insert_data.sql
```

### 2. Install Python libraries

```bash
pip install mysql-connector-python pandas matplotlib yfinance
```

### 3. Load real price data

Open `load_prices.py` and replace `your_password_here` with your MySQL root password. Then run:

```bash
python load_prices.py
```

This downloads 1 year of daily closing prices for all 5 stocks and inserts them into the `price_history` table.

### 4. Run the analytics and charts

```bash
python db.py       # test the connection first
python charts.py   # generates 3 charts
```

Three chart windows will open. Close each one for the next to appear. Chart images are also saved as `.png` files in the same folder.

---

## SQL concepts covered

- Primary keys and foreign keys
- Referential integrity (MySQL enforces FK constraints)
- Normalization — separate tables for separate concerns
- DDL — `CREATE TABLE`, `UNIQUE`, `NOT NULL`, `FOREIGN KEY`
- DML — `INSERT`, `SELECT`, `WHERE`, `ORDER BY`
- Multi-table `JOIN` queries
- Aggregate functions — `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`
- `GROUP BY` with aggregates
- Subqueries — `SELECT MAX(price_date)` nested inside `WHERE`

---

## Sample analytics queries

**Portfolio value today:**
```sql
SELECT s.company_name, t.shares,
       ROUND(t.shares * ph.close_price, 2) AS current_value
FROM transactions t
JOIN stocks s ON t.stock_id = s.stock_id
JOIN price_history ph ON t.stock_id = ph.stock_id
WHERE ph.price_date = (SELECT MAX(price_date) FROM price_history);
```

**Gain / loss per stock:**
```sql
SELECT s.ticker,
       ROUND((ph.close_price - t.buy_price) * t.shares, 2) AS total_gain,
       ROUND((ph.close_price - t.buy_price) / t.buy_price * 100, 2) AS gain_pct
FROM transactions t
JOIN stocks s ON t.stock_id = s.stock_id
JOIN price_history ph ON t.stock_id = ph.stock_id
WHERE ph.price_date = (SELECT MAX(price_date) FROM price_history);
```

---

## Author

Maansi BR — B.E. Computer Science Engineering, JSS Academy of Technical Education, Bangalore
