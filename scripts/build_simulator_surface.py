"""Precompute the response surface the interactive simulator reads.

The simulator lets a reader move one assumption at a time away from the base case and watch
which architectures still meet the service target. That is the one-way sensitivity the
protocol already specifies, so the surface is a set of one-at-a-time sweeps rather than a
full factorial: every point is a real paired simulation of every strategy at that input
value with all other inputs at base, on the same common random numbers as the report. The
simulator interpolates nothing and re-implements nothing.

Usage: .venv/bin/python scripts/build_simulator_surface.py [--runs 40] [--levels 5]
Writes results/design_space/simulator_surface.json.
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

from telo_feasibility.configs import load_all_strategies, load_gates, load_global, load_products
from telo_feasibility.design_space_analysis import (
    ALL_INPUTS,
    RESULTS_DS,
    _range,
    evaluate,
    write_json,
)
from telo_feasibility.disruptions import DAYS_PER_YEAR
from telo_feasibility.provenance import load_protocol
from telo_feasibility.regulatory import evaluate_all
from telo_feasibility.runner import load_sim_config
from telo_feasibility.simulation import SimSettings

# the seven inputs the assignment names, plus the three this study found decisive
SWEEPS: list[tuple[str, str, str]] = [
    ("capacity_utilization", "Annual demand", "units per year against a fixed plant"),
    ("release_time", "Sterility hold", "days from fill to released stock"),
    ("fixed_qa_labor_per_node", "Fixed quality cost", "USD per site-year"),
    ("yield", "Yield", "fraction of filled units saleable"),
    ("uptime", "Uptime", "fraction of scheduled time the line runs"),
    ("demand_cv", "Demand volatility", "coefficient of variation of routine demand"),
    ("raw_material_lead_time", "Raw-material lead time", "days from order to receipt"),
    ("commissioning_days", "Commissioning", "days from decision to first released batch"),
]

_STATE: dict[str, object] = {}


def _init() -> None:
    if _STATE:
        return
    cfg = load_sim_config()
    _STATE["listed"] = {
        p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]
    }
    _STATE["seed"] = int(cfg["master_seed"])
    _STATE["warm"] = int(cfg["warm_up_days"])
    _STATE["glob"] = load_global()
    _STATE["products"] = load_products()
    _STATE["designs"] = list(load_all_strategies().designs)
    _STATE["elig"] = {k.value: v.eligibility for k, v in evaluate_all(load_gates()).items()}
    _STATE["th"] = load_protocol().service_thresholds


def _point(task: tuple[str, str, float, int, float]) -> tuple[str, str, float, dict[str, object]]:
    """Evaluate every strategy at one input value on one product."""
    name, pid, value, n_runs, horizon_years = task
    _init()
    th = _STATE["th"]
    settings = SimSettings(
        horizon_days=_STATE["warm"] + round(horizon_years * DAYS_PER_YEAR),
        warm_up_days=_STATE["warm"],
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=th.fill_rate_mean_min,
        recovery_window_days=th.recovery_window_days,
        record_events=False,
        shortage_listed_at_t0=bool(_STATE["listed"].get(pid, False)),
    )
    pts = evaluate(
        _STATE["designs"],
        _STATE["products"][pid],
        _STATE["glob"],
        settings,
        seed=_STATE["seed"],
        runs=list(range(n_runs)),
        tau=th.fill_rate_mean_min,
        q=th.fill_rate_tail_confidence,
        inputs={name: value},
        eligibility=_STATE["elig"],
    )
    by_strategy = {
        p.strategy_id: {
            "fill": round(p.mean_fill, 5),
            "p_meet": round(p.p_meet, 4),
            "cost": round(p.mean_cost, 0),
            "cost_per_unit": round(p.mean_cost_per_unit, 3),
            "shortage_days": round(p.mean_shortage_days, 2),
            "feasible": p.feasible,
        }
        for p in pts
    }
    return name, pid, value, by_strategy


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=40)
    ap.add_argument("--levels", type=int, default=5)
    ap.add_argument("--horizon-years", type=float, default=5.0)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    t0 = time.time()
    _init()

    glob, products, designs = _STATE["glob"], _STATE["products"], _STATE["designs"]
    th = _STATE["th"]
    tau, q = th.fill_rate_mean_min, th.fill_rate_tail_confidence

    grids: dict[tuple[str, str], dict[str, object]] = {}
    tasks: list[tuple[str, str, float, int, float]] = []
    for name, _label, _units in SWEEPS:
        if name not in ALL_INPUTS:
            print(f"skipping unknown input {name}")
            continue
        for pid, product in products.items():
            lo, base, hi = _range(product, glob, name)
            levels = sorted({float(v) for v in np.linspace(lo, hi, args.levels)} | {float(base)})
            grids[(name, pid)] = {"low": lo, "base": base, "high": hi, "levels": levels}
            tasks.extend((name, pid, v, args.runs, args.horizon_years) for v in levels)

    print(f"{len(tasks)} points, {len(designs)} strategies, {args.runs} runs each", flush=True)
    results: dict[tuple[str, str, float], dict[str, object]] = {}
    done = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(_point, t) for t in tasks]
        for fut in as_completed(futures):
            name, pid, value, by_strategy = fut.result()
            results[(name, pid, value)] = by_strategy
            done += 1
            print(
                f"[{time.time() - t0:6.0f}s] {done}/{len(tasks)}  {name} {pid[:8]} {value:.4g}",
                flush=True,
            )

    sweeps: list[dict[str, object]] = []
    for name, label, units in SWEEPS:
        if name not in ALL_INPUTS:
            continue
        by_product: dict[str, object] = {}
        for pid in products:
            g = grids[(name, pid)]
            by_product[pid] = {
                "low": g["low"],
                "base": g["base"],
                "high": g["high"],
                "points": [
                    {
                        "value": v,
                        "is_base": abs(v - float(g["base"])) < 1e-9,
                        "by_strategy": results[(name, pid, v)],
                    }
                    for v in g["levels"]
                ],
            }
        sweeps.append({"input": name, "label": label, "units": units, "by_product": by_product})

    out = {
        "meta": {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tau": tau,
            "q": q,
            "runs_per_point": args.runs,
            "master_seed": _STATE["seed"],
            "horizon_years": args.horizon_years,
            "warm_up_days": _STATE["warm"],
            "method": (
                "one assumption varied at a time from its base value with every other input held "
                "at base; each point is a full paired simulation of every strategy on common "
                "random numbers, not an interpolation"
            ),
            "binomial_se_at_requirement": round(float(np.sqrt(q * (1 - q) / args.runs)), 4),
            "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
        },
        "products": {
            pid: {"name": p.presentation.ingredient, "presentation": p.presentation.presentation}
            for pid, p in products.items()
        },
        "strategies": [
            {
                "id": d.id.value,
                "name": d.name,
                "family": d.family or ("frozen comparator" if d.id.is_frozen else ""),
                "frozen": d.id.is_frozen,
                "durable": d.durable,
            }
            for d in designs
        ],
        "sweeps": sweeps,
    }
    path = write_json(out, RESULTS_DS / "simulator_surface.json")
    print(f"\nsurface -> {path} ({time.time() - t0:.0f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
