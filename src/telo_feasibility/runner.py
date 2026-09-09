"""Simulation runner: config -> paired runs across processes -> tidy results, summary, manifest."""

from __future__ import annotations

import csv
import json
import math
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from .configs import CONFIG_ROOT, load_all_strategies, load_gates, load_global, load_products
from .disruptions import DAYS_PER_YEAR
from .provenance import PACKAGE_ROOT, build_run_manifest, load_protocol, write_manifest
from .regulatory import evaluate_all
from .schemas import Eligibility, StrategyId
from .simulation import RunResult, SimSettings, run_paired

SIM_CONFIG_PATH = CONFIG_ROOT / "simulation.yaml"
RESULTS_SIM = PACKAGE_ROOT / "results" / "simulation"


def load_sim_config(path: Path = SIM_CONFIG_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError("simulation config must be a mapping")
    return cfg


def settings_from_config(cfg: dict[str, Any], listed: bool) -> SimSettings:
    protocol = load_protocol()
    th = protocol.service_thresholds
    return SimSettings(
        horizon_days=int(cfg["warm_up_days"]) + round(float(cfg["horizon_years"]) * DAYS_PER_YEAR),
        warm_up_days=int(cfg["warm_up_days"]),
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=th.fill_rate_mean_min,
        recovery_window_days=th.recovery_window_days,
        n_regions=int(cfg.get("n_regions", 4)),
        record_events=bool(cfg.get("record_events", False)),
        shortage_listed_at_t0=listed,
    )


def _worker(
    args: tuple[str, list[str], dict[str, Any], bool, int, list[int]],
) -> list[dict[str, Any]]:
    product_id, strategy_ids, cfg, listed, seed, runs = args
    glob = load_global()
    product = load_products()[product_id]
    strategies = load_all_strategies()
    designs = [strategies.by_id(StrategyId(s)) for s in strategy_ids]
    settings = settings_from_config(cfg, listed)
    out: list[dict[str, Any]] = []
    for r in run_paired(designs, product, glob, settings, seed, runs):
        out.append(_row(product_id, r))
    return out


def _row(product_id: str, r: RunResult) -> dict[str, Any]:
    row: dict[str, Any] = {
        "product_id": product_id,
        "strategy_id": r.strategy_id,
        "run_index": r.run_index,
    }
    row.update(r.metrics)
    row.update({f"ledger_{k}": v for k, v in asdict(r.ledger).items() if k != "notes"})
    row.update({f"fill_rate_{reg}": v["fill_rate"] for reg, v in r.regional.items()})
    row["episodes_json"] = json.dumps(r.episodes)
    row["event_digest"] = r.event_digest
    return row


def _chunks(items: list[int], n: int) -> list[list[int]]:
    n = max(n, 1)
    return [items[i::n] for i in range(n) if items[i::n]]


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Per product-strategy: mean, median, p5, p95, MCSE; paired differences vs S0 with MCSE."""
    metrics = [
        k for k in rows[0] if isinstance(rows[0][k], int | float) and k not in ("run_index",)
    ]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for r in rows:
        groups.setdefault((r["product_id"], r["strategy_id"]), []).append(r)
    summary: dict[str, Any] = {"by_strategy": {}, "paired_vs_S0": {}}
    for (pid, sid), rs in sorted(groups.items()):
        stats: dict[str, dict[str, float]] = {}
        for m in metrics:
            x = np.array([float(r[m]) for r in rs])
            x = x[np.isfinite(x)]
            if x.size == 0:
                continue
            stats[m] = {
                "mean": float(x.mean()),
                "median": float(np.median(x)),
                "p5": float(np.percentile(x, 5)),
                "p95": float(np.percentile(x, 95)),
                "mcse": float(x.std(ddof=1) / math.sqrt(x.size)) if x.size > 1 else float("nan"),
                "n": int(x.size),
            }
        summary["by_strategy"][f"{pid}|{sid}"] = stats
    for (pid, sid), rs in sorted(groups.items()):
        ref = groups.get((pid, "S0"))
        if not ref or sid == "S0":
            continue
        ref_by_run = {r["run_index"]: r for r in ref}
        diffs: dict[str, dict[str, float]] = {}
        for m in (
            "annual_total_cost",
            "cost_per_delivered_unit",
            "fill_rate",
            "shortage_days_per_year",
            "unmet_units_per_year",
        ):
            d = np.array(
                [
                    float(r[m]) - float(ref_by_run[r["run_index"]][m])
                    for r in rs
                    if r["run_index"] in ref_by_run
                ]
            )
            d = d[np.isfinite(d)]
            if d.size:
                diffs[m] = {
                    "mean": float(d.mean()),
                    "mcse": float(d.std(ddof=1) / math.sqrt(d.size))
                    if d.size > 1
                    else float("nan"),
                    "n": int(d.size),
                }
        summary["paired_vs_S0"][f"{pid}|{sid}"] = diffs
    return summary


def run_simulation(
    cfg_path: Path = SIM_CONFIG_PATH,
    n_runs: int | None = None,
    out_root: Path = RESULTS_SIM,
    strategy_ids_override: list[str] | None = None,
    product_ids_override: list[str] | None = None,
    run_id_override: str | None = None,
) -> Path:
    """Paired runs for the configured strategies, or for an explicit list.

    The overrides exist so design-space strategies (S8+) can be simulated without editing
    the frozen ``config/simulation.yaml``; the override is recorded in the run manifest.
    """
    cfg = load_sim_config(cfg_path)
    n = int(n_runs if n_runs is not None else cfg["n_runs"])
    seed = int(cfg["master_seed"])
    strategy_ids = [str(s) for s in (strategy_ids_override or cfg["strategies"])]
    if product_ids_override:
        keep = set(product_ids_override)
        cfg = {**cfg, "products": [p for p in cfg["products"] if str(p["id"]) in keep]}
        if not cfg["products"]:
            raise ValueError(f"no configured product matches {sorted(keep)}")
    workers = int(cfg.get("workers", 0)) or max((os.cpu_count() or 2) - 1, 1)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = run_id_override or f"sim_{stamp}"
    out = out_root / run_id
    out.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    tasks: list[tuple[str, list[str], dict[str, Any], bool, int, list[int]]] = []
    for p in cfg["products"]:
        for chunk in _chunks(list(range(n)), workers):
            tasks.append(
                (
                    str(p["id"]),
                    strategy_ids,
                    cfg,
                    bool(p.get("shortage_listed_at_t0", False)),
                    seed,
                    chunk,
                )
            )
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for part in ex.map(_worker, tasks):
                rows.extend(part)
    else:
        for t in tasks:
            rows.extend(_worker(t))
    rows.sort(key=lambda r: (r["product_id"], r["strategy_id"], r["run_index"]))
    with (out / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary = _summarize(rows)
    gates = load_gates()
    elig = evaluate_all(gates)
    summary["eligibility"] = {k.value: v.eligibility.value for k, v in elig.items()}
    summary["favorable_conclusion_possible"] = any(
        v.eligibility is Eligibility.ELIGIBLE for v in elig.values()
    )
    summary["banner"] = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"
    summary["n_runs"] = n
    summary["config"] = cfg
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    glob = load_global()
    products = load_products()
    illustrative = bool(glob.illustrative_ids()) or any(
        p.parameters.illustrative_ids() for p in products.values()
    )
    protocol = load_protocol()
    manifest = build_run_manifest(
        run_id,
        protocol=protocol,
        config_objects={
            "simulation": cfg,
            "global": glob.model_dump(mode="json"),
            "products": {k: v.parameters.model_dump(mode="json") for k, v in products.items()},
            "strategies": [d.model_dump(mode="json") for d in load_all_strategies().designs],
            "gates": gates.model_dump(mode="json"),
        },
        master_seed=seed,
        n_runs=n,
        illustrative=illustrative,
        gate_outcomes={
            k.value: {g: s.value for g, s in v.gate_statuses.items()} for k, v in elig.items()
        },
        notes=json.dumps(
            {
                "strategy_ids": strategy_ids,
                "products": [p["id"] for p in cfg["products"]],
                "results_dir": str(out),
            }
        ),
    )
    path = write_manifest(manifest)
    # the status checker reads strategy ids from the manifest
    data = json.loads(path.read_text(encoding="utf-8"))
    data["strategy_ids"] = strategy_ids
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out
