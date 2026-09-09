"""Sensitivity, decision-reversal map, and value of information (protocol 11).

Uses the optimized designs from the latest results/optimization run when present;
otherwise the illustrative baseline designs. Sizes are modest by default; raise them
with the flags and watch the reported sampling errors.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime

from telo_feasibility.configs import load_all_strategies, load_global, load_products
from telo_feasibility.provenance import PACKAGE_ROOT, load_protocol
from telo_feasibility.runner import load_sim_config
from telo_feasibility.sensitivity import (
    decision_reversal_map,
    dump,
    evaluate_scenario,
    global_sensitivity,
    input_range,
    one_way,
    value_of_information,
)
from telo_feasibility.simulation import SimSettings

OUT = PACKAGE_ROOT / "results" / "sensitivity"


def latest_optimized_designs() -> tuple[dict[str, dict[str, dict[str, float]]], str | None]:
    root = PACKAGE_ROOT / "results" / "optimization"
    runs = sorted(root.glob("opt_*/summary.json")) if root.exists() else []
    if not runs:
        return {}, None
    s = json.loads(runs[-1].read_text(encoding="utf-8"))
    out: dict[str, dict[str, dict[str, float]]] = {}
    for key, rec in s["records"].items():
        pid, sid = key.split("|")
        if rec.get("best_design"):
            out.setdefault(pid, {})[sid] = rec["best_design"]
    return out, s["run_id"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", default="sodium_bicarbonate_8_4_50ml")
    ap.add_argument("--runs", type=int, default=8, help="paired runs per scenario")
    ap.add_argument("--sobol-n", type=int, default=16, help="Saltelli base sample size")
    ap.add_argument("--voi-samples", type=int, default=48)
    ap.add_argument("--horizon-days", type=int, default=365 + 730)
    ap.add_argument(
        "--strategies", default="", help="comma-separated ids (default: every configured strategy)"
    )
    args = ap.parse_args()
    t0 = time.time()
    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    glob = load_global()
    product = load_products()[args.product]
    strategies = load_all_strategies()
    th = load_protocol().service_thresholds
    designs_by_pid, opt_run = latest_optimized_designs()
    keep = {s for s in args.strategies.split(",") if s}
    designs = []
    for d in strategies.designs:
        if keep and d.id.value not in keep:
            continue
        dd = d.model_copy(deep=True)
        dv = designs_by_pid.get(args.product, {}).get(d.id.value)
        if dv:
            dd.design_variables.update(dv)
        designs.append(dd)
    settings = SimSettings(
        horizon_days=args.horizon_days,
        warm_up_days=365,
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=th.fill_rate_mean_min,
        recovery_window_days=th.recovery_window_days,
        record_events=False,
        shortage_listed_at_t0=listed.get(args.product, False),
    )
    runs = list(range(args.runs))
    seed = int(cfg["master_seed"])
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    meta = {
        "product": args.product,
        "optimized_designs_run": opt_run,
        "designs": {d.id.value: d.design_variables for d in designs},
        "runs_per_scenario": args.runs,
        "horizon_days": args.horizon_days,
        "generated_at": stamp,
        "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
    }

    ow = one_way(
        designs,
        product,
        glob,
        settings,
        seed=seed,
        runs=runs,
        tau=th.fill_rate_mean_min,
        q=th.fill_rate_tail_confidence,
    )
    dump({"meta": meta, "one_way": ow}, str(OUT / "one_way.json"))
    print(
        f"one-way done ({time.time() - t0:.0f}s); reversals: {[k for k, v in ow['inputs'].items() if v['any_reversal']]}"
    )

    lo_u, b_u, hi_u = input_range(product, glob, "capacity_utilization")
    _lo_r, b_r, hi_r = input_range(product, glob, "release_time")
    lo_c, b_c, hi_c = input_range(product, glob, "common_cause_dependence")
    axes = {
        "capacity_utilization": [lo_u, b_u, hi_u],
        "release_time": [2.0, b_r, hi_r],
        "common_cause_dependence": [lo_c, b_c, hi_c],
    }
    drm = decision_reversal_map(
        designs,
        product,
        glob,
        settings,
        seed=seed,
        runs=runs,
        tau=th.fill_rate_mean_min,
        q=th.fill_rate_tail_confidence,
        axes=axes,
    )
    dump({"meta": meta, "map": drm}, str(OUT / "decision_reversal.json"))
    print(f"decision-reversal map done ({time.time() - t0:.0f}s)")

    names = [
        "capacity_utilization",
        "release_time",
        "fixed_qa_labor_per_node",
        "demand_cv",
        "raw_material_lead_time",
        "common_cause_dependence",
        "shelf_life",
        "node_scale",
    ]
    pair = ("S5", "S4")

    def response(vals: dict[str, float]) -> float:
        sc = evaluate_scenario(
            designs,
            product,
            glob,
            settings,
            seed,
            runs[: max(2, len(runs) // 2)],
            th.fill_rate_mean_min,
            th.fill_rate_tail_confidence,
            vals,
        )
        c = sc.cost_by_strategy
        return c[pair[0]] - c[pair[1]]

    gs = global_sensitivity(response, product, glob, names, n_base=args.sobol_n, seed=seed)
    dump(
        {"meta": meta, "response": f"annual cost {pair[0]} minus {pair[1]}", "sobol_prcc": gs},
        str(OUT / "global.json"),
    )
    print(
        f"Sobol/PRCC done ({time.time() - t0:.0f}s): ST={dict(zip(gs['names'], [round(x, 3) for x in gs['ST']], strict=False))}"
    )

    voi = value_of_information(
        designs,
        product,
        glob,
        settings,
        names=names,
        seed=seed,
        runs=runs[: max(2, len(runs) // 2)],
        tau=th.fill_rate_mean_min,
        q=th.fill_rate_tail_confidence,
        n_samples=args.voi_samples,
    )
    dump({"meta": meta, "voi": voi}, str(OUT / "voi.json"))
    print(f"VOI done ({time.time() - t0:.0f}s): EVPI={voi.evpi:.0f}; best={voi.best_strategy}")
    summary = {
        "meta": meta,
        "files": ["one_way.json", "decision_reversal.json", "global.json", "voi.json"],
        "reversal_inputs": [k for k, v in ow["inputs"].items() if v["any_reversal"]],
        "sobol_total_order": dict(zip(gs["names"], gs["ST"], strict=False)),
        "evpi": voi.evpi,
        "evppi": voi.evppi,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
