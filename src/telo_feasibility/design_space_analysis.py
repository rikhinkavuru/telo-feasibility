"""Feasibility regions, dominance, and reversal maps for the design-space strategies (Phase E).

Three questions, each answered by re-simulating on common random numbers:

* ``threshold``: along one named input, where does a strategy stop meeting the service
  target? A monotone bisection between the input's low and high records returns the exact
  crossing plus the two bracketing evaluations, so a condition can be stated as "feasible
  while X <= x*" rather than as a score.
* ``dominance``: at a matched service target, which strategies are dominated (cost at
  least as high and service no better) and which sit on the cost-service frontier.
* ``reversal``: over a grid of two or three inputs, which strategy is preferred, so the
  region where a recommendation flips is visible.

Every routine takes the strategies it is given (frozen comparators, design-space
strategies, or both) and never assumes a strategy is eligible: a strategy whose gates are
not PASS is evaluated for information and labeled, exactly as the optimizer does.
"""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from .configs import ProductConfig
from .provenance import PACKAGE_ROOT
from .schemas import Eligibility, ParameterSet, StrategyDesign
from .sensitivity import MANDATORY_INPUTS, apply_inputs, input_range
from .simulation import SimSettings, run_paired

RESULTS_DS = PACKAGE_ROOT / "results" / "design_space"
BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"

# Inputs the design-space questions need beyond the protocol's mandatory set. Each maps to
# a parameter that already carries provenance; the value swept is that parameter's base.
EXTRA_INPUTS: dict[str, tuple[str, str]] = {
    "commissioning_days": ("global", "node_commissioning_days"),
    "activation_latency_days": ("global", "reserved_capacity_activation_days"),
    "reservation_fee_fraction": ("global", "reserved_capacity_fee_fraction"),
    "os_integration_cost": ("global", "os_integration_usd_per_site_year"),
    "node_capital": ("product", "capital_usd_per_site"),
    "validation_cost": ("product", "validation_usd_one_time"),
    "testing_cost_per_batch": ("product", "testing_usd_per_batch"),
    "batches_per_site_year": ("product", "batches_per_site_year_nominal"),
    "common_cause_impact": ("global", "common_cause_capacity_impact"),
    "supplier_disruption_duration": ("global", "supplier_disruption_duration_days"),
    "site_failure_duration": ("global", "site_failure_duration_days"),
}
ALL_INPUTS: dict[str, tuple[str, str]] = {**MANDATORY_INPUTS, **EXTRA_INPUTS}


def _range(product: ProductConfig, glob: ParameterSet, name: str) -> tuple[float, float, float]:
    if name in MANDATORY_INPUTS:
        return input_range(product, glob, name)
    which, pid = EXTRA_INPUTS[name]
    prm = (glob if which == "global" else product.parameters).parameters[pid]
    base = prm.base if prm.base is not None else 0.0
    lo = prm.low if prm.low is not None else base
    hi = prm.high if prm.high is not None else base
    return lo, base, hi


def _apply(
    product: ProductConfig, glob: ParameterSet, values: dict[str, float]
) -> tuple[ProductConfig, ParameterSet]:
    mandatory = {k: v for k, v in values.items() if k in MANDATORY_INPUTS}
    extra = {k: v for k, v in values.items() if k in EXTRA_INPUTS}
    prod, g = apply_inputs(product, glob, mandatory) if mandatory else (product, glob)
    if extra:
        from .sensitivity import set_base

        pp = prod.parameters
        for name, v in extra.items():
            which, pid = EXTRA_INPUTS[name]
            if which == "global":
                g = set_base(g, pid, v)
            else:
                pp = set_base(pp, pid, v)
        prod = ProductConfig(prod.presentation, pp, prod.path)
    return prod, g


