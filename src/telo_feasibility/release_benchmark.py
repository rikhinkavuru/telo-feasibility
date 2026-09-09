"""Release-assurance benchmark package (protocol 9.3; task section 15).

Public IDRC 2002 NIR tablet data (frozen as source S28) are used to measure, for a
conventional calibration plus a conservative abstention gate:

* the twelve metrics that must travel together (released fraction, abstention fraction,
  unconditional wrong-release exposure, conditional error among released, empirical
  coverage, false-hold rate, risk-coverage curve, operational cost-coverage curve,
  performance by instrument / lot / time / concentration / shift, repair sample count,
  performance after repair, bootstrap intervals);
* baselines: no gate, mandatory hold, calibration transfer (slope/bias and PDS with n
  transfer standards), instrument standardization, recalibrated conformal quantile;
* stress tests with synthetic shifts (wavelength shift, baseline, gain, noise, spikes,
  dead channels, gradual drift) and label noise.

Grouped validation: the only real group is the instrument. Lot and time groups do not
exist in the public data; the package assigns SYNTHETIC lot and time blocks by tablet
index and labels every such result as synthetic. Nothing here is evidence on the target
drug chemistry or on any Telo process.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy.io import loadmat
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold
from sklearn.neighbors import NearestNeighbors

from .configs import load_global, load_products
from .provenance import PACKAGE_ROOT, RAW_SNAPSHOTS

RESULTS_RA = PACKAGE_ROOT / "results" / "release_assurance"
ASSAY_COL = 2  # 0 weight, 1 hardness, 2 assay (mg)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------


@dataclass
class TabletData:
    cal1: np.ndarray
    cal2: np.ndarray
    test1: np.ndarray
    test2: np.ndarray
    cal_y: np.ndarray
    test_y: np.ndarray
    source_sha256: str
    path: Path


def load_tablets(root: Path = RAW_SNAPSHOTS) -> TabletData:
    hits = sorted(root.glob("S28/*/nir_shootout_2002.mat"))
    if not hits:
        raise FileNotFoundError(
            "IDRC tablet snapshot missing; run scripts/acquire_sources.py --source S28"
        )
    path = hits[-1]
    manifest = json.loads(path.with_name(path.name + ".manifest.json").read_text(encoding="utf-8"))
    m = loadmat(path)

    def arr(key: str) -> np.ndarray:
        v = m[key]
        while isinstance(v, np.ndarray) and v.dtype == object:
            v = v[0, 0]
        if hasattr(v, "dtype") and v.dtype.names and "data" in v.dtype.names:
            v = v["data"]
            while isinstance(v, np.ndarray) and v.dtype == object:
                v = v[0, 0]
        return np.asarray(v, dtype=float)

    return TabletData(
        arr("calibrate_1"),
        arr("calibrate_2"),
        arr("test_1"),
        arr("test_2"),
        arr("calibrate_Y")[:, ASSAY_COL],
        arr("test_Y")[:, ASSAY_COL],
        str(manifest.get("sha256")),
        path,
    )


def snv(x: np.ndarray) -> np.ndarray:
    mu = x.mean(axis=1, keepdims=True)
    sd = x.std(axis=1, keepdims=True)
    return (x - mu) / np.where(sd > 0, sd, 1.0)


# ---------------------------------------------------------------------------
# Model: PLS with CV-selected components, split conformal, 1-NN novelty gate
# ---------------------------------------------------------------------------


@dataclass
class FittedLayer:
    pls: PLSRegression
    n_components: int
    q: float  # conformal half-width (alpha)
    nn: NearestNeighbors
    novelty_cal: np.ndarray  # calibration novelty scores (for conformal p-values)
    alpha: float
    ood_alpha: float
    train_idx: np.ndarray
    cal_idx: np.ndarray
    gate_score: str = "nn"  # "nn" (1-NN distance in PLS space) or "q_residual" (PCA SPE)
    pca: PCA | None = None
    pca_mean: np.ndarray | None = None


GATE_SCORES: tuple[str, ...] = ("nn", "q_residual")
COMPONENT_SELECTIONS: tuple[str, ...] = ("train_cv", "train_and_calibration_cv")


def q_residual(pca: PCA, mean: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """PCA squared prediction error (Q residual) of SNV spectra ``xs`` about ``mean``."""
    z = xs - mean
    return np.asarray(np.sum((z - pca.inverse_transform(pca.transform(z))) ** 2, axis=1))


def select_components(
    x: np.ndarray, y: np.ndarray, rng: np.random.Generator, max_k: int = 12
) -> int:
    """Choose PLS components by 5-fold CV RMSE on the training partition only."""
    kf = KFold(n_splits=5, shuffle=True, random_state=int(rng.integers(0, 2**31 - 1)))
    best_k, best = 1, float("inf")
    for k in range(1, max_k + 1):
        errs = []
        for tr, va in kf.split(x):
            m = PLSRegression(n_components=k, scale=False).fit(x[tr], y[tr])
            errs.append(float(np.mean((m.predict(x[va]).ravel() - y[va]) ** 2)))
        rmse = float(np.sqrt(np.mean(errs)))
        if rmse < best - 1e-9:
            best, best_k = rmse, k
    return best_k


def fit_layer(
    x_cal: np.ndarray,
    y_cal: np.ndarray,
    rng: np.random.Generator,
    *,
    alpha: float = 0.10,
    ood_alpha: float = 0.10,
    n_train: int = 105,
    label_noise_sd: float = 0.0,
    n_components: int | None = None,
    pls_scale: bool = False,
    gate_score: str = "nn",
    component_selection: str = "train_cv",
) -> FittedLayer:
    """Fit PLS + split-conformal interval + novelty gate on the calibration tablets.

    ``component_selection`` = "train_cv" (default) selects PLS components by 5-fold CV on
    the training partition only. "train_and_calibration_cv" deliberately reproduces a
    leak: the selection touches the conformal-calibration tablets whose residuals set the
    interval, so the exchangeability the guarantee rests on is broken. It exists to
    measure the size of that leak, never for reporting a guarantee.
    """
    if gate_score not in GATE_SCORES:
        raise ValueError(f"gate_score must be one of {GATE_SCORES}")
    if component_selection not in COMPONENT_SELECTIONS:
        raise ValueError(f"component_selection must be one of {COMPONENT_SELECTIONS}")
    n = x_cal.shape[0]
    idx = rng.permutation(n)
    tr, ca = idx[:n_train], idx[n_train:]
    y_used = y_cal + (rng.normal(0.0, label_noise_sd, size=n) if label_noise_sd > 0 else 0.0)
    xs = snv(x_cal)
    if n_components is not None:
        k = n_components
    elif component_selection == "train_and_calibration_cv":
        k = select_components(xs[idx], y_used[idx], rng)
    else:
        k = select_components(xs[tr], y_used[tr], rng)
    pls = PLSRegression(n_components=k, scale=pls_scale).fit(xs[tr], y_used[tr])
    resid = np.abs(pls.predict(xs[ca]).ravel() - y_used[ca])
    m = len(ca)
    rank = math.ceil((m + 1) * (1 - alpha))
    q = float(np.sort(resid)[min(rank, m) - 1]) if rank <= m else float("inf")
    scores_tr = pls.transform(xs[tr])
    nn = NearestNeighbors(n_neighbors=1).fit(scores_tr)
    if gate_score == "q_residual":
        mean = xs[tr].mean(axis=0, keepdims=True)
        pca = PCA(n_components=k).fit(xs[tr] - mean)
        nov_cal = q_residual(pca, mean, xs[ca])
        return FittedLayer(
            pls, k, q, nn, np.sort(nov_cal), alpha, ood_alpha, tr, ca, gate_score, pca, mean
        )
    nov_cal = nn.kneighbors(pls.transform(xs[ca]))[0].ravel()
    return FittedLayer(pls, k, q, nn, np.sort(nov_cal), alpha, ood_alpha, tr, ca)


def evaluate(
    layer: FittedLayer, x: np.ndarray, y: np.ndarray, *, ood_alpha: float | None = None
) -> dict[str, np.ndarray]:
    xs = snv(x)
    pred = layer.pls.predict(xs).ravel()
    covered = np.abs(pred - y) <= layer.q
    if layer.gate_score == "q_residual" and layer.pca is not None and layer.pca_mean is not None:
        nov = q_residual(layer.pca, layer.pca_mean, xs)
    else:
        nov = layer.nn.kneighbors(layer.pls.transform(xs))[0].ravel()
    m = layer.novelty_cal.shape[0]
    # conformal p-value: fraction of calibration novelty scores >= this score (plus one)
    pvals = (np.searchsorted(layer.novelty_cal, nov, side="left").astype(float) * -1 + m + 1) / (
        m + 1
    )
    thr = layer.ood_alpha if ood_alpha is None else ood_alpha
    released = pvals >= thr
    return {
        "pred": np.asarray(pred),
        "covered": np.asarray(covered),
        "released": np.asarray(released),
        "pval": np.asarray(pvals),
    }


# ---------------------------------------------------------------------------
# Metrics that travel together
# ---------------------------------------------------------------------------


@dataclass
class JointMetrics:
    n: int
    released_fraction: float
    abstention_fraction: float
    unconditional_wrong_release: float  # released and not covered / all
    conditional_error_among_released: float  # not covered / released (nan if none released)
    empirical_coverage: float  # covered / all (no gate)
    false_hold_rate: float  # abstained and covered / covered (unnecessary abstentions)
    n_released: int


def joint_metrics(ev: dict[str, np.ndarray]) -> JointMetrics:
    cov, rel = ev["covered"], ev["released"]
    n = int(cov.shape[0])
    n_rel = int(rel.sum())
    return JointMetrics(
        n=n,
        released_fraction=float(rel.mean()),
        abstention_fraction=float(1.0 - rel.mean()),
        unconditional_wrong_release=float((rel & ~cov).sum() / n),
        conditional_error_among_released=float((rel & ~cov).sum() / n_rel)
        if n_rel
        else float("nan"),
        empirical_coverage=float(cov.mean()),
        false_hold_rate=float((~rel & cov).sum() / cov.sum()) if cov.sum() else float("nan"),
        n_released=n_rel,
    )


def pooled(evs: list[dict[str, np.ndarray]]) -> JointMetrics:
    cat = {k: np.concatenate([e[k] for e in evs]) for k in ("covered", "released")}
    return joint_metrics(cat)


def bootstrap_ci(
    values: list[float], rng: np.random.Generator, n_boot: int = 1000
) -> tuple[float, float, float]:
    v = np.array([x for x in values if not math.isnan(x)])
    if v.size == 0:
        return float("nan"), float("nan"), float("nan")
    boots = np.array([rng.choice(v, size=v.size, replace=True).mean() for _ in range(n_boot)])
    return float(v.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


# ---------------------------------------------------------------------------
# Baselines: transfer and repair
# ---------------------------------------------------------------------------


def slope_bias_correct(
    layer: FittedLayer, x_std_home: np.ndarray, x_std_shift: np.ndarray, x: np.ndarray
) -> np.ndarray:
    """Slope/bias correction of predictions using paired transfer standards measured on both instruments."""
    p_home = layer.pls.predict(snv(x_std_home)).ravel()
    p_shift = layer.pls.predict(snv(x_std_shift)).ravel()
    a, b = np.polyfit(p_shift, p_home, 1) if p_shift.size >= 2 else (1.0, 0.0)
    return np.asarray(a * layer.pls.predict(snv(x)).ravel() + b)


def pds_transform(
    x_std_home: np.ndarray,
    x_std_shift: np.ndarray,
    x: np.ndarray,
    window: int = 5,
    ridge: float = 1e-3,
) -> np.ndarray:
    """Piecewise direct standardization: map shifted spectra into the home instrument's space."""
    hs, ss = snv(x_std_home), snv(x_std_shift)
    xs = snv(x)
    n_ch = hs.shape[1]
    out = np.zeros_like(xs)
    for j in range(n_ch):
        lo, hi = max(0, j - window), min(n_ch, j + window + 1)
        a = ss[:, lo:hi]
        beta = np.linalg.solve(a.T @ a + ridge * np.eye(hi - lo), a.T @ hs[:, j])
        out[:, j] = xs[:, lo:hi] @ beta
    return out


