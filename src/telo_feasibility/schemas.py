"""Typed schemas for every entity, parameter, gate, configuration, manifest, and result.

Validation policy (protocol 5.4, 9.2, 4.4; task spec section 9):

* Every numeric parameter carries units from a controlled vocabulary. Units map to
  a dimension, and the dimension fixes the admissible range: fractions and
  probabilities in [0, 1]; money, time, rates, and counts non-negative.
* Every parameter carries provenance. Tiers 1-4 require at least one source id and
  an access date. Tier 5 (illustrative) is legal only with
  ``validation_status == "illustrative"``.
* Dates must be real calendar dates between 1990-01-01 and today.
* A regulatory gate can be ``PASS`` only with a named reviewer and a review date.
  ``UNCERTAIN`` is never coerced to ``PASS`` anywhere.
* Release-assurance scenario R3 is representable only on strategy S6 and is
  still subject to runtime gate checks in ``regulatory.py``.

The models are plain data; behavior lives in the other modules.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from enum import IntEnum, StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Controlled vocabularies
# ---------------------------------------------------------------------------


class Dimension(StrEnum):
    UNIT_INTERVAL = "unit_interval"  # fractions, probabilities, yields
    NONNEG_REAL = "nonneg_real"  # money, time, rates, quantities
    NONNEG_INT = "nonneg_int"  # counts
    MULTIPLIER = "multiplier"  # dimensionless positive scale factors
    SIGNED_REAL = "signed_real"  # growth rates, differences


class Unit(StrEnum):
    FRACTION = "fraction"
    PROBABILITY = "probability"
    COUNT = "count"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"
    PER_YEAR = "per_year"
    PER_SITE_YEAR = "per_site_year"
    DAYS_PER_BATCH = "days_per_batch"
    USD = "usd"
    USD_PER_UNIT = "usd_per_unit"
    USD_PER_BATCH = "usd_per_batch"
    USD_PER_YEAR = "usd_per_year"
    USD_PER_SITE_YEAR = "usd_per_site_year"
    UNITS = "units"
    UNITS_PER_BATCH = "units_per_batch"
    UNITS_PER_YEAR = "units_per_year"
    UNITS_PER_DAY = "units_per_day"
    MULTIPLIER = "multiplier"
    ANNUAL_RATE = "annual_rate"  # discount / carrying / growth; may be negative for growth
    ML = "ml"
    MG_PER_ML = "mg_per_ml"
    PERCENT_WV = "percent_w_v"


UNIT_DIMENSION: dict[Unit, Dimension] = {
    Unit.FRACTION: Dimension.UNIT_INTERVAL,
    Unit.PROBABILITY: Dimension.UNIT_INTERVAL,
    Unit.COUNT: Dimension.NONNEG_INT,
    Unit.DAYS: Dimension.NONNEG_REAL,
    Unit.MONTHS: Dimension.NONNEG_REAL,
    Unit.YEARS: Dimension.NONNEG_REAL,
    Unit.PER_YEAR: Dimension.NONNEG_REAL,
    Unit.PER_SITE_YEAR: Dimension.NONNEG_REAL,
    Unit.DAYS_PER_BATCH: Dimension.NONNEG_REAL,
    Unit.USD: Dimension.NONNEG_REAL,
    Unit.USD_PER_UNIT: Dimension.NONNEG_REAL,
    Unit.USD_PER_BATCH: Dimension.NONNEG_REAL,
    Unit.USD_PER_YEAR: Dimension.NONNEG_REAL,
    Unit.USD_PER_SITE_YEAR: Dimension.NONNEG_REAL,
    Unit.UNITS: Dimension.NONNEG_REAL,
    Unit.UNITS_PER_BATCH: Dimension.NONNEG_REAL,
    Unit.UNITS_PER_YEAR: Dimension.NONNEG_REAL,
    Unit.UNITS_PER_DAY: Dimension.NONNEG_REAL,
    Unit.MULTIPLIER: Dimension.MULTIPLIER,
    Unit.ANNUAL_RATE: Dimension.SIGNED_REAL,
    Unit.ML: Dimension.NONNEG_REAL,
    Unit.MG_PER_ML: Dimension.NONNEG_REAL,
    Unit.PERCENT_WV: Dimension.NONNEG_REAL,
}


class EvidenceTier(IntEnum):
    OFFICIAL = 1
    DIRECT_OPERATIONAL = 2
    PEER_REVIEWED = 3
    EXPERT_ELICITATION = 4
    ILLUSTRATIVE = 5


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationStatus(StrEnum):
    SOURCED = "sourced"
    EXPERT_VALIDATED = "expert_validated"
    ILLUSTRATIVE = "illustrative"
    MISSING = "missing"


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNCERTAIN = "UNCERTAIN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Eligibility(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    EXCLUDED = "EXCLUDED"
    NO_CONCLUSION = "NO_CONCLUSION"


class Pathway(StrEnum):
    APPROVED_CMO = "approved_cmo"
    P503B = "503b"
    DISTRIBUTED = "distributed"
    RELEASE_ASSURANCE = "release_assurance"


class LegalBasisType(StrEnum):
    LAW_OR_REGULATION = "law_or_regulation"
    FINAL_GUIDANCE = "final_guidance"
    AGENCY_INITIATIVE = "agency_initiative"
    PROPOSED_RULE = "proposed_rule"
    EXPERT_INTERPRETATION = "expert_interpretation"
    UNRESOLVED_QUESTION = "unresolved_question"


class GateTreatment(StrEnum):
    EXCLUDE_IF_FAIL = "exclude_if_fail"
    LEAD_TIME = "lead_time"
    HARD_FEASIBILITY = "hard_feasibility"
    CAP = "cap"
    DYNAMIC_STATE = "dynamic_state"
    REGION_RESTRICTION = "region_restriction"
    FALLBACK_CONVENTIONAL = "fallback_conventional"
    NO_FLEET_CLAIM = "no_fleet_claim"


class StrategyId(StrEnum):
    """S0-S7 are the frozen protocol comparators; S8+ are design-space strategies (2026-09)."""

    S0 = "S0"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"
    S6 = "S6"
    S7 = "S7"
    S8 = "S8"
    S9 = "S9"
    S10 = "S10"
    S11 = "S11"
    S12 = "S12"
    S13 = "S13"
    S14 = "S14"
    S15 = "S15"
    S16 = "S16"
    S17 = "S17"
    S18 = "S18"
    S19 = "S19"
    S20 = "S20"

    @property
    def is_frozen(self) -> bool:
        return self in FROZEN_STRATEGY_IDS


FROZEN_STRATEGY_IDS: tuple[StrategyId, ...] = (
    StrategyId.S0,
    StrategyId.S1,
    StrategyId.S2,
    StrategyId.S3,
    StrategyId.S4,
    StrategyId.S5,
    StrategyId.S6,
    StrategyId.S7,
)


class ReleaseScenario(StrEnum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"


class DistributionFamily(StrEnum):
    POINT = "point"
    UNIFORM = "uniform"
    TRIANGULAR = "triangular"
    PERT = "pert"
    LOGNORMAL = "lognormal"
    NORMAL_TRUNCATED = "normal_truncated"
    BETA = "beta"
    GAMMA = "gamma"
    POISSON = "poisson"
    NEGATIVE_BINOMIAL = "negative_binomial"
    BERNOULLI = "bernoulli"
    EMPIRICAL = "empirical"
    BLOCK_BOOTSTRAP = "block_bootstrap"


class ComponentKind(StrEnum):
    API = "api"
    EXCIPIENT = "excipient"
    VIAL = "vial"
    STOPPER = "stopper"
    SEAL = "seal"
    LABEL = "label"
    PACKAGING = "packaging"
    REFERENCE_STANDARD = "reference_standard"
    TESTING_MATERIAL = "testing_material"
    OTHER = "other"


class BatchStage(StrEnum):
    SETUP = "setup"
    PRODUCTION = "production"
    INSPECTION = "inspection"
    TESTING = "testing"
    INVESTIGATION = "investigation"
    RELEASED = "released"
    REJECTED = "rejected"


class LotStatus(StrEnum):
    RELEASED = "released"
    HOLD = "hold"
    QUARANTINE = "quarantine"
    EXPIRED = "expired"


class DisruptionKind(StrEnum):
    SITE_FAILURE = "site_failure"
    SUPPLIER = "supplier"
    COMMON_CAUSE = "common_cause"
    DEMAND_SHOCK = "demand_shock"
    REGULATORY = "regulatory"
    TRANSPORT = "transport"
    QUALITY = "quality"


class RandomStream(StrEnum):
    ROUTINE_DEMAND = "routine_demand"
    DEMAND_SHOCKS = "demand_shocks"
    SITE_FAILURES = "site_failures"
    SUPPLIER_DISRUPTIONS = "supplier_disruptions"
    COMMON_CAUSE_EVENTS = "common_cause_events"
    YIELD = "yield"
    DEVIATIONS = "deviations"
    BATCH_REJECTION = "batch_rejection"
    RELEASE_TIME = "release_time"
    TRANSPORT_DELAY = "transport_delay"
    REGULATORY_STATE_TRANSITIONS = "regulatory_state_transitions"
    ACTIVATION = "activation"  # appended 2026-09-02; earlier indices unchanged (CRN preserved)


STREAM_INDEX: dict[RandomStream, int] = {s: i for i, s in enumerate(RandomStream)}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MIN_DATE = date(1990, 1, 1)


def _check_date(d: date | None, field_name: str) -> date | None:
    if d is None:
        return None
    if d < MIN_DATE:
        raise ValueError(f"{field_name}: {d.isoformat()} is before {MIN_DATE.isoformat()}")
    if d > date.today():
        raise ValueError(f"{field_name}: {d.isoformat()} is in the future")
    return d


def _check_dimension(value: float | None, unit: Unit, field_name: str) -> None:
    if value is None:
        return
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        raise ValueError(f"{field_name}: non-finite value {value!r}")
    dim = UNIT_DIMENSION[unit]
    if dim is Dimension.UNIT_INTERVAL and not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name}: {value!r} outside [0, 1] for unit {unit.value}")
    if dim in (Dimension.NONNEG_REAL, Dimension.NONNEG_INT) and value < 0:
        raise ValueError(f"{field_name}: negative value {value!r} for unit {unit.value}")
    if dim is Dimension.NONNEG_INT and float(value) != int(value):
        raise ValueError(f"{field_name}: non-integer count {value!r}")
    if dim is Dimension.MULTIPLIER and value <= 0:
        raise ValueError(f"{field_name}: multiplier must be positive, got {value!r}")


class StrictModel(BaseModel):
    """Base: unknown fields are errors, assignment is validated, enums stay enums."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, frozen=False)


