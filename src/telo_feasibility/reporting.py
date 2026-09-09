"""Reporting: definition-of-finished status and the preliminary banner.

Figure and report builders are added in later phases; the status checker exists
from day one because every report must say exactly which gates remain incomplete.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .configs import count_illustrative, load_gates, load_global, load_products
from .provenance import PACKAGE_ROOT, load_protocol
from .schemas import GateStatus

PRELIMINARY_BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"
RESULTS = PACKAGE_ROOT / "results"
DATA = PACKAGE_ROOT / "data"
DOCS = PACKAGE_ROOT / "docs"


@dataclass(frozen=True)
class FinishedTest:
    id: str
    test: str
    passed: bool
    evidence: str
    human_required: bool = False


def _json_or_none(path: Path) -> Any | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _count_json_with(path_glob: str, key: str, value: str) -> int:
    n = 0
    for p in PACKAGE_ROOT.glob(path_glob):
        d = _json_or_none(p)
        if isinstance(d, dict) and d.get(key) == value:
            n += 1
    return n


def finished_status() -> list[FinishedTest]:
    """Evaluate the 22 definition-of-finished tests from artifacts on disk. Never guesses."""
    protocol = load_protocol()
    tests: list[FinishedTest] = []

    # DF01 protocol frozen and signed off
    rev_path = PACKAGE_ROOT / "protocol" / "revisions.csv"
    pending: list[str] = []
    with rev_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if "pending" in row.get("approved_by", "").lower():
                pending.append(row["revision_id"])
    tests.append(
        FinishedTest(
            "DF01",
            "protocol version frozen",
            protocol.protocol.status == "frozen" and not pending,
            f"protocol v{protocol.version} status={protocol.protocol.status}; revisions pending sign-off: {pending or 'none'}",
        )
    )

    screen = _json_or_none(DATA / "product_dossiers" / "screen_manifest.json")
    n_cand = len(screen.get("candidates", [])) if isinstance(screen, dict) else 0
    dated = bool(screen and screen.get("snapshot_ids")) if isinstance(screen, dict) else False
    tests.append(
        FinishedTest(
            "DF02",
            "five-product dated screen complete",
            n_cand >= 5 and dated,
            f"screen_manifest.json candidates={n_cand}, dated snapshots={dated}",
        )
    )

    sel = _json_or_none(DATA / "product_dossiers" / "selection.json")
    n_sel = len(sel.get("selected", [])) if isinstance(sel, dict) else 0
    tests.append(
        FinishedTest(
            "DF03",
            "two exact product presentations selected",
            n_sel == 2,
            f"selection.json selected={n_sel}",
            human_required=True,
        )
    )

    complete_dossiers = _count_json_with(
        "data/product_dossiers/*/dossier.json", "status", "complete"
    )
    tests.append(
        FinishedTest(
            "DF04",
            "product dossiers complete",
            n_sel == 2 and complete_dossiers >= 2,
            f"complete dossiers={complete_dossiers}",
        )
    )

    sim_manifests = (
        list((RESULTS / "manifests").glob("sim_*.json")) if (RESULTS / "manifests").exists() else []
    )
    strategies_seen: set[str] = set()
    for m in sim_manifests:
        d = _json_or_none(m)
        if isinstance(d, dict):
            strategies_seen.update(str(s) for s in d.get("strategy_ids", []))
    tests.append(
        FinishedTest(
            "DF05",
            "all eight strategies represented",
            len(strategies_seen) == 8,
            f"strategies in simulation manifests: {sorted(strategies_seen) or 'none'}",
        )
    )

    opt = (
        list((RESULTS / "optimization").glob("*/summary.json"))
        if (RESULTS / "optimization").exists()
        else []
    )
    tests.append(
        FinishedTest(
            "DF06",
            "strategies optimized to matched service targets",
            bool(opt),
            f"optimization summaries={len(opt)}",
        )
    )

    maps = [
        (DOCS / "regulatory" / n).is_file()
        for n in ("approved_generic_cmo_map.md", "503b_shortage_response_map.md")
    ]
    tests.append(
        FinishedTest(
            "DF07",
            "approved-generic/CMO and 503B pathways separated",
            all(maps),
            f"decision maps present={maps}",
        )
    )

    gates = load_gates()
    reviewed = [g.id for g in gates.gates if g.reviewer]
    unresolved = [g.id for g in gates.gates if g.status is GateStatus.UNCERTAIN]
    tests.append(
        FinishedTest(
            "DF08",
            "material regulatory gates reviewed by a qualified expert",
            len(reviewed) == len(gates.gates) and not unresolved,
            f"reviewed {len(reviewed)}/{len(gates.gates)}; UNCERTAIN: {unresolved}",
            human_required=True,
        )
    )

    sets = [load_global()] + [p.parameters for p in load_products().values()]
    ic = count_illustrative(sets)
    tests.append(
        FinishedTest(
            "DF09",
            "no material illustrative input remains",
            not ic.any_illustrative,
            f"illustrative={ic.illustrative}, missing={ic.missing} of {ic.total_parameters} parameters",
        )
    )
    tests.append(
        FinishedTest(
            "DF10",
            "direct or expert-validated input distributions documented",
            not ic.any_illustrative and ic.total_parameters > 0,
            "same evidence as DF09 plus distribution records",
            human_required=True,
        )
    )

    rec = _json_or_none(RESULTS / "deterministic" / "reconciliation.json")
    rec_ok = bool(rec and rec.get("ok") is True) if isinstance(rec, dict) else False
    tests.append(
        FinishedTest(
            "DF11",
            "deterministic model reconciles with workbook",
            rec_ok,
            f"results/deterministic/reconciliation.json ok={rec_ok if rec else 'absent'}",
        )
    )

    tr = _json_or_none(RESULTS / "manifests" / "test_report.json")
    tests_ok = (
        bool(tr and tr.get("failed", 1) == 0 and tr.get("passed", 0) > 0)
        if isinstance(tr, dict)
        else False
    )
    tests.append(
        FinishedTest(
            "DF12",
            "stochastic simulation passes all tests",
            tests_ok and bool(sim_manifests),
            f"test_report.json={tr if tr else 'absent'}; simulation manifests={len(sim_manifests)}",
        )
    )
    tests.append(
        FinishedTest(
            "DF13",
            "common random numbers implemented",
            tests_ok and bool(tr and tr.get("crn_test_passed")),
            "requires test_report.json crn_test_passed",
        )
    )
    tests.append(
        FinishedTest(
            "DF14",
            "common-cause failures represented",
            tests_ok and bool(tr and tr.get("common_cause_test_passed")),
            "requires test_report.json common_cause_test_passed",
        )
    )

    back = (
        list((RESULTS / "backcasts").glob("*/comparison.json"))
        if (RESULTS / "backcasts").exists()
        else []
    )
    tests.append(
        FinishedTest(
            "DF15",
            "historical backcasts complete",
            len(back) >= 4,
            f"backcast comparisons={len(back)} (need >= 4 episode classes)",
        )
    )
    sens = (RESULTS / "sensitivity" / "summary.json").is_file()
    tests.append(
        FinishedTest(
            "DF16",
            "global and structural sensitivity complete",
            sens,
            f"results/sensitivity/summary.json present={sens}",
        )
    )
    voi = (RESULTS / "sensitivity" / "decision_reversal.json").is_file() and (
        RESULTS / "sensitivity" / "voi.json"
    ).is_file()
    tests.append(
        FinishedTest(
            "DF17",
            "decision-reversal and value-of-information analyses complete",
            voi,
            f"decision_reversal.json and voi.json present={voi}",
        )
    )

    interviews = _count_json_with("data/interview_evidence/*.json", "status", "complete")
    tests.append(
        FinishedTest(
            "DF18",
            "real interview evidence logged",
            interviews >= 25,
            f"completed interviews logged={interviews} (target 25-30)",
            human_required=True,
        )
    )
    reviews = _count_json_with("docs/reviewer_packets/reviews/*.json", "status", "complete")
    tests.append(
        FinishedTest(
            "DF19",
            "at least three qualified independent reviews completed",
            reviews >= 3,
            f"completed reviews={reviews}",
            human_required=True,
        )
    )

    release = _json_or_none(RESULTS / "manifests" / "public_release.json")
    tests.append(
        FinishedTest(
            "DF20",
            "public code, data dictionary, assumptions, model cards, run manifest, revision log, and limitations released",
            bool(release and release.get("released")),
            f"public_release.json={release if release else 'absent'}",
            human_required=True,
        )
    )

    finding = _json_or_none(RESULTS / "manifests" / "nonobvious_finding.json")
    tests.append(
        FinishedTest(
            "DF21",
            "at least one non-obvious result identified",
            bool(finding and finding.get("finding")),
            f"nonobvious_finding.json={'absent' if not finding else 'present'}",
        )
    )

    unsupported: list[str] = []
    with (PACKAGE_ROOT / "CLAIMS_REGISTER.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("evidence_status", "").startswith(
                ("unsupported", "contradicted", "retracted")
            ):
                unsupported.append(row["claim_id"])
    tests.append(
        FinishedTest(
            "DF22",
            "external claims do not exceed evidence",
            not unsupported,
            f"claims register rows unsupported/contradicted/retracted: {unsupported or 'none'}",
            human_required=True,
        )
    )
    return tests


def status_text(tests: list[FinishedTest]) -> str:
    done = sum(1 for t in tests if t.passed)
    lines = [
        PRELIMINARY_BANNER if done < len(tests) else "ALL DEFINITION-OF-FINISHED TESTS PASS",
        f"definition of finished: {done}/{len(tests)} complete",
        "",
    ]
    for t in tests:
        mark = "PASS" if t.passed else "----"
        human = " [human]" if t.human_required and not t.passed else ""
        lines.append(f"{t.id} {mark}{human} {t.test}")
        lines.append(f"      {t.evidence}")
    return "\n".join(lines)