def recalibrated_quantile(layer: FittedLayer, x_new: np.ndarray, y_new: np.ndarray) -> float:
    resid = np.abs(layer.pls.predict(snv(x_new)).ravel() - y_new)
    m = resid.shape[0]
    rank = math.ceil((m + 1) * (1 - layer.alpha))
    return float(np.sort(resid)[min(rank, m) - 1]) if rank <= m else float("inf")


def ds_transform(
    x_std_home: np.ndarray, x_std_shift: np.ndarray, x: np.ndarray, ridge: float = 1e-3
) -> np.ndarray:
    """Direct standardization (Wang, Veltkamp and Kowalski 1991): a full transfer matrix
    F mapping shifted spectra into the home instrument's space, fitted on paired transfer
    standards. With fewer standards than channels the normal equations are singular, so
    F is the ridge solution with the penalty scaled to the mean diagonal of S'S (scale
    free). Returns mapped SNV spectra, like ``pds_transform``.
    """
    hs, ss = snv(x_std_home), snv(x_std_shift)
    mu_h, mu_s = hs.mean(axis=0, keepdims=True), ss.mean(axis=0, keepdims=True)
    a = ss - mu_s
    gram = a.T @ a
    lam = ridge * float(np.trace(gram)) / max(gram.shape[0], 1)
    f = np.linalg.solve(gram + lam * np.eye(gram.shape[0]), a.T @ (hs - mu_h))
    return np.asarray((snv(x) - mu_s) @ f + mu_h)