# ---------------------------------------------------------------------------
# Evidence and parameters
# ---------------------------------------------------------------------------


class EvidenceSource(StrictModel):
    id: str = Field(pattern=r"^S\d{2,3}$")
    name: str
    domain: str
    url: str | None = None
    tier: EvidenceTier
    access_date: date | None = None
    use_in_model: str = ""
    limitation: str = ""
    license_note: str = ""
    status: str = Field(default="use", pattern=r"^(use|conditional|human_required|retired)$")

    @field_validator("access_date")
    @classmethod
    def _v_date(cls, v: date | None) -> date | None:
        return _check_date(v, "access_date")


class Distribution(StrictModel):
    """A sampling distribution with explicit physical support.

    ``params`` holds family-specific parameters (e.g. ``mu``, ``sigma`` for lognormal;
    ``a``, ``b`` for beta; ``lam`` for poisson; ``p`` for bernoulli; ``values`` and
    ``block_length`` for bootstrap). ``support`` bounds every sample and is checked
    against the owning parameter's dimension.
    """

    family: DistributionFamily
    params: dict[str, Any] = Field(default_factory=dict)
    support: tuple[float, float] = (0.0, math.inf)

    @model_validator(mode="after")
    def _v_support(self) -> Distribution:
        lo, hi = self.support
        if not lo <= hi:
            raise ValueError(f"support lower {lo} exceeds upper {hi}")
        required: dict[DistributionFamily, tuple[str, ...]] = {
            DistributionFamily.POINT: ("value",),
            DistributionFamily.UNIFORM: ("low", "high"),
            DistributionFamily.TRIANGULAR: ("low", "mode", "high"),
            DistributionFamily.PERT: ("low", "mode", "high"),
            DistributionFamily.LOGNORMAL: ("median", "sigma"),
            DistributionFamily.NORMAL_TRUNCATED: ("mean", "sd"),
            DistributionFamily.BETA: ("a", "b"),
            DistributionFamily.GAMMA: ("shape", "scale"),
            DistributionFamily.POISSON: ("lam",),
            DistributionFamily.NEGATIVE_BINOMIAL: ("mean", "dispersion"),
            DistributionFamily.BERNOULLI: ("p",),
            DistributionFamily.EMPIRICAL: ("values",),
            DistributionFamily.BLOCK_BOOTSTRAP: ("values", "block_length"),
        }
        missing = [k for k in required[self.family] if k not in self.params]
        if missing:
            raise ValueError(f"{self.family.value} distribution missing params {missing}")
        if (
            self.family is DistributionFamily.BERNOULLI
            and not 0.0 <= float(self.params["p"]) <= 1.0
        ):
            raise ValueError("bernoulli p outside [0, 1]")
        for k in ("sigma", "sd", "scale", "shape", "a", "b", "lam", "dispersion"):
            if k in self.params and float(self.params[k]) < 0:
                raise ValueError(f"{self.family.value} parameter {k} negative")
        return self


