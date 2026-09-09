"""Strategy optimization to the frozen service target (protocol 10.1, Eq. 10; task section 17).

Method (auditable; decision D010):

1. Coarse full-factorial grid over each strategy's design space, every point simulated on
   one common-random-number batch of runs. Feasible = mean fill rate >= tau and the share of
   runs meeting tau >= q (protocol service_thresholds). Regulatory eligibility is checked
   before any search; an EXCLUDED strategy is not optimized, and a NO_CONCLUSION strategy
   is optimized for information only and labeled.
2. Coordinate refinement from the best feasible grid point: each continuous variable is
   bisected toward its neighbors for a fixed number of rounds; integer variables are stepped.
3. The best feasible design is re-evaluated on the full run set with Monte Carlo standard
   errors.

Everything evaluated is recorded (design, cost, fill, feasibility) so the search can be
audited against the grid. No penalty converts an infeasible design into a feasible one.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from .configs import ProductConfig, load_all_strategies, load_gates, load_global, load_products
from .provenance import PACKAGE_ROOT
from .regulatory import evaluate_all
from .schemas import Eligibility, ParameterSet, StrategyDesign, StrategyId
from .simulation import SimSettings, run_paired

RESULTS_OPT = PACKAGE_ROOT / "results" / "optimization"


@dataclass(frozen=True)
class Variable:
    name: str
    low: float
    high: float
    kind: str  # "float" | "int"
    grid: int  # grid points in stage 1

    def points(self) -> list[float]:
        if self.kind == "int":
            lo, hi = round(self.low), round(self.high)
            vals = sorted({round(v) for v in np.linspace(lo, hi, min(self.grid, hi - lo + 1))})
            return [float(v) for v in vals]
        return [float(v) for v in np.linspace(self.low, self.high, self.grid)]


# Design spaces per strategy (protocol 3.2). Bounds are search bounds, not evidence.
LEGACY_DESIGN_SPACES: dict[StrategyId, list[Variable]] = {
    StrategyId.S0: [
        Variable("safety_stock_days", 5.0, 90.0, "float", 4),
        Variable("site_fg_days", 5.0, 60.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 3),
    ],
    StrategyId.S1: [
        Variable("safety_stock_days", 30.0, 365.0, "float", 5),
        Variable("site_fg_days", 5.0, 60.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 3),
    ],
    StrategyId.S2: [
        Variable("capacity_factor", 0.6, 2.0, "float", 4),
        Variable("independent_api_supplier", 0.0, 1.0, "int", 2),
        Variable("safety_stock_days", 10.0, 120.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 3),
    ],
    StrategyId.S3: [
        Variable("reserved_capacity_fraction", 0.1, 1.0, "float", 4),
        Variable("activation_threshold_days", 3.0, 45.0, "float", 3),
        Variable("campaign_batches", 1.0, 6.0, "int", 3),
        Variable("safety_stock_days", 10.0, 120.0, "float", 3),
    ],
    StrategyId.S4: [
        Variable("capacity_factor", 0.8, 2.5, "float", 5),
        Variable("safety_stock_days", 10.0, 120.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 3),
    ],
    StrategyId.S5: [
        Variable("sites", 1.0, 4.0, "int", 4),
        Variable("node_scale", 0.15, 1.0, "float", 4),
        Variable("safety_stock_days", 10.0, 90.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 2),
    ],
    StrategyId.S6: [
        Variable("sites", 1.0, 4.0, "int", 4),
        Variable("node_scale", 0.15, 1.0, "float", 4),
        Variable("safety_stock_days", 10.0, 90.0, "float", 3),
        Variable("material_target_days", 30.0, 180.0, "float", 2),
    ],
    StrategyId.S7: [
        Variable("capacity_factor", 1.05, 2.0, "float", 4),
        Variable("safety_stock_days", 5.0, 90.0, "float", 3),
    ],
}

# The inventory freedom every design-space strategy declares for itself. Revision R009
# (model defects MD-3 and MD-12) gives the frozen comparators the same freedom, because a
# comparison run across unequal search boxes measures the box and not the architecture.
# `scripts/run_matched_space_check.py` measured what the gap was worth before this change:
# added central capacity moved from infeasible to feasible on both products at roughly 60%
# of its declared-space cost.
# Grid counts are kept to the endpoints (2, 2, 2, 2 = 16 combinations) because the stage-1
# search is full factorial: adding four variables to a strategy that already has two would
# otherwise multiply its grid by an order of magnitude, and the twenty-strategy battery
# became an eight-hour job. Stage 1 is a screen; stage 2 bisects the continuous variables
# between the endpoints and stage 3 re-evaluates the incumbent at full N, so the interior
# of the range is searched by refinement rather than by enumeration.
MATCHED_INVENTORY_SPACE: list[Variable] = [
    Variable("safety_stock_days", 30.0, 365.0, "float", 2),
    Variable("region_base_stock", 0.0, 1.0, "int", 2),
    Variable("site_fg_days", 5.0, 180.0, "float", 2),
    Variable("material_target_days", 30.0, 180.0, "float", 2),
]
MATCHED_INVENTORY_NAMES = frozenset(v.name for v in MATCHED_INVENTORY_SPACE)


def _matched(space: list[Variable]) -> list[Variable]:
    """A strategy's own non-inventory variables plus the common inventory space."""
    return [v for v in space if v.name not in MATCHED_INVENTORY_NAMES] + MATCHED_INVENTORY_SPACE


