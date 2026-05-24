import pandas as pd
import numpy as np
from db import run_query
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_sample_weight
import pickle

MODEL_PATH = "/Users/maansibr/Desktop/Business & Finance/stock mysql/model.pkl"
FEATURE_COLS = ['return_1d', 'return_5d', 'return_20d', 'ma_5', 'ma_20', 'ma_ratio', 'rsi', 'macd']

def load_data():
    df = run_query("""
        SELECT s.ticker, DATE_FORMAT(ph.price_date, '%Y-%m-%d') AS date, ph.close_price AS close, ph.volume
        FROM price_history ph
        JOIN stocks s ON ph.stock_id = s.stock_id
        ORDER BY s.ticker, ph.price_date
    """)
    return df

def compute_rsi(series, period=14):
    #series: the close price column for one ticker
    #period: we look at the last 14 days, standard RSI period
    delta    = series.diff()
    #diff() gives us how much price changed each day (today - yesterday)
    gain     = delta.clip(lower=0)
    #clip(lower=0) keeps only positive changes (up days), sets down days to 0
    loss     = -delta.clip(upper=0)
    #clip(upper=0) keeps only negative changes (down days), sets up days to 0
    #we negate it so losses are positive numbers
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    #average gain and loss over the last 14 days
    rs       = avg_gain / avg_loss
    #RS = ratio of average gain to average loss
    #high RS means more/bigger up days than down days
    rsi      = 100 - (100 / (1 + rs))
    #standard RSI formula that converts RS into a 0-100 scale
    #RS of infinity (only up days) → RSI = 100
    #RS of 0 (only down days) → RSI = 0
    return rsi

def engineer_features(df):
    df = df.sort_values(['ticker', 'date']).copy() #all stocks of same company together and sorted by date
    df['return_1d']  = df.groupby('ticker')['close'].pct_change(1) #did price go up or down in 1 day? (today's close vs yesterday's close)
    df['return_5d']  = df.groupby('ticker')['close'].pct_change(5) #5d
    df['return_20d'] = df.groupby('ticker')['close'].pct_change(20) #20d
    #pct_change(1) = (today - yesterday) / yesterday
    df['ma_5']  = df.groupby('ticker')['close'].transform(lambda x: x.rolling(5).mean())
    df['ma_20'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(20).mean())
    #moving averages- calculated to identify the trend direction of a stock over a specific period of time.
    #rolling: creates a sliding window of 5 rows and 20 rows respectively and gets the mean.
    df['ma_ratio'] = df['close'] / df['ma_20']
    #ma_ratio > 1.0 means price is above the moving average (bullish), < 1.0 means below (bearish)
    df['ma_12'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(12).mean())
    df['ma_26'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(26).mean())
    df['macd']  = df['ma_12'] - df['ma_26']
    #macd > 0 means the short term average is above the long term average (bullish)
    #macd < 0 means the short term average is below the long term average (bearish)
    #macd crossing zero is a classic buy/sell signal in trading
    df['rsi'] = df.groupby('ticker')['close'].transform(compute_rsi)
    #rsi > 70 means overbought (likely to drop)
    #rsi < 30 means oversold (likely to bounce)
    #we compute it per ticker so AAPL's streak doesnt bleed into MSFT's calculation
    return df

def create_labels(df, lookahead=10, buy_threshold=0.01, sell_threshold=-0.01):
    #lookahead: increased to 10 days to give patterns more time to play out and reduce daily noise
    #buy_threshold: 1% move up in 10 days = Buy
    #sell_threshold: 1% move down in 10 days = Sell
    df = df.copy()
    df['future_close']  = df.groupby('ticker')['close'].shift(-lookahead) #price after 10 days
    df['future_return'] = (df['future_close'] - df['close']) / df['close'] #percentage change
    df['label'] = 1 #default is hold
    df.loc[df['future_return'] > buy_threshold,  'label'] = 2  # Buy
    df.loc[df['future_return'] < sell_threshold, 'label'] = 0  # Sell
    df = df.dropna(subset=['future_return'])
    return df

def train():
    df = load_data()
    df = engineer_features(df)
    df = create_labels(df)
    df = df.dropna(subset=FEATURE_COLS) #drop NaN rows, first 26 days wont have macd yet
    df = df.reset_index(drop=True)
    cutoff   = int(len(df) * 0.8) #80% data for training, 20% for testing
    train_df = df.iloc[:cutoff]
    test_df  = df.iloc[cutoff:]
    X_train = train_df[FEATURE_COLS]
    y_train = train_df['label']
    X_test  = test_df[FEATURE_COLS]
    y_test  = test_df['label']
    #compute_sample_weight tells XGBoost to pay more attention to rare classes (Buy/Sell)
    #without this the model just learns to always say Hold because its the most common label
    sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)
    model = xgb.XGBClassifier(
        n_estimators=200,   #200 trees, more than before for better accuracy
        max_depth=4,        #each tree asks 4 yes/no questions
        learning_rate=0.05, #slower learning = more careful = generally more accurate
        eval_metric='mlogloss'
    )
    model.fit(X_train, y_train, sample_weight=sample_weights)
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions, target_names=['Sell', 'Hold', 'Buy']))
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    print("Model trained and saved.")

def get_signals():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    df = load_data()
    df = engineer_features(df)
    df = df.dropna(subset=FEATURE_COLS)
    latest_rows = df.groupby('ticker').tail(1)
    X           = latest_rows[FEATURE_COLS]
    predictions = model.predict(X)
    results = latest_rows[['ticker', 'date', 'close']].copy()
    results['Signal'] = predictions
    results['Signal'] = results['Signal'].map({0: 'SELL', 1: 'HOLD', 2: 'BUY'})
    results = results.reset_index(drop=True)
    return results

if __name__ == "__main__":
    train()
    print(get_signals())