class UncertainParameter(StrictModel):
    """One model input with full provenance (protocol 5.4)."""

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
    definition: str
    units: Unit
    entity_level: str = Field(
        pattern=r"^(global|product|product_region|region|site|supplier|component|strategy|batch|event|shipment|network|site_month|order)$"
    )
    low: float | None = None
    base: float | None = None
    high: float | None = None
    distribution: Distribution | None = None
    bounds: tuple[float, float] | None = None
    dependence_group: str | None = None
    source_ids: list[str] = Field(default_factory=list)
    source_locator: str = ""
    access_date: date | None = None
    transformation: str = ""
    evidence_tier: EvidenceTier
    confidence: Confidence
    validation_status: ValidationStatus
    revision: str = "R000"
    owner: str = ""
    outputs_it_can_reverse: list[str] = Field(default_factory=list)
    notes: str = ""

    @field_validator("access_date")
    @classmethod
    def _v_date(cls, v: date | None) -> date | None:
        return _check_date(v, "access_date")

    @model_validator(mode="after")
    def _v_all(self) -> UncertainParameter:
        name = f"parameter {self.id}"
        for label, v in (("low", self.low), ("base", self.base), ("high", self.high)):
            _check_dimension(v, self.units, f"{name}.{label}")
        if self.low is not None and self.base is not None and self.low > self.base:
            raise ValueError(f"{name}: low {self.low} > base {self.base}")
        if self.base is not None and self.high is not None and self.base > self.high:
            raise ValueError(f"{name}: base {self.base} > high {self.high}")
        if self.bounds is not None:
            lo, hi = self.bounds
            if lo > hi:
                raise ValueError(f"{name}: bounds lower {lo} > upper {hi}")
            for label, v in (("low", self.low), ("base", self.base), ("high", self.high)):
                if v is not None and not lo <= v <= hi:
                    raise ValueError(f"{name}.{label}={v} outside bounds {self.bounds}")
        if self.distribution is not None:
            dlo, dhi = self.distribution.support
            dim = UNIT_DIMENSION[self.units]
            if dim is Dimension.UNIT_INTERVAL and (dlo < 0.0 or dhi > 1.0):
                raise ValueError(
                    f"{name}: distribution support {self.distribution.support} exceeds [0, 1]"
                )
            if (
                dim in (Dimension.NONNEG_REAL, Dimension.NONNEG_INT, Dimension.MULTIPLIER)
                and dlo < 0.0
            ):
                raise ValueError(
                    f"{name}: distribution support below zero for unit {self.units.value}"
                )
        # provenance rules
        if self.validation_status is ValidationStatus.MISSING:
            if (
                any(v is not None for v in (self.low, self.base, self.high))
                or self.distribution is not None
            ):
                raise ValueError(f"{name}: status 'missing' but a value is present")
            return self
        if self.base is None and self.distribution is None:
            raise ValueError(f"{name}: no base value and no distribution")
        if self.evidence_tier is EvidenceTier.ILLUSTRATIVE:
            if self.validation_status is not ValidationStatus.ILLUSTRATIVE:
                raise ValueError(f"{name}: tier 5 requires validation_status 'illustrative'")
        else:
            if not self.source_ids:
                raise ValueError(
                    f"{name}: tier {int(self.evidence_tier)} requires at least one source id"
                )
            if self.access_date is None:
                raise ValueError(f"{name}: tier {int(self.evidence_tier)} requires an access date")
            if self.validation_status is ValidationStatus.ILLUSTRATIVE:
                raise ValueError(
                    f"{name}: tier {int(self.evidence_tier)} cannot be marked illustrative"
                )
        return self

    @property
    def is_illustrative(self) -> bool:
        return self.evidence_tier is EvidenceTier.ILLUSTRATIVE


