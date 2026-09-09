"""Failure decomposition by ablation (design-space assignment, Phase A).

Every named failure mechanism is a ``Factor``: a set of parameter, design-variable, or
settings overrides that switch that mechanism off. Two complementary experiments bracket
each mechanism's contribution to a strategy's shortfall against the service target:

* leave-one-out (``loo``): start from the base world and switch one mechanism off; the
  improvement is the mechanism's marginal contribution given every other mechanism;
* add-one-in (``addin``): start from the quiet world (every mechanism off) and switch one
  mechanism on; the damage is its contribution in isolation.

The two deltas bound the Shapley attribution from above and below when mechanisms
interact. Structural factors (measurement window, lost-sales rule, review policy) are run
as leave-one-out only; cost-only factors change no service metric by construction and are
reported on cost. All runs share common random numbers with the base run, so a delta of
zero means the mechanism did not bind in any run.

Nothing here is a finding about the world: inputs are illustrative and the output is
model behavior under those inputs (banner on every artifact).
"""

from __future__ import annotations

import csv
import json
import math
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from .configs import (
    ProductConfig,
    load_all_strategies,
    load_gates,
    load_global,
    load_products,
)
from .disruptions import DAYS_PER_YEAR
from .production import SiteRuntime
from .provenance import PACKAGE_ROOT, build_run_manifest, load_protocol, write_manifest
from .regulatory import evaluate_all
from .schemas import ParameterSet, StrategyDesign, StrategyId
from .sensitivity import set_base
from .simulation import RunResult, SimSettings, run_paired
from .strategies import build_strategy

RESULTS_ABL = PACKAGE_ROOT / "results" / "ablation"
BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"
STATUS_QUO_UTILIZATION_TARGET = 0.75


@dataclass(frozen=True)
class Factor:
    """One failure mechanism and the overrides that switch it off."""

    id: str
    family: str  # capacity | demand | supply | release | quality | dependence | inventory | contract | regulatory | time | cost | structure
    description: str
    kind: str  # mechanism | cost | structure
    global_overrides: dict[str, float] = field(default_factory=dict)
    product_overrides: dict[str, float] = field(default_factory=dict)
    design_overrides: dict[str, dict[str, float]] = field(default_factory=dict)  # "*" or S-id
    settings_overrides: dict[str, Any] = field(default_factory=dict)
    special: str | None = None
    loo_only: bool = False  # not part of the quiet set; no add-one-in configuration


