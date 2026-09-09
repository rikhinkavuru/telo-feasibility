"""Phase G extensions of the release-assurance benchmark: transfer baselines, selective
prediction, held-out shift protocol, provenance-backed cost curve, gate options."""

from __future__ import annotations

import math

import numpy as np
import pytest

from telo_feasibility.configs import load_global
from telo_feasibility.release_benchmark import (
    HOLDOUT_FAMILIES,
    STRESS_FAMILIES,
    aurc,
    cost_curve_usd,
    cost_parameters,
    ds_transform,
    evaluate,
    fit_layer,
    holdout_shift_matrix,
    instrument_standardization,
    risk_coverage_points,
    snv,
    tune_threshold,
)


def _synthetic(seed: int = 0, n: int = 60, p: int = 40) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    basis = rng.normal(size=(3, p))
    scores = rng.normal(size=(n, 3))
    x = scores @ basis + 5.0 + 0.05 * rng.normal(size=(n, p))
    y = 200.0 + 10.0 * scores[:, 0] + 0.5 * rng.normal(size=n)
    return x, y


def test_ds_identity_when_instruments_agree() -> None:
    # more standards than channels: the ridge solution is the identity up to the penalty
    x, _y = _synthetic(n=60, p=20)
    std = x[:30]
    mapped = ds_transform(std, std, x[30:], ridge=1e-9)
    assert np.allclose(mapped, snv(x[30:]), atol=1e-3)


def test_ds_recovers_a_linear_channel_mixing() -> None:
    x, _y = _synthetic(n=80, p=12)
    rng = np.random.default_rng(1)
    mix = np.eye(12) + 0.05 * rng.normal(size=(12, 12))
    x_shift = x @ mix
    mapped = ds_transform(x[:50], x_shift[:50], x_shift[50:], ridge=1e-6)
    naive_err = float(np.abs(snv(x_shift[50:]) - snv(x[50:])).mean())
    ds_err = float(np.abs(mapped - snv(x[50:])).mean())
    assert ds_err < naive_err


def test_instrument_standardization_identity_and_affine_repair() -> None:
    x, _y = _synthetic(n=50, p=20)
    same = instrument_standardization(x[:30], x[:30], x[30:])
    assert np.allclose(same, snv(x[30:]))
    rng = np.random.default_rng(2)
    a = 1.0 + 0.5 * rng.random(20)
    b = 2.0 * rng.normal(size=20)
    shifted = x * a + b  # per-channel gain and offset on the second instrument
    mapped = instrument_standardization(x[:30], shifted[:30], shifted[30:])
    naive_err = float(np.abs(snv(shifted[30:]) - snv(x[30:])).mean())
    std_err = float(np.abs(mapped - snv(x[30:])).mean())
    assert mapped.shape == (20, 20) and std_err < naive_err


def test_risk_coverage_hand_case_with_tie_block() -> None:
    pvals = np.array([0.9, 0.5, 0.5, 0.1])
    covered = np.array([True, False, True, False])
    cov, risk = risk_coverage_points(pvals, covered)
    assert np.allclose(cov, [0.25, 0.5, 0.75, 1.0])
    assert np.allclose(risk, [0.0, 0.25, 1 / 3, 0.5])
    out = aurc(pvals, covered)
    assert math.isclose(out["aurc"], (0.0 + 0.25 + 1 / 3 + 0.5) / 4)
    assert math.isclose(out["aurc_oracle"], (0.0 + 0.0 + 1 / 3 + 0.5) / 4)
    assert math.isclose(out["e_aurc"], out["aurc"] - out["aurc_oracle"])


def test_aurc_perfect_ranking_has_zero_excess_and_empty_is_nan() -> None:
    pvals = np.array([0.9, 0.8, 0.7, 0.2, 0.1])
    covered = np.array([True, True, True, False, False])
    out = aurc(pvals, covered)
    assert math.isclose(out["e_aurc"], 0.0, abs_tol=1e-12)
    assert math.isnan(aurc(np.zeros(0), np.zeros(0, dtype=bool))["aurc"])


def test_tune_threshold_picks_smallest_reaching_target_or_falls_back() -> None:
    pv = np.array([0.02, 0.05, 0.05, 0.3, 0.9])
    grid = (0.0, 0.05, 0.1, 0.5)
    thr, ok = tune_threshold(pv, grid, detection_target=0.6)  # need >= 3 of 5 abstained
    assert thr == 0.1 and ok
    thr2, ok2 = tune_threshold(pv, grid, detection_target=0.95)
    assert thr2 == 0.5 and not ok2


