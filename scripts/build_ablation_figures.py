"""Figures for the Phase A failure decomposition from one ablation run.

Usage: uv run python scripts/build_ablation_figures.py --run abl_20260902_phaseA
Writes results/figures/ablation_<run>_*.png with the metadata figures.save_figure requires.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from telo_feasibility.ablation import FACTORS, RESULTS_ABL
from telo_feasibility.figures import FigureMeta, attribution_bars, config_heatmap
from telo_feasibility.provenance import PACKAGE_ROOT

FIGS = PACKAGE_ROOT / "results" / "figures"
SOURCE = "results/ablation/<run>/summary.json and attribution.csv; all inputs tier 5 illustrative"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="abl_20260902_phaseA")
    args = ap.parse_args()
    run_dir = RESULTS_ABL / args.run
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    meta = summary["meta"]
    by_key = summary["by_key"]
    rows = list(csv.DictReader((run_dir / "attribution.csv").open(encoding="utf-8")))
    products = meta["products"]
    strategies = sorted({k.split("|")[2] for k in by_key}, key=lambda s: int(s[1:]))
    configs = [c["id"] for c in meta["configs"]]
    written: list[Path] = []
    source = SOURCE.replace("<run>", args.run)
    for pid in products:
        for sid in strategies:
            sub = [r for r in rows if r["product_id"] == pid and r["strategy_id"] == sid]
            if not sub:
                continue
            for metric, unit in (("fill_rate", "fraction"), ("p_meet", "probability")):
                bars = [
                    (
                        f"{r['factor']} ({FACTORS[r['factor']].family})",
                        float(r[f"loo_delta_{metric}"]),
                        float(r[f"addin_delta_{metric}"]),
                    )
                    for r in sub
                    if r[f"loo_delta_{metric}"] not in ("nan", "")
                ]
                base = by_key.get(f"base|{pid}|{sid}", {})
                base_v = (
                    base.get(metric, {}).get("mean")
                    if metric == "fill_rate"
                    else base.get("p_meet")
                )
                written.append(
                    attribution_bars(
                        bars,
                        FigureMeta(
                            title=f"Failure attribution, {sid}, {pid}: {metric}",
                            xlabel=f"delta {metric} [{unit}]",
                            ylabel="mechanism (family) [-]",
                            product=pid,
                            scenario=f"ablation {args.run}; base {metric} = {base_v}",
                            manifest_id=args.run,
                            source_note=source,
                            decision_caption=(
                                "Blue: how much the service metric improves when this mechanism alone is switched "
                                "off in the base world. Orange: how much it degrades when this mechanism alone is "
                                "switched on in the quiet world. Bars that disagree signal interaction with other "
                                "mechanisms. Model behavior under illustrative inputs, not a finding."
                            ),
                        ),
                        FIGS / f"ablation_{args.run}_{pid}_{sid}_{metric}.png",
                    )
                )
        # heatmap of mean fill and p_meet over configs x strategies
        for metric, vmin, vmax in (("fill_rate", 0.5, 1.0), ("p_meet", 0.0, 1.0)):
            grid: list[list[float]] = []
            labels: list[str] = []
            for cid in configs:
                vals = []
                for sid in strategies:
                    e = by_key.get(f"{cid}|{pid}|{sid}")
                    if e is None:
                        vals.append(float("nan"))
                    else:
                        vals.append(
                            float(e[metric]["mean"])
                            if metric == "fill_rate"
                            else float(e["p_meet"])
                        )
                grid.append(vals)
                labels.append(cid)
            written.append(
                config_heatmap(
                    grid,
                    labels,
                    strategies,
                    FigureMeta(
                        title=f"{metric} by ablation configuration and strategy, {pid}",
                        xlabel="strategy [-]",
                        ylabel="configuration [-]",
                        product=pid,
                        scenario=f"ablation {args.run}; tau = {meta['tau']}, q = {meta['q']}",
                        manifest_id=args.run,
                        source_note=source,
                        decision_caption=(
                            "Rows: base, each mechanism switched off (loo), the quiet world, each mechanism "
                            "switched on alone (addin), and search-bound extensions. A row that lifts a column "
                            "to the target names the mechanism that binds for that strategy. Illustrative."
                        ),
                    ),
                    FIGS / f"ablation_{args.run}_{pid}_heatmap_{metric}.png",
                    vmin=vmin,
                    vmax=vmax,
                )
            )
    print(f"{len(written)} figures -> {FIGS}")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