FACTORS: dict[str, Factor] = {
    f.id: f
    for f in (
        Factor(
            "capacity_shortfall",
            "capacity",
            "Nominal batches per site-year raised so the status-quo plant runs at "
            f"{STATUS_QUO_UTILIZATION_TARGET:.0%} utilization instead of the illustrative >100%",
            "mechanism",
            special="status_quo_utilization",
        ),
        Factor(
            "surge_headroom",
            "demand",
            "No compound demand shocks (surge headroom never needed)",
            "mechanism",
            global_overrides={"demand_shocks_per_year": 0.0},
        ),
        Factor(
            "inventory_timing",
            "inventory",
            "Regional stock reviewed daily to a base-stock target instead of the frozen "
            "reorder-at-lane-time-plus-one-day rule",
            "mechanism",
            design_overrides={"*": {"region_base_stock": 1.0}},
        ),
        Factor(
            "api_lead_time",
            "supply",
            "API procurement lead time cut from the illustrative value to 7 days. Under the "
            "frozen material policy the buffer is (target + lead) days and raw-material stock "
            "carries no cost, so a shorter lead also shrinks the buffer: the sign is not "
            "guaranteed (model defect MD-1 in the decomposition)",
            "mechanism",
            product_overrides={"material_lead_time_days": 7.0},
        ),
        Factor(
            "component_lead_time",
            "supply",
            "Vial and stopper lead time cut to 5% of the API lead time; same buffer caveat as "
            "api_lead_time (MD-1)",
            "mechanism",
            design_overrides={"*": {"component_lead_fraction": 0.05}},
        ),
        Factor(
            "material_buffer",
            "supply",
            "Raw-material order-up-to target raised to 1000 days so no batch ever waits for "
            "API, vials, or stoppers (isolates material stockouts from supplier disruption "
            "events); leave-one-out only, since the quiet world has no stockouts to remove",
            "mechanism",
            design_overrides={"*": {"material_target_days": 1000.0}},
            loo_only=True,
        ),
        Factor(
            "release_queue",
            "release",
            "Chemical, endotoxin, environmental-monitoring, and QA review components set to zero "
            "(sterility incubation kept)",
            "mechanism",
            global_overrides={
                "assay_days": 0.0,
                "endotoxin_days": 0.0,
                "environmental_monitoring_days": 0.0,
                "qa_review_days": 0.0,
            },
        ),
        Factor(
            "sterility_delay",
            "release",
            "Sterility incubation set to zero (other release components kept)",
            "mechanism",
            global_overrides={"sterility_incubation_days": 0.0},
        ),
        Factor(
            "deviation_rejection",
            "quality",
            "No deviations, no batch rejections, no yield variance",
            "mechanism",
            global_overrides={
                "deviation_rate_per_batch": 0.0,
                "batch_rejection_rate": 0.0,
                "yield_sd": 0.0,
            },
        ),
        Factor(
            "demand_variance",
            "demand",
            "No routine demand noise or autocorrelation",
            "mechanism",
            global_overrides={"demand_cv": 0.0, "demand_autocorrelation": 0.0},
        ),
        Factor(
            "demand_covariance",
            "demand",
            "Demand shocks hit one region at a time, never all regions together",
            "mechanism",
            global_overrides={"demand_shock_all_regions_probability": 0.0},
        ),
        Factor(
            "common_cause",
            "dependence",
            "No common-cause events (shared API, vial, geography, OS, quality unit)",
            "mechanism",
            global_overrides={"common_cause_events_per_year": 0.0},
        ),
        Factor(
            "supplier_concentration",
            "supply",
            "No supplier disruptions",
            "mechanism",
            global_overrides={"supplier_disruptions_per_supplier_year": 0.0},
        ),
        Factor(
            "site_failures",
            "capacity",
            "No idiosyncratic site failures",
            "mechanism",
            global_overrides={"site_failures_per_site_year": 0.0},
        ),
        Factor(
            "contract_insufficiency",
            "contract",
            "Reserved capacity activates instantly, at full reservation, with long campaigns",
            "mechanism",
            global_overrides={"reserved_capacity_activation_days": 0.0},
            design_overrides={
                "S3": {
                    "reserved_capacity_fraction": 1.0,
                    "campaign_batches": 12.0,
                    "activation_threshold_days": 45.0,
                }
            },
        ),
        Factor(
            "regulatory_unavailability",
            "regulatory",
            "Product on the shortage list at t0 and never resolved (503B always available)",
            "mechanism",
            global_overrides={"shortage_list_resolution_rate_per_year": 0.0},
            settings_overrides={"shortage_listed_at_t0": True},
        ),
        Factor(
            "commissioning_delay",
            "time",
            "New sites and the second source exist from day 0 (no commissioning or qualification)",
            "mechanism",
            global_overrides={
                "node_commissioning_days": 0.0,
                "second_source_qualification_days": 0.0,
            },
            design_overrides={"S2": {"second_source_exists_at_t0": 1.0}},
        ),
        Factor(
            "fixed_quality_cost",
            "cost",
            "Fixed QA labor per site set to zero (cost only)",
            "cost",
            product_overrides={"fixed_qa_labor_usd_per_site_year": 0.0},
        ),
        Factor(
            "replicated_validation_cost",
            "cost",
            "One-time validation per site set to zero (cost only)",
            "cost",
            product_overrides={"validation_usd_one_time": 0.0},
        ),
        Factor(
            "capital_cost",
            "cost",
            "Capital per site set to zero (cost only)",
            "cost",
            product_overrides={"capital_usd_per_site": 0.0},
        ),
        Factor(
            "lost_sales_window",
            "structure",
            "Backorder window widened from 7 to 30 days (measurement rule for lost demand)",
            "structure",
            global_overrides={"backorder_window_days": 30.0},
        ),
        Factor(
            "horizon_10y",
            "structure",
            "Ten-year evaluation window instead of five (commissioning amortized over more years)",
            "structure",
            settings_overrides={"horizon_years": 10.0},
        ),
    )
}

MECHANISM_FACTORS: tuple[str, ...] = tuple(
    f.id for f in FACTORS.values() if f.kind == "mechanism" and not f.loo_only
)
COST_FACTORS: tuple[str, ...] = tuple(f.id for f in FACTORS.values() if f.kind == "cost")
STRUCTURE_FACTORS: tuple[str, ...] = tuple(f.id for f in FACTORS.values() if f.kind == "structure")


