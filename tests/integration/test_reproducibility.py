"""Seed reproduction, common random numbers, entity isolation, mass balance under random designs."""

from __future__ import annotations

from hypothesis import given
from hypothesis import settings as hsettings
from hypothesis import strategies as st

from telo_feasibility.disruptions import Roster, WorldParams, generate_world
from telo_feasibility.rng import RunStreams
from telo_feasibility.schemas import StrategyId
from telo_feasibility.simulation import SimSettings, run_paired, world_for_run
from telo_feasibility.strategies import universal_roster_ids


def test_same_seed_same_events_different_seed_different_events(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    a = run_paired(
        [designs.by_id(StrategyId.S2)], product, glob, settings, master_seed=11, run_indices=[0]
    )[0]
    b = run_paired(
        [designs.by_id(StrategyId.S2)], product, glob, settings, master_seed=11, run_indices=[0]
    )[0]
    c = run_paired(
        [designs.by_id(StrategyId.S2)], product, glob, settings, master_seed=12, run_indices=[0]
    )[0]
    assert a.event_digest == b.event_digest and a.metrics == b.metrics
    assert a.event_digest != c.event_digest


def test_common_random_numbers_world_identical_across_strategies(glob, settings) -> None:  # type: ignore[no-untyped-def]
    w1, _ = world_for_run(glob, settings, 5, 3)
    w2, _ = world_for_run(glob, settings, 5, 3)
    w3, _ = world_for_run(glob, settings, 5, 4)
    assert w1.digest() == w2.digest()
    assert w1.digest() != w3.digest()


def test_adding_an_entity_does_not_change_other_entities_draws(glob, settings) -> None:  # type: ignore[no-untyped-def]
    params = WorldParams.from_parameters(glob, settings.horizon_days, False)
    base = universal_roster_ids(4)
    extra = Roster(
        base.region_ids,
        (*base.site_ids, "extra_site"),
        (*base.supplier_ids, "extra_supplier"),
        base.lane_ids,
        base.group_ids,
    )
    wa = generate_world(params, base, RunStreams(9, 0))
    wb = generate_world(params, extra, RunStreams(9, 0))
    for sid in base.site_ids:
        assert (wa.site_capacity[sid] == wb.site_capacity[sid]).all()
    for sup in base.supplier_ids:
        assert (wa.supplier_capacity[sup] == wb.supplier_capacity[sup]).all()
    for r in base.region_ids:
        assert (wa.routine_demand_multiplier[r] == wb.routine_demand_multiplier[r]).all()
    assert "extra_site" in wb.site_capacity


def test_paired_strategies_share_demand_and_disruptions(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    res = run_paired(
        [designs.by_id(StrategyId.S0), designs.by_id(StrategyId.S1)],
        product,
        glob,
        settings,
        master_seed=2,
        run_indices=[0, 1],
    )
    by = {(r.strategy_id, r.run_index): r for r in res}
    for run in (0, 1):
        assert (by[("S0", run)].daily_demand == by[("S1", run)].daily_demand).all()
        assert (
            by[("S0", run)].metrics["site_failure_days"]
            == by[("S1", run)].metrics["site_failure_days"]
        )


@given(
    sites=st.integers(min_value=1, max_value=3),
    capacity=st.floats(min_value=0.3, max_value=3.0),
    safety=st.floats(min_value=3.0, max_value=120.0),
    seed=st.integers(min_value=0, max_value=1000),
)
@hsettings(max_examples=12, deadline=None)
def test_property_mass_balance_and_nonnegativity_hold(
    sites: int, capacity: float, safety: float, seed: int
) -> None:
    from telo_feasibility.configs import load_global, load_products, load_strategies

    glob = load_global()
    product = load_products()["norepinephrine_1mgml_4ml"]
    d = load_strategies().by_id(StrategyId.S2).model_copy(deep=True)
    d.design_variables.update(
        {
            "sites": float(sites),
            "capacity_factor": capacity,
            "safety_stock_days": safety,
            "second_source_exists_at_t0": 1.0,
        }
    )
    s = SimSettings(
        horizon_days=150,
        warm_up_days=30,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )
    r = run_paired([d], product, glob, s, master_seed=seed, run_indices=[0])[
        0
    ]  # asserts mass balance daily
    assert r.counters.served_units >= 0 and r.counters.expired_units >= 0
    assert 0.0 <= r.metrics["fill_rate"] <= 1.0
