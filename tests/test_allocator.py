from decimal import Decimal

import pandas as pd
import pytest

from engine import allocator


def test_validate_amount_minimum():
    assert allocator.validate_amount(5000) is None
    assert allocator.validate_amount(5000.01) is None
    err = allocator.validate_amount(4999.99)
    assert err is not None and "5000" in err


def test_validate_amount_non_numeric():
    assert allocator.validate_amount("abc") is not None


def test_allocate_equal_weight_basic():
    pairs = [("AAA", "Test"), ("BBB", "Test"), ("CCC", "Test"), ("DDD", "Test"), ("EEE", "Test")]
    prices = {"AAA": 100.0, "BBB": 200.0, "CCC": 50.0, "DDD": 80.0, "EEE": 25.0}
    df, residual = allocator.allocate(pairs, prices, 5000)
    assert list(df["Ticker"]) == ["AAA", "BBB", "CCC", "DDD", "EEE"]
    target = 1000.0
    assert df.loc[df.Ticker == "AAA", "Shares"].iloc[0] == 10
    assert df.loc[df.Ticker == "BBB", "Shares"].iloc[0] == 5
    assert df.loc[df.Ticker == "CCC", "Shares"].iloc[0] == 20
    assert df.loc[df.Ticker == "DDD", "Shares"].iloc[0] == 12
    assert df.loc[df.Ticker == "EEE", "Shares"].iloc[0] == 40
    invested = sum(df["Cost"])
    assert float(residual) == pytest.approx(5000 - invested, abs=0.01)
    assert all(df["% of Portfolio"] >= 0)


def test_allocate_residual_below_largest_share():
    pairs = [("X", "S"), ("Y", "S"), ("Z", "S")]
    prices = {"X": 333.33, "Y": 17.0, "Z": 91.5}
    df, residual = allocator.allocate(pairs, prices, 10000)
    largest_price = max(prices.values())
    assert float(residual) < largest_price


def test_allocate_below_minimum_raises():
    with pytest.raises(ValueError):
        allocator.allocate([("AAA", "Test")], {"AAA": 100.0}, 1000)


def test_allocate_skips_missing_prices():
    pairs = [("AAA", "S"), ("BBB", "S")]
    prices = {"AAA": 100.0}
    df, _ = allocator.allocate(pairs, prices, 5000)
    assert "BBB" not in df["Ticker"].values
    assert "AAA" in df["Ticker"].values


def test_allocate_skips_zero_price():
    pairs = [("AAA", "S"), ("BBB", "S")]
    prices = {"AAA": 100.0, "BBB": 0.0}
    df, _ = allocator.allocate(pairs, prices, 5000)
    assert "BBB" not in df["Ticker"].values


def test_allocate_no_tickers_raises():
    with pytest.raises(ValueError):
        allocator.allocate([], {}, 5000)


def test_current_value():
    df = pd.DataFrame([
        {"Ticker": "AAA", "Strategy": "S", "Price": 100.0, "Shares": 10, "Cost": 1000.0, "% of Portfolio": 50.0},
        {"Ticker": "BBB", "Strategy": "S", "Price": 50.0, "Shares": 20, "Cost": 1000.0, "% of Portfolio": 50.0},
    ])
    live = {"AAA": 110.0, "BBB": 55.0}
    val = allocator.current_value(df, live)
    assert val == Decimal("2200.00")


def test_percent_of_portfolio_sums_close_to_invested_fraction():
    pairs = [("AAA", "S"), ("BBB", "S")]
    prices = {"AAA": 100.0, "BBB": 100.0}
    df, residual = allocator.allocate(pairs, prices, 5000)
    total_pct = sum(df["% of Portfolio"])
    invested = sum(df["Cost"])
    assert total_pct == pytest.approx(invested / 5000.0 * 100.0, abs=0.05)