@dataclass(frozen=True)
class Config:
    """A named combination of factors applied on top of the base."""

    id: str
    factors: tuple[str, ...]
    design_overrides: dict[str, dict[str, float]] = field(default_factory=dict)
    role: str = "loo"  # base | loo | quiet | addin | bounds | pair


def default_configs() -> list[Config]:
    out = [Config("base", (), role="base")]
    for fid in FACTORS:
        out.append(Config(f"loo:{fid}", (fid,), role="loo"))
    out.append(Config("quiet_all", MECHANISM_FACTORS, role="quiet"))
    for fid in MECHANISM_FACTORS:
        out.append(
            Config(
                f"addin:{fid}",
                tuple(f for f in MECHANISM_FACTORS if f != fid),
                role="addin",
            )
        )
    out.append(
        Config(
            "bounds:ss365",
            (),
            design_overrides={"*": {"safety_stock_days": 365.0}},
            role="bounds",
        )
    )
    out.append(
        Config(
            "bounds:ss365+base_stock",
            ("inventory_timing",),
            design_overrides={"*": {"safety_stock_days": 365.0}},
            role="bounds",
        )
    )
    return out


def pair_configs(factor_ids: list[str]) -> list[Config]:
    """Full factorial over a short list of factors (interaction study)."""
    out: list[Config] = []
    n = len(factor_ids)
    for mask in range(1, 2**n):
        chosen = tuple(f for i, f in enumerate(factor_ids) if mask >> i & 1)
        if len(chosen) >= 2:
            out.append(Config("pair:" + "+".join(chosen), chosen, role="pair"))
    return out


def status_quo_utilization(product: ProductConfig, s0: StrategyDesign) -> float:
    """Demand divided by the status-quo plant's effective saleable capacity."""
    p = product.parameters
    cf = float(s0.design_variables.get("capacity_factor", 1.0))
    capacity = (
        p.base("batches_per_site_year_nominal")
        * cf
        * p.base("uptime_fraction")
        * p.base("yield_fraction")
        * p.base("units_per_batch")
    )
    return p.base("annual_demand_units") / capacity if capacity > 0 else float("inf")


def apply_factors(
    factor_ids: tuple[str, ...],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    designs: list[StrategyDesign],
    extra_design_overrides: dict[str, dict[str, float]] | None = None,
) -> tuple[ProductConfig, ParameterSet, SimSettings, list[StrategyDesign]]:
    pp = product.parameters
    g = glob
    st = settings
    ds = [d.model_copy(deep=True) for d in designs]
    s0 = next(d for d in ds if d.id is StrategyId.S0)
    for fid in factor_ids:
        f = FACTORS[fid]
        for k, v in f.global_overrides.items():
            g = set_base(g, k, v)
        for k, v in f.product_overrides.items():
            pp = set_base(pp, k, v)
        for k, v in f.settings_overrides.items():
            if k == "horizon_years":
                st = replace(st, horizon_days=st.warm_up_days + round(float(v) * DAYS_PER_YEAR))
            else:
                st = replace(st, **{k: v})
        for target, dv in f.design_overrides.items():
            for d in ds:
                if target == "*" or d.id.value == target:
                    d.design_variables.update(dv)
        if f.special == "status_quo_utilization":
            util = status_quo_utilization(ProductConfig(product.presentation, pp, product.path), s0)
            scale = util / STATUS_QUO_UTILIZATION_TARGET
            if scale > 1.0:
                pp = set_base(
                    pp,
                    "batches_per_site_year_nominal",
                    pp.base("batches_per_site_year_nominal") * scale,
                )
        elif f.special is not None:
            raise ValueError(f"unknown special factor {f.special}")
    for target, dv in (extra_design_overrides or {}).items():
        for d in ds:
            if target == "*" or d.id.value == target:
                d.design_variables.update(dv)
    return ProductConfig(product.presentation, pp, product.path), g, st, ds


def _site_capacity(site: SiteRuntime) -> float:
    return (
        site.batches_per_year
        * site.spec.uptime_fraction
        * site.spec.batch_size_units
        * site.spec.yield_fraction
    )


