"""Build reports and figures from the latest results (protocol 13.3; task section 24).

Every report opens with the banner until finished_status() is complete. Figures carry
their manifest id, product, scenario, source note, and decision caption.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from telo_feasibility.configs import load_design_space_strategies
from telo_feasibility.figures import (
    BANNER,
    FigureMeta,
    cost_reliability_frontier,
    feasibility_map,
    tornado,
)
from telo_feasibility.provenance import PACKAGE_ROOT, load_protocol
from telo_feasibility.reporting import finished_status, status_text

RESULTS = PACKAGE_ROOT / "results"
REPORTS = PACKAGE_ROOT / "reports"
FIG = RESULTS / "figures"


def latest(pattern: str) -> Path | None:
    hits = sorted(PACKAGE_ROOT.glob(pattern))
    return hits[-1] if hits else None


def main() -> int:
    protocol = load_protocol()
    tests = finished_status()
    complete = all(t.passed for t in tests)
    banner = "" if complete else BANNER
    stamp = datetime.now(UTC).isoformat()
    lines = [
        f"# Telo feasibility study: results report (auto-built {stamp})",
        "",
        f"**{banner}**" if banner else "",
        "",
        f"Protocol v{protocol.version}. Central question: {protocol.central_question.strip()}",
        "",
        "## Definition-of-finished status",
        "",
        "```",
        status_text(tests),
        "```",
        "",
    ]

    for opt in sorted(PACKAGE_ROOT.glob("results/optimization/opt_*/summary.json")):
        s = json.loads(opt.read_text(encoding="utf-8"))
        is_sens = "_tau" in s["run_id"]
        lines += [
            f"## Strategies optimized to {'a SENSITIVITY service target' if is_sens else 'the frozen service target'} (tau = {s['tau']}, q = {s['q']})",
            "",
            f"Run `{s['run_id']}`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. "
            + (
                "This run varies the threshold as a pre-registered sensitivity; it does not replace the frozen target."
                if is_sens
                else ""
            ),
            "",
            "| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |",
            "|---|---|---|---|---|---|---|---|",
        ]
        by_product: dict[str, list[dict[str, float | str | bool]]] = {}
        for key, r in s["records"].items():
            pid, sid = key.split("|")
            cost = (
                f"{r['mean_cost']:,.0f} ({r['mcse_cost']:,.0f})"
                if r["mean_cost"] is not None
                else "-"
            )
            fill = (
                f"{r['mean_fill']:.3f}"
                if r["mean_fill"] is not None
                else (
                    f"closest {r['closest_fill_if_infeasible']:.3f}"
                    if r.get("closest_fill_if_infeasible") is not None
                    else "-"
                )
            )
            cpu = f"{r['mean_cost_per_unit']:.2f}" if r["mean_cost_per_unit"] is not None else "-"
            lines.append(
                f"| {pid} | {sid} | {r['status']} | {json.dumps(r['best_design']) if r['best_design'] else '-'} | {cost} | {fill} | {r['p_meet'] if r['p_meet'] is not None else '-'} | {cpu} |"
            )
            if r["mean_cost"] is not None:
                by_product.setdefault(pid, []).append(
                    {
                        "strategy": sid,
                        "cost": r["mean_cost"],
                        "cost_err": r["mcse_cost"] or 0.0,
                        "fill": r["mean_fill"],
                        "feasible": r["status"] == "optimal",
                    }
                )
        for pid, pts in by_product.items():
            meta = FigureMeta(
                title=f"Cost-reliability frontier of optimized designs ({pid}, tau={s['tau']})",
                xlabel="mean fill rate [fraction]",
                ylabel="mean annual total cost [USD/yr]",
                product=pid,
                scenario=f"optimized to tau={s['tau']}, q={s['q']}; gates UNCERTAIN",
                manifest_id=s["run_id"],
                source_note="illustrative workbook inputs (tier 5); results/optimization",
                decision_caption="Solid markers met the service target on the full run set; hollow did not. No strategy can be preferred while regulatory gates are unresolved and inputs are illustrative.",
            )
            p = cost_reliability_frontier(pts, meta, FIG / f"frontier_{pid}_tau{s['tau']}.png")
            lines += ["", f"![frontier]({p.relative_to(PACKAGE_ROOT)})", ""]

    sim = latest("results/simulation/sim_*/summary.json")
    if sim:
        s = json.loads(sim.read_text(encoding="utf-8"))
        lines += [
            "## Paired simulation (baseline illustrative designs, not optimized)",
            "",
            f"{s['n_runs']} common-random-number runs per strategy. Paired differences vs S0 with Monte Carlo standard errors:",
            "",
            "| Product | Strategy | d cost/unit [USD] | d fill [fraction] | d shortage days [d/yr] |",
            "|---|---|---|---|---|",
        ]
        for key, v in s["paired_vs_S0"].items():
            pid, sid = key.split("|")
            c, f, d = v["cost_per_delivered_unit"], v["fill_rate"], v["shortage_days_per_year"]
            lines.append(
                f"| {pid} | {sid} | {c['mean']:+.2f} ({c['mcse']:.2f}) | {f['mean']:+.3f} ({f['mcse']:.3f}) | {d['mean']:+.1f} ({d['mcse']:.1f}) |"
            )

    sens = latest("results/sensitivity/summary.json")
    if sens:
        s = json.loads(sens.read_text(encoding="utf-8"))
        lines += [
            "",
            "## Sensitivity and value of information",
            "",
            f"Product {s['meta']['product']}; designs from optimization run {s['meta'].get('optimized_designs_run')}; {s['meta']['runs_per_scenario']} runs per scenario.",
            "",
            f"Inputs whose sweep changes the preferred strategy: {s['reversal_inputs'] or 'none'}",
            "",
            "| Input | Sobol total-order index |",
            "|---|---|",
        ]
        for k, v in s["sobol_total_order"].items():
            lines.append(f"| {k} | {v:.3f} |")
        lines += [
            "",
            f"EVPI on annual cost: {s['evpi']:,.0f} USD/yr. EVPPI by input: "
            + ", ".join(f"{k} {v:,.0f}" for k, v in s["evppi"].items()),
            "",
        ]
        drm = latest("results/sensitivity/decision_reversal.json")
        ow = latest("results/sensitivity/one_way.json")
        if drm:
            d = json.loads(drm.read_text(encoding="utf-8"))["map"]
            axes = d["axes"]
            fixed = {"common_cause_dependence": axes["common_cause_dependence"][1]}
            meta = FigureMeta(
                title="Preferred strategy across utilization and release time (common-cause rate at base)",
                xlabel="annual demand [units/yr] (utilization at fixed capacity)",
                ylabel="sterility incubation [days] (release critical path)",
                product=s["meta"]["product"],
                scenario="optimized designs; gates UNCERTAIN",
                manifest_id=s["meta"]["generated_at"],
                source_note="results/sensitivity/decision_reversal.json; tier-5 inputs",
                decision_caption="Cells show the minimum-cost strategy meeting the service target; 'None' means no strategy met it. Read as a map of conditions, not a verdict.",
            )
            p = feasibility_map(
                d["cells"],
                "capacity_utilization",
                "release_time",
                fixed,
                meta,
                FIG / "feasibility_map.png",
            )
            lines += [f"![feasibility map]({p.relative_to(PACKAGE_ROOT)})", ""]
        if ow:
            o = json.loads(ow.read_text(encoding="utf-8"))["one_way"]
            base_costs = {x["strategy_id"]: x["mean_cost"] for x in o["base"]["outcomes"]}
            target = "S5" if "S5" in base_costs else next(iter(base_costs))
            rows = []
            for name, v in o["inputs"].items():
                vals = [
                    next(x["mean_cost"] for x in r["outcomes"] if x["strategy_id"] == target)
                    for r in v["rows"]
                ]
                rows.append((name, vals[0], vals[-1]))
            meta = FigureMeta(
                title=f"One-way sensitivity of {target} annual cost",
                xlabel="annual total cost [USD/yr]",
                ylabel="input [protocol 11.2 list]",
                product=s["meta"]["product"],
                scenario="low vs high of each input, others at base",
                manifest_id=s["meta"]["generated_at"],
                source_note="results/sensitivity/one_way.json; tier-5 ranges",
                decision_caption="Bar length shows how far each input alone moves the strategy's cost; reversal inputs are listed in the report text.",
            )
            p = tornado(rows, base_costs[target], meta, FIG / f"tornado_{target}.png")
            lines += [f"![tornado]({p.relative_to(PACKAGE_ROOT)})", ""]

    back = latest("results/backcasts/back_*/summary.json")
    if back:
        s = json.loads(back.read_text(encoding="utf-8"))
        lines += [
            "## Backcasts",
            "",
            "| Episode | Observed | Simulated longest episode [d] | Consistent | Bottleneck (sim vs observed) | Mismatches |",
            "|---|---|---|---|---|---|",
        ]
        for e in s["episodes"]:
            if e.get("status") == "not_run":
                lines.append(f"| {e['episode_id']} | not documented | - | - | - | {e['reason']} |")
                continue
            obs = (
                f">= {e['observed_duration_days_min']:.0f} d, ongoing"
                if e["observed_ongoing"]
                else f"{e['observed_duration_days_min']} d"
            )
            lines.append(
                f"| {e['episode_id']} | {obs} | {e['simulated_longest_episode_days']:.0f} | {e['consistent_duration']} | {e['binding_bottleneck_simulated']} vs {e['binding_bottleneck_observed']} | {'; '.join(e['mismatches']) or 'none'} |"
            )
        lines.append("")

    ds_designs = load_design_space_strategies().designs
    if ds_designs:
        lines += [
            "## Design-space strategies (S8+)",
            "",
            "Added by the 2026-09 design-space assignment. S0-S7 are unchanged and are guarded "
            "by `tests/regression/test_frozen_strategies.py`. Gate status is UNCERTAIN for every "
            "strategy, so none can receive a favorable decision class.",
            "",
            "| Strategy | Name | Family | Sites | Pathway | Durable | Regulatory owner | Falsification test |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for d in ds_designs:
            pr = d.profile
            sites = ", ".join(sp.id for sp in (d.site_plans or []))
            lines.append(
                f"| {d.id.value} | {d.name} | {d.family or '-'} | {sites or '-'} | "
                f"{d.pathway.value} | {d.durable} | {pr.regulatory_owner if pr else '-'} | "
                f"{pr.falsification_test if pr else '-'} |"
            )
        lines.append("")

    # the decomposition run is the one with the most configurations, not the newest: the
    # supplementary runs (single factor, factorial) are narrower by construction
    abl_paths = sorted(PACKAGE_ROOT.glob("results/ablation/abl_*/summary.json"))
    abl = (
        max(
            abl_paths,
            key=lambda q: len(json.loads(q.read_text(encoding="utf-8"))["meta"]["configs"]),
        )
        if abl_paths
        else None
    )
    if abl:
        s_abl = json.loads(abl.read_text(encoding="utf-8"))
        meta, by_key = s_abl["meta"], s_abl["by_key"]
        lines += [
            f"## Failure decomposition by ablation (run `{meta['run_id']}`)",
            "",
            f"{meta['n_runs']} common-random-number runs per configuration; designs "
            f"{meta['designs']}; tau = {meta['tau']}, q = {meta['q']}. Status-quo utilization: "
            + ", ".join(f"{k} {v:.2f}" for k, v in meta["status_quo_utilization"].items())
            + ". A mechanism binds when switching it off alone raises the tail probability.",
            "",
            "| Product | Strategy | base fill | base P(meet) | quiet fill | mechanisms that raise P(meet) by >= 0.05 when removed |",
            "|---|---|---|---|---|---|",
        ]
        pairs = sorted({(k.split("|")[1], k.split("|")[2]) for k in by_key})
        for pid, sid in pairs:
            base = by_key.get(f"base|{pid}|{sid}")
            quiet = by_key.get(f"quiet_all|{pid}|{sid}")
            if base is None:
                continue
            binding = []
            for key, entry in by_key.items():
                cfg_id, k_pid, k_sid = key.split("|")
                if not cfg_id.startswith("loo:") or k_pid != pid or k_sid != sid:
                    continue
                if entry["p_meet"] - base["p_meet"] >= 0.05:
                    binding.append((entry["p_meet"] - base["p_meet"], cfg_id.split(":", 1)[1]))
            names = ", ".join(f"{n} (+{d:.2f})" for d, n in sorted(binding, reverse=True)) or "none"
            lines.append(
                f"| {pid} | {sid} | {base['fill_rate']['mean']:.3f} | {base['p_meet']:.2f} | "
                f"{quiet['fill_rate']['mean']:.3f} | {names} |"
                if quiet
                else f"| {pid} | {sid} | {base['fill_rate']['mean']:.3f} | {base['p_meet']:.2f} | - | {names} |"
            )
        lines.append("")
        for fig in sorted(FIG.glob(f"ablation_{meta['run_id']}_*_heatmap_p_meet.png")):
            lines += [f"![ablation heatmap]({fig.relative_to(PACKAGE_ROOT)})", ""]

        # interaction study: mechanisms switched off together, so a claim that fixing one
        # mechanism moves the bottleneck to another can be checked instead of asserted
        for pairs_path in sorted(PACKAGE_ROOT.glob("results/ablation/abl_*/summary.json")):
            s_pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
            cfg_ids = [c["id"] for c in s_pairs["meta"]["configs"]]
            if not any(c.startswith("pair:") for c in cfg_ids):
                continue
            pk = s_pairs["by_key"]
            strategies = sorted(
                {k.split("|")[2] for k in pk}, key=lambda x: int(x[1:]) if x[1:].isdigit() else 99
            )
            lines += [
                f"### Interaction study (run `{s_pairs['meta']['run_id']}`)",
                "",
                "Mechanisms switched off together. A strategy that clears the target only when two "
                "mechanisms are removed is limited by both, and one that clears with either is "
                "limited by whichever is cheaper to fix.",
                "",
                "| Configuration | Product | " + " | ".join(strategies) + " |",
                "|---|---|" + "---|" * len(strategies),
            ]
            for cid in cfg_ids:
                for pid in s_pairs["meta"]["products"]:
                    cells = []
                    for sid in strategies:
                        e = pk.get(f"{cid}|{pid}|{sid}")
                        if e is None:
                            cells.append("-")
                        else:
                            mark = "*" if e["feasible"] else ""
                            cells.append(f"{e['p_meet']:.2f}{mark}")
                    lines.append(
                        f"| {cid.replace('pair:', '')} | {pid} | " + " | ".join(cells) + " |"
                    )
            lines += [
                "",
                "Cells are P(fill >= tau); an asterisk marks a configuration that meets both the "
                "mean and the tail requirement.",
                "",
            ]
            break

    dsa = latest("results/design_space/ds_*/summary.json")
    if dsa:
        s_ds = json.loads(dsa.read_text(encoding="utf-8"))["meta"]
        run_dir = dsa.parent
        lines += [
            f"## Feasibility conditions and dominance (run `{s_ds['run_id']}`)",
            "",
            f"Bisection over {s_ds['bisection_steps']} steps on {s_ds['threshold_runs']} paired "
            f"runs per input; dominance on {s_ds['runs']} paired runs at tau = {s_ds['tau']}, "
            f"q = {s_ds['q']}. A condition is stated only where feasibility changes inside the "
            "input's recorded low-to-high range.",
            "",
        ]
        import csv as _csv

        dom_path = run_dir / "dominance.csv"
        if dom_path.is_file():
            rows = list(_csv.DictReader(dom_path.open(encoding="utf-8")))
            lines += [
                "| Product | Strategy | Mean cost [USD/yr] | Mean fill | P(meet) | Meets target | Dominated by |",
                "|---|---|---|---|---|---|---|",
            ]
            for r in rows:
                lines.append(
                    f"| {r['product_id']} | {r['strategy_id']} | {float(r['mean_cost']):,.0f} | "
                    f"{float(r['mean_fill']):.3f} | {float(r['p_meet']):.2f} | {r['feasible']} | "
                    f"{r['dominated_by'] or 'none (on the frontier)'} |"
                )
            lines.append("")
        thr_path = run_dir / "thresholds.csv"
        if thr_path.is_file():
            rows = [
                r
                for r in _csv.DictReader(thr_path.open(encoding="utf-8"))
                if r["direction"] in ("feasible_below", "feasible_above")
            ]
            if rows:
                lines += [
                    "| Product | Strategy | Input | Condition | Recorded range |",
                    "|---|---|---|---|---|",
                ]
                for r in rows:
                    rel = "<=" if r["direction"] == "feasible_below" else ">="
                    lines.append(
                        f"| {r['product_id']} | {r['strategy_id']} | {r['input_name']} "
                        f"({r['parameter_id']}) | feasible while {r['input_name']} {rel} "
                        f"{float(r['threshold']):,.3g} | {float(r['low']):,.3g} to {float(r['high']):,.3g} |"
                    )
                lines.append("")
        for fig in sorted(FIG.glob(f"design_space_{s_ds['run_id']}_*.png")):
            lines += [f"![design space]({fig.relative_to(PACKAGE_ROOT)})", ""]

    lines += [
        "## Limitations",
        "",
        "- Every numeric input except four release components is tier 5 (illustrative). Nothing here is a finding about Telo or any product.",
        "- All 15 regulatory gates are UNCERTAIN; no favorable decision class is possible.",
        "- No interviews or independent reviews have been completed.",
        "- The release-assurance benchmark evidence supports shift detection and abstention only.",
        "",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "rendered").mkdir(exist_ok=True)
    out = REPORTS / "rendered" / "results_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"report -> {out}")
    print(banner or "ALL DEFINITION-OF-FINISHED TESTS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