# Active spaces. S7 keeps `site_fg_days` and `material_target_days` like every other
# strategy; its 503B responder is the only site that cannot use them, and a variable a
# topology ignores costs only search time.
DESIGN_SPACES: dict[StrategyId, list[Variable]] = {
    sid: _matched(space) for sid, space in LEGACY_DESIGN_SPACES.items()
}


def space_for(design: StrategyDesign) -> list[Variable]:
    """Search space: the frozen table for S0-S7, the configuration block for S8+."""
    if design.id in DESIGN_SPACES:
        return DESIGN_SPACES[design.id]
    if not design.design_space:
        raise ValueError(f"{design.id.value}: no design space declared")
    return [Variable(v.name, v.low, v.high, v.kind, v.grid) for v in design.design_space]


@dataclass
class Evaluation:
    design_variables: dict[str, float]
    mean_cost: float
    mean_fill: float
    p_meet: float
    mean_shortage_days: float
    mean_cost_per_unit: float
    feasible: bool
    n_runs: int
    stage: str
    mcse_cost: float = float("nan")


def _fill_tolerance(evaluations: list[Evaluation], n_runs: int) -> float:
    """Fill difference below which two designs are not distinguishable on this screen.

    Two sources of noise bound a comparison of mean fill on a common-random-number batch:
    the Monte Carlo standard error of the mean fill itself, approximated here from the
    spread of the evaluated designs, and the resolution of the tail test, whose binomial
    standard error at the protocol's q is 0.067 on a 20-run screen. The larger of a
    conservative floor and the observed spread is used, so a screen that happens to be
    tight does not license a decision the run size cannot support.
    """
    if n_runs <= 0:
        return 0.0
    fills = [e.mean_fill for e in evaluations if math.isfinite(e.mean_fill)]
    if len(fills) < 2:
        return 0.0
    spread = float(np.std(np.array(fills), ddof=1)) / math.sqrt(n_runs)
    floor = 0.5 / n_runs  # half of one run's worth of the tail proportion
    return max(spread, floor)


@dataclass
class OptimizationRecord:
    product_id: str
    strategy_id: str
    eligibility: str
    tau: float
    q: float
    search_runs: list[int]
    final_runs: list[int]
    master_seed: int
    bounds: dict[str, tuple[float, float]]
    evaluations: list[Evaluation] = field(default_factory=list)
    best: Evaluation | None = None
    best_grid: Evaluation | None = None
    status: str = "not_run"  # optimal | infeasible | excluded
    fill_tolerance: float = 0.0  # MD-11: noise band used to rank infeasible points
    wall_time_s: float = 0.0
    notes: list[str] = field(default_factory=list)
    banner: str = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"


def _evaluate(
    design: StrategyDesign,
    dv: dict[str, float],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    seed: int,
    runs: list[int],
    tau: float,
    q: float,
    stage: str,
) -> Evaluation:
    d = design.model_copy(deep=True)
    d.design_variables.update(dv)
    res = run_paired([d], product, glob, settings, seed, runs)
    cost = np.array([r.metrics["annual_total_cost"] for r in res])
    fill = np.array([r.metrics["fill_rate"] for r in res])
    sd = np.array([r.metrics["shortage_days_per_year"] for r in res])
    cpu = np.array([r.metrics["cost_per_delivered_unit"] for r in res])
    p_meet = float((fill >= tau).mean())
    feasible = bool(fill.mean() >= tau and p_meet >= q)
    return Evaluation(
        design_variables=dict(dv),
        mean_cost=float(cost.mean()),
        mean_fill=float(fill.mean()),
        p_meet=p_meet,
        mean_shortage_days=float(sd.mean()),
        mean_cost_per_unit=float(cpu[np.isfinite(cpu)].mean())
        if np.isfinite(cpu).any()
        else float("inf"),
        feasible=feasible,
        n_runs=len(res),
        stage=stage,
        mcse_cost=float(cost.std(ddof=1) / math.sqrt(len(cost))) if len(cost) > 1 else float("nan"),
    )


