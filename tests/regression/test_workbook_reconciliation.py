"""Regression: the replica reproduces every cached workbook value; configs match workbook inputs."""

from __future__ import annotations

import pytest

from telo_feasibility.configs import load_global, load_products, load_strategies
from telo_feasibility.deterministic import (
    dashboard_rows,
    reconcile_dashboard,
    reconcile_screen,
    run_screen,
)
from telo_feasibility.provenance import load_protocol, sha256_file
from telo_feasibility.workbook import (
    WORKBOOK_ELIGIBILITY_FLAG,
    WORKBOOK_PATH,
    WORKBOOK_SHA256,
    cached_dashboard_rows,
    cached_screen_rows,
    workbook_inputs,
)

pytestmark = pytest.mark.skipif(
    not WORKBOOK_PATH.is_file(), reason="frozen workbook snapshot missing"
)


def test_workbook_snapshot_hash_is_frozen() -> None:
    assert sha256_file(WORKBOOK_PATH) == WORKBOOK_SHA256


def test_config_inputs_match_workbook_inputs() -> None:
    wb = workbook_inputs()
    g = load_global()
    for name, v in wb.global_base.items():
        assert g.base(name) == pytest.approx(v), name
        assert g.parameters[name].low == pytest.approx(wb.global_low[name]), name
        assert g.parameters[name].high == pytest.approx(wb.global_high[name]), name
    for pid, cfg in load_products().items():
        for name, v in wb.product_base[pid].items():
            assert cfg.parameters.base(name) == pytest.approx(v), f"{pid}.{name}"
            assert cfg.parameters.parameters[name].low == pytest.approx(
                wb.product_low[pid][name]
            ), f"{pid}.{name}"
            assert cfg.parameters.parameters[name].high == pytest.approx(
                wb.product_high[pid][name]
            ), f"{pid}.{name}"
    s = load_strategies()
    for sid, dv in wb.strategies.items():
        for k, v in dv.items():
            assert s.by_id(sid).design_variables[k] == pytest.approx(v), f"{sid.value}.{k}"
    assert wb.eligibility_flags == {k: v for k, v in WORKBOOK_ELIGIBILITY_FLAG.items()}
    assert wb.target_fill_rate == pytest.approx(
        load_protocol().service_thresholds.fill_rate_mean_min
    )


def test_replica_reconciles_every_cached_cell() -> None:
    protocol = load_protocol()
    rows = run_screen(load_products(), load_strategies(), load_global(), "workbook_replica")
    r1 = reconcile_screen(cached_screen_rows(), rows)
    assert r1.n == 16 * 20
    assert r1.ok, [
        f"{c.sheet}!{c.column}{c.row}: {c.workbook_value} vs {c.python_value}"
        for c in r1.mismatches
    ]
    dash = dashboard_rows(rows, load_global(), protocol.service_thresholds.fill_rate_mean_min, None)
    r2 = reconcile_dashboard(cached_dashboard_rows(), dash)
    assert r2.n == 16 * 8
    assert r2.ok, [
        f"{c.sheet}!{c.column}{c.row}: {c.workbook_value} vs {c.python_value}"
        for c in r2.mismatches
    ]


def test_corrected_variant_differs_only_in_documented_columns() -> None:
    products, strategies, glob = load_products(), load_strategies(), load_global()
    rep = {
        (r.product_id, r.strategy_id): r
        for r in run_screen(products, strategies, glob, "workbook_replica")
    }
    cor = {
        (r.product_id, r.strategy_id): r
        for r in run_screen(products, strategies, glob, "corrected")
    }
    unchanged = [
        "sites",
        "annual_demand",
        "units_per_batch",
        "batches_per_site_year",
        "yield_fraction",
        "uptime",
        "saleable_capacity",
        "utilization",
        "fixed_qa_labor",
        "reserved_capacity_cost",
        "response_days",
        "expected_shortage_days_screen",
    ]
    for key, r in rep.items():
        c = cor[key]
        for col in unchanged:
            assert getattr(r, col) == pytest.approx(getattr(c, col)), f"{key} {col}"
        # capex changes only by CRF(typed) vs CRF(computed): relative difference below 1e-4
        assert abs(r.annualized_capex - c.annualized_capex) / r.annualized_capex < 1e-4
        assert c.validation_annualized > r.validation_annualized  # CRF > 1/life at r > 0
