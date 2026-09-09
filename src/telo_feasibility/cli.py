"""Command-line entry point: ``telo-feasibility <command>``."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .acquire import AcquireOptions, acquire, load_sources
from .configs import load_all_strategies, load_gates, load_global, load_products, load_strategies
from .deterministic import (
    PRELIMINARY_BANNER,
    Mode,
    dashboard_rows,
    reconcile_dashboard,
    reconcile_screen,
    run_screen,
)
from .product_selection import DOSSIERS
from .product_selection import run_screen as run_product_screen
from .provenance import (
    PACKAGE_ROOT,
    build_run_manifest,
    load_protocol,
    verify_protocol_hashes,
    write_manifest,
)
from .regulatory import evaluate_all
from .reporting import finished_status, status_text
from .runner import run_simulation
from .workbook import WORKBOOK_PATH, cached_dashboard_rows, cached_screen_rows


def cmd_protocol_verify(args: argparse.Namespace) -> int:
    protocol = load_protocol()
    dirs = [Path(d) for d in args.search_dir] or [
        PACKAGE_ROOT / "protocol" / "source",
        PACKAGE_ROOT / "data" / "raw_snapshots" / "workbook_scaffold" / "2026-09-01",
    ]
    checks = verify_protocol_hashes(protocol, dirs)
    bad = 0
    print(f"protocol {protocol.version} ({protocol.protocol.status})")
    for c in checks:
        state = "OK" if c.ok else ("MISSING" if c.found_path is None else "HASH MISMATCH")
        print(f"  {c.document_id:<20} {state:<14} {c.found_path or c.filename}")
        bad += 0 if c.ok else 1
    return 1 if bad else 0


def cmd_status(args: argparse.Namespace) -> int:
    tests = finished_status()
    if args.json:
        print(json.dumps([asdict(t) for t in tests], indent=2))
    else:
        print(status_text(tests))
    return 0


def _write_rows(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def cmd_deterministic(args: argparse.Namespace) -> int:
    protocol = load_protocol()
    products = load_products()
    # Phase D requires every strategy through the deterministic screen, so the corrected mode
    # runs the full registry S0-S19. The workbook replica has no arithmetic for a declared
    # topology (`screen_row` raises), so it keeps the frozen eight, which is also what
    # reconciliation compares against. `cmd_reconcile` below stays on the frozen eight too.
    frozen_only = load_strategies()
    strategies = load_all_strategies()
    glob = load_global()
    gates = load_gates()
    elig = evaluate_all(gates)
    out = Path(args.out)
    modes: list[Mode] = ["workbook_replica", "corrected"] if args.mode == "both" else [args.mode]
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"det_{stamp}"
    illustrative = False
    for mode in modes:
        rows = run_screen(
            products, frozen_only if mode == "workbook_replica" else strategies, glob, mode
        )
        illustrative = illustrative or any(r.illustrative for r in rows)
        dash = dashboard_rows(
            rows,
            glob,
            protocol.service_thresholds.fill_rate_mean_min,
            None if mode == "workbook_replica" else {k: v.eligibility for k, v in elig.items()},
        )
        _write_rows(out / f"screen_{mode}.csv", [r.as_dict() for r in rows])
        _write_rows(out / f"dashboard_{mode}.csv", [r.as_dict() for r in dash])
        print(f"{mode}: {len(rows)} screen rows, {len(dash)} dashboard rows -> {out}")
    manifest = build_run_manifest(
        run_id,
        protocol=protocol,
        config_objects={
            "global": glob.model_dump(mode="json"),
            "products": {k: v.parameters.model_dump(mode="json") for k, v in products.items()},
            "strategies": [d.model_dump(mode="json") for d in strategies.designs],
            "gates": gates.model_dump(mode="json"),
        },
        master_seed=None,
        n_runs=None,
        illustrative=illustrative,
        gate_outcomes={
            k.value: {g: s.value for g, s in v.gate_statuses.items()} for k, v in elig.items()
        },
        notes="deterministic screen; " + (PRELIMINARY_BANNER if illustrative else ""),
    )
    path = write_manifest(manifest)
    print(f"manifest -> {path}")
    if illustrative:
        print(PRELIMINARY_BANNER)
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    protocol = load_protocol()
    products = load_products()
    strategies = load_strategies()
    glob = load_global()
    xlsx = Path(args.xlsx)
    rows = run_screen(products, strategies, glob, "workbook_replica")
    dash = dashboard_rows(rows, glob, protocol.service_thresholds.fill_rate_mean_min, None)
    r1 = reconcile_screen(
        cached_screen_rows(xlsx), rows, abs_tol=args.abs_tol, rel_tol=args.rel_tol
    )
    r2 = reconcile_dashboard(
        cached_dashboard_rows(xlsx), dash, abs_tol=args.abs_tol, rel_tol=args.rel_tol
    )
    ok = r1.ok and r2.ok
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = {
        "workbook": str(xlsx),
        "abs_tolerance": args.abs_tol,
        "rel_tolerance": args.rel_tol,
        "screen_cells": r1.n,
        "screen_mismatches": [asdict(c) for c in r1.mismatches],
        "dashboard_cells": r2.n,
        "dashboard_mismatches": [asdict(c) for c in r2.mismatches],
        "ok": ok,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    (out / "reconciliation.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )
    print(
        f"09_Deterministic: {r1.n - len(r1.mismatches)}/{r1.n} cells match; 12_Results: {r2.n - len(r2.mismatches)}/{r2.n} cells match"
    )
    for c in (r1.mismatches + r2.mismatches)[:40]:
        print(
            f"  MISMATCH {c.sheet}!{c.column}{c.row} workbook={c.workbook_value!r} python={c.python_value!r}"
        )
    print("RECONCILED" if ok else "NOT RECONCILED")
    return 0 if ok else 1


def cmd_acquire(args: argparse.Namespace) -> int:
    registry = load_sources()
    opts = AcquireOptions(
        root=Path(args.root),
        dry_run=args.dry_run,
        override_visiting_hours=args.override_visiting_hours,
    )
    manifests = acquire(registry, args.source or None, opts)
    auto = [m for m in manifests if m.access_method == "auto"]
    human = [m for m in manifests if m.access_method == "human"]
    for m in manifests:
        tag = "AUTO " if m.access_method == "auto" else "HUMAN"
        print(f"{tag} {m.source_id:<5} {m.http_status or '-':>4} {m.size_bytes or 0:>10} {m.url}")
        if m.access_method == "human":
            print(f"      {m.notes}")
    print(
        f"{len(auto)} payloads frozen, {len(human)} human-acquisition tasks recorded under {opts.root}"
    )
    return 0


def cmd_dossiers(args: argparse.Namespace) -> int:
    manifest = run_product_screen(root=Path(args.root), out_dir=Path(args.out))
    print(manifest["banner"])
    print(f"protocol v{manifest['protocol_version']}; snapshots: {len(manifest['snapshot_ids'])}")
    for c in manifest["candidates"]:
        score = (
            "n/a"
            if c["data_partial_score"] is None
            else f"{c['data_partial_score']:.2f}/{c['data_weight_covered']:.2f}"
        )
        print(
            f"  {c['id']:<36} gates={c['hard_gate_outcome']:<9} data-score={score:<10} status={c['status']}"
        )
    print(manifest["note"])
    return 0


def cmd_simulate(args: argparse.Namespace) -> int:
    out = run_simulation(n_runs=args.runs)
    print(f"results -> {out}")
    print(PRELIMINARY_BANNER)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="telo-feasibility", description="Telo feasibility study")
    sub = p.add_subparsers(dest="command", required=True)

    pp = sub.add_parser("protocol", help="protocol operations")
    psub = pp.add_subparsers(dest="protocol_command", required=True)
    pv = psub.add_parser("verify", help="verify source-document hashes")
    pv.add_argument("--search-dir", action="append", default=[])
    pv.set_defaults(func=cmd_protocol_verify)

    ps = sub.add_parser("status", help="definition-of-finished status")
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(func=cmd_status)

    pd = sub.add_parser("deterministic", help="run the deterministic screen")
    pd.add_argument("--mode", choices=["both", "workbook_replica", "corrected"], default="both")
    pd.add_argument("--out", default=str(PACKAGE_ROOT / "results" / "deterministic"))
    pd.set_defaults(func=cmd_deterministic)

    pr = sub.add_parser("reconcile", help="reconcile the replica against the Excel workbook")
    pr.add_argument("--xlsx", default=str(WORKBOOK_PATH))
    pr.add_argument("--out", default=str(PACKAGE_ROOT / "results" / "deterministic"))
    pr.add_argument("--abs-tol", type=float, default=1e-6)
    pr.add_argument("--rel-tol", type=float, default=1e-9)
    pr.set_defaults(func=cmd_reconcile)

    pa = sub.add_parser("acquire", help="freeze official source snapshots")
    pa.add_argument(
        "--source", action="append", default=[], help="source id (repeatable); default all"
    )
    pa.add_argument("--root", default=str(PACKAGE_ROOT / "data" / "raw_snapshots"))
    pa.add_argument("--dry-run", action="store_true")
    pa.add_argument("--override-visiting-hours", default=None, metavar="REASON")
    pa.set_defaults(func=cmd_acquire)

    pdo = sub.add_parser(
        "dossiers", help="build product dossiers and the screen manifest from frozen snapshots"
    )
    pdo.add_argument("--root", default=str(PACKAGE_ROOT / "data" / "raw_snapshots"))
    pdo.add_argument("--out", default=str(DOSSIERS))
    pdo.set_defaults(func=cmd_dossiers)

    psim = sub.add_parser("simulate", help="run the paired stochastic simulation")
    psim.add_argument("--runs", type=int, default=None)
    psim.set_defaults(func=cmd_simulate)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
