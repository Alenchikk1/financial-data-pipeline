import numpy as np
import sqlite3
import pandas as pd

def add_returns(df):
    df["simple_return"] = df["adj_close"].pct_change()
    df["log_return"] = np.log(df["adj_close"] / df["adj_close"].shift(1))
    return df

def resample_returns(df, period):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    return df["log_return"].resample(period).sum()

def rolling_volatility(df, window=21):
    return df["log_return"].rolling(window).std() * np.sqrt(252)

def max_drawdown(df):
    wealth = (1+df['simple_return']).cumprod()
    peak = wealth.cummax()
    drawdown = (wealth-peak)/peak
    return drawdown.min()

if __name__ == "__main__":
    conn = sqlite3.connect("data/market.db")
    spy = pd.read_sql_query(
        "SELECT * FROM prices WHERE ticker = 'SPY' ORDER BY date", conn
    )
    conn.close()

    spy = add_returns(spy)
    print(spy[["date", "adj_close", "simple_return", "log_return"]].head())  # daily table

    weekly = resample_returns(spy, "W")
    print(weekly.head())   # weekly Series — just print it directly

    vol = rolling_volatility(spy)
    print(vol.tail())

    print(max_drawdown(spy))