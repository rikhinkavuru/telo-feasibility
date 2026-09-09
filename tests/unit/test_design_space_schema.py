"""Design-space strategies (S8+): schema validators, loaders, the unmapped-gate guard, and
search-space resolution. S0-S7 stay frozen; everything here is for configuration-declared
strategies added by the 2026-09 assignment."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from telo_feasibility.configs import (
    load_all_strategies,
    load_design_space_strategies,
    load_gates,
    load_strategies,
)
from telo_feasibility.optimization import DESIGN_SPACES, Variable, space_for
from telo_feasibility.regulatory import evaluate_all, evaluate_strategy
from telo_feasibility.schemas import (
    FROZEN_STRATEGY_IDS,
    DesignVariableSpec,
    Eligibility,
    GateSet,
    GateStatus,
    RegulatoryGate,
    SitePlanSpec,
    StrategyDesign,
    StrategyId,
    SupplierSpec,
)

PROFILE: dict[str, Any] = {
    "family": "test",
    "product_archetype": "aqueous small-molecule sterile solution, standard vial",
    "asset_ownership": "owned central plant",
    "sites_summary": "one central plant",
    "regulatory_owner": "application holder (unnamed)",
    "quality_owner": "single quality unit",
    "supplier_graph": "api_1, vial_1, stopper_1",
    "material_flow": "supplier -> plant -> regions",
    "production_steps": "compounding, aseptic fill, release",
    "release_pathway": "R0 conventional",
    "inventory_policy": "order-up-to",
    "allocation_policy": "proportional",
    "customer": "hospitals (unverified)",
    "revenue_mechanism": "unit price (illustrative)",
    "contracting_requirement": "none modeled",
    "capital_requirement": "illustrative",
    "implementation_lead_time": "illustrative",
    "regulatory_gates": ["G01"],
    "dominant_risks": "test only",
    "potential_moat": "none",
    "falsification_test": "none",
}


def s8_dict(**over: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "id": "S8",
        "name": "design-space test strategy",
        "pathway": "approved_cmo",
        "durable": True,
        "family": "test",
        "design_variables": {"capacity_factor": 1.0, "safety_stock_days": 30.0},
        "site_plans": [
            {
                "id": "central",
                "region_id": "R1",
                "archetype": "central",
                "scale": 1.0,
                "groups": ["cc_api_1", "cc_vial_1", "cc_geo_R1"],
            }
        ],
        "design_space": [
            {"name": "safety_stock_days", "low": 10.0, "high": 90.0, "kind": "float", "grid": 3}
        ],
        "profile": dict(PROFILE),
    }
    d.update(over)
    return d


# ---------------------------------------------------------------------------- validators


def test_s8_requires_site_plans() -> None:
    d = s8_dict()
    d.pop("site_plans")
    with pytest.raises(ValidationError, match="site_plans"):
        StrategyDesign.model_validate(d)
    with pytest.raises(ValidationError, match="site_plans"):
        StrategyDesign.model_validate(s8_dict(site_plans=[]))


def test_frozen_ids_reject_site_plans() -> None:
    for sid in FROZEN_STRATEGY_IDS:
        d = s8_dict(id=sid.value, pathway="503b" if sid is StrategyId.S7 else "approved_cmo")
        d["durable"] = sid is not StrategyId.S7
        with pytest.raises(ValidationError, match="frozen"):
            StrategyDesign.model_validate(d)


def test_duplicate_site_ids_rejected() -> None:
    plan = s8_dict()["site_plans"][0]
    with pytest.raises(ValidationError, match="duplicate site plan ids"):
        StrategyDesign.model_validate(s8_dict(site_plans=[plan, dict(plan)]))


def test_reserved_only_fields_need_reserved() -> None:
    base = {"id": "cdmo", "region_id": "R2", "archetype": "cdmo_reserved", "scale": 1.0}
    with pytest.raises(ValidationError, match="reserved=true"):
        SitePlanSpec.model_validate({**base, "exercise_batches_per_year": 2.0})
    with pytest.raises(ValidationError, match="reserved=true"):
        SitePlanSpec.model_validate({**base, "activation_failure_probability": 0.2})
    ok = SitePlanSpec.model_validate(
        {
            **base,
            "reserved": True,
            "exercise_batches_per_year": 2.0,
            "activation_failure_probability": 0.2,
        }
    )
    assert ok.reserved and ok.exercise_batches_per_year == 2.0


def test_503b_pathway_requires_503b_archetype() -> None:
    with pytest.raises(ValidationError, match="503b archetype"):
        SitePlanSpec.model_validate(
            {
                "id": "p503b",
                "region_id": "R1",
                "archetype": "central",
                "scale": 0.2,
                "pathway": "503b",
            }
        )
    ok = SitePlanSpec.model_validate(
        {"id": "p503b", "region_id": "R1", "archetype": "503b", "scale": 0.2, "pathway": "503b"}
    )
    assert ok.archetype == "503b"


def test_503b_pathway_strategy_is_not_durable() -> None:
    plans = [
        {"id": "p503b_x", "region_id": "R1", "archetype": "503b", "scale": 0.2, "pathway": "503b"}
    ]
    with pytest.raises(ValidationError, match="not a durable"):
        StrategyDesign.model_validate(s8_dict(pathway="503b", durable=True, site_plans=plans))
    assert not StrategyDesign.model_validate(
        s8_dict(pathway="503b", durable=False, site_plans=plans)
    ).durable


def test_supplier_spec_needs_exactly_one_lead_time() -> None:
    base = {"id": "hub_bulk", "name": "hub bulk", "component_ids": ["api"]}
    with pytest.raises(ValidationError, match="lead_time_days or lead_time_factor"):
        SupplierSpec.model_validate(base)
    with pytest.raises(ValidationError, match="lead_time_days or lead_time_factor"):
        SupplierSpec.model_validate({**base, "lead_time_days": 20.0, "lead_time_factor": 0.2})
    assert SupplierSpec.model_validate({**base, "lead_time_days": 20.0}).lead_time_days == 20.0
    assert SupplierSpec.model_validate({**base, "lead_time_factor": 0.2}).lead_time_factor == 0.2


def test_design_variable_spec_rejects_inverted_bounds() -> None:
    with pytest.raises(ValidationError, match="high < low"):
        DesignVariableSpec(name="x", low=2.0, high=1.0)
    v = DesignVariableSpec(name="x", low=1.0, high=1.0)
    assert v.kind == "float" and v.grid == 3


def test_valid_s8_with_profile_round_trips() -> None:
    d = StrategyDesign.model_validate(s8_dict())
    assert d.profile is not None and d.profile.regulatory_gates == ["G01"]
    assert d.site_plans is not None and d.site_plans[0].serves == "all"
    again = StrategyDesign.model_validate(d.model_dump(mode="json"))
    assert again == d
    assert not d.id.is_frozen


# ---------------------------------------------------------------------------- loaders


def _write(path: Path, designs: list[dict[str, Any]]) -> Path:
    path.write_text(
        yaml.safe_dump({"id": "test_space", "description": "t", "designs": designs}),
        encoding="utf-8",
    )
    return path


def test_load_design_space_strategies_rejects_frozen_ids(tmp_path: Path) -> None:
    frozen = load_strategies().by_id(StrategyId.S0).model_dump(mode="json")
    with pytest.raises(ValueError, match="frozen"):
        load_design_space_strategies(_write(tmp_path / "ds.yaml", [frozen]))


def test_load_design_space_strategies_rejects_duplicates(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="duplicate"):
        load_design_space_strategies(_write(tmp_path / "ds.yaml", [s8_dict(), s8_dict()]))


def test_load_design_space_strategies_missing_file_is_empty(tmp_path: Path) -> None:
    s = load_design_space_strategies(tmp_path / "absent.yaml")
    assert s.designs == [] and s.id == "design_space"


def test_load_all_strategies_is_frozen_then_extras_in_order(tmp_path: Path) -> None:
    path = _write(tmp_path / "ds.yaml", [s8_dict(id="S9", name="nine"), s8_dict(id="S8")])
    reg = load_all_strategies(design_space_path=path)
    assert [d.id for d in reg.designs] == [*FROZEN_STRATEGY_IDS, StrategyId.S9, StrategyId.S8]
    assert reg.by_id(StrategyId.S9).name == "nine"
    with pytest.raises(KeyError):
        reg.by_id(StrategyId.S10)
    assert [
        d.id for d in load_all_strategies(design_space_path=tmp_path / "none.yaml").designs
    ] == list(FROZEN_STRATEGY_IDS)


# ---------------------------------------------------------------------------- regulatory guard


def _all_pass(gates: GateSet) -> GateSet:
    new: list[RegulatoryGate] = []
    for g in gates.gates:
        data = g.model_dump()
        data["status"] = GateStatus.PASS
        data["reviewer"] = "test reviewer"
        data["review_date"] = date(2026, 9, 2)
        new.append(RegulatoryGate.model_validate(data))
    return GateSet(
        version=gates.version,
        label=gates.label,
        statuses=gates.statuses,
        treatments=gates.treatments,
        gates=new,
    )


def test_unmapped_strategy_is_never_eligible() -> None:
    """An id no gate names is NO_CONCLUSION by omission, and stays so even if every gate passes.

    Protocol revision R006 named S8-S19 in every gate that applies to them, so S20 is now the
    only free id left to exercise the guard with.
    """
    gates = load_gates()
    default = evaluate_strategy(gates, StrategyId.S20)
    assert default.eligibility is Eligibility.NO_CONCLUSION
    assert not default.gates_mapped and default.uncertain == [] and default.failed == []
    all_pass = _all_pass(gates)
    assert evaluate_strategy(all_pass, StrategyId.S5).eligibility is Eligibility.ELIGIBLE
    assert evaluate_strategy(all_pass, StrategyId.S5).gates_mapped
    s20 = evaluate_strategy(all_pass, StrategyId.S20)
    assert s20.eligibility is Eligibility.NO_CONCLUSION and not s20.gates_mapped
    assert not s20.release_assurance_allowed and not s20.fleet_claim_allowed


def test_configured_design_space_ids_are_gated_by_analysis_not_by_omission() -> None:
    """Every strategy declared in config/strategies/design_space.yaml is named by the gates.

    Without this, a design-space strategy would report NO_CONCLUSION because nothing was
    mapped to it, which reads identically to NO_CONCLUSION because its gates are UNCERTAIN.
    """
    gates = load_gates()
    configured = [d.id for d in load_design_space_strategies().designs]
    assert configured, "config/strategies/design_space.yaml declares no strategies"
    ordinary = {"G01", "G02", "G03", "G04", "G05", "G06", "G07"}
    for sid in configured:
        e = evaluate_strategy(gates, sid)
        assert e.gates_mapped, sid
        assert e.eligibility is Eligibility.NO_CONCLUSION and e.failed == [], sid
        assert set(e.uncertain) >= ordinary, sid
        # no configured design claims a release-assurance component, so G15 stays on S6 alone
        assert "G15" not in e.gate_statuses, sid
        assert not e.release_assurance_allowed and not e.fleet_claim_allowed, sid


def test_evaluate_all_covers_every_strategy_id() -> None:
    res = evaluate_all(load_gates())
    assert set(res) == set(StrategyId)
    assert all(res[s].gates_mapped for s in FROZEN_STRATEGY_IDS)
    configured = {d.id for d in load_design_space_strategies().designs}
    assert all(res[s].gates_mapped for s in configured)
    unmapped = {s for s in StrategyId if not s.is_frozen} - configured
    assert unmapped == {StrategyId.S20}
    assert all(not res[s].gates_mapped for s in unmapped)


# ---------------------------------------------------------------------------- search space


def test_space_for_frozen_and_declared() -> None:
    s0 = load_strategies().by_id(StrategyId.S0)
    assert space_for(s0) is DESIGN_SPACES[StrategyId.S0]
    s8 = StrategyDesign.model_validate(s8_dict())
    assert space_for(s8) == [Variable("safety_stock_days", 10.0, 90.0, "float", 3)]
    bare = StrategyDesign.model_validate(s8_dict(design_space=[]))
    with pytest.raises(ValueError, match="no design space"):
        space_for(bare)
