"""Run the deterministic screen (both modes) and, with --reconcile, the workbook reconciliation."""

from __future__ import annotations

import sys

from telo_feasibility.cli import main

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--reconcile" in argv:
        argv = [a for a in argv if a != "--reconcile"]
        sys.exit(main(["reconcile", *argv]))
    sys.exit(main(["deterministic", *argv]))
