"""Exogenous world generation: demand multipliers, shocks, site and supplier failures,
common-cause events, regulatory (shortage-list) state, transport delays.

The world is generated once per run for the universal entity roster and shared by
every strategy in that run (common random numbers). Every entity draws from its own
entity-keyed stream, so adding a site never perturbs another site's failures.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .rng import RunStreams, beta_from_mean_sd, lognormal_from_median_cv
from .schemas import DisruptionEvent, DisruptionKind, ParameterSet, RandomStream

DAYS_PER_YEAR = 365.25


@dataclass(frozen=True)
class Roster:
    """Universal entity roster the world is generated for."""

    region_ids: tuple[str, ...]
    site_ids: tuple[str, ...]
    supplier_ids: tuple[str, ...]
    lane_ids: tuple[str, ...]
    group_ids: tuple[str, ...]


@dataclass(frozen=True)
class WorldParams:
    horizon_days: int
    demand_cv: float
    demand_autocorrelation: float
    seasonality_amplitude: float
    shock_rate_per_year: float
    shock_duration_median_days: float
    shock_multiplier_median: float
    shock_all_regions_probability: float
    site_failure_rate_per_year: float
    site_failure_duration_median_days: float
    site_failure_residual_capacity: float
    supplier_disruption_rate_per_year: float
    supplier_disruption_duration_median_days: float
    common_cause_rate_per_year: float
    common_cause_duration_median_days: float
    common_cause_impact_mean: float
    common_cause_impact_sd: float
    duration_cv: float
    transport_cv: float
    shortage_listed_at_t0: bool
    shortage_resolution_rate_per_year: float
    shortage_relisting_rate_per_year: float

    @classmethod
    def from_parameters(
        cls, glob: ParameterSet, horizon_days: int, shortage_listed_at_t0: bool
    ) -> WorldParams:
        b = glob.base
        return cls(
            horizon_days=horizon_days,
            demand_cv=b("demand_cv"),
            demand_autocorrelation=b("demand_autocorrelation"),
            seasonality_amplitude=b("demand_seasonality_amplitude"),
            shock_rate_per_year=b("demand_shocks_per_year"),
            shock_duration_median_days=b("demand_shock_duration_days"),
            shock_multiplier_median=b("demand_shock_multiplier"),
            shock_all_regions_probability=b("demand_shock_all_regions_probability"),
            site_failure_rate_per_year=b("site_failures_per_site_year"),
            site_failure_duration_median_days=b("site_failure_duration_days"),
            site_failure_residual_capacity=b("site_failure_residual_capacity"),
            supplier_disruption_rate_per_year=b("supplier_disruptions_per_supplier_year"),
            supplier_disruption_duration_median_days=b("supplier_disruption_duration_days"),
            common_cause_rate_per_year=b("common_cause_events_per_year"),
            common_cause_duration_median_days=b("common_cause_duration_days"),
            common_cause_impact_mean=b("common_cause_capacity_impact"),
            common_cause_impact_sd=b("common_cause_capacity_impact_sd"),
            duration_cv=b("disruption_duration_cv"),
            transport_cv=b("transport_time_cv"),
            shortage_listed_at_t0=shortage_listed_at_t0,
            shortage_resolution_rate_per_year=b("shortage_list_resolution_rate_per_year"),
            shortage_relisting_rate_per_year=b("shortage_list_relisting_rate_per_year"),
        )


@dataclass
class ExogenousWorld:
    horizon_days: int
    routine_demand_multiplier: dict[str, np.ndarray]  # region -> (n_days,) mean-1 multiplier
    shock_multiplier: dict[str, np.ndarray]  # region -> (n_days,) >= 1
    site_capacity: dict[str, np.ndarray]  # site -> (n_days,) fraction from idiosyncratic failures
    supplier_capacity: dict[str, np.ndarray]  # supplier -> (n_days,)
    group_capacity: dict[str, np.ndarray]  # common-cause group -> (n_days,)
    shortage_listed: np.ndarray  # (n_days,) bool
    transport_multiplier: dict[str, np.ndarray]  # lane -> (n_days,) >= 0 multiplier on transit days
    events: list[DisruptionEvent] = field(default_factory=list)

    def demand_multiplier(self, region_id: str) -> np.ndarray:
        return np.asarray(
            self.routine_demand_multiplier[region_id] * self.shock_multiplier[region_id],
            dtype=float,
        )

    def effective_site_capacity(self, site_id: str, group_ids: list[str]) -> np.ndarray:
        cap = self.site_capacity[site_id].copy()
        for g in group_ids:
            cap = np.minimum(cap, self.group_capacity[g])
        return cap

    def effective_supplier_capacity(self, supplier_id: str, group_ids: list[str]) -> np.ndarray:
        cap = self.supplier_capacity[supplier_id].copy()
        for g in group_ids:
            cap = np.minimum(cap, self.group_capacity[g])
        return cap

    def digest(self) -> str:
        """Stable hash of every array, used by the common-random-number test."""
        import hashlib

        h = hashlib.sha256()
        for name, table in (
            ("routine", self.routine_demand_multiplier),
            ("shock", self.shock_multiplier),
            ("site", self.site_capacity),
            ("supplier", self.supplier_capacity),
            ("group", self.group_capacity),
            ("transport", self.transport_multiplier),
        ):
            for k in sorted(table):
                h.update(name.encode())
                h.update(k.encode())
                h.update(np.ascontiguousarray(table[k]).tobytes())
        h.update(self.shortage_listed.tobytes())
        return h.hexdigest()


def _ar1_lognormal_multiplier(
    rng: np.random.Generator, n: int, cv: float, phi: float
) -> np.ndarray:
    """Mean-one lognormal AR(1) multiplier with stationary CV ``cv`` and lag-1 autocorrelation ``phi``."""
    if cv <= 0 or n == 0:
        return np.ones(n)
    sigma2 = float(np.log1p(cv * cv))
    phi = min(max(phi, 0.0), 0.99)
    innov_sd = float(np.sqrt(sigma2 * (1.0 - phi * phi)))
    x = np.empty(n)
    x[0] = rng.normal(0.0, np.sqrt(sigma2))
    eps = rng.normal(0.0, innov_sd, size=n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + eps[t]
    return np.asarray(np.exp(x - sigma2 / 2.0), dtype=float)


def _poisson_events(rng: np.random.Generator, rate_per_year: float, horizon: int) -> list[int]:
    n = int(rng.poisson(rate_per_year * horizon / DAYS_PER_YEAR)) if rate_per_year > 0 else 0
    if n == 0:
        return []
    starts = rng.integers(0, horizon, size=n)
    return sorted(int(s) for s in starts)


def _apply_capacity_loss(arr: np.ndarray, start: int, duration: int, remaining: float) -> None:
    end = min(start + max(duration, 1), arr.shape[0])
    arr[start:end] = np.minimum(arr[start:end], remaining)


def generate_world(params: WorldParams, roster: Roster, streams: RunStreams) -> ExogenousWorld:
    n_days = params.horizon_days
    events: list[DisruptionEvent] = []
    days = np.arange(n_days)
    season = 1.0 + params.seasonality_amplitude * np.sin(2.0 * np.pi * days / DAYS_PER_YEAR)

    routine: dict[str, np.ndarray] = {}
    for rid in roster.region_ids:
        g = streams.generator(RandomStream.ROUTINE_DEMAND, rid)
        routine[rid] = (
            _ar1_lognormal_multiplier(g, n_days, params.demand_cv, params.demand_autocorrelation)
            * season
        )

    shock = {rid: np.ones(n_days) for rid in roster.region_ids}
    g = streams.generator(RandomStream.DEMAND_SHOCKS, "network")
    for k, start in enumerate(_poisson_events(g, params.shock_rate_per_year, n_days)):
        dur = round(
            float(
                lognormal_from_median_cv(g, params.shock_duration_median_days, params.duration_cv)[
                    0
                ]
            )
        )
        mult = float(lognormal_from_median_cv(g, params.shock_multiplier_median, 0.25)[0])
        mult = max(mult, 1.0)
        if g.random() < params.shock_all_regions_probability or len(roster.region_ids) == 1:
            targets = list(roster.region_ids)
        else:
            targets = [roster.region_ids[int(g.integers(0, len(roster.region_ids)))]]
        for rid in targets:
            end = min(start + max(dur, 1), n_days)
            shock[rid][start:end] = np.maximum(shock[rid][start:end], mult)
        events.append(
            DisruptionEvent(
                id=f"shock{k}",
                kind=DisruptionKind.DEMAND_SHOCK,
                target_ids=targets,
                start_day=start,
                duration_days=max(dur, 1),
                magnitude=mult,
            )
        )

    site_cap: dict[str, np.ndarray] = {}
    for sid in roster.site_ids:
        arr = np.ones(n_days)
        gs = streams.generator(RandomStream.SITE_FAILURES, sid)
        for k, start in enumerate(_poisson_events(gs, params.site_failure_rate_per_year, n_days)):
            dur = round(
                float(
                    lognormal_from_median_cv(
                        gs, params.site_failure_duration_median_days, params.duration_cv
                    )[0]
                )
            )
            _apply_capacity_loss(arr, start, dur, params.site_failure_residual_capacity)
            events.append(
                DisruptionEvent(
                    id=f"{sid}:fail{k}",
                    kind=DisruptionKind.SITE_FAILURE,
                    target_ids=[sid],
                    start_day=start,
                    duration_days=max(dur, 1),
                    capacity_fraction_remaining=params.site_failure_residual_capacity,
                )
            )
        site_cap[sid] = arr

    sup_cap: dict[str, np.ndarray] = {}
    for sid in roster.supplier_ids:
        arr = np.ones(n_days)
        gs = streams.generator(RandomStream.SUPPLIER_DISRUPTIONS, sid)
        for k, start in enumerate(
            _poisson_events(gs, params.supplier_disruption_rate_per_year, n_days)
        ):
            dur = round(
                float(
                    lognormal_from_median_cv(
                        gs, params.supplier_disruption_duration_median_days, params.duration_cv
                    )[0]
                )
            )
            _apply_capacity_loss(arr, start, dur, 0.0)
            events.append(
                DisruptionEvent(
                    id=f"{sid}:disr{k}",
                    kind=DisruptionKind.SUPPLIER,
                    target_ids=[sid],
                    start_day=start,
                    duration_days=max(dur, 1),
                    capacity_fraction_remaining=0.0,
                )
            )
        sup_cap[sid] = arr

    grp_cap: dict[str, np.ndarray] = {}
    for gid in roster.group_ids:
        arr = np.ones(n_days)
        gg = streams.generator(RandomStream.COMMON_CAUSE_EVENTS, gid)
        for k, start in enumerate(_poisson_events(gg, params.common_cause_rate_per_year, n_days)):
            dur = round(
                float(
                    lognormal_from_median_cv(
                        gg, params.common_cause_duration_median_days, params.duration_cv
                    )[0]
                )
            )
            impact = beta_from_mean_sd(
                gg, params.common_cause_impact_mean, params.common_cause_impact_sd
            )
            _apply_capacity_loss(arr, start, dur, 1.0 - impact)
            events.append(
                DisruptionEvent(
                    id=f"{gid}:cc{k}",
                    kind=DisruptionKind.COMMON_CAUSE,
                    target_ids=[gid],
                    start_day=start,
                    duration_days=max(dur, 1),
                    capacity_fraction_remaining=1.0 - impact,
                    common_cause_group_id=gid,
                )
            )
        grp_cap[gid] = arr

    listed = np.empty(n_days, dtype=bool)
    gr = streams.generator(RandomStream.REGULATORY_STATE_TRANSITIONS, "shortage_list")
    state = params.shortage_listed_at_t0
    p_off = params.shortage_resolution_rate_per_year / DAYS_PER_YEAR
    p_on = params.shortage_relisting_rate_per_year / DAYS_PER_YEAR
    u = gr.random(n_days)
    for t in range(n_days):
        listed[t] = state
        if state and u[t] < p_off:
            state = False
            events.append(
                DisruptionEvent(
                    id=f"reg:off{t}",
                    kind=DisruptionKind.REGULATORY,
                    target_ids=["shortage_list"],
                    start_day=t,
                    duration_days=0,
                )
            )
        elif not state and u[t] < p_on:
            state = True

    transport: dict[str, np.ndarray] = {}
    for lid in roster.lane_ids:
        gt = streams.generator(RandomStream.TRANSPORT_DELAY, lid)
        transport[lid] = lognormal_from_median_cv(gt, 1.0, params.transport_cv, size=n_days)

    return ExogenousWorld(
        horizon_days=n_days,
        routine_demand_multiplier=routine,
        shock_multiplier=shock,
        site_capacity=site_cap,
        supplier_capacity=sup_cap,
        group_capacity=grp_cap,
        shortage_listed=listed,
        transport_multiplier=transport,
        events=sorted(events, key=lambda e: (e.start_day, e.id)),
    )
