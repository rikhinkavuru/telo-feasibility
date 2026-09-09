"""Freeze official source snapshots under data/raw_snapshots/<source>/<date>/ with manifests.

Usage:
  uv run python scripts/acquire_sources.py                 # every auto source; human sources get task manifests
  uv run python scripts/acquire_sources.py --source S01 --source S16
  uv run python scripts/acquire_sources.py --dry-run
  uv run python scripts/acquire_sources.py --override-visiting-hours "one-off daytime snapshot approved by author"
"""

from __future__ import annotations

import sys

from telo_feasibility.cli import main

if __name__ == "__main__":
    sys.exit(main(["acquire", *sys.argv[1:]]))
