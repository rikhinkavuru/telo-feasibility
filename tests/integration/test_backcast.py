from __future__ import annotations

from telo_feasibility.backcast import backcast_episode, inject, load_episodes
from telo_feasibility.simulation import SimSettings, world_for_run


def test_episodes_load_and_cover_required_classes() -> None:
    eps = load_episodes()
    classes = {e["episode_class"] for e in eps}
    assert {"site_failure", "upstream_or_common_cause", "demand_shock_or_substitution"} <= classes
    assert any(
        e.get("information_frozen_at") is None for e in eps
    )  # undocumented template stays not-run


def test_injected_site_failure_zeroes_capacity(glob) -> None:  # type: ignore[no-untyped-def]
    s = SimSettings(
        horizon_days=200,
        warm_up_days=10,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
    )
    world, _ = world_for_run(glob, s, 1, 0)
    notes = inject(
        world, {"kind": "site_failure", "target": "central", "start_day": 50, "duration_days": 30}
    )
    assert (world.site_capacity["central"][50:80] == 0).all() and world.site_capacity["central"][
        80
    ] == 1.0
    assert notes


def test_chronic_shortage_backcast_is_consistent_with_ongoing_status() -> None:
    ep = next(e for e in load_episodes() if e["id"] == "sodium_bicarbonate_2017_ongoing")
    c = backcast_episode(ep, horizon_days=365 + 400)
    assert c.observed_ongoing
    assert c.binding_bottleneck_simulated.startswith("capacity below demand")
    assert c.consistent_duration is True
