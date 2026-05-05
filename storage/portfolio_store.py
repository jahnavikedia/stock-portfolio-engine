"""Save / load named portfolios to a single JSON file."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

PORTFOLIOS_PATH = os.path.join("data", "portfolios.json")


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _load_all(path: str = PORTFOLIOS_PATH) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def list_portfolio_names(path: str = PORTFOLIOS_PATH) -> list[str]:
    return sorted(_load_all(path).keys())


def save_portfolio(
    name: str,
    payload: dict,
    path: str = PORTFOLIOS_PATH,
) -> None:
    """Persist a portfolio under `name`.

    `payload` should include: amount, strategies, holdings (list of dicts),
    residual_cash, created_at (auto-filled if missing).
    """
    if not name or not name.strip():
        raise ValueError("Portfolio name cannot be empty.")
    name = name.strip()
    _ensure_parent(path)
    all_data = _load_all(path)
    payload = dict(payload)
    payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    payload["name"] = name
    all_data[name] = payload
    with open(path, "w") as f:
        json.dump(all_data, f, indent=2, default=str)


def load_portfolio(name: str, path: str = PORTFOLIOS_PATH) -> dict | None:
    return _load_all(path).get(name)


def delete_portfolio(name: str, path: str = PORTFOLIOS_PATH) -> bool:
    all_data = _load_all(path)
    if name in all_data:
        del all_data[name]
        with open(path, "w") as f:
            json.dump(all_data, f, indent=2, default=str)
        return True
    return False
