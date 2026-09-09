"""Backcast the documented historical episodes."""

from __future__ import annotations

from telo_feasibility.backcast import run_backcasts

if __name__ == "__main__":
    out = run_backcasts()
    print(f"results -> {out}")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
