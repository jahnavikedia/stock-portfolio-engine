"""Strategy definitions and ticker mappings.

Pure module with no external dependencies. Each strategy maps to a list of
five tickers and a short description shown in the UI.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Strategy:
    name: str
    description: str
    tickers: tuple[str, ...]


STRATEGIES: dict[str, Strategy] = {
    "Ethical Investing": Strategy(
        name="Ethical Investing",
        description=(
            "Focuses on companies with strong environmental, social, and "
            "governance practices. Prioritizes responsible business conduct "
            "alongside long-term financial performance."
        ),
        tickers=("AAPL", "ADBE", "MSFT", "NSRGY", "COST"),
    ),
    "Growth Investing": Strategy(
        name="Growth Investing",
        description=(
            "Targets companies with above-average earnings and revenue growth. "
            "Accepts higher volatility in exchange for outsized capital "
            "appreciation potential."
        ),
        tickers=("NVDA", "TSLA", "AMZN", "GOOGL", "META"),
    ),
    "Index Investing": Strategy(
        name="Index Investing",
        description=(
            "Buys broad market index funds for diversified, low-cost exposure. "
            "Aims to match overall market returns rather than beat them."
        ),
        tickers=("VTI", "IXUS", "ILTB", "VOO", "QQQ"),
    ),
    "Quality Investing": Strategy(
        name="Quality Investing",
        description=(
            "Selects companies with durable competitive advantages, healthy "
            "balance sheets, and consistent profitability across market cycles."
        ),
        tickers=("V", "MA", "JNJ", "PG", "UNH"),
    ),
    "Value Investing": Strategy(
        name="Value Investing",
        description=(
            "Looks for established businesses trading below intrinsic value. "
            "Emphasizes margin of safety and reasonable valuation multiples."
        ),
        tickers=("BRK-B", "JPM", "WMT", "KO", "XOM"),
    ),
}


def list_strategies() -> list[str]:
    return list(STRATEGIES.keys())


def get_strategy(name: str) -> Strategy:
    if name not in STRATEGIES:
        raise KeyError(f"Unknown strategy: {name}")
    return STRATEGIES[name]


def combine_tickers(selected: list[str], max_total: int = 6) -> list[tuple[str, str]]:
    """Combine tickers from selected strategies.

    For a single strategy, returns all five of its tickers.
    For two strategies, takes the first three tickers of each (capped at six),
    deduping by ticker symbol while preserving the first-seen strategy label.

    Returns a list of (ticker, strategy_name) pairs.
    """
    if not selected:
        raise ValueError("At least one strategy must be selected.")
    if len(selected) > 2:
        raise ValueError("Select at most two strategies.")

    if len(selected) == 1:
        s = get_strategy(selected[0])
        return [(t, s.name) for t in s.tickers]

    per_strategy = max_total // 2
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for name in selected:
        s = get_strategy(name)
        for t in s.tickers[:per_strategy]:
            if t not in seen:
                result.append((t, s.name))
                seen.add(t)
        if len(result) >= max_total:
            break
    return result[:max_total]


def validate_selection(selected: list[str]) -> str | None:
    """Return None if valid, otherwise a user-facing error string."""
    if len(selected) == 0:
        return "Select 1 or 2 strategies."
    if len(selected) > 2:
        return "Select at most 2 strategies."
    for name in selected:
        if name not in STRATEGIES:
            return f"Unknown strategy: {name}"
    return None
