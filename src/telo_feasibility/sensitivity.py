"""Sensitivity, structural uncertainty, decision reversal, and value of information (protocol 11).

All analyses re-simulate the paired strategy set on common random numbers. Inputs are
varied through their low/base/high records in the parameter sets, never by ad-hoc
numbers. Outputs are written as JSON so figures and tables are built from one source.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample
from scipy import stats

from .configs import ProductConfig
from .schemas import ParameterSet, StrategyDesign
from .simulation import SimSettings, run_paired

MANDATORY_INPUTS: dict[str, tuple[str, str]] = {
    # protocol 11.2 input -> (parameter set, parameter id)
    "capacity_utilization": (
        "product",
        "annual_demand_units",
    ),  # utilization moves through demand at fixed capacity
    "release_time": ("global", "sterility_incubation_days"),
    "fixed_qa_labor_per_node": ("product", "fixed_qa_labor_usd_per_site_year"),
    "yield": ("product", "yield_fraction"),
    "uptime": ("product", "uptime_fraction"),
    "demand_cv": ("global", "demand_cv"),
    "regional_demand_covariance": ("global", "demand_shock_all_regions_probability"),
    "raw_material_lead_time": ("product", "material_lead_time_days"),
    "supplier_concentration": ("global", "supplier_disruptions_per_supplier_year"),
    "common_cause_dependence": ("global", "common_cause_events_per_year"),
    "shelf_life": ("product", "shelf_life_months"),
    "expiry": ("product", "expiry_scrap_fraction"),
    "batch_size": ("product", "units_per_batch"),
    "changeover_burden": ("product", "changeover_days"),
    "deviation_rejection_rate": ("global", "deviation_rate_per_batch"),
    "capital_per_site": ("product", "capital_usd_per_site"),
    "node_scale": ("global", "node_scale_fraction"),
    "site_failure_rate": ("global", "site_failures_per_site_year"),
    "investigation_duration": ("global", "investigation_duration_days"),
}


def set_base(ps: ParameterSet, pid: str, value: float) -> ParameterSet:
    out = ps.model_copy(deep=True)
    prm = out.parameters[pid]
    lo = prm.low if prm.low is not None else value
    hi = prm.high if prm.high is not None else value
    prm.low = min(lo, value)
    prm.high = max(hi, value)
    prm.base = value
    return out


def apply_inputs(
    product: ProductConfig, glob: ParameterSet, values: dict[str, float]
) -> tuple[ProductConfig, ParameterSet]:
    g = glob
    pp = product.parameters
    for name, v in values.items():
        which, pid = MANDATORY_INPUTS[name]
        if which == "global":
            g = set_base(g, pid, v)
        else:
            pp = set_base(pp, pid, v)
    return ProductConfig(product.presentation, pp, product.path), g


def input_range(
    product: ProductConfig, glob: ParameterSet, name: str
) -> tuple[float, float, float]:
    which, pid = MANDATORY_INPUTS[name]
    prm = (glob if which == "global" else product.parameters).parameters[pid]
    base = prm.base if prm.base is not None else 0.0
    lo = prm.low if prm.low is not None else base
    hi = prm.high if prm.high is not None else base
    return lo, base, hi


@dataclass
class StrategyOutcome:
    strategy_id: str
    mean_cost: float
    mean_fill: float
    p_meet: float
    feasible: bool


@dataclass
class ScenarioOutcome:
    inputs: dict[str, float]
    outcomes: list[StrategyOutcome]
    preferred: str | None  # min-cost feasible strategy, or None if nothing feasible

    @property
    def cost_by_strategy(self) -> dict[str, float]:
        return {o.strategy_id: o.mean_cost for o in self.outcomes}


def evaluate_scenario(
    designs: list[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    seed: int,
    runs: list[int],
    tau: float,
    q: float,
    inputs: dict[str, float],
    eligible: set[str] | None = None,
) -> ScenarioOutcome:
    prod, g = apply_inputs(product, glob, inputs)
    res = run_paired(designs, prod, g, settings, seed, runs)
    outs: list[StrategyOutcome] = []
    for d in designs:
        rs = [r for r in res if r.strategy_id == d.id.value]
        fill = np.array([r.metrics["fill_rate"] for r in rs])
        cost = np.array([r.metrics["annual_total_cost"] for r in rs])
        p_meet = float((fill >= tau).mean())
        feasible = bool(fill.mean() >= tau and p_meet >= q) and (
            eligible is None or d.id.value in eligible
        )
        outs.append(
            StrategyOutcome(d.id.value, float(cost.mean()), float(fill.mean()), p_meet, feasible)
        )
    feas = [o for o in outs if o.feasible]
    preferred = min(feas, key=lambda o: o.mean_cost).strategy_id if feas else None
    return ScenarioOutcome(inputs, outs, preferred)


# ---------------------------------------------------------------------------
# One-way thresholds and decision reversal
# ---------------------------------------------------------------------------


def one_way(
    designs: list[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    seed: int,
    runs: list[int],
    tau: float,
    q: float,
    inputs: list[str] | None = None,
    levels: int = 3,
) -> dict[str, Any]:
    names = inputs or list(MANDATORY_INPUTS)
    base = evaluate_scenario(designs, product, glob, settings, seed, runs, tau, q, {})
    table: dict[str, Any] = {"base": asdict(base), "inputs": {}}
    for name in names:
        lo, b, hi = input_range(product, glob, name)
        grid = np.linspace(lo, hi, levels) if levels > 1 else np.array([b])
        rows = []
        for v in grid:
            sc = evaluate_scenario(
                designs, product, glob, settings, seed, runs, tau, q, {name: float(v)}
            )
            rows.append(
                {
                    "value": float(v),
                    "preferred": sc.preferred,
                    "reversal": sc.preferred != base.preferred,
                    "outcomes": [asdict(o) for o in sc.outcomes],
                }
            )
        table["inputs"][name] = {
            "low": lo,
            "base": b,
            "high": hi,
            "rows": rows,
            "any_reversal": any(r["reversal"] for r in rows),
        }
    return table


def decision_reversal_map(
    designs: list[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    seed: int,
    runs: list[int],
    tau: float,
    q: float,
    axes: dict[str, list[float]],
) -> dict[str, Any]:
    """Preferred strategy over a grid of 2-3 axes (protocol 11.4)."""
    names = list(axes)
    cells = []
    for combo in (
        np.array(np.meshgrid(*[axes[n] for n in names], indexing="ij")).reshape(len(names), -1).T
    ):
        inputs = {n: float(v) for n, v in zip(names, combo, strict=True)}
        sc = evaluate_scenario(designs, product, glob, settings, seed, runs, tau, q, inputs)
        cells.append(
            {
                "inputs": inputs,
                "preferred": sc.preferred,
                "costs": sc.cost_by_strategy,
                "feasible": [o.strategy_id for o in sc.outcomes if o.feasible],
            }
        )
    return {"axes": axes, "cells": cells}


# ---------------------------------------------------------------------------
# Global sensitivity: Sobol and PRCC on a paired response
# ---------------------------------------------------------------------------


def _problem(product: ProductConfig, glob: ParameterSet, names: list[str]) -> dict[str, Any]:
    bounds = []
    for n in names:
        lo, _b, hi = input_range(product, glob, n)
        if hi <= lo:
            hi = lo + max(abs(lo) * 1e-3, 1e-6)
        bounds.append([lo, hi])
    return {"num_vars": len(names), "names": names, "bounds": bounds}


def prcc(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Partial rank correlation coefficients of each column of x with y."""
    rx = np.apply_along_axis(stats.rankdata, 0, x)
    ry = stats.rankdata(y)
    n, k = rx.shape
    out = np.zeros(k)
    for j in range(k):
        others = np.delete(rx, j, axis=1)
        a = np.column_stack([np.ones(n), others])
        beta_x, *_ = np.linalg.lstsq(a, rx[:, j], rcond=None)
        beta_y, *_ = np.linalg.lstsq(a, ry, rcond=None)
        res_x = rx[:, j] - a @ beta_x
        res_y = ry - a @ beta_y
        denom = float(np.sqrt((res_x**2).sum() * (res_y**2).sum()))
        out[j] = float((res_x * res_y).sum() / denom) if denom > 0 else 0.0
    return out


