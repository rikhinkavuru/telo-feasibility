"""Demand process: presentation-specific daily demand by region.

Base case (protocol 8.1): annual demand x regional share, growth, seasonality, a mean-one
lognormal AR(1) routine multiplier, and compound shocks, all from the exogenous world.
Contracted demand is a share of potential demand and is what node economics may count.
Substitution matrices are represented as a field but disabled until clinically reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .disruptions import DAYS_PER_YEAR, ExogenousWorld


@dataclass(frozen=True)
class DemandSpec:
    annual_demand_units: float
    region_shares: dict[str, float]
    annual_growth: float
    contracted_share: float = 1.0
    substitution_enabled: bool = False

    def mean_daily(self, region_id: str, day: int) -> float:
        growth = (1.0 + self.annual_growth) ** (day / DAYS_PER_YEAR)
        return float(
            self.annual_demand_units * self.region_shares[region_id] / DAYS_PER_YEAR * growth
        )


def generate_demand_paths(spec: DemandSpec, world: ExogenousWorld) -> dict[str, np.ndarray]:
    """Integer daily demand per region for the whole horizon (rounded, nonnegative)."""
    n_days = world.horizon_days
    out: dict[str, np.ndarray] = {}
    days = np.arange(n_days)
    for rid, share in spec.region_shares.items():
        growth = (1.0 + spec.annual_growth) ** (days / DAYS_PER_YEAR)
        mean = spec.annual_demand_units * share / DAYS_PER_YEAR * growth
        path = mean * world.demand_multiplier(rid)
        out[rid] = np.maximum(np.rint(path), 0).astype(np.int64)
    return out


def demand_moments(paths: dict[str, np.ndarray]) -> dict[str, dict[str, float]]:
    """Mean, CV, lag-1 autocorrelation per region; used by posterior predictive checks."""
    out: dict[str, dict[str, float]] = {}
    for rid, x in paths.items():
        xf = x.astype(float)
        mean = float(xf.mean()) if xf.size else 0.0
        sd = float(xf.std()) if xf.size else 0.0
        cv = sd / mean if mean > 0 else 0.0
        if xf.size > 2 and sd > 0:
            a = xf[:-1] - mean
            b = xf[1:] - mean
            rho = float((a * b).sum() / ((a * a).sum() ** 0.5 * (b * b).sum() ** 0.5))
        else:
            rho = 0.0
        out[rid] = {"mean": mean, "cv": cv, "lag1": rho}
    return out
