"""Product-selection pipeline (protocol section 2): longlist, hard gates, weighted score, dossiers.

Evidence comes only from frozen snapshots under ``data/raw_snapshots`` (via their
manifests) and from the candidate's own configuration. Criteria that need clinical,
manufacturing, or commercial judgment are left unscored (``score is None``) until a
logged expert provides them; the workbook's provisional 1-5 scores are carried
separately as tier-5 values and never mixed into the data-based partial score.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field

from .configs import CONFIG_ROOT
from .provenance import PACKAGE_ROOT, RAW_SNAPSHOTS, load_protocol, read_manifests
from .schemas import GateStatus, SnapshotManifest, StrictModel

LONGLIST_PATH = CONFIG_ROOT / "longlist.yaml"
DOSSIERS = PACKAGE_ROOT / "data" / "product_dossiers"


class CandidateSpec(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    ingredient: str
    presentation: str
    strength_pattern: str
    ingredient_pattern: str
    ingredient_exact: list[str] = Field(default_factory=list)
    dosage_form_pattern: str
    protocol_role: str
    flags: dict[str, bool]
    identity_fixed: bool


class Longlist(StrictModel):
    version: str
    candidates: list[CandidateSpec]


def load_longlist(path: Path = LONGLIST_PATH) -> Longlist:
    with path.open("r", encoding="utf-8") as f:
        ll = Longlist.model_validate(yaml.safe_load(f))
    if len(ll.candidates) < 5:
        raise ValueError("protocol 2.2 requires a longlist of at least five presentations")
    return ll


# ---------------------------------------------------------------------------
# Snapshot location and readers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Snapshot:
    manifest: SnapshotManifest
    path: Path

    @property
    def sha256(self) -> str:
        return self.manifest.sha256 or ""


def latest_snapshot(source_id: str, filename: str, root: Path = RAW_SNAPSHOTS) -> Snapshot | None:
    """Most recent auto snapshot of ``source_id`` whose raw file is ``filename``."""
    best: Snapshot | None = None
    for m in read_manifests(root):
        if m.source_id != source_id or m.access_method != "auto" or not m.raw_path:
            continue
        if Path(m.raw_path).name != filename:
            continue
        p = root.parent.parent / m.raw_path
        if not p.is_file():
            continue
        if best is None or m.retrieved_at > best.manifest.retrieved_at:
            best = Snapshot(m, p)
    return best


def read_fda_shortage_csv(path: Path) -> list[dict[str, str]]:
    """FDA's export starts with a blank line and pads column names with spaces; normalize both."""
    text = path.read_text(encoding="utf-8-sig", errors="replace").lstrip("\r\n")
    reader = csv.DictReader(io.StringIO(text))
    rows: list[dict[str, str]] = []
    for row in reader:
        rows.append({(k or "").strip(): (v or "").strip() for k, v in row.items() if k is not None})
    return rows


def read_openfda_shortages_zip(path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.endswith(".json")]
        if not names:
            return []
        data = json.loads(z.read(names[0]).decode("utf-8"))
    results = data.get("results", []) if isinstance(data, dict) else []
    return [r for r in results if isinstance(r, dict)]


def _read_zip_table(path: Path, member_suffix: str, delimiter: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(member_suffix.lower())]
        if not names:
            return []
        raw = z.read(names[0])
    text = raw.decode("latin-1")
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def read_drugsatfda_products(path: Path) -> list[dict[str, str]]:
    return _read_zip_table(path, "Products.txt", "\t")


def read_drugsatfda_applications(path: Path) -> list[dict[str, str]]:
    return _read_zip_table(path, "Applications.txt", "\t")


def read_orange_book_products(path: Path) -> list[dict[str, str]]:
    return _read_zip_table(path, "products.txt", "~")


