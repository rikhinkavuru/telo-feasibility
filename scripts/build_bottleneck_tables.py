"""Markdown tables for the Phase A bottleneck decomposition, generated from one ablation run.

Usage: uv run python scripts/build_bottleneck_tables.py --run abl_20260902_phaseA [--pairs-run abl_x]
Prints markdown to stdout (the decomposition document embeds it verbatim so every number
traces to results/ablation/<run>/{summary.json,attribution.csv}).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from typing import Any

from telo_feasibility.ablation import RESULTS_ABL


def _f(v: float | None, nd: int = 3) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"{v:.{nd}f}"


def _mean(by_key: dict[str, Any], key: str, metric: str) -> float:
    e = by_key.get(key)
    if e is None:
        return float("nan")
    v = e[metric]
    return float(v["mean"]) if isinstance(v, dict) else float(v)


def ladder_table(
    by_key: dict[str, Any],
    configs: list[str],
    products: list[str],
    strategies: list[str],
    metric: str,
    label: str,
) -> str:
    lines = [
        "| configuration | "
        + " | ".join(f"{p.split('_')[0]} {s}" for p in products for s in strategies)
        + " |",
        "|---|" + "---|" * (len(products) * len(strategies)),
    ]
    for cid in configs:
        cells = [
            _f(_mean(by_key, f"{cid}|{p}|{s}", metric), 3 if metric != "p_meet" else 2)
            for p in products
            for s in strategies
        ]
        lines.append(f"| {cid} | " + " | ".join(cells) + " |")
    return f"**{label}**\n\n" + "\n".join(lines)


def attribution_table(rows: list[dict[str, str]], product: str, strategy: str) -> str:
    sub = [r for r in rows if r["product_id"] == product and r["strategy_id"] == strategy]
    sub.sort(
        key=lambda r: (
            -max(
                abs(float(r["loo_delta_fill_rate"])),
                abs(float(r["addin_delta_fill_rate"]))
                if r["addin_delta_fill_rate"] != "nan"
                else 0.0,
            )
        )
    )
    lines = [
        "| mechanism | family | kind | loo delta fill | addin delta fill | loo delta P(meet) | addin delta P(meet) | loo delta shortage d/yr | loo delta cost USD/yr |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in sub:
        lines.append(
            f"| {r['factor']} | {r['family']} | {r['kind']} | {_f(float(r['loo_delta_fill_rate']))} | {_f(float(r['addin_delta_fill_rate']))} | {_f(float(r['loo_delta_p_meet']), 2)} | {_f(float(r['addin_delta_p_meet']), 2)} | {_f(float(r['loo_delta_shortage_days_per_year']), 1)} | {_f(float(r['loo_delta_annual_total_cost']), 0)} |"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="abl_20260902_phaseA")
    ap.add_argument("--pairs-run", default="")
    args = ap.parse_args()
    run_dir = RESULTS_ABL / args.run
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    meta, by_key = summary["meta"], summary["by_key"]
    rows = list(csv.DictReader((run_dir / "attribution.csv").open(encoding="utf-8")))
    products = list(meta["products"])
    strategies = sorted({k.split("|")[2] for k in by_key}, key=lambda s: int(s[1:]))
    configs = [c["id"] for c in meta["configs"]]
    out: list[str] = []
    util = ", ".join(f"{p} {v:.3f}" for p, v in meta["status_quo_utilization"].items())
    out.append(
        f"Run `{args.run}`: {meta['n_runs']} common-random-number runs per configuration, "
        f"master seed {meta['master_seed']}, horizon {meta['horizon_years']} y after "
        f"{meta['warm_up_days']} d warm-up, tau = {meta['tau']}, q = {meta['q']}, designs = "
        f"{meta['designs']}. Status-quo utilization (demand / effective saleable capacity of the "
        f"S0 plant): {util}. {meta['banner']}\n"
    )
    out.append(
        ladder_table(
            by_key,
            configs,
            products,
            strategies,
            "fill_rate",
            "Mean fill rate by configuration (fraction)",
        )
    )
    out.append("")
    out.append(
        ladder_table(
            by_key,
            configs,
            products,
            strategies,
            "p_meet",
            f"P(fill >= {meta['tau']}) by configuration",
        )
    )
    out.append("")
    out.append(
        ladder_table(
            by_key,
            configs,
            products,
            strategies,
            "shortage_days_per_year",
            "Shortage days per year by configuration",
        )
    )
    out.append("")
    out.append(
        ladder_table(
            by_key,
            ["base", "quiet_all"],
            products,
            strategies,
            "capacity_utilization",
            "Capacity utilization (served / saleable capacity over the measured horizon)",
        )
    )
    out.append("")
    for p in products:
        for s in strategies:
            base = by_key.get(f"base|{p}|{s}", {})
            quiet = by_key.get(f"quiet_all|{p}|{s}", {})
            out.append(
                f"**Attribution, {p}, {s}** (base fill {_f(_mean(by_key, f'base|{p}|{s}', 'fill_rate'))}, P(meet) {_f(base.get('p_meet'), 2)}; quiet fill {_f(_mean(by_key, f'quiet_all|{p}|{s}', 'fill_rate'))}, P(meet) {_f(quiet.get('p_meet'), 2)})\n"
            )
            out.append(attribution_table(rows, p, s))
            out.append("")
    if args.pairs_run:
        pr = RESULTS_ABL / args.pairs_run
        ps = json.loads((pr / "summary.json").read_text(encoding="utf-8"))
        pcfg = [c["id"] for c in ps["meta"]["configs"]]
        out.append(f"**Interaction study `{args.pairs_run}`: mean fill rate**\n")
        out.append(
            ladder_table(
                ps["by_key"],
                pcfg,
                products,
                strategies,
                "fill_rate",
                "Mean fill rate, factor combinations",
            )
        )
        out.append("")
        out.append(
            ladder_table(
                ps["by_key"],
                pcfg,
                products,
                strategies,
                "p_meet",
                f"P(fill >= {ps['meta']['tau']}), factor combinations",
            )
        )
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
