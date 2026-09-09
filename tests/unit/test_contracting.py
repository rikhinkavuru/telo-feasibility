"""Contract terms and the volume arithmetic a resilience architecture needs."""

from __future__ import annotations

import math

import pytest

from telo_feasibility.contracting import (
    ContractTerms,
    contract_requirement,
    maximum_fixed_cost_per_site,
    minimum_contracted_utilization,
)


def test_terms_report_what_is_unanswered() -> None:
    t = ContractTerms(strategy_id="S8", mechanism="take_or_pay")
    assert not t.complete
    assert set(t.missing()) == set(ContractTerms.REQUIRED)
    t.payer = "hospital consortium"
    t.purchaser = "group purchasing organization"
    t.beneficiary = "member hospitals"
    t.term_years = 5.0
    t.committed_units_per_year = 500_000.0
    t.activation_condition = "always on; volume commitment independent of shortage state"
    t.allocation_rights = "pro rata among members during allocation"
    t.default_risk = "member exit at 12 months notice"
    t.price_required_usd_per_unit = 14.0
    assert t.complete and t.missing() == []
    row = t.as_row()
    assert row["complete"] is True and row["missing"] == "" and "evidence" in row


def test_requirement_arithmetic_at_the_break_even_price() -> None:
    r = contract_requirement(
        strategy_id="S5",
        reference_strategy_id="S0",
        annual_cost_usd=60_000_000.0,
        reference_annual_cost_usd=12_000_000.0,
        delivered_units_per_year=1_000_000.0,
        fixed_and_resilience_cost_usd=40_000_000.0,
        variable_cost_usd_per_unit=1.2,
        capacity_units_per_year=2_000_000.0,
    )
    assert r.break_even_price_usd_per_unit == pytest.approx(60.0)
    assert r.incremental_cost_usd_per_year == pytest.approx(48_000_000.0)
    assert r.resilience_premium_usd_per_unit == pytest.approx(48.0)
    # at the break-even price the committed volume is the delivered volume, by construction
    assert r.committed_units_for_fixed_cost == pytest.approx(40_000_000.0 / (60.0 - 1.2))
    assert r.implied_utilization == pytest.approx(0.5)
    assert any("no price supplied" in n for n in r.notes)


def test_requirement_at_a_supplied_price_can_be_impossible() -> None:
    r = contract_requirement(
        strategy_id="S5",
        reference_strategy_id="S0",
        annual_cost_usd=60_000_000.0,
        reference_annual_cost_usd=12_000_000.0,
        delivered_units_per_year=1_000_000.0,
        fixed_and_resilience_cost_usd=40_000_000.0,
        variable_cost_usd_per_unit=1.2,
        capacity_units_per_year=2_000_000.0,
        price_usd_per_unit=1.0,  # below variable cost: no volume covers fixed cost
    )
    assert math.isinf(r.committed_units_for_fixed_cost)
    assert math.isinf(r.take_or_pay_fraction_of_capacity)
    assert any("margin is not positive" in n for n in r.notes)
    assert r.notes and not any("no price supplied" in n for n in r.notes)


def test_take_or_pay_fraction_can_exceed_one() -> None:
    r = contract_requirement(
        strategy_id="S6",
        reference_strategy_id="S0",
        annual_cost_usd=60_000_000.0,
        reference_annual_cost_usd=12_000_000.0,
        delivered_units_per_year=1_000_000.0,
        fixed_and_resilience_cost_usd=40_000_000.0,
        variable_cost_usd_per_unit=1.2,
        capacity_units_per_year=2_000_000.0,
        price_usd_per_unit=15.0,
    )
    # 40M / (15 - 1.2) = 2.899M units needed against 2.0M of capacity
    assert r.take_or_pay_fraction_of_capacity > 1.0
    assert r.committed_units_for_fixed_cost > r.capacity_units_per_year


def test_utilization_and_fixed_cost_ceilings() -> None:
    assert minimum_contracted_utilization(
        fixed_and_resilience_cost_usd=1_000_000.0,
        contribution_margin_usd_per_unit=10.0,
        capacity_units_per_year=500_000.0,
    ) == pytest.approx(0.2)
    assert math.isinf(
        minimum_contracted_utilization(
            fixed_and_resilience_cost_usd=1_000_000.0,
            contribution_margin_usd_per_unit=0.0,
            capacity_units_per_year=500_000.0,
        )
    )
    assert math.isinf(
        minimum_contracted_utilization(
            fixed_and_resilience_cost_usd=1.0,
            contribution_margin_usd_per_unit=10.0,
            capacity_units_per_year=0.0,
        )
    )
    assert maximum_fixed_cost_per_site(
        contribution_margin_usd_per_unit=10.0, committed_units_per_year=250_000.0
    ) == pytest.approx(2_500_000.0)
    assert (
        maximum_fixed_cost_per_site(
            contribution_margin_usd_per_unit=-1.0, committed_units_per_year=250_000.0
        )
        == 0.0
    )


def test_zero_delivery_is_an_error_not_a_number() -> None:
    with pytest.raises(ValueError, match="delivered units"):
        contract_requirement(
            strategy_id="S0",
            reference_strategy_id="S0",
            annual_cost_usd=1.0,
            reference_annual_cost_usd=1.0,
            delivered_units_per_year=0.0,
            fixed_and_resilience_cost_usd=1.0,
            variable_cost_usd_per_unit=1.0,
            capacity_units_per_year=1.0,
        )
