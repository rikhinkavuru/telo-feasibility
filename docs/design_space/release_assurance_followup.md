# Release-assurance follow-up (design-space assignment, Phase G)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Date 2026-09-02, session 2. Scope: the public-tablet release-gate evidence behind Telo's release-assurance claims. Nothing here is evidence about a sterile injectable, about Telo's own data, or about a validated method; the regulatory reading stays UNCERTAIN pending qualified review (`config/regulatory_gates.yaml` G15; `regulatory/release-constraints.md`).

Every number below names the artifact it comes from. Stored repository artifacts (`research/conformal/results/*.json`, produced by scripts that were read but never modified) are cited as `tablet_summary.json:instruments.shift.r2`; feasibility-package artifacts are cited by run id and key under `results/release_assurance/<run>/metrics.json`. Methods for the new benchmark components are in `docs/methods/release_benchmark.md` (Phase G section); this document answers the assignment's questions.

## 1. The 615-versus-654 audit and the claims-to-results map

### 1.1 Where the three counts come from

| Count | Origin | Evidence |
|---|---|---|
| 654 | Eigenvector's distribution page text, copied into the repository docstring | `research/conformal/data_tablet.py:3` ("654 pharmaceutical tablets measured on two NIR spectrometers"); `research/conformal/README.md:37-40` records that "the split sums to 655 while Eigenvector's distribution page says 654; the discrepancy is unresolved". The page text is not in any frozen snapshot (S28 froze only the `.mat` file), so 654 is a secondary quotation that this package cannot verify. |
| 655 | The shipped file | `data/raw_snapshots/S28/2026-09-02/nir_shootout_2002.mat` (sha256 `129a32ec9e194e568cbd96a200c88aabeb347156081b5dfbb0120372fdd6c22a`, 6,868,936 bytes; MD5 `9cdc57e841cbb8a422c44906f2b6d714`, identical to `research/conformal/data/tablet.mat`) holds `calibrate_1/2` (155, 650), `test_1/2` (460, 650) and `validate_1/2` (40, 650) with `calibrate_Y`, `test_Y`, `validate_Y`: 155 + 460 + 40 = 655 tablets, each measured on two instruments. |
| 615 | What the experiments use | `research/conformal/experiment_tablet.py:46-47` permutes the 155 calibration tablets and `:55-57` evaluates on the 460 test tablets; the 40 validation tablets are never loaded (`data_tablet.py:48-53` does not read `validate_*`). 155 + 460 = 615. The feasibility benchmark (`release_benchmark.load_tablets`) reads the same four arrays and also ignores the validation block. |

Verdict: every public sentence that says "654 tablets" describes a page count that neither the file nor the experiments reproduce. The defensible sentence is "615 tablets (155 calibration, 460 test) from the IDRC 2002 NIR shootout, each measured on two spectrometers; the distributed file holds 655 including 40 validation tablets that were not used". If a sentence describes the dataset rather than the experiment, "655 tablets in the distributed file" is the only count this package can verify.

### 1.2 Claims-to-results map

Reproduction status refers to the feasibility package's independent re-implementation in its three modes (`docs/methods/release_benchmark.md`): reproduction mode (8 components, per-wavelength standardization on, run `ra_20260902T045127Z`), 8 components without standardization (`ra_20260902T044739Z`), CV-selected components without standardization (`ra_20260902T044654Z`). Phase G re-ran all three with the extended metrics; the new run ids are listed in section 3 and give the same legacy values (the extension is bit-compatible on legacy keys).

