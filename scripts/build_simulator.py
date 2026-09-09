"""Inline the precomputed response surface into the interactive simulator page.

The page ships as one self-contained HTML file so it runs from a file, a static host, or a
published artifact with no network call and no server. Run
scripts/build_simulator_surface.py first.

Usage: .venv/bin/python scripts/build_simulator.py
Writes reports/simulator/index.html.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "reports" / "simulator" / "template.html"
SURFACE = ROOT / "results" / "design_space" / "simulator_surface.json"
OUT = ROOT / "reports" / "simulator" / "index.html"
PLACEHOLDER = "__SURFACE_JSON__"


def main() -> int:
    if not SURFACE.exists():
        raise SystemExit(f"missing {SURFACE}; run scripts/build_simulator_surface.py first")
    surface = json.loads(SURFACE.read_text())
    template = TEMPLATE.read_text()
    if PLACEHOLDER not in template:
        raise SystemExit(f"{TEMPLATE} has no {PLACEHOLDER} placeholder")

    n_sweeps = len(surface["sweeps"])
    n_points = sum(len(g["points"]) for sw in surface["sweeps"] for g in sw["by_product"].values())
    n_str = len(surface["strategies"])
    expected = n_points * n_str
    actual = sum(
        len(p["by_strategy"])
        for sw in surface["sweeps"]
        for g in sw["by_product"].values()
        for p in g["points"]
    )
    if actual != expected:
        raise SystemExit(f"surface is ragged: {actual} strategy points, expected {expected}")

    # a script element cannot contain the closing tag sequence, in any casing
    payload = json.dumps(surface, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(template.replace(PLACEHOLDER, payload))
    kb = OUT.stat().st_size / 1024
    print(f"{OUT.relative_to(ROOT)}  {kb:.0f} kB")
    print(f"{n_sweeps} sweeps, {n_points} points, {n_str} architectures, {actual} simulated cells")
    print(
        f"runs per point {surface['meta']['runs_per_point']}, seed {surface['meta']['master_seed']}"
    )
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
