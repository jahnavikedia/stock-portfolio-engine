from decimal import Decimal
from datetime import datetime, timedelta

import pandas as pd
import pytest

from engine import portfolio


@pytest.fixture
def holdings_df():
    return pd.DataFrame([
        {"Ticker": "AAA", "Strategy": "S", "Price": 100.0, "Shares": 10, "Cost": 1000.0, "% of Portfolio": 50.0},
        {"Ticker": "BBB", "Strategy": "S", "Price": 50.0, "Shares": 20, "Cost": 1000.0, "% of Portfolio": 50.0},
    ])


@pytest.fixture
def history_df():
    dates = pd.to_datetime([
        "2026-04-28", "2026-04-29", "2026-04-30", "2026-05-01", "2026-05-04",
    ])
    return pd.DataFrame({
        "AAA": [100, 101, 99, 102, 105],
        "BBB": [50, 51, 49, 52, 55],
    }, index=dates)


def test_historical_values_basic(holdings_df, history_df):
    out = portfolio.historical_values(holdings_df, history_df, Decimal("0.00"), n_days=5)
    assert len(out) == 5
    expected_first = 10 * 100 + 20 * 50
    assert out["value"].iloc[0] == pytest.approx(expected_first)
    expected_last = 10 * 105 + 20 * 55
    assert out["value"].iloc[-1] == pytest.approx(expected_last)


def test_historical_values_includes_residual_cash(holdings_df, history_df):
    out = portfolio.historical_values(holdings_df, history_df, Decimal("123.45"), n_days=5)
    assert all(v >= 123.45 for v in out["value"])
    expected_first = 10 * 100 + 20 * 50 + 123.45
    assert out["value"].iloc[0] == pytest.approx(expected_first)


def test_historical_values_handles_empty():
    empty = pd.DataFrame()
    out = portfolio.historical_values(empty, empty, Decimal("0"))
    assert out.empty


def test_benchmark_curve_normalizes_to_initial():
    dates = pd.to_datetime(["2026-04-28", "2026-04-29", "2026-04-30", "2026-05-01", "2026-05-04"])
    series = pd.Series([400.0, 410.0, 405.0, 420.0, 430.0], index=dates)
    out = portfolio.benchmark_curve(series, initial_value=10000.0, n_days=5)
    assert len(out) == 5
    assert out["value"].iloc[0] == pytest.approx(10000.0, abs=0.5)
    assert out["value"].iloc[-1] > 10000.0


def test_benchmark_curve_empty_series():
    out = portfolio.benchmark_curve(pd.Series(dtype=float), 10000.0)
    assert out.empty


def test_risk_metrics_basic():
    df = pd.DataFrame({
        "date": pd.date_range("2026-04-28", periods=5),
        "value": [10000, 10100, 9900, 10200, 10500],
    })
    m = portfolio.risk_metrics(df)
    assert m["return_pct"] == pytest.approx(5.0, abs=0.01)
    assert m["volatility_pct"] > 0
    assert m["max_drawdown_pct"] <= 0


def test_risk_metrics_short_series():
    df = pd.DataFrame({"date": [pd.Timestamp("2026-05-01")], "value": [10000]})
    m = portfolio.risk_metrics(df)
    assert m == {"return_pct": 0.0, "volatility_pct": 0.0, "max_drawdown_pct": 0.0}
