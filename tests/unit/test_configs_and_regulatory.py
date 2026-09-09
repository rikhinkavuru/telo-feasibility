from __future__ import annotations

import itertools
from datetime import date

from hypothesis import given
from hypothesis import strategies as st

from telo_feasibility.configs import (
    count_illustrative,
    load_gates,
    load_global,
    load_products,
    load_strategies,
)
from telo_feasibility.regulatory import evaluate_all, evaluate_strategy, r3_permitted
from telo_feasibility.schemas import (
    FROZEN_STRATEGY_IDS,
    Eligibility,
    GateSet,
    GateStatus,
    RegulatoryGate,
    StrategyId,
)


def test_global_and_products_load_and_are_all_illustrative() -> None:
    g = load_global()
    products = load_products()
    assert set(products) == {"sodium_bicarbonate_8_4_50ml", "norepinephrine_1mgml_4ml"}
    for p in products.values():
        assert len(p.parameters.parameters) == 20
        assert p.presentation.archetype_fit
    ic = count_illustrative([g] + [p.parameters for p in products.values()])
    assert ic.total_parameters == len(g.parameters) + 40
    # every product parameter is illustrative; only the release components carry sources
    assert all(
        p.parameters.illustrative_ids() == sorted(p.parameters.parameters)
        for p in products.values()
    )
    sourced = sorted(k for k, p in g.parameters.items() if not p.is_illustrative)
    assert sourced == [
        "assay_days",
        "endotoxin_days",
        "environmental_monitoring_days",
        "sterility_incubation_days",
    ]
    assert ic.any_illustrative


def test_strategies_load_in_protocol_order() -> None:
    s = load_strategies()
    assert [d.id for d in s.designs] == list(FROZEN_STRATEGY_IDS)
    assert s.by_id(StrategyId.S6).design_variables["release_time_factor"] == 0.6
    assert not s.by_id(StrategyId.S7).durable


def test_all_strategies_are_no_conclusion_while_gates_uncertain() -> None:
    gates = load_gates()
    res = evaluate_all(gates)
    assert {r.eligibility for r in res.values()} == {Eligibility.NO_CONCLUSION}
    assert not r3_permitted(gates)
    assert all(not r.reviewed_by_qualified_expert for r in res.values())
    assert res[StrategyId.S6].uncertain[-1] == "G15"


def _with_statuses(gates: GateSet, status_by_id: dict[str, GateStatus]) -> GateSet:
    new: list[RegulatoryGate] = []
    for g in gates.gates:
        s = status_by_id.get(g.id, g.status)
        data = g.model_dump()
        data["status"] = s
        if s in (GateStatus.PASS, GateStatus.FAIL):
            data["reviewer"] = "test reviewer"
            data["review_date"] = date(2026, 9, 1)
        new.append(RegulatoryGate.model_validate(data))
    return GateSet(
        version=gates.version,
        label=gates.label,
        statuses=gates.statuses,
        treatments=gates.treatments,
        gates=new,
    )


def test_fail_excludes_and_all_pass_is_eligible() -> None:
    gates = load_gates()
    ids = [g.id for g in gates.for_strategy(StrategyId.S5)]
    all_pass = _with_statuses(gates, dict.fromkeys(ids, GateStatus.PASS))
    assert evaluate_strategy(all_pass, StrategyId.S5).eligibility is Eligibility.ELIGIBLE
    one_fail = _with_statuses(all_pass, {ids[0]: GateStatus.FAIL})
    assert evaluate_strategy(one_fail, StrategyId.S5).eligibility is Eligibility.EXCLUDED


def test_r3_requires_s6_eligible_and_g15_pass() -> None:
    gates = load_gates()
    ids = [g.id for g in gates.for_strategy(StrategyId.S6)]
    all_pass = _with_statuses(gates, dict.fromkeys(ids, GateStatus.PASS))
    assert r3_permitted(all_pass)
    g15_uncertain = _with_statuses(all_pass, {"G15": GateStatus.UNCERTAIN})
    assert not r3_permitted(g15_uncertain)


@given(
    st.lists(
        st.sampled_from(
            [GateStatus.PASS, GateStatus.UNCERTAIN, GateStatus.FAIL, GateStatus.NOT_APPLICABLE]
        ),
        min_size=10,
        max_size=10,
    )
)
def test_property_uncertain_never_eligible(statuses: list[GateStatus]) -> None:
    gates = load_gates()
    ids = [g.id for g in gates.for_strategy(StrategyId.S6)]  # G01-G07, G13, G14, G15
    assert len(ids) == 10
    gs = _with_statuses(gates, dict(zip(ids, statuses, strict=True)))
    e = evaluate_strategy(gs, StrategyId.S6)
    applicable = [s for s in statuses if s is not GateStatus.NOT_APPLICABLE]
    if GateStatus.FAIL in applicable:
        assert e.eligibility is Eligibility.EXCLUDED
    elif GateStatus.UNCERTAIN in applicable:
        assert e.eligibility is Eligibility.NO_CONCLUSION
    else:
        assert e.eligibility is Eligibility.ELIGIBLE


def test_every_gate_combination_with_uncertain_is_not_eligible_for_s7() -> None:
    gates = load_gates()
    ids = [g.id for g in gates.for_strategy(StrategyId.S7)]
    for combo in itertools.product([GateStatus.PASS, GateStatus.UNCERTAIN], repeat=len(ids)):
        if GateStatus.UNCERTAIN not in combo:
            continue
        gs = _with_statuses(gates, dict(zip(ids, combo, strict=True)))
        assert evaluate_strategy(gs, StrategyId.S7).eligibility is not Eligibility.ELIGIBLE
