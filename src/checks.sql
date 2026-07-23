-- ============================================================
-- Data sanity checks for the prices table
-- Run with:  sqlite3 data/market.db < src/checks.sql
-- ============================================================


-- Check 1: rows per ticker
-- Each ticker should have roughly the expected number of trading days.
SELECT ticker, COUNT(*) AS n_rows
FROM prices
GROUP BY ticker;


-- Check 2: duplicate (ticker, date) pairs
-- Should return nothing — the composite primary key prevents duplicates.
SELECT ticker, date, COUNT(*) AS n
FROM prices
GROUP BY ticker, date
HAVING COUNT(*) > 1;


-- Check 3: suspicious gaps in the date sequence
-- Normal spacing is 1 day (weekday) or 3 days (weekend).
-- Anything else (2, or 4+) is flagged for inspection.
-- Note: US market holidays legitimately produce 2- and 4-day gaps.
WITH gaps AS (
    SELECT
        ticker,
        date,
        LAG(date) OVER (PARTITION BY ticker ORDER BY date) AS prev_date
    FROM prices
)
SELECT
    ticker,
    date,
    prev_date,
    julianday(date) - julianday(prev_date) AS gap_days
FROM gaps
WHERE prev_date IS NOT NULL
  AND (gap_days > 3 OR gap_days = 2);


-- Check 4: extreme daily moves (|return| > 20%)
-- A real 20% daily move is a historic crash; usually it flags bad data.
-- Uses adj_close so dividends/splits don't create phantom moves.
WITH price_moves AS (
    SELECT
        ticker,
        date,
        adj_close,
        LAG(adj_close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
    FROM prices
)
SELECT
    ticker,
    date,
    adj_close,
    prev_close,
    (adj_close - prev_close) / prev_close AS daily_return
FROM price_moves
WHERE prev_close IS NOT NULL
  AND ABS( (adj_close - prev_close) / prev_close ) > 0.20;