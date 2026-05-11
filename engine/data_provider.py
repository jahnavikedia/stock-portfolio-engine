"""yfinance wrapper.

This module is the only one that touches the network. Tests mock these
functions rather than calling them. Caching decorators (e.g. @st.cache_data)
are applied in app.py at the call site so unit tests can import freely.
"""

from __future__ import annotations

import logging
from datetime import date

import pandas as pd
import yfinance as yf

log = logging.getLogger(__name__)

BENCHMARK_TICKER = "SPY"


def fetch_current_prices(tickers: list[str]) -> dict[str, float]:
    """Return latest close price per ticker. Skips tickers that fail."""
    if not tickers:
        return {}
    out: dict[str, float] = {}
    try:
        data = yf.download(
            tickers=tickers,
            period="1d",
            interval="1d",
            progress=False,
            auto_adjust=False,
            group_by="ticker",
            threads=True,
        )
    except Exception as e:
        log.warning("yfinance download failed: %s", e)
        data = None

    if data is None or len(data) == 0:
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(period="5d")
                if not hist.empty:
                    out[t] = float(hist["Close"].dropna().iloc[-1])
            except Exception as e:
                log.warning("Per-ticker fallback failed for %s: %s", t, e)
        return out

    if len(tickers) == 1:
        t = tickers[0]
        try:
            close_series = data["Close"] if "Close" in data.columns else None
            if close_series is not None and not close_series.empty:
                out[t] = float(close_series.dropna().iloc[-1])
        except Exception as e:
            log.warning("Single-ticker parse failed for %s: %s", t, e)
        return out

    for t in tickers:
        try:
            close_series = data[t]["Close"].dropna()
            if not close_series.empty:
                out[t] = float(close_series.iloc[-1])
        except Exception:
            try:
                hist = yf.Ticker(t).history(period="5d")
                if not hist.empty:
                    out[t] = float(hist["Close"].dropna().iloc[-1])
            except Exception as e:
                log.warning("Could not fetch price for %s: %s", t, e)
    return out


def fetch_history(tickers: list[str], days: int = 7) -> pd.DataFrame:
    """Return a DataFrame of close prices indexed by date.

    Columns are tickers. We request a slightly wider window so callers can
    pick the trailing N trading days they need.
    """
    if not tickers:
        return pd.DataFrame()
    period = f"{max(days, 5)}d"
    try:
        data = yf.download(
            tickers=tickers,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=False,
            group_by="ticker",
            threads=True,
        )
    except Exception as e:
        log.warning("yfinance history download failed: %s", e)
        return pd.DataFrame()

    if data is None or len(data) == 0:
        return pd.DataFrame()

    if len(tickers) == 1:
        t = tickers[0]
        if isinstance(data.columns, pd.MultiIndex) and t in data.columns.get_level_values(0):
            close = data[t]["Close"] if "Close" in data[t].columns else None
        elif "Close" in data.columns:
            close = data["Close"]
        else:
            close = None
        if close is None:
            return pd.DataFrame()
        return pd.DataFrame({t: close}).dropna(how="all")

    closes = {}
    for t in tickers:
        try:
            closes[t] = data[t]["Close"]
        except Exception:
            continue
    if not closes:
        return pd.DataFrame()
    return pd.DataFrame(closes).dropna(how="all")


def fetch_benchmark_history(days: int = 7) -> pd.Series:
    df = fetch_history([BENCHMARK_TICKER], days=days)
    if df.empty or BENCHMARK_TICKER not in df.columns:
        return pd.Series(dtype=float)
    return df[BENCHMARK_TICKER].dropna()


def fetch_sector_map(tickers: list[str]) -> dict[str, str]:
    """Best-effort sector lookup. Unknowns get labeled 'Other'."""
    out: dict[str, str] = {}
    for t in tickers:
        sector = "Other"
        try:
            info = yf.Ticker(t).info or {}
            raw = info.get("sector") or info.get("category") or ""
            if isinstance(raw, str) and raw.strip():
                sector = raw.strip()
        except Exception as e:
            log.warning("Sector lookup failed for %s: %s", t, e)
        out[t] = sector
    return out


def today_iso() -> str:
    return date.today().isoformat()
