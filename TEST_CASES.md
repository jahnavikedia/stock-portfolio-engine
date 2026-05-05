# Test Cases — Grading Rubric

This document contains the **10 detailed test cases** that the grader will
run against the project. Each case follows a uniform
**Purpose / Setup / Steps / Expected Result** template so it can be executed
by anyone who has never seen the project before.

> **Per the term project instructions, only these 10 test cases will be
> graded. They cover every required and extra feature of the project.**

---

## Grader Setup (run once, before Test Case 1)

> You only need Python 3.11+ and an internet connection. There are no API
> keys, no databases, and no Docker images to build.

```bash
# 1. Clone the project and enter the directory
git clone https://github.com/jahnavikedia/stock-portfolio-engine.git
cd stock-portfolio-engine

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate            # Windows PowerShell

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. (Optional) Run the offline test suite to confirm install — should print "30 passed"
pytest

# 5. Launch the Streamlit dashboard
streamlit run app.py
```

A browser tab opens automatically at **http://localhost:8501**. If it does
not, open that URL manually. Press `Ctrl + C` in the terminal to stop the app
when you are done.

> If a test step says "fresh page", press `Cmd + R` (macOS) or `Ctrl + R`
> (Windows / Linux) to reload the tab. If a test step says "clear caches",
> click the three-dot menu in the upper-right of the Streamlit tab and choose
> "Clear cache".

---

## Test Case 1: Minimum investment, single strategy

**Purpose:** Confirm the smallest valid investment with one strategy produces
a complete equal-weight portfolio with all expected outputs.

**Setup:** App is running at `localhost:8501`. Fresh page load.

**Steps:**
  1. In the left sidebar, click the `Investment Amount (USD)` field and enter
     `5000`.
  2. In the `Investment Strategy (pick 1 or 2)` multiselect, click
     `Index Investing`. No other strategy should be selected.
  3. Click the red `Build Portfolio` button.

**Expected Result:**
  - The main panel renders a `Holdings` table with **exactly 5 rows**, in
    this order: `VTI`, `IXUS`, `ILTB`, `VOO`, `QQQ`.
  - The `Strategy` column shows `Index Investing` for every row.
  - Each row's `Cost` value is roughly `$1,000` (the equal-weight target of
    `$5,000 / 5`).
  - Three metric cards appear: `Initial Investment` showing `$5,000.00`,
    `Total Invested` showing the sum of the Cost column, and `Residual Cash`
    showing the leftover from whole-share rounding.
  - `Total Invested` plus `Residual Cash` equals `$5,000.00`.
  - A `Live Total Value` metric card and `Refresh Live Prices` button are
    visible below the holdings table.
  - The `Weekly Trend — 5-Day Portfolio Value` chart renders with a
    horizontal dotted reference line labeled `Initial: $5,000`.

---

## Test Case 2: Below-minimum investment is rejected

**Purpose:** Confirm the `$5,000` minimum is enforced and the portfolio is
not built when the amount is too small.

**Setup:** App is running. Fresh page load (or click `Refresh Live Prices`
after a previous build to reset state if needed).

**Steps:**
  1. In the sidebar, change `Investment Amount (USD)` to `4999`.
  2. In `Investment Strategy`, pick any single strategy
     (e.g., `Growth Investing`).
  3. Click `Build Portfolio`.

**Expected Result:**
  - A red error banner appears in the main panel reading
    **`Minimum investment is $5000.`**
  - **No** holdings table, value metric, chart, sector pie, or risk card is
    rendered.
  - The sidebar inputs remain editable so the user can correct the amount and
    retry.

---

## Test Case 3: No strategy selected is rejected

**Purpose:** Confirm the app blocks submission when zero strategies are
selected.

**Setup:** App is running. Fresh page load.

**Steps:**
  1. In the sidebar, set `Investment Amount (USD)` to `10000`.
  2. Make sure the `Investment Strategy` field is empty (no pills selected).
     If any are selected, click their `×` to remove them.
  3. Click `Build Portfolio`.

**Expected Result:**
  - A red error banner appears reading **`Select 1 or 2 strategies.`**
  - **No** holdings table, value metric, or chart is rendered.

