"""Portfolio valuation: current value and 5-day historical valuation."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import pandas as pd


def _q2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def historical_values(
    holdings: pd.DataFrame,
    history: pd.DataFrame,
    residual_cash: Decimal,
    n_days: int = 5,
) -> pd.DataFrame:
    """Compute portfolio value at the close of each of the last n trading days.

    holdings: DataFrame with at least Ticker and Shares columns.
    history: DataFrame indexed by date with one column per ticker (close prices).
    residual_cash: leftover cash from the initial allocation, added at every
                   point so the chart matches the real total.

    Returns a DataFrame with columns ['date', 'value'] sorted ascending.
    """
    if history is None or history.empty or holdings is None or holdings.empty:
        return pd.DataFrame(columns=["date", "value"])

    hist = history.tail(n_days).copy()
    shares = {row["Ticker"]: int(row["Shares"]) for _, row in holdings.iterrows()}

    rows = []
    for idx, day_prices in hist.iterrows():
        total = Decimal("0")
        for ticker, qty in shares.items():
            if ticker not in day_prices.index:
                continue
            price = day_prices.get(ticker)
            if price is None or pd.isna(price):
                continue
            total += Decimal(str(float(price))) * Decimal(qty)
        total += residual_cash
        d = idx.date() if hasattr(idx, "date") else idx
        rows.append({"date": d, "value": float(_q2(total))})

    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def benchmark_curve(
    benchmark_close: pd.Series,
    initial_value: float,
    n_days: int = 5,
) -> pd.DataFrame:
    """Normalize a benchmark close series so its first point equals initial_value.

    Returns columns ['date', 'value'].
    """
    if benchmark_close is None or benchmark_close.empty:
        return pd.DataFrame(columns=["date", "value"])
    series = benchmark_close.dropna().tail(n_days)
    if series.empty:
        return pd.DataFrame(columns=["date", "value"])
    base = float(series.iloc[0])
    if base == 0:
        return pd.DataFrame(columns=["date", "value"])
    scale = initial_value / base
    rows = []
    for idx, price in series.items():
        d = idx.date() if hasattr(idx, "date") else idx
        rows.append({"date": d, "value": round(float(price) * scale, 2)})
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def risk_metrics(values: pd.DataFrame) -> dict[str, float]:
    """Return total return %, daily volatility %, and max drawdown % over the
    given value series. Empty/short series produce zeros so the UI stays clean.
    """
    if values is None or values.empty or len(values) < 2:
        return {"return_pct": 0.0, "volatility_pct": 0.0, "max_drawdown_pct": 0.0}

    v = values["value"].astype(float).reset_index(drop=True)
    total_return = (v.iloc[-1] / v.iloc[0] - 1.0) * 100.0
    daily_returns = v.pct_change().dropna()
    volatility = float(daily_returns.std() * 100.0) if not daily_returns.empty else 0.0

    running_max = v.cummax()
    drawdowns = (v - running_max) / running_max
    max_dd = float(drawdowns.min() * 100.0)

    return {
        "return_pct": round(float(total_return), 2),
        "volatility_pct": round(volatility, 2),
        "max_drawdown_pct": round(max_dd, 2),
    }