def instrument_standardization(
    x_std_home: np.ndarray, x_std_shift: np.ndarray, x: np.ndarray, floor: float = 1e-9
) -> np.ndarray:
    """Per-wavelength mean and standard-deviation matching fitted on transfer standards
    measured on both instruments (a domain-standardization baseline with no model, no
    labels, and no target-instrument assays). Returns mapped SNV spectra.
    """
    hs, ss = snv(x_std_home), snv(x_std_shift)
    mu_h, mu_s = hs.mean(axis=0), ss.mean(axis=0)
    sd_h, sd_s = hs.std(axis=0), ss.std(axis=0)
    return np.asarray((snv(x) - mu_s) / np.maximum(sd_s, floor) * sd_h + mu_h)


# ---------------------------------------------------------------------------
# Selective prediction: risk-coverage curve and AURC
# ---------------------------------------------------------------------------


def risk_coverage_points(pvals: np.ndarray, covered: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Selective risk at every coverage level k/n when units are released in order of
    decreasing gate confidence (conformal p-value).

    Selective risk and coverage follow Geifman and El-Yaniv (NeurIPS 2017): coverage is
    the fraction of units released, selective risk is the error rate among them; the
    error here is an interval miss. Ties in the p-value (which is discrete, with at most
    m + 1 distinct values from m calibration scores) are broken in expectation: inside a
    tie block of b units with e misses, the first j released units carry j * e / b
    expected misses, which is the mean over random orderings of the block.
    """
    p = np.asarray(pvals, dtype=float)
    miss = (~np.asarray(covered, dtype=bool)).astype(float)
    n = p.shape[0]
    if n == 0:
        return np.zeros(0), np.zeros(0)
    order = np.argsort(-p, kind="stable")
    ps, ms = p[order], miss[order]
    cum = np.zeros(n)
    start = 0
    while start < n:
        end = start
        while end + 1 < n and ps[end + 1] == ps[start]:
            end += 1
        b = end - start + 1
        e = float(ms[start : end + 1].sum())
        before = cum[start - 1] if start > 0 else 0.0
        for j in range(1, b + 1):
            cum[start + j - 1] = before + j * e / b
        start = end + 1
    k = np.arange(1, n + 1, dtype=float)
    return k / n, cum / k


def aurc(pvals: np.ndarray, covered: np.ndarray) -> dict[str, float]:
    """Area under the risk-coverage curve and its excess over the oracle ranking.

    AURC (Geifman, Uziel and El-Yaniv, ICLR 2019) is the mean selective risk over the n
    coverage levels 1/n .. 1 of ``risk_coverage_points``; the oracle ranks every covered
    unit ahead of every missed one, giving risk max(0, k - n_covered) / k at level k, and
    E-AURC = AURC - AURC_oracle. Both are zero for a perfect gate and equal for a gate
    whose confidence carries no information beyond the base miss rate.
    """
    cov = np.asarray(covered, dtype=bool)
    n = cov.shape[0]
    if n == 0:
        return {"aurc": float("nan"), "e_aurc": float("nan"), "aurc_oracle": float("nan")}
    _c, r = risk_coverage_points(np.asarray(pvals, dtype=float), cov)
    k = np.arange(1, n + 1, dtype=float)
    oracle = np.maximum(0.0, k - float(cov.sum())) / k
    a, o = float(r.mean()), float(oracle.mean())
    return {"aurc": a, "e_aurc": a - o, "aurc_oracle": o}


# ---------------------------------------------------------------------------
# Held-out shift-type protocol
# ---------------------------------------------------------------------------

STRESS_FAMILIES: tuple[tuple[str, float], ...] = (
    ("wavelength_shift", 2),
    ("baseline_offset", 0.5),
    ("baseline_slope", 0.5),
    ("gain", 0.1),
    ("noise", 0.5),
    ("spikes", 3),
    ("dead_channels", 20),
    ("gradual_drift", 1.0),
)
HOLDOUT_FAMILIES: tuple[str, ...] = (*(k for k, _m in STRESS_FAMILIES), "instrument")


def tune_threshold(
    pvals_family: np.ndarray, grid: tuple[float, ...], detection_target: float
) -> tuple[float, bool]:
    """Smallest gate threshold in ``grid`` whose abstention on the family reaches
    ``detection_target``; returns (threshold, reachable). Falls back to max(grid)."""
    for thr in sorted(grid):
        released = float((pvals_family >= thr).mean())
        if 1.0 - released >= detection_target:
            return float(thr), True
    return float(max(grid)), False


def holdout_shift_matrix(
    layer: FittedLayer,
    x_home: np.ndarray,
    x_shift: np.ndarray,
    y: np.ndarray,
    rng: np.random.Generator,
    *,
    families: tuple[str, ...] = HOLDOUT_FAMILIES,
    grid: tuple[float, ...],
    detection_target: float,
) -> dict[str, Any]:
    """Tune the gate threshold on one shift family, evaluate on every other family.

    Rows are the family the threshold was tuned on; columns the family it is evaluated
    on. Each cell is the released fraction on the evaluation family (1 - detection). The
    ``home_clean`` column is the abstention on unshifted home spectra (false-hold proxy)
    and ``tuned_threshold`` / ``target_reachable`` record the tuning outcome. An
    off-diagonal cell far above its diagonal is a shift type the gate would miss when
    its threshold was set on a different kind of shift.
    """
    mags = dict(STRESS_FAMILIES)
    pv: dict[str, np.ndarray] = {}
    for fam in families:
        xf = x_shift if fam == "instrument" else apply_shift(x_home, fam, rng, mags[fam])
        pv[fam] = evaluate(layer, xf, y)["pval"]
    pv_home = evaluate(layer, x_home, y)["pval"]
    out: dict[str, Any] = {"rows": {}}
    for tune_on in families:
        thr, ok = tune_threshold(pv[tune_on], grid, detection_target)
        row: dict[str, Any] = {
            "tuned_threshold": thr,
            "target_reachable": ok,
            "home_clean_abstention": float((pv_home < thr).mean()),
            "released_on": {fam: float((pv[fam] >= thr).mean()) for fam in families},
        }
        out["rows"][tune_on] = row
    return out


# ---------------------------------------------------------------------------
# Operational cost parameters with provenance
# ---------------------------------------------------------------------------


def cost_parameters(product_id: str) -> dict[str, Any]:
    """Cost of a false hold and of a wrong release, from the study's parameter sets.

    false hold (an abstained batch goes to the conventional laboratory path) =
    testing_usd_per_batch + assay_days x batch value x inventory_carrying_rate / 365.25;
    with_investigation adds investigation_cost_usd. Wrong release = wrong_release_cost_usd
    (tier 5 illustrative global parameter). Every input carries its provenance tier.
    """
    g = load_global()
    p = load_products()[product_id].parameters

    def rec(ps: Any, key: str) -> dict[str, Any]:
        prm = ps.parameters[key]
        return {
            "value": ps.base(key),
            "tier": int(prm.evidence_tier),
            "status": str(prm.validation_status),
            "source": prm.source_locator,
        }

    inputs = {
        "testing_usd_per_batch": rec(p, "testing_usd_per_batch"),
        "units_per_batch": rec(p, "units_per_batch"),
        "variable_materials_usd_per_unit": rec(p, "variable_materials_usd_per_unit"),
        "variable_conversion_usd_per_unit": rec(p, "variable_conversion_usd_per_unit"),
        "assay_days": rec(g, "assay_days"),
        "inventory_carrying_rate": rec(g, "inventory_carrying_rate"),
        "investigation_cost_usd": rec(g, "investigation_cost_usd"),
        "wrong_release_cost_usd": rec(g, "wrong_release_cost_usd"),
    }
    batch_value = p.base("units_per_batch") * (
        p.base("variable_materials_usd_per_unit") + p.base("variable_conversion_usd_per_unit")
    )
    delay = g.base("assay_days") * batch_value * g.base("inventory_carrying_rate") / 365.25
    fallback = p.base("testing_usd_per_batch") + delay
    return {
        "product_id": product_id,
        "inputs": inputs,
        "batch_value_usd": batch_value,
        "false_hold_delay_carrying_usd": delay,
        "false_hold_usd": fallback,
        "false_hold_with_investigation_usd": fallback + g.base("investigation_cost_usd"),
        "wrong_release_usd": g.base("wrong_release_cost_usd"),
        "implied_cost_ratio_wrong_to_false_hold": g.base("wrong_release_cost_usd") / fallback,
        "legacy_relative_ratio": 50.0,
        "note": "wrong release = interval miss on a released batch (a wrong certificate), "
        "not a shipped out-of-specification unit; illustrative inputs",
    }


def cost_curve_usd(
    curve: dict[str, dict[str, float]], params: dict[str, Any]
) -> dict[str, dict[str, float]]:
    """Expected cost per batch decision at each gate threshold, in USD from ``cost_parameters``."""
    out: dict[str, dict[str, float]] = {}
    for key, v in curve.items():
        abstain = 1.0 - float(v["released_fraction"])
        expo = float(v["unconditional_wrong_release"])
        fh = float(params["false_hold_usd"])
        out[key] = {
            "abstention_fraction": abstain,
            "unconditional_wrong_release": expo,
            "cost_usd_per_batch": abstain * fh + expo * params["wrong_release_usd"],
            "cost_usd_per_batch_with_investigation": abstain
            * params["false_hold_with_investigation_usd"]
            + expo * params["wrong_release_usd"],
            # the wrong-release cost below which the gate beats holding every batch
            # (cost of holding everything = one false hold per batch)
            "break_even_wrong_release_usd": fh * (1.0 - abstain) / expo
            if expo > 0
            else float("inf"),
        }
    return out


# ---------------------------------------------------------------------------
# Synthetic shifts and faults
# ---------------------------------------------------------------------------


def apply_shift(
    x: np.ndarray, kind: str, rng: np.random.Generator, magnitude: float = 1.0
) -> np.ndarray:
    out = x.copy()
    n, p = out.shape
    if kind == "wavelength_shift":
        s = round(magnitude)
        return np.asarray(np.roll(out, s, axis=1))
    if kind == "baseline_offset":
        return out + magnitude * out.std()
    if kind == "baseline_slope":
        return out + magnitude * out.std() * np.linspace(-1, 1, p)[None, :]
    if kind == "gain":
        return out * (1.0 + magnitude)
    if kind == "noise":
        return out + rng.normal(0.0, magnitude * out.std(), size=out.shape)
    if kind == "spikes":
        for i in range(n):
            j = rng.integers(0, p, size=max(1, int(magnitude)))
            out[i, j] += 5.0 * out.std()
        return out
    if kind == "dead_channels":
        j = rng.choice(p, size=max(1, int(magnitude)), replace=False)
        out[:, j] = 0.0
        return out
    if kind == "gradual_drift":
        ramp = np.linspace(0.0, magnitude, n)[:, None] * out.std()
        return out + ramp
    raise ValueError(kind)


# ---------------------------------------------------------------------------
# Benchmark driver
# ---------------------------------------------------------------------------


@dataclass
class BenchmarkConfig:
    seeds: int = 50
    alpha: float = 0.10
    ood_alpha: float = 0.10
    n_train: int = 105
    repair_sizes: tuple[int, ...] = (5, 9, 15, 30, 50)
    ood_grid: tuple[float, ...] = (0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50)
    fallback_cost: float = 1.0  # relative cost of an unnecessary hold
    wrong_release_cost: float = 50.0  # relative cost of a wrong release
    synthetic_lots: int = 5
    synthetic_time_blocks: int = 4
    n_components: int | None = None  # None = 5-fold CV selection; 8 = the repository's fixed choice
    pls_scale: bool = (
        False  # True = sklearn default per-wavelength standardization, as in the repository script
    )
    gate_score: str = "nn"  # "nn" (repository gate) or "q_residual" (PCA SPE, the industry score)
    component_selection: str = "train_cv"  # "train_and_calibration_cv" reproduces a selection leak
    extra_repair_sizes: tuple[int, ...] = (
        3,
    )  # drawn from a separate stream; existing keys unchanged
    transfer_sizes: tuple[int, ...] = (
        15,
        30,
        50,
    )  # standards for DS and instrument standardization
    holdout_grid: tuple[float, ...] = (
        0.0,
        0.02,
        0.04,
        0.06,
        0.08,
        0.10,
        0.12,
        0.14,
        0.16,
        0.18,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
    )
    holdout_detection_target: float = 0.90
    cost_product_id: str = "sodium_bicarbonate_8_4_50ml"


@dataclass
class BenchmarkResult:
    config: BenchmarkConfig
    data_sha256: str
    metrics: dict[str, Any] = field(default_factory=dict)
    curves: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    banner: str = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"


def _ci_block(
    per_seed: dict[str, list[float]], rng: np.random.Generator
) -> dict[str, dict[str, float]]:
    out = {}
    for k, vals in per_seed.items():
        mean, lo, hi = bootstrap_ci(vals, rng)
        n_ok = sum(1 for v in vals if not math.isnan(v))
        out[k] = {"mean": mean, "ci95_low": lo, "ci95_high": hi, "seeds_with_value": n_ok}
    return out


def run_benchmark(
    cfg: BenchmarkConfig | None = None, data: TabletData | None = None
) -> BenchmarkResult:
    cfg = cfg or BenchmarkConfig()
    data = data or load_tablets()
    res = BenchmarkResult(cfg, data.source_sha256)
    np.random.default_rng(20260901)
    per_seed: dict[str, dict[str, list[float]]] = {}
    pooled_evs: dict[str, list[dict[str, np.ndarray]]] = {}
    curve_acc: dict[str, list[list[float]]] = {}
    curve_acc_home: dict[str, list[list[float]]] = {}
    holdout_acc: list[dict[str, Any]] = []

    def acc(group: str, jm: JointMetrics) -> None:
        d = per_seed.setdefault(group, {})
        for k, v in asdict(jm).items():
            if k in ("n", "n_released"):
                continue
            d.setdefault(k, []).append(float(v))

    n_test = data.test1.shape[0]
    lot_id = np.arange(n_test) % cfg.synthetic_lots
    time_id = (np.arange(n_test) * cfg.synthetic_time_blocks) // n_test
    conc_edges = np.percentile(data.test_y, [33.3, 66.7])
    conc_id = np.digitize(data.test_y, conc_edges)

    for seed in range(cfg.seeds):
        srng = np.random.default_rng(seed)
        layer = fit_layer(
            data.cal1,
            data.cal_y,
            srng,
            alpha=cfg.alpha,
            ood_alpha=cfg.ood_alpha,
            n_train=cfg.n_train,
            n_components=cfg.n_components,
            pls_scale=cfg.pls_scale,
            gate_score=cfg.gate_score,
            component_selection=cfg.component_selection,
        )
        ev_home = evaluate(layer, data.test1, data.test_y)
        ev_shift = evaluate(layer, data.test2, data.test_y)
        acc("home", joint_metrics(ev_home))
        acc("shift", joint_metrics(ev_shift))
        pooled_evs.setdefault("home", []).append(ev_home)
        pooled_evs.setdefault("shift", []).append(ev_shift)
        # by synthetic lot / time / concentration on the shifted instrument
        for name, groups in (
            ("synthetic_lot", lot_id),
            ("synthetic_time", time_id),
            ("concentration_tertile", conc_id),
        ):
            for g in np.unique(groups):
                mask = groups == g
                acc(
                    f"shift_by_{name}_{g}", joint_metrics({k: v[mask] for k, v in ev_shift.items()})
                )
        # risk-coverage curve over the gate threshold (shift instrument)
        for thr in cfg.ood_grid:
            e = evaluate(layer, data.test2, data.test_y, ood_alpha=thr)
            jm = joint_metrics(e)
            cost = (
                cfg.fallback_cost * jm.abstention_fraction
                + cfg.wrong_release_cost * jm.unconditional_wrong_release
            )
            curve_acc.setdefault(f"thr_{thr}", []).append(
                [
                    jm.released_fraction,
                    jm.conditional_error_among_released,
                    jm.unconditional_wrong_release,
                    cost,
                ]
            )
        # baselines on the shifted instrument
        acc(
            "shift_no_gate",
            joint_metrics(
                {"covered": ev_shift["covered"], "released": np.ones(n_test, dtype=bool)}
            ),
        )
        acc(
            "shift_mandatory_hold",
            joint_metrics(
                {"covered": ev_shift["covered"], "released": np.zeros(n_test, dtype=bool)}
            ),
        )
        # repair: recalibrated quantile with n verified assays measured on the shifted instrument (from the calibration set)
        for n_rep in cfg.repair_sizes:
            pick = srng.choice(layer.cal_idx, size=min(n_rep, len(layer.cal_idx)), replace=False)
            q_new = recalibrated_quantile(layer, data.cal2[pick], data.cal_y[pick])
            pred = layer.pls.predict(snv(data.test2)).ravel()
            cov = np.abs(pred - data.test_y) <= q_new
            acc(
                f"shift_repaired_quantile_n{n_rep}",
                joint_metrics({"covered": cov, "released": np.ones(n_test, dtype=bool)}),
            )
            per_seed.setdefault(f"shift_repaired_quantile_n{n_rep}", {}).setdefault(
                "interval_half_width_mg", []
            ).append(q_new)
            # slope/bias transfer with the same n standards
            pred_sb = slope_bias_correct(layer, data.cal1[pick], data.cal2[pick], data.test2)
            acc(
                f"shift_slope_bias_n{n_rep}",
                joint_metrics(
                    {
                        "covered": np.abs(pred_sb - data.test_y) <= layer.q,
                        "released": np.ones(n_test, dtype=bool),
                    }
                ),
            )
            if n_rep >= 15:
                x_pds = pds_transform(data.cal1[pick], data.cal2[pick], data.test2)
                pred_pds = layer.pls.predict(x_pds).ravel()
                acc(
                    f"shift_pds_n{n_rep}",
                    joint_metrics(
                        {
                            "covered": np.abs(pred_pds - data.test_y) <= layer.q,
                            "released": np.ones(n_test, dtype=bool),
                        }
                    ),
                )
        # instrument standardization baseline: center shifted spectra to the home mean
        x_std = snv(data.test2) - snv(data.cal2).mean(axis=0) + snv(data.cal1).mean(axis=0)
        pred_std = layer.pls.predict(x_std).ravel()
        acc(
            "shift_mean_centering",
            joint_metrics(
                {
                    "covered": np.abs(pred_std - data.test_y) <= layer.q,
                    "released": np.ones(n_test, dtype=bool),
                }
            ),
        )
        # stress tests on home spectra: does the gate abstain, and what is the exposure?
        for kind, mag in (
            ("wavelength_shift", 2),
            ("baseline_offset", 0.5),
            ("baseline_slope", 0.5),
            ("gain", 0.1),
            ("noise", 0.5),
            ("spikes", 3),
            ("dead_channels", 20),
            ("gradual_drift", 1.0),
        ):
            xs = apply_shift(data.test1, kind, srng, mag)
            acc(f"stress_{kind}", joint_metrics(evaluate(layer, xs, data.test_y)))
        # label noise in the calibration references
        noisy = fit_layer(
            data.cal1,
            data.cal_y,
            np.random.default_rng(seed + 10_000),
            alpha=cfg.alpha,
            ood_alpha=cfg.ood_alpha,
            n_train=cfg.n_train,
            label_noise_sd=5.0,
            n_components=cfg.n_components,
            pls_scale=cfg.pls_scale,
            gate_score=cfg.gate_score,
            component_selection=cfg.component_selection,
        )
        acc("home_label_noise_5mg", joint_metrics(evaluate(noisy, data.test1, data.test_y)))
        per_seed.setdefault("model", {}).setdefault("n_components", []).append(
            float(layer.n_components)
        )
        per_seed["model"].setdefault("interval_half_width_mg", []).append(layer.q)

        # ---- extensions (design-space Phase G). Every draw below comes from separate
        # streams so the values above are bit-identical to the pre-extension package.
        ext = np.random.default_rng(seed + 20_000)
        for name, ev in (("home", ev_home), ("shift", ev_shift)):
            sst = float(((data.test_y - data.test_y.mean()) ** 2).sum())
            r2 = 1.0 - float(((ev["pred"] - data.test_y) ** 2).sum()) / sst if sst > 0 else 0.0
            per_seed[name].setdefault("r2", []).append(r2)
            sel = aurc(ev["pval"], ev["covered"])
            for k, v in sel.items():
                per_seed.setdefault("selective_prediction", {}).setdefault(
                    f"{name}_{k}", []
                ).append(v)
        for n_rep in cfg.extra_repair_sizes:
            pick = ext.choice(layer.cal_idx, size=min(n_rep, len(layer.cal_idx)), replace=False)
            q_new = recalibrated_quantile(layer, data.cal2[pick], data.cal_y[pick])
            pred = layer.pls.predict(snv(data.test2)).ravel()
            cov = np.abs(pred - data.test_y) <= q_new
            acc(
                f"shift_repaired_quantile_n{n_rep}",
                joint_metrics({"covered": cov, "released": np.ones(n_test, dtype=bool)}),
            )
            per_seed.setdefault(f"shift_repaired_quantile_n{n_rep}", {}).setdefault(
                "interval_half_width_mg", []
            ).append(q_new)
        for n_std in cfg.transfer_sizes:
            pick = ext.choice(layer.cal_idx, size=min(n_std, len(layer.cal_idx)), replace=False)
            for label, xmap in (
                ("ds", ds_transform(data.cal1[pick], data.cal2[pick], data.test2)),
                (
                    "instrument_std",
                    instrument_standardization(data.cal1[pick], data.cal2[pick], data.test2),
                ),
            ):
                pred_map = layer.pls.predict(xmap).ravel()
                acc(
                    f"shift_{label}_n{n_std}",
                    joint_metrics(
                        {
                            "covered": np.abs(pred_map - data.test_y) <= layer.q,
                            "released": np.ones(n_test, dtype=bool),
                        }
                    ),
                )
        for thr in cfg.ood_grid:  # home-instrument curve: what the gate costs when nothing shifted
            jm_h = joint_metrics(evaluate(layer, data.test1, data.test_y, ood_alpha=thr))
            curve_acc_home.setdefault(f"thr_{thr}", []).append(
                [
                    jm_h.released_fraction,
                    jm_h.conditional_error_among_released,
                    jm_h.unconditional_wrong_release,
                    cfg.fallback_cost * jm_h.abstention_fraction
                    + cfg.wrong_release_cost * jm_h.unconditional_wrong_release,
                ]
            )
        hold = holdout_shift_matrix(
            layer,
            data.test1,
            data.test2,
            data.test_y,
            np.random.default_rng(seed + 30_000),
            grid=cfg.holdout_grid,
            detection_target=cfg.holdout_detection_target,
        )
        holdout_acc.append(hold)

    # Bootstrap intervals: keys that existed before the Phase G extension are drawn first,
    # in their original order and from the original stream, so their intervals are
    # bit-identical to earlier runs; extension keys draw from a second stream.
    ext_groups = {"selective_prediction"} | {
        f"shift_repaired_quantile_n{n}" for n in cfg.extra_repair_sizes
    }

    def is_ext(group: str, key: str) -> bool:
        return (
            group in ext_groups
            or group.startswith(("shift_ds_n", "shift_instrument_std_n"))
            or key == "r2"
        )

    boot = np.random.default_rng(12345)
    res.metrics = {}
    for g, vals in per_seed.items():
        legacy = {k: v for k, v in vals.items() if not is_ext(g, k)}
        if legacy:
            res.metrics[g] = _ci_block(legacy, boot)
    boot_ext = np.random.default_rng(12346)
    for g, vals in per_seed.items():
        extension = {k: v for k, v in vals.items() if is_ext(g, k)}
        if extension:
            res.metrics.setdefault(g, {}).update(_ci_block(extension, boot_ext))
    res.metrics["pooled_home"] = asdict(pooled(pooled_evs["home"]))
    res.metrics["pooled_shift"] = asdict(pooled(pooled_evs["shift"]))
    res.curves["risk_coverage_shift"] = {
        k: {
            "released_fraction": float(np.nanmean([r[0] for r in v])),
            "conditional_error_among_released": float(np.nanmean([r[1] for r in v])),
            "unconditional_wrong_release": float(np.nanmean([r[2] for r in v])),
            "operational_cost": float(np.nanmean([r[3] for r in v])),
        }
        for k, v in curve_acc.items()
    }
    res.curves["risk_coverage_home"] = {
        k: {
            "released_fraction": float(np.nanmean([r[0] for r in v])),
            "conditional_error_among_released": float(np.nanmean([r[1] for r in v])),
            "unconditional_wrong_release": float(np.nanmean([r[2] for r in v])),
            "operational_cost": float(np.nanmean([r[3] for r in v])),
        }
        for k, v in curve_acc_home.items()
    }
    res.curves["holdout_shift"] = _aggregate_holdout(holdout_acc)
    res.curves["cost_parameters"] = cost_parameters(cfg.cost_product_id)
    res.curves["cost_curve_usd_shift"] = cost_curve_usd(
        res.curves["risk_coverage_shift"], res.curves["cost_parameters"]
    )
    res.curves["cost_curve_usd_home"] = cost_curve_usd(
        res.curves["risk_coverage_home"], res.curves["cost_parameters"]
    )
    res.notes += [
        "Instrument is the only real group; lot and time groups are SYNTHETIC index blocks and test nothing about real lots or time.",
        "Wrong release here means the certified interval missed the reference assay; it is not an out-of-specification release rate.",
        "Repair curves reuse calibration tablets re-measured on the shifted instrument; they never touch the test set.",
        "PLS components are chosen by 5-fold CV on the training partition of each seed (the repository's fixed N_PLS=8 is not reproduced).",
        "No Telo data, no target chemistry, no prospective validation; this supports stop-the-line detection claims only.",
        f"Gate statistic: {cfg.gate_score}; component selection: {cfg.component_selection}.",
        "AURC and E-AURC (selective prediction) use the conformal p-value as confidence and an interval miss as the error; ties broken in expectation.",
        "Held-out shift-type matrix: threshold tuned to reach the detection target on one family, evaluated on every other; synthetic families are generated from a separate stream.",
        "Operational cost curve in USD uses the study's parameter sets (tier 5 illustrative) instead of the relative 1:50 weights; the wrong-release cost is a placeholder until a recall-cost source exists.",
    ]
    return res


def _aggregate_holdout(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Mean over seeds of the held-out shift-type matrix."""
    if not runs:
        return {}
    fams = list(runs[0]["rows"])
    out: dict[str, Any] = {"families": fams, "rows": {}}
    for tune_on in fams:
        rows = [r["rows"][tune_on] for r in runs]
        out["rows"][tune_on] = {
            "tuned_threshold_mean": float(np.mean([r["tuned_threshold"] for r in rows])),
            "target_reachable_fraction": float(np.mean([r["target_reachable"] for r in rows])),
            "home_clean_abstention": float(np.mean([r["home_clean_abstention"] for r in rows])),
            "released_on": {
                fam: float(np.mean([r["released_on"][fam] for r in rows])) for fam in fams
            },
        }
    diag = [out["rows"][f]["released_on"][f] for f in fams]
    off = [out["rows"][a]["released_on"][b] for a in fams for b in fams if a != b]
    out["summary"] = {
        "mean_released_in_family": float(np.mean(diag)),
        "mean_released_out_of_family": float(np.mean(off)),
        "worst_out_of_family_released": float(np.max(off)),
    }
    return out


def _fmt(d: dict[str, dict[str, float]], k: str) -> str:
    if k not in d:
        return "-"
    return f"{d[k]['mean']:.3f} [{d[k]['ci95_low']:.3f}, {d[k]['ci95_high']:.3f}] (seeds {int(d[k]['seeds_with_value'])})"


def model_card(res: BenchmarkResult) -> str:
    m = res.metrics
    home, shift = m["home"], m["shift"]

    lines = [
        "# Model card: conservative release gate on public NIR tablet spectra",
        "",
        f"**{res.banner}**",
        "",
        "## Intended use",
        "Research evidence that a conventional PLS calibration fails under instrument shift and that a conformal novelty gate can detect the shift and decline to certify. Not for batch release, not evidence on any sterile injectable, not a validated method.",
        "",
        "## Data",
        f"IDRC 2002 NIR tablet shootout (frozen as source S28, sha256 {res.data_sha256[:12]}...): 155 calibration and 460 test tablets measured on two instruments; assay (mg) as reference. No lot, time, operator, or site metadata exist; synthetic groups are index blocks.",
        "",
        "## Method",
        f"SNV, PLS with {'a fixed ' + str(res.config.n_components) + ' components (repository reproduction mode)' if res.config.n_components else '5-fold-CV-selected components'}{' with per-wavelength standardization (scale=True)' if res.config.pls_scale else ' without per-wavelength standardization (scale=False)'} on a {res.config.n_train}-tablet training partition, split-conformal interval at alpha = {res.config.alpha} on the remaining calibration tablets, 1-NN novelty gate with conformal p-value threshold {res.config.ood_alpha}; {res.config.seeds} random partitions; bootstrap 95% intervals over partitions.",
        "",
        "## Metrics that travel together (test instrument = shift)",
        "",
        "| Metric | Home instrument | Shifted instrument |",
        "|---|---|---|",
    ]
    for k in (
        "released_fraction",
        "abstention_fraction",
        "unconditional_wrong_release",
        "conditional_error_among_released",
        "empirical_coverage",
        "false_hold_rate",
        "r2",
    ):
        lines.append(f"| {k} | {_fmt(home, k)} | {_fmt(shift, k)} |")
    lines += [
        "",
        f"Pooled shifted-instrument counts: released {m['pooled_shift']['n_released']} of {m['pooled_shift']['n']} tablet-evaluations.",
        "",
        "## Risk-coverage curve (shifted instrument, gate threshold sweep)",
        "",
        "| threshold | released | conditional error | unconditional exposure | operational cost (relative) |",
        "|---|---|---|---|---|",
    ]
    for k, v in res.curves["risk_coverage_shift"].items():
        lines.append(
            f"| {k.replace('thr_', '')} | {v['released_fraction']:.3f} | {v['conditional_error_among_released']:.3f} | {v['unconditional_wrong_release']:.3f} | {v['operational_cost']:.3f} |"
        )
    lines += [
        "",
        "## Baselines and repair (shifted instrument, no gate)",
        "",
        "| Configuration | empirical coverage | unconditional wrong release |",
        "|---|---|---|",
    ]
    for k in sorted(m):
        if k.startswith(
            (
                "shift_no_gate",
                "shift_mandatory",
                "shift_repaired",
                "shift_slope",
                "shift_pds",
                "shift_mean",
                "shift_ds",
                "shift_instrument_std",
            )
        ):
            lines.append(
                f"| {k} | {_fmt(m[k], 'empirical_coverage')} | {_fmt(m[k], 'unconditional_wrong_release')} |"
            )
    lines += [
        "",
        "## Stress tests (home spectra with synthetic faults)",
        "",
        "| Fault | released fraction | unconditional wrong release |",
        "|---|---|---|",
    ]
    for k in sorted(m):
        if k.startswith(("stress_", "home_label")):
            lines.append(
                f"| {k} | {_fmt(m[k], 'released_fraction')} | {_fmt(m[k], 'unconditional_wrong_release')} |"
            )
    sp = m.get("selective_prediction", {})
    if sp:
        lines += [
            "",
            "## Selective prediction (gate confidence = conformal p-value; error = interval miss)",
            "",
            "| Metric | Home instrument | Shifted instrument |",
            "|---|---|---|",
        ]
        for k in ("aurc", "e_aurc", "aurc_oracle"):
            lines.append(f"| {k} | {_fmt(sp, 'home_' + k)} | {_fmt(sp, 'shift_' + k)} |")
    hold = res.curves.get("holdout_shift", {})
    if hold:
        fams = hold["families"]
        lines += [
            "",
            f"## Held-out shift-type protocol (threshold tuned for {res.config.holdout_detection_target:.0%} detection on the row family; cells = released fraction on the column family)",
            "",
            "| tuned on | threshold | home abstention | " + " | ".join(fams) + " |",
            "|---|---|---|" + "---|" * len(fams),
        ]
        for tune_on in fams:
            r = hold["rows"][tune_on]
            cells = " | ".join(f"{r['released_on'][f]:.2f}" for f in fams)
            lines.append(
                f"| {tune_on} | {r['tuned_threshold_mean']:.2f} | {r['home_clean_abstention']:.2f} | {cells} |"
            )
        s = hold["summary"]
        lines.append("")
        lines.append(
            f"In-family released {s['mean_released_in_family']:.2f}; out-of-family released {s['mean_released_out_of_family']:.2f} (worst {s['worst_out_of_family_released']:.2f})."
        )
    cp = res.curves.get("cost_parameters")
    if cp:
        lines += [
            "",
            "## Operational cost curves in USD (illustrative cost inputs)",
            "",
            f"False hold {cp['false_hold_usd']:,.0f} USD (testing {cp['inputs']['testing_usd_per_batch']['value']:,.0f} + {cp['false_hold_delay_carrying_usd']:,.0f} delay carrying on a {cp['batch_value_usd']:,.0f} USD batch); with investigation {cp['false_hold_with_investigation_usd']:,.0f}; wrong release {cp['wrong_release_usd']:,.0f} (tier {cp['inputs']['wrong_release_cost_usd']['tier']}); implied ratio {cp['implied_cost_ratio_wrong_to_false_hold']:.1f} vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.",
        ]
        for label, key in (
            ("home instrument", "cost_curve_usd_home"),
            ("shifted instrument", "cost_curve_usd_shift"),
        ):
            cc_ = res.curves.get(key)
            if not cc_:
                continue
            lines += [
                "",
                f"### {label}",
                "",
                "| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |",
                "|---|---|---|---|---|---|",
            ]
            for k, v in cc_.items():
                be = v["break_even_wrong_release_usd"]
                lines.append(
                    f"| {k.replace('thr_', '')} | {v['abstention_fraction']:.3f} | {v['unconditional_wrong_release']:.3f} | {v['cost_usd_per_batch']:,.0f} | {v['cost_usd_per_batch_with_investigation']:,.0f} | {'inf' if not math.isfinite(be) else f'{be:,.0f}'} |"
                )
    lines += ["", "## Limitations", ""] + [f"- {n}" for n in res.notes]
    lines += [
        "",
        "## Claims table",
        "",
        "| Claim | Allowed |",
        "|---|---|",
        "| Detects this instrument shift and abstains | yes, as measured above |",
        "| Automates batch release | no |",
        "| Useful operational coverage under shift | no (see released fraction on the shifted instrument) |",
        "| Evidence on the target drug chemistry | no |",
        "| Prospective product/site validation | no |",
        "| Replaces sterility assurance or any mandatory test | no |",
    ]
    return "\n".join(lines) + "\n"


def write_results(res: BenchmarkResult, out_root: Path = RESULTS_RA) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = out_root / f"ra_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(
        json.dumps(
            {
                "config": asdict(res.config),
                "data_sha256": res.data_sha256,
                "metrics": res.metrics,
                "curves": res.curves,
                "notes": res.notes,
                "banner": res.banner,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    (out / "model_card.md").write_text(model_card(res), encoding="utf-8")
    return out
