"""Protocol Appendix C falsification tests on the daily engine."""

from __future__ import annotations

import math

import pytest

from telo_feasibility.configs import ProductConfig
from telo_feasibility.release_assurance import ReleaseAssuranceParams
from telo_feasibility.schemas import ParameterSet, ReleaseScenario, StrategyDesign, StrategyId
from telo_feasibility.simulation import SimSettings, run_paired, simulate_run, world_for_run
from telo_feasibility.strategies import build_strategy

from .conftest import override, quiet


def _run(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    seed: int = 7,
    ra: ReleaseAssuranceParams | None = None,
):  # type: ignore[no-untyped-def]
    world, streams = world_for_run(glob, settings, seed, 0)
    rt = build_strategy(design, product, glob, n_regions=settings.n_regions, release_assurance=ra)
    return simulate_run(rt, product, glob, world, streams, settings)


def _design(designs, sid: StrategyId, **dv: float) -> StrategyDesign:  # type: ignore[no-untyped-def]
    d = designs.by_id(sid).model_copy(deep=True)
    d.design_variables.update(dv)
    return d


def test_zero_demand_no_shortage_no_variable_cost_fixed_cost_remains(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    p = ProductConfig(
        product.presentation, override(product.parameters, annual_demand_units=0.0), product.path
    )
    r = _run(designs.by_id(StrategyId.S0), p, quiet(glob), settings)
    assert r.metrics["fill_rate"] == 1.0
    assert r.metrics["shortage_days"] == 0
    assert r.metrics["batches_started_per_year"] == 0
    assert r.ledger.variable_production == 0
    assert r.ledger.fixed_site_operations > 0 and r.ledger.capital_annualized > 0


def test_zero_capacity_serves_only_initial_stock(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    r = _run(_design(designs, StrategyId.S0, capacity_factor=0.0), product, quiet(glob), settings)
    assert r.metrics["batches_started_per_year"] == 0
    assert r.counters.served_units <= r.counters.initial_units
    assert r.metrics["fill_rate"] < 0.5


def test_infinite_supply_fill_rate_approaches_one(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    """Appendix C: ample capacity serves everything.

    ``instant_expansion`` is set because this case is about the capacity level, not about
    how long capacity takes to build. Since revision R004 (MD-7) capacity above the
    status-quo scale is commissioned over ``capacity_expansion_days``, which is longer than
    this short horizon, so without the switch the case would be testing the ramp instead.
    """
    r = _run(
        _design(
            designs,
            StrategyId.S0,
            capacity_factor=50.0,
            safety_stock_days=60.0,
            instant_expansion=1.0,
        ),
        product,
        quiet(glob),
        settings,
    )
    assert r.metrics["fill_rate"] > 0.999
    assert r.metrics["shortage_days"] == 0


def test_no_failures_reproduces_deterministic_throughput(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    # instant_expansion for the same reason as the infinite-supply case: the throughput
    # identity is about the steady state, not about the R004 commissioning ramp
    r = _run(
        _design(
            designs,
            StrategyId.S0,
            capacity_factor=2.0,
            safety_stock_days=45.0,
            instant_expansion=1.0,
        ),
        product,
        q,
        settings,
    )
    demand_per_year = product.parameters.base("annual_demand_units")
    units_per_batch = product.parameters.base("units_per_batch") * product.parameters.base(
        "yield_fraction"
    )
    expected_batches = demand_per_year / units_per_batch
    # whole-horizon batch rate must track demand within 20% once initial stock is netted out
    assert abs(r.metrics["batches_started_per_year"] - expected_batches) / expected_batches < 0.2
    assert r.metrics["fill_rate"] > 0.98


def test_independent_sites_help_and_perfectly_correlated_sites_do_not(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    settings = SimSettings(
        horizon_days=800,
        warm_up_days=200,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=False,
    )
    base = override(
        quiet(glob),
        node_commissioning_days=0.0,
        site_failure_duration_days=90.0,
        common_cause_duration_days=90.0,
    )
    s0 = designs.by_id(StrategyId.S0)
    s5 = _design(designs, StrategyId.S5, node_scale=0.5)
    # idiosyncratic failures only: node redundancy should raise fill relative to status quo
    indep = override(
        base,
        site_failures_per_site_year=3.0,
        common_cause_events_per_year=0.0,
        site_failure_residual_capacity=0.0,
    )
    r0i, r5i = run_paired([s0, s5], product, indep, settings, master_seed=3, run_indices=[0])
    # common-cause failures only (all sites share cc_api_1): redundancy buys nothing
    corr = override(
        base,
        site_failures_per_site_year=0.0,
        common_cause_events_per_year=3.0,
        common_cause_capacity_impact=0.999,
        common_cause_capacity_impact_sd=0.0005,
    )
    r0c, r5c = run_paired([s0, s5], product, corr, settings, master_seed=3, run_indices=[0])
    gain_indep = r5i.metrics["fill_rate"] - r0i.metrics["fill_rate"]
    gain_corr = r5c.metrics["fill_rate"] - r0c.metrics["fill_rate"]
    assert r5i.metrics["site_failure_days"] > 0 and r5c.metrics["common_cause_days"] > 0
    assert gain_indep > gain_corr
    assert gain_indep > 0.0


def test_zero_shelf_life_makes_stockpiling_infeasible(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    p = ProductConfig(
        product.presentation, override(product.parameters, shelf_life_months=0.0), product.path
    )
    r = _run(_design(designs, StrategyId.S1, capacity_factor=2.0), p, quiet(glob), settings)
    assert r.metrics["expiry_rate"] > 0.9
    assert r.metrics["fill_rate"] < 0.1


def test_infinite_shelf_life_has_no_expiry_but_carrying_cost(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    p = ProductConfig(
        product.presentation, override(product.parameters, shelf_life_months=1e5), product.path
    )
    r = _run(_design(designs, StrategyId.S1, capacity_factor=2.0), p, quiet(glob), settings)
    assert r.counters.expired_units == 0
    assert r.ledger.failure_waste == 0.0
    assert r.ledger.inventory_logistics > 0.0


def test_release_assurance_with_zero_benefit_reduces_to_conventional(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    d = _design(designs, StrategyId.S6, capacity_factor=2.0)
    r0 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(scenario=ReleaseScenario.R0, release_time_cv=0.0),
    )
    r1 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(
            scenario=ReleaseScenario.R1, admin_reduction_days=0.0, release_time_cv=0.0
        ),
    )
    r2 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(
            scenario=ReleaseScenario.R2, released_fraction=0.5, release_time_cv=0.0
        ),
    )
    for r in (r1, r2):
        for k in ("fill_rate", "shortage_days", "batches_started_per_year", "served_units"):
            assert r.metrics[k] == r0.metrics[k], k
        assert (
            r.ledger.os_integration > r0.ledger.os_integration
        )  # R1/R2 still pay integration cost
    assert r2.metrics["abstentions"] > 0  # counted, not acted on


def test_total_abstention_has_no_release_time_benefit(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    q = quiet(glob)
    d = _design(designs, StrategyId.S6, capacity_factor=2.0)
    r0 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(scenario=ReleaseScenario.R0, release_time_cv=0.0),
    )
    r3 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(
            scenario=ReleaseScenario.R3,
            permitted=True,
            released_fraction=0.0,
            fallback_investigation_days=5.0,
            release_time_cv=0.0,
        ),
    )
    assert r3.metrics["abstentions"] == r3.counters.batches_started
    assert r3.metrics["wrong_releases"] == 0
    assert r3.metrics["fill_rate"] <= r0.metrics["fill_rate"]
    assert r3.metrics["served_units"] <= r0.metrics["served_units"]


def test_full_release_assurance_saves_no_days_when_sterility_binds(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    """H7 mechanism: removing the assay component changes nothing while the 14-day sterility incubation is the critical path."""
    q = quiet(glob)
    d = _design(designs, StrategyId.S6, capacity_factor=2.0)
    r0 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(scenario=ReleaseScenario.R0, release_time_cv=0.0),
    )
    r3 = _run(
        d,
        product,
        q,
        settings,
        ra=ReleaseAssuranceParams(
            scenario=ReleaseScenario.R3,
            permitted=True,
            released_fraction=1.0,
            conditional_error=0.0,
            release_time_cv=0.0,
        ),
    )
    assert r3.metrics["abstentions"] == 0
    assert r3.metrics["served_units"] == r0.metrics["served_units"]
    assert r3.metrics["fill_rate"] == r0.metrics["fill_rate"]
    # and when sterility is short (rapid micro validated) the same layer does save time
    fast = override(q, sterility_incubation_days=2.0, environmental_monitoring_days=2.0)
    f0 = _run(
        d,
        product,
        fast,
        settings,
        ra=ReleaseAssuranceParams(scenario=ReleaseScenario.R0, release_time_cv=0.0),
    )
    f3 = _run(
        d,
        product,
        fast,
        settings,
        ra=ReleaseAssuranceParams(
            scenario=ReleaseScenario.R3, permitted=True, released_fraction=1.0, release_time_cv=0.0
        ),
    )
    assert f3.counters.batches_started >= f0.counters.batches_started


def test_r3_cannot_be_instantiated_without_permission() -> None:
    with pytest.raises(ValueError, match="regulatory gates permit"):
        ReleaseAssuranceParams(scenario=ReleaseScenario.R3, permitted=False, released_fraction=0.5)


def test_metrics_are_finite_and_ledgers_nonnegative(product, glob, designs, settings) -> None:  # type: ignore[no-untyped-def]
    for d in designs.designs:
        r = _run(d, product, glob, settings)
        for k, v in r.metrics.items():
            assert not math.isnan(v), k
        r.ledger.check_nonnegative()
