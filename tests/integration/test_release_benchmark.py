from __future__ import annotations

import numpy as np
import pytest

from telo_feasibility.release_benchmark import (
    BenchmarkConfig,
    apply_shift,
    joint_metrics,
    load_tablets,
    run_benchmark,
)

try:
    DATA = load_tablets()
except FileNotFoundError:  # pragma: no cover
    DATA = None

pytestmark = pytest.mark.skipif(DATA is None, reason="tablet snapshot not frozen")


def test_joint_metrics_denominators() -> None:
    cov = np.array([True, True, False, False])
    rel = np.array([True, False, True, False])
    jm = joint_metrics({"covered": cov, "released": rel})
    assert jm.released_fraction == 0.5 and jm.unconditional_wrong_release == 0.25
    assert jm.conditional_error_among_released == 0.5 and jm.false_hold_rate == 0.5


def test_tablet_data_shapes() -> None:
    assert DATA is not None
    assert DATA.cal1.shape == (155, 650) and DATA.test2.shape == (460, 650)
    assert DATA.test_y.shape == (460,) and 150 < DATA.test_y.mean() < 240


def test_benchmark_reproduces_shift_collapse_and_gate_abstention() -> None:
    assert DATA is not None
    res = run_benchmark(BenchmarkConfig(seeds=3, repair_sizes=(9,)), DATA)
    home, shift = res.metrics["home"], res.metrics["shift"]
    assert home["empirical_coverage"]["mean"] > 0.85
    assert shift["empirical_coverage"]["mean"] < home["empirical_coverage"]["mean"] - 0.2
    assert shift["abstention_fraction"]["mean"] > home["abstention_fraction"]["mean"] + 0.2
    assert res.metrics["shift_mandatory_hold"]["unconditional_wrong_release"]["mean"] == 0.0
    assert (
        res.metrics["shift_no_gate"]["unconditional_wrong_release"]["mean"]
        > shift["unconditional_wrong_release"]["mean"]
    )
    assert "risk_coverage_shift" in res.curves and len(res.curves["risk_coverage_shift"]) == len(
        res.config.ood_grid
    )


def test_synthetic_faults_change_spectra() -> None:
    assert DATA is not None
    rng = np.random.default_rng(0)
    for kind in (
        "wavelength_shift",
        "baseline_offset",
        "gain",
        "noise",
        "spikes",
        "dead_channels",
        "gradual_drift",
        "baseline_slope",
    ):
        out = apply_shift(
            DATA.test1[:5], kind, rng, 2 if kind in ("wavelength_shift", "spikes") else 0.5
        )
        assert out.shape == (5, 650) and not np.allclose(out, DATA.test1[:5])


def test_fixed_eight_components_mode_runs_and_is_reported_separately() -> None:
    assert DATA is not None
    res = run_benchmark(BenchmarkConfig(seeds=2, repair_sizes=(9,), n_components=8), DATA)
    assert res.metrics["model"]["n_components"]["mean"] == 8.0
    assert "repository reproduction mode" in __import__(
        "telo_feasibility.release_benchmark", fromlist=["model_card"]
    ).model_card(res)