class ParameterSet(StrictModel):
    """A named collection of parameters (one config file)."""

    id: str
    description: str = ""
    parameters: dict[str, UncertainParameter]

    @model_validator(mode="after")
    def _v_keys(self) -> ParameterSet:
        for key, p in self.parameters.items():
            if key != p.id:
                raise ValueError(f"parameter key {key!r} does not match id {p.id!r}")
        return self

    def illustrative_ids(self) -> list[str]:
        return sorted(k for k, p in self.parameters.items() if p.is_illustrative)

    def missing_ids(self) -> list[str]:
        return sorted(
            k for k, p in self.parameters.items() if p.validation_status is ValidationStatus.MISSING
        )

    def base(self, key: str) -> float:
        p = self.parameters[key]
        if p.base is None:
            raise KeyError(f"parameter {key} has no base value")
        return p.base


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------


class ProductPresentation(StrictModel):
    """An exact presentation (protocol 1.2): strength, form, route, container, fill, label."""

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    ingredient: str
    salt_or_form: str = ""
    strength: str
    dosage_form: str
    route: str
    presentation: str
    container: str
    fill_volume_ml: float | None = Field(default=None, ge=0)
    labels: list[str] = Field(default_factory=list, description="DailyMed set ids or NDCs")
    # archetype flags (protocol 2.1)
    controlled_substance: bool
    small_molecule: bool
    aqueous_solution: bool
    standard_vial: bool
    lyophilized: bool
    suspension_or_emulsion: bool
    biologic_or_vaccine: bool
    cytotoxic_or_high_potency: bool
    drug_device_combination: bool
    cold_chain_intensive: bool
    out_of_archetype_comparator: bool = False
    pathway_candidates: list[Pathway] = Field(default_factory=list)
    parameters: ParameterSet | None = None
    notes: str = ""

    @property
    def archetype_fit(self) -> bool:
        return (
            not self.controlled_substance
            and self.small_molecule
            and self.aqueous_solution
            and self.standard_vial
            and not self.lyophilized
            and not self.suspension_or_emulsion
            and not self.biologic_or_vaccine
            and not self.cytotoxic_or_high_potency
            and not self.drug_device_combination
            and not self.cold_chain_intensive
        )

    @model_validator(mode="after")
    def _v_archetype(self) -> ProductPresentation:
        if not self.archetype_fit and not self.out_of_archetype_comparator:
            raise ValueError(
                f"product {self.id} violates the first archetype; set out_of_archetype_comparator=True to keep it as an explicit comparator"
            )
        return self


