from __future__ import annotations

import math

import pytest

from telo_feasibility.configs import load_global, load_products, load_strategies
from telo_feasibility.deterministic import dashboard_rows, run_screen, screen_row
from telo_feasibility.economics import crf
from telo_feasibility.schemas import StrategyId


@pytest.fixture(scope="module")
def inputs() -> tuple[dict, object, object]:  # type: ignore[type-arg]
    return load_products(), load_strategies(), load_global()


def test_replica_row_5_matches_workbook_cached_values(inputs: tuple[dict, object, object]) -> None:  # type: ignore[type-arg]
    products, strategies, glob = inputs
    row = screen_row(
        products["sodium_bicarbonate_8_4_50ml"],
        strategies.by_id(StrategyId.S0),
        glob,
        "workbook_replica",
    )  # type: ignore[attr-defined]
    # 09_Deterministic row 5 cached values (docs/audits/02_workbook_audit.md)
    assert row.saleable_capacity == pytest.approx(963900.0)
    assert row.utilization == pytest.approx(1.2449424214130096)
    assert row.annualized_capex == pytest.approx(6510000.0)
    assert row.validation_annualized == pytest.approx(400000.0)
    assert row.variable_production == pytest.approx(1469387.755102041)
    assert row.testing == pytest.approx(1440000.0)
    assert row.inventory_carrying_expiry == pytest.approx(53542.07436399218)
    assert row.total_annual_cost == pytest.approx(13112929.829466032)
    assert row.cost_per_unit == pytest.approx(10.927441524555027)
    assert row.response_days == pytest.approx(115.0)
    assert row.expected_shortage_days_screen == pytest.approx(17.45025)
    assert row.illustrative


def test_corrected_variant_caps_delivery_and_uses_delivered_denominator(
    inputs: tuple[dict, object, object],
) -> None:  # type: ignore[type-arg]
    products, strategies, glob = inputs
    rep = screen_row(
        products["sodium_bicarbonate_8_4_50ml"],
        strategies.by_id(StrategyId.S0),
        glob,
        "workbook_replica",
    )  # type: ignore[attr-defined]
    cor = screen_row(
        products["sodium_bicarbonate_8_4_50ml"], strategies.by_id(StrategyId.S0), glob, "corrected"
    )  # type: ignore[attr-defined]
    assert cor.delivered_units < rep.annual_demand
    assert cor.delivered_units == pytest.approx(rep.saleable_capacity * (1 - 0.02))
    assert cor.chronic_shortfall_days == pytest.approx(
        365 * (1 - cor.delivered_units / rep.annual_demand)
    )
    assert cor.crf_used == pytest.approx(crf(0.10, 10))
    assert cor.validation_annualized == pytest.approx(4_000_000 * crf(0.10, 10))
    # no second expiry charge in the corrected inventory line
    assert cor.inventory_carrying_expiry == pytest.approx(cor.variable_production * 30 / 365 * 0.20)
    assert cor.cost_per_unit == pytest.approx(cor.total_annual_cost / cor.delivered_units)


def test_corrected_equals_replica_when_capacity_suffices_except_documented_terms(
    inputs: tuple[dict, object, object],
) -> None:  # type: ignore[type-arg]
    products, strategies, glob = inputs
    rep = screen_row(
        products["norepinephrine_1mgml_4ml"],
        strategies.by_id(StrategyId.S0),
        glob,
        "workbook_replica",
    )  # type: ignore[attr-defined]
    cor = screen_row(
        products["norepinephrine_1mgml_4ml"], strategies.by_id(StrategyId.S0), glob, "corrected"
    )  # type: ignore[attr-defined]
    assert rep.utilization < 1.0
    assert cor.delivered_units == pytest.approx(rep.annual_demand)
    assert cor.variable_production == pytest.approx(rep.variable_production)
    assert cor.distribution == pytest.approx(rep.distribution)
    assert cor.fixed_qa_labor == pytest.approx(rep.fixed_qa_labor)
    assert cor.response_days == pytest.approx(rep.response_days)
    assert cor.chronic_shortfall_days == 0.0


def test_screen_never_ranks_safety_stock_or_release_time(
    inputs: tuple[dict, object, object],
) -> None:  # type: ignore[type-arg]
    products, strategies, glob = inputs
    rows = run_screen(products, strategies, glob, "workbook_replica")  # type: ignore[arg-type]
    by = {(r.product_id, r.strategy_id): r for r in rows}
    a0 = by[("sodium_bicarbonate_8_4_50ml", "S0")]
    a1 = by[("sodium_bicarbonate_8_4_50ml", "S1")]
    a5 = by[("sodium_bicarbonate_8_4_50ml", "S5")]
    a6 = by[("sodium_bicarbonate_8_4_50ml", "S6")]
    assert a1.expected_shortage_days_screen == a0.expected_shortage_days_screen  # WB-02
    assert a6.expected_shortage_days_screen == a5.expected_shortage_days_screen  # WB-03
    assert a6.response_days < a5.response_days


def test_dashboard_replica_uses_typed_flags_and_gate_mode_reports_unresolved(
    inputs: tuple[dict, object, object],
) -> None:  # type: ignore[type-arg]
    from telo_feasibility.configs import load_gates
    from telo_feasibility.regulatory import evaluate_all

    products, strategies, glob = inputs
    rows = run_screen(products, strategies, glob, "workbook_replica")  # type: ignore[arg-type]
    dash = dashboard_rows(rows, glob, 0.99, None)
    by = {(d.product_id, d.strategy_id): d for d in dash}
    assert by[("sodium_bicarbonate_8_4_50ml", "S0")].interpretation == "Below service target"
    assert by[("sodium_bicarbonate_8_4_50ml", "S2")].interpretation == "Resilience premium required"
    assert (
        by[("sodium_bicarbonate_8_4_50ml", "S5")].interpretation
        == "Regulatory eligibility unresolved"
    )
    assert by[("sodium_bicarbonate_8_4_50ml", "S0")].cost_per_shortage_day_avoided is None
    elig = {k: v.eligibility for k, v in evaluate_all(load_gates()).items()}
    gated = dashboard_rows(rows, glob, 0.99, elig)
    assert {d.interpretation for d in gated} == {"Regulatory eligibility unresolved"}


def test_zero_demand_is_handled_without_division_error(inputs: tuple[dict, object, object]) -> None:  # type: ignore[type-arg]
    products, strategies, glob = inputs
    p = products["sodium_bicarbonate_8_4_50ml"]
    zero = p.parameters.model_copy(deep=True)
    zero.parameters["annual_demand_units"].low = 0.0
    zero.parameters["annual_demand_units"].base = 0.0
    from telo_feasibility.configs import ProductConfig

    pz = ProductConfig(presentation=p.presentation, parameters=zero, path=p.path)
    cor = screen_row(pz, strategies.by_id(StrategyId.S0), glob, "corrected")  # type: ignore[attr-defined]
    assert cor.variable_production == 0.0 and cor.delivered_units == 0.0
    assert math.isinf(cor.cost_per_unit)
    assert cor.fixed_qa_labor > 0
