"""Seeded random streams with common random numbers.

Every draw is keyed by (run index, stream, entity id, optional ordinal) through
``numpy.random.SeedSequence`` so that

* two strategies in the same run see identical exogenous events (common random numbers);
* adding an entity never changes another entity's draws;
* results are reproducible across processes and platforms.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .provenance import stable_hash64
from .schemas import STREAM_INDEX, RandomStream


@dataclass(frozen=True)
class StreamKey:
    run_index: int
    stream: RandomStream
    entity_id: str
    ordinal: int = 0


class RunStreams:
    """Factory for per-entity generators inside one run."""

    def __init__(self, master_seed: int, run_index: int) -> None:
        if master_seed < 0 or run_index < 0:
            raise ValueError("seed and run index must be non-negative")
        self.master_seed = master_seed
        self.run_index = run_index

    def generator(
        self, stream: RandomStream, entity_id: str, ordinal: int = 0
    ) -> np.random.Generator:
        key = (
            self.run_index,
            STREAM_INDEX[stream],
            stable_hash64(entity_id) & 0xFFFFFFFF,
            (stable_hash64(entity_id) >> 32) & 0xFFFFFFFF,
            ordinal,
        )
        seq = np.random.SeedSequence(entropy=self.master_seed, spawn_key=key)
        return np.random.Generator(np.random.PCG64(seq))


def lognormal_from_median_cv(
    rng: np.random.Generator, median: float, cv: float, size: int | None = None
) -> np.ndarray:
    """Lognormal with the given median and coefficient of variation (of the lognormal)."""
    if median <= 0:
        return np.zeros(size or 1) if size else np.zeros(1)
    sigma = float(np.sqrt(np.log1p(cv * cv))) if cv > 0 else 0.0
    out = rng.lognormal(mean=np.log(median), sigma=sigma, size=size)
    return np.atleast_1d(out)


def beta_from_mean_sd(rng: np.random.Generator, mean: float, sd: float) -> float:
    """Beta draw parameterized by mean and standard deviation; degenerate when sd = 0."""
    mean = min(max(mean, 1e-9), 1 - 1e-9)
    if sd <= 0:
        return float(mean)
    var = min(sd * sd, mean * (1 - mean) * 0.999)
    k = mean * (1 - mean) / var - 1.0
    a = max(mean * k, 1e-6)
    b = max((1 - mean) * k, 1e-6)
    return float(rng.beta(a, b))