def network_capacity_units_per_year(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    n_regions: int,
    include_contracted: bool = True,
) -> float:
    """Saleable units per year of the sites whose output the numerator counts.

    MD-9 (revision R004): reserved and 503B sites used to be left out of this denominator
    while their output stayed in the numerator, so utilization read above 1.0 for S3 and S7.
    The default now covers every site that can produce. Pass ``include_contracted=False``
    for the owned-capacity-only figure, and use ``reserved_capacity_units_per_year`` to see
    the contracted share on its own.
    """
    rt = build_strategy(design, product, glob, n_regions=n_regions)
    return sum(
        _site_capacity(site)
        for site in rt.sites.values()
        if include_contracted or not (site.reserved or site.is_503b())
    )


def reserved_capacity_units_per_year(
    design: StrategyDesign, product: ProductConfig, glob: ParameterSet, n_regions: int
) -> float:
    """Saleable units per year held as reserved or 503B contracted capacity."""
    rt = build_strategy(design, product, glob, n_regions=n_regions)
    return sum(
        _site_capacity(site) for site in rt.sites.values() if site.reserved or site.is_503b()
    )


def _row(config_id: str, product_id: str, r: RunResult, capacity: float) -> dict[str, Any]:
    row: dict[str, Any] = {
        "config_id": config_id,
        "product_id": product_id,
        "strategy_id": r.strategy_id,
        "run_index": r.run_index,
    }
    row.update(r.metrics)
    row.update({f"ledger_{k}": v for k, v in asdict(r.ledger).items() if k != "notes"})
    row["network_capacity_units_per_year"] = capacity
    return row


@dataclass(frozen=True)
class Task:
    config: Config
    product_id: str
    listed_at_t0: bool
    design_variables: dict[str, dict[str, float]]
    settings: SimSettings
    master_seed: int
    runs: list[int]


def _worker(task: Task) -> list[dict[str, Any]]:
    glob = load_global()
    product = load_products()[task.product_id]
    designs = []
    for d in load_all_strategies().designs:
        dd = d.model_copy(deep=True)
        dd.design_variables.update(task.design_variables.get(d.id.value, {}))
        designs.append(dd)
    settings = replace(task.settings, shortage_listed_at_t0=task.listed_at_t0)
    prod, g, st, ds = apply_factors(
        task.config.factors, product, glob, settings, designs, task.config.design_overrides
    )
    cap = {d.id.value: network_capacity_units_per_year(d, prod, g, st.n_regions) for d in ds}
    years = (st.horizon_days - st.warm_up_days) / DAYS_PER_YEAR
    out: list[dict[str, Any]] = []
    for r in run_paired(ds, prod, g, st, task.master_seed, task.runs):
        row = _row(task.config.id, task.product_id, r, cap[r.strategy_id])
        # utilization over the measured horizon: served units / saleable capacity
        row["capacity_utilization"] = (
            r.metrics["served_units"] / (cap[r.strategy_id] * years)
            if cap[r.strategy_id] > 0
            else float("nan")
        )
        out.append(row)
    return out


def _chunks(items: list[int], n: int) -> list[list[int]]:
    n = max(n, 1)
    return [items[i::n] for i in range(n) if items[i::n]]


def _stat(x: np.ndarray) -> dict[str, float]:
    x = x[np.isfinite(x)]
    if x.size == 0:
        return {"mean": float("nan"), "mcse": float("nan"), "n": 0}
    return {
        "mean": float(x.mean()),
        "mcse": float(x.std(ddof=1) / math.sqrt(x.size)) if x.size > 1 else float("nan"),
        "n": int(x.size),
    }


SUMMARY_METRICS: tuple[str, ...] = (
    "fill_rate",
    "shortage_days_per_year",
    "unmet_units_per_year",
    "annual_total_cost",
    "cost_per_delivered_unit",
    "capacity_utilization",
    "material_stockouts",
    "site_failure_days",
    "common_cause_days",
    "supplier_disruption_days",
    "emergency_shipments",
    "batches_started_per_year",
    "expiry_rate",
    "time_to_stable_recovery_median_days",
)


