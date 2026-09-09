"""Figures with the metadata the protocol requires on every plot (task section 24).

Every figure carries: descriptive title, labeled axes with units, uncertainty where
relevant, product and scenario, run manifest id, source note, and a decision caption.
Figures without all of these are refused by ``save_figure``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"


@dataclass(frozen=True)
class FigureMeta:
    title: str
    xlabel: str
    ylabel: str
    product: str
    scenario: str
    manifest_id: str
    source_note: str
    decision_caption: str
    illustrative: bool = True

    def validate(self) -> None:
        for name in (
            "title",
            "xlabel",
            "ylabel",
            "product",
            "scenario",
            "manifest_id",
            "source_note",
            "decision_caption",
        ):
            v = getattr(self, name)
            if not isinstance(v, str) or not v.strip():
                raise ValueError(f"figure metadata {name} missing")
        if "[" not in self.xlabel or "[" not in self.ylabel:
            raise ValueError(
                "axis labels must state units in square brackets, e.g. 'fill rate [fraction]'"
            )


def save_figure(fig: Figure, meta: FigureMeta, path: Path) -> Path:
    meta.validate()
    ax = fig.axes[0] if fig.axes else fig.add_subplot(111)
    ax.set_title(meta.title)
    ax.set_xlabel(meta.xlabel)
    ax.set_ylabel(meta.ylabel)
    footer = (
        f"{meta.product} | {meta.scenario} | run {meta.manifest_id} | source: {meta.source_note}"
    )
    if meta.illustrative:
        footer = BANNER + "\n" + footer
    fig.text(0.01, 0.01, footer, fontsize=7, ha="left", va="bottom")
    fig.text(
        0.01,
        -0.06,
        "Decision: " + meta.decision_caption,
        fontsize=8,
        ha="left",
        va="top",
        wrap=True,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    (path.with_suffix(".meta.txt")).write_text(
        "\n".join(
            f"{k}: {getattr(meta, k)}"
            for k in (
                "title",
                "xlabel",
                "ylabel",
                "product",
                "scenario",
                "manifest_id",
                "source_note",
                "decision_caption",
                "illustrative",
            )
        ),
        encoding="utf-8",
    )
    return path


def cost_reliability_frontier(
    points: list[dict[str, float | str | bool]], meta: FigureMeta, path: Path
) -> Path:
    """points: {strategy, cost, cost_err, fill, feasible}. Feasible points solid, infeasible hollow."""
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for p in points:
        marker = "o" if p.get("feasible") else "x"
        ax.errorbar(
            [float(p["fill"])],
            [float(p["cost"])],
            yerr=[float(p.get("cost_err", 0.0))],
            fmt=marker,
            capsize=3,
            label=str(p["strategy"]),
        )
        ax.annotate(
            str(p["strategy"]),
            (float(p["fill"]), float(p["cost"])),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=8,
        )
    ax.grid(True, alpha=0.3)
    return save_figure(fig, meta, path)


def feasibility_map(
    cells: list[dict[str, Any]],
    x_name: str,
    y_name: str,
    fixed: dict[str, float],
    meta: FigureMeta,
    path: Path,
) -> Path:
    """Categorical map of the preferred strategy over two axes; None = no feasible strategy."""
    xs = sorted({float(c["inputs"][x_name]) for c in cells})
    ys = sorted({float(c["inputs"][y_name]) for c in cells})
    labels = sorted({str(c["preferred"]) for c in cells})
    idx = {lab: i for i, lab in enumerate(labels)}
    grid = [[float("nan")] * len(xs) for _ in ys]
    for c in cells:
        if all(abs(float(c["inputs"][k]) - v) < 1e-9 for k, v in fixed.items()):
            i = ys.index(float(c["inputs"][y_name]))
            j = xs.index(float(c["inputs"][x_name]))
            grid[i][j] = idx[str(c["preferred"])]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    im = ax.imshow(
        grid,
        origin="lower",
        aspect="auto",
        extent=(min(xs), max(xs), min(ys), max(ys)),
        interpolation="nearest",
    )
    cbar = fig.colorbar(im, ax=ax, ticks=list(range(len(labels))))
    cbar.ax.set_yticklabels(labels)
    return save_figure(fig, meta, path)


def tornado(
    rows: list[tuple[str, float, float]], base: float, meta: FigureMeta, path: Path
) -> Path:
    """rows: (input, value_at_low, value_at_high) of a response; drawn around base."""
    rows = sorted(rows, key=lambda r: abs(r[2] - r[1]), reverse=True)
    fig, ax = plt.subplots(figsize=(6.4, 0.35 * len(rows) + 1.5))
    for i, (_name, lo, hi) in enumerate(rows):
        ax.barh(i, lo - base, left=base, color="tab:blue", alpha=0.7)
        ax.barh(i, hi - base, left=base, color="tab:orange", alpha=0.7)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.axvline(base, color="k", lw=0.8)
    return save_figure(fig, meta, path)


def attribution_bars(rows: list[tuple[str, float, float]], meta: FigureMeta, path: Path) -> Path:
    """Paired horizontal bars per factor: leave-one-out delta (blue) and add-one-in delta (orange).

    rows: (factor, loo_delta, addin_delta) in the response's units; sorted by the larger
    absolute delta so the binding mechanisms sit at the top.
    """
    rows = sorted(rows, key=lambda r: max(abs(r[1]), abs(r[2])), reverse=True)
    fig, ax = plt.subplots(figsize=(7.0, 0.32 * len(rows) + 1.6))
    y = list(range(len(rows)))
    ax.barh(
        [v + 0.2 for v in y],
        [r[1] for r in rows],
        height=0.4,
        color="tab:blue",
        alpha=0.8,
        label="leave-one-out (base minus mechanism)",
    )
    ax.barh(
        [v - 0.2 for v in y],
        [r[2] for r in rows],
        height=0.4,
        color="tab:orange",
        alpha=0.8,
        label="add-one-in (quiet plus mechanism)",
    )
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.invert_yaxis()
    ax.axvline(0.0, color="k", lw=0.8)
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(True, axis="x", alpha=0.3)
    return save_figure(fig, meta, path)


def config_heatmap(
    values: list[list[float]],
    row_labels: list[str],
    col_labels: list[str],
    meta: FigureMeta,
    path: Path,
    vmin: float | None = None,
    vmax: float | None = None,
    fmt: str = "{:.2f}",
) -> Path:
    """Annotated matrix (rows = configurations, columns = strategies) of one response."""
    fig, ax = plt.subplots(figsize=(0.55 * len(col_labels) + 3.0, 0.28 * len(row_labels) + 1.8))
    im = ax.imshow(values, aspect="auto", cmap="viridis", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, fontsize=8)
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=7)
    for i, row in enumerate(values):
        for j, v in enumerate(row):
            ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=6, color="w")
    fig.colorbar(im, ax=ax, fraction=0.03)
    return save_figure(fig, meta, path)
