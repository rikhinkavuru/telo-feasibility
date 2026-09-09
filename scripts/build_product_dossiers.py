"""Build one dossier per longlist candidate from frozen snapshots; write the screen manifest."""

from __future__ import annotations

import sys

from telo_feasibility.cli import main

if __name__ == "__main__":
    sys.exit(main(["dossiers", *sys.argv[1:]]))
