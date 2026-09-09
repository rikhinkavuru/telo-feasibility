"""Unit tests for the failure-decomposition module (design-space Phase A)."""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from telo_feasibility.ablation import (
    ATTRIBUTION_METRICS,
    FACTORS,
    MECHANISM_FACTORS,
    STATUS_QUO_UTILIZATION_TARGET,
    Config,
    apply_factors,
    attribution,
    default_configs,
    load_design_variables,
    pair_configs,
    status_quo_utilization,
)
from telo_feasibility.configs import ProductConfig, load_global, load_products, load_strategies
from telo_feasibility.disruptions import DAYS_PER_YEAR
from telo_feasibility.optimization import RESULTS_OPT
from telo_feasibility.schemas import FROZEN_STRATEGY_IDS, StrategyId
from telo_feasibility.sensitivity import set_base
from telo_feasibility.simulation import SimSettings

SODIUM = "sodium_bicarbonate_8_4_50ml"
NOREPI = "norepinephrine_1mgml_4ml"


@pytest.fixture(scope="module")
def glob():  # type: ignore[no-untyped-def]
    return load_global()


@pytest.fixture(scope="module")
def products():  # type: ignore[no-untyped-def]
    return load_products()


@pytest.fixture(scope="module")
def designs():  # type: ignore[no-untyped-def]
    return load_strategies().designs


@pytest.fixture
def settings() -> SimSettings:
    return SimSettings(
        horizon_days=365 + round(5 * DAYS_PER_YEAR),
        warm_up_days=365,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=False,
        shortage_listed_at_t0=False,
    )


def test_factor_registry_is_consistent(glob, products) -> None:  # type: ignore[no-untyped-def]
    ids = [f.id for f in FACTORS.values()]
    assert len(ids) == len(set(ids))
    assert all(k == f.id for k, f in FACTORS.items())
    product_keys = set(products[SODIUM].parameters.parameters)
    for f in FACTORS.values():
        assert f.kind in {"mechanism", "cost", "structure"}, f.id
        for k in f.global_overrides:
            assert k in glob.parameters, f"{f.id}: unknown global parameter {k}"
        for k in f.product_overrides:
            assert k in product_keys, f"{f.id}: unknown product parameter {k}"
        for target in f.design_overrides:
            assert target == "*" or target in {s.value for s in StrategyId}, f.id
        for k in f.settings_overrides:
            assert (
                k == "horizon_years" or hasattr(SimSettings, k) or k in SimSettings.__annotations__
            )
    assert set(MECHANISM_FACTORS) == {
        f.id for f in FACTORS.values() if f.kind == "mechanism" and not f.loo_only
    }
    assert FACTORS["material_buffer"].loo_only and "material_buffer" not in MECHANISM_FACTORS
    assert "capacity_shortfall" in MECHANISM_FACTORS
    assert FACTORS["fixed_quality_cost"].kind == "cost"
    assert FACTORS["horizon_10y"].kind == "structure"


