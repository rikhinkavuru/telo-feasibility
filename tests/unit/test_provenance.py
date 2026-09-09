"""Provenance: hashing stability, protocol loading, snapshot manifests."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from telo_feasibility.provenance import (
    GATES_PATH,
    hash_config,
    load_protocol,
    read_manifests,
    sha256_bytes,
    stable_hash64,
    write_snapshot,
)
from telo_feasibility.schemas import (
    FROZEN_STRATEGY_IDS,
    GateSet,
    GateStatus,
    SnapshotManifest,
    StrategyId,
)


def test_stable_hash64_is_deterministic() -> None:
    assert stable_hash64("site:A") == stable_hash64("site:A")
    assert stable_hash64("site:A") != stable_hash64("site:B")
    assert 0 <= stable_hash64("x") < 2**64


def test_hash_config_is_order_independent() -> None:
    assert hash_config({"a": 1, "b": [1, 2]}) == hash_config({"b": [1, 2], "a": 1})
    assert sha256_bytes(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_protocol_loads_and_is_frozen() -> None:
    p = load_protocol()
    assert p.protocol.status == "frozen"
    assert p.version == "1.0.0"
    assert abs(sum(p.product_selection.weights.values()) - 1.0) < 1e-9
    assert [s.id for s in p.strategies] == list(FROZEN_STRATEGY_IDS)
    assert p.service_thresholds.fill_rate_mean_min == 0.99
    assert p.service_thresholds.recovery_window_days == 30


def test_gates_load_all_uncertain_and_r3_gate_present() -> None:
    g = GateSet.model_validate(yaml.safe_load(GATES_PATH.read_text(encoding="utf-8")))
    # 15 gates from revision R002, plus G16 (alternate source qualification) from R007
    assert len(g.gates) == 16
    assert {x.status for x in g.gates} == {GateStatus.UNCERTAIN}
    assert g.by_id("G15").applies_to_strategies == [StrategyId.S6]
    assert g.by_id("G16").applies_to_strategies == [StrategyId.S9, StrategyId.S18, StrategyId.S19]
    assert all(not x.reviewer for x in g.gates)


def test_auto_snapshot_requires_payload_fields() -> None:
    with pytest.raises(ValidationError, match="missing"):
        SnapshotManifest(
            source_id="S01",
            url="https://example.invalid",
            retrieved_at=datetime.now(UTC),
            license_note="public domain",
            access_method="auto",
        )


def test_write_and_read_snapshot_roundtrip(tmp_path: Path) -> None:
    root = tmp_path / "data" / "raw_snapshots"
    m = write_snapshot(
        source_id="S16",
        url="https://example.invalid/drugsatfda.zip",
        content=b"hello",
        http_status=200,
        content_type="application/zip",
        license_note="US government work",
        filename="drugsatfda.zip",
        access_method="auto",
        robots_allowed=True,
        root=root,
    )
    assert m.sha256 == sha256_bytes(b"hello")
    assert m.size_bytes == 5
    back = read_manifests(root)
    assert len(back) == 1 and back[0].source_id == "S16"


def test_human_snapshot_records_task_without_payload(tmp_path: Path) -> None:
    root = tmp_path / "data" / "raw_snapshots"
    m = write_snapshot(
        source_id="S21",
        url="https://www.ashp.org/drug-shortages",
        content=None,
        http_status=None,
        content_type="",
        license_note="copyrighted; manual retrieval",
        filename="none",
        access_method="human",
        robots_allowed=False,
        notes="HUMAN-ACQUISITION-TASK",
        root=root,
    )
    assert m.raw_path is None and m.sha256 is None
