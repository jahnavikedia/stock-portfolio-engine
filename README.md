# Stock Portfolio Suggestion Engine

A Streamlit web application that turns a dollar amount and one or two
investing strategies into a concrete equal-weight portfolio. Live prices come
from Yahoo Finance via `yfinance` (no API key required). The dashboard shows
the resulting holdings, the live portfolio value with one-click refresh, a
five-day weekly trend chart with an S&P 500 benchmark overlay, sector
diversification, risk metrics, CSV export, and named-portfolio save/load.
All persistence is plain JSON files on local disk — no database.

---

## Team Members

Group: **Stock Portfolio Suggestion Engine**

| # | Name             | SJSU ID    | Role                                                    |
|---|------------------|------------|---------------------------------------------------------|
| 1 | Lam Nguyen       | 018229432  | Allocation Engine & Strategy Mapping                    |
| 2 | Jahnavi Kedia    | 018282368  | Streamlit UI & Visualization                            |
| 3 | Nishan Paudel    | 018280561  | Market Data Integration & Portfolio Valuation           |
| 4 | Harishita Gupta  | 018323331  | Persistence, Testing & Documentation                    |

Work was split into four equal-sized vertical slices:

- **Lam (Allocation Engine & Strategy Mapping)** — owns
  [engine/strategies.py](engine/strategies.py) (5 strategies × 5 tickers each,
  combine/dedupe logic, validation) and [engine/allocator.py](engine/allocator.py)
  (equal-weight allocation, whole-share rounding, residual-cash tracking).
  Wrote the matching unit tests in
  [tests/test_strategies.py](tests/test_strategies.py) and
  [tests/test_allocator.py](tests/test_allocator.py).
- **Jahnavi (Streamlit UI & Visualization)** — owns [app.py](app.py): sidebar
  inputs and validation flow, holdings table, live-value metric card, the 5-day
  Plotly trend chart with SPY benchmark and reference line, sector pie chart,
  risk metrics card, CSV download button, and the strategy-comparison toggle.
- **Nishan (Market Data Integration & Portfolio Valuation)** — owns
  [engine/data_provider.py](engine/data_provider.py) (the only module that
  talks to `yfinance`: live prices, history, sector lookup, SPY benchmark) and
  [engine/portfolio.py](engine/portfolio.py) (5-day historical valuation,
  benchmark normalization, risk metrics). Wrote the matching tests in
  [tests/test_portfolio.py](tests/test_portfolio.py).
