from __future__ import annotations

import math

import pytest

from telo_feasibility.economics import (
    CostLedger,
    break_even_volume,
    crf,
    icer,
    resilience_premium,
    straight_line,
)


def test_crf_matches_workbook_typed_constants() -> None:
    # 05_Assumptions!B25:D25 = 0.10296 (0.06, 15 y), 0.16275 (0.10, 10 y), 0.24036 (0.15, 7 y)
    assert crf(0.10, 10) == pytest.approx(0.16275, abs=5e-6)
    assert crf(0.06, 15) == pytest.approx(0.10296, abs=5e-6)
    assert crf(0.15, 7) == pytest.approx(0.24036, abs=5e-6)


def test_crf_zero_rate_is_straight_line() -> None:
    assert crf(0.0, 10) == pytest.approx(0.1)
    assert straight_line(100.0, 10) == pytest.approx(10.0)


def test_crf_rejects_bad_inputs() -> None:
    with pytest.raises(ValueError):
        crf(0.1, 0)
    with pytest.raises(ValueError):
        crf(-0.1, 5)


def test_ledger_total_and_per_unit() -> None:
    led = CostLedger(capital_annualized=100.0, variable_production=50.0)
    assert led.total() == 150.0
    assert led.per_delivered_unit(10.0) == 15.0
    assert math.isinf(led.per_delivered_unit(0.0))
    led.check_nonnegative()


def test_icer_dominance_labels() -> None:
    assert icer(120.0, 100.0, 10.0, 10.0).label == "dominated"
    assert icer(90.0, 100.0, 8.0, 10.0).label == "dominant"
    r = icer(120.0, 100.0, 5.0, 10.0)
    assert r.label == "trade_off" and r.value == pytest.approx(4.0)
    assert icer(100.0, 100.0, 10.0, 10.0).label == "equivalent"
    assert icer(120.0, 100.0, 10.0, 10.0).value is None


def test_break_even_and_premium() -> None:
    assert break_even_volume(1000.0, 2.0) == 500.0
    assert math.isinf(break_even_volume(1000.0, 0.0))
    assert resilience_premium(1200.0, 1000.0, 100.0) == 2.0