def global_sensitivity(
    response: Callable[[dict[str, float]], float],
    product: ProductConfig,
    glob: ParameterSet,
    names: list[str],
    *,
    n_base: int = 32,
    seed: int = 1,
) -> dict[str, Any]:
    """Sobol first/total indices (Saltelli sampling) and PRCC on the same sample."""
    problem = _problem(product, glob, names)
    x = sobol_sample.sample(problem, n_base, calc_second_order=False, seed=seed)
    y = np.array([response({n: float(v) for n, v in zip(names, row, strict=True)}) for row in x])
    finite = np.isfinite(y)
    si = sobol_analyze.analyze(
        problem,
        np.where(finite, y, np.nanmax(y[finite]) if finite.any() else 0.0),
        calc_second_order=False,
        print_to_console=False,
        seed=seed,
    )
    pr = (
        prcc(x[finite], y[finite]) if finite.sum() > len(names) + 2 else np.full(len(names), np.nan)
    )
    return {
        "names": names,
        "n_samples": int(x.shape[0]),
        "S1": [float(v) for v in si["S1"]],
        "S1_conf": [float(v) for v in si["S1_conf"]],
        "ST": [float(v) for v in si["ST"]],
        "ST_conf": [float(v) for v in si["ST_conf"]],
        "PRCC": [float(v) for v in pr],
        "response_finite_fraction": float(finite.mean()),
    }