def optimize_strategy(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    *,
    master_seed: int,
    search_runs: list[int],
    final_runs: list[int],
    tau: float,
    q: float,
    eligibility: Eligibility,
    refinement_rounds: int = 2,
    space: list[Variable] | None = None,
) -> OptimizationRecord:
    t0 = time.time()
    vars_ = space if space is not None else space_for(design)
    rec = OptimizationRecord(
        product_id=product.id,
        strategy_id=design.id.value,
        eligibility=eligibility.value,
        tau=tau,
        q=q,
        search_runs=list(search_runs),
        final_runs=list(final_runs),
        master_seed=master_seed,
        bounds={v.name: (v.low, v.high) for v in vars_},
    )
    if eligibility is Eligibility.EXCLUDED:
        rec.status = "excluded"
        rec.notes.append("strategy excluded by a failed regulatory gate; not optimized")
        rec.wall_time_s = time.time() - t0
        return rec
    if eligibility is Eligibility.NO_CONCLUSION:
        rec.notes.append(
            "regulatory gates UNCERTAIN: optimized for information only; no favorable conclusion possible"
        )

    # stage 1: grid
    grid_points = list(itertools.product(*[v.points() for v in vars_]))
    for pt in grid_points:
        dv = {v.name: float(x) for v, x in zip(vars_, pt, strict=True)}
        rec.evaluations.append(
            _evaluate(design, dv, product, glob, settings, master_seed, search_runs, tau, q, "grid")
        )
    feasible = [e for e in rec.evaluations if e.feasible]
    if not feasible:
        rec.status = "infeasible"
        # MD-11 (revision R009): rank infeasible points on fill only where the difference
        # is larger than the noise the screen carries, then on cost. Ranking on raw fill
        # bought large cost increases for differences inside a standard error: on the
        # 2026-09-03 run norepinephrine S5 paid 9.26M USD/yr more for 0.00004 of fill,
        # about 0.02 of one standard error.
        tol = _fill_tolerance(rec.evaluations, len(search_runs))
        rec.fill_tolerance = tol
        best_fill = max(e.mean_fill for e in rec.evaluations)
        near_best = [e for e in rec.evaluations if e.mean_fill >= best_fill - tol]
        cheapest_closest = min(near_best, key=lambda e: (e.mean_cost, -e.mean_fill))
        rec.best_grid = cheapest_closest
        rec.notes.append(
            f"no grid design met tau={tau} with q={q}; closest fill {best_fill:.3f}; "
            f"reported design is the cheapest within a fill tolerance of {tol:.5f} "
            f"({len(near_best)} of {len(rec.evaluations)} evaluations qualified)"
        )
        rec.wall_time_s = time.time() - t0
        return rec
    best = min(feasible, key=lambda e: e.mean_cost)
    rec.best_grid = best

    # stage 2: coordinate refinement (bisection toward neighbors) on continuous variables
    current = dict(best.design_variables)
    current_eval = best
    for _round in range(refinement_rounds):
        improved = False
        for v in vars_:
            pts = v.points()
            x = current[v.name]
            idx = int(np.argmin([abs(p - x) for p in pts]))
            candidates: list[float] = []
            if v.kind == "int":
                candidates = [x - 1.0, x + 1.0]
            else:
                step = (v.high - v.low) / max(v.grid - 1, 1) / (2 ** (_round + 1))
                candidates = [x - step, x + step]
            for cand in candidates:
                if cand < v.low or cand > v.high:
                    continue
                dv = dict(current)
                dv[v.name] = float(cand)
                ev = _evaluate(
                    design,
                    dv,
                    product,
                    glob,
                    settings,
                    master_seed,
                    search_runs,
                    tau,
                    q,
                    f"refine{_round + 1}",
                )
                rec.evaluations.append(ev)
                if ev.feasible and ev.mean_cost < current_eval.mean_cost:
                    current, current_eval, improved = dv, ev, True
            _ = idx
        if not improved:
            break

    # stage 3: full re-evaluation of the incumbent
    final = _evaluate(
        design, current, product, glob, settings, master_seed, final_runs, tau, q, "final"
    )
    rec.evaluations.append(final)
    rec.best = final
    rec.status = "optimal" if final.feasible else "infeasible_at_full_n"
    if not final.feasible:
        rec.notes.append(
            "search-batch feasibility did not survive full-N re-evaluation; report as infeasible"
        )
    rec.wall_time_s = time.time() - t0
    return rec


