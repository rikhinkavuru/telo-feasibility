"""Shared helpers for engine tests: parameter overrides and short-horizon settings."""

from __future__ import annotations

import pytest

from telo_feasibility.configs import ProductConfig, load_global, load_products, load_strategies
from telo_feasibility.schemas import ParameterSet
from telo_feasibility.simulation import SimSettings


def override(ps: ParameterSet, **values: float) -> ParameterSet:
    """Deep copy with base values replaced (low/high widened so ordering validation holds)."""
    out = ps.model_copy(deep=True)
    for k, v in values.items():
        prm = out.parameters[k]
        lo = prm.low if prm.low is not None else v
        hi = prm.high if prm.high is not None else v
        prm.low = min(lo, v)
        prm.high = max(hi, v)
        prm.base = v
    return out


def quiet(ps: ParameterSet) -> ParameterSet:
    """No randomness and no failures: deterministic throughput."""
    return override(
        ps,
        demand_cv=0.0,
        demand_shocks_per_year=0.0,
        site_failures_per_site_year=0.0,
        supplier_disruptions_per_supplier_year=0.0,
        common_cause_events_per_year=0.0,
        transport_time_cv=0.0,
        deviation_rate_per_batch=0.0,
        batch_rejection_rate=0.0,
        yield_sd=0.0,
        release_time_cv=0.0,
        shortage_list_resolution_rate_per_year=0.0,
        shortage_list_relisting_rate_per_year=0.0,
    )


@pytest.fixture(scope="session")
def glob() -> ParameterSet:
    return load_global()


@pytest.fixture(scope="session")
def product() -> ProductConfig:
    return load_products()["sodium_bicarbonate_8_4_50ml"]


@pytest.fixture(scope="session")
def designs():  # type: ignore[no-untyped-def]
    return load_strategies()


@pytest.fixture
def settings() -> SimSettings:
    return SimSettings(
        horizon_days=400,
        warm_up_days=100,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=True,
    )
