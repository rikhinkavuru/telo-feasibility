"""Optimize every eligible strategy to the frozen service target (protocol 10.1)."""

from __future__ import annotations

import argparse
import time

from telo_feasibility.optimization import optimize_all
from telo_feasibility.runner import load_sim_config

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--search-runs", type=int, default=20)
    ap.add_argument("--final-runs", type=int, default=100)
    ap.add_argument("--product", action="append", default=[])
    ap.add_argument("--strategy", action="append", default=[])
    ap.add_argument(
        "--tau",
        type=float,
        default=None,
        help="override mean fill-rate threshold (sensitivity only)",
    )
    ap.add_argument(
        "--q", type=float, default=None, help="override tail confidence (sensitivity only)"
    )
    args = ap.parse_args()
    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    t0 = time.time()
    out = optimize_all(
        product_ids=args.product or None,
        strategy_ids=args.strategy or None,
        search_n=args.search_runs,
        final_n=args.final_runs,
        master_seed=int(cfg["master_seed"]),
        listed_by_product=listed,
        tau_override=args.tau,
        q_override=args.q,
    )
    print(f"results -> {out} ({time.time() - t0:.0f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
