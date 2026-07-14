import sqlite3
import pandas as pd

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

if __name__ == "__main__":
    init_db()