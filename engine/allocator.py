"""Equal-weight allocation logic.

Pure module: takes tickers, a strategy label per ticker, current prices, and a
total dollar amount. Returns a holdings DataFrame and the residual cash from
whole-share rounding. No I/O, no network — fully unit-testable offline.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from math import floor

import pandas as pd

MIN_INVESTMENT_USD = Decimal("5000")


def _q2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_amount(amount: float | int | Decimal) -> str | None:
    try:
        a = Decimal(str(amount))
    except Exception:
        return "Investment amount must be a number."
    if a < MIN_INVESTMENT_USD:
        return f"Minimum investment is ${MIN_INVESTMENT_USD:.0f}."
    return None


def allocate(
    ticker_strategies: list[tuple[str, str]],
    prices: dict[str, float],
    total_dollars: float | int | Decimal,
) -> tuple[pd.DataFrame, Decimal]:
    """Equal-weight allocation across the given (ticker, strategy) pairs.

    Returns (holdings_df, residual_cash). The DataFrame columns are:
        Ticker | Strategy | Price | Shares | Cost | % of Portfolio
    Cost is in dollars; % is of the total investment.
    """
    if not ticker_strategies:
        raise ValueError("No tickers to allocate.")

    err = validate_amount(total_dollars)
    if err:
        raise ValueError(err)

    total = Decimal(str(total_dollars))
    n = len(ticker_strategies)
    target_per_ticker = total / Decimal(n)

    rows = []
    invested = Decimal("0")
    for ticker, strategy in ticker_strategies:
        if ticker not in prices:
            continue
        price = Decimal(str(prices[ticker]))
        if price <= 0:
            continue
        shares = floor(target_per_ticker / price)
        cost = price * Decimal(shares)
        invested += cost
        rows.append(
            {
                "Ticker": ticker,
                "Strategy": strategy,
                "Price": float(_q2(price)),
                "Shares": int(shares),
                "Cost": float(_q2(cost)),
            }
        )

    if not rows:
        raise ValueError("No valid prices supplied for any ticker.")

    df = pd.DataFrame(rows)
    if invested > 0:
        df["% of Portfolio"] = df["Cost"].apply(
            lambda c: float(_q2(Decimal(str(c)) / total * Decimal("100")))
        )
    else:
        df["% of Portfolio"] = 0.0

    residual = _q2(total - invested)
    return df, residual


def current_value(holdings: pd.DataFrame, live_prices: dict[str, float]) -> Decimal:
    """Current portfolio value from a holdings table and live prices."""
    total = Decimal("0")
    for _, row in holdings.iterrows():
        t = row["Ticker"]
        if t not in live_prices:
            continue
        total += Decimal(str(live_prices[t])) * Decimal(int(row["Shares"]))
    return _q2(total)