def _optimize_task(
    args: tuple[str, str, SimSettings, int, int, int, float, float, str],
) -> OptimizationRecord:
    pid, sid, settings, master_seed, search_n, final_n, tau, q, elig = args
    return optimize_strategy(
        load_all_strategies().by_id(StrategyId(sid)),
        load_products()[pid],
        load_global(),
        settings,
        master_seed=master_seed,
        search_runs=list(range(search_n)),
        final_runs=list(range(final_n)),
        tau=tau,
        q=q,
        eligibility=Eligibility(elig),
    )


def optimize_all(
    *,
    product_ids: list[str] | None = None,
    strategy_ids: list[str] | None = None,
    search_n: int = 20,
    final_n: int = 100,
    master_seed: int = 20260901,
    horizon_days: int = 365 + 1826,
    warm_up_days: int = 365,
    out_root: Path = RESULTS_OPT,
    listed_by_product: dict[str, bool] | None = None,
    tau_override: float | None = None,
    q_override: float | None = None,
) -> Path:
    from .provenance import build_run_manifest, load_protocol, write_manifest

    protocol = load_protocol()
    th = protocol.service_thresholds
    tau = tau_override if tau_override is not None else th.fill_rate_mean_min
    q = q_override if q_override is not None else th.fill_rate_tail_confidence
    load_global()
    products = load_products()
    registry = load_all_strategies()
    gates = load_gates()
    elig = evaluate_all(gates)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"opt_{stamp}" + (f"_tau{tau}" if tau_override is not None else "")
    out = out_root / run_id
    out.mkdir(parents=True, exist_ok=True)
    pids = product_ids or list(products)
    sids = [StrategyId(s) for s in (strategy_ids or [d.id.value for d in registry.designs])]
    summary: dict[str, Any] = {
        "run_id": run_id,
        "tau": tau,
        "q": q,
        "records": {},
        "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
    }
    import os
    from concurrent.futures import ProcessPoolExecutor

    tasks: list[tuple[str, str, SimSettings, int, int, int, float, float, str]] = []
    for pid in pids:
        listed = bool((listed_by_product or {}).get(pid, False))
        settings = SimSettings(
            horizon_days=horizon_days,
            warm_up_days=warm_up_days,
            shortage_day_threshold=th.shortage_day_threshold,
            fill_rate_mean_min=th.fill_rate_mean_min,
            recovery_window_days=th.recovery_window_days,
            record_events=False,
            shortage_listed_at_t0=listed,
        )
        for sid in sids:
            tasks.append(
                (
                    pid,
                    sid.value,
                    settings,
                    master_seed,
                    search_n,
                    final_n,
                    tau,
                    q,
                    elig[sid].eligibility.value,
                )
            )
    workers = max((os.cpu_count() or 2) - 1, 1)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        records = list(ex.map(_optimize_task, tasks))
    for rec in records:
        pid, sid_value = rec.product_id, rec.strategy_id
        (out / f"{pid}__{sid_value}.json").write_text(
            json.dumps(asdict(rec), indent=2, default=str), encoding="utf-8"
        )
        b = rec.best
        summary["records"][f"{pid}|{sid_value}"] = {
            "status": rec.status,
            "eligibility": rec.eligibility,
            "best_design": b.design_variables if b else None,
            "mean_cost": b.mean_cost if b else None,
            "mcse_cost": b.mcse_cost if b else None,
            "mean_fill": b.mean_fill if b else None,
            "p_meet": b.p_meet if b else None,
            "mean_cost_per_unit": b.mean_cost_per_unit if b else None,
            "evaluations": len(rec.evaluations),
            "wall_time_s": rec.wall_time_s,
            "closest_fill_if_infeasible": rec.best_grid.mean_fill
            if (rec.best_grid and rec.status == "infeasible")
            else None,
        }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    manifest = build_run_manifest(
        run_id,
        protocol=protocol,
        config_objects={
            "search_n": search_n,
            "final_n": final_n,
            "spaces": {
                d.id.value: [asdict(v) for v in space_for(d)]
                for d in registry.designs
                if d.id in sids
            },
        },
        master_seed=master_seed,
        n_runs=final_n,
        illustrative=True,
        gate_outcomes={
            k.value: {g: s.value for g, s in v.gate_statuses.items()} for k, v in elig.items()
        },
        notes=f"optimization; results {out}",
    )
    write_manifest(manifest)
    return out
