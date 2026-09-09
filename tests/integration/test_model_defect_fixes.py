"""Regression tests for the model defects the Phase A decomposition found (revision R004).

Each test names the MD id it pins. These are the tests that would have caught the defect:
they assert the corrected behaviour and, where the defect had a measurable signature, that
the signature is gone.
"""

from __future__ import annotations

import numpy as np
import pytest

from telo_feasibility.configs import ProductConfig, load_all_strategies
from telo_feasibility.deterministic import screen_row
from telo_feasibility.production import SiteRuntime
from telo_feasibility.schemas import ManufacturingSite, Pathway, StrategyId
from telo_feasibility.simulation import SimSettings, simulate_run, world_for_run
from telo_feasibility.strategies import STATUS_QUO_SCALE, build_strategy
from telo_feasibility.suppliers import MaterialStore, PurchaseOrder

from .conftest import override, quiet


def _settings(**kw: object) -> SimSettings:
    base = {
        "horizon_days": 900,
        "warm_up_days": 200,
        "shortage_day_threshold": 0.95,
        "fill_rate_mean_min": 0.99,
        "recovery_window_days": 30,
        "record_events": False,
    }
    base.update(kw)
    return SimSettings(**base)  # type: ignore[arg-type]


def _run(design, product, glob, settings, seed=13):  # type: ignore[no-untyped-def]
    world, streams = world_for_run(glob, settings, seed, 0, [design])
    rt = build_strategy(design, product, glob, n_regions=settings.n_regions)
    return simulate_run(rt, product, glob, world, streams, settings), rt


# --------------------------------------------------------------------- MD-7


