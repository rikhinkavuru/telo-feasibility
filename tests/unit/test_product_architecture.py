"""Feature extraction from the frozen dossiers for product-architecture matching."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from telo_feasibility.product_architecture import (
    ProductFeatures,
    features_from_dossier,
    load_product_features,
    write_features_csv,
)
from telo_feasibility.product_selection import DOSSIERS

SODIUM = "sodium_bicarbonate_8_4_50ml"
NOREPI = "norepinephrine_1mgml_4ml"


@pytest.fixture(scope="module")
def feats() -> dict[str, ProductFeatures]:
    if not DOSSIERS.exists():
        pytest.skip("dossiers not built")
    return {f.candidate_id: f for f in load_product_features()}


def test_every_dossier_yields_a_feature_record(feats: dict[str, ProductFeatures]) -> None:
    assert len(feats) == len(list(DOSSIERS.glob("*/dossier.json"))) >= 5
    for f in feats.values():
        assert f.hard_gate_outcome in {"PASS", "FAIL", "UNCERTAIN"}
        # every populated snapshot-derived feature names its snapshot
        for key in ("shortage_current_rows", "application_count", "bulks_list_status"):
            if getattr(f, key) is not None:
                assert key in f.evidence and ":" in f.evidence[key], (f.candidate_id, key)
        # human-only features stay empty until evidence exists
        assert f.sterilization_route is None and f.contractability is None


def test_frozen_snapshot_values_are_read_not_guessed(feats: dict[str, ProductFeatures]) -> None:
    d = json.loads((DOSSIERS / SODIUM / "dossier.json").read_text(encoding="utf-8"))
    s01 = d["sources"]["S01"]["summary"]
    f = feats[SODIUM]
    assert f.shortage_current_rows == s01["status_counts"]["Current"]
    assert f.shortage_total_rows == s01["rows_ingredient"]
    assert f.shortage_listed_now is True
    assert (
        f.shortage_years_since_first_posting is not None
        and f.shortage_years_since_first_posting > 9
    )
    assert f.bulks_list_status == d["sources"]["S14"]["summary"]["bulks_list_status"]
    assert f.application_count == d["sources"]["S16"]["summary"]["applications"]
    assert f.annual_demand_units == 1_200_000.0  # tier-5 config value, labeled as such
    assert (
        f.evidence["annual_demand_units"].startswith("config:")
        and "tier5" in f.evidence["annual_demand_units"]
    )


def test_unlisted_product_and_missing_config(feats: dict[str, ProductFeatures]) -> None:
    n = feats[NOREPI]
    assert n.shortage_current_rows == 0 and n.shortage_listed_now is False
    others = [f for cid, f in feats.items() if cid not in (SODIUM, NOREPI)]
    assert others and all(f.annual_demand_units is None for f in others)
    assert any(f.flags.get("lyophilized") for f in feats.values())


def test_features_from_dossier_handles_absent_sources() -> None:
    d = {
        "candidate_id": "x_vial",
        "ingredient": "x",
        "presentation": "vial",
        "protocol_role": "reserve",
        "generated_at": "2026-09-02T00:00:00+00:00",
        "sources": {"S01": {"available": False}},
        "hard_gate_outcome": "UNCERTAIN",
    }
    f = features_from_dossier(d, {"aqueous_solution": True}, None)
    assert f.shortage_current_rows is None and f.shortage_listed_now is None
    assert f.evidence == {} and f.flags == {"aqueous_solution": True}


def test_csv_round_trip(tmp_path: Path, feats: dict[str, ProductFeatures]) -> None:
    out = write_features_csv(list(feats.values()), tmp_path / "f.csv")
    rows = list(csv.DictReader(out.open(encoding="utf-8")))
    assert len(rows) == len(feats)
    assert json.loads(rows[0]["evidence"]) is not None