---

## Test Case 4: More than 2 strategies is blocked at the input

**Purpose:** Confirm the multiselect enforces an upper bound of 2 strategies
so the user cannot submit an invalid selection.

**Setup:** App is running. Fresh page load.

**Steps:**
  1. Set `Investment Amount (USD)` to `10000`.
  2. In `Investment Strategy`, click `Growth Investing` (now 1 selected).
  3. Click `Value Investing` (now 2 selected).
  4. Open the multiselect dropdown again and attempt to click a third
     strategy, e.g. `Quality Investing`.

**Expected Result:**
  - The third strategy click has **no effect** — the multiselect refuses to
    add a third pill because `max_selections=2`.
  - At all times, **at most 2** strategy pills are visible in the multiselect.
  - To pick a different second strategy, the user must first remove an
    existing one by clicking its `×`.

---

## Test Case 5: Two strategies are combined and deduped

**Purpose:** Confirm that selecting two strategies produces a combined,
deduped portfolio capped at six tickers, with the contributing strategy
labeled per row.

**Setup:** App is running. Fresh page load.

**Steps:**
  1. Set `Investment Amount (USD)` to `20000`.
  2. In `Investment Strategy`, pick **both** `Ethical Investing` **and**
     `Quality Investing`.
  3. Click `Build Portfolio`.

**Expected Result:**
  - The `Holdings` table contains **at most 6 rows** (the cap).
  - All ticker symbols in the table are **unique** (no duplicate rows).
  - The `Strategy` column tags each row with whichever of the two strategies
    contributed it (a row is `Ethical Investing` *or* `Quality Investing`,
    not both).
  - Each row's `Cost` is roughly `$20,000 / N` where N is the number of rows
    in the table.
  - `Residual Cash` is shown and is **less than the highest single share
    price** in the table.

---

## Test Case 6: Large investment, single strategy

**Purpose:** Confirm allocation scales correctly to a large amount and that
share counts are inversely proportional to price.

**Setup:** App is running. Fresh page load.

**Steps:**
  1. Set `Investment Amount (USD)` to `100000`.
  2. In `Investment Strategy`, pick only `Growth Investing`.
  3. Click `Build Portfolio`.

**Expected Result:**
  - The `Holdings` table contains exactly 5 rows, in this order: `NVDA`,
    `TSLA`, `AMZN`, `GOOGL`, `META`.
  - Each row's `Cost` is roughly `$20,000` (the equal-weight target of
    `$100,000 / 5`).
  - Cheaper-priced tickers show **more shares** than expensive ones — for
    example, the row with the lowest `Price` will have the highest `Shares`
    count, and vice versa.
  - `Residual Cash` is **strictly less than** the highest single share price
    among the five rows.

---

## Test Case 7: Live refresh re-pulls prices and updates the value

**Purpose:** Confirm that the manual refresh clears the live-price cache and
updates the `Live Total Value` metric.

**Setup:** Build a portfolio first (any valid amount and strategy, e.g.
`$10000` + `Index Investing`). The `Live Total Value` card must already be
on screen.

**Steps:**
  1. Note the current value displayed in `Live Total Value`.
  2. Click the `Refresh Live Prices` button.
  3. Wait one to two seconds for the metric to redraw.

**Expected Result:**
  - The 60-second live-price cache is cleared and `yfinance` is re-queried
    for the current portfolio's tickers.
  - The `Live Total Value` either updates to a new value (if the market moved)
    or remains the same (if no movement happened in the cache window) — in
    either case the metric is visibly redrawn without an error.
  - The delta line under the metric (e.g. `+$123.45 (+1.23%)`) is recomputed
    against the original `Initial Investment`.
  - No red error banner appears.

---

## Test Case 8: Five-day chart renders with reference line and benchmark

**Purpose:** Confirm the weekly trend chart includes the portfolio line, a
horizontal initial-investment reference, and the SPY benchmark overlay.

**Setup:** Build a portfolio first using `$10000` + `Index Investing`.

**Steps:**
  1. Scroll down to the section titled
     `Weekly Trend — 5-Day Portfolio Value`.
  2. Hover over each line in the chart to inspect tooltips.

