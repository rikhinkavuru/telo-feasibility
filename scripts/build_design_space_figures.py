"""Feasibility-region, dominance, and reversal figures from one design-space analysis run.

Usage: uv run python scripts/build_design_space_figures.py --run ds_2026...
Writes results/figures/design_space_<run>_*.png with the metadata figures.save_figure requires.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from telo_feasibility.design_space_analysis import RESULTS_DS
from telo_feasibility.figures import FigureMeta, config_heatmap, save_figure
from telo_feasibility.provenance import PACKAGE_ROOT

FIGS = PACKAGE_ROOT / "results" / "figures"


def _sid_key(s: str) -> int:
    return int(s[1:]) if s[1:].isdigit() else 999


def feasibility_region_figure(
    rows: list[dict[str, Any]], product: str, meta: FigureMeta, path: Path
) -> Path:
    """One row per strategy, one marker per input: where the feasibility boundary sits.

    Each input's recorded low-to-high range is drawn as a light bar in normalized units and
    the crossing is marked, so a reader sees both the condition and how much of the range
    it leaves. Inputs with no crossing inside the range are drawn as an open bar.
    """
    inputs = sorted({r["input_name"] for r in rows})
    strategies = sorted({r["strategy_id"] for r in rows}, key=_sid_key)
    # room for rotated input names below the axes so they do not collide with the footer
    label_room = 0.06 * max((len(n) for n in inputs), default=10)
    height = 0.4 * len(strategies) + 2.2 + label_room
    fig, ax = plt.subplots(figsize=(1.0 * len(inputs) + 3.0, height))
    fig.subplots_adjust(bottom=min(0.15 + label_room / height, 0.6), top=0.9)
    for i, sid in enumerate(strategies):
        for j, name in enumerate(inputs):
            r = next((x for x in rows if x["strategy_id"] == sid and x["input_name"] == name), None)
            if r is None:
                continue
            lo, hi = float(r["low"]), float(r["high"])
            span = hi - lo if hi > lo else 1.0
            ax.plot([j - 0.4, j + 0.4], [i, i], color="0.85", lw=6, solid_capstyle="butt")
            direction = r["direction"]
            if direction in ("feasible_below", "feasible_above") and r["threshold"] not in (
                "",
                None,
            ):
                x = (float(r["threshold"]) - lo) / span
                ax.plot([j - 0.4 + 0.8 * x], [i], marker="|", ms=14, color="tab:blue", mew=2)
                left = j - 0.4 if direction == "feasible_below" else j - 0.4 + 0.8 * x
                width = 0.8 * x if direction == "feasible_below" else 0.8 * (1 - x)
                ax.plot(
                    [left, left + width], [i, i], color="tab:green", lw=6, solid_capstyle="butt"
                )
            elif direction == "feasible_everywhere":
                ax.plot([j - 0.4, j + 0.4], [i, i], color="tab:green", lw=6, solid_capstyle="butt")
    ax.set_xticks(range(len(inputs)))
    ax.set_xticklabels([n.replace("_", " ") for n in inputs], rotation=40, ha="right", fontsize=7)
    ax.set_yticks(range(len(strategies)))
    ax.set_yticklabels(strategies, fontsize=8)
    ax.set_xlim(-0.6, len(inputs) - 0.4)
    ax.set_ylim(-0.7, len(strategies) - 0.3)
    ax.grid(True, axis="x", alpha=0.2)
    return save_figure(fig, meta, path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    run_dir = RESULTS_DS / args.run
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))["meta"]
    thresholds = list(csv.DictReader((run_dir / "thresholds.csv").open(encoding="utf-8")))
    dom = list(csv.DictReader((run_dir / "dominance.csv").open(encoding="utf-8")))
    source = f"results/design_space/{args.run}/; all inputs tier 5 illustrative"
    written: list[Path] = []
    for pid in summary["products"]:
        rows = [r for r in thresholds if r["product_id"] == pid]
        if rows:
            written.append(
                feasibility_region_figure(
                    rows,
                    pid,
                    FigureMeta(
                        title=f"Feasibility conditions by strategy and input, {pid}",
                        xlabel="input, normalized over its recorded low-to-high range [-]",
                        ylabel="strategy [-]",
                        product=pid,
                        scenario=f"tau = {summary['tau']}, q = {summary['q']}; bisection {summary['bisection_steps']} steps on {summary['threshold_runs']} paired runs",
                        manifest_id=args.run,
                        source_note=source,
                        decision_caption=(
                            "Green: the part of each input's recorded range where the strategy meets "
                            "the service target. The tick marks the crossing. Grey only: no crossing "
                            "inside the range, so the condition is not binding there. Illustrative."
                        ),
                    ),
                    FIGS / f"design_space_{args.run}_{pid}_feasibility.png",
                )
            )
        drows = [r for r in dom if r["product_id"] == pid]
        if drows:
            fig, ax = plt.subplots(figsize=(6.8, 4.4))
            for r in drows:
                feasible = r["feasible"] == "True"
                ax.errorbar(
                    [float(r["mean_fill"])],
                    [float(r["mean_cost"])],
                    fmt="o" if feasible else "x",
                    color="tab:green" if r["on_frontier"] == "True" else "tab:red",
                    capsize=3,
                )
                ax.annotate(
                    r["strategy_id"],
                    (float(r["mean_fill"]), float(r["mean_cost"])),
                    textcoords="offset points",
                    xytext=(4, 4),
                    fontsize=8,
                )
            ax.axvline(float(summary["tau"]), color="k", lw=0.8, ls="--")
            ax.grid(True, alpha=0.3)
            written.append(
                save_figure(
                    fig,
                    FigureMeta(
                        title=f"Cost against service, dominance marked, {pid}",
                        xlabel="mean fill rate [fraction]",
                        ylabel="mean annual total cost [USD/yr]",
                        product=pid,
                        scenario=f"tau = {summary['tau']} (dashed), q = {summary['q']}, {summary['runs']} paired runs",
                        manifest_id=args.run,
                        source_note=source,
                        decision_caption=(
                            "Green markers sit on the cost-service frontier; red markers are dominated "
                            "by at least one other strategy. Circles meet the tail requirement, crosses "
                            "do not. Illustrative inputs; not a recommendation."
                        ),
                    ),
                    FIGS / f"design_space_{args.run}_{pid}_dominance.png",
                )
            )
    rev_path = run_dir / "reversal.json"
    if rev_path.is_file():
        rev = json.loads(rev_path.read_text(encoding="utf-8"))
        for pid, m in rev.items():
            names = list(m["axes"])
            x_name, y_name = names[0], names[1]
            fixed_name = names[2] if len(names) > 2 else None
            for fixed_val in m["axes"].get(fixed_name, [None]) if fixed_name else [None]:
                cells = [
                    c
                    for c in m["cells"]
                    if fixed_name is None
                    or math.isclose(float(c["inputs"][fixed_name]), float(fixed_val))
                ]
                xs = sorted({float(c["inputs"][x_name]) for c in cells})
                ys = sorted({float(c["inputs"][y_name]) for c in cells})
                labels = sorted(
                    {str(c["preferred"]) for c in cells},
                    key=lambda s: _sid_key(s) if s != "None" else -1,
                )
                idx = {lab: i for i, lab in enumerate(labels)}
                grid = [[float("nan")] * len(xs) for _ in ys]
                for c in cells:
                    grid[ys.index(float(c["inputs"][y_name]))][
                        xs.index(float(c["inputs"][x_name]))
                    ] = idx[str(c["preferred"])]
                tag = f"_{fixed_name}{fixed_val:g}" if fixed_name else ""
                written.append(
                    config_heatmap(
                        grid,
                        [f"{y_name}={v:g}" for v in ys],
                        [f"{v:g}" for v in xs],
                        FigureMeta(
                            title=f"Preferred strategy over {x_name} and {y_name}, {pid}",
                            xlabel=f"{x_name} [input units]",
                            ylabel=f"{y_name} [input units]",
                            product=pid,
                            scenario=f"{fixed_name} = {fixed_val:g}"
                            if fixed_name
                            else "two-axis map",
                            manifest_id=args.run,
                            source_note=source + f"; index order {labels}",
                            decision_caption=(
                                "Cell value indexes the cheapest strategy that meets the service target; "
                                f"the index order is {labels}, where None means no strategy qualifies. "
                                "A change of index across the map is a decision reversal. Illustrative."
                            ),
                        ),
                        FIGS / f"design_space_{args.run}_{pid}_reversal{tag}.png",
                        fmt="{:.0f}",
                    )
                )
    print(f"{len(written)} figures -> {FIGS}")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
