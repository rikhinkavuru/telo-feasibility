"""Source acquisition: robots-aware, rate-limited freezing of official sources.

Rules (task section 5):

* Every fetch records retrieval time, URL, HTTP status, sha256, content type, size,
  license note, and the unmodified payload, through ``provenance.write_snapshot``.
* ``robots.txt`` is fetched once per host and honored, including the non-standard
  ``Hit-rate`` and ``Visiting-hours`` directives used by accessdata.fda.gov. A path the
  robots file disallows is not fetched; a HUMAN-ACQUISITION-TASK manifest is written.
* Sources marked ``human`` are never fetched; their task text is written to the manifest.
* Payloads larger than the per-fetch cap are abandoned and recorded, never truncated.
* No access control is circumvented. Failures are recorded, not retried into submission.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import robotparser
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import httpx
import yaml
from pydantic import Field

from .provenance import PACKAGE_ROOT, RAW_SNAPSHOTS, write_snapshot
from .schemas import EvidenceTier, SnapshotManifest, StrictModel

SOURCES_PATH = PACKAGE_ROOT / "config" / "sources.yaml"
EASTERN = ZoneInfo("America/New_York")


class FetchSpec(StrictModel):
    key: str
    url: str
    filename: str
    method: str = Field(default="GET", pattern=r"^(GET|POST)$")
    body: dict[str, Any] | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    max_bytes: int = Field(default=5_000_000, ge=1)


class SourceSpec(StrictModel):
    id: str = Field(pattern=r"^S\d{2,3}[A-Z]?$")
    name: str
    domain: str
    tier: EvidenceTier
    landing_url: str
    access_method: str = Field(pattern=r"^(auto|human)$")
    license_note: str
    robots_note: str = ""
    min_interval_seconds: float = Field(default=5.0, ge=0)
    visiting_hours_edt: tuple[str, str] | None = None
    update_frequency: str = ""
    notes: str = ""
    human_task: str = ""
    fetches: list[FetchSpec] = Field(default_factory=list)


class SourceRegistry(StrictModel):
    version: str
    user_agent: str
    default_min_interval_seconds: float = 5.0
    sources: list[SourceSpec]

    def by_id(self, sid: str) -> SourceSpec:
        for s in self.sources:
            if s.id == sid:
                return s
        raise KeyError(sid)


def load_sources(path: Path = SOURCES_PATH) -> SourceRegistry:
    with path.open("r", encoding="utf-8") as f:
        return SourceRegistry.model_validate(yaml.safe_load(f))


# ---------------------------------------------------------------------------
# robots.txt handling
# ---------------------------------------------------------------------------


@dataclass
class HostRules:
    parser: robotparser.RobotFileParser | None
    fetched: bool
    status: int | None
    hit_rate_seconds: float | None = None
    crawl_delay_seconds: float | None = None
    visiting_hours: tuple[str, str] | None = None

    @property
    def required_interval(self) -> float:
        return max(self.hit_rate_seconds or 0.0, self.crawl_delay_seconds or 0.0)


@dataclass
class RobotsCache:
    client: httpx.Client
    user_agent: str
    rules: dict[str, HostRules] = field(default_factory=dict)

    def _load(self, host: str, scheme: str) -> HostRules:
        if host in self.rules:
            return self.rules[host]
        url = f"{scheme}://{host}/robots.txt"
        parser: robotparser.RobotFileParser | None = None
        status: int | None = None
        hit: float | None = None
        hours: tuple[str, str] | None = None
        try:
            r = self.client.get(url, headers={"User-Agent": self.user_agent})
            status = r.status_code
            if r.status_code == 200 and "text" in r.headers.get("content-type", "text/plain"):
                parser = robotparser.RobotFileParser()
                lines = r.text.splitlines()
                parser.parse(lines)
                for line in lines:
                    low = line.strip().lower()
                    if low.startswith("hit-rate:"):
                        try:
                            hit = float(low.split(":", 1)[1].split("#")[0].strip())
                        except ValueError:
                            hit = None
                    elif low.startswith("visiting-hours:"):
                        spec = low.split(":", 1)[1].split("#")[0].strip()
                        parsed = _parse_visiting_hours(spec)
                        if parsed:
                            hours = parsed
        except httpx.HTTPError:
            status = None
        crawl: float | None = None
        if parser is not None:
            cd = parser.crawl_delay(self.user_agent)
            if cd is None:
                cd = parser.crawl_delay("*")
            crawl = float(cd) if cd is not None else None
        rules = HostRules(
            parser=parser,
            fetched=status is not None,
            status=status,
            hit_rate_seconds=hit,
            crawl_delay_seconds=crawl,
            visiting_hours=hours,
        )
        self.rules[host] = rules
        return rules

    def allowed(self, url: str) -> bool:
        parts = urlsplit(url)
        rules = self._load(parts.netloc, parts.scheme or "https")
        if rules.parser is None:
            return True  # no robots file retrievable: standard interpretation is allowed
        return rules.parser.can_fetch(self.user_agent, url)

    def host_rules(self, url: str) -> HostRules:
        parts = urlsplit(url)
        return self._load(parts.netloc, parts.scheme or "https")


def _parse_visiting_hours(spec: str) -> tuple[str, str] | None:
    """Parse '23:00EDT-05:00EDT' (accessdata form) into ('23:00', '05:00')."""
    spec = spec.replace("edt", "").replace("est", "").replace(" ", "")
    if "-" not in spec:
        return None
    a, b = spec.split("-", 1)
    if len(a) >= 4 and len(b) >= 4 and ":" in a and ":" in b:
        return a, b
    return None


def in_visiting_window(now_utc: datetime, window: tuple[str, str]) -> bool:
    """True when the Eastern local time is inside a possibly-overnight [start, end) window."""
    local = now_utc.astimezone(EASTERN)
    minutes = local.hour * 60 + local.minute
    sh, sm = (int(x) for x in window[0].split(":"))
    eh, em = (int(x) for x in window[1].split(":"))
    start = sh * 60 + sm
    end = eh * 60 + em
    if start <= end:
        return start <= minutes < end
    return minutes >= start or minutes < end


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


@dataclass
class AcquireOptions:
    root: Path = RAW_SNAPSHOTS
    dry_run: bool = False
    override_visiting_hours: str | None = None  # a logged reason, or None to respect the window
    timeout_seconds: float = 90.0
    now: datetime | None = None


def _now(opts: AcquireOptions) -> datetime:
    return opts.now or datetime.now(UTC)


def human_manifest(
    spec: SourceSpec, opts: AcquireOptions, reason: str, url: str | None = None
) -> SnapshotManifest:
    return write_snapshot(
        source_id=spec.id,
        url=url or spec.landing_url,
        content=None,
        http_status=None,
        content_type="",
        license_note=spec.license_note,
        filename="none",
        access_method="human",
        robots_allowed=None,
        notes=f"HUMAN-ACQUISITION-TASK: {reason}",
        retrieved_at=_now(opts),
        root=opts.root,
    )


def fetch_one(
    client: httpx.Client,
    robots: RobotsCache,
    spec: SourceSpec,
    fetch: FetchSpec,
    opts: AcquireOptions,
    user_agent: str,
) -> SnapshotManifest:
    """Fetch one payload under the source's rules and write its manifest."""
    if not robots.allowed(fetch.url):
        return human_manifest(
            spec,
            opts,
            f"robots.txt disallows {fetch.url}; retrieve manually if terms permit",
            fetch.url,
        )
    rules = robots.host_rules(fetch.url)
    window = spec.visiting_hours_edt or rules.visiting_hours
    if window and not in_visiting_window(_now(opts), window) and not opts.override_visiting_hours:
        return human_manifest(
            spec,
            opts,
            f"outside robots Visiting-hours {window[0]}-{window[1]} Eastern; rerun inside the window or pass --override-visiting-hours with a reason",
            fetch.url,
        )
    if opts.dry_run:
        return human_manifest(spec, opts, f"dry run; would fetch {fetch.url}", fetch.url)

    headers = {"User-Agent": user_agent, **fetch.headers}
    status: int | None = None
    content_type = ""
    note = ""
    payload: bytes | None = None
    try:
        if fetch.method == "POST":
            req = client.build_request("POST", fetch.url, json=fetch.body, headers=headers)
        else:
            req = client.build_request("GET", fetch.url, headers=headers)
        with client.stream(
            req.method,
            req.url,
            headers=headers,
            json=fetch.body if fetch.method == "POST" else None,
        ) as r:
            status = r.status_code
            content_type = r.headers.get("content-type", "")
            declared = r.headers.get("content-length")
            if declared and declared.isdigit() and int(declared) > fetch.max_bytes:
                note = f"declared size {declared} exceeds cap {fetch.max_bytes}; not downloaded"
            elif status >= 400:
                note = f"HTTP {status}"
            else:
                chunks: list[bytes] = []
                total = 0
                for chunk in r.iter_bytes():
                    total += len(chunk)
                    if total > fetch.max_bytes:
                        note = f"payload exceeded cap {fetch.max_bytes} bytes during download; abandoned"
                        chunks = []
                        break
                    chunks.append(chunk)
                if not note:
                    payload = b"".join(chunks)
    except httpx.HTTPError as e:
        note = f"transport error: {type(e).__name__}: {e}"

    if opts.override_visiting_hours and window:
        note = (
            note + "; " if note else ""
        ) + f"visiting-hours overridden: {opts.override_visiting_hours}"
    return write_snapshot(
        source_id=spec.id,
        url=fetch.url,
        content=payload,
        http_status=status,
        content_type=content_type,
        license_note=spec.license_note,
        filename=fetch.filename,
        access_method="auto" if payload is not None else "human",
        robots_allowed=True,
        notes=note
        if payload is not None
        else f"HUMAN-ACQUISITION-TASK: automatic fetch failed ({note or 'unknown'})",
        retrieved_at=_now(opts),
        root=opts.root,
    )


