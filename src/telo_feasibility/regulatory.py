"""Regulatory gates: per-strategy eligibility and the 503B state machine.

Rules (protocol 3.1, 4.4; task section 7):

* Any applicable gate FAIL -> EXCLUDED.
* Any applicable gate UNCERTAIN (and none FAIL) -> NO_CONCLUSION. The strategy may be
  simulated for information but can never receive a favorable decision class.
* All applicable gates PASS -> ELIGIBLE.
* NOT_APPLICABLE gates are ignored.
* A strategy that no gate names at all is NO_CONCLUSION (a design-space strategy whose
  gates have not been mapped yet must never read as eligible by omission).
* There is no penalty-cost path. UNCERTAIN is never coerced to PASS.

The label "preliminary regulatory analysis; not legal advice" travels with every
evaluation until a qualified reviewer is recorded on every applicable gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .schemas import Eligibility, GateSet, GateStatus, GateTreatment, RegulatoryGate, StrategyId

NOT_LEGAL_ADVICE = "preliminary regulatory analysis; not legal advice"


@dataclass(frozen=True)
class StrategyEligibility:
    strategy_id: StrategyId
    eligibility: Eligibility
    gate_statuses: dict[str, GateStatus]
    failed: list[str]
    uncertain: list[str]
    lead_time_gates: list[str]
    cap_gates: list[str]
    dynamic_gates: list[str]
    region_restriction_gates: list[str]
    release_assurance_allowed: bool
    fleet_claim_allowed: bool
    reviewed_by_qualified_expert: bool
    gates_mapped: bool = True
    label: str = field(default=NOT_LEGAL_ADVICE)


def evaluate_strategy(gates: GateSet, strategy: StrategyId) -> StrategyEligibility:
    applicable: list[RegulatoryGate] = [
        g for g in gates.for_strategy(strategy) if g.status is not GateStatus.NOT_APPLICABLE
    ]
    statuses = {g.id: g.status for g in applicable}
    failed = sorted(g.id for g in applicable if g.status is GateStatus.FAIL)
    uncertain = sorted(g.id for g in applicable if g.status is GateStatus.UNCERTAIN)
    mapped = bool(gates.for_strategy(strategy))
    if failed:
        elig = Eligibility.EXCLUDED
    elif uncertain or not mapped:
        elig = Eligibility.NO_CONCLUSION
    else:
        elig = Eligibility.ELIGIBLE

    def with_treatment(t: GateTreatment) -> list[str]:
        return sorted(g.id for g in applicable if g.treatment is t)

    ra_gates = with_treatment(GateTreatment.FALLBACK_CONVENTIONAL)
    ra_allowed = (
        bool(ra_gates)
        and all(statuses[g] is GateStatus.PASS for g in ra_gates)
        and elig is Eligibility.ELIGIBLE
    )
    fleet_gates = with_treatment(GateTreatment.NO_FLEET_CLAIM)
    fleet_allowed = bool(fleet_gates) and all(statuses[g] is GateStatus.PASS for g in fleet_gates)
    reviewed = all(bool(g.reviewer) for g in applicable) if applicable else False
    return StrategyEligibility(
        strategy_id=strategy,
        eligibility=elig,
        gate_statuses=statuses,
        failed=failed,
        uncertain=uncertain,
        lead_time_gates=with_treatment(GateTreatment.LEAD_TIME),
        cap_gates=with_treatment(GateTreatment.CAP),
        dynamic_gates=with_treatment(GateTreatment.DYNAMIC_STATE),
        region_restriction_gates=with_treatment(GateTreatment.REGION_RESTRICTION),
        release_assurance_allowed=ra_allowed,
        fleet_claim_allowed=fleet_allowed,
        reviewed_by_qualified_expert=reviewed,
        gates_mapped=mapped,
    )


def evaluate_all(gates: GateSet) -> dict[StrategyId, StrategyEligibility]:
    return {s: evaluate_strategy(gates, s) for s in StrategyId}


def r3_permitted(gates: GateSet) -> bool:
    """R3 (validated release component) may be enabled only when S6 is ELIGIBLE and G15 is PASS."""
    e = evaluate_strategy(gates, StrategyId.S6)
    return e.release_assurance_allowed


@dataclass(frozen=True)
class Shortage503BState:
    """Time-varying legal availability of the 503B pathway for one presentation.

    ``on_shortage_list`` is exogenous (from the simulation's regulatory stream or a
    frozen history). Compounding, distribution, and dispensing are lawful under the
    essentially-a-copy exception only while the product is on the list (gates G09,
    G10). ``eligible_today`` also requires the static gates to be PASS.
    """

    on_shortage_list: bool
    static_gates_pass: bool
    state_permission: bool

    @property
    def eligible_today(self) -> bool:
        return self.on_shortage_list and self.static_gates_pass and self.state_permission


def static_503b_gates_pass(gates: GateSet) -> bool:
    static_ids = {"G08", "G11"}
    return all(gates.by_id(i).status is GateStatus.PASS for i in static_ids)
