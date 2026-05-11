"""Stock Portfolio Suggestion Engine — Streamlit dashboard.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import io
import logging
import uuid
from datetime import date, timedelta
from decimal import Decimal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import allocator, data_provider, portfolio, strategies
from storage import portfolio_store, snapshot_store

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

st.set_page_config(
    page_title="Stock Portfolio Suggestion Engine",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)


# ---------- cached wrappers around the data provider ----------

@st.cache_data(ttl=60)
def cached_current_prices(tickers: tuple[str, ...]) -> dict[str, float]:
    return data_provider.fetch_current_prices(list(tickers))


@st.cache_data(ttl=3600)
def cached_history(tickers: tuple[str, ...], days: int = 7) -> pd.DataFrame:
    return data_provider.fetch_history(list(tickers), days=days)


@st.cache_data(ttl=3600)
def cached_benchmark(days: int = 7) -> pd.Series:
    return data_provider.fetch_benchmark_history(days=days)


@st.cache_data(ttl=3600)
def cached_sector_map(tickers: tuple[str, ...]) -> dict[str, str]:
    return data_provider.fetch_sector_map(list(tickers))


# ---------- session state setup ----------

def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("holdings", None)        # pd.DataFrame
    ss.setdefault("residual_cash", None)   # Decimal
    ss.setdefault("amount", 5000.0)
    ss.setdefault("selected_strategies", [])
    ss.setdefault("portfolio_id", None)
    ss.setdefault("ticker_strategies", None)
    ss.setdefault("compare_mode", False)
    ss.setdefault("error", None)


def _reset_portfolio() -> None:
    for k in ("holdings", "residual_cash", "portfolio_id", "ticker_strategies"):
        st.session_state[k] = None


# ---------- sidebar ----------

def render_sidebar() -> dict:
    st.sidebar.title("Build Your Portfolio")

    amount = st.sidebar.number_input(
        "Investment Amount (USD)",
        min_value=0.0,
        value=float(st.session_state.get("amount", 5000.0)),
        step=500.0,
        help="Minimum investment is $5,000.",
        format="%.2f",
    )

    selected = st.sidebar.multiselect(
        "Investment Strategy (pick 1 or 2)",
        options=strategies.list_strategies(),
        default=st.session_state.get("selected_strategies", []),
        max_selections=2,
        help="Choose one or two strategies. Two strategies are combined and capped at 6 tickers.",
    )

    compare = st.sidebar.checkbox(
        "Compare strategies side-by-side",
        value=st.session_state.get("compare_mode", False),
        help="When two strategies are picked, show allocation broken out by strategy.",
    )

    build_clicked = st.sidebar.button("Build Portfolio", type="primary", use_container_width=True)

    st.sidebar.divider()
    st.sidebar.subheader("Saved Portfolios")
    saved_names = portfolio_store.list_portfolio_names()
    save_name = st.sidebar.text_input("Save as name", value="", placeholder="e.g. test1")
    save_clicked = st.sidebar.button("Save current portfolio", use_container_width=True)
    load_name = st.sidebar.selectbox(
        "Load saved portfolio",
        options=["—"] + saved_names,
        index=0,
    )
    load_clicked = st.sidebar.button("Load selected", use_container_width=True)

    with st.sidebar.expander("Strategy descriptions"):
        for name in strategies.list_strategies():
            s = strategies.get_strategy(name)
            st.markdown(f"**{s.name}** — {s.description}")

    return {
        "amount": amount,
        "selected": selected,
        "compare": compare,
        "build_clicked": build_clicked,
        "save_name": save_name,
        "save_clicked": save_clicked,
        "load_name": load_name,
        "load_clicked": load_clicked,
    }


# ---------- actions ----------

def action_build(amount: float, selected: list[str]) -> None:
    err = allocator.validate_amount(amount)
    if err:
        st.session_state["error"] = err
        return
    err = strategies.validate_selection(selected)
    if err:
        st.session_state["error"] = err
        return

    ticker_strategies = strategies.combine_tickers(selected)
    tickers = [t for t, _ in ticker_strategies]
    prices = cached_current_prices(tuple(tickers))
    if not prices:
        st.session_state["error"] = (
            "Could not fetch live prices from yfinance. Check your internet connection and try again."
        )
        return

    try:
        df, residual = allocator.allocate(ticker_strategies, prices, amount)
    except ValueError as e:
        st.session_state["error"] = str(e)
        return

    st.session_state["holdings"] = df
    st.session_state["residual_cash"] = residual
    st.session_state["amount"] = float(amount)
    st.session_state["selected_strategies"] = selected
    st.session_state["ticker_strategies"] = ticker_strategies
    st.session_state["portfolio_id"] = st.session_state.get("portfolio_id") or f"p-{uuid.uuid4().hex[:8]}"
    st.session_state["error"] = None


def action_save(name: str) -> None:
    if st.session_state.get("holdings") is None:
        st.session_state["error"] = "Build a portfolio before saving."
        return
    if not name.strip():
        st.session_state["error"] = "Enter a name to save the portfolio."
        return
    df: pd.DataFrame = st.session_state["holdings"]
    payload = {
        "amount": float(st.session_state["amount"]),
        "strategies": list(st.session_state["selected_strategies"]),
        "residual_cash": float(st.session_state["residual_cash"]),
        "holdings": df.to_dict(orient="records"),
        "ticker_strategies": st.session_state["ticker_strategies"],
        "portfolio_id": st.session_state["portfolio_id"],
    }
    portfolio_store.save_portfolio(name.strip(), payload)
    st.session_state["error"] = None
    st.toast(f"Saved portfolio '{name.strip()}'.", icon="✅")


def action_load(name: str) -> None:
    if not name or name == "—":
        return
    payload = portfolio_store.load_portfolio(name)
    if not payload:
        st.session_state["error"] = f"Portfolio '{name}' not found."
        return
    st.session_state["holdings"] = pd.DataFrame(payload["holdings"])
    st.session_state["residual_cash"] = Decimal(str(payload["residual_cash"]))
    st.session_state["amount"] = float(payload["amount"])
    st.session_state["selected_strategies"] = list(payload["strategies"])
    st.session_state["ticker_strategies"] = [tuple(p) for p in payload.get("ticker_strategies", [])]
    st.session_state["portfolio_id"] = payload.get("portfolio_id") or f"p-{uuid.uuid4().hex[:8]}"
    st.session_state["error"] = None
    st.toast(f"Loaded portfolio '{name}'.", icon="📥")


# ---------- rendering ----------

def render_holdings_section(df: pd.DataFrame, residual: Decimal, amount: float) -> None:
    st.subheader("Holdings")
    display = df.copy()
    display["Price"] = display["Price"].map(lambda v: f"${v:,.2f}")
    display["Cost"] = display["Cost"].map(lambda v: f"${v:,.2f}")
    display["% of Portfolio"] = display["% of Portfolio"].map(lambda v: f"{v:.2f}%")
    st.dataframe(display, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Initial Investment", f"${amount:,.2f}")
    invested = float(sum(Decimal(str(v)) for v in df["Cost"]))
    c2.metric("Total Invested", f"${invested:,.2f}")
    c3.metric("Residual Cash", f"${float(residual):,.2f}")

    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(
        label="Download Holdings CSV",
        data=csv_buf.getvalue(),
        file_name="holdings.csv",
        mime="text/csv",
    )


def render_live_value(df: pd.DataFrame, amount: float, residual: Decimal) -> tuple[float, dict[str, float]]:
    st.subheader("Current Portfolio Value")
    refresh = st.button("Refresh Live Prices", help="Re-pull current prices from yfinance")
    if refresh:
        cached_current_prices.clear()

    tickers = tuple(df["Ticker"].tolist())
    live_prices = cached_current_prices(tickers)
    if not live_prices:
        st.error("Live prices unavailable. Showing last known cost basis.")
        current = float(sum(Decimal(str(v)) for v in df["Cost"])) + float(residual)
    else:
        current = float(allocator.current_value(df, live_prices)) + float(residual)

    delta_dollars = current - amount
    delta_pct = (delta_dollars / amount * 100.0) if amount else 0.0
    c1, c2 = st.columns([2, 1])
    c1.metric(
        "Live Total Value",
        f"${current:,.2f}",
        delta=f"{delta_dollars:+,.2f} ({delta_pct:+.2f}%)",
    )
    c2.caption("Live prices cached for 60 seconds. Click *Refresh Live Prices* to bypass cache.")
    return current, live_prices


def _build_chart_frame(holdings: pd.DataFrame, residual: Decimal, portfolio_id: str) -> tuple[pd.DataFrame, set[str]]:
    """Return ('date','value','source') frame with source in {'snapshot','backfill'}."""
    tickers = tuple(holdings["Ticker"].tolist())
    history = cached_history(tickers, days=10)

    backfilled = portfolio.historical_values(holdings, history, residual, n_days=5)
    backfilled["source"] = "backfill"

    snaps = snapshot_store.load_snapshots(portfolio_id)
    snap_df = pd.DataFrame(snaps)
    if not snap_df.empty:
        snap_df["date"] = pd.to_datetime(snap_df["date"]).dt.date
        snap_df["source"] = "snapshot"
    else:
        snap_df = pd.DataFrame(columns=["date", "value", "source"])

    if not backfilled.empty:
        backfilled["date"] = pd.to_datetime(backfilled["date"]).dt.date

    combined = pd.concat([backfilled, snap_df], ignore_index=True)
    if combined.empty:
        return combined, set()
    combined = combined.sort_values(["date", "source"]).drop_duplicates(subset=["date"], keep="last")
    combined = combined.sort_values("date").reset_index(drop=True)
    sources = set(combined["source"].unique().tolist())
    return combined, sources


def render_history_chart(df: pd.DataFrame, amount: float, residual: Decimal, current_value: float) -> pd.DataFrame:
    st.subheader("Weekly Trend — 5-Day Portfolio Value")

    pid = st.session_state.get("portfolio_id") or f"p-{uuid.uuid4().hex[:8]}"
    st.session_state["portfolio_id"] = pid
    snapshot_store.append_snapshot(pid, current_value)

    chart_df, sources = _build_chart_frame(df, residual, pid)
    if chart_df.empty:
        st.info("Not enough historical data to plot the 5-day trend yet.")
        return chart_df

    bench = cached_benchmark(days=10)
    bench_curve = portfolio.benchmark_curve(bench, initial_value=amount, n_days=5)

    fig = go.Figure()
    backfill_part = chart_df[chart_df["source"] == "backfill"]
    snap_part = chart_df[chart_df["source"] == "snapshot"]

    if not backfill_part.empty:
        fig.add_trace(go.Scatter(
            x=backfill_part["date"], y=backfill_part["value"],
            mode="lines+markers",
            line=dict(dash="dash", color="#1f77b4"),
            name="Backfilled (historical close)",
        ))
    if not snap_part.empty:
        fig.add_trace(go.Scatter(
            x=snap_part["date"], y=snap_part["value"],
            mode="lines+markers",
            line=dict(color="#1f77b4"),
            name="Snapshot (recorded)",
        ))

    if not bench_curve.empty:
        fig.add_trace(go.Scatter(
            x=bench_curve["date"], y=bench_curve["value"],
            mode="lines",
            line=dict(color="#ff7f0e", dash="dot"),
            name="S&P 500 (SPY) benchmark",
        ))

    fig.add_hline(
        y=amount,
        line_dash="dot",
        line_color="gray",
        annotation_text=f"Initial: ${amount:,.0f}",
        annotation_position="top left",
    )
    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Date",
        yaxis_title="Portfolio Value (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    st.plotly_chart(fig, use_container_width=True)
    return chart_df


def render_risk(chart_df: pd.DataFrame) -> None:
    st.subheader("Risk Metrics (last 5 trading days)")
    metrics = portfolio.risk_metrics(chart_df.rename(columns={"value": "value"}))
    c1, c2, c3 = st.columns(3)
    c1.metric("5-Day Return", f"{metrics['return_pct']:.2f}%")
    c2.metric("Daily Volatility", f"{metrics['volatility_pct']:.2f}%")
    c3.metric("Max Drawdown", f"{metrics['max_drawdown_pct']:.2f}%")


def render_sector_pie(df: pd.DataFrame) -> None:
    st.subheader("Sector Diversification")
    tickers = tuple(df["Ticker"].tolist())
    sector_map = cached_sector_map(tickers)
    rows = []
    for _, r in df.iterrows():
        sector = sector_map.get(r["Ticker"], "Other") or "Other"
        rows.append({"Sector": sector, "Cost": float(r["Cost"])})
    if not rows:
        return
    pie_df = pd.DataFrame(rows).groupby("Sector", as_index=False)["Cost"].sum()
    fig = px.pie(pie_df, values="Cost", names="Sector", hole=0.4)
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)


def render_strategy_comparison(df: pd.DataFrame) -> None:
    st.subheader("Strategy Comparison")
    grouped = df.groupby("Strategy").agg(
        Tickers=("Ticker", lambda s: ", ".join(s)),
        Total_Cost=("Cost", "sum"),
        Avg_Pct=("% of Portfolio", "sum"),
    ).reset_index()
    grouped["Total_Cost"] = grouped["Total_Cost"].map(lambda v: f"${v:,.2f}")
    grouped["Avg_Pct"] = grouped["Avg_Pct"].map(lambda v: f"{v:.2f}%")
    grouped = grouped.rename(columns={"Total_Cost": "Total Cost", "Avg_Pct": "Allocation %"})
    st.dataframe(grouped, use_container_width=True, hide_index=True)


# ---------- main ----------

def main() -> None:
    _init_state()

    st.title("Stock Portfolio Suggestion Engine")
    st.caption(
        "Pick a strategy, set an amount, get an equal-weight portfolio with live valuation "
        "and a 5-day trend chart."
    )

    inputs = render_sidebar()

    st.session_state["compare_mode"] = inputs["compare"]
    st.session_state["amount"] = float(inputs["amount"])
    st.session_state["selected_strategies"] = inputs["selected"]

    if inputs["build_clicked"]:
        action_build(inputs["amount"], inputs["selected"])
    if inputs["save_clicked"]:
        action_save(inputs["save_name"])
    if inputs["load_clicked"]:
        action_load(inputs["load_name"])

    if st.session_state.get("error"):
        st.error(st.session_state["error"])

    df = st.session_state.get("holdings")
    if df is None or df.empty:
        st.info(
            "Use the sidebar to enter an amount of at least $5,000, pick 1 or 2 strategies, "
            "and click *Build Portfolio*."
        )
        return

    amount = float(st.session_state["amount"])
    residual = st.session_state["residual_cash"] or Decimal("0")

    render_holdings_section(df, residual, amount)
    current_value, _ = render_live_value(df, amount, residual)
    chart_df = render_history_chart(df, amount, residual, current_value)
    render_risk(chart_df)

    left, right = st.columns(2)
    with left:
        render_sector_pie(df)
    with right:
        if st.session_state.get("compare_mode") and len(st.session_state.get("selected_strategies", [])) == 2:
            render_strategy_comparison(df)
        else:
            st.subheader("Strategy Mix")
            mix = df.groupby("Strategy", as_index=False)["Cost"].sum()
            fig = px.bar(mix, x="Strategy", y="Cost", text_auto=".2s")
            fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