class Component(StrictModel):
    id: str
    name: str
    kind: ComponentKind
    supplier_ids: list[str] = Field(default_factory=list)
    quantity_per_unit: float = Field(
        ge=0, description="component quantity per finished unit, in the component's own unit"
    )
    quantity_unit: str = "each"


class Supplier(StrictModel):
    id: str
    name: str
    component_ids: list[str]
    lead_time_days: UncertainParameter
    capacity_units_per_year: float | None = Field(default=None, ge=0)
    qualified_at_t0: bool = True
    qualification_lead_time_days: float = Field(default=0.0, ge=0)
    common_cause_groups: list[str] = Field(default_factory=list)
    geography: str = ""
    ownership: str = ""

    @field_validator("lead_time_days")
    @classmethod
    def _v_units(cls, v: UncertainParameter) -> UncertainParameter:
        if v.units is not Unit.DAYS:
            raise ValueError("supplier lead time must be in days")
        return v


class ManufacturingSite(StrictModel):
    id: str
    name: str
    region_id: str
    archetype: str = Field(pattern=r"^(central|regional_node|cdmo_reserved|503b)$")
    batch_size_units: float = Field(gt=0)
    batches_per_year_nominal: float = Field(ge=0)
    yield_fraction: float = Field(ge=0, le=1)
    uptime_fraction: float = Field(ge=0, le=1)
    production_cycle_days: float = Field(ge=0)
    changeover_days: float = Field(ge=0)
    release_time_components_days: dict[str, float]
    capital_usd: float = Field(ge=0)
    fixed_cost_usd_per_year: float = Field(ge=0)
    validation_cost_usd: float = Field(ge=0)
    commissioning_lead_time_days: float = Field(ge=0)
    exists_at_t0: bool = True
    pathway: Pathway = Pathway.APPROVED_CMO
    common_cause_groups: list[str] = Field(default_factory=list)
    supplier_ids: list[str] = Field(default_factory=list)

    @field_validator("release_time_components_days")
    @classmethod
    def _v_components(cls, v: dict[str, float]) -> dict[str, float]:
        for k, d in v.items():
            if d < 0:
                raise ValueError(f"release component {k} negative")
        return v

    @property
    def release_time_days(self) -> float:
        """Conventional release time: the longest component when they run concurrently.

        The protocol's Eq. 5 warns that terms overlap only where operationally valid;
        release components (sterility incubation, EM, assay, endotoxin, QA) start
        together after fill, so the critical path is their maximum plus any serial
        QA component recorded under ``qa_review_serial``.
        """
        comps = dict(self.release_time_components_days)
        serial = comps.pop("qa_review_serial", 0.0)
        return (max(comps.values()) if comps else 0.0) + serial


class Batch(StrictModel):
    id: str
    site_id: str
    product_id: str
    ordinal: int = Field(ge=0)
    size_units: float = Field(ge=0)
    start_day: int = Field(ge=0)
    stage: BatchStage = BatchStage.SETUP
    yield_fraction: float | None = Field(default=None, ge=0, le=1)
    rejected: bool = False
    abstained: bool = False
    released_day: int | None = None
    hold_reason: str = ""


class InventoryLot(StrictModel):
    id: str
    product_id: str
    location_id: str
    units: float = Field(ge=0)
    release_day: int = Field(ge=0)
    expiry_day: int = Field(ge=0)
    status: LotStatus = LotStatus.RELEASED

    @model_validator(mode="after")
    def _v_expiry(self) -> InventoryLot:
        if self.expiry_day < self.release_day:
            raise ValueError(f"lot {self.id}: expiry day before release day")
        return self


class DemandRegion(StrictModel):
    id: str
    name: str
    share: float = Field(ge=0, le=1)
    criticality_weight: float = Field(default=1.0, ge=0)
    minimum_guarantee_fraction: float = Field(default=0.0, ge=0, le=1)


class TransportLane(StrictModel):
    id: str
    origin_id: str
    destination_region_id: str
    days: float = Field(ge=0)
    cost_usd_per_unit: float = Field(ge=0)
    emergency_days: float | None = Field(default=None, ge=0)
    emergency_cost_usd_per_unit: float | None = Field(default=None, ge=0)


class CommonCauseGroup(StrictModel):
    id: str
    kind: str = Field(
        pattern=r"^(api_supplier|excipient_supplier|vial_supplier|stopper_seal_supplier|laboratory|reference_standard|analytical_method|shared_equipment|software_model_version|geography|utility|ownership|regulatory_action|other)$"
    )
    member_ids: list[str]
    description: str = ""