@dataclass(frozen=True)
class Point:
    """One strategy evaluated at one point of the input space."""

    strategy_id: str
    inputs: dict[str, float]
    mean_fill: float
    p_meet: float
    mean_cost: float
    mcse_cost: float
    mean_shortage_days: float
    mean_cost_per_unit: float
    capacity_utilization: float
    feasible: bool
    n_runs: int
    eligibility: str


def evaluate(
    designs: Sequence[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    seed: int,
    runs: Sequence[int],
    tau: float,
    q: float,
    inputs: dict[str, float] | None = None,
    eligibility: dict[str, Eligibility] | None = None,
) -> list[Point]:
    prod, g = _apply(product, glob, inputs or {})
    res = run_paired(list(designs), prod, g, settings, seed, list(runs))
    out: list[Point] = []
    for d in designs:
        rs = [r for r in res if r.strategy_id == d.id.value]
        fill = np.array([r.metrics["fill_rate"] for r in rs])
        cost = np.array([r.metrics["annual_total_cost"] for r in rs])
        cpu = np.array([r.metrics["cost_per_delivered_unit"] for r in rs])
        sd = np.array([r.metrics["shortage_days_per_year"] for r in rs])
        served = np.array([r.metrics["served_units"] for r in rs])
        p_meet = float((fill >= tau).mean())
        elig = (eligibility or {}).get(d.id.value, Eligibility.NO_CONCLUSION)
        out.append(
            Point(
                strategy_id=d.id.value,
                inputs=dict(inputs or {}),
                mean_fill=float(fill.mean()),
                p_meet=p_meet,
                mean_cost=float(cost.mean()),
                mcse_cost=float(cost.std(ddof=1) / math.sqrt(cost.size))
                if cost.size > 1
                else float("nan"),
                mean_shortage_days=float(sd.mean()),
                mean_cost_per_unit=float(cpu[np.isfinite(cpu)].mean())
                if np.isfinite(cpu).any()
                else float("inf"),
                capacity_utilization=float(served.mean()),
                feasible=bool(fill.mean() >= tau and p_meet >= q),
                n_runs=len(rs),
                eligibility=elig.value,
            )
        )
    return out


@dataclass
class Threshold:
    """Where one strategy crosses the feasibility boundary along one input."""

    strategy_id: str
    product_id: str
    input_name: str
    parameter_id: str
    low: float
    base: float
    high: float
    feasible_at_low: bool
    feasible_at_high: bool
    threshold: float | None
    direction: str  # feasible_below | feasible_above | feasible_everywhere | infeasible_everywhere | non_monotone
    bracket: tuple[float, float] | None
    evaluations: list[dict[str, Any]] = field(default_factory=list)
    note: str = ""


def threshold(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    input_name: str,
    seed: int,
    runs: Sequence[int],
    tau: float,
    q: float,
    steps: int = 5,
    eligibility: dict[str, Eligibility] | None = None,
) -> Threshold:
    """Bisect between the input's low and high records for the feasibility crossing.

    Bisection assumes the feasibility indicator is monotone in the input. The two endpoint
    evaluations are always reported, so a non-monotone response is visible rather than
    hidden: when both endpoints agree the result is ``feasible_everywhere`` or
    ``infeasible_everywhere`` over the recorded range, and no threshold is claimed.
    """
    lo, base, hi = _range(product, glob, input_name)
    which, pid = ALL_INPUTS[input_name]
    ev: list[dict[str, Any]] = []

    def feasible_at(x: float) -> bool:
        p = evaluate(
            [design],
            product,
            glob,
            settings,
            seed=seed,
            runs=runs,
            tau=tau,
            q=q,
            inputs={input_name: x},
            eligibility=eligibility,
        )[0]
        ev.append({"value": x, **{k: v for k, v in asdict(p).items() if k != "inputs"}})
        return p.feasible

    f_lo, f_hi = feasible_at(lo), feasible_at(hi)
    t = Threshold(
        strategy_id=design.id.value,
        product_id=product.id,
        input_name=input_name,
        parameter_id=f"{which}.{pid}",
        low=lo,
        base=base,
        high=hi,
        feasible_at_low=f_lo,
        feasible_at_high=f_hi,
        threshold=None,
        direction="feasible_everywhere" if f_lo and f_hi else "infeasible_everywhere",
        bracket=None,
        evaluations=ev,
    )
    if f_lo == f_hi:
        t.note = (
            f"feasibility does not change between {lo} and {hi}; no threshold inside the "
            "recorded range"
        )
        return t
    a, b = (lo, hi) if f_lo else (hi, lo)  # a is feasible, b is not
    for _ in range(steps):
        mid = 0.5 * (a + b)
        if feasible_at(mid):
            a = mid
        else:
            b = mid
    t.threshold = 0.5 * (a + b)
    t.bracket = (min(a, b), max(a, b))
    t.direction = "feasible_below" if f_lo else "feasible_above"
    t.note = f"bisection over {steps} steps on {len(runs)} paired runs"
    return t


@dataclass(frozen=True)
class DominanceRow:
    strategy_id: str
    mean_cost: float
    mean_fill: float
    p_meet: float
    feasible: bool
    dominated_by: list[str]
    on_frontier: bool
    eligibility: str


def dominance(points: Sequence[Point], cost_tolerance: float = 0.0) -> list[DominanceRow]:
    """A strategy is dominated when another costs no more and serves at least as well.

    Comparison uses mean annual cost and mean fill rate together with the tail probability;
    ``cost_tolerance`` (absolute USD) lets Monte Carlo noise be discounted explicitly.
    """
    rows: list[DominanceRow] = []
    for p in points:
        dom = [
            o.strategy_id
            for o in points
            if o.strategy_id != p.strategy_id
            and o.mean_cost <= p.mean_cost + cost_tolerance
            and o.mean_fill >= p.mean_fill
            and o.p_meet >= p.p_meet
            and (o.mean_cost < p.mean_cost - cost_tolerance or o.mean_fill > p.mean_fill)
        ]
        rows.append(
            DominanceRow(
                strategy_id=p.strategy_id,
                mean_cost=p.mean_cost,
                mean_fill=p.mean_fill,
                p_meet=p.p_meet,
                feasible=p.feasible,
                dominated_by=sorted(dom),
                on_frontier=not dom,
                eligibility=p.eligibility,
            )
        )
    return rows


def reversal_map(
    designs: Sequence[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    axes: dict[str, list[float]],
    seed: int,
    runs: Sequence[int],
    tau: float,
    q: float,
    eligibility: dict[str, Eligibility] | None = None,
) -> dict[str, Any]:
    """Preferred (cheapest feasible) strategy over a grid of two or three inputs."""
    names = list(axes)
    cells: list[dict[str, Any]] = []
    grid = np.array(np.meshgrid(*[axes[n] for n in names], indexing="ij")).reshape(len(names), -1).T
    for combo in grid:
        inputs = {n: float(v) for n, v in zip(names, combo, strict=True)}
        pts = evaluate(
            designs,
            product,
            glob,
            settings,
            seed=seed,
            runs=runs,
            tau=tau,
            q=q,
            inputs=inputs,
            eligibility=eligibility,
        )
        feas = [p for p in pts if p.feasible]
        cells.append(
            {
                "inputs": inputs,
                "preferred": min(feas, key=lambda p: p.mean_cost).strategy_id if feas else None,
                "feasible": [p.strategy_id for p in feas],
                "cost": {p.strategy_id: p.mean_cost for p in pts},
                "fill": {p.strategy_id: p.mean_fill for p in pts},
                "p_meet": {p.strategy_id: p.p_meet for p in pts},
            }
        )
    return {"axes": axes, "cells": cells, "banner": BANNER}


def write_json(obj: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")
    return path


def run_id(prefix: str = "ds") -> str:
    return f"{prefix}_{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
