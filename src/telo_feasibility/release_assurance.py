"""Release-assurance submodel: scenarios R0-R3 and the exact delay they may touch.

Rules (protocol 9; task section 15):

* R0 conventional: release time is the critical path of the concurrent test components
  plus serial QA review.
* R1 documentation/orchestration: subtracts a measured administrative reduction from the
  serial QA component only; never below zero.
* R2 shadow mode: no change to release time; abstention events are counted for reporting.
* R3 validated release component: may remove ONLY components in ``REDUCIBLE_COMPONENTS``
  (chemical assay) for batches the layer releases; abstained batches fall back to the
  full conventional path plus a fallback investigation delay; a released batch is a
  wrong release with probability ``conditional_error``. Sterility, endotoxin, EM, QA
  disposition, investigation, validation, and change control are never touched.
* R3 is refused unless ``permitted`` is True (gates, checked by the caller).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rng import lognormal_from_median_cv
from .schemas import ReleaseScenario

REDUCIBLE_COMPONENTS: frozenset[str] = frozenset({"assay"})
NEVER_REDUCIBLE: frozenset[str] = frozenset(
    {"sterility", "endotoxin", "environmental_monitoring", "qa_review_serial"}
)


@dataclass(frozen=True)
class ReleaseAssuranceParams:
    scenario: ReleaseScenario = ReleaseScenario.R0
    permitted: bool = False  # True only when regulatory.r3_permitted(...) is True
    released_fraction: float = 0.0  # coverage of the layer (fraction of batches it releases)
    conditional_error: float = 0.0  # wrong-release probability among released batches
    false_hold_rate: float = 0.0  # fraction of in-spec batches the layer abstains on
    admin_reduction_days: float = 0.0  # R1: measured reduction of serial QA time
    fallback_investigation_days: float = 0.0  # added after an abstention before conventional path
    release_time_cv: float = 0.2

    def __post_init__(self) -> None:
        for name in ("released_fraction", "conditional_error", "false_hold_rate"):
            v = getattr(self, name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{name} outside [0, 1]")
        if self.admin_reduction_days < 0 or self.fallback_investigation_days < 0:
            raise ValueError("negative days")
        if self.scenario is ReleaseScenario.R3 and not self.permitted:
            raise ValueError("R3 cannot be instantiated unless regulatory gates permit it")


@dataclass(frozen=True)
class ReleaseOutcome:
    release_days: float
    abstained: bool
    wrong_release: bool
    components_removed: tuple[str, ...]


def conventional_release_days(components: dict[str, float]) -> float:
    comps = dict(components)
    serial = comps.pop("qa_review_serial", 0.0)
    return (max(comps.values()) if comps else 0.0) + serial


def release_outcome(
    components: dict[str, float], params: ReleaseAssuranceParams, rng: np.random.Generator
) -> ReleaseOutcome:
    """Release time for one batch under the scenario, with the random release-time spread.

    The same generator is consumed in the same order for every scenario (three draws)
    so common random numbers hold across R0-R3.
    """
    u_abstain = float(rng.random())
    u_wrong = float(rng.random())
    spread = float(lognormal_from_median_cv(rng, 1.0, params.release_time_cv)[0])
    comps = dict(components)
    removed: tuple[str, ...] = ()
    abstained = False
    wrong = False
    if params.scenario is ReleaseScenario.R1:
        comps["qa_review_serial"] = max(
            comps.get("qa_review_serial", 0.0) - params.admin_reduction_days, 0.0
        )
    elif params.scenario is ReleaseScenario.R2:
        abstained = u_abstain >= params.released_fraction  # counted, no effect on time
    elif params.scenario is ReleaseScenario.R3:
        if not params.permitted:
            raise RuntimeError("R3 requested without permission")
        if u_abstain < params.released_fraction:
            for c in REDUCIBLE_COMPONENTS:
                if c in comps:
                    comps.pop(c)
                    removed = (*removed, c)
            wrong = u_wrong < params.conditional_error
        else:
            abstained = True
            comps["qa_review_serial"] = (
                comps.get("qa_review_serial", 0.0) + params.fallback_investigation_days
            )
    base = conventional_release_days(comps)
    return ReleaseOutcome(
        release_days=base * spread,
        abstained=abstained,
        wrong_release=wrong,
        components_removed=removed,
    )
