"""Feasibility regions, dominance, and reversal maps for every strategy (Phase E).

Usage:
  uv run python scripts/run_design_space_analysis.py [--products id,id] [--strategies S0,S8,...]
      [--runs 40] [--threshold-runs 20] [--inputs a,b,c] [--horizon-years 5] [--run-id ds_x]

Writes results/design_space/<run_id>/{thresholds.csv,dominance.csv,reversal.json,
contract_scenarios.csv,summary.json} and a run manifest. Designs come from the latest
optimization run when one covers the strategy, else from the strategy's configured design
variables.

``take_or_pay_fraction`` is swept here as a labelled contract scenario rather than searched
as a design variable. Model defect MD-24: it enters only the cost ledger and changes no
service quantity, so an optimizer selecting on cost among feasible designs would always
return its lower bound and delete the instrument that pays for the reserved line. The sweep
reports what each commitment level costs at unchanged service; choosing one is a contract
decision, not an optimization result.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict
from typing import Any

from telo_feasibility.ablation import load_design_variables
from telo_feasibility.configs import load_all_strategies, load_gates, load_global, load_products
from telo_feasibility.design_space_analysis import (
    ALL_INPUTS,
    RESULTS_DS,
    dominance,
    evaluate,
    reversal_map,
    threshold,
    write_json,
)
from telo_feasibility.design_space_analysis import (
    run_id as make_run_id,
)
from telo_feasibility.disruptions import DAYS_PER_YEAR
from telo_feasibility.optimization import RESULTS_OPT
from telo_feasibility.provenance import build_run_manifest, load_protocol, write_manifest
from telo_feasibility.regulatory import evaluate_all
from telo_feasibility.runner import load_sim_config
from telo_feasibility.simulation import SimSettings

DEFAULT_INPUTS = [
    "capacity_utilization",
    "fixed_qa_labor_per_node",
    "release_time",
    "shelf_life",
    "raw_material_lead_time",
    "common_cause_dependence",
    "supplier_concentration",
    "commissioning_days",
    "activation_latency_days",
    "node_capital",
    "batches_per_site_year",
    "changeover_burden",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--products", default="")
    ap.add_argument("--strategies", default="")
    ap.add_argument("--runs", type=int, default=40, help="paired runs for dominance and maps")
    ap.add_argument("--threshold-runs", type=int, default=20)
    ap.add_argument("--steps", type=int, default=5, help="bisection steps per threshold")
    ap.add_argument("--inputs", default=",".join(DEFAULT_INPUTS))
    ap.add_argument("--horizon-years", type=float, default=5.0)
    ap.add_argument("--opt-run", default="opt_20260902T043854Z")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--skip-reversal", action="store_true")
    ap.add_argument(
        "--take-or-pay",
        default="0.0,0.25,0.5,0.75,1.0",
        help="labelled contract scenario levels for take_or_pay_fraction (MD-24); empty to skip",
    )
    args = ap.parse_args()

    t0 = time.time()
    cfg = load_sim_config()
    listed = {p["id"]: bool(p.get("shortage_listed_at_t0", False)) for p in cfg["products"]}
    protocol = load_protocol()
    th = protocol.service_thresholds
    tau, q = th.fill_rate_mean_min, th.fill_rate_tail_confidence
    glob = load_global()
    products = load_products()
    registry = load_all_strategies()
    gates = load_gates()
    elig_by_id = {k.value: v.eligibility for k, v in evaluate_all(gates).items()}
    dv_by_product = load_design_variables(RESULTS_OPT / args.opt_run)

    pids = [p.strip() for p in args.products.split(",") if p.strip()] or list(products)
    sids = [s.strip() for s in args.strategies.split(",") if s.strip()] or [
        d.id.value for d in registry.designs
    ]
    names = [n.strip() for n in args.inputs.split(",") if n.strip()]
    unknown = [n for n in names if n not in ALL_INPUTS]
    if unknown:
        raise SystemExit(f"unknown inputs: {unknown}")

    rid = args.run_id or make_run_id()
    out = RESULTS_DS / rid
    out.mkdir(parents=True, exist_ok=True)
    seed = int(cfg["master_seed"])
    warm_up = int(cfg["warm_up_days"])
    settings_for = lambda pid: SimSettings(  # noqa: E731
        horizon_days=warm_up + round(args.horizon_years * DAYS_PER_YEAR),
        warm_up_days=warm_up,
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=tau,
        recovery_window_days=th.recovery_window_days,
        record_events=False,
        shortage_listed_at_t0=bool(listed.get(pid, False)),
    )

    def designs_for(pid: str) -> list[Any]:
        ds = []
        for d in registry.designs:
            if d.id.value not in sids:
                continue
            dd = d.model_copy(deep=True)
            dv = dv_by_product.get(pid, {}).get(d.id.value)
            if dv:
                dd.design_variables.update(dv)
            ds.append(dd)
        return ds

    thresholds: list[dict[str, Any]] = []
    dom_rows: list[dict[str, Any]] = []
    reversal: dict[str, Any] = {}
    for pid in pids:
        product = products[pid]
        settings = settings_for(pid)
        ds = designs_for(pid)
        pts = evaluate(
            ds,
            product,
            glob,
            settings,
            seed=seed,
            runs=list(range(args.runs)),
            tau=tau,
            q=q,
            eligibility=elig_by_id,
        )
        for r in dominance(pts, cost_tolerance=0.0):
            dom_rows.append(
                {"product_id": pid, **asdict(r), "dominated_by": ";".join(r.dominated_by)}
            )
        print(f"[{time.time() - t0:.0f}s] {pid}: dominance over {len(pts)} strategies")
        for d in ds:
            for name in names:
                t = threshold(
                    d,
                    product,
                    glob,
                    settings,
                    input_name=name,
                    seed=seed,
                    runs=list(range(args.threshold_runs)),
                    tau=tau,
                    q=q,
                    steps=args.steps,
                    eligibility=elig_by_id,
                )
                row = asdict(t)
                row["bracket_low"] = t.bracket[0] if t.bracket else None
                row["bracket_high"] = t.bracket[1] if t.bracket else None
                row.pop("bracket")
                row["evaluations"] = json.dumps(row["evaluations"])
                thresholds.append(row)
            print(f"[{time.time() - t0:.0f}s] {pid} {d.id.value}: {len(names)} thresholds")
        if not args.skip_reversal:
            from telo_feasibility.design_space_analysis import _range

            lo_u, b_u, hi_u = _range(product, glob, "capacity_utilization")
            lo_c, b_c, hi_c = _range(product, glob, "common_cause_dependence")
            lo_f, b_f, hi_f = _range(product, glob, "fixed_qa_labor_per_node")
            reversal[pid] = reversal_map(
                ds,
                product,
                glob,
                settings,
                axes={
                    "capacity_utilization": [lo_u, b_u, hi_u],
                    "common_cause_dependence": [lo_c, b_c, hi_c],
                    "fixed_qa_labor_per_node": [lo_f, b_f, hi_f],
                },
                seed=seed,
                runs=list(range(max(args.runs // 4, 2))),
                tau=tau,
                q=q,
                eligibility=elig_by_id,
            )
            print(
                f"[{time.time() - t0:.0f}s] {pid}: reversal map {len(reversal[pid]['cells'])} cells"
            )

    # --- labelled contract scenario: take_or_pay_fraction (MD-24, never optimized) --------
    top_rows: list[dict[str, Any]] = []
    top_levels = [float(x) for x in args.take_or_pay.split(",") if x.strip()]
    if top_levels:
        for pid in pids:
            product = products[pid]
            settings = settings_for(pid)
            carriers = [d for d in designs_for(pid) if "take_or_pay_fraction" in d.design_variables]
            for d in carriers:
                variants = []
                for lvl in top_levels:
                    v = d.model_copy(deep=True)
                    v.design_variables["take_or_pay_fraction"] = lvl
                    variants.append((lvl, v))
                for lvl, v in variants:
                    pt = evaluate(
                        [v],
                        product,
                        glob,
                        settings,
                        seed=seed,
                        runs=list(range(args.threshold_runs)),
                        tau=tau,
                        q=q,
                        eligibility=elig_by_id,
                    )[0]
                    top_rows.append(
                        {
                            "product_id": pid,
                            "strategy_id": d.id.value,
                            "take_or_pay_fraction": lvl,
                            "mean_fill": pt.mean_fill,
                            "p_meet": pt.p_meet,
                            "mean_annual_cost_usd": pt.mean_cost,
                            "mean_cost_per_unit_usd": pt.mean_cost_per_unit,
                            "n_runs": pt.n_runs,
                            "note": (
                                "labelled contract scenario, not an optimization target: "
                                "take_or_pay_fraction has no service channel (MD-24)"
                            ),
                        }
                    )
                print(
                    f"[{time.time() - t0:.0f}s] {pid} {d.id.value}: "
                    f"{len(top_levels)} take-or-pay contract scenarios"
                )
        if top_rows:
            with (out / "contract_scenarios.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(top_rows[0].keys()))
                w.writeheader()
                w.writerows(top_rows)

    with (out / "thresholds.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(thresholds[0].keys()))
        w.writeheader()
        w.writerows(thresholds)
    with (out / "dominance.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(dom_rows[0].keys()))
        w.writeheader()
        w.writerows(dom_rows)
    if reversal:
        write_json(reversal, out / "reversal.json")
    meta = {
        "run_id": rid,
        "tau": tau,
        "q": q,
        "products": pids,
        "strategies": sids,
        "inputs": names,
        "runs": args.runs,
        "threshold_runs": args.threshold_runs,
        "bisection_steps": args.steps,
        "horizon_years": args.horizon_years,
        "master_seed": seed,
        "designs_from": args.opt_run,
        "take_or_pay_scenarios": top_levels,
        "eligibility": {k: v.value for k, v in elig_by_id.items()},
        "wall_time_s": round(time.time() - t0, 1),
        "banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS",
    }
    write_json(
        {
            "meta": meta,
            "n_thresholds": len(thresholds),
            "n_dominance": len(dom_rows),
            "n_contract_scenarios": len(top_rows),
        },
        out / "summary.json",
    )
    manifest = build_run_manifest(
        rid,
        protocol=protocol,
        config_objects={
            "design_space_analysis": meta,
            "global": glob.model_dump(mode="json"),
            "strategies": [d.model_dump(mode="json") for d in registry.designs],
            "gates": gates.model_dump(mode="json"),
        },
        master_seed=seed,
        n_runs=args.runs,
        illustrative=True,
        gate_outcomes={
            k.value: {g: s.value for g, s in v.gate_statuses.items()}
            for k, v in evaluate_all(gates).items()
        },
        notes=json.dumps({"kind": "design_space_analysis", "results_dir": str(out)}),
    )
    write_manifest(manifest)
    print(f"results -> {out} ({time.time() - t0:.0f}s)")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