# ---------------------------------------------------------------------------
# Value of information
# ---------------------------------------------------------------------------


@dataclass
class VoiResult:
    evpi: float
    evppi: dict[str, float]
    n_samples: int
    expected_cost_by_strategy: dict[str, float]
    best_strategy: str | None
    notes: list[str] = field(default_factory=list)


def value_of_information(
    designs: list[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    names: list[str],
    seed: int,
    runs: list[int],
    tau: float,
    q: float,
    n_samples: int = 64,
    infeasible_cost: float | None = None,
) -> VoiResult:
    """EVPI and single-parameter EVPPI (regression, Strong-Oakley-Brennan) on annual cost.

    Loss = annual cost for feasible strategies; an infeasible strategy in a sample gets
    ``infeasible_cost`` (default: the maximum feasible cost observed x 2) so that it is
    never chosen when any feasible strategy exists.
    """
    rng = np.random.default_rng(seed)
    ranges = {n: input_range(product, glob, n) for n in names}
    x = np.column_stack(
        [
            rng.triangular(ranges[n][0], ranges[n][1], ranges[n][2], size=n_samples)
            if ranges[n][2] > ranges[n][0]
            else np.full(n_samples, ranges[n][1])
            for n in names
        ]
    )
    sids = [d.id.value for d in designs]
    cost = np.full((n_samples, len(designs)), np.nan)
    feas = np.zeros((n_samples, len(designs)), dtype=bool)
    for i in range(n_samples):
        sc = evaluate_scenario(
            designs,
            product,
            glob,
            settings,
            seed,
            runs,
            tau,
            q,
            {n: float(v) for n, v in zip(names, x[i], strict=True)},
        )
        for j, o in enumerate(sc.outcomes):
            cost[i, j] = o.mean_cost
            feas[i, j] = o.feasible
    cap = (
        infeasible_cost
        if infeasible_cost is not None
        else (
            float(np.nanmax(np.where(feas, cost, np.nan))) * 2.0
            if feas.any()
            else float(np.nanmax(cost)) * 2.0
        )
    )
    loss = np.where(feas, cost, cap)
    exp_cost = loss.mean(axis=0)
    best = int(np.argmin(exp_cost))
    evpi = float(exp_cost[best] - loss.min(axis=1).mean())
    evppi: dict[str, float] = {}
    for j, n in enumerate(names):
        xi = x[:, j]
        if np.ptp(xi) == 0:
            evppi[n] = 0.0
            continue
        fitted = np.column_stack(
            [np.polyval(np.polyfit(xi, loss[:, k], 3), xi) for k in range(len(designs))]
        )
        evppi[n] = max(float(exp_cost[best] - fitted.min(axis=1).mean()), 0.0)
    return VoiResult(
        evpi=max(evpi, 0.0),
        evppi=evppi,
        n_samples=n_samples,
        expected_cost_by_strategy={s: float(v) for s, v in zip(sids, exp_cost, strict=True)},
        best_strategy=sids[best] if feas.any() else None,
        notes=[f"infeasible strategies charged {cap:.0f} per sample"],
    )


def dump(obj: Any, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            obj,
            f,
            indent=2,
            default=lambda o: (
                asdict(o)
                if hasattr(o, "__dataclass_fields__")
                else (float(o) if isinstance(o, np.floating) else str(o))
            ),
        )


def _finite(v: float) -> float:
    return v if math.isfinite(v) else float("nan")