def test_md7_expansion_above_the_status_quo_scale_waits_to_be_commissioned(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    """Capacity above what the plant runs on day zero is an expansion, not a free upgrade."""
    rt = build_strategy(designs.by_id(StrategyId.S2), product, glob)
    central = rt.sites["central"]
    nominal = product.parameters.base("batches_per_site_year_nominal")
    assert central.baseline_batches_per_year == pytest.approx(nominal * STATUS_QUO_SCALE)
    assert central.batches_per_year > central.baseline_batches_per_year
    assert central.expansion_available_day == round(glob.base("capacity_expansion_days"))
    # the ramp is what the scheduler sees
    assert central.batches_per_year_on(0) == central.baseline_batches_per_year
    assert central.batches_per_year_on(central.expansion_available_day) == central.batches_per_year
    assert central.occupancy_days_on(0) > central.occupancy_days_on(central.expansion_available_day)
    assert any("status-quo scale" in n for n in rt.notes)


def test_md7_a_plant_at_or_below_the_status_quo_scale_has_no_ramp(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    for sid in (StrategyId.S0, StrategyId.S1, StrategyId.S5):
        rt = build_strategy(designs.by_id(sid), product, glob)
        central = rt.sites["central"]
        assert central.baseline_batches_per_year is None, sid
        assert central.batches_per_year_on(0) == central.batches_per_year, sid


def test_md7_instant_expansion_restores_the_previous_behaviour(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    d = designs.by_id(StrategyId.S4).model_copy(deep=True)
    d.design_variables["instant_expansion"] = 1.0
    rt = build_strategy(d, product, glob)
    assert rt.sites["central"].baseline_batches_per_year is None
    ramped, _ = _run(designs.by_id(StrategyId.S4), product, quiet(glob), _settings())
    instant, _ = _run(d, product, quiet(glob), _settings())
    # the sensitivity switch can only help: the plant is larger sooner
    assert instant.metrics["served_units"] >= ramped.metrics["served_units"]


def test_md7_contracted_capacity_is_not_ramped(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """Reserved and 503B lines are not built by Telo, so they keep their activation lead."""
    for sid, site_id in ((StrategyId.S3, "reserved_cdmo"), (StrategyId.S7, "p503b_1")):
        rt = build_strategy(designs.by_id(sid), product, glob)
        assert rt.sites[site_id].baseline_batches_per_year is None, site_id


# --------------------------------------------------------------------- MD-6


def test_md6_fixed_operations_do_not_accrue_before_a_site_exists(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """A node under construction costs capital, not payroll."""
    q = quiet(glob)
    d = designs.by_id(StrategyId.S5).model_copy(deep=True)
    late, rt_late = _run(d, product, override(q, node_commissioning_days=800.0), _settings())
    early, rt_early = _run(d, product, override(q, node_commissioning_days=0.0), _settings())
    assert rt_late.site_fixed_usd_per_year == rt_early.site_fixed_usd_per_year
    # same sites, same fixed rate, but the late network operates them for fewer days
    assert late.ledger.fixed_site_operations < early.ledger.fixed_site_operations
    # capital is sunk either way
    assert late.ledger.capital_annualized == pytest.approx(early.ledger.capital_annualized)
    assert late.ledger.product_site_launch == pytest.approx(early.ledger.product_site_launch)


def test_md6_open_backlog_at_the_horizon_is_reported_not_charged(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    settings = _settings()
    r, _ = _run(designs.by_id(StrategyId.S0), product, glob, settings)
    assert "open_backlog_units_at_horizon" in r.metrics
    assert r.metrics["open_backlog_units_at_horizon"] >= 0.0
    # nothing younger than the backorder window can have been counted lost
    assert r.metrics["fill_rate"] <= 1.0


# --------------------------------------------------------------------- MD-4


def test_md4_opening_stock_is_not_all_stamped_with_the_same_expiry(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """Half the shelf life fell on the first measured day, so opening stock expired at once."""
    q = quiet(glob)
    d = designs.by_id(StrategyId.S1).model_copy(deep=True)
    d.design_variables["capacity_factor"] = 2.0
    settings = _settings(horizon_days=800, warm_up_days=200)
    world, streams = world_for_run(q, settings, 5, 0, [d])
    rt = build_strategy(d, product, q, n_regions=settings.n_regions)
    from telo_feasibility.simulation import _Sim

    sim = _Sim(rt, product, q, world, streams, settings)
    expiries = sorted({lot.expiry_day for lots in sim.book.lots.values() for lot in lots})
    assert len(expiries) > 1, "opening stock must hold a mix of ages"
    shelf = round(rt.shelf_life_days)
    assert max(expiries) <= shelf and min(expiries) >= 1
    # the mass balance still holds exactly
    assert sim.c.initial_units == sim.book.total()


def test_md4_more_opening_stock_is_not_harmful(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    settings = _settings()
    small = designs.by_id(StrategyId.S0).model_copy(deep=True)
    small.design_variables.update({"capacity_factor": 1.5, "safety_stock_days": 30.0})
    large = small.model_copy(deep=True)
    large.design_variables["safety_stock_days"] = 300.0
    r_small, _ = _run(small, product, q, settings)
    r_large, _ = _run(large, product, q, settings)
    assert r_large.metrics["fill_rate"] >= r_small.metrics["fill_rate"] - 1e-9


# --------------------------------------------------------------------- MD-14


def test_md14_a_reserved_line_telo_does_not_own_carries_no_capital(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rt = build_strategy(designs.by_id(StrategyId.S3), product, glob)
    assert rt.site_capital_usd["reserved_cdmo"] == 0.0
    assert rt.site_fixed_usd_per_year["reserved_cdmo"] == 0.0
    assert rt.site_validation_usd["reserved_cdmo"] == 0.0
    # the reservation fee is still charged, and is still based on what the line costs its owner
    assert rt.reserved_fee_usd_per_year["reserved_cdmo"] > 0.0


def test_md14_an_owned_standby_line_still_carries_its_asset(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    d = designs.by_id(StrategyId.S3).model_copy(deep=True)
    d.design_variables["reserved_site_owned"] = 1.0
    rt = build_strategy(d, product, glob)
    assert rt.site_capital_usd["reserved_cdmo"] > 0.0
    assert rt.site_fixed_usd_per_year["reserved_cdmo"] > 0.0
    assert any("reserved capacity is owned" in n for n in rt.notes)


def test_md14_the_cost_boundary_change_lowers_the_reserved_strategy_cost(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    contracted, _ = _run(designs.by_id(StrategyId.S3), product, q, _settings())
    owned_d = designs.by_id(StrategyId.S3).model_copy(deep=True)
    owned_d.design_variables["reserved_site_owned"] = 1.0
    owned, _ = _run(owned_d, product, q, _settings())
    assert contracted.metrics["annual_total_cost"] < owned.metrics["annual_total_cost"]
    assert contracted.metrics["served_units"] == owned.metrics["served_units"]


# --------------------------------------------------------------------- MD-2


def test_md2_the_reorder_point_covers_at_least_one_batch() -> None:
    store = MaterialStore(
        site_id="s",
        stock={"api": 0},
        supplier_for={"api": "api_1"},
        lead_time_days={"api": 1.0},
        target_days=10.0,
        reorder_point_days=1.0,
        batch_units=25_000,
    )
    # a tiny daily draw would put the reorder point far below one batch without the fix
    placed = store.place_orders(0, daily_consumption=100.0)
    assert placed and placed[0].units >= store.batch_units


def test_md2_short_component_leads_no_longer_stall_the_store(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """The defect showed up as stockouts exploding when the lead time was cut."""
    q = override(quiet(glob), supplier_disruptions_per_supplier_year=0.0)
    d = designs.by_id(StrategyId.S5).model_copy(deep=True)
    d.design_variables["node_scale"] = 0.35
    long_lead = ProductConfig(
        product.presentation,
        override(product.parameters, material_lead_time_days=90.0),
        product.path,
    )
    short_lead = ProductConfig(
        product.presentation,
        override(product.parameters, material_lead_time_days=7.0),
        product.path,
    )
    r_long, _ = _run(d, long_lead, q, _settings())
    r_short, _ = _run(d, short_lead, q, _settings())
    assert r_short.metrics["material_stockouts"] <= r_long.metrics["material_stockouts"] + 5


# --------------------------------------------------------------------- MD-13


def test_md13_more_nodes_than_regions_are_placed_round_robin(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    d = designs.by_id(StrategyId.S5).model_copy(deep=True)
    d.design_variables["sites"] = 6.0
    rt = build_strategy(d, product, glob, n_regions=4)
    node_ids = sorted(s for s in rt.sites if s.startswith("node_"))
    assert len(node_ids) == 6
    assert "node_R1_2" in node_ids and "node_R2_2" in node_ids
    # a second node in a region shares that region's geography group
    assert "cc_geo_R1" in rt.sites["node_R1_2"].common_cause_groups
    assert "cc_geo_R1" not in rt.sites["node_R1"].common_cause_groups


def test_md13_four_nodes_are_unchanged(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rt = build_strategy(designs.by_id(StrategyId.S5), product, glob, n_regions=4)
    assert sorted(s for s in rt.sites if s.startswith("node_")) == [
        "node_R1",
        "node_R2",
        "node_R3",
        "node_R4",
    ]


# --------------------------------------------------------------------- MD-9


def test_md9_utilization_denominator_covers_the_sites_the_numerator_counts(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    from telo_feasibility.ablation import (
        network_capacity_units_per_year,
        reserved_capacity_units_per_year,
    )

    for sid in (StrategyId.S3, StrategyId.S7):
        d = designs.by_id(sid)
        total = network_capacity_units_per_year(d, product, glob, 4)
        owned = network_capacity_units_per_year(d, product, glob, 4, include_contracted=False)
        contracted = reserved_capacity_units_per_year(d, product, glob, 4)
        assert contracted > 0.0, sid
        assert total == pytest.approx(owned + contracted), sid
        assert total > owned, sid


# --------------------------------------------------------------------- MD-10, MD-16


def test_md10_an_absent_addin_arm_makes_the_bracket_undefined() -> None:
    import math

    from telo_feasibility.ablation import attribution

    summary = {
        "base|p|S0": {
            "fill_rate": {"mean": 0.9},
            "p_meet": 0.5,
            "shortage_days_per_year": {"mean": 10.0},
            "unmet_units_per_year": {"mean": 5.0},
            "annual_total_cost": {"mean": 1.0},
        },
        "quiet_all|p|S0": {
            "fill_rate": {"mean": 1.0},
            "p_meet": 1.0,
            "shortage_days_per_year": {"mean": 0.0},
            "unmet_units_per_year": {"mean": 0.0},
            "annual_total_cost": {"mean": 1.0},
        },
        "loo:capital_cost|p|S0": {
            "fill_rate": {"mean": 0.9},
            "p_meet": 0.5,
            "shortage_days_per_year": {"mean": 10.0},
            "unmet_units_per_year": {"mean": 5.0},
            "annual_total_cost": {"mean": 0.5},
        },
    }
    rows = {r["factor"]: r for r in attribution(summary) if r["product_id"] == "p"}
    cost_row = rows["capital_cost"]
    assert math.isnan(cost_row["addin_delta_fill_rate"])
    assert math.isnan(cost_row["shapley_bracket_fill_low"])
    assert math.isnan(cost_row["shapley_bracket_fill_high"])


def test_md16_p_meet_carries_its_binomial_standard_error() -> None:
    import math

    from telo_feasibility.ablation import summarize

    rows = [
        {
            "config_id": "base",
            "product_id": "p",
            "strategy_id": "S0",
            "run_index": i,
            "fill_rate": 1.0 if i < 9 else 0.5,
            "shortage_days_per_year": 0.0,
            "unmet_units_per_year": 0.0,
            "annual_total_cost": 1.0,
            "cost_per_delivered_unit": 1.0,
            "capacity_utilization": 0.5,
            "material_stockouts": 0.0,
            "site_failure_days": 0.0,
            "common_cause_days": 0.0,
            "supplier_disruption_days": 0.0,
            "emergency_shipments": 0.0,
            "batches_started_per_year": 1.0,
            "expiry_rate": 0.0,
            "time_to_stable_recovery_median_days": 0.0,
        }
        for i in range(10)
    ]
    entry = summarize(rows, tau=0.99, q=0.9, tau_alt=0.98)["base|p|S0"]
    assert entry["p_meet"] == pytest.approx(0.9)
    assert entry["p_meet_mcse"] == pytest.approx(math.sqrt(0.9 * 0.1 / 10))


def test_site_runtime_ramp_is_inert_by_default() -> None:
    spec = ManufacturingSite(
        id="x",
        name="x",
        region_id="R1",
        archetype="central",
        batch_size_units=100.0,
        batches_per_year_nominal=10.0,
        yield_fraction=1.0,
        uptime_fraction=1.0,
        production_cycle_days=1.0,
        changeover_days=0.0,
        release_time_components_days={},
        capital_usd=0.0,
        fixed_cost_usd_per_year=0.0,
        validation_cost_usd=0.0,
        commissioning_lead_time_days=0.0,
        pathway=Pathway.APPROVED_CMO,
    )
    rt = SiteRuntime(spec=spec, batches_per_year=10.0, serves_region_ids=("R1",))
    assert rt.batches_per_year_on(0) == 10.0
    assert rt.occupancy_days_on(0) == rt.occupancy_days


# --------------------------------------------------------------------- MD-19 (R007)


def test_md19_a_degraded_supplier_stretches_the_order_in_proportion() -> None:
    """A supplier at capacity fraction f takes 1 / f times as long to complete an order.

    Before R007, shipment was gated on ``cap[day] > 0.0``. A common-cause group sets its
    members to ``1 - impact``, which never reaches zero, so a group declared on a supplier
    could not delay a single unit at any parameter value.
    """
    store = MaterialStore(
        site_id="s",
        stock={"api": 0},
        supplier_for={"api": "api_1"},
        lead_time_days={"api": 5.0},
        target_days=10.0,
        reorder_point_days=1.0,
    )
    store.open_orders = [PurchaseOrder("api", "api_1", 1000, 5)]
    cap = {"api_1": np.full(40, 0.25)}
    day = 5
    while store.open_orders and day < 40:
        store.receive(day, cap)
        day += 1
    assert store.stock["api"] == 1000
    # arrival day 5 plus three more days at a quarter of one full order per day
    assert day - 1 == 8


def test_md19_full_and_zero_capacity_are_unchanged() -> None:
    full = MaterialStore(
        site_id="s",
        stock={"api": 0},
        supplier_for={"api": "api_1"},
        lead_time_days={"api": 5.0},
        target_days=10.0,
        reorder_point_days=1.0,
    )
    full.open_orders = [PurchaseOrder("api", "api_1", 1000, 5)]
    assert full.receive(5, {"api_1": np.ones(40)}) == 1000
    assert not full.open_orders

    down = MaterialStore(
        site_id="s",
        stock={"api": 0},
        supplier_for={"api": "api_1"},
        lead_time_days={"api": 5.0},
        target_days=10.0,
        reorder_point_days=1.0,
    )
    down.open_orders = [PurchaseOrder("api", "api_1", 1000, 5)]
    assert down.receive(5, {"api_1": np.zeros(40)}) == 0
    assert down.open_orders and down.delayed_order_days == 1


def test_md19_frozen_comparators_are_unchanged(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """The fix touches only fractional capacity, which S0-S7 never see on a supplier."""
    r, _ = _run(designs.by_id(StrategyId.S2), product, glob, _settings())
    assert r.metrics["fill_rate"] > 0.0  # the digest pin lives in tests/regression


# --------------------------------------------------------------------- MD-20 (R007)


def test_md20_the_screen_credits_a_reserved_line_and_charges_its_contract(product, glob) -> None:  # type: ignore[no-untyped-def]
    """Before R007 a contracted-capacity design screened byte-identical to S0."""
    registry = load_all_strategies()
    s0 = registry.by_id(StrategyId.S0)
    s17 = registry.by_id(StrategyId.S17)
    base = screen_row(product, s0, glob, "corrected")
    contracted = screen_row(product, s17, glob, "corrected")
    assert contracted.saleable_capacity > base.saleable_capacity
    assert contracted.sites > base.sites
    assert contracted.reserved_capacity_cost > 0.0
    # the credit is the exercise duty cycle only, never the whole reserved line
    rt = build_strategy(s17, product, glob)
    full = sum(
        s.batches_per_year
        * s.spec.batch_size_units
        * s.spec.yield_fraction
        * s.spec.uptime_fraction
        for s in rt.sites.values()
    )
    assert contracted.saleable_capacity < full


def test_md20_a_reserved_line_with_no_exercise_cadence_is_credited_nothing(product, glob) -> None:  # type: ignore[no-untyped-def]
    registry = load_all_strategies()
    s17 = registry.by_id(StrategyId.S17)
    with_cadence = screen_row(product, s17, glob, "corrected")
    cold = s17.model_copy(deep=True)
    for plan in cold.site_plans or []:
        plan.exercise_batches_per_year = 0.0
    without = screen_row(product, cold, glob, "corrected")
    assert without.saleable_capacity < with_cadence.saleable_capacity
    assert without.sites == pytest.approx(1.0)  # only the incumbent line is left
    # the fee is still charged: Telo pays for access whether or not it exercises
    assert without.reserved_capacity_cost > 0.0


# --------------------------------------------------------------------- MD-21 (R007)


def test_md21_a_reservation_fee_does_not_accrue_before_the_line_exists(product, glob) -> None:  # type: ignore[no-untyped-def]
    """R005 guarded fixed operations on ``exists(day)`` and did not guard the contract lines."""
    registry = load_all_strategies()
    s16 = registry.by_id(StrategyId.S16)
    early = _settings(horizon_days=300, warm_up_days=0)
    late = _settings(horizon_days=900, warm_up_days=0)
    r_early, rt = _run(s16, product, glob, early)
    r_late, _ = _run(s16, product, glob, late)
    assert all(not s.exists(299) for s in rt.sites.values() if s.reserved)
    assert any(s.exists(899) for s in rt.sites.values() if s.reserved)
    assert r_early.ledger.resilience_contracts == pytest.approx(0.0)
    assert r_late.ledger.resilience_contracts > 0.0


# ---------------------------------------------------------------------------
# MD-17 (revision R008): the commissioning clock must run inside the measured window
# ---------------------------------------------------------------------------


def test_md17_commissioning_clock_starts_at_the_measured_window(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    """A lead time at or below the warm-up period used to cost nothing that was measured."""
    from telo_feasibility.simulation import SimSettings, run_paired

    def loss(flag: bool) -> dict[str, float]:
        st = SimSettings(
            horizon_days=365 + 1826,
            warm_up_days=365,
            shortage_day_threshold=0.95,
            fill_rate_mean_min=0.99,
            recovery_window_days=30,
            record_events=False,
            commissioning_from_measurement_start=flag,
        )
        return {
            r.strategy_id: r.metrics["capacity_days_lost_to_commissioning_fraction"]
            for r in run_paired(designs.designs, product, glob, st, 20260901, [0])
        }

    before, after = loss(False), loss(True)
    # S2's second source qualifies in 365 days, exactly the warm-up period, so before the
    # fix it opened on the first measured day and its lead time was invisible
    assert before["S2"] == pytest.approx(0.0)
    assert after["S2"] > 0.05
    # every build strategy loses strictly more of the window once the clock is honest
    for sid in ("S2", "S4", "S5", "S6"):
        assert after[sid] > before[sid], sid
    # strategies that build nothing are untouched
    for sid in ("S0", "S1", "S7"):
        assert after[sid] == before[sid] == pytest.approx(0.0), sid


def test_md17_metric_is_capacity_weighted_and_bounded(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    from telo_feasibility.schemas import StrategyId
    from telo_feasibility.simulation import SimSettings, run_paired

    st = SimSettings(
        horizon_days=365 + 1826,
        warm_up_days=365,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=False,
    )
    for r in run_paired(designs.designs, product, glob, st, 20260901, [0]):
        v = r.metrics["capacity_days_lost_to_commissioning_fraction"]
        assert 0.0 <= v <= 1.0, (r.strategy_id, v)
    # a design whose nodes never arrive inside the horizon loses almost the whole window
    d = designs.by_id(StrategyId.S5).model_copy(deep=True)
    d.design_variables["sites"] = 4
    g = glob.model_copy(deep=True)
    g.parameters["node_commissioning_days"].high = 100_000.0
    g.parameters["node_commissioning_days"].base = 100_000.0
    late = run_paired([d], product, g, st, 20260901, [0])[0]
    assert late.metrics["capacity_days_lost_to_commissioning_fraction"] > 0.5
