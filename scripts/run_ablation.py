"""Failure decomposition by ablation (design-space assignment, Phase A).

Runs every strategy for both products under the base world, each mechanism switched off
one at a time (leave-one-out), the quiet world, and each mechanism switched on alone
(add-one-in), all on common random numbers. Designs default to the frozen-target
optimization run's best (or closest) design per strategy.

Usage: uv run python scripts/run_ablation.py [--runs 100] [--opt-run opt_20260902T043854Z]
       [--designs baseline] [--pairs factor1,factor2,...] [--horizon-years 5]
"""

from __future__ import annotations

import argparse
import time

from telo_feasibility.ablation import (
    RESULTS_ABL,
    default_configs,
    load_design_variables,
    pair_configs,
    run_ablation,
)
from telo_feasibility.optimization import RESULTS_OPT
from telo_feasibility.runner import load_sim_config


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=100)
    ap.add_argument("--opt-run", default="opt_20260902T043854Z")
    ap.add_argument("--designs", choices=["optimized", "baseline"], default="optimized")
    ap.add_argument("--pairs", default="", help="comma-separated factors for a factorial study")
    ap.add_argument("--only", default="", help="comma-separated config ids to run (default all)")
    ap.add_argument("--horizon-years", type=float, default=5.0)
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--workers", type=int, default=0, help="0 = all CPUs minus one")
    args = ap.parse_args()
    t0 = time.time()
    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    if args.pairs:
        configs = pair_configs(args.pairs.split(","))
        configs.insert(0, default_configs()[0])
    else:
        configs = default_configs()
    if args.only:
        keep = set(args.only.split(","))
        configs = [c for c in configs if c.id in keep]
    dvs = load_design_variables(RESULTS_OPT / args.opt_run) if args.designs == "optimized" else {}
    out = run_ablation(
        configs=configs,
        n_runs=args.runs,
        master_seed=int(cfg["master_seed"]),
        product_ids=[str(p["id"]) for p in cfg["products"]],
        listed_by_product=listed,
        horizon_years=args.horizon_years,
        warm_up_days=int(cfg["warm_up_days"]),
        design_variables=dvs,
        designs_label=f"{args.designs}:{args.opt_run}"
        if args.designs == "optimized"
        else "baseline",
        out_root=RESULTS_ABL,
        workers=args.workers,
        run_id=args.run_id,
    )
    print(f"results -> {out} ({time.time() - t0:.0f}s, {len(configs)} configs)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
