"""Shared fixtures."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from telo_feasibility.schemas import (
    Confidence,
    EvidenceTier,
    UncertainParameter,
    Unit,
    ValidationStatus,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def package_root() -> Path:
    return PACKAGE_ROOT


def make_param(
    pid: str = "site.yield_fraction",
    *,
    units: Unit = Unit.FRACTION,
    low: float | None = 0.9,
    base: float | None = 0.96,
    high: float | None = 0.99,
    tier: EvidenceTier = EvidenceTier.ILLUSTRATIVE,
    status: ValidationStatus = ValidationStatus.ILLUSTRATIVE,
    source_ids: list[str] | None = None,
    access_date: date | None = None,
    **kw: object,
) -> UncertainParameter:
    return UncertainParameter(
        id=pid,
        definition="test parameter",
        units=units,
        entity_level="site",
        low=low,
        base=base,
        high=high,
        evidence_tier=tier,
        confidence=Confidence.LOW,
        validation_status=status,
        source_ids=source_ids or [],
        access_date=access_date,
        **kw,  # type: ignore[arg-type]
    )


@pytest.fixture
def illustrative_param() -> UncertainParameter:
    return make_param()