**Expected Result:**
  - The chart renders with **5 data points** along the X-axis (each labeled
    with a recent trading-day date).
  - The Y-axis shows portfolio value in U.S. dollars.
  - A **dotted gray horizontal line** is drawn at the initial-investment
    level, with an annotation reading approximately `Initial: $10,000`.
  - A **second line** appears, labeled `S&P 500 (SPY) benchmark` in the
    legend, normalized to start at the same `$10,000` value as the portfolio
    on the leftmost date.
  - The legend distinguishes `Backfilled (historical close)` (dashed) from
    `Snapshot (recorded)` (solid) and the SPY benchmark (dotted orange).

---

## Test Case 9: CSV export downloads a valid file

**Purpose:** Confirm the `Download Holdings CSV` button produces a file whose
contents match the on-screen holdings table exactly.

**Setup:** Build a portfolio first (e.g. `$10000` + `Quality Investing`). The
`Holdings` table must be visible.

**Steps:**
  1. Click the `Download Holdings CSV` button just below the holdings table.
  2. Save the resulting file (the browser will prompt or auto-download as
     `holdings.csv`).
  3. Open `holdings.csv` in any spreadsheet application (Excel, Numbers,
     Google Sheets) or in a text editor.

**Expected Result:**
  - A file named `holdings.csv` is downloaded.
  - The first row is a header:
    `Ticker,Strategy,Price,Shares,Cost,% of Portfolio`.
  - The number of data rows equals the number of tickers in the on-screen
    `Holdings` table (5 for a single strategy, up to 6 for two strategies).
  - For each row, the `Ticker`, `Shares`, and `Cost` values match what is
    displayed in the dashboard.

---

## Test Case 10: Save and load a named portfolio

**Purpose:** Confirm that a portfolio can be saved by name and reloaded after
a full page refresh, with all derived views (chart, sector pie, risk metrics)
repopulating.

**Setup:** App is running. Fresh page load.

**Steps:**
  1. Build a portfolio: enter `$10000`, pick `Quality Investing`, click
     `Build Portfolio`. Note the tickers and share counts in the table.
  2. In the sidebar `Saved Portfolios` section, type `test1` into the
     `Save as name` field.
  3. Click `Save current portfolio`.
  4. Refresh the browser tab (`Cmd + R` on macOS or `Ctrl + R` on Windows /
     Linux).
  5. After the page reloads, in the sidebar `Saved Portfolios` section,
     click the `Load saved portfolio` dropdown and choose `test1`.
  6. Click `Load selected`.

**Expected Result:**
  - Step 3 shows a green toast in the lower-right reading
    `Saved portfolio 'test1'.`.
  - After step 4, the main panel returns to the empty `Use the sidebar...`
    info banner, but the `Load saved portfolio` dropdown now lists `test1`.
  - Step 6 shows a green toast reading `Loaded portfolio 'test1'.`.
  - The `Holdings` table reappears with **the same tickers and share counts**
    as before the refresh.
  - `Live Total Value`, the `Weekly Trend — 5-Day Portfolio Value` chart, the
    `Sector Diversification` pie, the `Risk Metrics (last 5 trading days)`
    card, and the `Strategy Mix` bar chart all repopulate with values
    consistent with the loaded holdings.

---

## Coverage matrix

| Test | Spec requirement covered                                                       |
|------|--------------------------------------------------------------------------------|
| 1    | Min `$5,000`; strategy → tickers; equal-weight; "which stocks selected"        |
| 2    | Min-investment validation                                                      |
| 3    | "Pick one or two" lower bound (zero rejected)                                  |
| 4    | "Pick one or two" upper bound (three blocked)                                  |
| 5    | Two-strategy combination, dedupe, cap                                          |
| 6    | "How money is divided" with proportional share counts at scale                 |
| 7    | "Up-to-the-second" current value via Internet                                  |
| 8    | "Weekly trend — 5 days history of portfolio value" + benchmark + reference     |
| 9    | CSV export (extra feature)                                                     |
| 10   | Named portfolio save/load (extra feature) + persistence verification           |
