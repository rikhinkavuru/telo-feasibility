"""Fair-comparison check: optimize named strategies over a matched search space.

The frozen comparators' design spaces (``optimization.DESIGN_SPACES``) were written for
the workbook's multiplier designs and give the distributed-node strategies less inventory
freedom than the design-space strategies declare for themselves: safety stock to 90 days
with no daily base-stock review, against 365 days with the review binary. Model defect
MD-12 records the omission. A comparison across that gap is not a comparison of
architectures, so this script re-optimizes the named strategies over one common inventory
space and reports both results side by side.

It writes a labelled supplementary run; it does not change any frozen design space.

Usage: uv run python scripts/run_matched_space_check.py [--strategies S1,S5,S6] [--runs 40]
"""

from __future__ import annotations

import argparse
import time
from dataclasses import asdict

from telo_feasibility.configs import load_all_strategies, load_gates, load_global, load_products
from telo_feasibility.design_space_analysis import RESULTS_DS, write_json
from telo_feasibility.disruptions import DAYS_PER_YEAR
from telo_feasibility.optimization import Variable, optimize_strategy, space_for
from telo_feasibility.provenance import load_protocol
from telo_feasibility.regulatory import evaluate_all
from telo_feasibility.runner import load_sim_config
from telo_feasibility.schemas import StrategyId
from telo_feasibility.simulation import SimSettings

# the inventory freedom every design-space strategy declares for itself
MATCHED_INVENTORY = [
    Variable("safety_stock_days", 30.0, 365.0, "float", 4),
    Variable("region_base_stock", 0.0, 1.0, "int", 2),
]


def matched_space(design_space: list[Variable]) -> list[Variable]:
    """The strategy's own non-inventory variables plus the common inventory space."""
    keep = [v for v in design_space if v.name not in {"safety_stock_days", "region_base_stock"}]
    return keep + MATCHED_INVENTORY


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategies", default="S1,S5,S6")
    ap.add_argument("--runs", type=int, default=40)
    ap.add_argument("--search-runs", type=int, default=12)
    ap.add_argument("--horizon-years", type=float, default=5.0)
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    t0 = time.time()
    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    protocol = load_protocol()
    th = protocol.service_thresholds
    glob, products = load_global(), load_products()
    registry = load_all_strategies()
    elig = {k.value: v.eligibility for k, v in evaluate_all(load_gates()).items()}
    sids = [s.strip() for s in args.strategies.split(",") if s.strip()]
    seed, warm = int(cfg["master_seed"]), int(cfg["warm_up_days"])
    out: dict[str, dict[str, object]] = {}
    for pid, product in products.items():
        settings = SimSettings(
            horizon_days=warm + round(args.horizon_years * DAYS_PER_YEAR),
            warm_up_days=warm,
            shortage_day_threshold=th.shortage_day_threshold,
            fill_rate_mean_min=th.fill_rate_mean_min,
            recovery_window_days=th.recovery_window_days,
            record_events=False,
            shortage_listed_at_t0=bool(listed.get(pid, False)),
        )
        for sid in sids:
            design = registry.by_id(StrategyId(sid))
            own = space_for(design)
            for label, space in (("declared", own), ("matched", matched_space(own))):
                rec = optimize_strategy(
                    design,
                    product,
                    glob,
                    settings,
                    master_seed=seed,
                    search_runs=list(range(args.search_runs)),
                    final_runs=list(range(args.runs)),
                    tau=th.fill_rate_mean_min,
                    q=th.fill_rate_tail_confidence,
                    eligibility=elig[sid],
                    space=space,
                )
                b = rec.best or rec.best_grid
                out[f"{pid}|{sid}|{label}"] = {
                    "status": rec.status,
                    "space": [v.name for v in space],
                    "best_design": b.design_variables if b else None,
                    "mean_cost": b.mean_cost if b else None,
                    "mean_fill": b.mean_fill if b else None,
                    "p_meet": b.p_meet if b else None,
                    "feasible": b.feasible if b else False,
                    "evaluations": len(rec.evaluations),
                }
                print(
                    f"[{time.time() - t0:.0f}s] {pid[:6]} {sid} {label:8s} {rec.status:20s} "
                    f"fill={b.mean_fill if b else float('nan'):.4f} p={b.p_meet if b else float('nan'):.2f} "
                    f"cost={(b.mean_cost / 1e6) if b else float('nan'):.1f}M"
                )
    rid = args.run_id or f"matched_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    path = write_json(
        {
            "meta": {
                "run_id": rid,
                "purpose": (
                    "fair-comparison check for model defect MD-12: the frozen comparators' design "
                    "spaces give less inventory freedom than the design-space strategies declare, "
                    "so this run optimizes each named strategy twice, over its declared space and "
                    "over a common inventory space, and reports both"
                ),
                "matched_inventory_space": [asdict(v) for v in MATCHED_INVENTORY],
                "tau": th.fill_rate_mean_min,
                "q": th.fill_rate_tail_confidence,
                "runs": args.runs,
                "search_runs": args.search_runs,
                "master_seed": seed,
                "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
            },
            "by_key": out,
        },
        RESULTS_DS / f"{rid}.json",
    )
    print(f"results -> {path} ({time.time() - t0:.0f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
