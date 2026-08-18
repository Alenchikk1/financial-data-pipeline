import time
from downloader import get_prices
from database import init_db, save_prices

TICKERS = ["SPY", "QQQ", "XLK", "XLF", "XLE", "TLT", "GLD"]

if __name__ == "__main__":
    init_db()
    for ticker in TICKERS:
        try:
            ticker_info = get_prices(ticker)
            save_prices(ticker, ticker_info)
            print(f"saved {ticker}")
        except Exception as e:
            print(f"FAILED {ticker}: {e}")
        time.sleep(2)