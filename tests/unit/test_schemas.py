"""Schema validation: units, ranges, dates, provenance, gates, strategies."""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from telo_feasibility.schemas import (
    Distribution,
    DistributionFamily,
    EvidenceTier,
    GateStatus,
    GateTreatment,
    InventoryLot,
    LegalBasisType,
    ParameterSet,
    Pathway,
    ProductPresentation,
    RegulatoryGate,
    ReleaseScenario,
    StrategyDesign,
    StrategyId,
    Unit,
    ValidationStatus,
)

from ..conftest import make_param

# ---------------------------------------------------------------------------
# UncertainParameter
# ---------------------------------------------------------------------------


def test_fraction_outside_unit_interval_rejected() -> None:
    with pytest.raises(ValidationError, match=r"outside \[0, 1\]"):
        make_param(base=1.2, high=1.5)


def test_probability_negative_rejected() -> None:
    with pytest.raises(ValidationError):
        make_param(units=Unit.PROBABILITY, low=-0.1, base=0.2, high=0.3)


def test_negative_cost_rejected() -> None:
    with pytest.raises(ValidationError, match="negative value"):
        make_param("site.capital_usd", units=Unit.USD, low=-1.0, base=5.0, high=9.0)


def test_non_integer_count_rejected() -> None:
    with pytest.raises(ValidationError, match="non-integer count"):
        make_param("network.regions", units=Unit.COUNT, low=3, base=4.5, high=8)


def test_low_base_high_ordering_enforced() -> None:
    with pytest.raises(ValidationError, match=r"low .* > base"):
        make_param(low=0.97, base=0.96, high=0.99)
    with pytest.raises(ValidationError, match=r"base .* > high"):
        make_param(low=0.9, base=0.99, high=0.96)


def test_bounds_must_contain_values() -> None:
    with pytest.raises(ValidationError, match="outside bounds"):
        make_param(bounds=(0.95, 1.0))


def test_future_access_date_rejected() -> None:
    with pytest.raises(ValidationError, match="in the future"):
        make_param(
            tier=EvidenceTier.OFFICIAL,
            status=ValidationStatus.SOURCED,
            source_ids=["S01"],
            access_date=date.today() + timedelta(days=1),
        )


def test_ancient_access_date_rejected() -> None:
    with pytest.raises(ValidationError, match="before 1990"):
        make_param(
            tier=EvidenceTier.OFFICIAL,
            status=ValidationStatus.SOURCED,
            source_ids=["S01"],
            access_date=date(1980, 1, 1),
        )


def test_tier1_requires_source_and_date() -> None:
    with pytest.raises(ValidationError, match="requires at least one source id"):
        make_param(tier=EvidenceTier.OFFICIAL, status=ValidationStatus.SOURCED)
    with pytest.raises(ValidationError, match="requires an access date"):
        make_param(tier=EvidenceTier.OFFICIAL, status=ValidationStatus.SOURCED, source_ids=["S01"])


def test_tier5_must_be_marked_illustrative() -> None:
    with pytest.raises(ValidationError, match="tier 5 requires validation_status 'illustrative'"):
        make_param(status=ValidationStatus.SOURCED)


def test_sourced_tier_cannot_be_illustrative() -> None:
    with pytest.raises(ValidationError, match="cannot be marked illustrative"):
        make_param(
            tier=EvidenceTier.DIRECT_OPERATIONAL,
            status=ValidationStatus.ILLUSTRATIVE,
            source_ids=["S05"],
            access_date=date(2026, 9, 1),
        )


def test_missing_status_forbids_values() -> None:
    with pytest.raises(ValidationError, match="status 'missing' but a value is present"):
        make_param(
            status=ValidationStatus.MISSING,
            tier=EvidenceTier.EXPERT_ELICITATION,
            source_ids=["S04"],
            access_date=date(2026, 9, 1),
        )
    p = make_param(
        low=None,
        base=None,
        high=None,
        status=ValidationStatus.MISSING,
        tier=EvidenceTier.EXPERT_ELICITATION,
    )
    assert p.base is None


def test_distribution_support_checked_against_dimension() -> None:
    d = Distribution(
        family=DistributionFamily.LOGNORMAL,
        params={"median": 0.5, "sigma": 0.2},
        support=(0.0, 5.0),
    )
    with pytest.raises(ValidationError, match=r"exceeds \[0, 1\]"):
        make_param(distribution=d)


def test_distribution_requires_family_params() -> None:
    with pytest.raises(ValidationError, match="missing params"):
        Distribution(family=DistributionFamily.BETA, params={"a": 2.0})
    with pytest.raises(ValidationError, match=r"bernoulli p outside"):
        Distribution(family=DistributionFamily.BERNOULLI, params={"p": 1.5}, support=(0, 1))


