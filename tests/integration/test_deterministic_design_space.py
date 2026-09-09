"""The deterministic screen for design-space strategies: runtime topology, not multipliers."""

from __future__ import annotations

import pytest

from telo_feasibility.deterministic import screen_inputs, screen_row
from telo_feasibility.schemas import (
    DesignVariableSpec,
    Pathway,
    SitePlanSpec,
    StrategyDesign,
    StrategyId,
)
from telo_feasibility.strategies import build_strategy


def _s8(**kw: object) -> StrategyDesign:
    dv = dict(kw.pop("design_variables", {}))  # type: ignore[arg-type]
    plans = kw.pop(
        "site_plans",
        [
            SitePlanSpec(
                id="central",
                region_id="R1",
                archetype="central",
                scale=1.0,
                exists_at_t0=True,
                groups=["cc_api_1", "cc_vial_1", "cc_geo_R1"],
            ),
            SitePlanSpec(
                id="node_R2",
                region_id="R2",
                archetype="regional_node",
                scale=0.5,
                exists_at_t0=False,
                serves="own_region",
                groups=["cc_api_1", "cc_os", "cc_quality"],
            ),
        ],
    )
    return StrategyDesign(
        id=StrategyId.S8,
        name="test topology",
        pathway=Pathway.APPROVED_CMO,
        durable=True,
        family="test",
        site_plans=plans,  # type: ignore[arg-type]
        design_space=[DesignVariableSpec(name="safety_stock_days", low=10.0, high=90.0)],
        design_variables={"safety_stock_days": 45.0, **dv},
        **kw,  # type: ignore[arg-type]
    )


def test_replica_mode_refuses_a_declared_topology(product, glob) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError, match="workbook replica has no arithmetic"):
        screen_row(product, _s8(), glob, "workbook_replica")


def test_screen_inputs_come_from_the_built_runtime(product, glob) -> None:  # type: ignore[no-untyped-def]
    d = _s8()
    si = screen_inputs(product, d, glob)
    rt = build_strategy(d, product, glob)
    assert si.source == "runtime_topology"
    assert si.sites == 2.0
    expected = sum(
        s.batches_per_year
        * s.spec.batch_size_units
        * s.spec.yield_fraction
        * s.spec.uptime_fraction
        for s in rt.sites.values()
    )
    assert si.saleable_capacity == pytest.approx(expected)
    assert si.capital_total == pytest.approx(sum(rt.site_capital_usd.values()))
    assert si.fixed_total == pytest.approx(sum(rt.site_fixed_usd_per_year.values()))
    # both sites share the API supplier, so one event can take out the whole network
    assert si.common_impact_factor == pytest.approx(1.0)


def test_independent_api_lowers_the_common_impact_factor(product, glob) -> None:  # type: ignore[no-untyped-def]
    plans = [
        SitePlanSpec(
            id="central",
            region_id="R1",
            archetype="central",
            scale=1.0,
            exists_at_t0=True,
            api_supplier="api_1",
            groups=["cc_api_1"],
        ),
        SitePlanSpec(
            id="second_source",
            region_id="R2",
            archetype="central",
            scale=1.0,
            exists_at_t0=True,
            api_supplier="api_2",
            groups=["cc_api_2"],
        ),
    ]
    si = screen_inputs(product, _s8(site_plans=plans), glob)
    assert si.common_impact_factor == pytest.approx(0.5)


def test_reserved_capacity_is_not_counted_as_capacity(product, glob) -> None:  # type: ignore[no-untyped-def]
    plans = [
        SitePlanSpec(
            id="central",
            region_id="R1",
            archetype="central",
            scale=1.0,
            exists_at_t0=True,
            groups=["cc_api_1"],
        ),
        SitePlanSpec(
            id="reserved_cdmo",
            region_id="R2",
            archetype="cdmo_reserved",
            scale=1.0,
            exists_at_t0=True,
            reserved=True,
            groups=["cc_api_1"],
        ),
    ]
    si = screen_inputs(product, _s8(site_plans=plans), glob)
    one = screen_inputs(product, _s8(site_plans=plans[:1]), glob)
    assert si.sites == 1.0
    assert si.saleable_capacity == pytest.approx(one.saleable_capacity)
    # Since revision R004 (MD-14) a reserved line Telo does not own carries no capital,
    # fixed operations, or validation on Telo's ledger: it is charged as a reservation fee.
    assert si.capital_total == pytest.approx(one.capital_total)
    owned = screen_inputs(
        product, _s8(site_plans=plans, design_variables={"reserved_site_owned": 1.0}), glob
    )
    assert owned.capital_total > one.capital_total


def test_corrected_screen_row_runs_for_a_declared_topology(product, glob) -> None:  # type: ignore[no-untyped-def]
    row = screen_row(product, _s8(), glob, "corrected")
    assert row.strategy_id == "S8" and row.mode == "corrected"
    assert row.sites == 2.0 and row.saleable_capacity > 0
    assert row.delivered_units <= product.parameters.base("annual_demand_units")
    assert row.total_annual_cost > 0 and row.cost_per_unit > 0
    assert row.illustrative is True
