# Demo Script — Part b (15 minutes)

This script walks the grader through the 10 test cases from
[TEST_CASES.md](TEST_CASES.md), end to end. **Total target: 15 minutes**,
which is Part b of the 20-minute term-project video. Part a (the 5-minute
slide deck) is scripted in [SLIDES.md](SLIDES.md).

> **Pacing:** ~30 seconds intro + 10 test cases at ~1 minute 20 seconds each
> + ~30 seconds outro = ~14 minutes 20 seconds total. The minute-by-minute
> markers below give you a 15-minute hard cap.

| Segment        | Time budget   |
|----------------|---------------|
| Intro          | 0:00 – 0:30   |
| Test Case 1    | 0:30 – 1:50   |
| Test Case 2    | 1:50 – 3:10   |
| Test Case 3    | 3:10 – 4:30   |
| Test Case 4    | 4:30 – 5:50   |
| Test Case 5    | 5:50 – 7:10   |
| Test Case 6    | 7:10 – 8:30   |
| Test Case 7    | 8:30 – 9:50   |
| Test Case 8    | 9:50 – 11:10  |
| Test Case 9    | 11:10 – 12:30 |
| Test Case 10   | 12:30 – 14:00 |
| Outro          | 14:00 – 15:00 |

---

## Intro (0:00 – 0:30)

> "Welcome to the demo of the Stock Portfolio Suggestion Engine. The slides
> covered the architecture and features. For the next fifteen minutes I'll
> walk through each of the ten test cases from `TEST_CASES.md`, in order.
> The app is already running at `localhost:8501` after `streamlit run app.py`."

---

## Test Case 1: Minimum investment, single strategy (0:30 – 1:50)

> "Test Case 1 verifies the smallest valid investment with a single strategy.
> I enter `5000` for Investment Amount, pick only `Index Investing`, and
> click `Build Portfolio`. As you can see, the holdings table shows exactly
> five rows — VTI, IXUS, ILTB, VOO, and QQQ — and the Strategy column shows
> `Index Investing` for every row. Each Cost is roughly one thousand dollars,
> which is the equal-weight target of five thousand divided by five.
> `Total Invested` plus `Residual Cash` reconciles back to five thousand
> exactly. The 5-day chart, sector pie, and risk card all populate below."

---

## Test Case 2: Below-minimum rejected (1:50 – 3:10)

> "Test Case 2 verifies the five-thousand-dollar minimum is enforced. I change
> the amount to `4999` and click Build Portfolio. As you can see, a red error
> banner reads `Minimum investment is $5000`. No holdings table, value
> metric, or chart is rendered, and the sidebar inputs remain editable so the
> user can correct the amount. This validation lives in
> `engine/allocator.py` so it's enforced both in the UI and in unit tests."

---

## Test Case 3: No strategy selected (3:10 – 4:30)

> "Test Case 3 verifies the lower bound on strategy selection. I raise the
> amount back to `10000`, then remove all strategy pills from the multiselect.
> I click Build Portfolio. As you can see, a red banner appears reading
> `Select 1 or 2 strategies`, and no portfolio is built. This is the
> zero-strategies branch of the validator."

---

## Test Case 4: More than 2 strategies blocked (4:30 – 5:50)

> "Test Case 4 verifies the upper bound. I click Growth Investing — one
> selected. I click Value Investing — two selected. I open the multiselect
> again and try to click a third, Quality Investing. As you can see, the
> third click has no effect. The Streamlit multiselect is configured with
> `max_selections=2`, so the user cannot construct an invalid selection in
> the first place. To pick a different second strategy, you'd remove an
> existing pill first."

---

## Test Case 5: Two strategies combined (5:50 – 7:10)

> "Test Case 5 verifies combining two strategies. I enter `20000`, pick
> Ethical Investing plus Quality Investing, and click Build. As you can see,
> the holdings table shows at most six rows, all unique. The Strategy column
> tags each row with whichever strategy contributed it. We take the first
> three tickers from each strategy and dedupe by symbol — that's the
> `combine_tickers` function in `engine/strategies.py`. Each Cost is roughly
> twenty thousand divided by the row count."

---

## Test Case 6: Large investment, single strategy (7:10 – 8:30)

> "Test Case 6 verifies the allocator scales to a large amount. I enter
> `100000`, pick only Growth Investing, and click Build. NVDA, TSLA, AMZN,
> GOOGL, and META each get roughly twenty thousand dollars of exposure. As
> you can see, the cheaper tickers have higher share counts and the more
> expensive ones have lower share counts — share counts are inversely
> proportional to price. Residual cash stays well below the highest single
> share price, which is what you'd expect from whole-share rounding."

---

## Test Case 7: Live refresh updates value (8:30 – 9:50)

> "Test Case 7 verifies the live refresh. The Live Total Value card here
> shows the value computed during the last build. I click Refresh Live
> Prices — that clears the sixty-second cache and forces yfinance to
> requery. As you can see, the value redraws and the delta line against the
> initial investment is recomputed. If markets are open and prices have
> moved, the number changes. If we're inside the same minute, it stays
> equal — that's the documented cache window."

---

## Test Case 8: 5-day chart with reference line (9:50 – 11:10)

> "Test Case 8 verifies the weekly-trend chart. Scrolling down, you can see
> the chart with five data points along the X-axis, each labeled with a
> recent trading-day date. The dotted gray horizontal line is the initial
> investment reference, annotated `Initial: $10,000`. The orange dotted line
> is the S&P 500 benchmark, normalized so it starts at the same value as our
> portfolio on the leftmost date — that lets you compare us against the
> market on the same axis. The legend distinguishes backfilled historical
> close points from recorded snapshots."

---

## Test Case 9: CSV export (11:10 – 12:30)

> "Test Case 9 verifies the CSV export. I scroll back up to the Holdings
> section and click Download Holdings CSV. The browser saves a file named
> `holdings.csv`. I'm opening it in a spreadsheet now. As you can see, the
> header row is `Ticker, Strategy, Price, Shares, Cost, % of Portfolio`, and
> the data row count matches the number of tickers in the on-screen table.
> Tickers, share counts, and costs all match exactly."

---

## Test Case 10: Save and load portfolio (12:30 – 14:00)

> "Test Case 10 verifies named-portfolio persistence. I build a portfolio
> with ten thousand dollars and Quality Investing, type `test1` into the
> Save-as-name field, and click Save current portfolio. A green toast
> confirms `Saved portfolio 'test1'`. Now I refresh the browser tab — full
> page reload. The dashboard returns to the empty state, but the
> Load-saved-portfolio dropdown now lists `test1`. I select it and click
> Load selected. A toast confirms the load. As you can see, the original
> tickers, share counts, and costs all reappear, and the live value, 5-day
> chart, sector pie, and risk metrics all repopulate. Persistence is just
> a JSON file at `data/portfolios.json`."

---

## Outro (14:00 – 15:00)

> "That covers all ten test cases. To recap: the Stock Portfolio Suggestion
> Engine takes a dollar amount of at least five thousand dollars and one or
> two investing strategies, equal-weight-allocates the dollars across the
> strategy's tickers, and shows you live valuation, a five-day trend with an
> S&P 500 benchmark overlay, sector diversification, risk metrics, CSV
> export, and named portfolio save and load. Setup is just `pip install` and
> `streamlit run`. The full source is at `github.com/jahnavikedia/stock-portfolio-engine`.
> Thanks for watching."