@given(
    lo=st.floats(min_value=0.0, max_value=1.0),
    span=st.floats(min_value=0.0, max_value=1.0),
    span2=st.floats(min_value=0.0, max_value=1.0),
)
def test_property_ordered_fractions_always_load(lo: float, span: float, span2: float) -> None:
    base = min(1.0, lo + span * (1.0 - lo))
    high = min(1.0, base + span2 * (1.0 - base))
    p = make_param(low=lo, base=base, high=high)
    assert p.low is not None and p.base is not None and p.high is not None
    assert p.low <= p.base <= p.high


def test_parameter_set_keys_match_ids() -> None:
    p = make_param()
    with pytest.raises(ValidationError, match="does not match id"):
        ParameterSet(id="x", parameters={"wrong": p})
    ps = ParameterSet(id="x", parameters={p.id: p})
    assert ps.illustrative_ids() == [p.id]


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------


def _gate(**kw: object) -> RegulatoryGate:
    base: dict[str, object] = {
        "id": "G01",
        "pathway": Pathway.APPROVED_CMO,
        "name": "owner",
        "evidence_required": "x",
        "model_effect": "y",
        "treatment": GateTreatment.EXCLUDE_IF_FAIL,
        "applies_to_strategies": [StrategyId.S0],
        "legal_basis_type": LegalBasisType.LAW_OR_REGULATION,
    }
    base.update(kw)
    return RegulatoryGate.model_validate(base)


def test_gate_defaults_to_uncertain() -> None:
    assert _gate().status is GateStatus.UNCERTAIN


def test_gate_pass_requires_reviewer_and_date() -> None:
    with pytest.raises(ValidationError, match="requires a named reviewer"):
        _gate(status=GateStatus.PASS)
    with pytest.raises(ValidationError, match="requires a named reviewer"):
        _gate(status=GateStatus.FAIL, reviewer="Jane Doe, RAC")
    g = _gate(status=GateStatus.PASS, reviewer="Jane Doe, RAC", review_date=date(2026, 9, 1))
    assert g.status is GateStatus.PASS


def test_gate_status_cannot_be_flipped_to_pass_by_assignment() -> None:
    g = _gate()
    with pytest.raises(ValidationError):
        g.status = GateStatus.PASS


# ---------------------------------------------------------------------------
# Strategies and products
# ---------------------------------------------------------------------------


def test_r3_only_on_s6() -> None:
    with pytest.raises(ValidationError, match="R3 is representable only on strategy S6"):
        StrategyDesign(
            id=StrategyId.S5,
            name="d",
            pathway=Pathway.APPROVED_CMO,
            durable=True,
            release_scenario=ReleaseScenario.R3,
        )
    s = StrategyDesign(
        id=StrategyId.S6,
        name="d",
        pathway=Pathway.APPROVED_CMO,
        durable=True,
        release_scenario=ReleaseScenario.R3,
    )
    assert s.release_scenario is ReleaseScenario.R3


def test_503b_pathway_only_s7_and_not_durable() -> None:
    with pytest.raises(ValidationError, match="only S7 may use the 503b pathway"):
        StrategyDesign(id=StrategyId.S1, name="x", pathway=Pathway.P503B, durable=True)
    with pytest.raises(ValidationError, match="S7 must use the 503b pathway"):
        StrategyDesign(id=StrategyId.S7, name="x", pathway=Pathway.APPROVED_CMO, durable=False)
    with pytest.raises(ValidationError, match="not a durable architecture"):
        StrategyDesign(id=StrategyId.S7, name="x", pathway=Pathway.P503B, durable=True)


def _product(**kw: object) -> ProductPresentation:
    base: dict[str, object] = {
        "id": "sodium_bicarbonate_8_4_50ml",
        "ingredient": "sodium bicarbonate",
        "strength": "8.4% (1 mEq/mL)",
        "dosage_form": "injection, solution",
        "route": "intravenous",
        "presentation": "50 mL single-dose vial",
        "container": "glass vial",
        "fill_volume_ml": 50,
        "controlled_substance": False,
        "small_molecule": True,
        "aqueous_solution": True,
        "standard_vial": True,
        "lyophilized": False,
        "suspension_or_emulsion": False,
        "biologic_or_vaccine": False,
        "cytotoxic_or_high_potency": False,
        "drug_device_combination": False,
        "cold_chain_intensive": False,
    }
    base.update(kw)
    return ProductPresentation.model_validate(base)


def test_out_of_archetype_product_needs_explicit_flag() -> None:
    with pytest.raises(ValidationError, match="violates the first archetype"):
        _product(id="acetazolamide_500mg", lyophilized=True)
    p = _product(id="acetazolamide_500mg", lyophilized=True, out_of_archetype_comparator=True)
    assert not p.archetype_fit


def test_inventory_lot_expiry_after_release() -> None:
    with pytest.raises(ValidationError, match="expiry day before release day"):
        InventoryLot(
            id="l", product_id="p", location_id="r1", units=10, release_day=10, expiry_day=5
        )
