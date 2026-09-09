"""Historical backcasting framework (protocol 12.2; task section 20).

An episode record freezes what was observable at its start (from snapshots) and states
what the simulation is allowed to use. The framework injects the episode's class into the
shared exogenous world, simulates the chosen architecture, and compares simulated
duration, severity, recovery shape, and binding bottleneck with the observed record.
Every mismatch is logged; nothing here is a counterfactual proof.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from .configs import load_all_strategies, load_global, load_products
from .disruptions import ExogenousWorld
from .provenance import PACKAGE_ROOT, load_protocol
from .schemas import StrategyId
from .simulation import SimSettings, simulate_run, world_for_run
from .strategies import build_strategy

EPISODES_PATH = PACKAGE_ROOT / "data" / "historical_backcasts" / "episodes.yaml"
RESULTS_BACK = PACKAGE_ROOT / "results" / "backcasts"


def load_episodes(path: Path = EPISODES_PATH) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    eps = data.get("episodes", []) if isinstance(data, dict) else []
    return [e for e in eps if isinstance(e, dict)]


def inject(world: ExogenousWorld, spec: dict[str, Any] | None) -> list[str]:
    """Overlay a deterministic episode on the world; returns notes."""
    if not spec:
        return ["no injection: observed episode is reproduced only if the base inputs imply it"]
    kind = str(spec["kind"])
    start = int(spec["start_day"])
    dur = int(spec["duration_days"])
    end = min(start + dur, world.horizon_days)
    if kind == "site_failure":
        arr = world.site_capacity[str(spec["target"])]
        arr[start:end] = 0.0
    elif kind == "supplier":
        arr = world.supplier_capacity[str(spec["target"])]
        arr[start:end] = 0.0
    elif kind == "common_cause":
        arr = world.group_capacity[str(spec["target"])]
        arr[start:end] = max(0.0, 1.0 - float(spec.get("impact", 1.0)))
    elif kind == "demand_shock":
        mult = float(spec.get("magnitude", 1.35))
        targets = (
            list(world.shock_multiplier)
            if spec.get("target") in (None, "all")
            else [str(spec["target"])]
        )
        for r in targets:
            world.shock_multiplier[r][start:end] = np.maximum(
                world.shock_multiplier[r][start:end], mult
            )
    else:
        raise ValueError(f"unknown injection kind {kind}")
    return [f"injected {kind} on {spec.get('target')} from day {start} for {dur} days"]


@dataclass
class BackcastComparison:
    episode_id: str
    product_id: str
    strategy_id: str
    observed_duration_days_min: float | None
    observed_ongoing: bool
    simulated_episode_count: float
    simulated_longest_episode_days: float
    simulated_recovered_fraction: float
    simulated_fill_rate: float
    simulated_peak_unmet_units: float
    simulated_material_stockouts: float
    simulated_site_failure_days: float
    binding_bottleneck_simulated: str
    binding_bottleneck_observed: str
    consistent_duration: bool | None
    mismatches: list[str]
    human_required: list[str]
    notes: list[str]


def _binding_bottleneck(metrics: dict[str, float], utilization: float) -> str:
    if utilization > 1.0:
        return "capacity below demand (chronic)"
    if metrics.get("material_stockouts", 0) > metrics.get("site_failure_days", 0):
        return "material availability"
    if metrics.get("site_failure_days", 0) > 0:
        return "site failure"
    return "none dominant"


def backcast_episode(
    ep: dict[str, Any], *, seed: int = 20260901, horizon_days: int = 365 + 1826
) -> BackcastComparison:
    products = load_products()
    glob = load_global()
    th = load_protocol().service_thresholds
    pid = str(ep["product_id"])
    notes: list[str] = []
    if pid not in products:
        notes.append(
            f"no product config for {pid}; scaffold product sodium_bicarbonate_8_4_50ml used for a behavior test only"
        )
        pid_used = "sodium_bicarbonate_8_4_50ml"
    else:
        pid_used = pid
    product = products[pid_used]
    sid = StrategyId(str(ep["simulate"]["strategy_id"]))
    design = load_all_strategies().by_id(sid)
    settings = SimSettings(
        horizon_days=horizon_days,
        warm_up_days=365,
        shortage_day_threshold=th.shortage_day_threshold,
        fill_rate_mean_min=th.fill_rate_mean_min,
        recovery_window_days=th.recovery_window_days,
        record_events=False,
        shortage_listed_at_t0=True,
    )
    world, streams = world_for_run(glob, settings, seed, 0)
    notes += inject(world, ep["simulate"].get("inject"))
    rt = build_strategy(design, product, glob, n_regions=settings.n_regions)
    res = simulate_run(rt, product, glob, world, streams, settings)
    site = rt.sites["central"].spec
    capacity = (
        site.batch_size_units
        * site.batches_per_year_nominal
        * site.yield_fraction
        * site.uptime_fraction
    )
    utilization = (
        product.parameters.base("annual_demand_units") / capacity if capacity > 0 else float("inf")
    )
    longest = (
        max(
            (
                e["time_to_stable_recovery_days"]
                if e["recovered"] == 1.0
                else float(horizon_days - 365 - e["start_day"])
            )
            for e in res.episodes
        )
        if res.episodes
        else 0.0
    )
    obs = ep.get("observed", {})
    obs_min = obs.get("observed_duration_days_min")
    ongoing = obs.get("end_date") is None and obs.get("start_date") is not None
    consistent: bool | None = None
    mismatches: list[str] = []
    if obs_min is not None:
        sim_span = horizon_days - 365
        if ongoing:
            consistent = bool(res.episodes) and res.metrics["episodes_recovered_fraction"] < 1.0
            if not consistent:
                mismatches.append(
                    "observed shortage is ongoing but the simulation recovers within the horizon"
                )
        else:
            consistent = abs(longest - float(obs_min)) <= 0.5 * float(obs_min)
        if longest >= sim_span * 0.95 and not ongoing:
            mismatches.append("simulation never recovers although the observed episode resolved")
    observed_bottleneck = "; ".join(obs.get("stated_reasons", [])) or "unknown"
    return BackcastComparison(
        episode_id=str(ep["id"]),
        product_id=pid_used,
        strategy_id=sid.value,
        observed_duration_days_min=float(obs_min) if obs_min is not None else None,
        observed_ongoing=bool(ongoing),
        simulated_episode_count=res.metrics["episodes"],
        simulated_longest_episode_days=float(longest),
        simulated_recovered_fraction=res.metrics["episodes_recovered_fraction"],
        simulated_fill_rate=res.metrics["fill_rate"],
        simulated_peak_unmet_units=res.metrics["peak_shortfall_units"],
        simulated_material_stockouts=res.metrics["material_stockouts"],
        simulated_site_failure_days=res.metrics["site_failure_days"],
        binding_bottleneck_simulated=_binding_bottleneck(res.metrics, utilization),
        binding_bottleneck_observed=observed_bottleneck,
        consistent_duration=consistent,
        mismatches=mismatches,
        human_required=[str(x) for x in ep.get("human_required", [])],
        notes=[*notes, str(ep.get("frozen_inputs_note", ""))],
    )


def run_backcasts(out_root: Path = RESULTS_BACK) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = out_root / f"back_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    comps = []
    for ep in load_episodes():
        if ep.get("information_frozen_at") is None:
            comps.append(
                {
                    "episode_id": ep["id"],
                    "status": "not_run",
                    "reason": "episode not yet documented from primary sources",
                    "human_required": ep.get("human_required", []),
                }
            )
            continue
        c = backcast_episode(ep)
        comps.append(asdict(c))
        (out / f"{c.episode_id}").mkdir(exist_ok=True)
        (out / f"{c.episode_id}" / "comparison.json").write_text(
            json.dumps(asdict(c), indent=2, default=str), encoding="utf-8"
        )
    (out / "summary.json").write_text(
        json.dumps(
            {"banner": "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS", "episodes": comps},
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    return out