| Claim | Where stated | Stored artifact and key | Stored value | Reproduced by this package | Allowed wording |
|---|---|---|---|---|---|
| C001 654 tablets, two spectrometers | web research page; `data_tablet.py:3` | file contents (section 1.1) | 655 in file, 615 used | yes (shapes read from the frozen file) | "615 tablets (155 calibration, 460 test) ... the file holds 655" |
| C002 R2 0.88 to 0.05 | `README.md:321`; web page | `tablet_summary.json:instruments.home.r2` = 0.8772; `instruments.shift.r2` = 0.0463 | 0.88 / 0.05 (means over 200 seeds) | reproduction mode: home R2 0.876, shift 0.111 (this run's `metrics.home.r2`, `metrics.shift.r2`; 50 seeds); the shift R2 is a mean of a widely dispersed quantity (audit 03: per-seed range -4.62 to 0.855) | "mean R2 fell from 0.88 to about 0.05-0.11 depending on partition; the shifted-instrument R2 is unstable across partitions" |
| C003 coverage 91% to 42% | `README.md:322`; web | `tablet_summary.json:instruments.home.naive_coverage` = 0.9142; `shift.naive_coverage` = 0.4159 | 0.91 / 0.42 | reproduction mode `metrics.home.empirical_coverage` 0.909 [0.896, 0.922], `metrics.shift.empirical_coverage` 0.410 [0.328, 0.493] | supported, with the standardization caveat below |
| C004 58% wrong certificate without a gate | web | `tablet_summary.json:instruments.shift.misrelease_naive` = 0.5841 (= 1 - coverage) | 0.58 | `metrics.shift_no_gate.unconditional_wrong_release` 0.590 [0.507, 0.673] | "58% of shifted-instrument predictions fell outside their certified interval"; this is an interval-miss rate, not an out-of-specification release rate |
| C005 gate holds exposure near 1% by abstaining on 98.9% | older README; task statement | `tablet_summary.json:instruments.shift.misrelease_gated` = 0.0074; `shift.release_rate` = 0.0110 | 0.7% / 98.9% | reproduction mode `metrics.shift.unconditional_wrong_release` 0.006 [0.001, 0.014]; `metrics.shift.released_fraction` 0.010 [0.001, 0.027]. Without per-wavelength standardization: released 0.303, exposure 0.046; with CV components: released 0.561, exposure 0.155 | true for one pipeline only (8 components with standardization); under a standard pipeline the gate releases 30-56% of shifted tablets with 16-29% conditional error |
| C006 conditional coverage among released 32.6% | task statement | `tablet_summary.json:instruments.shift.coverage_on_released` = 0.3260 (mean over the 23 of 200 seeds that released anything; audit 03: pooled 308 / 1,009 = 0.305) | 0.33 | reproduction mode `metrics.shift.conditional_error_among_released` 0.609 [0.272, 0.881] over 7 of 50 seeds, i.e. conditional coverage 0.39; small denominators in both packages | "among the few released shifted tablets, coverage was roughly 30-40%; fewer than one seed in eight released anything" |
| C007 mis-release "near 3%" | web page and `research.js` `shiftGated: 3` | no tablet key equals 3%. Nearest stored numbers: corn `summary.json:properties.protein.instruments.mp5.abstain_release_rate` = 0.044 and `mp6` = 0.0348 (these are release rates, not mis-release); tablet gated exposure is 0.0074 | none | not reproduced; no artifact | remove until traced to a key; the tablet gated exposure is 0.7% in one pipeline and 4.6-15.5% in the others |
| "86.9% release yield at a proved 90%" | `README.md:63,81,118,573,584` | `benchmark_summary.json:methods.ours_rrcm.release_yield` = 0.8688; `guarantee_summary.json:methods.rrcm_full_conformal.release_yield` = 0.8688, `coverage` 0.95, `mean_width_mg` 12.23; `risk_summary.json:uncertified_baseline.release_yield_of_in_spec` = 0.8698 (on 360 held-back tablets) | 86.9% | not reproduced here: the feasibility benchmark implements split conformal only; full-conformal ridge is out of its scope | "86.9% of in-specification tablets released with the interval inside the USP window, home instrument, official split; coverage 95% against a 90% guarantee that is exact conditional on the ridge penalty selected from the same 155 labels (`guarantee_summary.json:methods.rrcm_in_bag_penalty` removes that condition at coverage 0.943, yield 0.864)" |
| Comparator rows (split 84.3%, CV+ 89.2%, jackknife+-after-bootstrap 90.3%, crepes 66.0%, RTRT 84.4%) | `README.md:105-119` | `benchmark_summary.json:methods.{mapie_split,mapie_cv,mapie_jab,crepes_norm,rtrt_fixed}.release_yield` = 0.8426, 0.8922, 0.9032, 0.6601, 0.8438 | as stated | not reproduced (out of scope); the README rows match the JSON; whether the web page rows match is the claims-corrections track's finding (`docs/design_space/public_claims_corrections.md`) | quote from the JSON with "100 random partitions, home instrument" |
| "nine assays is enough" (coverage 90.1% at 48.3 mg width) | `README.md:340-348` | `operating_summary.json:recal_cost.disjoint[n=9]` coverage 0.9009, width 48.30 mg; paired variant 0.9057 / 49.05 | 90.1% / 48.3 mg | `metrics.shift_repaired_quantile_n9.empirical_coverage` 0.910 [0.883, 0.933] (reproduction mode), 0.894 [0.867, 0.919] (CV mode); half-width 21.6 mg in reproduction mode (the operating script's 25-tablet split produces wider intervals) | "with nine verified assays on the new instrument the recalibrated interval covered about 90% at roughly 2-4 times the home width" |
| Corn: coverage 1.4% / 1.1% on changed sensors, release 4.4% / 3.5%, recalibrated 89.9% / 91.0% | `README.md:305-313` | `summary.json:properties.protein.instruments.{mp5,mp6}.{naive_coverage,abstain_release_rate,recal_coverage}` = 0.0143 / 0.0113, 0.044 / 0.0348, 0.8987 / 0.9098 | as stated | not reproduced (corn data are not frozen as a study source) | quote with "protein, 300 partitions" |

Proposed `CLAIMS_REGISTER.csv` updates (not applied here; the claims-corrections track owns the file this session):

| claim_id | evidence_status | evidence_pointer addition | allowed_external_wording |
|---|---|---|---|
| C001 | partial | `data/raw_snapshots/S28/2026-09-02/nir_shootout_2002.mat` shapes 155/460/40 | as in section 1.1 |
| C002 | supported with caveat | add `ra_<reproduction run>/metrics.json:metrics.shift.r2` | shifted R2 unstable across partitions |
| C005 | supported for one pipeline; implementation-sensitive | add held-out shift matrix (section 4) | the gate's abstention on the real instrument change does not transfer to other shift types at the same threshold |
| C006 | supported with small-denominator caveat | unchanged | unchanged |
| C007 | unsupported | no artifact; nearest are corn release rates | remove |
| new C011 | supported (README only) | `benchmark_summary.json:methods.ours_rrcm`; `guarantee_summary.json:methods.rrcm_in_bag_penalty` | 86.9% yield with the penalty-selection condition stated, or 86.4% without it |
| new C012 | supported with caveat | `operating_summary.json:recal_cost.disjoint` | nine assays restore coverage at 2-4x width; three do not (section 3) |

## 2. Leakage audit of `research/conformal`

Scope: `experiment_tablet.py`, `conformal_core.py`, `data_tablet.py`, `experiment.py` (corn), `validate_core.py`, plus the scripts that produce the other public numbers (`benchmark_release.py`, `experiment_guarantee.py`, `experiment_risk.py`, `experiment_operating.py`, `experiment_gate.py`). Nothing under `research/conformal` was modified; effect sizes were measured by re-running the affected path inside the feasibility package (section 3 run ids).

| # | Check | Where | Finding | Verdict | Effect size |
|---|---|---|---|---|---|
| a1 | Hyperparameter selection touching the guarantee's calibration data | `experiment_tablet.py:23` `N_PLS = 8  # chosen by held-out R2 on instrument 1 (R2~0.90)`; no selection code exists | The selection rule is unreproducible. Audit 03 found the argmax is 4 under both the official test set (R2 0.907) and a 50-tablet hold-out (0.956); 8 gives 0.878 / 0.935. Whatever was done did not pick the test-optimal value. | not reproducible; no evidence of inflation | Feasibility package: fixed 8 components vs 5-fold CV on the training partition (mean 4.1 components): home coverage 0.903 vs 0.928 (runs in section 3); the fixed choice under-fits rather than over-fits |
| a2 | Component selection with the conformal-calibration tablets included | `experiment_tablet.py` cannot be checked (no code); the feasibility package measures the leak explicitly with `component_selection=train_and_calibration_cv` | If components had been chosen with the 50 calibration tablets in the CV pool, the calibration residuals would no longer be exchangeable with test residuals | measured, see section 3 | section 3, run D vs run C |
| a3 | Lasso penalty selected on all 155 calibration tablets, then split conformal calibrated on 25 of them | `benchmark_release.py:131` `alpha_full = pick_alpha(cal1[allidx], ...)` (5-fold CV over all 155), `:149` per-seed 130 / 25 split, `:176-179` MAPIE split conformalized on the 25 | The 25 calibration tablets' labels entered the hyperparameter; the "exact 90%" label on the `mapie_split` and `crepes_norm` rows is conditional on that selection | leak of type (a); affects comparator rows, not the tablet drift result | not measured here (Lasso path out of scope); the RRCM analogue below sizes the same mechanism |
| a4 | Ridge penalty for RRCM selected on the same 155 labels the full-conformal set is built from | `benchmark_release.py:140-142`; `experiment_guarantee.py:114-116` | Acknowledged in `README.md` ("exact conditional on that choice"); the repository's own `rrcm_in_bag_penalty` row selects the penalty inside the augmented bag and restores the unconditional theorem | acknowledged; measured by the repository | `guarantee_summary.json:methods.rrcm_full_conformal` vs `rrcm_in_bag_penalty`: coverage 0.950 vs 0.943, width 12.23 vs 12.36 mg, yield 0.869 vs 0.864 (100 partitions). The headline should quote the in-bag row or state the condition |
| a5 | RCPS calibration losses independent of the fit | `experiment_risk.py:118-119` (penalty on the 155 reference tablets only), `:130-136` (100 test tablets carved out for losses, 360 held back) | Two earlier designs leaked (documented in the module docstring, `:35-49`); the current one does not | no leak | n/a |
| b1 | SNV fitted on pooled data including test | `experiment_tablet.py:30-32`, `experiment.py:51-53`, `release_benchmark.snv` | SNV is a row-wise transform (each spectrum by its own mean and standard deviation); no cross-sample statistic | no leak | n/a |
| b2 | Per-wavelength standardization | `experiment_tablet.py:49` `PLSRegression(n_components=N_PLS)` uses sklearn's default `scale=True`, fitted on the 105 training tablets only | Not a leak (training statistics only) but the source of the implementation sensitivity: standardizing shifted spectra with home statistics amplifies the shift (`docs/methods/release_benchmark.md`) | benign; reported as sensitivity | coverage on the shifted instrument 0.410 with vs 0.768 without (runs `ra_20260902T045127Z` vs `ra_20260902T044739Z`) |
| c1 | Same physical tablet in train and calibration within a seed | `experiment_tablet.py:46-47` `idx = rng.permutation(155); tr, ca = idx[:105], idx[105:]` | Disjoint by construction | no leak | n/a |
| c2 | Same physical tablets across home and shift evaluations | `data_tablet.py:37-39`: `test1` and `test2` are the same 460 tablets on two instruments | Home and shift metrics are paired, not independent; harmless for the shift comparison and stated in the docstring | benign | n/a |
| c3 | Repair tablets shared with the home calibration | `experiment_tablet.py:67-69` recalibrates on `cal2[ca]`, the 50 conformal-calibration tablets re-measured on instrument 2 (paired) | The most favourable repair case; `experiment_operating.py:16-21, 99, 146` adds the disjoint variant and reports both (paired 0.906 vs disjoint 0.901 at n = 9) | benign; documented | 0.5 coverage points at n = 9 (`operating_summary.json:recal_cost`) |
| d1 | Gate threshold tuned on the shifted test set | `experiment_tablet.py:24` `OOD_ALPHA = 0.10` fixed before any evaluation; `experiment.py:44` likewise | Not tuned | no leak | n/a |
| d2 | Gate statistic chosen on the shifted test set | `experiment_operating.py:109-114`: the Q residual replaced the 1-NN score because "at a matched 5% false-alarm rate on home tablets, Q detects 99% of drifted tablets versus 71% for 1-NN"; the drifted tablets are `test2`, which `experiment_operating.py:125-141` then evaluates on | Model selection on the evaluation set (a binary choice, but the detection rates quoted for it were measured on the same 460 tablets that the operating curve reports) | leak (selection on test), small design space | section 3, run E vs run C: the two gate statistics' released fraction and exposure on the shifted instrument; the gap is the optimistic bias a fresh shift would not enjoy |
| d3 | Gate limits calibrated on home tablets | `experiment_gate.py:65,197-198`: 60 home calibration tablets calibrate every limit; evaluation on `test1`/`test2` | Calibration and evaluation disjoint | no leak | n/a |
| e1 | Instrument grouping respected | tablet: fit and calibrate on instrument 1 (`cal1`), evaluate on both; corn `experiment.py:90-91` fit on `m5` only | Respected | no leak | n/a |
| e2 | Pooled re-split | `experiment_guarantee.py:81-136` pools the 615 home tablets and re-splits | Deliberate diagnostic of the non-exchangeable official split, labelled "not a benchmark claim" | benign | RRCM coverage 0.950 (official) vs 0.905 (exchangeable); width 12.2 vs 10.5 mg (`guarantee_summary.json:exchangeable_split_diagnostic`) |
| e3 | Lot and time groups | none exist in either public dataset | Cannot be respected or violated; the feasibility benchmark's lot and time blocks are synthetic index blocks and say so | limitation | n/a |
| f1 | Corn recalibration and weighting | `experiment.py:125` fits the density-ratio classifier on calibration and unlabeled test covariates (legitimate for weighted conformal); `:134-137` recalibrates on the same 20 calibration samples re-measured on the target instrument (paired) | Weighted conformal uses unlabeled test covariates by definition; recalibration is the paired favourable case | benign | n/a |

Summary of the audit: no leak affects the tablet drift numbers (C002-C006). Two selection-on-data issues affect other public numbers: the Lasso and ridge penalties selected on the full reference set (a3, a4; the ridge case is acknowledged and its size is 0.5-0.7 coverage points) and the gate statistic chosen on the evaluation instrument (d2). The stated `N_PLS` selection rule is not reproducible (a1). The dominant fragility of the drift result is not leakage but implementation sensitivity (b2).

## 3. Extended benchmark runs (50 partitions each, frozen S28 data)

| Run | Mode | Run id | Purpose |
|---|---|---|---|
| A | 8 components, per-wavelength standardization on (repository reproduction) | `ra_20260902T222443Z` | reproduces the public drift numbers |
| B | 8 components, standardization off | `ra_20260902T222725Z` | isolates the standardization effect |
| C | 5-fold CV components (mean 4.14), standardization off | `ra_20260902T222900Z` | the standard pipeline |
| D | as C, components selected with the calibration tablets included | `ra_20260902T223019Z` | size of selection leak a2 |
| E | as C, gate statistic = PCA Q residual instead of 1-NN | `ra_20260902T223132Z` | size of gate-choice leak d2; the industry statistic |

Bit compatibility: every legacy metric and curve value in A, B, C equals the corresponding value in `ra_20260902T045127Z`, `ra_20260902T044739Z`, `ra_20260902T044654Z` (265 values each, zero differences; checked 2026-09-02). The five runs below therefore supersede the three earlier ones without changing any number already cited.

### 3.1 Shifted instrument (home in parentheses); keys `metrics.shift.*` and `metrics.home.*`

| Run | components | empirical_coverage | released_fraction | conditional_error_among_released | unconditional_wrong_release | false_hold_rate | r2 |
|---|---|---|---|---|---|---|---|
| A | 8 | 0.410 [0.328, 0.493] (0.909) | 0.010 [0.001, 0.027] (0.931) | 0.609 [0.272, 0.881], 7 seeds (0.077) | 0.006 [0.001, 0.014] (0.071) | 0.990 [0.973, 1.000] (0.054) | 0.111 (0.876) |
| B | 8 | 0.768 [0.733, 0.799] (0.903) | 0.303 [0.260, 0.347] (0.915) | 0.160 [0.137, 0.185] (0.081) | 0.046 [0.036, 0.055] (0.074) | 0.669 [0.622, 0.712] (0.069) | 0.735 (0.859) |
| C | 4.14 | 0.717 [0.685, 0.746] (0.928) | 0.561 [0.523, 0.602] (0.919) | 0.290 [0.256, 0.327] (0.067) | 0.155 [0.137, 0.172] (0.061) | 0.441 [0.393, 0.486] (0.076) | 0.774 (0.908) |
| D | 4.2 | 0.722 [0.695, 0.748] (0.927) | 0.563 [0.525, 0.602] (0.919) | 0.284 [0.253, 0.319] (0.067) | 0.152 [0.135, 0.169] (0.061) | 0.438 [0.391, 0.484] (0.075) | 0.774 (0.907) |
| E | 4.14 | 0.717 [0.684, 0.745] (0.928) | 0.000 [0.000, 0.001] (0.930) | 0.667 [0.400, 1.000], 3 seeds (0.068) | 0.000 [0.000, 0.001] (0.063) | 1.000 [0.999, 1.000] (0.065) | 0.774 (0.908) |

Leakage effect sizes (section 2):

- a2, component selection with the calibration tablets included (D versus C): every shifted-instrument metric moves by at most 0.5 points and stays inside the other run's interval; home coverage 0.927 versus 0.928. The leak is real in principle and negligible in size on this data.
- d2, gate statistic chosen on the evaluation instrument (E versus C): at the same nominal threshold the Q residual releases 0.000 of shifted tablets against 0.561 for the 1-NN score, with a lower home false-hold rate (0.065 versus 0.076). The repository's own comparison (`gate_summary.json:detectors."Q | conformal limit".detect@0.05` = 0.990 at false alarm 0.0435; `"1NN-PLS (ours, prior) | conformal limit"` = 0.7125 at 0.052) is consistent. The choice was made on the tablets it is evaluated on, so the abstention headline for the Q gate carries an unmeasured optimism; section 3.4 tests it on shift types it was never chosen on.
- a1/b2, fixed 8 components and standardization (A versus B versus C): the "98.9% abstention" is a property of run A only; B releases 30% and C 56%.

### 3.2 Selective prediction; keys `metrics.selective_prediction.*`

| Run | home aurc | home e_aurc | home aurc_oracle | shift aurc | shift e_aurc | shift aurc_oracle |
|---|---|---|---|---|---|---|
| A | 0.069 [0.060, 0.078] | 0.063 [0.056, 0.071] | 0.006 [0.004, 0.008] | 0.587 [0.498, 0.672] | 0.232 [0.203, 0.259] | 0.355 [0.271, 0.443] |
| B | 0.068 [0.059, 0.078] | 0.062 [0.054, 0.070] | 0.006 [0.005, 0.008] | 0.185 [0.159, 0.213] | 0.146 [0.129, 0.163] | 0.039 [0.027, 0.054] |
| C | 0.066 [0.058, 0.074] | 0.062 [0.055, 0.068] | 0.004 [0.003, 0.005] | 0.303 [0.266, 0.343] | 0.249 [0.224, 0.274] | 0.054 [0.042, 0.068] |
| D | 0.066 [0.059, 0.074] | 0.062 [0.056, 0.068] | 0.004 [0.003, 0.005] | 0.298 [0.265, 0.334] | 0.249 [0.224, 0.273] | 0.050 [0.040, 0.060] |
| E | 0.054 [0.047, 0.062] | 0.051 [0.044, 0.057] | 0.004 [0.003, 0.005] | 0.313 [0.279, 0.350] | 0.259 [0.234, 0.281] | 0.054 [0.042, 0.068] |

Reading: on the home instrument the excess AURC is almost the whole AURC (0.062 of 0.066 in C), so the gate's confidence carries almost no information about which released units will miss their interval; home misses are label and model errors that leave a normal spectrum (the repository's own finding, `risk_summary.json:where_marginal_coverage_fails`). On the shifted instrument the excess is 0.15 to 0.26 in every mode: the novelty score separates shifted from unshifted spectra but does not rank, within the shifted set, which predictions are still right. A gate that detects "something changed" is what this statistic supports; a gate that selects "which of these batches I can still certify" is not.

### 3.3 Repair and transfer; keys `metrics.<configuration>.empirical_coverage` on the shifted instrument, no gate

| Configuration | needs | A | B | C |
|---|---|---|---|---|
| shift_no_gate | nothing | 0.410 [0.330, 0.490] | 0.768 [0.735, 0.799] | 0.717 [0.686, 0.746] |
| shift_mean_centering | all 155 calibration spectra on both instruments, no assays | 0.841 [0.830, 0.852] | 0.839 [0.825, 0.852] | 0.861 [0.853, 0.870] |
| shift_instrument_std_n15 / n30 / n50 | 15 / 30 / 50 paired standards, no assays | 0.808 / 0.825 / 0.831 | 0.829 / 0.853 / 0.864 | 0.864 / 0.877 / 0.880 [0.873, 0.887] |
| shift_ds_n15 / n30 / n50 | paired standards, no assays | 0.844 / 0.826 / 0.777 | 0.857 / 0.831 / 0.768 | 0.845 / 0.852 / 0.826 |
| shift_pds_n15 / n30 / n50 | paired standards, no assays | 0.722 / 0.886 / 0.912 [0.901, 0.923] | 0.706 / 0.900 / 0.929 [0.919, 0.937] | 0.827 / 0.894 / 0.897 [0.889, 0.904] |
| shift_slope_bias_n9 / n30 | 9 / 30 verified assays | 0.817 / 0.834 | 0.805 / 0.831 | 0.856 / 0.865 |
| shift_repaired_quantile_n3 | 3 verified assays | 1.000, half-width +inf | 1.000, +inf | 1.000, +inf |
| shift_repaired_quantile_n5 | 5 verified assays | 1.000, +inf | 1.000, +inf | 1.000, +inf |
| shift_repaired_quantile_n9 | 9 verified assays | 0.910 [0.883, 0.933], half-width 21.6 mg | 0.913 [0.889, 0.934], 15.3 mg | 0.894 [0.867, 0.919], 13.3 mg |
| shift_repaired_quantile_n15 | 15 verified assays | 0.931, 22.4 mg | 0.923, 15.9 mg | 0.927, 15.2 mg |
| shift_repaired_quantile_n30 | 30 verified assays | 0.894, 18.6 mg | 0.909, 13.1 mg | 0.866, 10.8 mg |

Home half-widths for scale (`metrics.model.interval_half_width_mg`): A 8.35, B 8.86, C 7.09 mg. Reading: below nine verified assays there is no finite guarantee at alpha = 0.10 (the conformal rank exceeds n), so "repair with three samples" is not a degraded guarantee but no guarantee. Nine assays restore coverage near 0.90 at 1.9 to 2.6 times the home half-width. Among label-free repairs, piecewise direct standardization with 30 to 50 standards (0.89 to 0.93) beats full direct standardization, which degrades as standards are added because the 650-channel transfer matrix is under-determined and the ridge solution over-fits (0.83 to 0.78 at n = 50); the plain per-wavelength standardization fitted on standards reaches 0.86 to 0.88 in the standard pipeline with no model at all. None of the label-free repairs is inside the nominal 0.90 with its interval except PDS at n = 50 in modes A and B.

### 3.4 Held-out shift types; key `curves.holdout_shift` (released fraction on the column family at the threshold tuned for 90% detection on the row family)

Which families matter is fixed by the stress tests without a gate (`metrics.stress_<family>.empirical_coverage`, C mode): wavelength shift 0.002, dead channels 0.289, noise 0.462, spikes 0.601, baseline slope 0.821, and the real instrument change 0.717 collapse coverage; baseline offset, gain and gradual drift leave it at 0.928 because SNV removes them exactly, and every gate sees them as clean spectra (released 0.919, the same as clean home). Those three families are therefore harmless and invisible, and rows tuned on them cannot reach the target (`target_reachable_fraction` 0.00; the threshold falls to the grid maximum and abstains about half of clean batches). The informative cells are the harmful families.

| Run, tuned on | threshold | home abstention | wavelength | noise | spikes | dead channels | slope | instrument |
|---|---|---|---|---|---|---|---|---|
| A (1-NN, repro), instrument | 0.04 | 0.03 | 0.61 | 0.04 | 0.44 | 0.00 | 0.00 | 0.02 |
| A, wavelength shift | 0.17 | 0.12 | 0.07 | 0.00 | 0.04 | 0.00 | 0.00 | 0.00 |
| B (1-NN, no scaling), instrument | 0.23 | 0.19 | 0.21 | 0.11 | 0.43 | 0.01 | 0.14 | 0.08 |
| C (1-NN, CV), instrument | 0.48 (target reached in 32% of seeds) | 0.47 | 0.12 | 0.20 | 0.33 | 0.07 | 0.09 | 0.13 |
| C, dead channels | 0.23 | 0.22 | 0.39 | 0.57 | 0.69 | 0.10 | 0.40 | 0.46 |
| E (Q residual, CV), instrument | 0.04 | 0.02 | 0.07 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 |
| E, noise or spikes or dead channels | 0.02 (grid floor) | 0.00 | 0.54 | 0.00 | 0.00 | 0.00 | 0.36 | 0.44 |

Summary keys `curves.holdout_shift.summary`: in-family released A 0.19, B 0.24, C 0.27, E 0.17; out-of-family 0.38, 0.34, 0.31, 0.35. Reading:

1. With the repository's 1-NN gate in the standard pipeline (C), a threshold that abstains on 90% of the real instrument change is reachable in only a third of partitions and then holds 47% of clean batches; the gate has no operating point that detects the instrument change without gutting throughput.
2. With the industry Q residual under a conformal limit (E), a threshold set on the instrument change (0.04) transfers to every harmful synthetic fault at 2% false holds. Transfer fails in the other direction: a threshold set on a gross fault (noise, spikes, dead channels, which any threshold catches, so tuning stops at the grid floor) releases 44% of instrument-shifted and 54% of wavelength-shifted spectra. The protocol answer to "unknown shift types" is: tune on the subtlest shift you expect, never on the grossest.
3. In mode A the 1-NN gate tuned on the instrument change releases 61% of wavelength-shifted spectra whose coverage is 0.048, i.e. about 58% of those units would be certified wrongly. The repository's headline abstention does not transfer to a shift type it was not measured on.

### 3.5 Operational cost in USD; keys `curves.cost_parameters`, `curves.cost_curve_usd_home`, `curves.cost_curve_usd_shift`

Inputs (all tier 5 illustrative, product `sodium_bicarbonate_8_4_50ml`): testing 30,000 USD per batch; batch value 25,000 units x 1.20 USD = 30,000 USD; assay delay 5 days at a 0.20 carrying rate = 82 USD; false hold 30,082 USD (50,082 with an investigation); wrong release 2,000,000 USD (`wrong_release_cost_usd`, new placeholder); implied ratio 66.5 against the earlier relative weight of 50. Holding every batch for the laboratory costs one false hold per batch, 30,082 USD.

| Run | instrument | threshold 0.10: abstention, exposure, cost per batch | best threshold in grid: cost | break-even wrong-release cost at 0.10 |
|---|---|---|---|---|
| A | home | 0.069, 0.071, 144,155 | 0.5: 75,422 | 394,326 |
| A | shift | 0.990, 0.006, 41,348 | 0.5: 30,082 (abstain all) | 51,796 |
| B | home | 0.085, 0.074, 150,815 | 0.5: 86,597 | 371,342 |
| B | shift | 0.697, 0.046, 112,182 | 0.5: 33,408 | 199,907 |
| C | home | 0.081, 0.061, 125,230 | 0.5: 73,581 | 450,145 |
| C | shift | 0.439, 0.155, 323,811 | 0.5: 107,239 | 108,690 |

Reading: at an interval-miss exposure of 6 to 9% (alpha = 0.10) and a 2 M USD wrong-release cost, the gate loses to testing every batch on the home instrument in every mode (125,000 to 151,000 USD per batch against 30,082) and only breaks even if a wrong release costs less than about 0.37 to 0.45 M USD. On the shifted instrument the cheapest gate setting is to abstain on everything. Two qualifications fix the size of this conclusion rather than its direction. First, an interval miss is not a shipped out-of-specification unit: the repository measured out-of-specification-among-released at 0.36% on the home instrument (`risk_summary.json:uncertified_baseline.measured_out_of_spec_among_released` = 0.0036) and could certify only 2.95% with 100 calibration tablets (`rcps_certified."risk<=0.05".certified_risk_bound` = 0.0295). At the measured rate the gate would cost about 7,300 USD per batch in wrong releases plus its abstentions and would beat testing everything; at the certified bound it would cost 59,000 USD and would not. Second, every cost input is a placeholder; the parameter that decides the sign, `wrong_release_cost_usd`, has no source (`config/global.yaml`, source_locator).

## 4. Is the initial product "release prediction"?

Question from the assignment: is the best initial product release prediction, or is the defensible product drift detection, mandatory-hold support, documentation, deviation triage, or another quality workflow?

Answer from the numbers, in order of strength:

1. Release prediction (certifying a batch on the spectral prediction) is not defensible on this evidence.
   - Under an instrument change the calibration's coverage falls to 0.41 to 0.77 and the units the 1-NN gate still releases carry 16 to 61% conditional error (section 3.1). No mode has an operating point that keeps both released fraction and conditional error acceptable (`curves.risk_coverage_shift`, all runs).
   - The gate's confidence does not rank correctness among released units (E-AURC 0.15 to 0.26 on shift, and on home the excess is the whole AURC; section 3.2). Selective prediction in the sense of "release the ones I am sure of" is not what this statistic does.
   - At a 90% design coverage the interval-miss exposure alone makes the gate more expensive than testing every batch under the illustrative cost inputs unless a wrong release costs under about 0.4 M USD (section 3.5). The design level for a release decision has to come from the cost ratio and the certifiable out-of-specification bound, not from a conventional 90%.
   - The certificate a quality unit needs is on out-of-specification release, and it scales with reference units, not with model quality: a Clopper-Pearson bound at delta = 0.05 with zero observed losses needs 199 units for 1.5%, 299 for 1.0% and 598 for 0.5% (`risk_summary.json:reference_tablets_needed_to_certify`; recomputed here with the exact binomial). The repository has 155 reference tablets.
   - For an aseptically filled injectable, chemical real-time release removes about zero days from the hold because the sterility incubation is the critical path (`regulatory/release-constraints.md`, section 1; `test_full_release_assurance_saves_no_days_when_sterility_binds`). The manufacturing value that the pitch attached to release prediction does not exist for the product class.
   - Regulatory reading, UNCERTAIN pending qualified review: EU GMP Annex 17 section 3.10 forbids substituting end-product testing once real-time release testing fails or trends toward failure, so an abstention cannot be filed as "fall back to the laboratory"; it must be a pre-declared exclusion from the real-time-release scope (`regulatory/release-constraints.md`, section 2). The high-abstention behaviour that makes the gate safe is the behaviour that regulation makes hard to file as a release method.

2. Drift detection with a distribution-free limit on the industry's own statistic is defensible, narrowly.
   - The PCA Q residual under a conformal limit detects the instrument change completely at a 2% false-hold rate on clean batches (run E: released 0.000, home false hold 0.065 at the nominal threshold; tuned threshold 0.04 with home abstention 0.02) and the same threshold transfers to every harmful synthetic fault (section 3.4). The repository's incumbent comparison says the parametric Jackson-Mudholkar limit on the same statistic fires at 18.7% when it claims 5% (`gate_summary.json:detectors."Q | parametric limit".false_alarm@0.05` = 0.1868 against 0.0435 for the conformal limit at detection 0.990).
   - This is a "stop the line and hold" decision, which is what the protocol's evidence boundary already said the benchmark supports. It does not need a release claim, a coverage guarantee on the prediction, or a change to the sterility-bound release path.
   - Its limits are also measured: shifts that SNV removes are invisible (harmless here, not necessarily elsewhere), a threshold set on a gross fault misses subtle shifts, and there are no real lots, real drift, or target chemistry in the data.

3. Mandatory-hold support and documentation of the hold decision are the workflow around item 2 and do not depend on the prediction being right; the feasibility model's R1 scenario (measured administrative reduction of the serial QA component) is where such a product enters the network simulation, and its benefit is bounded by `qa_review_days` (base 2 days, tier 5).

4. Deviation triage and other quality workflows are outside this benchmark's evidence; nothing here supports or refutes them.

Conditions under which release prediction would become defensible, each with the evidence that would establish it:

| Condition | Threshold implied by this evidence | Evidence required |
|---|---|---|
| Certified out-of-specification release bound x wrong-release cost below the per-batch testing cost | at 2 M USD and 30,000 USD per batch: certified bound below 1.5%, i.e. about 200 reference batches with zero observed losses at delta = 0.05; at 0.5 M USD, 6%, about 50 batches | prospective reference assays on real batches of the target product; a sourced wrong-release cost (recall records or elicitation, HA-22) |
| Coverage under the shifts that occur in the plant, with the gate's abstention below the cost-optimal false-hold rate | conditional error among released within the design alpha under each real shift type; false holds below roughly 10% at the illustrative costs | real instrument, lot, operator and time metadata; the held-out-shift protocol run on real shift families instead of synthetic ones |
| Repair budget | at least nine verified assays per shift event for a finite guarantee at alpha = 0.10; more for a tighter alpha | agreed sampling plan and laboratory capacity for verification assays |
| A release-time benefit that exists for the product class | rapid-sterility and rapid-EM methods validated so that the assay is the critical path (`sterility_incubation_days` from 14 to about 2) | USP <72>/<73>/<1071> validation package for the product and site; regulatory acceptance (gate G15), UNCERTAIN |
| Regulatory form of abstention | abstention filed as a pre-declared exclusion from real-time-release scope | qualified regulatory review (HA-31) |

Until those conditions are met, the flagship should not be "release automation"; the defensible function this evidence supports is stop-the-line drift detection with a distribution-free limit, and the decision workflow around it.

## 5. What this leaves open

- Real lots, real drift, real operators and the target chemistry: absent from the data; the synthetic families and index-block groups test nothing about them.
- The wrong-release cost and the testing cost are placeholders; the sign of section 3.5 depends on their ratio.
- The Q-residual gate was chosen on the evaluation instrument (leak d2); section 3.4 shows it generalizes to synthetic faults, which is evidence, not proof, that it would generalize to a new real shift.
- Full-conformal ridge (RRCM), which carries the "86.9% at a proved 90%" claim, is outside this package; its reproduction would need the repository's `conformal_core.py` re-implemented or imported, and its guarantee should be quoted from the in-bag-penalty row.
- `CLAIMS_REGISTER.csv` updates proposed in section 1.2 are not applied here.

## 6. Artifacts

- Code: `src/telo_feasibility/release_benchmark.py` (additive: `q_residual`, `ds_transform`, `instrument_standardization`, `risk_coverage_points`, `aurc`, `tune_threshold`, `holdout_shift_matrix`, `cost_parameters`, `cost_curve_usd`, `_aggregate_holdout`, config fields `gate_score`, `component_selection`, `extra_repair_sizes`, `transfer_sizes`, `holdout_grid`, `holdout_detection_target`, `cost_product_id`); `scripts/run_release_benchmark.py` flags; `config/global.yaml` `wrong_release_cost_usd`.
- Tests: `tests/unit/test_release_benchmark_ext.py` (9 tests: DS identity and mixing recovery, standardization identity and affine repair, hand-computed AURC with a tie block, oracle and empty cases, threshold tuning, held-out matrix shape and bounds, cost parameters traced to configs and curve arithmetic with break-even, gate and selection option validation and Q-gate evaluation).
- Results: `results/release_assurance/ra_20260902T222443Z`, `ra_20260902T222725Z`, `ra_20260902T222900Z`, `ra_20260902T223019Z`, `ra_20260902T223132Z`, each with `metrics.json` and `model_card.md`; log `results/manifests/logs/release_benchmark_phaseG.log`.
- Methods: `docs/methods/release_benchmark.md`, Phase G section. Matrix rows R103 to R108.