def acquire(
    registry: SourceRegistry,
    source_ids: list[str] | None,
    opts: AcquireOptions,
    client: httpx.Client | None = None,
    sleep: Any = time.sleep,
) -> list[SnapshotManifest]:
    """Acquire the selected sources (all when ``source_ids`` is None), one manifest per fetch."""
    own_client = client is None
    cl = client or httpx.Client(follow_redirects=True, timeout=opts.timeout_seconds)
    robots = RobotsCache(client=cl, user_agent=registry.user_agent)
    manifests: list[SnapshotManifest] = []
    last_hit: dict[str, float] = {}
    try:
        for spec in registry.sources:
            if source_ids and spec.id not in source_ids:
                continue
            if spec.access_method == "human" or not spec.fetches:
                manifests.append(
                    human_manifest(spec, opts, spec.human_task or "human retrieval required")
                )
                continue
            for fetch in spec.fetches:
                host = urlsplit(fetch.url).netloc
                rules = robots.host_rules(fetch.url)
                interval = max(
                    spec.min_interval_seconds,
                    rules.required_interval,
                    registry.default_min_interval_seconds,
                )
                if host in last_hit and not opts.dry_run:
                    wait = interval - (time.monotonic() - last_hit[host])
                    if wait > 0:
                        sleep(wait)
                manifests.append(fetch_one(cl, robots, spec, fetch, opts, registry.user_agent))
                last_hit[host] = time.monotonic()
    finally:
        if own_client:
            cl.close()
    return manifests
