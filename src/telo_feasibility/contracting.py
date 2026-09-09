"""Contract economics for a resilience architecture (assignment Phase B family 10, Phase E).

A technically feasible plant without contractable demand is not feasible, so every
architecture carries a contract description and the volume arithmetic that goes with it.
This module holds both:

* ``ContractTerms`` names the nine things a resilience contract has to answer (payer,
  purchaser, beneficiary, length, committed volume, activation condition, allocation
  rights, default risk, price required). Fields stay ``None`` until a person supplies
  them; ``missing()`` lists what is unanswered so a strategy is never presented as
  contractable by omission.
* the arithmetic that turns a simulated cost into the commercial conditions a strategy
  needs: the resilience premium per committed unit against a reference strategy, the
  break-even price, the committed volume that covers fixed and resilience cost, the share
  of capacity that must be committed (take-or-pay), and the utilization that implies.

Prices, reimbursement, and production cost stay separate arguments here exactly as in
``economics``: nothing in this module infers a price from a cost.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, fields
from typing import Any

from .economics import break_even_volume, resilience_premium


@dataclass
class ContractTerms:
    """The commercial description a strategy needs before it can be called feasible."""

    strategy_id: str
    mechanism: str  # take_or_pay | capacity_subscription | advance_purchase | availability_payment | stockpile | option | outcome_based | spot | none
    payer: str | None = None
    purchaser: str | None = None
    beneficiary: str | None = None
    term_years: float | None = None
    committed_units_per_year: float | None = None
    activation_condition: str | None = None
    allocation_rights: str | None = None
    default_risk: str | None = None
    price_required_usd_per_unit: float | None = None
    evidence: list[str] = field(default_factory=list)
    notes: str = ""

    REQUIRED: tuple[str, ...] = (
        "payer",
        "purchaser",
        "beneficiary",
        "term_years",
        "committed_units_per_year",
        "activation_condition",
        "allocation_rights",
        "default_risk",
        "price_required_usd_per_unit",
    )

    def missing(self) -> list[str]:
        return [
            f.name
            for f in fields(self)
            if f.name in self.REQUIRED and getattr(self, f.name) in (None, "")
        ]

    @property
    def complete(self) -> bool:
        return not self.missing()

    def as_row(self) -> dict[str, Any]:
        row = {f.name: getattr(self, f.name) for f in fields(self) if f.name not in ("evidence",)}
        row["evidence"] = "; ".join(self.evidence)
        row["missing"] = "; ".join(self.missing())
        row["complete"] = self.complete
        return row


@dataclass(frozen=True)
class ContractRequirement:
    """What a strategy needs commercially, derived from its simulated annual cost."""

    strategy_id: str
    reference_strategy_id: str
    annual_cost_usd: float
    reference_annual_cost_usd: float
    delivered_units_per_year: float
    incremental_cost_usd_per_year: float
    resilience_premium_usd_per_unit: float
    break_even_price_usd_per_unit: float
    committed_units_for_fixed_cost: float
    take_or_pay_fraction_of_capacity: float
    implied_utilization: float
    capacity_units_per_year: float
    notes: tuple[str, ...] = ()


def contract_requirement(
    *,
    strategy_id: str,
    reference_strategy_id: str,
    annual_cost_usd: float,
    reference_annual_cost_usd: float,
    delivered_units_per_year: float,
    fixed_and_resilience_cost_usd: float,
    variable_cost_usd_per_unit: float,
    capacity_units_per_year: float,
    price_usd_per_unit: float | None = None,
) -> ContractRequirement:
    """Commercial conditions implied by one simulated strategy.

    ``break_even_price`` is the price at which delivered volume covers the whole annual
    cost. ``committed_units_for_fixed_cost`` is protocol Eq. 6 at the given price: the
    volume whose contribution margin covers fixed and resilience cost. When no price is
    given, the break-even price is used, which makes the committed volume equal delivered
    volume by construction; that is reported as a note rather than hidden, because the
    interesting question is what happens at a price someone will actually pay.
    """
    notes: list[str] = []
    if delivered_units_per_year <= 0:
        raise ValueError("delivered units must be positive")
    break_even_price = annual_cost_usd / delivered_units_per_year
    price = price_usd_per_unit
    if price is None:
        price = break_even_price
        notes.append(
            "no price supplied: the break-even price is used, so committed volume equals "
            "delivered volume by construction (protocol 5.2 keeps price and cost separate; "
            "a real price needs HA-11 or HA-24 evidence)"
        )
    margin = price - variable_cost_usd_per_unit
    committed = break_even_volume(fixed_and_resilience_cost_usd, margin)
    if not math.isfinite(committed):
        notes.append(
            f"contribution margin is not positive at {price:,.2f} USD per unit: no volume "
            "covers the fixed and resilience cost"
        )
    top = committed / capacity_units_per_year if capacity_units_per_year > 0 else float("inf")
    util = (
        delivered_units_per_year / capacity_units_per_year
        if capacity_units_per_year > 0
        else float("nan")
    )
    return ContractRequirement(
        strategy_id=strategy_id,
        reference_strategy_id=reference_strategy_id,
        annual_cost_usd=annual_cost_usd,
        reference_annual_cost_usd=reference_annual_cost_usd,
        delivered_units_per_year=delivered_units_per_year,
        incremental_cost_usd_per_year=annual_cost_usd - reference_annual_cost_usd,
        resilience_premium_usd_per_unit=resilience_premium(
            annual_cost_usd, reference_annual_cost_usd, delivered_units_per_year
        ),
        break_even_price_usd_per_unit=break_even_price,
        committed_units_for_fixed_cost=committed,
        take_or_pay_fraction_of_capacity=top,
        implied_utilization=util,
        capacity_units_per_year=capacity_units_per_year,
        notes=tuple(notes),
    )


def minimum_contracted_utilization(
    *,
    fixed_and_resilience_cost_usd: float,
    contribution_margin_usd_per_unit: float,
    capacity_units_per_year: float,
) -> float:
    """Share of a site's saleable capacity that must be sold under contract to break even.

    Returns ``inf`` when the margin is not positive and a value above 1 when the site
    cannot cover its fixed cost even if every unit it can make is committed.
    """
    if capacity_units_per_year <= 0:
        return float("inf")
    volume = break_even_volume(fixed_and_resilience_cost_usd, contribution_margin_usd_per_unit)
    return volume / capacity_units_per_year


def maximum_fixed_cost_per_site(
    *,
    contribution_margin_usd_per_unit: float,
    committed_units_per_year: float,
) -> float:
    """Largest annual fixed and resilience cost a committed volume can carry."""
    if contribution_margin_usd_per_unit <= 0 or committed_units_per_year <= 0:
        return 0.0
    return contribution_margin_usd_per_unit * committed_units_per_year
