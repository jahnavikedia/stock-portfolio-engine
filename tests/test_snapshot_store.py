import json
import os

import pytest

from storage import snapshot_store, portfolio_store


@pytest.fixture
def tmp_snap_dir(tmp_path):
    d = tmp_path / "snapshots"
    d.mkdir()
    return str(d)


def test_load_empty(tmp_snap_dir):
    assert snapshot_store.load_snapshots("nope", base_dir=tmp_snap_dir) == []


def test_append_and_load(tmp_snap_dir):
    snapshot_store.append_snapshot("p1", 10000.0, on_date="2026-05-01", base_dir=tmp_snap_dir)
    snapshot_store.append_snapshot("p1", 10100.0, on_date="2026-05-02", base_dir=tmp_snap_dir)
    snaps = snapshot_store.load_snapshots("p1", base_dir=tmp_snap_dir)
    assert [s["date"] for s in snaps] == ["2026-05-01", "2026-05-02"]
    assert snaps[1]["value"] == 10100.0


def test_append_replaces_same_day(tmp_snap_dir):
    snapshot_store.append_snapshot("p1", 100.0, on_date="2026-05-01", base_dir=tmp_snap_dir)
    snapshot_store.append_snapshot("p1", 200.0, on_date="2026-05-01", base_dir=tmp_snap_dir)
    snaps = snapshot_store.load_snapshots("p1", base_dir=tmp_snap_dir)
    assert len(snaps) == 1
    assert snaps[0]["value"] == 200.0


def test_caps_at_five(tmp_snap_dir):
    for i, d in enumerate(["2026-04-28", "2026-04-29", "2026-04-30", "2026-05-01", "2026-05-02", "2026-05-03"]):
        snapshot_store.append_snapshot("p2", 1000.0 + i, on_date=d, base_dir=tmp_snap_dir)
    snaps = snapshot_store.load_snapshots("p2", base_dir=tmp_snap_dir)
    assert len(snaps) == 5
    assert snaps[0]["date"] == "2026-04-29"
    assert snaps[-1]["date"] == "2026-05-03"


def test_sanitizes_portfolio_id(tmp_snap_dir):
    snapshot_store.append_snapshot("../evil/path", 100.0, on_date="2026-05-01", base_dir=tmp_snap_dir)
    files = os.listdir(tmp_snap_dir)
    assert all(".." not in f and "/" not in f for f in files)


def test_portfolio_store_roundtrip(tmp_path):
    path = str(tmp_path / "portfolios.json")
    payload = {
        "amount": 10000.0,
        "strategies": ["Growth Investing"],
        "residual_cash": 12.34,
        "holdings": [{"Ticker": "NVDA", "Shares": 5}],
        "ticker_strategies": [["NVDA", "Growth Investing"]],
        "portfolio_id": "p-test",
    }
    portfolio_store.save_portfolio("test1", payload, path=path)
    assert "test1" in portfolio_store.list_portfolio_names(path=path)
    loaded = portfolio_store.load_portfolio("test1", path=path)
    assert loaded["amount"] == 10000.0
    assert loaded["holdings"][0]["Ticker"] == "NVDA"
    assert portfolio_store.delete_portfolio("test1", path=path) is True
    assert portfolio_store.list_portfolio_names(path=path) == []


def test_portfolio_store_rejects_empty_name(tmp_path):
    path = str(tmp_path / "portfolios.json")
    with pytest.raises(ValueError):
        portfolio_store.save_portfolio("   ", {"amount": 5000.0}, path=path)
