import pandas as pd
import yfinance as yf

def get_prices(ticker, start="2014-01-01"):
    # 1. fetch daily data for `ticker` from `start` to today, using yfinance
    df = yf.download(ticker, start, auto_adjust=False, multi_level_index=False) 

    # 2. if nothing came back (bad ticker / no internet), handle it
    #    (return None or raise — your choice; retries come later)
    if df.empty:
       raise ValueError(f"No data returned for ticker '{ticker}'")

    # 3. tidy the frame:
    #    - rename columns to lowercase snake_case (e.g. "Adj Close" -> "adj_close")
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_", regex=False)
    #    - ensure the index is a real datetime, sorted oldest -> newest
    df = df.sort_index(ascending=True)

    # 4. return the cleaned DataFrame
    return df

if __name__ == "__main__":
    spy = get_prices("SPY")
    print(spy.head())
    print(spy.columns)