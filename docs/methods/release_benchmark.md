# Release-assurance benchmark: methods and the implementation-sensitivity finding

Code: `src/telo_feasibility/release_benchmark.py`; script `scripts/run_release_benchmark.py`; data source S28 (IDRC 2002 tablet NIR shootout, frozen 2026-09-02, sha256 in the manifest; MD5 equals the repository's copy). Outputs under `results/release_assurance/ra_*/` (metrics with bootstrap intervals over random calibration partitions, risk-coverage curve, model card, claims table).

## Three modes, one dataset

| Mode | PLS components | Per-wavelength standardization (`scale`) | Home coverage | Shifted coverage | Released on shift | Conditional error among released (seeds with any release) |
|---|---|---|---|---|---|---|
| Reproduction of the repository script (`n_components=8, pls_scale=True`), 50 seeds | 8 fixed | on (sklearn default) | 0.909 [0.896, 0.922] | 0.410 [0.328, 0.493] | 0.010 [0.001, 0.027] | 0.61 (7 of 50 seeds); pooled 0.58 over 229 released of 23,000 |
| Same components, no standardization (`n_components=8, pls_scale=False`), 50 seeds | 8 fixed | off | 0.903 [0.890, 0.914] | 0.768 [0.733, 0.799] | 0.303 | 0.160 (50 seeds) |
| Standard pipeline (`pls_scale=False`, 5-fold CV components), 50 seeds | 4.1 mean | off | 0.928 [0.916, 0.939] | 0.717 [0.685, 0.746] | 0.561 | 0.290 (50 seeds) |

Bootstrap 95% intervals over 50 random calibration partitions; runs `ra_20260902T045127Z` (reproduction), `ra_20260902T044739Z` (8 components, no standardization), `ra_20260902T044654Z` (CV components). The repository's stored result (200 seeds, different partitions) is shifted coverage 0.416, released 0.011, conditional coverage 0.326 over 23 seeds; the reproduction mode reproduces it within the intervals, and the two other modes do not.

## What this means

1. The headline "R2 0.88 to 0.05, coverage 91% to 42%, gate abstains on 98.9%" is a property of one pipeline: eight components with per-wavelength standardization, which both amplifies the instrument shift in the model's input space and makes the shift easy for a nearest-neighbour novelty score to detect. Removing the standardization halves the coverage collapse and the gate releases ten times as many shifted tablets.
2. In no mode is the gate operationally useful under this shift: released fractions are 4% to 60% with conditional error among released of 14% to 34%, against a 10% nominal. The protocol's evidence boundary stands: stop-the-line detection, not release.
3. Repair with a handful of verified assays on the new instrument (recalibrated quantile, n = 9) restores coverage near 0.90 at a wider interval; slope/bias transfer and PDS with 30 standards do similarly. These are the operationally relevant comparators for a plant that can afford reference assays.
4. Synthetic stress tests: baseline offset, gain, and gradual drift are invisible to SNV-based pipelines (SNV removes them) and harmless to coverage; wavelength shift, dead channels, noise, and spikes collapse coverage while the gate abstains only partially (released 0.35 to 0.86 with exposure up to 0.49). A gate that misses a wavelength shift is a gap the model card records.
5. Lot and time groups are synthetic index blocks in this data; nothing about real lots or drift is established.

## Consequences for the study

- `CLAIMS_REGISTER.csv` C005 and C006 now carry the implementation-sensitivity caveat.
- The release-assurance submodel's R2/R3 parameters, when used for scenario analysis, must cite the mode; the base scenario stays R0.
- This is a candidate non-obvious result (`results/manifests/nonobvious_finding_candidates.json`); it becomes the study's finding only if the author adopts it after review.

## Phase G extensions (2026-09-02, design-space assignment)

Everything below is additive: every metric key that existed before is computed from the same seeds and streams and is bit-identical (verified on a three-seed run in both modes, 530 legacy values, zero differences). Extension draws come from separate generators (`seed + 20000` for repair and transfer standards, `seed + 30000` for the held-out shift families) and the bootstrap for legacy keys runs first from the original stream.

### Calibration-transfer and domain-standardization baselines

| Baseline | Metric keys | What it needs | Method |
|---|---|---|---|
| Direct standardization (DS) | `shift_ds_n{15,30,50}` | paired transfer standards on both instruments, no assays | full transfer matrix F from shifted to home space, ridge-regularized because n standards < 650 channels (penalty scaled to the mean diagonal of S'S); Wang, Veltkamp, Kowalski 1991 |
| Per-wavelength instrument standardization | `shift_instrument_std_n{15,30,50}` | paired transfer standards, no assays | per-channel mean and standard-deviation matching fitted on the standards; the honest counterpart of the repository's `scale=True`, which standardized with home statistics only |
| Recalibrated quantile with n = 3 | `shift_repaired_quantile_n3` | 3 verified assays on the new instrument | finite-sample conformal quantile at alpha = 0.10 needs at least 9 residuals; with 3 the quantile is +inf, so the interval covers everything at infinite width (reported, not hidden) |

### Selective prediction

`selective_prediction.{home,shift}_{aurc,e_aurc,aurc_oracle}`. Confidence is the gate's conformal p-value; the error is an interval miss. Selective risk and coverage follow Geifman and El-Yaniv (NeurIPS 2017); AURC and its excess over the oracle ranking (E-AURC) follow Geifman, Uziel and El-Yaniv (ICLR 2019). The p-value is discrete (at most m + 1 values from m calibration scores), so ties are broken in expectation over random orderings within a tie block; `risk_coverage_points` documents the rule and a hand-computed test fixes it.

### Held-out shift-type protocol

`curves.holdout_shift`. For each seed the gate threshold is tuned on one family (the eight synthetic faults on home spectra, plus the real instrument change) to the smallest grid value that abstains on at least the detection target (default 90%) of that family, then evaluated on every family. Rows are the tuning family, columns the evaluation family, cells the released fraction (1 minus detection). The `home_clean_abstention` column is the false-hold proxy at that threshold, and `target_reachable_fraction` records how often the target was attainable within the grid (0 to 0.5). A large off-diagonal cell is a shift type the gate misses when its threshold was set on a different kind of shift.

### Operational cost curve in USD

`curves.cost_parameters` and `curves.cost_curve_usd_shift`. The earlier curve weighted a wrong release at 50 relative to a false hold at 1 with no provenance. The cost of a false hold is now `testing_usd_per_batch` plus `assay_days` of carrying cost on the batch's variable value (`units_per_batch` times materials plus conversion cost, times `inventory_carrying_rate` / 365.25), optionally plus `investigation_cost_usd`; the cost of a wrong release is the new global parameter `wrong_release_cost_usd` (tier 5, illustrative, no source; see `config/global.yaml`). Every input carries its tier and source locator into `metrics.json`. A wrong release here is a released batch whose certified interval missed the reference assay; it is not a shipped out-of-specification unit.

### Gate and selection options (for leakage effect sizes)

`BenchmarkConfig.gate_score` = `nn` (the repository's 1-NN distance in PLS-score space) or `q_residual` (PCA squared prediction error, the industry statistic); `component_selection` = `train_cv` (default) or `train_and_calibration_cv`, which deliberately selects PLS components with the conformal-calibration tablets included so the size of that selection leak can be measured. `R2` per instrument is now recorded next to coverage.

### Phase G runs (50 partitions each)

| Run id | components | standardization | gate | selection | shifted coverage | released on shift | shift E-AURC | held-out: out-of-family released |
|---|---|---|---|---|---|---|---|---|
| `ra_20260902T222443Z` | 8 | on | 1-NN | train CV | 0.410 [0.328, 0.493] | 0.010 | 0.232 | 0.38 |
| `ra_20260902T222725Z` | 8 | off | 1-NN | train CV | 0.768 [0.733, 0.799] | 0.303 | 0.146 | 0.34 |
| `ra_20260902T222900Z` | 4.14 (CV) | off | 1-NN | train CV | 0.717 [0.685, 0.746] | 0.561 | 0.249 | 0.31 |
| `ra_20260902T223019Z` | 4.2 (CV) | off | 1-NN | train + calibration CV (leak) | 0.722 [0.695, 0.748] | 0.563 | 0.249 | 0.31 |
| `ra_20260902T223132Z` | 4.14 (CV) | off | Q residual | train CV | 0.717 [0.684, 0.745] | 0.000 | 0.259 | 0.35 |

Keys: `metrics.shift.empirical_coverage`, `metrics.shift.released_fraction`, `metrics.selective_prediction.shift_e_aurc`, `curves.holdout_shift.summary.mean_released_out_of_family`. The first three runs reproduce every legacy value of `ra_20260902T045127Z`, `ra_20260902T044739Z` and `ra_20260902T044654Z` exactly. The reading of these runs, the leakage effect sizes, the repair and transfer table, the held-out matrix, and the cost curves are in `docs/design_space/release_assurance_followup.md`.
