# 15-Minute Demo Script

This script walks the grader through the 10 test cases from `TEST_CASES.md`,
end to end, with a small intro and outro. Aim for ~1 minute 20 seconds per
test case.

---

## Intro (0:00 – 0:30)

> "Hi, this is the demo of the Stock Portfolio Suggestion Engine. I'll start
> the app with `streamlit run app.py` and then walk through each of the 10
> test cases in our `TEST_CASES.md`. The app is open in my browser at
> `localhost:8501`."

---

## Test Case 1: Minimum investment, single strategy (0:30 – 1:50)

> "Now I'll demonstrate Test Case 1: minimum investment with a single
> strategy. I enter `5000` for Investment Amount, pick `Index Investing` as
> the only strategy, and click `Build Portfolio`. As you can see, the
> holdings table shows VTI, IXUS, ILTB, VOO, and QQQ, each allocated roughly
> $1,000. The Residual Cash metric shows the leftover from whole-share
> rounding, and you can see Total Invested plus Residual Cash sums to
> $5,000."

---

## Test Case 2: Below minimum rejected (1:50 – 3:10)

> "Now I'll demonstrate Test Case 2: below-minimum rejected. I change the
> Investment Amount to `4999` and click `Build Portfolio`. As you can see, a
> red error appears: `Minimum investment is $5000`. No portfolio is built and
> the previous results are not affected."

---

## Test Case 3: No strategy selected (3:10 – 4:30)

> "Now I'll demonstrate Test Case 3: no strategy selected. I bump the amount
> back up to `10000`, clear all strategy selections, and click
> `Build Portfolio`. As you can see, the app shows `Select 1 or 2 strategies`
> and refuses to build a portfolio."

---

## Test Case 4: More than 2 strategies blocked (4:30 – 5:50)

> "Now I'll demonstrate Test Case 4: more than two strategies blocked. I pick
> `Growth Investing` and `Value Investing` — that's two. When I try to add
> `Quality Investing` as a third, the multiselect itself prevents the click
> because we set `max_selections=2`. As you can see, only two pills are
> selected at any time."

---

## Test Case 5: Two strategies combined (5:50 – 7:10)

> "Now I'll demonstrate Test Case 5: two strategies combined. I enter
> `20000`, pick `Ethical Investing` plus `Quality Investing`, and click
> Build. As you can see, the holdings table shows up to 6 unique tickers, the
> Strategy column tags each row with whichever strategy contributed it, and
> the costs are equally distributed across the deduped pool."

---

## Test Case 6: Large investment, single strategy (7:10 – 8:30)

> "Now I'll demonstrate Test Case 6: a large single-strategy investment. I
> enter `100000`, pick only `Growth Investing`, and click Build. As you can
> see, NVDA, TSLA, AMZN, GOOGL, and META each get roughly $20,000 of
> exposure. Cheaper tickers naturally show more shares than expensive ones,
> and the residual cash is well below the largest single share price."

---

## Test Case 7: Live refresh updates value (8:30 – 9:50)

> "Now I'll demonstrate Test Case 7: live refresh. The `Live Total Value`
> card currently shows the value just computed. I click `Refresh Live Prices`
> — that clears the 60-second cache and forces a re-pull from yfinance. As
> you can see, the value redraws and the delta against the initial
> investment is recalculated."

---

## Test Case 8: 5-day chart with reference line (9:50 – 11:10)

> "Now I'll demonstrate Test Case 8: the 5-day weekly trend chart. Scrolling
> down, you can see the line chart with five data points along the X-axis.
> The dotted gray line is the initial investment reference. The orange dotted
> line is the S&P 500 benchmark, normalized to start at the same value as our
> portfolio. The legend distinguishes backfilled historical points from
> recorded snapshots."

---

## Test Case 9: CSV export (11:10 – 12:30)

> "Now I'll demonstrate Test Case 9: CSV export. I scroll back up to the
> Holdings section and click `Download Holdings CSV`. The browser saves a
> `holdings.csv` file. I open it in [Excel / Numbers / a text editor]. As you
> can see, the header row is `Ticker, Strategy, Price, Shares, Cost,
> % of Portfolio`, and the row count matches the on-screen table."

---

## Test Case 10: Save and load portfolio (12:30 – 14:00)

> "Now I'll demonstrate Test Case 10: save and load. I build a portfolio with
> `$10000` and `Quality Investing`, type `test1` in the Save-as-name field,
> and click `Save current portfolio`. A green toast confirms the save. I
> refresh the browser tab. The dashboard is empty again, but the dropdown
> under `Saved Portfolios` now lists `test1`. I select it and click
> `Load selected`. As you can see, the original holdings, value, chart,
> sector pie, and risk metrics all reappear with the same numbers."

---

## Outro (14:00 – 15:00)

> "That covers all 10 test cases. To recap, the Stock Portfolio Suggestion
> Engine takes a dollar amount and one or two investing strategies and
> produces a fully equal-weighted portfolio with live valuation, a 5-day
> trend chart with an S&P 500 benchmark, sector and risk metrics, CSV
> export, and named portfolio persistence. The full source is on GitHub at
> `github.com/jahnavikedia/stock-portfolio-engine`. Thank you."