def test_holdout_matrix_shape_and_bounds() -> None:
    x, y = _synthetic(n=70, p=40)
    rng = np.random.default_rng(3)
    layer = fit_layer(x[:40], y[:40], rng, n_train=28, n_components=2)
    x_home, x_shift, y_te = x[40:], x[40:] * 1.2 + 0.5, y[40:]
    hold = holdout_shift_matrix(
        layer,
        x_home,
        x_shift,
        y_te,
        np.random.default_rng(4),
        grid=(0.0, 0.1, 0.3, 0.5),
        detection_target=0.5,
    )
    assert list(hold["rows"]) == list(HOLDOUT_FAMILIES)
    assert len(STRESS_FAMILIES) + 1 == len(HOLDOUT_FAMILIES)
    for row in hold["rows"].values():
        assert row["tuned_threshold"] in (0.0, 0.1, 0.3, 0.5)
        assert 0.0 <= row["home_clean_abstention"] <= 1.0
        assert set(row["released_on"]) == set(HOLDOUT_FAMILIES)
        assert all(0.0 <= v <= 1.0 for v in row["released_on"].values())


def test_cost_parameters_trace_to_configs_and_curve_arithmetic() -> None:
    cp = cost_parameters("sodium_bicarbonate_8_4_50ml")
    g = load_global()
    prm = g.parameters["wrong_release_cost_usd"]
    assert int(prm.evidence_tier) == 5 and prm.is_illustrative
    assert cp["wrong_release_usd"] == g.base("wrong_release_cost_usd")
    assert math.isclose(cp["batch_value_usd"], 25000 * (0.6 + 0.6))
    expected_delay = 5.0 * cp["batch_value_usd"] * 0.2 / 365.25
    assert math.isclose(cp["false_hold_delay_carrying_usd"], expected_delay)
    assert math.isclose(cp["false_hold_usd"], 30000 + expected_delay)
    assert math.isclose(
        cp["false_hold_with_investigation_usd"],
        cp["false_hold_usd"] + g.base("investigation_cost_usd"),
    )
    assert all("tier" in v and "source" in v for v in cp["inputs"].values())
    curve = {"thr_0.1": {"released_fraction": 0.6, "unconditional_wrong_release": 0.1}}
    cc = cost_curve_usd(curve, cp)["thr_0.1"]
    assert math.isclose(cc["abstention_fraction"], 0.4)
    assert math.isclose(
        cc["cost_usd_per_batch"], 0.4 * cp["false_hold_usd"] + 0.1 * cp["wrong_release_usd"]
    )
    assert math.isclose(cc["break_even_wrong_release_usd"], cp["false_hold_usd"] * 0.6 / 0.1)
    zero = cost_curve_usd(
        {"thr_0.5": {"released_fraction": 0.0, "unconditional_wrong_release": 0.0}}, cp
    )["thr_0.5"]
    assert math.isinf(zero["break_even_wrong_release_usd"])
    assert math.isclose(zero["cost_usd_per_batch"], cp["false_hold_usd"])


def test_gate_and_selection_options_validate_and_q_gate_evaluates() -> None:
    x, y = _synthetic(n=60, p=30)
    with pytest.raises(ValueError, match="gate_score"):
        fit_layer(x[:40], y[:40], np.random.default_rng(0), n_train=28, gate_score="bogus")
    with pytest.raises(ValueError, match="component_selection"):
        fit_layer(x[:40], y[:40], np.random.default_rng(0), n_train=28, component_selection="bogus")
    layer = fit_layer(
        x[:40],
        y[:40],
        np.random.default_rng(0),
        n_train=28,
        n_components=2,
        gate_score="q_residual",
    )
    assert layer.gate_score == "q_residual" and layer.pca is not None
    ev = evaluate(layer, x[40:], y[40:])
    m = layer.novelty_cal.shape[0]
    assert ev["pval"].min() >= 1 / (m + 1) - 1e-12 and ev["pval"].max() <= 1.0
    leaky = fit_layer(
        x[:40],
        y[:40],
        np.random.default_rng(0),
        n_train=28,
        component_selection="train_and_calibration_cv",
    )
    assert 1 <= leaky.n_components <= 12