def test_apply_no_factors_is_identity_and_does_not_mutate(
    glob, products, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    product = products[SODIUM]
    before_p = product.parameters.model_dump(mode="json")
    before_g = glob.model_dump(mode="json")
    before_d = [d.model_dump(mode="json") for d in designs]
    prod, g, st, ds = apply_factors((), product, glob, settings, designs)
    assert prod.parameters.model_dump(mode="json") == before_p
    assert g.model_dump(mode="json") == before_g
    assert st == settings
    assert [d.model_dump(mode="json") for d in ds] == before_d
    # returned designs are copies
    ds[0].design_variables["region_base_stock"] = 1.0
    assert "region_base_stock" not in designs[0].design_variables
    assert product.parameters.model_dump(mode="json") == before_p
    assert glob.model_dump(mode="json") == before_g


@pytest.mark.parametrize("fid", list(FACTORS))
def test_each_factor_changes_only_its_intended_fields(
    fid, glob, products, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    f = FACTORS[fid]
    product = products[SODIUM]
    prod, g, st, ds = apply_factors((fid,), product, glob, settings, designs)
    for k, prm in g.parameters.items():
        if k in f.global_overrides:
            assert prm.base == f.global_overrides[k], (fid, k)
        else:
            assert prm.model_dump(mode="json") == glob.parameters[k].model_dump(mode="json"), (
                fid,
                k,
            )
    special_keys = (
        {"batches_per_site_year_nominal"} if f.special == "status_quo_utilization" else set()
    )
    for k, prm in prod.parameters.parameters.items():
        if k in f.product_overrides:
            assert prm.base == f.product_overrides[k], (fid, k)
        elif k in special_keys:
            assert prm.base is not None and prm.base > product.parameters.base(k), (fid, k)
        else:
            assert prm.model_dump(mode="json") == product.parameters.parameters[k].model_dump(
                mode="json"
            ), (fid, k)
    for d, orig in zip(ds, designs, strict=True):
        expected = dict(orig.design_variables)
        for target, dv in f.design_overrides.items():
            if target == "*" or d.id.value == target:
                expected.update(dv)
        assert d.design_variables == expected, (fid, d.id.value)
    expected_settings = settings
    for k, v in f.settings_overrides.items():
        if k == "horizon_years":
            expected_settings = replace(
                expected_settings,
                horizon_days=settings.warm_up_days + round(float(v) * DAYS_PER_YEAR),
            )
        else:
            expected_settings = replace(expected_settings, **{k: v})
    assert st == expected_settings, fid


def test_horizon_and_listing_overrides(glob, products, designs, settings) -> None:  # type: ignore[no-untyped-def]
    _p, _g, st, _d = apply_factors(("horizon_10y",), products[SODIUM], glob, settings, designs)
    assert st.horizon_days == settings.warm_up_days + round(10 * DAYS_PER_YEAR)
    assert st.warm_up_days == settings.warm_up_days
    _p, _g, st2, _d = apply_factors(
        ("regulatory_unavailability",), products[NOREPI], glob, settings, designs
    )
    assert st2.shortage_listed_at_t0 is True
    assert _g.base("shortage_list_resolution_rate_per_year") == 0.0


def test_capacity_shortfall_targets_status_quo_utilization(
    glob, products, designs, settings
) -> None:  # type: ignore[no-untyped-def]
    s0 = next(d for d in designs if d.id is StrategyId.S0)
    for pid in (SODIUM, NOREPI):
        product = products[pid]
        before = status_quo_utilization(product, s0)
        prod, _g, _s, _d = apply_factors(("capacity_shortfall",), product, glob, settings, designs)
        after = status_quo_utilization(prod, s0)
        if before > STATUS_QUO_UTILIZATION_TARGET:
            assert after == pytest.approx(STATUS_QUO_UTILIZATION_TARGET, abs=1e-9), pid
            assert prod.parameters.base("batches_per_site_year_nominal") == pytest.approx(
                product.parameters.base("batches_per_site_year_nominal")
                * before
                / STATUS_QUO_UTILIZATION_TARGET
            )
        else:
            assert after == pytest.approx(before)
    # a product already below the target keeps its nominal capacity
    slack_params = set_base(products[NOREPI].parameters, "annual_demand_units", 300_000.0)
    slack = ProductConfig(products[NOREPI].presentation, slack_params, products[NOREPI].path)
    assert status_quo_utilization(slack, s0) < STATUS_QUO_UTILIZATION_TARGET
    prod, _g, _s, _d = apply_factors(("capacity_shortfall",), slack, glob, settings, designs)
    assert prod.parameters.base("batches_per_site_year_nominal") == slack.parameters.base(
        "batches_per_site_year_nominal"
    )


def test_extra_design_overrides_apply_after_factors(glob, products, designs, settings) -> None:  # type: ignore[no-untyped-def]
    _p, _g, _s, ds = apply_factors(
        ("inventory_timing",),
        products[SODIUM],
        glob,
        settings,
        designs,
        extra_design_overrides={"*": {"safety_stock_days": 365.0}, "S3": {"campaign_batches": 2.0}},
    )
    for d in ds:
        assert d.design_variables["region_base_stock"] == 1.0
        assert d.design_variables["safety_stock_days"] == 365.0
    assert next(d for d in ds if d.id is StrategyId.S3).design_variables["campaign_batches"] == 2.0
    assert "campaign_batches" not in next(d for d in ds if d.id is StrategyId.S0).design_variables


def test_unknown_factor_raises(glob, products, designs, settings) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(KeyError):
        apply_factors(("no_such_factor",), products[SODIUM], glob, settings, designs)


def test_default_configs_cover_every_factor() -> None:
    cfgs = default_configs()
    ids = [c.id for c in cfgs]
    assert len(ids) == len(set(ids))
    by_id = {c.id: c for c in cfgs}
    assert by_id["base"].factors == () and by_id["base"].role == "base"
    assert set(by_id["quiet_all"].factors) == set(MECHANISM_FACTORS)
    for fid in FACTORS:
        assert by_id[f"loo:{fid}"].factors == (fid,)
        assert by_id[f"loo:{fid}"].role == "loo"
    for fid in MECHANISM_FACTORS:
        cfg = by_id[f"addin:{fid}"]
        assert set(cfg.factors) == set(MECHANISM_FACTORS) - {fid}
        assert cfg.role == "addin"
    for fid in FACTORS:
        if FACTORS[fid].kind != "mechanism":
            assert f"addin:{fid}" not in by_id
    assert by_id["bounds:ss365"].design_overrides == {"*": {"safety_stock_days": 365.0}}
    assert by_id["bounds:ss365+base_stock"].factors == ("inventory_timing",)
    assert len(cfgs) == 1 + len(FACTORS) + 1 + len(MECHANISM_FACTORS) + 2


def test_pair_configs_enumerates_subsets_of_size_two_or_more() -> None:
    cfgs = pair_configs(["a", "b", "c"])
    assert {c.factors for c in cfgs} == {("a", "b"), ("a", "c"), ("b", "c"), ("a", "b", "c")}
    assert all(c.role == "pair" and c.id.startswith("pair:") for c in cfgs)
    assert isinstance(cfgs[0], Config)


def _entry(fill: float, p_meet: float, sd: float, unmet: float, cost: float) -> dict[str, object]:
    return {
        "fill_rate": {"mean": fill, "mcse": 0.0, "n": 3},
        "p_meet": p_meet,
        "shortage_days_per_year": {"mean": sd, "mcse": 0.0, "n": 3},
        "unmet_units_per_year": {"mean": unmet, "mcse": 0.0, "n": 3},
        "annual_total_cost": {"mean": cost, "mcse": 0.0, "n": 3},
    }


def test_attribution_deltas_and_shares() -> None:
    fid = "site_failures"
    summary = {
        "base|P|S": _entry(0.90, 0.2, 50.0, 1000.0, 10.0),
        "quiet_all|P|S": _entry(1.00, 1.0, 0.0, 0.0, 8.0),
        f"loo:{fid}|P|S": _entry(0.95, 0.6, 20.0, 400.0, 9.5),
        f"addin:{fid}|P|S": _entry(0.98, 0.9, 5.0, 100.0, 8.4),
    }
    rows = attribution(summary)
    assert len(rows) == len(FACTORS)
    row = next(r for r in rows if r["factor"] == fid)
    assert row["product_id"] == "P" and row["strategy_id"] == "S"
    assert row["family"] == FACTORS[fid].family and row["kind"] == "mechanism"
    assert row["base_fill_rate"] == pytest.approx(0.90)
    assert row["loo_fill_rate"] == pytest.approx(0.95)
    assert row["loo_delta_fill_rate"] == pytest.approx(0.05)
    assert row["addin_delta_fill_rate"] == pytest.approx(0.02)
    assert row["loo_share_fill_rate"] == pytest.approx(0.5)
    assert row["addin_share_fill_rate"] == pytest.approx(0.2)
    assert row["loo_delta_p_meet"] == pytest.approx(0.4)
    assert row["addin_delta_p_meet"] == pytest.approx(0.1)
    assert row["loo_delta_shortage_days_per_year"] == pytest.approx(-30.0)
    assert row["loo_share_shortage_days_per_year"] == pytest.approx(0.6)
    assert row["addin_delta_annual_total_cost"] == pytest.approx(-0.4)
    assert row["shapley_bracket_fill_low"] == pytest.approx(0.02)
    assert row["shapley_bracket_fill_high"] == pytest.approx(0.05)
    other = next(r for r in rows if r["factor"] == "surge_headroom")
    for m in ATTRIBUTION_METRICS:
        assert math.isnan(other[f"loo_delta_{m}"]) and math.isnan(other[f"addin_delta_{m}"])
        assert math.isnan(other[f"loo_share_{m}"])
    assert math.isnan(other["shapley_bracket_fill_low"])


def test_attribution_is_nan_safe_without_quiet_world() -> None:
    rows = attribution({"base|P|S": _entry(0.9, 0.2, 50.0, 1000.0, 10.0)})
    assert len(rows) == len(FACTORS)
    for r in rows:
        assert r["base_fill_rate"] == pytest.approx(0.9)
        for m in ATTRIBUTION_METRICS:
            assert math.isnan(r[f"loo_share_{m}"]) and math.isnan(r[f"addin_share_{m}"])
    assert attribution({}) == []


def test_load_design_variables_picks_best_else_closest_grid() -> None:
    run_dir = RESULTS_OPT / "opt_20260902T043854Z"
    if not run_dir.exists():
        pytest.skip("frozen-target optimization run not present")
    dvs = load_design_variables(run_dir)
    assert set(dvs) == {SODIUM, NOREPI}
    for pid in dvs:
        assert set(dvs[pid]) == {s.value for s in FROZEN_STRATEGY_IDS}
    # sodium S5 was infeasible: closest grid point carried node_scale ~0.7167
    assert dvs[SODIUM]["S5"]["node_scale"] == pytest.approx(0.7166666666666667)
    assert dvs[SODIUM]["S5"]["sites"] == 4.0
    # sodium S2 had a full-N incumbent ('best'), not the grid point
    assert dvs[SODIUM]["S2"]["capacity_factor"] == pytest.approx(0.95)
    assert dvs[SODIUM]["S2"]["safety_stock_days"] == 120.0
    assert load_design_variables(None) == {}
