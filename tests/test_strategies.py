from engine import strategies


def test_all_five_strategies_present():
    names = strategies.list_strategies()
    assert set(names) == {
        "Ethical Investing",
        "Growth Investing",
        "Index Investing",
        "Quality Investing",
        "Value Investing",
    }


def test_each_strategy_has_five_tickers():
    for name in strategies.list_strategies():
        s = strategies.get_strategy(name)
        assert len(s.tickers) == 5
        assert s.description.strip()


def test_combine_single_strategy_returns_all_five():
    pairs = strategies.combine_tickers(["Index Investing"])
    tickers = [t for t, _ in pairs]
    assert tickers == ["VTI", "IXUS", "ILTB", "VOO", "QQQ"]
    assert all(s == "Index Investing" for _, s in pairs)


def test_combine_two_strategies_caps_at_six():
    pairs = strategies.combine_tickers(["Growth Investing", "Value Investing"])
    assert len(pairs) <= 6
    tickers = [t for t, _ in pairs]
    assert len(tickers) == len(set(tickers))


def test_combine_two_strategies_dedupes_overlap():
    pairs = strategies.combine_tickers(["Ethical Investing", "Quality Investing"])
    tickers = [t for t, _ in pairs]
    assert len(tickers) == len(set(tickers))


def test_validate_selection():
    assert strategies.validate_selection([]) is not None
    assert strategies.validate_selection(["Growth Investing"]) is None
    assert strategies.validate_selection(["Growth Investing", "Value Investing"]) is None
    assert strategies.validate_selection(["A", "B", "C"]) is not None
    assert strategies.validate_selection(["NotAStrategy"]) is not None
