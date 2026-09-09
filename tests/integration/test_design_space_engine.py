"""Engine behavior of configuration-declared strategies (S8+).

Covers: the generic capacity formula against the frozen S5 node quirk, roster and world
invariance when design-space entities are added, frozen digests unchanged in mixed batches,
warm-standby exercise batches and activation failure, a hub acting as a bulk supplier,
portfolio shares, and the ``serves`` field.
"""

from __future__ import annotations

import numpy as np

from telo_feasibility.configs import ProductConfig
from telo_feasibility.schemas import (
    ParameterSet,
    SitePlanSpec,
    StrategyDesign,
    StrategyId,
    SupplierSpec,
)
from telo_feasibility.simulation import SimSettings, _Sim, run_paired, simulate_run, world_for_run
from telo_feasibility.strategies import build_strategy, universal_roster_ids

from .conftest import override, quiet

CENTRAL_GROUPS = ["cc_api_1", "cc_vial_1", "cc_geo_R1"]
NODE_GROUPS = ["cc_api_1", "cc_vial_1", "cc_os", "cc_quality"]


def _s8(
    plans: list[SitePlanSpec],
    dv: dict[str, float],
    *,
    sid: StrategyId = StrategyId.S8,
    extra: list[SupplierSpec] | None = None,
) -> StrategyDesign:
    return StrategyDesign(
        id=sid,
        name=f"{sid.value} test",
        pathway="approved_cmo",
        durable=True,
        family="test",
        design_variables=dict(dv),
        site_plans=plans,
        extra_suppliers=extra or [],
    )


def _central(scale: float = 1.0, **kw: object) -> SitePlanSpec:
    return SitePlanSpec(
        id="central", region_id="R1", archetype="central", scale=scale, groups=CENTRAL_GROUPS, **kw
    )


def _s5_replica(dv: dict[str, float]) -> StrategyDesign:
    plans = [_central(1.0)]
    for r in ("R1", "R2", "R3", "R4"):
        plans.append(
            SitePlanSpec(
                id=f"node_{r}",
                region_id=r,
                archetype="regional_node",
                scale=1.0,
                exists_at_t0=False,
                serves="own_region",
                groups=NODE_GROUPS,
            )
        )
    return _s8(plans, dv)


def _run(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    seed: int = 3,
):  # type: ignore[no-untyped-def]
    return run_paired([design], product, glob, settings, seed, [0])[0]


# ------------------------------------------------------------------ capacity formulas


