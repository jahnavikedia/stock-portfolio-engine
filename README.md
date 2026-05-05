# Stock Portfolio Suggestion Engine

## Overview

The Stock Portfolio Suggestion Engine is a Streamlit dashboard that turns a
dollar amount and one or two investing strategies into a concrete equal-weight
portfolio. Live prices come from Yahoo Finance via `yfinance`, so no API key is
required. The app shows the resulting holdings, the current portfolio value
with a one-click refresh, a 5-day weekly trend chart with an S&P 500 benchmark
overlay, and risk metrics. Portfolios can be saved, loaded, and exported as
CSV. All data is persisted to local JSON files; there is no database.

## Team Members

- Member 1: [Name], [Role]
- Member 2: [Name], [Role]
- Member 3: [Name], [Role]
- Member 4: [Name], [Role]

## Setup

```bash
git clone https://github.com/jahnavikedia/stock-portfolio-engine.git
cd stock-portfolio-engine
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The first run opens the app at `http://localhost:8501`.

**Tested on:** Python 3.11, macOS / Windows / Linux.

## Run the tests

```bash
pytest
```

All tests run offline — no internet connection is required because the test
suite does not import `yfinance` from any path that performs network I/O.

## Features

### Core

- Investment amount input with hard $5,000 minimum
- Strategy multiselect with enforced 1-or-2 selection
- Five strategies, each mapped to five tickers:
  Ethical, Growth, Index, Quality, Value
- Equal-weight allocation with whole-share rounding and residual-cash tracking
- Holdings table: Ticker, Strategy, Price, Shares, Cost, % of Portfolio
- Live portfolio value with one-click refresh (60-second cache)
- Weekly trend — 5-day historical portfolio value line chart with a horizontal
  reference line at the initial investment

### Extras

- S&P 500 (SPY) benchmark overlay normalized to the initial investment
- Sector diversification pie chart (uses `yfinance.Ticker.info` sector field;
  unknowns labeled "Other")
- CSV export of the holdings table
- Save and load named portfolios to `data/portfolios.json`
- Risk metrics card: 5-day return, daily volatility, max drawdown
- Strategy comparison mode: side-by-side allocation breakdown when two
  strategies are selected

## Architecture

```
                    +----------------------+
                    |        User          |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Streamlit UI       |
                    |   (app.py)           |
                    +----------+-----------+
                               |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
+---------------+      +---------------+      +-----------------+
| strategies.py |      |  allocator.py |      |  portfolio.py   |
|  (mapping)    |      | (equal weight)|      | (5-day values,  |
|               |      |               |      |  risk metrics)  |
+-------+-------+      +-------+-------+      +--------+--------+
        |                      |                       |
        +----------+-----------+--------+--------------+
                   |                    |
                   v                    v
        +----------------------+   +-------------------------+
        |  data_provider.py    |   |  storage/               |
        |  (yfinance wrapper)  |   |   snapshot_store.py     |
        |                      |   |   portfolio_store.py    |
        +----------+-----------+   +-----------+-------------+
                   |                           |
                   v                           v
            +-------------+              +------------+
            |  yfinance   |              |  data/*.json|
            |  (Yahoo)    |              +------------+
            +-------------+
```

## Project layout

```
stock-portfolio-engine/
├── app.py                   # Streamlit entrypoint
├── engine/
│   ├── strategies.py        # Strategy → ticker mapping + descriptions
│   ├── allocator.py         # Equal-weight allocation (pure)
│   ├── data_provider.py     # yfinance wrapper
│   └── portfolio.py         # Current value + 5-day historical valuation
├── storage/
│   ├── snapshot_store.py    # Daily portfolio-value snapshots → JSON
│   └── portfolio_store.py   # Save/load named portfolios → JSON
├── tests/                   # pytest, fully offline
├── data/                    # gitignored; created at runtime
├── requirements.txt
├── README.md
├── TEST_CASES.md
├── SLIDES.md
└── DEMO_SCRIPT.md
```
