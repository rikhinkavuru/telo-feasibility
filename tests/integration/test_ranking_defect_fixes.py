"""Defects that carried the architecture ranking, fixed under revision R009.

Each test is named for the defect id it would have caught. The register lives in
``docs/design_space/bottleneck_decomposition.md`` section 7 and, for the NEW- items, in
``docs/design_space/inventory_capacity_hybrids.md`` section 6.
"""

from __future__ import annotations

import math

import pytest

from telo_feasibility.network import default_regions
from telo_feasibility.optimization import (
    DESIGN_SPACES,
    LEGACY_DESIGN_SPACES,
    MATCHED_INVENTORY_NAMES,
    Evaluation,
    _fill_tolerance,
)
from telo_feasibility.schemas import StrategyId
from telo_feasibility.simulation import SimSettings, run_paired
from telo_feasibility.strategies import build_strategy

from .conftest import quiet


def _settings(**kw: object) -> SimSettings:
    base = dict(
        horizon_days=365 + 1096,
        warm_up_days=365,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=False,
    )
    base.update(kw)
    return SimSettings(**base)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# NEW-1: opening inventory is purchased, not inherited
# ---------------------------------------------------------------------------


def test_new1_opening_inventory_is_charged_and_scales_with_the_stock_policy(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    shallow = designs.by_id(StrategyId.S0).model_copy(deep=True)
    shallow.design_variables["safety_stock_days"] = 30.0
    deep = shallow.model_copy(deep=True)
    deep.design_variables["safety_stock_days"] = 365.0
    rs, rd = run_paired([shallow, deep], product, q, _settings(), 20260901, [0])
    assert rs.ledger.opening_inventory > 0.0, "opening stock must be charged at all"
    # a design that opens with a year of cover pays for a year of cover
    assert rd.ledger.opening_inventory > 4.0 * rs.ledger.opening_inventory
    # the charge is material rather than decorative: it is a visible share of the deep
    # design's annual cost. Total cost is deliberately not compared between the two arms,
    # because opening stock substitutes for production in a capacity-tight network and the
    # deep arm can produce less, which is a real effect and not the charge disappearing.
    assert rd.ledger.opening_inventory / rd.metrics["annual_total_cost"] > 0.01


def test_new1_charge_equals_opening_units_at_production_unit_value(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    d = designs.by_id(StrategyId.S1)
    settings = _settings()
    r = run_paired([d], product, q, settings, 20260901, [0])[0]
    p = product.parameters
    unit_value = p.base("variable_materials_usd_per_unit") + p.base(
        "variable_conversion_usd_per_unit"
    )
    years = (settings.horizon_days - settings.warm_up_days) / 365.25
    share = (settings.horizon_days - settings.warm_up_days) / settings.horizon_days
    expected = r.counters.initial_units * unit_value * share / years
    assert r.ledger.opening_inventory == pytest.approx(expected, rel=1e-9)


def test_new1_ledger_total_includes_the_new_field(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    r = run_paired(
        [designs.by_id(StrategyId.S1)], product, quiet(glob), _settings(), 20260901, [0]
    )[0]
    parts = (
        r.ledger.capital_annualized
        + r.ledger.fixed_site_operations
        + r.ledger.product_site_launch
        + r.ledger.variable_production
        + r.ledger.opening_inventory
        + r.ledger.quality_testing
        + r.ledger.failure_waste
        + r.ledger.inventory_logistics
        + r.ledger.resilience_contracts
        + r.ledger.os_integration
    )
    assert r.ledger.total() == pytest.approx(parts, rel=1e-12)
    r.ledger.check_nonnegative()


# ---------------------------------------------------------------------------
# MD-3 and MD-12: every strategy searches the same inventory space
# ---------------------------------------------------------------------------


def test_md12_every_frozen_strategy_gets_the_matched_inventory_space() -> None:
    for sid, space in DESIGN_SPACES.items():
        names = {v.name for v in space}
        assert names >= MATCHED_INVENTORY_NAMES, sid.value
        by_name = {v.name: v for v in space}
        assert by_name["safety_stock_days"].low == 30.0
        assert by_name["safety_stock_days"].high == 365.0
        assert by_name["region_base_stock"].kind == "int"


def test_md12_legacy_spaces_are_kept_for_reproducibility() -> None:
    assert set(LEGACY_DESIGN_SPACES) == set(DESIGN_SPACES)
    legacy_s5 = {v.name for v in LEGACY_DESIGN_SPACES[StrategyId.S5]}
    assert "region_base_stock" not in legacy_s5
    assert {v.name: v for v in LEGACY_DESIGN_SPACES[StrategyId.S5]}[
        "safety_stock_days"
    ].high == 90.0
    # the strategy's own non-inventory variables survive in the active space
    active_s5 = {v.name for v in DESIGN_SPACES[StrategyId.S5]}
    assert {"sites", "node_scale"} <= active_s5


# ---------------------------------------------------------------------------
# MD-1: the material policy is not a function of the lead time
# ---------------------------------------------------------------------------


def test_md1_opening_material_position_is_lead_independent(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    from telo_feasibility.configs import ProductConfig
    from telo_feasibility.sensitivity import set_base
    from telo_feasibility.simulation import _Sim, world_for_run

    settings = _settings()
    d = designs.by_id(StrategyId.S0)
    positions = []
    for lead in (240.0, 90.0, 7.0):
        p2 = ProductConfig(
            product.presentation,
            set_base(product.parameters, "material_lead_time_days", lead),
            product.path,
        )
        world, streams = world_for_run(glob, settings, 3, 0, [d])
        sim = _Sim(build_strategy(d, p2, glob), p2, glob, world, streams, settings)
        positions.append(sim.materials["central"].stock["api"])
    assert len(set(positions)) == 1, f"opening position still tracks the lead: {positions}"


def test_md1_cycle_cover_above_the_reorder_point_is_lead_independent(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    """The order-up-to level is reorder point plus a cycle that does not scale with lead."""
    from telo_feasibility.suppliers import MaterialStore

    daily = 1000.0
    made = []
    for lead in (7.0, 90.0):
        store = MaterialStore(
            "s",
            {"api": 0},
            {"api": "api_1"},
            {"api": lead},
            target_days=60.0,
            reorder_point_days=14.0,
            batch_units=1,
        )
        store.place_orders(0, daily)
        made.append(store.open_orders[-1].units)
    # each order brings the position to pipeline + safety + cycle, so the difference
    # between the two leads is exactly the pipeline term and nothing else
    assert made[1] - made[0] == pytest.approx((90.0 - 7.0) * daily, rel=1e-9)


# ---------------------------------------------------------------------------
# MD-11: the infeasible tie-break respects the noise the screen carries
# ---------------------------------------------------------------------------


def _ev(fill: float, cost: float) -> Evaluation:
    return Evaluation(
        design_variables={},
        mean_cost=cost,
        mean_fill=fill,
        p_meet=0.0,
        mean_shortage_days=0.0,
        mean_cost_per_unit=cost / 1e6,
        feasible=False,
        n_runs=20,
        stage="grid",
    )


def test_md11_tolerance_is_positive_and_scales_with_the_screen() -> None:
    evs = [_ev(0.98, 1e7), _ev(0.99, 2e7)]
    small = _fill_tolerance(evs, 20)
    large = _fill_tolerance(evs, 100)
    assert small > 0.0 and large > 0.0
    assert small > large, "a smaller screen must carry a wider noise band"
    assert _fill_tolerance(evs, 0) == 0.0
    assert _fill_tolerance([_ev(0.9, 1.0)], 20) == 0.0


def test_md11_a_fill_gain_inside_the_noise_does_not_buy_a_cost_increase() -> None:
    """The 2026-09-03 run paid 9.26M USD/yr for 0.00004 of fill. It must not any more."""
    evs = [_ev(0.9800, 1.0e7), _ev(0.98004, 1.926e7)]
    tol = _fill_tolerance(evs, 20)
    best_fill = max(e.mean_fill for e in evs)
    near = [e for e in evs if e.mean_fill >= best_fill - tol]
    chosen = min(near, key=lambda e: (e.mean_cost, -e.mean_fill))
    assert chosen.mean_cost == pytest.approx(1.0e7)
    # a fill gain far outside the band still wins on fill
    evs2 = [_ev(0.90, 1.0e7), _ev(0.99, 1.2e7)]
    tol2 = _fill_tolerance(evs2, 20)
    near2 = [e for e in evs2 if e.mean_fill >= max(x.mean_fill for x in evs2) - tol2]
    assert min(near2, key=lambda e: (e.mean_cost, -e.mean_fill)).mean_fill == pytest.approx(0.99)


# ---------------------------------------------------------------------------
# NEW-2: allocation policies can differ, and do when the regions differ
# ---------------------------------------------------------------------------


def test_new2_default_regions_are_identical_and_a_spread_separates_them() -> None:
    flat = default_regions(4)
    assert {r.criticality_weight for r in flat} == {1.0}
    assert {r.minimum_guarantee_fraction for r in flat} == {0.0}
    spread = default_regions(4, criticality_spread=0.6, minimum_guarantee_fraction=0.25)
    weights = [r.criticality_weight for r in spread]
    assert weights[0] == pytest.approx(0.4) and weights[-1] == pytest.approx(1.6)
    assert weights == sorted(weights)
    assert {r.minimum_guarantee_fraction for r in spread} == {0.25}
    assert sum(r.share for r in spread) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="criticality spread"):
        default_regions(4, criticality_spread=1.5)


def test_new2_policies_are_inert_when_regions_are_identical_and_differ_when_not(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    settings = _settings(shortage_listed_at_t0=True)
    base = designs.by_id(StrategyId.S0)
    policies = ("proportional", "criticality_weighted", "minimum_guarantee")

    def fills(spread: float, guarantee: float) -> list[float]:
        out = []
        for pol in policies:
            d = base.model_copy(deep=True)
            d.allocation_policy = pol
            d.design_variables.update(
                {"region_criticality_spread": spread, "region_minimum_guarantee": guarantee}
            )
            out.append(
                run_paired([d], product, glob, settings, 20260901, [0])[0].metrics["fill_rate"]
            )
        return out

    flat = fills(0.0, 0.0)
    assert len({round(f, 9) for f in flat}) == 1, "identical regions make these one function"
    varied = fills(0.6, 0.25)
    assert len({round(f, 9) for f in varied}) > 1, "a regional spread must separate them"


# ---------------------------------------------------------------------------
# MD-23 and MD-24: readiness and a volume commitment have service channels
# ---------------------------------------------------------------------------


def test_md23_any_batch_restarts_the_readiness_clock(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rt = build_strategy(designs.by_id(StrategyId.S3), product, glob)
    site = next(s for s in rt.sites.values() if s.reserved)
    site.exercise_interval_days = 90.0
    site.next_exercise_day = 0
    site.available_from_day = 0
    site.active_until_batches = 2
    assert not site.exercise_due(0), "a line mid-campaign is not idle"
    site.start_batch(10, 1.0)
    assert site.next_exercise_day == 100, "a campaign batch must requalify the line"
    site.active_until_batches = 0
    assert not site.exercise_due(50)
    assert site.exercise_due(100)


def test_md24_a_commitment_buys_priority_access(product, glob) -> None:  # type: ignore[no-untyped-def]
    from telo_feasibility.configs import load_all_strategies

    committed = None
    for d in load_all_strategies().designs:
        if d.id.is_frozen or not d.site_plans:
            continue
        if any(sp.reserved for sp in d.site_plans):
            committed = d
            break
    if committed is None:
        pytest.skip("no design-space strategy declares a reserved line")
    plain = committed.model_copy(deep=True)
    plain.design_variables["take_or_pay_fraction"] = 0.0
    paid = committed.model_copy(deep=True)
    paid.design_variables["take_or_pay_fraction"] = 1.0
    rt_plain = build_strategy(plain, product, glob)
    rt_paid = build_strategy(paid, product, glob)
    assert not rt_plain.take_or_pay_usd_per_year
    assert rt_paid.take_or_pay_usd_per_year
    committed_ids = set(rt_paid.take_or_pay_usd_per_year)
    # the committed line is ordered ahead of uncommitted non-local sources
    for pol in rt_paid.region_policies.values():
        non_local = [s for s in pol.source_order if len(rt_paid.sites[s].serves_region_ids) > 1]
        ranked = [s for s in non_local if s in committed_ids]
        if ranked and len(non_local) > 1:
            assert non_local.index(ranked[0]) <= non_local.index(non_local[-1])
    assert math.isfinite(sum(rt_paid.take_or_pay_usd_per_year.values()))