def test_generic_builder_reproduces_s5_when_capacity_factor_is_one(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    """With capacity_factor = 1 the declared replica and frozen S5 build identical runtimes.

    Frozen S5 fixes the central plant at scale 1.0 and gives nodes cadence nominal x
    capacity_factor with batch size x node_scale x capacity_factor (capacity_factor enters
    twice). The generic formula is capacity = nominal x scale with batch fraction = scale.
    The two agree only at capacity_factor = 1; the divergence is asserted in the next test.
    """
    dv = {"capacity_factor": 1.0, "node_scale": 0.35, "safety_stock_days": 45.0}
    q = override(quiet(glob), node_commissioning_days=50.0)
    s5 = designs.by_id(StrategyId.S5).model_copy(deep=True)
    s5.design_variables.update(dv)
    replica = _s5_replica(dv)
    rt5 = build_strategy(s5, product, q, n_regions=4)
    rt8 = build_strategy(replica, product, q, n_regions=4)
    assert set(rt5.sites) == set(rt8.sites)
    for sid in rt5.sites:
        assert rt5.sites[sid].batches_per_year == rt8.sites[sid].batches_per_year, sid
        assert rt5.sites[sid].spec.batch_size_units == rt8.sites[sid].spec.batch_size_units, sid
        assert rt5.sites[sid].serves_region_ids == rt8.sites[sid].serves_region_ids, sid
        assert rt5.sites[sid].available_from_day == rt8.sites[sid].available_from_day, sid
    r5, r8 = run_paired([s5, replica], product, q, settings, 3, [0])
    assert r5.metrics["served_units"] == r8.metrics["served_units"]
    assert r5.metrics["fill_rate"] == r8.metrics["fill_rate"]
    assert r5.event_digest == r8.event_digest


def test_generic_and_frozen_node_formulas_diverge_at_capacity_factor_above_one(
    product, glob, designs
) -> None:  # type: ignore[no-untyped-def]
    dv = {"capacity_factor": 1.35, "node_scale": 0.35, "safety_stock_days": 45.0}
    s5 = designs.by_id(StrategyId.S5).model_copy(deep=True)
    s5.design_variables.update(dv)
    rt5 = build_strategy(s5, product, glob, n_regions=4)
    rt8 = build_strategy(_s5_replica(dv), product, glob, n_regions=4)
    nominal = product.parameters.base("batches_per_site_year_nominal")
    units = product.parameters.base("units_per_batch")
    node_scale = 0.35 * 1.35
    # frozen quirk: cadence nominal x capacity_factor, central fixed at scale 1.0
    assert rt5.sites["node_R2"].batches_per_year == nominal * 1.35
    assert rt5.sites["node_R2"].spec.batch_size_units == max(round(units * node_scale), 1)
    assert rt5.sites["central"].batches_per_year == nominal * 1.0
    # generic: capacity nominal x scale, batch fraction = scale, so cadence is nominal
    assert rt8.sites["node_R2"].batches_per_year == nominal * node_scale / node_scale
    assert rt8.sites["node_R2"].spec.batch_size_units == max(round(units * node_scale), 1)
    assert rt8.sites["central"].batches_per_year == nominal * 1.35
    assert rt5.sites["node_R2"].batches_per_year != rt8.sites["node_R2"].batches_per_year


# ------------------------------------------------------------------ roster and worlds


def _hub_design(dv: dict[str, float] | None = None) -> StrategyDesign:
    plans = [
        _central(1.5),
        SitePlanSpec(
            id="spoke_r2",
            region_id="R2",
            archetype="regional_node",
            scale=0.5,
            serves="own_region",
            api_supplier="hub_bulk",
            groups=["cc_hub"],
        ),
    ]
    hub = SupplierSpec(
        id="hub_bulk",
        name="hub bulk solution",
        component_ids=["api"],
        lead_time_days=20.0,
        groups=["cc_hub"],
    )
    return _s8(plans, dv or {"capacity_factor": 1.0, "safety_stock_days": 30.0}, extra=[hub])


def test_roster_appends_declared_entities_after_frozen_ones(glob, settings) -> None:  # type: ignore[no-untyped-def]
    base = universal_roster_ids(4)
    ext = universal_roster_ids(4, [_hub_design()])
    assert ext.site_ids[: len(base.site_ids)] == base.site_ids
    assert ext.supplier_ids[: len(base.supplier_ids)] == base.supplier_ids
    assert ext.group_ids[: len(base.group_ids)] == base.group_ids
    assert (
        "spoke_r2" in ext.site_ids and "hub_bulk" in ext.supplier_ids and "cc_hub" in ext.group_ids
    )
    assert "central" in ext.site_ids and ext.site_ids.count("central") == 1
    assert set(base.lane_ids) < set(ext.lane_ids)
    wa, _ = world_for_run(glob, settings, 5, 2)
    wb, _ = world_for_run(glob, settings, 5, 2, [_hub_design()])
    for sid in base.site_ids:
        assert (wa.site_capacity[sid] == wb.site_capacity[sid]).all()
    for sup in base.supplier_ids:
        assert (wa.supplier_capacity[sup] == wb.supplier_capacity[sup]).all()
    for gid in base.group_ids:
        assert (wa.group_capacity[gid] == wb.group_capacity[gid]).all()
    for r in base.region_ids:
        assert (wa.routine_demand_multiplier[r] == wb.routine_demand_multiplier[r]).all()
        assert (wa.shock_multiplier[r] == wb.shock_multiplier[r]).all()
    for lid in base.lane_ids:
        assert (wa.transport_multiplier[lid] == wb.transport_multiplier[lid]).all()
    assert (wa.shortage_listed == wb.shortage_listed).all()
    assert "hub_bulk" in wb.supplier_capacity and "spoke_r2" in wb.site_capacity


def test_frozen_results_unchanged_with_design_space_strategy_in_batch(
    product, glob, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    s0, s5 = designs.by_id(StrategyId.S0), designs.by_id(StrategyId.S5)
    alone = run_paired([s0, s5], product, glob, settings, 7, [0, 1])
    mixed = run_paired([s0, s5, _hub_design()], product, glob, settings, 7, [0, 1])
    by_alone = {(r.strategy_id, r.run_index): r for r in alone}
    by_mixed = {(r.strategy_id, r.run_index): r for r in mixed}
    for key, r in by_alone.items():
        assert by_mixed[key].event_digest == r.event_digest, key
        assert by_mixed[key].metrics == r.metrics, key
    assert ("S8", 0) in by_mixed


# ------------------------------------------------------------------ warm standby


def _standby(
    exercise: float, p_fail: float, central_groups: list[str] | None = None
) -> StrategyDesign:
    plans = [
        SitePlanSpec(
            id="central",
            region_id="R1",
            archetype="central",
            scale=2.0,
            groups=central_groups if central_groups is not None else CENTRAL_GROUPS,
        ),
        SitePlanSpec(
            id="backup_cdmo",
            region_id="R2",
            archetype="cdmo_reserved",
            scale=1.5,
            reserved=True,
            exercise_batches_per_year=exercise,
            activation_failure_probability=p_fail,
            groups=[],
        ),
    ]
    return _s8(plans, {"capacity_factor": 1.0, "safety_stock_days": 30.0, "campaign_batches": 6.0})


def test_warm_standby_exercises_on_cadence_without_activating(product, glob, settings) -> None:  # type: ignore[no-untyped-def]
    """Exercise batches run on the declared cadence at the reserved site and their output
    goes to stock; the central plant then starts fewer batches (its position reaches target
    sooner), so total batches do not simply add up."""
    q = quiet(glob)
    interval = max(round(365.25 / 4.0), 1)
    expected = len(range(0, settings.horizon_days, interval))
    runs = {}
    for label, exercise in (("with", 4.0), ("without", 0.0)):
        d = _standby(exercise, 0.0)
        d.design_variables["activation_threshold_days"] = 0.0  # never request activation
        world, streams = world_for_run(q, settings, 3, 0, [d])
        rt = build_strategy(d, product, q, n_regions=settings.n_regions)
        runs[label] = (rt, simulate_run(rt, product, q, world, streams, settings))
    rt_w, r_w = runs["with"]
    rt_o, r_o = runs["without"]
    assert r_w.metrics["exercise_batches"] == expected
    assert rt_w.sites["backup_cdmo"].batches_started == expected
    assert rt_o.sites["backup_cdmo"].batches_started == 0 and r_o.metrics["exercise_batches"] == 0
    assert r_w.metrics["activations"] == 0 and r_w.metrics["activation_failures"] == 0
    assert r_w.metrics["served_units"] >= r_o.metrics["served_units"]
    assert rt_w.sites["central"].batches_started <= rt_o.sites["central"].batches_started
    assert (
        r_w.counters.produced_filled
        == r_o.counters.produced_filled
        + (rt_w.sites["central"].batches_started - rt_o.sites["central"].batches_started)
        * rt_w.sites["central"].spec.batch_size_units
        + expected * rt_w.sites["backup_cdmo"].spec.batch_size_units
    )


def test_activation_failure_probability_orders_fill_and_counts(product, glob, settings) -> None:  # type: ignore[no-untyped-def]
    """Central plant knocked out by common-cause events on a group only it belongs to; the
    reserved site is requested when days of supply fall below the threshold."""
    forcing = override(
        quiet(glob),
        common_cause_events_per_year=4.0,
        common_cause_duration_days=90.0,
        common_cause_capacity_impact=0.999,
        common_cause_capacity_impact_sd=0.0005,
    )
    results = {}
    for p in (0.0, 0.5, 1.0):
        d = _standby(0.0, p, central_groups=["cc_geo_R1"])
        d.design_variables["activation_threshold_days"] = 45.0
        rs = run_paired([d], product, forcing, settings, 11, [0, 1, 2])
        results[p] = {
            "fill": float(np.mean([x.metrics["fill_rate"] for x in rs])),
            "activations": sum(x.metrics["activations"] for x in rs),
            "failures": sum(x.metrics["activation_failures"] for x in rs),
            "cc_days": sum(x.metrics["common_cause_days"] for x in rs),
        }
    assert results[0.0]["cc_days"] > 0
    assert results[0.0]["activations"] > 0 and results[0.0]["failures"] == 0
    assert results[1.0]["activations"] == 0 and results[1.0]["failures"] > 0
    assert results[0.5]["activations"] > 0 and results[0.5]["failures"] > 0
    assert results[0.0]["fill"] >= results[0.5]["fill"] >= results[1.0]["fill"]
    assert results[0.0]["fill"] > results[1.0]["fill"]


# ------------------------------------------------------------------ hub as supplier


def test_hub_bulk_supplier_feeds_the_spoke(product, glob, settings) -> None:  # type: ignore[no-untyped-def]
    d = _hub_design()
    rt = build_strategy(d, product, glob, n_regions=4)
    assert rt.topology.supplier("hub_bulk").lead_time_days.base == 20.0
    assert rt.sites["spoke_r2"].supplier_ids == ("hub_bulk", "vial_1", "stopper_1")
    assert rt.sites["spoke_r2"].serves_region_ids == ("R2",)
    assert any(
        g.id == "cc_hub" and "hub_bulk" in g.member_ids and "spoke_r2" in g.member_ids
        for g in rt.topology.common_cause_groups
    )
    world, streams = world_for_run(glob, settings, 3, 0, [d])
    sim = _Sim(rt, product, glob, world, streams, settings)
    assert sim.materials["spoke_r2"].lead_time_days["api"] == 20.0
    assert sim.materials["spoke_r2"].supplier_for["api"] == "hub_bulk"
    assert sim.materials["central"].supplier_for["api"] == "api_1"
    r = simulate_run(rt, product, quiet(glob), world, streams, settings)
    assert r.metrics["fill_rate"] > 0.5
    forcing = override(
        quiet(glob),
        supplier_disruptions_per_supplier_year=8.0,
        supplier_disruption_duration_days=150.0,
    )
    rf = _run(d, product, forcing, settings)
    assert rf.metrics["supplier_disruption_days"] > 0
    assert rf.metrics["material_stockouts"] > 0


# ------------------------------------------------------------------ portfolio shares


def test_portfolio_shares_scale_capacity_and_fixed_cost(product, glob) -> None:  # type: ignore[no-untyped-def]
    def design(cap: float, cost: float) -> StrategyDesign:
        node = SitePlanSpec(
            id="node_r2",
            region_id="R2",
            archetype="regional_node",
            scale=0.5,
            serves="own_region",
            groups=NODE_GROUPS,
            portfolio_capacity_share=cap,
            portfolio_fixed_cost_share=cost,
        )
        return _s8([_central(1.0), node], {"capacity_factor": 1.0})

    full = build_strategy(design(1.0, 1.0), product, glob, n_regions=4)
    half_cap = build_strategy(design(0.5, 1.0), product, glob, n_regions=4)
    half_cost = build_strategy(design(1.0, 0.5), product, glob, n_regions=4)
    assert (
        half_cap.sites["node_r2"].batches_per_year == full.sites["node_r2"].batches_per_year * 0.5
    )
    assert (
        half_cap.sites["node_r2"].spec.batch_size_units
        == full.sites["node_r2"].spec.batch_size_units
    )
    assert half_cap.site_fixed_usd_per_year["node_r2"] == full.site_fixed_usd_per_year["node_r2"]
    assert half_cost.sites["node_r2"].batches_per_year == full.sites["node_r2"].batches_per_year
    for table in ("site_fixed_usd_per_year", "site_capital_usd", "site_validation_usd"):
        assert getattr(half_cost, table)["node_r2"] == getattr(full, table)["node_r2"] * 0.5, table
        assert getattr(half_cost, table)["central"] == getattr(full, table)["central"], table
    assert half_cap.sites["central"].batches_per_year == full.sites["central"].batches_per_year


# ------------------------------------------------------------------ serves


def test_serves_own_region_restricts_production_sizing_not_fallback_shipping(
    product, glob, settings
) -> None:  # type: ignore[no-untyped-def]
    """``serves`` sets which regions a site sizes production for (and its local priority);
    regions without a serving site still source from any existing site as a fallback
    (``others`` in the source order), so their fill does not go to zero."""
    own = _s8(
        [_central(1.0, serves="own_region")], {"capacity_factor": 1.0, "safety_stock_days": 30.0}
    )
    every = _s8([_central(1.0, serves="all")], {"capacity_factor": 1.0, "safety_stock_days": 30.0})
    rt_own = build_strategy(own, product, glob, n_regions=4)
    rt_all = build_strategy(every, product, glob, n_regions=4)
    assert rt_own.sites["central"].serves_region_ids == ("R1",)
    assert rt_all.sites["central"].serves_region_ids == ("R1", "R2", "R3", "R4")
    rt_own.topology.validate()
    assert rt_own.region_policies["R2"].source_order == ["central"]
    assert rt_own.region_policies["R1"].source_order == ["central"]
    q = quiet(glob)
    r_own, r_all = run_paired([own, every], product, q, settings, 3, [0])
    assert r_own.metrics["fill_rate"] < r_all.metrics["fill_rate"]
    # fallback sourcing keeps every region above zero; proportional allocation gives the
    # served region no priority (measured: R1 0.304 vs R2 0.317 on this seed)
    assert all(v["fill_rate"] > 0.0 for v in r_own.regional.values())
    assert r_own.metrics["fill_rate"] < 0.5
