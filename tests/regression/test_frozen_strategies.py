"""Regression: the frozen comparators S0-S7 reproduce their pre-extension event digests.

``frozen_digests_s0_s7.json`` was captured on 2026-09-02 before the design-space engine
extensions (opt-in design variables ``region_base_stock``, ``region_reorder_point_days``,
``component_lead_fraction``) were added to ``strategies.build_strategy``. Capture settings:
horizon 600 days, warm-up 200 days, shortage-day threshold 0.95, mean fill target 0.99,
recovery window 30 days, events recorded, ``shortage_listed_at_t0`` true only for the
sodium bicarbonate product, master seed 20260901, run indices 0 and 1, both products,
all eight designs from ``config/strategies/illustrative_baseline.yaml``, global parameters
from ``config/global.yaml``. Any change to the engine or the strategy builders that alters
an S0-S7 event digest or annual cost fails here; the frozen designs may only change through
``protocol/revisions.csv``.

Cost column re-captured 2026-09-02 after revision R003 (raw-material inventory carrying
cost, model defect MD-1); event digests were asserted identical before and after, and the
pre-R003 cost is kept in each entry as ``cost_before_R003`` (change +0.10% to +0.36%).

Re-captured again after revisions R004, R005 and R008; each entry keeps the previous
values as ``digest_before_R004``, ``cost_before_R004``, ``fill_before_R004`` and the same
triple for R008 and again for R009, so what each revision moved stays visible.

Re-captured again 2026-09-03 after revision R004, which fixed the model defects the Phase A
decomposition found: the capacity ramp for expansions at an existing site (MD-7), fixed
operations charged only while a site exists and end-of-horizon backlog no longer censored
as lost at any age (MD-6), opening stock spread across shelf-life cohorts (MD-4), a reserved
line Telo does not own carrying no capital, fixed operations, or validation (MD-14), and a
lot-sized material reorder point (MD-2). Twelve of the thirty-two event digests and twenty
of the costs changed. The pre-R004 values are kept in each entry as ``digest_before_R004``,
``cost_before_R004`` and ``fill_before_R004``: the largest service change is sodium
bicarbonate S4 at -0.171 fill (its expansion no longer arrives free on day zero) and the
largest cost change is S3 at about -40% (its reserved line is no longer charged as if owned).
Re-captured again 2026-09-03 after revision R007 (a supplier at capacity fraction f ships at most f
of one full order per day instead of the whole order, model defect MD-19). No event digest and no
fill rate changed; twelve of the thirty-two costs moved, the largest by 8.6e-7 relative (S0
norepinephrine run 1, 12,469,383.06 -> 12,469,376.48 USD/yr), because a partly shipped order spends a
day in transit rather than in stock and the material carrying-cost integral moves with it. The
pre-R007 values are kept in each entry as ``digest_before_R007``, ``cost_before_R007`` and
``fill_before_R007``.

This file pins current behaviour; it is not a claim that current behaviour is correct.
"""

from __future__ import annotations

import json
from pathlib import Path

from telo_feasibility.configs import load_global, load_products, load_strategies
from telo_feasibility.simulation import SimSettings, run_paired

FROZEN = Path(__file__).with_name("frozen_digests_s0_s7.json")
MASTER_SEED = 20260901
RUN_INDICES = [0, 1]


def _settings(listed: bool) -> SimSettings:
    return SimSettings(
        horizon_days=600,
        warm_up_days=200,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=30,
        record_events=True,
        shortage_listed_at_t0=listed,
    )


def test_frozen_strategies_reproduce_pre_extension_digests() -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    glob = load_global()
    designs = load_strategies().designs
    seen: set[str] = set()
    for pid, product in load_products().items():
        settings = _settings(pid.startswith("sodium"))
        for r in run_paired(designs, product, glob, settings, MASTER_SEED, RUN_INDICES):
            key = f"{pid}|{r.strategy_id}|{r.run_index}"
            assert key in frozen, f"{key} missing from the frozen snapshot"
            ref = frozen[key]
            assert r.event_digest == ref["digest"], f"{key}: event digest changed"
            assert abs(r.metrics["annual_total_cost"] - ref["cost"]) <= 1e-6, f"{key}: cost"
            assert abs(r.metrics["fill_rate"] - ref["fill"]) <= 1e-12, f"{key}: fill"
            seen.add(key)
    assert seen == set(frozen), "snapshot and regenerated run sets differ"
    assert len(seen) == 32