def summarize(rows: list[dict[str, Any]], tau: float, q: float, tau_alt: float) -> dict[str, Any]:
    """Per config x product x strategy: means, MCSE, tail probabilities, feasibility."""
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for r in rows:
        groups.setdefault((r["config_id"], r["product_id"], r["strategy_id"]), []).append(r)
    out: dict[str, Any] = {}
    for (cid, pid, sid), rs in sorted(groups.items()):
        fill = np.array([float(r["fill_rate"]) for r in rs])
        entry: dict[str, Any] = {
            m: _stat(np.array([float(r[m]) for r in rs])) for m in SUMMARY_METRICS
        }
        entry["p_meet"] = float((fill >= tau).mean())
        # MD-16 (revision R004): feasibility is decided on p_meet, so it needs its own
        # uncertainty. The runs are a Bernoulli sample, so the standard error is binomial.
        n_runs = int(fill.size)
        entry["p_meet_mcse"] = (
            float(math.sqrt(entry["p_meet"] * (1.0 - entry["p_meet"]) / n_runs))
            if n_runs > 0
            else float("nan")
        )
        entry["p_meet_alt"] = float((fill >= tau_alt).mean())
        entry["fill_p5"] = float(np.percentile(fill, 5))
        entry["fill_p10"] = float(np.percentile(fill, 10))
        entry["fill_min"] = float(fill.min())
        entry["feasible"] = bool(fill.mean() >= tau and entry["p_meet"] >= q)
        entry["feasible_alt"] = bool(fill.mean() >= tau_alt and entry["p_meet_alt"] >= q)
        out[f"{cid}|{pid}|{sid}"] = entry
    return out


ATTRIBUTION_METRICS: tuple[str, ...] = (
    "fill_rate",
    "p_meet",
    "shortage_days_per_year",
    "unmet_units_per_year",
    "annual_total_cost",
)


def _val(summary: dict[str, Any], key: str, metric: str) -> float:
    e = summary.get(key)
    if e is None:
        return float("nan")
    v = e[metric]
    return float(v["mean"]) if isinstance(v, dict) else float(v)


def attribution(summary: dict[str, Any]) -> list[dict[str, Any]]:
    """Leave-one-out and add-one-in deltas per product x strategy x factor.

    Sign convention: a positive ``loo_delta`` for fill means removing the mechanism raised
    fill; a positive ``addin_delta`` for fill means adding the mechanism alone lowered fill
    (damage). Shares are relative to the base-to-quiet gap for that product x strategy.
    """
    keys = {tuple(k.split("|")) for k in summary}
    pairs = sorted({(p, s) for (_c, p, s) in keys})
    rows: list[dict[str, Any]] = []
    for pid, sid in pairs:
        base = f"base|{pid}|{sid}"
        quiet = f"quiet_all|{pid}|{sid}"
        gap = {m: _val(summary, quiet, m) - _val(summary, base, m) for m in ATTRIBUTION_METRICS}
        for fid, f in FACTORS.items():
            row: dict[str, Any] = {
                "product_id": pid,
                "strategy_id": sid,
                "factor": fid,
                "family": f.family,
                "kind": f.kind,
            }
            loo = f"loo:{fid}|{pid}|{sid}"
            addin = f"addin:{fid}|{pid}|{sid}"
            for m in ATTRIBUTION_METRICS:
                b = _val(summary, base, m)
                l_ = _val(summary, loo, m)
                q_ = _val(summary, quiet, m)
                a = _val(summary, addin, m)
                row[f"base_{m}"] = b
                row[f"loo_{m}"] = l_
                row[f"loo_delta_{m}"] = l_ - b
                row[f"addin_delta_{m}"] = q_ - a
                g = gap[m]
                ok = g != 0.0 and math.isfinite(g)
                row[f"loo_share_{m}"] = (l_ - b) / g if ok else float("nan")
                row[f"addin_share_{m}"] = (q_ - a) / g if ok else float("nan")
            # MD-10 (revision R004): a cost or structure factor has no add-one-in arm, so its
            # add-in delta is nan. min(abs(x), abs(nan)) returns x, which printed a measured
            # zero where nothing had been measured. An absent arm makes the bracket undefined.
            lo_d, hi_d = abs(row["loo_delta_fill_rate"]), abs(row["addin_delta_fill_rate"])
            undefined = math.isnan(lo_d) or math.isnan(hi_d)
            row["shapley_bracket_fill_low"] = float("nan") if undefined else min(lo_d, hi_d)
            row["shapley_bracket_fill_high"] = float("nan") if undefined else max(lo_d, hi_d)
            rows.append(row)
    return rows


