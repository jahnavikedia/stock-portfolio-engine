# Test Cases

The following 10 tests are the grading rubric for this project. Run them in
order against the running Streamlit app (`streamlit run app.py`).

---

### Test Case 1: Minimum investment, single strategy
**Purpose:** Verify the smallest valid investment with one strategy produces a
complete equal-weight portfolio.
**Setup:** App is running, `data/portfolios.json` does not exist or is empty.
**Steps:**
  1. In the sidebar, enter `5000` for Investment Amount (USD).
  2. In Investment Strategy, pick only `Index Investing`.
  3. Click `Build Portfolio`.
**Expected Result:**
  - Holdings table shows 5 rows: VTI, IXUS, ILTB, VOO, QQQ.
  - Strategy column shows `Index Investing` for every row.
  - Each ticker's Cost is roughly `$1000` (the equal-weight target).
  - Residual Cash metric is shown and is less than the largest single share
    price among the five tickers.
  - "Total Invested + Residual Cash" sums to `$5,000.00`.

---

### Test Case 2: Below minimum rejected
**Purpose:** Confirm the $5,000 minimum is enforced.
**Setup:** App is running, no portfolio currently built.
**Steps:**
  1. Enter `4999` for Investment Amount.
  2. Pick any single strategy.
  3. Click `Build Portfolio`.
**Expected Result:**
  - Red error banner reads: `Minimum investment is $5000.`
  - No holdings table, value metric, or chart appears.
  - Sidebar inputs remain editable so the user can correct the amount.

---

### Test Case 3: No strategy selected
**Purpose:** Confirm the app blocks submission when no strategy is picked.
**Setup:** App is running, fresh page load.
**Steps:**
  1. Enter `10000` for Investment Amount.
  2. Leave Investment Strategy empty (no selections).
  3. Click `Build Portfolio`.
**Expected Result:**
  - Red error banner reads: `Select 1 or 2 strategies.`
  - No portfolio is built.

---

### Test Case 4: More than 2 strategies blocked
**Purpose:** Confirm the multiselect enforces an upper bound of 2.
**Setup:** App is running.
**Steps:**
  1. Enter `10000` for Investment Amount.
  2. In Investment Strategy, click two strategies (e.g., `Growth Investing` and
     `Value Investing`).
  3. Attempt to add a third strategy (e.g., `Quality Investing`).
**Expected Result:**
  - The multiselect prevents the third selection (Streamlit's
    `max_selections=2` blocks the click and shows a hint).
  - At most 2 strategies are ever selected at the same time.

---

### Test Case 5: Two strategies combined
**Purpose:** Verify combining two strategies caps tickers at 6 and dedupes.
**Setup:** App is running.
**Steps:**
  1. Enter `20000` for Investment Amount.
  2. Pick `Ethical Investing` AND `Quality Investing`.
  3. Click `Build Portfolio`.
**Expected Result:**
  - Holdings table contains at most 6 rows.
  - All ticker symbols are unique (no duplicates).
  - Each row's Strategy column shows the strategy that contributed it.
  - Each ticker's Cost is roughly `$20,000 / N` where N is the row count.
  - Residual Cash is shown and is less than the largest single share price.

---

### Test Case 6: Large investment, single strategy
**Purpose:** Verify allocation scales to a large amount with rounding behaving.
**Setup:** App is running.
**Steps:**
  1. Enter `100000` for Investment Amount.
  2. Pick only `Growth Investing`.
  3. Click `Build Portfolio`.
**Expected Result:**
  - Holdings table shows 5 rows: NVDA, TSLA, AMZN, GOOGL, META.
  - Each ticker's Cost is roughly `$20,000` (the equal-weight target).
  - Share counts are inversely proportional to price: cheaper tickers have
    more shares than expensive ones.
  - Residual Cash is strictly less than the highest share price among the
    five tickers.

---

### Test Case 7: Live refresh updates value
**Purpose:** Verify the manual refresh re-pulls live prices and updates value.
**Setup:** A portfolio has just been built (any strategy/amount).
**Steps:**
  1. Note the value shown under `Live Total Value`.
  2. Click `Refresh Live Prices`.
  3. Wait for the metric to redraw.
**Expected Result:**
  - The 60-second cache is cleared and yfinance is re-queried.
  - `Live Total Value` either changes (if prices moved) or stays equal (within
    one minute of the previous fetch — this is the documented cache window).
  - The delta (`+$X (+Y%)`) recomputes against the initial investment.

---

### Test Case 8: 5-day chart renders with reference line
**Purpose:** Verify the weekly-trend chart renders with all three series.
**Setup:** App is running with internet access.
**Steps:**
  1. Build any portfolio (e.g., `$10000` + `Index Investing`).
  2. Scroll to `Weekly Trend — 5-Day Portfolio Value`.
**Expected Result:**
  - Line chart shows 5 data points along the X-axis (dates).
  - Y-axis shows portfolio value in dollars.
  - A dotted horizontal reference line is drawn at the initial investment with
    a label like `Initial: $10,000`.
  - A second dotted line labeled `S&P 500 (SPY) benchmark` overlays the chart,
    starting at the same initial value.
  - Legend distinguishes `Backfilled (historical close)` from
    `Snapshot (recorded)` and the SPY benchmark.

---

### Test Case 9: CSV export
**Purpose:** Verify the Download Holdings CSV button produces a valid file.
**Setup:** A portfolio has been built.
**Steps:**
  1. Click `Download Holdings CSV`.
  2. Save the file and open it in a spreadsheet (Excel, Numbers, Google
     Sheets) or a text editor.
**Expected Result:**
  - File downloads as `holdings.csv`.
  - First row is a header: `Ticker,Strategy,Price,Shares,Cost,% of Portfolio`.
  - Number of data rows equals the number of tickers shown in the UI table.
  - Ticker symbols, share counts, and costs match the on-screen values.

---

### Test Case 10: Save and load portfolio
**Purpose:** Verify named portfolios persist across page refreshes.
**Setup:** App is running with internet access.
**Steps:**
  1. Build a portfolio: enter `$10000`, pick `Quality Investing`, click
     `Build Portfolio`.
  2. In the sidebar `Saved Portfolios` section, type `test1` into the
     `Save as name` field.
  3. Click `Save current portfolio`.
  4. Refresh the browser tab (`Cmd+R` / `Ctrl+R`).
  5. In the sidebar, choose `test1` from the `Load saved portfolio` dropdown.
  6. Click `Load selected`.
**Expected Result:**
  - After save: a green toast confirms `Saved portfolio 'test1'.`
  - After refresh: `test1` appears in the dropdown.
  - After load: a toast confirms `Loaded portfolio 'test1'.`
  - Holdings table reappears with the same tickers, share counts, and costs
    as before the refresh.
  - Live value metric, 5-day chart, sector pie, and risk metrics all repopulate.
