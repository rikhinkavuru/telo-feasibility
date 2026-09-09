"""Optimization sanity: relaxing a constraint never worsens the optimum; refinement never beats the grid on infeasible points; infeasibility is detected."""

from __future__ import annotations

from telo_feasibility.optimization import Variable, optimize_strategy
from telo_feasibility.schemas import Eligibility, StrategyId
from telo_feasibility.simulation import SimSettings

SMALL = [
    Variable("safety_stock_days", 10.0, 60.0, "float", 2),
    Variable("site_fg_days", 10.0, 30.0, "float", 2),
]


def _settings() -> SimSettings:
    return SimSettings(
        horizon_days=300,
        warm_up_days=60,
        shortage_day_threshold=0.95,
        fill_rate_mean_min=0.99,
        recovery_window_days=14,
        record_events=False,
    )


def test_relaxing_the_service_constraint_cannot_worsen_the_optimum(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    from .conftest import quiet

    q = quiet(glob)
    d = designs.by_id(StrategyId.S4).model_copy(deep=True)
    d.design_variables["capacity_factor"] = 2.0
    strict = optimize_strategy(
        d,
        product,
        q,
        _settings(),
        master_seed=1,
        search_runs=[0, 1],
        final_runs=[0, 1, 2],
        tau=0.99,
        q=0.9,
        eligibility=Eligibility.NO_CONCLUSION,
        refinement_rounds=1,
        space=SMALL,
    )
    relaxed = optimize_strategy(
        d,
        product,
        q,
        _settings(),
        master_seed=1,
        search_runs=[0, 1],
        final_runs=[0, 1, 2],
        tau=0.80,
        q=0.5,
        eligibility=Eligibility.NO_CONCLUSION,
        refinement_rounds=1,
        space=SMALL,
    )
    assert relaxed.best is not None
    if strict.best is not None and strict.status == "optimal":
        assert relaxed.best.mean_cost <= strict.best.mean_cost + 1e-6
    assert any(e.stage == "grid" for e in relaxed.evaluations)
    assert relaxed.best_grid is not None and relaxed.best is not None
    assert (
        relaxed.best.mean_cost <= relaxed.best_grid.mean_cost + 1e-6
        or relaxed.best.n_runs != relaxed.best_grid.n_runs
    )


def test_status_quo_is_infeasible_for_a_capacity_short_product(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rec = optimize_strategy(
        designs.by_id(StrategyId.S0),
        product,
        glob,
        _settings(),
        master_seed=2,
        search_runs=[0],
        final_runs=[0],
        tau=0.99,
        q=0.9,
        eligibility=Eligibility.NO_CONCLUSION,
        refinement_rounds=0,
        space=SMALL,
    )
    assert rec.status == "infeasible"
    assert rec.best is None and rec.best_grid is not None
    assert "no grid design met" in rec.notes[-1]


def test_excluded_strategy_is_not_optimized(product, glob, designs) -> None:  # type: ignore[no-untyped-def]
    rec = optimize_strategy(
        designs.by_id(StrategyId.S5),
        product,
        glob,
        _settings(),
        master_seed=2,
        search_runs=[0],
        final_runs=[0],
        tau=0.99,
        q=0.9,
        eligibility=Eligibility.EXCLUDED,
        space=SMALL,
    )
    assert rec.status == "excluded" and not rec.evaluations
