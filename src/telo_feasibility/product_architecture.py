"""Product-architecture matching, data layer (design-space assignment, Phase B item 12).

Reads the frozen product dossiers (``data/product_dossiers/<id>/dossier.json``), the
longlist flags, and the two provisional product configurations into one feature record
per candidate presentation. Every feature carries the source snapshot it came from; a
feature no frozen source supports is ``None`` and stays ``None`` until a person supplies
it (sterilization route, substitution difficulty, contractability, regional demand).

The matching rules that map features to architecture families live in configuration
(``config/product_architecture_rules.yaml``) and are applied by ``match``; they are
written only after the Phase A decomposition names which mechanisms bind.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .configs import ProductConfig, load_products
from .product_selection import DOSSIERS, load_longlist

BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"


@dataclass(frozen=True)
class ProductFeatures:
    candidate_id: str
    ingredient: str
    presentation: str
    protocol_role: str
    dossier_generated_at: str
    # shortage history (FDA shortage export S01; openFDA S01B)
    shortage_current_rows: int | None
    shortage_total_rows: int | None
    shortage_years_since_first_posting: float | None
    shortage_reasons: tuple[str, ...]
    shortage_listed_now: bool | None
    # supplier structure (Drugs@FDA S16; Orange Book S17)
    application_count: int | None
    anda_count: int | None
    nda_count: int | None
    orange_book_applicants: int | None
    # pathway and demand proxies (503B bulks list S14; CMS Part B S19; DailyMed S18)
    bulks_list_status: str | None
    cms_partb_rows: int | None
    dailymed_injectable_titles: int | None
    # archetype flags (longlist configuration)
    flags: dict[str, bool]
    # provisional configuration parameters (tier 5 illustrative) where a product config exists
    annual_demand_units: float | None
    shelf_life_months: float | None
    units_per_batch: float | None
    material_lead_time_days: float | None
    # screen outcome
    hard_gate_outcome: str
    data_partial_score: float | None
    # human-only features (None until evidence exists)
    sterilization_route: str | None = None
    substitution_difficulty: str | None = None
    contractability: str | None = None
    evidence: dict[str, str] = field(default_factory=dict)

    def as_row(self) -> dict[str, Any]:
        row = asdict(self)
        row["shortage_reasons"] = "; ".join(self.shortage_reasons)
        row["flags"] = json.dumps(self.flags, sort_keys=True)
        row["evidence"] = json.dumps(self.evidence, sort_keys=True)
        return row


def _years_between(earlier: str | None, later: str) -> float | None:
    if not earlier:
        return None
    d0 = date.fromisoformat(earlier[:10])
    d1 = datetime.fromisoformat(later.replace("Z", "+00:00")).date()
    return round((d1 - d0).days / 365.25, 2)


def _src(d: dict[str, Any], sid: str) -> tuple[dict[str, Any], str | None]:
    s = d.get("sources", {}).get(sid)
    if not s or not s.get("available"):
        return {}, None
    sha = s.get("snapshot_sha256") or ""
    return dict(s.get("summary") or {}), f"{sid}:{sha[:12]}"


def features_from_dossier(
    d: dict[str, Any], flags: dict[str, bool], product: ProductConfig | None
) -> ProductFeatures:
    ev: dict[str, str] = {}
    s01, e01 = _src(d, "S01")
    _s01b, e01b = _src(d, "S01B")
    s16, e16 = _src(d, "S16")
    s17, e17 = _src(d, "S17")
    s14, e14 = _src(d, "S14")
    s19, e19 = _src(d, "S19")
    s18, e18 = _src(d, "S18")
    counts = s01.get("status_counts") or {}
    current = int(counts.get("Current", 0)) if s01 else None
    total = int(s01["rows_ingredient"]) if "rows_ingredient" in s01 else None
    if e01:
        ev.update(
            {"shortage_current_rows": e01, "shortage_total_rows": e01, "shortage_reasons": e01}
        )
    if e01b:
        ev["openfda_records"] = e01b
    years = _years_between(s01.get("earliest_initial_posting"), d["generated_at"]) if s01 else None
    if years is not None and e01:
        ev["shortage_years_since_first_posting"] = e01
    app_types = s16.get("application_types") or {}
    if e16:
        ev.update({"application_count": e16, "anda_count": e16, "nda_count": e16})
    if e17:
        ev["orange_book_applicants"] = e17
    if e14:
        ev["bulks_list_status"] = e14
    if e19:
        ev["cms_partb_rows"] = e19
    if e18:
        ev["dailymed_injectable_titles"] = e18
    p = product.parameters if product else None

    def base(key: str) -> float | None:
        if product is None or p is None or key not in p.parameters:
            return None
        ev[key] = f"config:{product.path.name}:tier{p.parameters[key].evidence_tier.value}"
        return p.base(key)

    return ProductFeatures(
        candidate_id=d["candidate_id"],
        ingredient=d["ingredient"],
        presentation=d["presentation"],
        protocol_role=d["protocol_role"],
        dossier_generated_at=d["generated_at"],
        shortage_current_rows=current,
        shortage_total_rows=total,
        shortage_years_since_first_posting=years,
        shortage_reasons=tuple(s01.get("reasons") or ()),
        shortage_listed_now=(current > 0) if current is not None else None,
        application_count=int(s16["applications"]) if "applications" in s16 else None,
        anda_count=int(app_types["ANDA"]) if "ANDA" in app_types else None,
        nda_count=int(app_types["NDA"]) if "NDA" in app_types else None,
        orange_book_applicants=len(s17["applicants"]) if "applicants" in s17 else None,
        bulks_list_status=str(s14["bulks_list_status"]) if "bulks_list_status" in s14 else None,
        cms_partb_rows=int(s19["rows"]) if "rows" in s19 else None,
        dailymed_injectable_titles=(
            int(s18["injectable_titles"]) if "injectable_titles" in s18 else None
        ),
        flags=dict(flags),
        annual_demand_units=base("annual_demand_units"),
        shelf_life_months=base("shelf_life_months"),
        units_per_batch=base("units_per_batch"),
        material_lead_time_days=base("material_lead_time_days"),
        hard_gate_outcome=str(d.get("hard_gate_outcome", "UNCERTAIN")),
        data_partial_score=d.get("data_partial_score"),
        evidence=ev,
    )


def load_product_features(
    dossiers: Path = DOSSIERS, products: dict[str, ProductConfig] | None = None
) -> list[ProductFeatures]:
    products = products if products is not None else load_products()
    flags_by_id = {c.id: dict(c.flags) for c in load_longlist().candidates}
    out: list[ProductFeatures] = []
    for path in sorted(dossiers.glob("*/dossier.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        cid = str(d["candidate_id"])
        out.append(features_from_dossier(d, flags_by_id.get(cid, {}), products.get(cid)))
    if not out:
        raise FileNotFoundError(f"no dossiers under {dossiers}")
    return out


def write_features_csv(features: list[ProductFeatures], path: Path) -> Path:
    rows = [f.as_row() for f in features]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path