def load_design_variables(opt_run_dir: Path | None) -> dict[str, dict[str, dict[str, float]]]:
    """product -> strategy -> design variables from an optimization run (best, else closest grid)."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    if opt_run_dir is None:
        return out
    for path in sorted(opt_run_dir.glob("*__S*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        pick = rec.get("best") or rec.get("best_grid")
        if pick and pick.get("design_variables"):
            out.setdefault(rec["product_id"], {})[rec["strategy_id"]] = {
                k: float(v) for k, v in pick["design_variables"].items()
            }
    return out


def run_ablation(
    *,
    configs: list[Config],
    n_runs: int,
    master_seed: int,
    product_ids: list[str],
    listed_by_product: dict[str, bool],
    horizon_years: float,
    warm_up_days: int,
    design_variables: dict[str, dict[str, dict[str, float]]],
    designs_label: str,
    out_root: Path = RESULTS_ABL,
    workers: int = 0,
    run_id: str | None = None,
) -> Path:
    protocol = load_protocol()
    th = protocol.service_thresholds
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_id = run_id or f"abl_{stamp}"
    out = out_root / run_id
    out.mkdir(parents=True, exist_ok=True)
    workers = workers or max((os.cpu_count() or 2) - 1, 1)
    settings = SimSettings(
        horizon_days=warm_up_days + round(horizon_years * DAYS_PER_YEAR),
        warm_up_days=warm_up_days,
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=th.fill_rate_mean_min,
        recovery_window_days=th.recovery_window_days,
        record_events=False,
    )
    tasks: list[Task] = []
    for cfg in configs:
        for pid in product_ids:
            for chunk in _chunks(list(range(n_runs)), max(workers // max(len(configs) // 4, 1), 1)):
                tasks.append(
                    Task(
                        cfg,
                        pid,
                        bool(listed_by_product.get(pid, False)),
                        design_variables.get(pid, {}),
                        settings,
                        master_seed,
                        chunk,
                    )
                )
    rows: list[dict[str, Any]] = []
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for part in ex.map(_worker, tasks):
                rows.extend(part)
    else:
        for t in tasks:
            rows.extend(_worker(t))
    rows.sort(key=lambda r: (r["config_id"], r["product_id"], r["strategy_id"], r["run_index"]))
    with (out / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    tau_alt = 0.98
    summary = summarize(rows, th.fill_rate_mean_min, th.fill_rate_tail_confidence, tau_alt)
    attr = attribution(summary)
    with (out / "attribution.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(attr[0].keys()) if attr else ["product_id"])
        w.writeheader()
        w.writerows(attr)
    gates = load_gates()
    elig = evaluate_all(gates)
    glob = load_global()
    products = load_products()
    meta = {
        "run_id": run_id,
        "banner": BANNER,
        "tau": th.fill_rate_mean_min,
        "q": th.fill_rate_tail_confidence,
        "tau_alt": tau_alt,
        "n_runs": n_runs,
        "master_seed": master_seed,
        "horizon_years": horizon_years,
        "warm_up_days": warm_up_days,
        "designs": designs_label,
        "design_variables": design_variables,
        "products": product_ids,
        "listed_at_t0": listed_by_product,
        "configs": [asdict(c) for c in configs],
        "factors": {k: asdict(v) for k, v in FACTORS.items()},
        "status_quo_utilization": {
            pid: status_quo_utilization(products[pid], load_all_strategies().by_id(StrategyId.S0))
            for pid in product_ids
        },
        "eligibility": {k.value: v.eligibility.value for k, v in elig.items()},
    }
    (out / "summary.json").write_text(
        json.dumps({"meta": meta, "by_key": summary}, indent=2, default=str), encoding="utf-8"
    )
    manifest = build_run_manifest(
        run_id,
        protocol=protocol,
        config_objects={
            "ablation": meta,
            "global": glob.model_dump(mode="json"),
            "products": {k: v.parameters.model_dump(mode="json") for k, v in products.items()},
            "strategies": [d.model_dump(mode="json") for d in load_all_strategies().designs],
            "gates": gates.model_dump(mode="json"),
        },
        master_seed=master_seed,
        n_runs=n_runs,
        illustrative=True,
        gate_outcomes={
            k.value: {g: s.value for g, s in v.gate_statuses.items()} for k, v in elig.items()
        },
        notes=json.dumps({"kind": "ablation", "results_dir": str(out), "n_configs": len(configs)}),
    )
    write_manifest(manifest)
    return out
