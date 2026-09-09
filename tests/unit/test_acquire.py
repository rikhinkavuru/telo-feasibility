"""Acquisition: robots, visiting hours, size caps, failures, human tasks (offline, mock transport)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import httpx

from telo_feasibility.acquire import (
    AcquireOptions,
    FetchSpec,
    SourceRegistry,
    SourceSpec,
    acquire,
    in_visiting_window,
    load_sources,
)
from telo_feasibility.provenance import read_manifests
from telo_feasibility.schemas import EvidenceTier

ROBOTS_ACCESSDATA = """User-agent: *
Disallow: /scripts/warningletters/
Crawl-delay: 7
Hit-rate: 30 # wait 30 seconds
Visiting-hours: 23:00EDT-05:00EDT
"""


def test_crawl_delay_and_hit_rate_both_parsed(tmp_path: Path) -> None:
    from telo_feasibility.acquire import RobotsCache

    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=ROBOTS_ACCESSDATA, headers={"content-type": "text/plain"})

    cache = RobotsCache(client=_client(handler), user_agent="TeloTest/0")
    rules = cache.host_rules("https://accessdata.test/scripts/x.cfm")
    assert rules.hit_rate_seconds == 30.0 and rules.crawl_delay_seconds == 7.0
    assert rules.required_interval == 30.0
    assert rules.visiting_hours == ("23:00", "05:00")
    assert not cache.allowed("https://accessdata.test/scripts/warningletters/x")
    assert cache.allowed("https://accessdata.test/scripts/drugshortages/x")


def _registry(*specs: SourceSpec) -> SourceRegistry:
    return SourceRegistry(
        version="t", user_agent="TeloTest/0", default_min_interval_seconds=0.0, sources=list(specs)
    )


def _spec(
    sid: str,
    url: str,
    *,
    max_bytes: int = 1000,
    hours: tuple[str, str] | None = None,
    method: str = "human" if False else "auto",
) -> SourceSpec:
    return SourceSpec(
        id=sid,
        name="t",
        domain="t",
        tier=EvidenceTier.OFFICIAL,
        landing_url=url,
        access_method=method,
        license_note="public domain",
        min_interval_seconds=0.0,
        visiting_hours_edt=hours,
        fetches=[FetchSpec(key="k", url=url, filename="payload.bin", max_bytes=max_bytes)],
    )


def _client(handler: object) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)  # type: ignore[arg-type]


def test_registry_file_loads_and_has_human_and_auto_sources() -> None:
    reg = load_sources()
    ids = [s.id for s in reg.sources]
    assert ids[0] == "S01" and "S21" in ids
    assert reg.by_id("S21").access_method == "human" and reg.by_id("S21").human_task
    assert all(s.license_note for s in reg.sources)
    assert all(f.max_bytes >= 1 for s in reg.sources for f in s.fetches)


def test_visiting_window_overnight() -> None:
    win = ("23:00", "05:00")
    # 03:30 UTC in September = 23:30 EDT previous day -> inside
    assert in_visiting_window(datetime(2026, 9, 2, 3, 30, tzinfo=UTC), win)
    # 18:30 UTC = 14:30 EDT -> outside
    assert not in_visiting_window(datetime(2026, 9, 1, 18, 30, tzinfo=UTC), win)


def test_successful_fetch_writes_payload_and_manifest(tmp_path: Path) -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/robots.txt":
            return httpx.Response(
                200,
                text="User-agent: *\nDisallow: /private/\n",
                headers={"content-type": "text/plain"},
            )
        return httpx.Response(200, content=b"a,b\n1,2\n", headers={"content-type": "text/csv"})

    reg = _registry(_spec("S90", "https://example.test/data.csv"))
    out = acquire(
        reg,
        None,
        AcquireOptions(root=tmp_path, now=datetime(2026, 9, 1, 12, 0, tzinfo=UTC)),
        client=_client(handler),
        sleep=lambda s: None,
    )
    assert len(out) == 1
    m = out[0]
    assert m.access_method == "auto" and m.http_status == 200 and m.size_bytes == 8
    assert m.sha256 is not None and m.robots_allowed is True
    assert (tmp_path / "S90" / "2026-09-01" / "payload.bin").read_bytes() == b"a,b\n1,2\n"
    assert read_manifests(tmp_path)[0].source_id == "S90"


def test_robots_disallow_becomes_human_task_without_fetching(tmp_path: Path) -> None:
    calls: list[str] = []

    def handler(req: httpx.Request) -> httpx.Response:
        calls.append(req.url.path)
        if req.url.path == "/robots.txt":
            return httpx.Response(
                200,
                text="User-agent: *\nDisallow: /private/\n",
                headers={"content-type": "text/plain"},
            )
        return httpx.Response(200, content=b"secret")

    reg = _registry(_spec("S91", "https://example.test/private/x.csv"))
    out = acquire(
        reg, None, AcquireOptions(root=tmp_path), client=_client(handler), sleep=lambda s: None
    )
    assert out[0].access_method == "human" and "robots.txt disallows" in out[0].notes
    assert "/private/x.csv" not in calls


def test_visiting_hours_respected_and_overridable(tmp_path: Path) -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/robots.txt":
            return httpx.Response(
                200, text=ROBOTS_ACCESSDATA, headers={"content-type": "text/plain"}
            )
        return httpx.Response(200, content=b"ok")

    reg = _registry(_spec("S92", "https://accessdata.test/scripts/x.cfm"))
    daytime = datetime(2026, 9, 1, 18, 30, tzinfo=UTC)
    out = acquire(
        reg,
        None,
        AcquireOptions(root=tmp_path, now=daytime),
        client=_client(handler),
        sleep=lambda s: None,
    )
    assert out[0].access_method == "human" and "Visiting-hours" in out[0].notes
    out2 = acquire(
        reg,
        None,
        AcquireOptions(root=tmp_path, now=daytime, override_visiting_hours="author approved"),
        client=_client(handler),
        sleep=lambda s: None,
    )
    assert out2[0].access_method == "auto" and "overridden: author approved" in out2[0].notes


def test_size_cap_abandons_payload(tmp_path: Path) -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, content=b"x" * 5000)

    reg = _registry(_spec("S93", "https://example.test/big.bin", max_bytes=100))
    out = acquire(
        reg, None, AcquireOptions(root=tmp_path), client=_client(handler), sleep=lambda s: None
    )
    assert out[0].access_method == "human" and "cap 100" in out[0].notes
    assert out[0].raw_path is None
    assert not list((tmp_path / "S93").glob("*/big.bin"))


def test_size_cap_without_content_length_abandons_mid_stream(tmp_path: Path) -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, stream=httpx.ByteStream(b"x" * 5000))

    reg = _registry(_spec("S96", "https://example.test/stream.bin", max_bytes=100))
    out = acquire(
        reg, None, AcquireOptions(root=tmp_path), client=_client(handler), sleep=lambda s: None
    )
    assert out[0].access_method == "human" and "exceeded cap" in out[0].notes
    assert out[0].raw_path is None


def test_http_error_is_recorded_not_raised(tmp_path: Path) -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(503, content=b"busy")

    reg = _registry(_spec("S94", "https://example.test/x"))
    out = acquire(
        reg, None, AcquireOptions(root=tmp_path), client=_client(handler), sleep=lambda s: None
    )
    assert out[0].http_status == 503 and out[0].access_method == "human"


def test_human_source_writes_task_only(tmp_path: Path) -> None:
    spec = SourceSpec(
        id="S95",
        name="ASHP",
        domain="t",
        tier=EvidenceTier.DIRECT_OPERATIONAL,
        landing_url="https://ashp.test/",
        access_method="human",
        license_note="copyrighted",
        human_task="browser capture",
    )

    def handler(req: httpx.Request) -> httpx.Response:  # pragma: no cover - must not be called
        raise AssertionError("human source must not be fetched")

    out = acquire(
        _registry(spec),
        None,
        AcquireOptions(root=tmp_path),
        client=_client(handler),
        sleep=lambda s: None,
    )
    assert (
        out[0].access_method == "human"
        and "browser capture" in out[0].notes
        and out[0].raw_path is None
    )
