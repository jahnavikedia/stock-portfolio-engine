"""Persist daily portfolio-value snapshots to JSON.

One file per portfolio, capped at the most recent 5 trading-day entries.
"""

from __future__ import annotations

import json
import os
from datetime import date

SNAPSHOTS_DIR = os.path.join("data", "snapshots")
MAX_SNAPSHOTS = 5


def _path(portfolio_id: str) -> str:
    safe = "".join(c for c in portfolio_id if c.isalnum() or c in ("-", "_"))
    if not safe:
        safe = "default"
    return os.path.join(SNAPSHOTS_DIR, f"{safe}.json")


def _ensure_dir(base_dir: str = SNAPSHOTS_DIR) -> None:
    os.makedirs(base_dir, exist_ok=True)


def load_snapshots(portfolio_id: str, base_dir: str = SNAPSHOTS_DIR) -> list[dict]:
    """Return list of {'date': 'YYYY-MM-DD', 'value': float} sorted ascending."""
    path = os.path.join(base_dir, os.path.basename(_path(portfolio_id)))
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    cleaned = [
        {"date": str(item["date"]), "value": float(item["value"])}
        for item in data
        if isinstance(item, dict) and "date" in item and "value" in item
    ]
    cleaned.sort(key=lambda r: r["date"])
    return cleaned


def append_snapshot(
    portfolio_id: str,
    value: float,
    on_date: str | None = None,
    base_dir: str = SNAPSHOTS_DIR,
) -> list[dict]:
    """Append today's value (or `on_date`) to the snapshot file.

    If a snapshot for the same date already exists, it is replaced.
    Trims to the most recent MAX_SNAPSHOTS entries.
    """
    _ensure_dir(base_dir)
    snaps = load_snapshots(portfolio_id, base_dir=base_dir)
    d = on_date or date.today().isoformat()
    snaps = [s for s in snaps if s["date"] != d]
    snaps.append({"date": d, "value": float(value)})
    snaps.sort(key=lambda r: r["date"])
    snaps = snaps[-MAX_SNAPSHOTS:]
    path = os.path.join(base_dir, os.path.basename(_path(portfolio_id)))
    with open(path, "w") as f:
        json.dump(snaps, f, indent=2)
    return snaps


def clear_snapshots(portfolio_id: str, base_dir: str = SNAPSHOTS_DIR) -> None:
    path = os.path.join(base_dir, os.path.basename(_path(portfolio_id)))
    if os.path.exists(path):
        os.remove(path)
