"""Provenance: hashing, protocol verification, snapshot manifests, run manifests.

Everything that later claims "this number came from there" passes through here.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from . import __version__
from .schemas import Protocol, RunManifest, SnapshotManifest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = PACKAGE_ROOT / "protocol" / "protocol.yaml"
GATES_PATH = PACKAGE_ROOT / "config" / "regulatory_gates.yaml"
RAW_SNAPSHOTS = PACKAGE_ROOT / "data" / "raw_snapshots"
MANIFESTS = PACKAGE_ROOT / "results" / "manifests"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def stable_hash64(text: str) -> int:
    """Process- and version-stable 64-bit hash for seed keys (BLAKE2b, 8 bytes)."""
    return int.from_bytes(hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest(), "big")


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def hash_config(obj: Any) -> str:
    return sha256_bytes(canonical_json(obj).encode("utf-8"))


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


def load_protocol(path: Path = PROTOCOL_PATH) -> Protocol:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Protocol.model_validate(raw)


@dataclass(frozen=True)
class HashCheck:
    document_id: str
    filename: str
    expected_sha256: str
    found_path: Path | None
    actual_sha256: str | None

    @property
    def ok(self) -> bool:
        return self.actual_sha256 == self.expected_sha256


def verify_protocol_hashes(protocol: Protocol, search_dirs: list[Path]) -> list[HashCheck]:
    """Locate each protocol source document and compare its sha256 with the frozen value."""
    checks: list[HashCheck] = []
    for doc in protocol.protocol.source_documents:
        found: Path | None = None
        for d in search_dirs:
            candidate = d / doc.filename
            if candidate.is_file():
                found = candidate
                break
        actual = sha256_file(found) if found else None
        checks.append(HashCheck(doc.id, doc.filename, doc.sha256, found, actual))
    return checks


def protocol_file_sha256(path: Path = PROTOCOL_PATH) -> str:
    return sha256_file(path)


# ---------------------------------------------------------------------------
# Environment capture
# ---------------------------------------------------------------------------


def git_state(repo: Path = PACKAGE_ROOT) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain", "--", str(repo)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return commit, bool(status.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None


def build_run_manifest(
    run_id: str,
    *,
    protocol: Protocol,
    config_objects: dict[str, Any],
    master_seed: int | None,
    n_runs: int | None,
    illustrative: bool,
    gate_outcomes: dict[str, dict[str, str]] | None = None,
    notes: str = "",
) -> RunManifest:
    commit, dirty = git_state()
    return RunManifest(
        run_id=run_id,
        created_at=datetime.now(UTC),
        protocol_version=protocol.version,
        protocol_sha256=protocol_file_sha256(),
        package_version=__version__,
        git_commit=commit,
        git_dirty=dirty,
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        config_hashes={k: hash_config(v) for k, v in config_objects.items()},
        master_seed=master_seed,
        n_runs=n_runs,
        illustrative=illustrative,
        gate_outcomes=gate_outcomes or {},
        notes=notes,
    )


def write_manifest(manifest: RunManifest, directory: Path = MANIFESTS) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{manifest.run_id}.json"
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------


def snapshot_dir(source_id: str, retrieved_at: datetime, root: Path = RAW_SNAPSHOTS) -> Path:
    return root / source_id / retrieved_at.strftime("%Y-%m-%d")


def write_snapshot(
    *,
    source_id: str,
    url: str,
    content: bytes | None,
    http_status: int | None,
    content_type: str,
    license_note: str,
    filename: str,
    access_method: str,
    robots_allowed: bool | None,
    notes: str = "",
    retrieved_at: datetime | None = None,
    root: Path = RAW_SNAPSHOTS,
    manifest_name: str | None = None,
) -> SnapshotManifest:
    """Persist an unmodified raw payload next to its manifest. Human tasks store no payload.

    Each fetch gets its own manifest (``<filename>.manifest.json``) so several fetches of one
    source on one day never overwrite each other. Human tasks default to ``task_<n>.manifest.json``.
    """
    ts = retrieved_at or datetime.now(UTC)
    d = snapshot_dir(source_id, ts, root)
    d.mkdir(parents=True, exist_ok=True)
    if manifest_name is None:
        if content is not None:
            manifest_name = f"{filename}.manifest.json"
        else:
            n = len(list(d.glob("task_*.manifest.json")))
            manifest_name = f"task_{n + 1:03d}.manifest.json"
    raw_path: str | None = None
    digest: str | None = None
    size: int | None = None
    if content is not None:
        target = d / filename
        target.write_bytes(content)
        raw_path = str(target.relative_to(root.parent.parent))
        digest = sha256_bytes(content)
        size = len(content)
    manifest = SnapshotManifest(
        source_id=source_id,
        url=url,
        retrieved_at=ts,
        http_status=http_status,
        sha256=digest,
        content_type=content_type,
        size_bytes=size,
        license_note=license_note,
        raw_path=raw_path,
        access_method=access_method,
        robots_allowed=robots_allowed,
        notes=notes,
    )
    (d / manifest_name).write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return manifest


def read_manifests(root: Path = RAW_SNAPSHOTS) -> list[SnapshotManifest]:
    out: list[SnapshotManifest] = []
    if not root.exists():
        return out
    for p in sorted(root.glob("*/*/*.manifest.json")):
        out.append(SnapshotManifest.model_validate_json(p.read_text(encoding="utf-8")))
    return out
