"""Site production state: campaign occupancy, commissioning, activation, batch starts."""

from __future__ import annotations

from dataclasses import dataclass, field

from .disruptions import DAYS_PER_YEAR
from .schemas import ManufacturingSite, Pathway


@dataclass
class SiteRuntime:
    spec: ManufacturingSite
    batches_per_year: float  # design capacity (nominal x scale) once fully commissioned
    serves_region_ids: tuple[str, ...]
    reserved: bool = False  # reserved contract capacity: idle until activated
    activation_threshold_days: float = 0.0
    activation_lead_days: float = 0.0
    campaign_batches: int = 0
    available_from_day: int = 0
    busy_until: int = -1
    next_ordinal: int = 0
    active_until_batches: int = 0  # remaining campaign batches when reserved
    activation_pending_day: int | None = None
    batches_started: int = 0
    fg_target_days: float = 30.0
    common_cause_groups: tuple[str, ...] = ()
    supplier_ids: tuple[str, ...] = field(default_factory=tuple)
    # warm standby (design-space strategies): exercise cadence and activation reliability
    exercise_interval_days: float = 0.0  # 0 = no exercise batches
    next_exercise_day: int = 0
    activation_failure_probability: float = 0.0
    activation_attempts: int = 0
    activation_failures: int = 0
    # capacity ramp (model defect MD-7, revision R004): capacity above what the site runs on
    # day zero is an expansion and is not available until it has been built and qualified.
    # ``baseline_batches_per_year`` is what the site can run from day zero; the design
    # capacity arrives at ``expansion_available_day``. A site that does not exist at t0 has
    # no baseline and is gated by ``available_from_day`` instead, as before.
    baseline_batches_per_year: float | None = None
    expansion_available_day: int = 0

    def batches_per_year_on(self, day: int) -> float:
        """Scheduling capacity on ``day``: the baseline until the expansion is commissioned."""
        if self.baseline_batches_per_year is None or day >= self.expansion_available_day:
            return self.batches_per_year
        return self.baseline_batches_per_year

    def occupancy_days_on(self, day: int) -> float:
        rate = self.batches_per_year_on(day)
        if rate <= 0:
            return float("inf")
        return DAYS_PER_YEAR / rate / max(self.spec.uptime_fraction, 1e-9)

    @property
    def occupancy_days(self) -> float:
        """Occupancy at full design capacity. Scheduling uses ``occupancy_days_on``."""
        return self.occupancy_days_on(self.expansion_available_day)

    def exists(self, day: int) -> bool:
        return day >= self.available_from_day

    def is_503b(self) -> bool:
        return self.spec.pathway is Pathway.P503B

    def can_start(self, day: int, capacity_fraction: float, shortage_listed: bool) -> bool:
        if self.batches_per_year_on(day) <= 0.0:
            return False
        if not self.exists(day) or day < self.busy_until or capacity_fraction <= 0.0:
            return False
        if self.reserved and self.active_until_batches <= 0:
            return False
        return not (self.is_503b() and not shortage_listed)

    def start_batch(self, day: int, capacity_fraction: float) -> tuple[int, int]:
        """Occupy the line; return (ordinal, completion_day)."""
        ordinal = self.next_ordinal
        self.next_ordinal += 1
        self.batches_started += 1
        latency = self.spec.changeover_days + self.spec.production_cycle_days
        occupancy = self.occupancy_days_on(day) / max(capacity_fraction, 1e-9)
        self.busy_until = day + round(max(occupancy, latency))
        if self.reserved:
            self.active_until_batches -= 1
            # MD-23 (revision R009): readiness is time since the last qualified batch, not
            # time since the last batch labelled an exercise. Any batch requalifies the
            # line, so the exercise clock restarts here. Before this, `exercise_due`
            # required the line to be idle, so on a frequently activated line a campaign
            # batch displaced an exercise batch one for one and the cadence was almost
            # unmeasurable: the S16 exercise ablation moved fill by 0.0016 while the same
            # ablation on the rarely activated S17 moved it by 0.0107.
            if self.exercise_interval_days > 0:
                self.next_exercise_day = day + max(round(self.exercise_interval_days), 1)
        return ordinal, day + round(latency)

    def request_activation(self, day: int) -> None:
        if self.reserved and self.activation_pending_day is None and self.active_until_batches <= 0:
            self.activation_pending_day = day + round(self.activation_lead_days)

    def activation_due(self, day: int) -> bool:
        return self.activation_pending_day is not None and day >= self.activation_pending_day

    def advance_activation(self, day: int, u: float = 1.0) -> bool:
        """Resolve a due activation; ``u`` in [0, 1) below the failure probability fails it.

        A failed activation is re-requested immediately (another full lead time), so a
        site with failure probability p needs 1/(1-p) attempts on average.
        """
        if not self.activation_due(day):
            return False
        self.activation_pending_day = None
        self.activation_attempts += 1
        if u < self.activation_failure_probability:
            self.activation_failures += 1
            self.activation_pending_day = day + round(self.activation_lead_days)
            return False
        self.active_until_batches = self.campaign_batches
        return True

    def exercise_due(self, day: int) -> bool:
        """Warm standby: a scheduled exercise batch keeps the line validated while idle."""
        if not self.reserved or self.exercise_interval_days <= 0 or not self.exists(day):
            return False
        return self.active_until_batches <= 0 and day >= self.next_exercise_day

    def start_exercise(self, day: int) -> None:
        self.active_until_batches = 1
        self.next_exercise_day = day + max(round(self.exercise_interval_days), 1)
