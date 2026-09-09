"""Run the paired stochastic simulation from config/simulation.yaml.

Usage: uv run python scripts/run_simulation.py [--runs N]
"""

from __future__ import annotations

import argparse
import time

from telo_feasibility.runner import run_simulation

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument(
        "--strategies", default="", help="comma-separated ids (default: config/simulation.yaml)"
    )
    ap.add_argument("--products", default="", help="comma-separated product ids (default: all)")
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    t0 = time.time()
    out = run_simulation(
        n_runs=args.runs,
        strategy_ids_override=[s for s in args.strategies.split(",") if s] or None,
        product_ids_override=[p for p in args.products.split(",") if p] or None,
        run_id_override=args.run_id,
    )
    print(f"results -> {out} ({time.time() - t0:.1f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