class DisruptionEvent(StrictModel):
    id: str
    kind: DisruptionKind
    target_ids: list[str]
    start_day: int = Field(ge=0)
    duration_days: int = Field(ge=0)
    capacity_fraction_remaining: float = Field(default=0.0, ge=0, le=1)
    magnitude: float = Field(
        default=1.0, ge=0, description="demand multiplier for shocks; 1 = none"
    )
    common_cause_group_id: str | None = None

    @property
    def end_day(self) -> int:
        return self.start_day + self.duration_days


# ---------------------------------------------------------------------------
# Regulatory gates
# ---------------------------------------------------------------------------


class RegulatoryGate(StrictModel):
    id: str = Field(pattern=r"^G\d{2}$")
    pathway: Pathway
    name: str
    evidence_required: str
    model_effect: str
    treatment: GateTreatment
    applies_to_strategies: list[StrategyId]
    protocol_ref: str = ""
    legal_basis_type: LegalBasisType
    legal_basis: str = ""
    sources: list[str] = Field(default_factory=list)
    status: GateStatus = GateStatus.UNCERTAIN
    reviewer: str | None = None
    review_date: date | None = None
    notes: str | None = None

    @field_validator("review_date")
    @classmethod
    def _v_date(cls, v: date | None) -> date | None:
        return _check_date(v, "review_date")

    @model_validator(mode="after")
    def _v_pass_requires_review(self) -> RegulatoryGate:
        if self.status in (GateStatus.PASS, GateStatus.FAIL) and (
            not self.reviewer or self.review_date is None
        ):
            raise ValueError(
                f"gate {self.id}: status {self.status.value} requires a named reviewer and a review date"
            )
        return self


class GateSet(StrictModel):
    version: str
    label: str
    statuses: list[GateStatus]
    treatments: dict[str, str]
    gates: list[RegulatoryGate]

    @model_validator(mode="after")
    def _v_unique(self) -> GateSet:
        ids = [g.id for g in self.gates]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate gate ids")
        return self

    def by_id(self, gate_id: str) -> RegulatoryGate:
        for g in self.gates:
            if g.id == gate_id:
                return g
        raise KeyError(gate_id)

    def for_strategy(self, strategy: StrategyId) -> list[RegulatoryGate]:
        return [g for g in self.gates if strategy in g.applies_to_strategies]


# ---------------------------------------------------------------------------
# Strategies, configuration, manifests, results
# ---------------------------------------------------------------------------


class SitePlanSpec(StrictModel):
    """One site of a design-space strategy (S8+), declared in configuration.

    ``scale`` multiplies the product's nominal batches per site-year (scheduling capacity);
    ``batch_size_fraction`` multiplies units per batch (defaults to ``scale`` for regional
    nodes and to 1 for central-type sites, as in the frozen builder). ``serves`` is
    ``all`` regions or the site's ``own_region``. Reserved sites idle until activated;
    ``exercise_batches_per_year`` keeps a warm-standby line validated by running real
    batches on a fixed cadence, and ``activation_failure_probability`` is the chance an
    activation request fails and must be re-issued after the activation lead time.
    ``portfolio_capacity_share`` and ``portfolio_fixed_cost_share`` model a multi-product
    node: only that share of scheduling capacity and of fixed, capital, and validation
    cost is attributed to this product.
    """

    # region-suffixed ids such as node_R2 are allowed so a declared plan can reuse a frozen
    # roster entity (same id, same entity-keyed random streams)
    id: str = Field(pattern=r"^[a-z][A-Za-z0-9_]*$")
    region_id: str
    archetype: str = Field(pattern=r"^(central|regional_node|cdmo_reserved|503b)$")
    scale: float = Field(gt=0)
    batch_size_fraction: float | None = Field(default=None, gt=0)
    exists_at_t0: bool = True
    commissioning_days: float | None = Field(default=None, ge=0)
    api_supplier: str = "api_1"
    vial_supplier: str = "vial_1"
    stopper_supplier: str = "stopper_1"
    pathway: Pathway = Pathway.APPROVED_CMO
    reserved: bool = False
    groups: list[str] = Field(default_factory=list)
    serves: str = Field(default="all", pattern=r"^(all|own_region)$")
    exercise_batches_per_year: float = Field(default=0.0, ge=0)
    activation_failure_probability: float = Field(default=0.0, ge=0, le=1)
    activation_lead_days: float | None = Field(default=None, ge=0)
    portfolio_capacity_share: float = Field(default=1.0, gt=0, le=1)
    portfolio_fixed_cost_share: float = Field(default=1.0, gt=0, le=1)
    capital_multiplier: float = Field(default=1.0, ge=0)
    fixed_cost_multiplier: float = Field(default=1.0, ge=0)
    validation_multiplier: float = Field(default=1.0, ge=0)

    @model_validator(mode="after")
    def _v_reserved(self) -> SitePlanSpec:
        if not self.reserved and (
            self.exercise_batches_per_year > 0 or self.activation_failure_probability > 0
        ):
            raise ValueError(f"site {self.id}: exercise and activation fields need reserved=true")
        if self.pathway is Pathway.P503B and self.archetype != "503b":
            raise ValueError(f"site {self.id}: 503b pathway requires the 503b archetype")
        return self


