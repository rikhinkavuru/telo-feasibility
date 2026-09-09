"""Take-or-pay on reserved capacity and strategy-level quality factors (S8+ levers).

Both default to off, so the frozen comparators are unaffected; that is asserted by
``tests/regression/test_frozen_strategies.py`` and again here on the runtime.
"""

from __future__ import annotations

import pytest

from telo_feasibility.schemas import StrategyId
from telo_feasibility.simulation import (
    SimSettings,
    _quality_params,
    run_paired,
    simulate_run,
    world_for_run,
)
from telo_feasibility.strategies import build_strategy

from .conftest import override, quiet


def _settings() -> SimSettings:
    return SimSettings(
        horizon_days=500,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=True,
    )


def _run(design, product, glob, settings, seed=11):  # type: ignore[no-untyped-def]
    world, streams = world_for_run(glob, settings, seed, 0, [design])
    rt = build_strategy(design, product, glob, n_regions=settings.n_regions)
    return simulate_run(rt, product, glob, world, streams, settings), rt


def test_take_or_pay_defaults_off_and_charges_when_set(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    base = designs.by_id(StrategyId.S3).model_copy(deep=True)
    assert build_strategy(base, product, q).take_or_pay_usd_per_year == {}
    r0, rt0 = _run(base, product, q, _settings())
    top = base.model_copy(deep=True)
    top.design_variables["take_or_pay_fraction"] = 0.5
    rt = build_strategy(top, product, q)
    assert set(rt.take_or_pay_usd_per_year) == {"reserved_cdmo"}
    assert rt.take_or_pay_usd_per_year["reserved_cdmo"] > 0
    assert any("take-or-pay charges 50%" in n for n in rt.notes)
    r1, _ = _run(top, product, q, _settings())
    # a volume commitment is a cost, never a service change
    assert r1.metrics["served_units"] == r0.metrics["served_units"]
    assert r1.metrics["fill_rate"] == r0.metrics["fill_rate"]
    assert r1.event_digest == r0.event_digest
    assert r1.ledger.resilience_contracts > r0.ledger.resilience_contracts
    assert r1.metrics["annual_total_cost"] > r0.metrics["annual_total_cost"]
    _ = rt0


def test_take_or_pay_scales_with_the_committed_fraction(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    d = designs.by_id(StrategyId.S3).model_copy(deep=True)
    fees = {}
    for f in (0.25, 0.5, 1.0):
        dd = d.model_copy(deep=True)
        dd.design_variables["take_or_pay_fraction"] = f
        fees[f] = build_strategy(dd, product, q).take_or_pay_usd_per_year["reserved_cdmo"]
    assert fees[0.5] == pytest.approx(2 * fees[0.25])
    assert fees[1.0] == pytest.approx(4 * fees[0.25])


def test_quality_factors_default_to_the_global_values(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rt = build_strategy(designs.by_id(StrategyId.S0), product, glob)
    assert rt.deviation_rate_factor == 1.0 and rt.investigation_duration_factor == 1.0
    qp_plain = _quality_params(glob)
    qp_runtime = _quality_params(glob, rt)
    assert qp_plain == qp_runtime


def test_quality_factors_reduce_deviations_and_investigation_time(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """An operating system that closes deviations faster, modeled honestly as that and
    nothing else: release time and capacity are untouched."""
    g = override(quiet(glob), deviation_rate_per_batch=0.5, investigation_duration_days=60.0)
    d = designs.by_id(StrategyId.S0).model_copy(deep=True)
    d.design_variables["capacity_factor"] = 2.0
    r0, _ = _run(d, product, g, _settings())
    os_d = d.model_copy(deep=True)
    os_d.design_variables.update(
        {"deviation_rate_factor": 0.2, "investigation_duration_factor": 0.25}
    )
    rt = build_strategy(os_d, product, g)
    assert rt.deviation_rate_factor == 0.2
    qp = _quality_params(g, rt)
    assert qp.deviation_rate == pytest.approx(0.1)
    assert qp.investigation_median_days == pytest.approx(15.0)
    r1, _ = _run(os_d, product, g, _settings())
    assert r1.metrics["deviations"] < r0.metrics["deviations"]
    assert any("operating-system" in n for n in rt.notes)


def test_quality_factors_cannot_push_a_rate_out_of_range(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    g = override(quiet(glob), deviation_rate_per_batch=0.9)
    d = designs.by_id(StrategyId.S0).model_copy(deep=True)
    d.design_variables["deviation_rate_factor"] = 5.0
    rt = build_strategy(d, product, g)
    assert _quality_params(g, rt).deviation_rate == 1.0
    d.design_variables["deviation_rate_factor"] = 0.0
    assert _quality_params(g, build_strategy(d, product, g)).deviation_rate == 0.0


def test_frozen_strategies_are_untouched_by_both_levers(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    settings = _settings()
    res = run_paired(
        designs.designs, product, quiet(glob), settings, master_seed=4, run_indices=[0]
    )
    for r in res:
        assert r.ledger.resilience_contracts >= 0.0
    rts = [build_strategy(d, product, quiet(glob)) for d in designs.designs]
    assert all(not rt.take_or_pay_usd_per_year for rt in rts)
    assert all(rt.deviation_rate_factor == 1.0 for rt in rts)
