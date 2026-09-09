"""Release queue: batch disposition with yield, deviation, rejection, and release time."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .release_assurance import ReleaseAssuranceParams, release_outcome
from .rng import RunStreams, beta_from_mean_sd, lognormal_from_median_cv
from .schemas import RandomStream


@dataclass(frozen=True)
class QualityParams:
    deviation_rate: float
    rejection_rate: float
    investigation_median_days: float
    duration_cv: float
    yield_sd: float


@dataclass
class QueuedBatch:
    batch_id: str
    site_id: str
    ordinal: int
    filled_units: int
    saleable_units: int
    start_day: int
    completion_day: int
    release_day: int
    deviation: bool
    rejected: bool
    abstained: bool
    wrong_release: bool
    release_days: float
    pathway: str


def disposition(
    *,
    batch_id: str,
    site_id: str,
    ordinal: int,
    filled_units: int,
    start_day: int,
    completion_day: int,
    yield_mean: float,
    components: dict[str, float],
    qp: QualityParams,
    ra: ReleaseAssuranceParams,
    streams: RunStreams,
    pathway: str,
) -> QueuedBatch:
    """Draw yield, deviation, rejection, and release time from entity-keyed streams.

    Each stream is keyed by (site, ordinal) so a batch at the same site and ordinal
    receives identical draws in every strategy that produces it.
    """
    g_yield = streams.generator(RandomStream.YIELD, site_id, ordinal)
    g_dev = streams.generator(RandomStream.DEVIATIONS, site_id, ordinal)
    g_rej = streams.generator(RandomStream.BATCH_REJECTION, site_id, ordinal)
    g_rel = streams.generator(RandomStream.RELEASE_TIME, site_id, ordinal)
    y = beta_from_mean_sd(g_yield, yield_mean, qp.yield_sd)
    saleable = int(np.floor(filled_units * y))
    deviation = bool(g_dev.random() < qp.deviation_rate)
    rejected = bool(g_rej.random() < qp.rejection_rate)
    out = release_outcome(components, ra, g_rel)
    days = out.release_days
    if deviation:
        days += float(
            lognormal_from_median_cv(g_dev, qp.investigation_median_days, qp.duration_cv)[0]
        )
    release_day = completion_day + round(days)
    return QueuedBatch(
        batch_id=batch_id,
        site_id=site_id,
        ordinal=ordinal,
        filled_units=filled_units,
        saleable_units=0 if rejected else saleable,
        start_day=start_day,
        completion_day=completion_day,
        release_day=release_day,
        deviation=deviation,
        rejected=rejected,
        abstained=out.abstained,
        wrong_release=out.wrong_release,
        release_days=days,
        pathway=pathway,
    )
