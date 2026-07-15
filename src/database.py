import sqlite3
import pandas as pd
import downloader

def init_db():
    conn = sqlite3.connect("data/market.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            ticker      TEXT PRIMARY KEY,
            asset_type  TEXT,
            exchange    TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            ticker     TEXT    NOT NULL,
            date       TEXT    NOT NULL,
            open       REAL,
            high       REAL,
            low        REAL,
            close      REAL,
            adj_close  REAL,
            volume     INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)
    conn.commit()
    conn.close()

def save_prices(ticker, df):
    conn = sqlite3.connect("data/market.db")
    cursor = conn.cursor()

    for date, row in df.iterrows():
        # 1. turn `date` (a Timestamp) into a 'YYYY-MM-DD' string
        date_str = date.strftime("%Y-%m-%d")

        # 2. build the tuple of 8 values, in the same order as the columns below
        values = (ticker, date_str, row["open"], row["high"], row["low"], row["close"], row["adj_close"], row["volume"])

        # 3. run the insert for this one row
        cursor.execute("""
            INSERT OR REPLACE INTO prices
                (ticker, date, open, high, low, close, adj_close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, values)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    spy = downloader.get_prices("SPY")
    save_prices("SPY", spy)