"""Economics: capital recovery, cost ledgers, break-even, resilience premium, ICER.

Concepts kept separate by construction (protocol 5.2, task section 16): production
cost, reimbursement, market price, willingness to pay, and provider shortage cost
are distinct arguments and are never summed inside this module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, fields


def crf(rate: float, life_years: float) -> float:
    """Capital recovery factor, protocol Eq. 3: r(1+r)^n / ((1+r)^n - 1).

    At r = 0 the limit is 1/n (straight line).
    """
    if life_years <= 0:
        raise ValueError("economic life must be positive")
    if rate < 0:
        raise ValueError("discount rate must be non-negative")
    if rate == 0:
        return 1.0 / life_years
    growth = float((1.0 + rate) ** life_years)
    return float(rate * growth / (growth - 1.0))


def annualize(capital: float, rate: float, life_years: float) -> float:
    if capital < 0:
        raise ValueError("capital must be non-negative")
    return capital * crf(rate, life_years)


def straight_line(capital: float, life_years: float) -> float:
    if life_years <= 0:
        raise ValueError("economic life must be positive")
    if capital < 0:
        raise ValueError("capital must be non-negative")
    return capital / life_years


@dataclass
class CostLedger:
    """Annual cost by protocol 6.1 ledger. USD per year. Each ledger is filled once."""

    capital_annualized: float = 0.0
    fixed_site_operations: float = 0.0
    product_site_launch: float = 0.0
    variable_production: float = 0.0
    opening_inventory: float = 0.0
    quality_testing: float = 0.0
    failure_waste: float = 0.0
    inventory_logistics: float = 0.0
    resilience_contracts: float = 0.0
    os_integration: float = 0.0
    notes: list[str] = field(default_factory=list)

    def total(self) -> float:
        return sum(float(getattr(self, f.name)) for f in fields(self) if f.name != "notes")

    def per_delivered_unit(self, delivered_units: float) -> float:
        """Protocol Eq. 4. Denominator is delivered non-expired units; zero delivery is undefined."""
        if delivered_units <= 0:
            return math.inf
        return self.total() / delivered_units

    def check_nonnegative(self) -> None:
        for f in fields(self):
            if f.name == "notes":
                continue
            v = float(getattr(self, f.name))
            if v < 0 or math.isnan(v):
                raise ValueError(f"ledger {f.name} is {v}")


def break_even_volume(
    annual_fixed_and_resilience_cost: float, contribution_margin_per_unit: float
) -> float:
    """Protocol Eq. 6: fixed/resilience cost divided by contribution margin per delivered unit.

    Contribution margin = price net of variable production, testing, distribution, and
    expected waste. Returns +inf when the margin is non-positive.
    """
    if annual_fixed_and_resilience_cost < 0:
        raise ValueError("fixed cost must be non-negative")
    if contribution_margin_per_unit <= 0:
        return math.inf
    return annual_fixed_and_resilience_cost / contribution_margin_per_unit


def resilience_premium(
    cost_strategy: float, cost_status_quo: float, committed_units: float
) -> float:
    """Protocol Eq. 7: incremental annual cost per committed unit. Who pays is stated elsewhere."""
    if committed_units <= 0:
        return math.inf
    return (cost_strategy - cost_status_quo) / committed_units


@dataclass(frozen=True)
class IcerResult:
    incremental_cost: float
    shortage_days_avoided: float
    value: float | None
    label: str

    @property
    def dominated(self) -> bool:
        return self.label == "dominated"


def icer(
    cost_strategy: float,
    cost_reference: float,
    shortage_days_strategy: float,
    shortage_days_reference: float,
) -> IcerResult:
    """Protocol Eq. 11 with dominance labeling.

    * dominated: costs more and avoids no shortage days (or is worse) -> no ICER.
    * dominant: costs less and is at least as effective -> reported as cost-saving.
    * otherwise a ratio in USD per shortage-day avoided.
    """
    dc = cost_strategy - cost_reference
    dsd = shortage_days_reference - shortage_days_strategy
    if dc >= 0 and dsd <= 0:
        if dc == 0 and dsd == 0:
            return IcerResult(dc, dsd, None, "equivalent")
        return IcerResult(dc, dsd, None, "dominated")
    if dc <= 0 and dsd >= 0:
        return IcerResult(dc, dsd, None, "dominant")
    if dsd > 0:
        return IcerResult(dc, dsd, dc / dsd, "trade_off")
    # more effective in cost but less effective in shortage days: negative ratio, report as trade-off with sign
    return IcerResult(dc, dsd, dc / dsd, "trade_off_worse_service")
