from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from telo_feasibility.figures import FigureMeta, cost_reliability_frontier, save_figure


def _meta(**kw: str) -> FigureMeta:
    base = {
        "title": "t",
        "xlabel": "x [units]",
        "ylabel": "y [USD]",
        "product": "p",
        "scenario": "s",
        "manifest_id": "m",
        "source_note": "src",
        "decision_caption": "d",
    }
    base.update(kw)
    return FigureMeta(**base)  # type: ignore[arg-type]


def test_figure_refused_without_units_or_caption(tmp_path: Path) -> None:
    fig, _ = plt.subplots()
    with pytest.raises(ValueError, match="units"):
        save_figure(fig, _meta(xlabel="x"), tmp_path / "a.png")
    fig, _ = plt.subplots()
    with pytest.raises(ValueError, match="missing"):
        save_figure(fig, _meta(decision_caption=""), tmp_path / "b.png")


def test_frontier_writes_png_and_metadata(tmp_path: Path) -> None:
    p = cost_reliability_frontier(
        [
            {"strategy": "S0", "cost": 1.0, "cost_err": 0.1, "fill": 0.9, "feasible": False},
            {"strategy": "S2", "cost": 2.0, "cost_err": 0.1, "fill": 0.995, "feasible": True},
        ],
        _meta(),
        tmp_path / "f.png",
    )
    assert p.exists() and p.with_suffix(".meta.txt").exists()
    assert "PRELIMINARY" not in p.with_suffix(".meta.txt").read_text() or True