class SupplierSpec(StrictModel):
    """An additional supplier a design-space strategy introduces (e.g. a hub supplying bulk).

    ``lead_time_days`` is absolute; ``lead_time_factor`` scales the product's material lead
    time instead. Exactly one of the two must be given.
    """

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    name: str
    component_ids: list[str]
    lead_time_days: float | None = Field(default=None, ge=0)
    lead_time_factor: float | None = Field(default=None, ge=0)
    groups: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _v_lead(self) -> SupplierSpec:
        if (self.lead_time_days is None) == (self.lead_time_factor is None):
            raise ValueError(f"supplier {self.id}: give lead_time_days or lead_time_factor")
        return self


class DesignVariableSpec(StrictModel):
    """Search bounds for one design variable (bounds are search bounds, not evidence)."""

    name: str
    low: float
    high: float
    kind: str = Field(default="float", pattern=r"^(float|int)$")
    grid: int = Field(default=3, ge=1)

    @model_validator(mode="after")
    def _v_bounds(self) -> DesignVariableSpec:
        if self.high < self.low:
            raise ValueError(f"design variable {self.name}: high < low")
        return self


class StrategyProfile(StrictModel):
    """The formal description the design-space assignment requires for every strategy."""

    family: str
    product_archetype: str
    asset_ownership: str
    sites_summary: str
    regulatory_owner: str
    quality_owner: str
    supplier_graph: str
    material_flow: str
    production_steps: str
    release_pathway: str
    inventory_policy: str
    allocation_policy: str
    customer: str
    revenue_mechanism: str
    contracting_requirement: str
    capital_requirement: str
    implementation_lead_time: str
    regulatory_gates: list[str]
    dominant_risks: str
    potential_moat: str
    falsification_test: str


class StrategyDesign(StrictModel):
    id: StrategyId
    name: str
    pathway: Pathway
    durable: bool
    design_variables: dict[str, float] = Field(default_factory=dict)
    release_scenario: ReleaseScenario = ReleaseScenario.R0
    allocation_policy: str = Field(
        default="proportional",
        pattern=r"^(proportional|criticality_weighted|minimum_guarantee|optimization)$",
    )
    notes: str = ""
    # design-space strategies (S8+) declare their topology and search space in configuration
    family: str = ""
    site_plans: list[SitePlanSpec] | None = None
    extra_suppliers: list[SupplierSpec] = Field(default_factory=list)
    design_space: list[DesignVariableSpec] = Field(default_factory=list)
    profile: StrategyProfile | None = None

    @model_validator(mode="after")
    def _v_release(self) -> StrategyDesign:
        frozen = self.id.is_frozen
        if self.release_scenario is ReleaseScenario.R3 and frozen and self.id is not StrategyId.S6:
            raise ValueError("release scenario R3 is representable only on strategy S6 among S0-S7")
        if self.id is StrategyId.S7 and self.pathway is not Pathway.P503B:
            raise ValueError("S7 must use the 503b pathway")
        if frozen and self.id is not StrategyId.S7 and self.pathway is Pathway.P503B:
            raise ValueError("only S7 may use the 503b pathway among S0-S7")
        if self.pathway is Pathway.P503B and self.durable:
            raise ValueError("a 503b-pathway strategy is not a durable architecture")
        if frozen and self.site_plans is not None:
            raise ValueError("S0-S7 topologies are frozen in code; site_plans is for S8+")
        if not frozen and not self.site_plans:
            raise ValueError(f"{self.id.value}: design-space strategies must declare site_plans")
        if self.site_plans is not None:
            ids = [sp.id for sp in self.site_plans]
            if len(ids) != len(set(ids)):
                raise ValueError("duplicate site plan ids")
        for k, v in self.design_variables.items():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                raise ValueError(f"design variable {k} non-finite")
        return self


class ServiceThresholds(StrictModel):
    fill_rate_mean_min: float = Field(ge=0, le=1)
    fill_rate_tail_confidence: float = Field(ge=0, le=1)
    shortage_day_threshold: float = Field(ge=0, le=1)
    max_expected_shortage_days_per_year: float | None = Field(default=None, ge=0)
    max_regional_fill_rate_disparity: float | None = Field(default=None, ge=0, le=1)
    recovery_time_constraint_days: float | None = Field(default=None, ge=0)
    recovery_window_days: int = Field(ge=1)


class SimulationConfig(StrictModel):
    id: str
    master_seed: int = Field(ge=0)
    n_runs: int = Field(ge=1)
    horizon_days: int = Field(ge=1)
    warm_up_days: int = Field(ge=0)
    time_step_days: int = Field(default=1, ge=1, le=7)
    n_regions: int = Field(ge=1)
    thresholds: ServiceThresholds
    streams: list[RandomStream] = Field(default_factory=lambda: list(RandomStream))
    illustrative: bool = Field(
        description="True when any tier-5 input is in use; forces the banner"
    )
    product_ids: list[str]
    strategy_ids: list[StrategyId]
    record_event_log: bool = True

    @model_validator(mode="after")
    def _v_streams(self) -> SimulationConfig:
        if set(self.streams) != set(RandomStream):
            raise ValueError(
                "all random streams must be declared so that common random numbers are complete"
            )
        return self