- **Harishita (Persistence, Testing & Documentation)** — owns
  [storage/snapshot_store.py](storage/snapshot_store.py) (per-portfolio daily
  value snapshots, capped at 5) and
  [storage/portfolio_store.py](storage/portfolio_store.py) (named-portfolio
  save/load). Wrote the storage tests in
  [tests/test_snapshot_store.py](tests/test_snapshot_store.py) and authored
  [README.md](README.md), [TEST_CASES.md](TEST_CASES.md),
  [SLIDES.md](SLIDES.md), and [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

---

## For the Grader (Submission Notes)

This section maps the project to the official term-project submission rules:

- **The 10 detailed test cases live in [TEST_CASES.md](TEST_CASES.md).**
  They are numbered Test Case 1 through Test Case 10 and use a uniform
  Purpose / Setup / Steps / Expected Result template.
- **Only the test cases will be graded.** Every case in
  [TEST_CASES.md](TEST_CASES.md) is reproducible from a freshly cloned repo.
  No hidden state, no environment variables, no API keys.
- **The instructions are detailed enough for any grader to test the project**
  even without prior context. Every step lists exact button labels, the exact
  values to type, and the exact text or visual element to look for.
- **Setup instructions are below** under *Setup*. They are copy-paste ready.
- **The matching demo walkthrough** for the 10 test cases (used for the video
  recording) is in [DEMO_SCRIPT.md](DEMO_SCRIPT.md).
- **The 5-slide presentation content** (team, architecture, features, extras,
  challenges) is in [SLIDES.md](SLIDES.md).

---

## Setup

Requires only **Python 3.11 or newer** and an internet connection (for live
prices). No Docker, no Poetry, no database.

```bash
git clone https://github.com/jahnavikedia/stock-portfolio-engine.git
cd stock-portfolio-engine

# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate            # Windows PowerShell

# install pinned dependencies
pip install -r requirements.txt

# launch the dashboard
streamlit run app.py
```

The dashboard opens automatically at **http://localhost:8501**. Press
`Ctrl + C` in the terminal to stop the app.

**Tested on:** Python 3.11 / 3.13 — macOS, Windows, and Linux.

### Run the automated test suite (optional)

```bash
pytest
```

Expected output: **30 passed**. The test suite is fully offline — it does not
hit the network, so it works on any machine after `pip install`.

---

## How to Use the App

1. In the **left sidebar**, enter an **Investment Amount (USD)** of at least
   `$5000`.
2. In **Investment Strategy**, pick **1 or 2** of: Ethical Investing,
   Growth Investing, Index Investing, Quality Investing, Value Investing.
3. Click **Build Portfolio**.
4. The main panel shows:
   - The **Holdings** table (Ticker, Strategy, Price, Shares, Cost, % of Portfolio)
   - **Initial Investment**, **Total Invested**, **Residual Cash** metrics
   - A **Download Holdings CSV** button
   - A **Live Total Value** metric with a **Refresh Live Prices** button
   - The **5-day Weekly Trend** chart with a horizontal initial-investment
     reference line and an S&P 500 (SPY) benchmark overlay
   - A **Risk Metrics** card (5-day return, daily volatility, max drawdown)
   - A **Sector Diversification** pie chart
   - A **Strategy Mix** bar chart (or side-by-side comparison if you toggled
     *Compare strategies side-by-side* with two strategies selected)
5. Save the portfolio under a name in the **Saved Portfolios** section, and
   reload it later from the dropdown.

---

## Features

### Core (from the spec)

- Investment amount input with hard `$5,000` minimum (validated; below-min
  shows a red error and blocks the build)
- Strategy multiselect that enforces **exactly 1 or 2** selections
- Five strategies, each mapped to **five tickers** (the spec requires at least
  three; we provide five)
- Equal-weight allocation with whole-share rounding and explicit residual-cash
  tracking
- Holdings output: which stocks were selected, how the money is divided
  (`$` and `%` columns)
- Up-to-the-second live portfolio value via `yfinance`, with a manual refresh
  button (60-second cache)
- Five-day weekly trend chart of the overall portfolio value, with a
  horizontal reference line at the initial investment

### Extras (improvements beyond spec)

- **S&P 500 (SPY) benchmark overlay** on the 5-day chart, normalized to start
  at the initial investment for an apples-to-apples comparison
- **Sector diversification pie chart** using `yfinance.Ticker.info`
  (unknowns labeled "Other")
- **CSV export** of the holdings table
- **Save / load named portfolios** to `data/portfolios.json`
- **Risk metrics card**: 5-day return, daily volatility, max drawdown
- **Strategy comparison mode**: when two strategies are selected, a side-by-
  side breakdown shows how each strategy contributed to the portfolio

---

## Strategy → Ticker Mapping

| Strategy           | Tickers                                  |
|--------------------|------------------------------------------|
| Ethical Investing  | AAPL, ADBE, MSFT, NSRGY, COST            |
| Growth Investing   | NVDA, TSLA, AMZN, GOOGL, META            |
| Index Investing    | VTI, IXUS, ILTB, VOO, QQQ                |
| Quality Investing  | V, MA, JNJ, PG, UNH                      |
| Value Investing    | BRK-B, JPM, WMT, KO, XOM                 |

When two strategies are selected, the app combines their pools by taking the
first three tickers from each (deduped by symbol), capped at six tickers
total.

---

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
            +-------------+              +-------------+
            |  yfinance   |              |  data/*.json|
            |  (Yahoo)    |              +-------------+
            +-------------+
```

Streamlit caches wrap the `data_provider` calls at the call site
(`@st.cache_data(ttl=60)` for live prices, `ttl=3600` for history and sector
data) to keep the request volume modest and the UI responsive.

---

## Project Layout

```
stock-portfolio-engine/
├── app.py                       # Streamlit entrypoint
├── engine/
│   ├── strategies.py            # Strategy → ticker mapping + descriptions
│   ├── allocator.py             # Equal-weight allocation (pure)
│   ├── data_provider.py         # yfinance wrapper
│   └── portfolio.py             # Current value + 5-day historical valuation
├── storage/
│   ├── snapshot_store.py        # Daily portfolio-value snapshots → JSON
│   └── portfolio_store.py       # Save/load named portfolios → JSON
├── tests/
│   ├── test_allocator.py
│   ├── test_strategies.py
│   ├── test_portfolio.py
│   └── test_snapshot_store.py
├── data/                        # gitignored; created at runtime
├── requirements.txt
├── README.md                    # this file
├── TEST_CASES.md                # the 10 graded test cases
├── SLIDES.md                    # 5-slide presentation content
├── DEMO_SCRIPT.md               # 15-min demo walkthrough script
└── .gitignore
```

---

## Troubleshooting

- **"Could not fetch live prices from yfinance."** — Yahoo Finance occasionally
  rate-limits or returns transient errors. Click **Refresh Live Prices**, or
  wait 30 seconds and click **Build Portfolio** again. Make sure you are on a
  network that allows outbound HTTPS to `query2.finance.yahoo.com`.
- **Streamlit will not start / "address already in use"** — another instance
  is already on port 8501. Stop it with `Ctrl + C`, or run on a different
  port: `streamlit run app.py --server.port 8502`.
- **Saved portfolios disappear** — they are persisted to `data/portfolios.json`,
  which is intentionally git-ignored. Deleting `data/` clears all saved
  portfolios and snapshots.
