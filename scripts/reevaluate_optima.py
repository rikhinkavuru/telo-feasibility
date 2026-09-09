"""Re-evaluate an optimization run's incumbent designs at full run count.

An optimizer decides feasibility from the share of runs meeting the mean-fill target, so at
a small final-run count the classification is a coin flip near the requirement: at n = 40
the binomial standard error at q = 0.90 is 0.047, which is wider than most of the margins
that separate a feasible cell from an infeasible one. This script does not search. It takes
the design each cell already converged to and evaluates that one design on a larger paired
run set, so a change of classification can be attributed to the design rather than to the
screen size.

Usage: uv run python scripts/reevaluate_optima.py --opt-run opt_x [--runs 100] [--compare opt_y]
"""

from __future__ import annotations

import argparse
import json
import math
import time

from telo_feasibility.configs import load_all_strategies, load_gates, load_global, load_products
from telo_feasibility.design_space_analysis import RESULTS_DS, evaluate, write_json
from telo_feasibility.disruptions import DAYS_PER_YEAR
from telo_feasibility.optimization import RESULTS_OPT
from telo_feasibility.provenance import load_protocol
from telo_feasibility.regulatory import evaluate_all
from telo_feasibility.runner import load_sim_config
from telo_feasibility.schemas import StrategyId
from telo_feasibility.simulation import SimSettings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--opt-run", required=True)
    ap.add_argument("--runs", type=int, default=100)
    ap.add_argument("--compare", default="", help="an earlier optimization run to diff against")
    ap.add_argument("--horizon-years", type=float, default=5.0)
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    t0 = time.time()

    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    th = load_protocol().service_thresholds
    tau, q = th.fill_rate_mean_min, th.fill_rate_tail_confidence
    glob, products, registry = load_global(), load_products(), load_all_strategies()
    elig = {k.value: v.eligibility for k, v in evaluate_all(load_gates()).items()}
    seed, warm = int(cfg["master_seed"]), int(cfg["warm_up_days"])

    src = RESULTS_OPT / args.opt_run
    cells: dict[str, dict[str, object]] = {}
    for path in sorted(src.glob("*__S*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        pick = rec.get("best") or rec.get("best_grid")
        if not pick:
            continue
        cells[f"{rec['product_id']}|{rec['strategy_id']}"] = {
            "design": {k: float(v) for k, v in pick["design_variables"].items()},
            "declared_status": rec["status"],
            "declared_p_meet": pick.get("p_meet"),
            "declared_n": pick.get("n_runs"),
        }

    se_declared = None
    out: dict[str, object] = {}
    for key, cell in cells.items():
        pid, sid = key.split("|")
        design = registry.by_id(StrategyId(sid)).model_copy(deep=True)
        design.design_variables.update(cell["design"])  # type: ignore[arg-type]
        settings = SimSettings(
            horizon_days=warm + round(args.horizon_years * DAYS_PER_YEAR),
            warm_up_days=warm,
            shortage_day_threshold=th.shortage_day_threshold,
            fill_rate_mean_min=tau,
            recovery_window_days=th.recovery_window_days,
            record_events=False,
            shortage_listed_at_t0=bool(listed.get(pid, False)),
        )
        pt = evaluate(
            [design],
            products[pid],
            glob,
            settings,
            seed=seed,
            runs=list(range(args.runs)),
            tau=tau,
            q=q,
            eligibility=elig,
        )[0]
        se = math.sqrt(max(pt.p_meet * (1 - pt.p_meet), 1e-9) / args.runs)
        dn = int(cell["declared_n"] or args.runs)
        dp = float(cell["declared_p_meet"] or 0.0)
        se_declared = math.sqrt(max(dp * (1 - dp), 1e-9) / dn)
        out[key] = {
            **cell,
            "p_meet_at_full_n": pt.p_meet,
            "p_meet_se": se,
            "mean_fill": pt.mean_fill,
            "mean_cost": pt.mean_cost,
            "feasible_at_full_n": pt.feasible,
            "declared_p_meet_se": se_declared,
            "within_one_se_of_requirement": abs(pt.p_meet - q) <= se,
            "classification_changed": bool(pt.feasible) != (cell["declared_status"] == "optimal"),
        }
        print(
            f"[{time.time() - t0:.0f}s] {key:44s} declared {cell['declared_status']!s:20s} "
            f"p={dp:.3f}+-{se_declared:.3f}  ->  full n p={pt.p_meet:.3f}+-{se:.3f} "
            f"{'FEASIBLE' if pt.feasible else 'infeasible'}"
            f"{'  [within 1 SE of the requirement]' if abs(pt.p_meet - q) <= se else ''}",
            flush=True,
        )

    changed = [k for k, v in out.items() if v["classification_changed"]]
    borderline = [k for k, v in out.items() if v["within_one_se_of_requirement"]]
    meta = {
        "run_id": args.run_id or f"reeval_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}",
        "source_optimization": args.opt_run,
        "runs": args.runs,
        "tau": tau,
        "q": q,
        "master_seed": seed,
        "purpose": (
            "separate a change of feasibility classification caused by a model fix from one "
            "caused by a small final-run count, by re-evaluating each cell's own incumbent "
            "design on a larger paired run set without re-searching"
        ),
        "cells_reclassified_against_their_own_declaration": changed,
        "cells_within_one_standard_error_of_the_requirement": borderline,
        "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
    }
    path = write_json({"meta": meta, "by_key": out}, RESULTS_DS / f"{meta['run_id']}.json")
    print(f"\n{len(changed)} of {len(out)} cells change classification at full n")
    print(f"{len(borderline)} of {len(out)} sit within one standard error of the requirement")
    print(f"results -> {path} ({time.time() - t0:.0f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