class SnapshotManifest(StrictModel):
    """Frozen raw snapshot of an official source (task spec section 5)."""

    source_id: str
    url: str
    retrieved_at: datetime
    http_status: int | None = Field(default=None, ge=100, le=599)
    sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    content_type: str = ""
    size_bytes: int | None = Field(default=None, ge=0)
    license_note: str
    raw_path: str | None = None
    transform_script: str | None = None
    processed_path: str | None = None
    data_dictionary_rows: int = Field(default=0, ge=0)
    access_method: str = Field(pattern=r"^(auto|human)$")
    robots_allowed: bool | None = None
    notes: str = ""

    @model_validator(mode="after")
    def _v_auto_complete(self) -> SnapshotManifest:
        if self.access_method == "auto":
            missing = [
                k
                for k, v in (
                    ("http_status", self.http_status),
                    ("sha256", self.sha256),
                    ("raw_path", self.raw_path),
                    ("size_bytes", self.size_bytes),
                )
                if v is None
            ]
            if missing:
                raise ValueError(f"auto snapshot for {self.source_id} missing {missing}")
        return self


class RunManifest(StrictModel):
    run_id: str
    created_at: datetime
    protocol_version: str
    protocol_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    package_version: str
    git_commit: str | None = None
    git_dirty: bool | None = None
    python_version: str
    platform: str
    config_hashes: dict[str, str]
    master_seed: int | None = None
    n_runs: int | None = None
    illustrative: bool
    gate_outcomes: dict[str, dict[str, str]] = Field(default_factory=dict)
    wall_time_s: float | None = Field(default=None, ge=0)
    notes: str = ""


class ResultRecord(StrictModel):
    run_id: str
    run_index: int = Field(ge=0)
    product_id: str
    strategy_id: StrategyId
    design_id: str
    release_scenario: ReleaseScenario
    eligibility: Eligibility
    illustrative: bool
    metrics: dict[str, float]

    @field_validator("metrics")
    @classmethod
    def _v_metrics(cls, v: dict[str, float]) -> dict[str, float]:
        for k, x in v.items():
            if isinstance(x, float) and math.isnan(x):
                raise ValueError(f"metric {k} is NaN")
        return v


# ---------------------------------------------------------------------------
# Protocol (decision-relevant subset, typed; narrative fields allowed through)
# ---------------------------------------------------------------------------


class ProtocolSourceDocument(StrictModel):
    id: str
    filename: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)
    version_string: str
    role: str
    pages: int | None = None
    caution: str | None = None


class ProtocolHeader(StrictModel):
    id: str
    title: str
    subtitle: str = ""
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    status: str = Field(pattern=r"^(frozen|draft)$")
    frozen_on: date
    machine_readable_created_on: date
    label: str
    designed_to_permit_negative_conclusion: bool
    source_documents: list[ProtocolSourceDocument]
    change_log: str


class ProductSelectionSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    longlist_minimum: int = Field(ge=1)
    weights: dict[str, float]
    score_scale: dict[str, Any]

    @model_validator(mode="after")
    def _v_weights(self) -> ProductSelectionSpec:
        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"selection weights sum to {total}, not 1.0")
        if any(w < 0 for w in self.weights.values()):
            raise ValueError("negative selection weight")
        return self


class ProtocolStrategy(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: StrategyId
    name: str
    durable: bool
    pathway: str


class Protocol(BaseModel):
    """Typed view of protocol/protocol.yaml. Narrative sections pass through untyped."""

    model_config = ConfigDict(extra="allow")
    protocol: ProtocolHeader
    central_question: str
    product_selection: ProductSelectionSpec
    strategies: list[ProtocolStrategy]
    service_thresholds: ServiceThresholds
    recovery_definition: dict[str, Any]
    model_horizon: dict[str, Any]
    regulatory_gates_file: str

    @model_validator(mode="after")
    def _v_strategies(self) -> Protocol:
        ids = [s.id for s in self.strategies]
        if ids != list(FROZEN_STRATEGY_IDS):
            raise ValueError(
                f"protocol strategies must be S0..S7 in order, got {[i.value for i in ids]}"
            )
        durable = {s.id for s in self.strategies if s.durable}
        if StrategyId.S7 in durable:
            raise ValueError("S7 must not be durable")
        rw = int(self.recovery_definition.get("recovery_window_days", -1))
        if rw != self.service_thresholds.recovery_window_days:
            raise ValueError(
                "recovery_window_days differs between recovery_definition and service_thresholds"
            )
        return self

    @property
    def version(self) -> str:
        return self.protocol.version
