"""Thresholds, dominance, and reversal maps (Phase E machinery)."""

from __future__ import annotations

import math

from telo_feasibility.design_space_analysis import (
    ALL_INPUTS,
    EXTRA_INPUTS,
    Point,
    _apply,
    _range,
    dominance,
    evaluate,
    reversal_map,
    threshold,
)
from telo_feasibility.schemas import Eligibility, StrategyId
from telo_feasibility.simulation import SimSettings

from .conftest import quiet


def _pt(sid: str, cost: float, fill: float, p_meet: float = 1.0, feasible: bool = True) -> Point:
    return Point(
        sid, {}, fill, p_meet, cost, 0.0, 0.0, cost / 1e6, 0.0, feasible, 1, "no_conclusion"
    )


def test_every_extra_input_names_a_real_parameter(glob, product) -> None:  # type: ignore[no-untyped-def]
    for name, (which, pid) in EXTRA_INPUTS.items():
        params = glob.parameters if which == "global" else product.parameters.parameters
        assert pid in params, f"{name} -> {pid}"
        lo, base, hi = _range(product, glob, name)
        assert lo <= base <= hi
    assert set(ALL_INPUTS) > set(EXTRA_INPUTS)


def test_apply_sets_only_the_named_parameters(glob, product) -> None:  # type: ignore[no-untyped-def]
    prod, g = _apply(product, glob, {"commissioning_days": 111.0, "shelf_life": 7.0})
    assert g.base("node_commissioning_days") == 111.0
    assert prod.parameters.base("shelf_life_months") == 7.0
    # untouched parameters keep their values and the inputs are not mutated
    assert g.base("discount_rate") == glob.base("discount_rate")
    assert glob.base("node_commissioning_days") != 111.0
    assert product.parameters.base("shelf_life_months") != 7.0


def test_dominance_marks_the_frontier() -> None:
    pts = [
        _pt("S0", 10.0, 0.90),
        _pt("S1", 12.0, 0.90),  # costs more, serves the same: dominated by S0
        _pt("S2", 12.0, 0.99),  # costs more but serves better: on the frontier
        _pt("S3", 9.0, 0.99),  # cheapest and best: dominates S1 and S2
    ]
    rows = {r.strategy_id: r for r in dominance(pts)}
    assert rows["S3"].on_frontier and rows["S3"].dominated_by == []
    # S1 costs as much as S2 and serves worse, and S0 serves the same for less
    assert rows["S1"].dominated_by == ["S0", "S2", "S3"]
    assert rows["S2"].dominated_by == ["S3"]
    assert rows["S0"].dominated_by == ["S3"]
    # The tolerance is a noise band on cost. A rival inside the band dominates only by
    # serving better, and a rival that is merely cheaper by less than the band does not.
    loose = {r.strategy_id: r for r in dominance(pts, cost_tolerance=3.0)}
    assert loose["S1"].dominated_by == ["S2", "S3"]  # S0's 2.0 saving is inside the band
    assert loose["S0"].dominated_by == ["S2", "S3"]  # both serve better at a tied cost
    assert loose["S2"].dominated_by == [] and loose["S3"].dominated_by == []


def test_evaluate_reports_per_strategy_rows(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    settings = SimSettings(
        horizon_days=300,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )
    ds = [designs.by_id(StrategyId.S0), designs.by_id(StrategyId.S2)]
    pts = evaluate(
        ds,
        product,
        quiet(glob),
        settings,
        seed=5,
        runs=[0, 1],
        tau=0.99,
        q=0.9,
        eligibility={"S0": Eligibility.NO_CONCLUSION},
    )
    assert [p.strategy_id for p in pts] == ["S0", "S2"]
    assert all(p.n_runs == 2 and math.isfinite(p.mean_cost) for p in pts)
    assert pts[0].eligibility == Eligibility.NO_CONCLUSION.value
    assert pts[1].eligibility == Eligibility.NO_CONCLUSION.value  # default when unmapped


def test_threshold_finds_a_capacity_crossing(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """Demand is swept through capacity_utilization: S0 is feasible below some demand."""
    settings = SimSettings(
        horizon_days=400,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )
    d = designs.by_id(StrategyId.S0).model_copy(deep=True)
    d.design_variables.update({"capacity_factor": 1.05, "region_base_stock": 1.0})
    t = threshold(
        d,
        product,
        quiet(glob),
        settings,
        input_name="capacity_utilization",
        seed=3,
        runs=[0],
        tau=0.99,
        q=0.5,
        steps=3,
    )
    assert (
        t.input_name == "capacity_utilization" and t.parameter_id == "product.annual_demand_units"
    )
    assert t.feasible_at_low and not t.feasible_at_high
    assert t.direction == "feasible_below"
    assert t.bracket is not None and t.bracket[0] <= t.threshold <= t.bracket[1]
    assert t.low < t.threshold < t.high
    assert len(t.evaluations) == 2 + 3


def test_threshold_reports_no_crossing_when_endpoints_agree(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    settings = SimSettings(
        horizon_days=300,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )
    d = designs.by_id(StrategyId.S0).model_copy(deep=True)
    d.design_variables["capacity_factor"] = 0.0  # no production: infeasible at any release time
    t = threshold(
        d,
        product,
        quiet(glob),
        settings,
        input_name="release_time",
        seed=3,
        runs=[0],
        tau=0.99,
        q=0.9,
        steps=2,
    )
    assert t.direction == "infeasible_everywhere" and t.threshold is None
    assert "no threshold" in t.note and len(t.evaluations) == 2


def test_reversal_map_shape_and_preference(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    settings = SimSettings(
        horizon_days=300,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )
    ds = [designs.by_id(StrategyId.S0), designs.by_id(StrategyId.S4)]
    lo, _base, hi = _range(product, glob, "capacity_utilization")
    m = reversal_map(
        ds,
        product,
        quiet(glob),
        settings,
        axes={"capacity_utilization": [lo, hi], "release_time": [2.0, 14.0]},
        seed=4,
        runs=[0],
        tau=0.99,
        q=0.5,
    )
    assert len(m["cells"]) == 4
    for c in m["cells"]:
        assert set(c["cost"]) == {"S0", "S4"}
        assert c["preferred"] in (None, "S0", "S4")
        if c["preferred"] is not None:
            # the preferred strategy is the cheapest feasible one
            feas = {k: v for k, v in c["cost"].items() if k in c["feasible"]}
            assert c["preferred"] == min(feas, key=lambda k: feas[k])