def read_dailymed_spls(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("data", []) if isinstance(data, dict) else []
    return [r for r in rows if isinstance(r, dict)]


def read_cms_partb_csv(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def bulks_list_status(html: str, ingredient_pattern: str) -> str:
    """'included', 'not_included', or 'absent' for the FDA 503B bulks list page."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    low = text.lower()
    inc = low.find("included")
    not_inc = low.find("not included")
    pat = re.compile(ingredient_pattern, re.IGNORECASE)
    hits = [m.start() for m in pat.finditer(text)]
    if not hits:
        return "absent"
    if not_inc >= 0 and any(h > not_inc for h in hits):
        return "not_included"
    if inc >= 0:
        return "included"
    return "absent"


# ---------------------------------------------------------------------------
# Evidence model
# ---------------------------------------------------------------------------


@dataclass
class EvidenceItem:
    source_id: str
    snapshot_sha256: str
    retrieved_at: str
    description: str
    value: Any = None


@dataclass
class GateResult:
    gate_id: str
    name: str
    status: str
    rationale: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    human_task: str | None = None


@dataclass
class CriterionScore:
    criterion: str
    weight: float
    score: int | None
    basis: str  # data_rule | expert_pending | expert
    rule: str
    confidence: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    disagreement: str = ""
    workbook_provisional_score: int | None = (
        None  # tier 5; never enters the data-based partial score
    )


@dataclass
class SourceSummary:
    source_id: str
    snapshot_sha256: str | None
    retrieved_at: str | None
    available: bool
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class Dossier:
    candidate_id: str
    ingredient: str
    presentation: str
    protocol_role: str
    generated_at: str
    protocol_version: str
    snapshot_ids: list[str]
    sources: dict[str, SourceSummary]
    gates: list[GateResult]
    criteria: list[CriterionScore]
    data_partial_score: float | None
    data_weight_covered: float
    workbook_provisional_total: float | None
    hard_gate_outcome: str
    status: str  # partial | complete
    human_tasks: list[str]
    banner: str


BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"

# Workbook 03_Product_Score H:N (tier 5 provisional judgments; author's scaffold values).
WORKBOOK_PROVISIONAL: dict[str, dict[str, int]] = {
    "sodium_bicarbonate_8_4_50ml": {
        "clinical_criticality": 5,
        "shortage_recurrence_duration": 5,
        "supplier_vulnerability": 4,
        "public_data_strength": 3,
        "manufacturing_fit": 5,
        "regional_relevance": 4,
        "demand_contract_fit": 4,
    },
    "acyclovir_sodium_50mgml_vial": {
        "clinical_criticality": 4,
        "shortage_recurrence_duration": 4,
        "supplier_vulnerability": 3,
        "public_data_strength": 3,
        "manufacturing_fit": 4,
        "regional_relevance": 3,
        "demand_contract_fit": 3,
    },
    "norepinephrine_1mgml_4ml": {
        "clinical_criticality": 5,
        "shortage_recurrence_duration": 4,
        "supplier_vulnerability": 2,
        "public_data_strength": 4,
        "manufacturing_fit": 4,
        "regional_relevance": 3,
        "demand_contract_fit": 3,
    },
    "acetazolamide_500mg_vial": {
        "clinical_criticality": 4,
        "shortage_recurrence_duration": 5,
        "supplier_vulnerability": 3,
        "public_data_strength": 3,
        "manufacturing_fit": 1,
        "regional_relevance": 2,
        "demand_contract_fit": 3,
    },
    "sterile_water_for_injection_vial": {
        "clinical_criticality": 5,
        "shortage_recurrence_duration": 5,
        "supplier_vulnerability": 3,
        "public_data_strength": 4,
        "manufacturing_fit": 5,
        "regional_relevance": 1,
        "demand_contract_fit": 1,
    },
    "furosemide_10mgml_vial": {
        "clinical_criticality": 4,
        "shortage_recurrence_duration": 4,
        "supplier_vulnerability": 3,
        "public_data_strength": 4,
        "manufacturing_fit": 5,
        "regional_relevance": 3,
        "demand_contract_fit": 4,
    },
}


def _ev(snap: Snapshot, description: str, value: Any = None) -> EvidenceItem:
    return EvidenceItem(
        snap.manifest.source_id,
        snap.sha256,
        snap.manifest.retrieved_at.isoformat(),
        description,
        value,
    )


def _match(pattern: str, text: str) -> bool:
    return re.search(pattern, text or "", re.IGNORECASE) is not None


def _ingredient_match(cand: CandidateSpec, active_ingredient: str, drug_name: str = "") -> bool:
    """Exact single-ingredient match on structured fields; regex fallback only when no exact list."""
    if cand.ingredient_exact:
        return (active_ingredient or "").strip().upper() in {
            x.upper() for x in cand.ingredient_exact
        }
    return _match(cand.ingredient_pattern, f"{active_ingredient} {drug_name}")


# ---------------------------------------------------------------------------
# Evidence attachment
# ---------------------------------------------------------------------------


@dataclass
class EvidenceBundle:
    fda_csv: Snapshot | None
    openfda: Snapshot | None
    drugsatfda: Snapshot | None
    orange_book: Snapshot | None
    dailymed: dict[str, Snapshot]
    bulks_page: Snapshot | None
    cms_partb: Snapshot | None

    @property
    def snapshot_ids(self) -> list[str]:
        ids: list[str] = []
        for s in (
            self.fda_csv,
            self.openfda,
            self.drugsatfda,
            self.orange_book,
            self.bulks_page,
            self.cms_partb,
        ):
            if s is not None:
                ids.append(f"{s.manifest.source_id}:{s.sha256[:12]}")
        for k, s in self.dailymed.items():
            ids.append(f"S18/{k}:{s.sha256[:12]}")
        return sorted(set(ids))


DAILYMED_FILES = {
    "sodium_bicarbonate_8_4_50ml": "spls_sodium_bicarbonate.json",
    "norepinephrine_1mgml_4ml": "spls_norepinephrine.json",
    "acyclovir_sodium_50mgml_vial": "spls_acyclovir.json",
    "furosemide_10mgml_vial": "spls_furosemide.json",
    "sterile_water_for_injection_vial": "spls_sterile_water.json",
    "acetazolamide_500mg_vial": "spls_acetazolamide.json",
}


def collect_evidence(root: Path = RAW_SNAPSHOTS) -> EvidenceBundle:
    dm: dict[str, Snapshot] = {}
    for cid, fn in DAILYMED_FILES.items():
        s = latest_snapshot("S18", fn, root)
        if s is not None:
            dm[cid] = s
    return EvidenceBundle(
        fda_csv=latest_snapshot("S01", "Drugshortages.csv", root),
        openfda=latest_snapshot("S01B", "drug-shortages-0001-of-0001.json.zip", root),
        drugsatfda=latest_snapshot("S16", "drugsatfda.zip", root),
        orange_book=latest_snapshot("S17", "EOBZIP.zip", root),
        dailymed=dm,
        bulks_page=latest_snapshot("S14", "503b_bulks_list.html", root),
        cms_partb=latest_snapshot("S19", "part_b_spending_by_drug_2024.csv", root),
    )


def _summarize_fda_csv(rows: list[dict[str, str]], cand: CandidateSpec) -> dict[str, Any]:
    hits = [r for r in rows if _match(cand.ingredient_pattern, r.get("Generic Name", ""))]
    pres = [r for r in hits if _match(cand.strength_pattern, r.get("Presentation", ""))]
    statuses: dict[str, int] = {}
    for r in hits:
        statuses[r.get("Status", "")] = statuses.get(r.get("Status", ""), 0) + 1
    posting_dates: list[date] = []
    for r in hits:
        raw = r.get("Initial Posting Date", "")
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                posting_dates.append(datetime.strptime(raw, fmt).date())
                break
            except ValueError:
                continue
    reasons = sorted(
        {r.get("Reason for Shortage", "") for r in hits if r.get("Reason for Shortage")}
    )
    companies = sorted({r.get("Company Name", "") for r in hits if r.get("Company Name")})
    return {
        "rows_ingredient": len(hits),
        "rows_presentation_match": len(pres),
        "status_counts": statuses,
        "earliest_initial_posting": min(posting_dates).isoformat() if posting_dates else None,
        "reasons": reasons,
        "companies": companies,
        "presentations": sorted({r.get("Presentation", "") for r in hits})[:40],
    }


def _summarize_openfda(rows: list[dict[str, Any]], cand: CandidateSpec) -> dict[str, Any]:
    hits = [r for r in rows if _match(cand.ingredient_pattern, str(r.get("generic_name", "")))]
    statuses: dict[str, int] = {}
    for r in hits:
        statuses[str(r.get("status", ""))] = statuses.get(str(r.get("status", "")), 0) + 1
    return {"records": len(hits), "status_counts": statuses}


def _summarize_drugsatfda(
    products: list[dict[str, str]], applications: list[dict[str, str]], cand: CandidateSpec
) -> dict[str, Any]:
    app_type = {a.get("ApplNo", ""): a.get("ApplType", "") for a in applications}
    sponsor = {a.get("ApplNo", ""): a.get("SponsorName", "") for a in applications}
    hits = [
        p
        for p in products
        if _ingredient_match(cand, p.get("ActiveIngredient", ""), p.get("DrugName", ""))
        and _match(cand.dosage_form_pattern, p.get("Form", ""))
    ]
    strength_hits = [p for p in hits if _match(cand.strength_pattern, p.get("Strength", ""))]
    appls = sorted({p.get("ApplNo", "") for p in hits})
    sponsors = sorted({sponsor.get(a, "") for a in appls if sponsor.get(a)})
    types: dict[str, int] = {}
    for a in appls:
        t = app_type.get(a, "")
        types[t] = types.get(t, 0) + 1
    return {
        "products_ingredient_form": len(hits),
        "products_strength_match": len(strength_hits),
        "applications": len(appls),
        "application_types": types,
        "sponsors": sponsors,
        "forms": sorted({p.get("Form", "") for p in hits})[:20],
    }


def _summarize_orange_book(rows: list[dict[str, str]], cand: CandidateSpec) -> dict[str, Any]:
    hits = [
        r
        for r in rows
        if _ingredient_match(cand, r.get("Ingredient", ""), r.get("Trade_Name", ""))
        and _match(cand.dosage_form_pattern, r.get("DF;Route", ""))
    ]
    applicants = sorted({r.get("Applicant", "") for r in hits if r.get("Applicant")})
    rld = [r for r in hits if r.get("RLD", "").strip().upper() == "YES"]
    return {
        "products": len(hits),
        "applicants": applicants,
        "rld_products": len(rld),
        "strength_matches": len(
            [r for r in hits if _match(cand.strength_pattern, r.get("Strength", ""))]
        ),
    }


def _summarize_dailymed(rows: list[dict[str, Any]], cand: CandidateSpec) -> dict[str, Any]:
    titles = [str(r.get("title", "")) for r in rows]
    inj = [t for t in titles if _match(cand.dosage_form_pattern, t)]
    strength = [t for t in inj if _match(cand.strength_pattern, t)]
    return {
        "spls": len(rows),
        "injectable_titles": len(inj),
        "strength_matches": len(strength),
        "sample_titles": inj[:10],
    }


def _summarize_cms(rows: list[dict[str, str]], cand: CandidateSpec) -> dict[str, Any]:
    fields = [
        k for k in (rows[0].keys() if rows else []) if "name" in k.lower() or "drug" in k.lower()
    ]
    hits = [r for r in rows if any(_match(cand.ingredient_pattern, r.get(f, "")) for f in fields)]
    return {"rows": len(hits), "note": "utilization/reimbursement proxy only; never cost"}


# ---------------------------------------------------------------------------
# Gates and scores
# ---------------------------------------------------------------------------


def evaluate_hard_gates(
    cand: CandidateSpec, sources: dict[str, SourceSummary], bundle: EvidenceBundle
) -> list[GateResult]:
    f = cand.flags
    gates: list[GateResult] = []
    gates.append(
        GateResult(
            "PG1",
            "Product identity",
            GateStatus.PASS.value if cand.identity_fixed else GateStatus.UNCERTAIN.value,
            "presentation fully specified in config"
            if cand.identity_fixed
            else "exact fill volume/container not yet fixed",
            human_task=None
            if cand.identity_fixed
            else "fix the exact presentation from DailyMed labels",
        )
    )
    fit_fail = [
        k
        for k in (
            "lyophilized",
            "suspension_or_emulsion",
            "biologic_or_vaccine",
            "cytotoxic_or_high_potency",
            "drug_device_combination",
            "cold_chain_intensive",
        )
        if f.get(k)
    ]
    if (
        not f.get("aqueous_solution", False)
        or not f.get("small_molecule", False)
        or not f.get("standard_vial", False)
    ):
        fit_fail.append("not aqueous small-molecule solution in a standard vial")
    gates.append(
        GateResult(
            "PG2",
            "Manufacturing fit",
            GateStatus.FAIL.value if fit_fail else GateStatus.PASS.value,
            "violates first archetype: " + ", ".join(fit_fail)
            if fit_fail
            else "aqueous small-molecule solution in a standard vial (config flags; process train review pending)",
        )
    )
    gates.append(
        GateResult(
            "PG3",
            "Control status",
            GateStatus.FAIL.value if f.get("controlled_substance") else GateStatus.PASS.value,
            "controlled substance"
            if f.get("controlled_substance")
            else "non-controlled (config flag)",
        )
    )
    dfa = sources.get("S16")
    ob = sources.get("S17")
    n_appl = int(dfa.summary.get("applications", 0)) if dfa and dfa.available else 0
    n_ob = int(ob.summary.get("products", 0)) if ob and ob.available else 0
    ev4: list[EvidenceItem] = []
    if dfa and dfa.available and bundle.drugsatfda:
        ev4.append(
            _ev(bundle.drugsatfda, f"Drugs@FDA applications for ingredient+form: {n_appl}", n_appl)
        )
    if ob and ob.available and bundle.orange_book:
        ev4.append(
            _ev(bundle.orange_book, f"Orange Book products for ingredient+form: {n_ob}", n_ob)
        )
    if (dfa and dfa.available) or (ob and ob.available):
        st4 = GateStatus.FAIL.value if (n_appl + n_ob) == 0 else GateStatus.UNCERTAIN.value
        why = (
            "no approved application found for this ingredient and form"
            if st4 == "FAIL"
            else f"approved applications exist ({n_appl} Drugs@FDA, {n_ob} Orange Book products); whether Telo can own, contract, or license one needs regulatory review"
        )
    else:
        st4 = GateStatus.UNCERTAIN.value
        why = "Drugs@FDA and Orange Book snapshots not available"
    gates.append(
        GateResult(
            "PG4",
            "Regulatory pathway",
            st4,
            why,
            ev4,
            human_task="regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31)",
        )
    )
    cms = sources.get("S19")
    ev5: list[EvidenceItem] = []
    if cms and cms.available and bundle.cms_partb:
        ev5.append(
            _ev(
                bundle.cms_partb,
                f"CMS Part B rows (proxy only): {cms.summary.get('rows', 0)}",
                cms.summary.get("rows", 0),
            )
        )
    gates.append(
        GateResult(
            "PG5",
            "Demand observability",
            GateStatus.UNCERTAIN.value,
            "national/regional utilization requires hospital, GPO, or wholesaler evidence; CMS is a proxy",
            ev5,
            human_task="obtain utilization evidence (HA-11)",
        )
    )
    gates.append(
        GateResult(
            "PG6",
            "Clinical substitutability",
            GateStatus.UNCERTAIN.value,
            "presentation-specific substitution behavior must be described by clinicians or pharmacists",
            human_task="hospital pharmacy interviews (HA-20)",
        )
    )
    dm = sources.get("S18")
    ev7: list[EvidenceItem] = []
    if dm and dm.available and cand.id in bundle.dailymed:
        ev7.append(
            _ev(
                bundle.dailymed[cand.id],
                f"DailyMed SPLs: {dm.summary.get('spls', 0)} (labelers as a supplier-count proxy)",
                dm.summary.get("spls", 0),
            )
        )
    gates.append(
        GateResult(
            "PG7",
            "Input feasibility",
            GateStatus.UNCERTAIN.value,
            "API, vial, stopper, seal, label, and testing dependencies not yet mapped",
            ev7,
            human_task="supplier and component map (HA-12)",
        )
    )
    scale_note = "volume plausibly compatible with micro nodes; needs demand evidence"
    if cand.id.startswith("sterile_water"):
        scale_note = "diluent volumes are very large relative to a micro node; the workbook flagged scale mismatch"
    gates.append(
        GateResult(
            "PG8",
            "Economic relevance",
            GateStatus.UNCERTAIN.value,
            scale_note,
            human_task="demand evidence (HA-11) and node sizing",
        )
    )
    return gates


def _score_recurrence(fda: SourceSummary | None, today: date) -> tuple[int | None, str, str]:
    if fda is None or not fda.available:
        return None, "no FDA shortage snapshot", "low"
    rows = int(fda.summary.get("rows_ingredient", 0))
    current = int(fda.summary.get("status_counts", {}).get("Current", 0))
    first = fda.summary.get("earliest_initial_posting")
    if current == 0:
        return (
            1,
            f"no current FDA shortage rows ({rows} rows total); resolved history not visible in a single snapshot",
            "low",
        )
    years = None
    if first:
        years = (today - date.fromisoformat(first)).days / 365.25
    if years is None:
        return 3, f"{current} current rows; initial posting date unparsed", "low"
    if years >= 3:
        return (
            5,
            f"{current} current rows; earliest initial posting {first} ({years:.1f} y ago)",
            "medium",
        )
    if years >= 1:
        return (
            4,
            f"{current} current rows; earliest initial posting {first} ({years:.1f} y ago)",
            "medium",
        )
    return 3, f"{current} current rows; earliest initial posting {first} ({years:.1f} y ago)", "low"


def _score_supplier_vulnerability(
    dfa: SourceSummary | None, ob: SourceSummary | None
) -> tuple[int | None, str, str]:
    if (dfa is None or not dfa.available) and (ob is None or not ob.available):
        return None, "no Drugs@FDA or Orange Book snapshot", "low"
    sponsors = set(dfa.summary.get("sponsors", [])) if dfa and dfa.available else set()
    applicants = set(ob.summary.get("applicants", [])) if ob and ob.available else set()
    n = len(sponsors | applicants)
    if n == 0:
        return None, "no application holders found; cannot score", "low"
    score = 5 if n == 1 else 4 if n == 2 else 3 if n <= 4 else 2 if n <= 7 else 1
    return (
        score,
        f"{n} distinct application holders (fewer holders = higher vulnerability = higher score); finished-dose only, API and component concentration not yet mapped",
        "low",
    )


def _score_public_data(sources: dict[str, SourceSummary]) -> tuple[int | None, str, str]:
    hits = 0
    for sid in ("S01", "S01B", "S16", "S17", "S18", "S19"):
        s = sources.get(sid)
        if not s or not s.available:
            continue
        v = s.summary
        if any(
            isinstance(x, int) and x > 0
            for x in (
                v.get("rows_ingredient"),
                v.get("records"),
                v.get("applications"),
                v.get("products"),
                v.get("spls"),
                v.get("rows"),
            )
        ):
            hits += 1
    if not any(s.available for s in sources.values()):
        return None, "no snapshots", "low"
    score = 1 if hits <= 1 else 2 if hits == 2 else 3 if hits == 3 else 4 if hits == 4 else 5
    return score, f"{hits} of 6 official sources return records for the ingredient", "medium"


def score_candidate(
    cand: CandidateSpec, sources: dict[str, SourceSummary], weights: dict[str, float], today: date
) -> list[CriterionScore]:
    wb = WORKBOOK_PROVISIONAL.get(cand.id, {})
    out: list[CriterionScore] = []
    rec, rec_rule, rec_conf = _score_recurrence(sources.get("S01"), today)
    sup, sup_rule, sup_conf = _score_supplier_vulnerability(sources.get("S16"), sources.get("S17"))
    pub, pub_rule, pub_conf = _score_public_data(sources)
    spec: dict[str, tuple[int | None, str, str, str]] = {
        "clinical_criticality": (
            None,
            "expert_pending",
            "hospital role, substitution difficulty, patient consequences: pharmacist/clinician judgment",
            "low",
        ),
        "shortage_recurrence_duration": (rec, "data_rule", rec_rule, rec_conf),
        "supplier_vulnerability": (sup, "data_rule", sup_rule, sup_conf),
        "manufacturing_fit": (
            None,
            "expert_pending",
            "scored against the actual first-node train by a sterile-manufacturing professional",
            "low",
        ),
        "public_data_strength": (pub, "data_rule", pub_rule, pub_conf),
        "regional_relevance": (
            None,
            "expert_pending",
            "whether geography or response speed matters after release/material delays: needs release-time and logistics evidence",
            "low",
        ),
        "demand_contract_fit": (
            None,
            "expert_pending",
            "bounded demand and a credible institutional purchasing model: GPO/wholesaler evidence",
            "low",
        ),
    }
    for crit, w in weights.items():
        score, basis, rule, conf = spec[crit]
        if basis == "data_rule" and score is None:
            basis = "data_unavailable"
        out.append(
            CriterionScore(
                crit, w, score, basis, rule, conf, workbook_provisional_score=wb.get(crit)
            )
        )
    return out


def build_dossier(
    cand: CandidateSpec,
    bundle: EvidenceBundle,
    weights: dict[str, float],
    protocol_version: str,
    today: date | None = None,
) -> Dossier:
    today = today or datetime.now(UTC).date()
    sources: dict[str, SourceSummary] = {}

    def add(sid: str, snap: Snapshot | None, summarize: Callable[[Path], dict[str, Any]]) -> None:
        if snap is None:
            sources[sid] = SourceSummary(sid, None, None, False, {"note": "snapshot not available"})
            return
        sources[sid] = SourceSummary(
            sid, snap.sha256, snap.manifest.retrieved_at.isoformat(), True, summarize(snap.path)
        )

    add("S01", bundle.fda_csv, lambda p: _summarize_fda_csv(read_fda_shortage_csv(p), cand))
    add("S01B", bundle.openfda, lambda p: _summarize_openfda(read_openfda_shortages_zip(p), cand))
    add(
        "S16",
        bundle.drugsatfda,
        lambda p: _summarize_drugsatfda(
            read_drugsatfda_products(p), read_drugsatfda_applications(p), cand
        ),
    )
    add(
        "S17",
        bundle.orange_book,
        lambda p: _summarize_orange_book(read_orange_book_products(p), cand),
    )
    add(
        "S18",
        bundle.dailymed.get(cand.id),
        lambda p: _summarize_dailymed(read_dailymed_spls(p), cand),
    )
    add(
        "S14",
        bundle.bulks_page,
        lambda p: {
            "bulks_list_status": bulks_list_status(
                p.read_text(encoding="utf-8", errors="replace"), cand.ingredient_pattern
            )
        },
    )
    add("S19", bundle.cms_partb, lambda p: _summarize_cms(read_cms_partb_csv(p), cand))

    gates = evaluate_hard_gates(cand, sources, bundle)
    criteria = score_candidate(cand, sources, weights, today)
    scored = [c for c in criteria if c.score is not None]
    covered = sum(c.weight for c in scored)
    partial = sum(c.weight * c.score for c in scored if c.score is not None) if scored else None
    wb_total = None
    if all(c.workbook_provisional_score is not None for c in criteria):
        wb_total = sum(c.weight * float(c.workbook_provisional_score or 0) for c in criteria)
    statuses = {g.status for g in gates}
    outcome = "FAIL" if "FAIL" in statuses else ("UNCERTAIN" if "UNCERTAIN" in statuses else "PASS")
    tasks = sorted({g.human_task for g in gates if g.human_task and g.status != "PASS"})
    complete = outcome == "PASS" and all(c.score is not None for c in criteria)
    return Dossier(
        candidate_id=cand.id,
        ingredient=cand.ingredient,
        presentation=cand.presentation,
        protocol_role=cand.protocol_role,
        generated_at=datetime.now(UTC).isoformat(),
        protocol_version=protocol_version,
        snapshot_ids=bundle.snapshot_ids,
        sources=sources,
        gates=gates,
        criteria=criteria,
        data_partial_score=partial,
        data_weight_covered=covered,
        workbook_provisional_total=wb_total,
        hard_gate_outcome=outcome,
        status="complete" if complete else "partial",
        human_tasks=tasks,
        banner=BANNER,
    )


def dossier_markdown(d: Dossier) -> str:
    lines = [
        f"# Product dossier: {d.ingredient} - {d.presentation}",
        "",
        f"**{d.banner}**",
        "",
        f"Role (protocol 2.5): {d.protocol_role}. Generated {d.generated_at} under protocol v{d.protocol_version}. Status: {d.status}. Hard-gate outcome: {d.hard_gate_outcome}.",
        "",
        "## Frozen evidence",
        "",
    ]
    for sid, s in d.sources.items():
        if s.available:
            lines.append(
                f"- {sid} (sha256 {s.snapshot_sha256[:12] if s.snapshot_sha256 else '?'}, retrieved {s.retrieved_at}): {json.dumps(s.summary, default=str)[:600]}"
            )
        else:
            lines.append(f"- {sid}: not available")
    lines += [
        "",
        "## Hard gates",
        "",
        "| Gate | Status | Rationale | Human task |",
        "|---|---|---|---|",
    ]
    for g in d.gates:
        lines.append(
            f"| {g.gate_id} {g.name} | {g.status} | {g.rationale} | {g.human_task or ''} |"
        )
    lines += [
        "",
        "## Weighted criteria",
        "",
        "| Criterion | Weight | Data score | Basis | Rule / evidence | Confidence | Workbook provisional (tier 5) |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in d.criteria:
        lines.append(
            f"| {c.criterion} | {c.weight:.2f} | {c.score if c.score is not None else '-'} | {c.basis} | {c.rule} | {c.confidence} | {c.workbook_provisional_score if c.workbook_provisional_score is not None else '-'} |"
        )
    lines += [
        "",
        f"Data-based partial score: {d.data_partial_score if d.data_partial_score is not None else 'n/a'} over weight {d.data_weight_covered:.2f} of 1.00. Workbook provisional total (tier 5, not evidence): {d.workbook_provisional_total if d.workbook_provisional_total is not None else 'n/a'}.",
        "",
        "## Open human tasks",
        "",
    ]
    lines += [f"- {t}" for t in d.human_tasks] or ["- none"]
    return "\n".join(lines) + "\n"


def run_screen(
    root: Path = RAW_SNAPSHOTS, out_dir: Path = DOSSIERS, today: date | None = None
) -> dict[str, Any]:
    protocol = load_protocol()
    weights = protocol.product_selection.weights
    longlist = load_longlist()
    bundle = collect_evidence(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    dossiers: list[Dossier] = []
    for cand in longlist.candidates:
        d = build_dossier(cand, bundle, weights, protocol.version, today)
        dossiers.append(d)
        cd = out_dir / cand.id
        cd.mkdir(parents=True, exist_ok=True)
        (cd / "dossier.json").write_text(
            json.dumps(asdict(d), indent=2, default=str), encoding="utf-8"
        )
        (cd / "dossier.md").write_text(dossier_markdown(d), encoding="utf-8")
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_version": protocol.version,
        "weights": weights,
        "snapshot_ids": bundle.snapshot_ids,
        "candidates": [
            {
                "id": d.candidate_id,
                "role": d.protocol_role,
                "hard_gate_outcome": d.hard_gate_outcome,
                "data_partial_score": d.data_partial_score,
                "data_weight_covered": d.data_weight_covered,
                "workbook_provisional_total": d.workbook_provisional_total,
                "status": d.status,
            }
            for d in dossiers
        ],
        "selection": None,
        "banner": BANNER,
        "note": "No candidate is selected by this screen. Selection requires expert scores, resolved gates, and the challenge step (protocol 2.2 step 5).",
    }
    (out_dir / "screen_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )
    return manifest
