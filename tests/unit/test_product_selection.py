from __future__ import annotations

import io
import json
import zipfile
from datetime import UTC, date, datetime
from pathlib import Path

from telo_feasibility.product_selection import (
    CandidateSpec,
    EvidenceBundle,
    build_dossier,
    bulks_list_status,
    collect_evidence,
    load_longlist,
)
from telo_feasibility.provenance import write_snapshot

WEIGHTS = {
    "clinical_criticality": 0.20,
    "shortage_recurrence_duration": 0.20,
    "supplier_vulnerability": 0.15,
    "manufacturing_fit": 0.15,
    "public_data_strength": 0.10,
    "regional_relevance": 0.10,
    "demand_contract_fit": 0.10,
}


def _cand(cid: str = "sodium_bicarbonate_8_4_50ml", **flags: bool) -> CandidateSpec:
    base = {
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
    base.update(flags)
    return CandidateSpec(
        id=cid,
        ingredient="sodium bicarbonate",
        presentation="8.4% 50 mL vial",
        strength_pattern=r"8\.4|84 ?mg",
        ingredient_pattern="sodium bicarbonate",
        dosage_form_pattern="injection|solution",
        protocol_role="case",
        flags=base,
        identity_fixed=True,
    )


def test_longlist_loads_with_at_least_five() -> None:
    ll = load_longlist()
    assert len(ll.candidates) >= 5
    assert {c.id for c in ll.candidates} >= {
        "sodium_bicarbonate_8_4_50ml",
        "norepinephrine_1mgml_4ml",
    }


def test_fda_csv_reader_handles_leading_blank_line_and_padded_headers(tmp_path: Path) -> None:
    from telo_feasibility.product_selection import read_fda_shortage_csv

    p = tmp_path / "Drugshortages.csv"
    p.write_bytes(
        b"\r\nGeneric Name,Company Name, Presentation, Status, Initial Posting Date\r\n"
        b'Sodium Bicarbonate Injection,Exela,"Sodium Bicarbonate, Injection, 84 mg/1 mL", Current ,03/01/2017\r\n'
    )
    rows = read_fda_shortage_csv(p)
    assert rows[0]["Generic Name"] == "Sodium Bicarbonate Injection"
    assert rows[0]["Status"] == "Current" and rows[0]["Initial Posting Date"] == "03/01/2017"


def test_bulks_list_status_detects_not_included() -> None:
    html = "<h2>Included</h2><table><tr><td>Quinacrine</td></tr></table><h2>Not Included</h2><table><tr><td>Sodium bicarbonate</td><td>88 FR 20531</td></tr></table>"
    assert bulks_list_status(html, "sodium bicarbonate") == "not_included"
    assert bulks_list_status(html, "quinacrine") == "included"
    assert bulks_list_status(html, "norepinephrine") == "absent"


def _write_fixture_snapshots(root: Path) -> None:
    ts = datetime(2026, 9, 1, 12, 0, tzinfo=UTC)
    csv_text = (
        "Generic Name,Company Name,Contact Info,Presentation,Type of Update,Date of Update,Availability Information,Related Information,Resolved Note,Reason for Shortage,Therapeutic Category,Status,Change Date,Date Discontinued,Initial Posting Date,Generic Name Note,Generic Name Link,Company Info Link,Availability Link,Related Info Link,Resolved Note Link,Discontinued Note Link\r\n"
        'Sodium Bicarbonate Injection,Exela,x,"Sodium Bicarbonate, Injection, 84 mg/1 mL (NDC 1)",Reverified,08/01/2026,Limited,,,Demand increase,Endocrinology,Current,08/01/2026,,03/01/2017,,,,,,,\r\n'
        'Sodium Bicarbonate Injection,Hospira,x,"Sodium Bicarbonate, Injection, 84 mg/1 mL (NDC 2)",New,07/01/2026,Available,,,Manufacturing delay,Endocrinology,Current,07/01/2026,,03/01/2017,,,,,,,\r\n'
        'Furosemide Injection,Baxter,x,"Furosemide, Injection, 10 mg/mL",New,06/01/2026,Limited,,,Demand,Cardio,Current,06/01/2026,,01/15/2026,,,,,,,\r\n'
    )
    write_snapshot(
        source_id="S01",
        url="u",
        content=csv_text.encode(),
        http_status=200,
        content_type="text/csv",
        license_note="pd",
        filename="Drugshortages.csv",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "drug-shortages-0001-of-0001.json",
            json.dumps(
                {"results": [{"generic_name": "Sodium Bicarbonate Injection", "status": "Current"}]}
            ),
        )
    write_snapshot(
        source_id="S01B",
        url="u",
        content=buf.getvalue(),
        http_status=200,
        content_type="application/zip",
        license_note="cc0",
        filename="drug-shortages-0001-of-0001.json.zip",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    buf2 = io.BytesIO()
    with zipfile.ZipFile(buf2, "w") as z:
        z.writestr(
            "Products.txt",
            "ApplNo\tProductNo\tForm\tStrength\tReferenceDrug\tDrugName\tActiveIngredient\tReferenceStandard\r\n012345\t001\tINJECTABLE;INJECTION\t8.4%\t0\tSODIUM BICARBONATE\tSODIUM BICARBONATE\t0\r\n067890\t001\tINJECTABLE;INJECTION\t8.4%\t0\tSODIUM BICARBONATE\tSODIUM BICARBONATE\t0\r\n",
        )
        z.writestr(
            "Applications.txt",
            "ApplNo\tApplType\tApplPublicNotes\tSponsorName\r\n012345\tANDA\t\tEXELA\r\n067890\tNDA\t\tHOSPIRA\r\n",
        )
    write_snapshot(
        source_id="S16",
        url="u",
        content=buf2.getvalue(),
        http_status=200,
        content_type="application/zip",
        license_note="pd",
        filename="drugsatfda.zip",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    buf3 = io.BytesIO()
    with zipfile.ZipFile(buf3, "w") as z:
        z.writestr(
            "products.txt",
            "Ingredient~DF;Route~Trade_Name~Applicant~Strength~Appl_Type~Appl_No~Product_No~TE_Code~Approval_Date~RLD~RS~Type~Applicant_Full_Name\r\nSODIUM BICARBONATE~INJECTABLE;INJECTION~SODIUM BICARBONATE~EXELA~8.4%~A~012345~001~AP~Jan 1, 2010~No~No~RX~EXELA PHARMA\r\n",
        )
    write_snapshot(
        source_id="S17",
        url="u",
        content=buf3.getvalue(),
        http_status=200,
        content_type="application/zip",
        license_note="pd",
        filename="EOBZIP.zip",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    write_snapshot(
        source_id="S18",
        url="u",
        content=json.dumps(
            {
                "data": [
                    {"setid": "a", "title": "SODIUM BICARBONATE injection, solution 8.4%"},
                    {"setid": "b", "title": "SODIUM BICARBONATE tablet"},
                ]
            }
        ).encode(),
        http_status=200,
        content_type="application/json",
        license_note="nlm",
        filename="spls_sodium_bicarbonate.json",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    write_snapshot(
        source_id="S14",
        url="u",
        content=b"<h2>Included</h2><table><tr><td>Quinacrine</td></tr></table><h2>Not Included</h2><table><tr><td>Sodium bicarbonate</td></tr></table>",
        http_status=200,
        content_type="text/html",
        license_note="pd",
        filename="503b_bulks_list.html",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )
    write_snapshot(
        source_id="S19",
        url="u",
        content=b"HCPCS_Cd,Brnd_Name,Gnrc_Name,Tot_Spndng_2024\r\nJ1940,Lasix,Furosemide,100\r\n",
        http_status=200,
        content_type="text/csv",
        license_note="pd",
        filename="part_b_spending_by_drug_2024.csv",
        access_method="auto",
        robots_allowed=True,
        retrieved_at=ts,
        root=root,
    )


def test_dossier_from_fixture_snapshots(tmp_path: Path) -> None:
    root = tmp_path / "data" / "raw_snapshots"
    _write_fixture_snapshots(root)
    bundle = collect_evidence(root)
    assert bundle.fda_csv is not None and bundle.drugsatfda is not None
    d = build_dossier(_cand(), bundle, WEIGHTS, "1.0.0", today=date(2026, 9, 1))
    by_gate = {g.gate_id: g for g in d.gates}
    assert by_gate["PG2"].status == "PASS" and by_gate["PG3"].status == "PASS"
    assert by_gate["PG4"].status == "UNCERTAIN" and "2 Drugs@FDA" in by_gate["PG4"].rationale
    assert d.hard_gate_outcome == "UNCERTAIN" and d.status == "partial"
    by_crit = {c.criterion: c for c in d.criteria}
    assert by_crit["shortage_recurrence_duration"].score == 5  # current since 2017-03-01, > 3 years
    assert by_crit["supplier_vulnerability"].score == 4  # EXELA + HOSPIRA = 2 holders
    assert (
        by_crit["public_data_strength"].score == 5
    )  # S01, S01B, S16, S17, S18 hit; S19 no rows -> 5 sources
    assert (
        by_crit["clinical_criticality"].score is None
        and by_crit["clinical_criticality"].basis == "expert_pending"
    )
    assert by_crit["clinical_criticality"].workbook_provisional_score == 5
    assert d.data_weight_covered == 0.45 and d.data_partial_score == 0.2 * 5 + 0.15 * 4 + 0.10 * 5
    assert d.sources["S14"].summary["bulks_list_status"] == "not_included"
    assert d.sources["S19"].summary["rows"] == 0


def test_lyophilized_candidate_fails_manufacturing_gate(tmp_path: Path) -> None:
    bundle = EvidenceBundle(None, None, None, None, {}, None, None)
    d = build_dossier(
        _cand("acetazolamide_500mg_vial", lyophilized=True, aqueous_solution=False),
        bundle,
        WEIGHTS,
        "1.0.0",
        today=date(2026, 9, 1),
    )
    assert d.hard_gate_outcome == "FAIL"
    assert {g.gate_id: g.status for g in d.gates}["PG2"] == "FAIL"
    assert all(
        c.score is None or c.basis != "data_rule"
        for c in d.criteria
        if c.basis == "data_unavailable"
    )
    assert d.data_partial_score is None
