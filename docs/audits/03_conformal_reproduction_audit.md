# Release-assurance evidence audit: reproduction of `research/conformal/`

Audit date 2026-09-01. Scope: the older public-benchmark spectroscopy experiment behind the claims listed in the task specification, and the current state of the research directory it lives in. Method: the directory (17 MB, code + `data/*.mat` + `results/`) was copied to a scratch location and re-run with the project interpreter (`~/telo/.venv`, Python 3.12.13, numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0); an independent code review read every script; nothing under `~/telo` was modified. Full agent reports are summarized here; numbers are quoted from result files or re-run stdout.

## 1. Verdict

The stored tablet result reproduces bit-for-bit, every claimed number traces to a result key, and there is no test-data leakage in the tablet script. The evidence supports exactly what the protocol says it supports: a conventional calibration collapses under instrument shift and a conservative conformal layer detects it and abstains. It does not support automated release, useful operational coverage, or anything about the target drug chemistry. Three things weaken even the narrow claim: the conditional-coverage number rests on 23 of 200 seeds, no confidence intervals exist anywhere, and the public website carries a mis-release figure ("near 3%") that matches no stored result.

## 2. Reproduction

| Script | Runtime | Output | Match to stored |
|---|---|---|---|
| `experiment_tablet.py` (200 seeds) | 2.75 s | `results/tablet_summary.json` | byte-identical (MD5 877efdd8...) and identical to the version committed at 4645879 (2026-07-17) |
| `experiment.py` (corn, 300 seeds) | 19.3 s | `results/summary.json` | byte-identical (MD5 597f8dfc...) |
| `validate_core.py` | 7.8 s | 16 checks | all pass; RRCM closed form vs brute force gap 1.57e-3; MAPIE cross-check coverage 0.900 both |

Dataset: `data/tablet.mat` (IDRC 2002 NIR shootout, MATLAB file created 2004-06-02). Contents 155 calibration + 460 test + 40 validation tablets = 655; the experiment uses 615 (the 40-tablet file is unused); public text says 654 (Eigenvector's page count). Test tablets are the same 460 physical tablets measured on two instruments. The official calibration/test split is not exchangeable (KS D = 0.256, p = 3.4e-7; calibration assay sd 21.98 mg vs test 15.76 mg), which the repository documents and which makes measured coverage run conservative.

## 3. Claim traceability

| Claim (task statement) | Result key | Stored / re-run | Status |
|---|---|---|---|
| 654 tablets, two spectrometers | dataset description | 655 shipped, 615 used | partial: say 615 (155 + 460) |
| Trained on one instrument | PLS fit on `cal1[tr]` | yes | supported |
| R2 ~0.88 -> ~0.05 | `instruments.home.r2`, `instruments.shift.r2` | 0.8772 / 0.0463 | supported; shift R2 is a mean of a wildly dispersed quantity (per-seed range -4.62 to 0.855; bootstrap 95% CI [-0.10, 0.18]) |
| Coverage ~91% -> ~42% | `naive_coverage` | 0.9142 / 0.4159 (CI [0.371, 0.460]) | supported |
| Wrong-certificate exposure ~58% | `shift.misrelease_naive` = 1 - coverage | 0.5841 | supported as unconditional interval-miss rate over 92,000 tablet-evaluations |
| Gated exposure ~1% | `shift.misrelease_gated` | 0.00739 | approximately: 0.74%; the script's console prints 0.01; current README says 0.7% |
| Abstains on ~98.9% | 1 - `shift.release_rate` | release rate 0.01097 | supported; 177 of 200 seeds released zero tablets |
| Conditional coverage ~32.6% | `shift.coverage_on_released` | 0.3260 | supported with caveat: mean over the 23 seeds that released anything; pooled 308 / 1,009 = 0.305; one seed contributed 304 of the 1,009 releases; bootstrap CI [0.17, 0.50] |

Denominators (shift instrument, 460 tablets x 200 seeds = 92,000): naive covered 38,266; released 1,009; released and covered 308; recal covered 82,274. No confidence intervals are computed by any script; the intervals above were computed by the audit (5,000 bootstrap resamples over seeds).

## 4. Design review of `experiment_tablet.py`

- Split: per seed, permute the 155 official calibration tablets into 105 train / 50 conformal-calibration; evaluate on the fixed 460 official test tablets on instrument 1 (home) and instrument 2 (shift). Grouped by instrument: yes. Grouped by lot or time: not possible; the file carries no lot, batch, operator, or timestamp metadata.
- Leakage: SNV is row-wise; PLS, the 1-NN novelty model, and the conformal quantile are fit on instrument-1 calibration tablets only; the shifted test set never touches training; the recalibration arm uses the 50 conformal-calibration tablets re-measured on instrument 2 with their labels, never test tablets.
- Hyperparameter: `N_PLS = 8` is hard-coded with the comment "chosen by held-out R2 on instrument 1 (R2~0.90)"; the selection code is absent. An audit sweep finds the argmax is 4 under both the official test set (R2 0.907) and a 50-tablet calibration hold-out (0.956); 8 gives 0.878 / 0.935. This does not inflate the result (a better N_PLS raises home R2), but the stated selection rule is not reproducible.
- Seeds: `np.random.default_rng(seed)` for seeds 0..199; the tablet script is bitwise reproducible. Elsewhere, PCA and MAPIE objects without `random_state` make some later experiments reproducible only to tolerance.
- Metric semantics: "mis-release" in this script is an interval-miss rate (1 - coverage), not an out-of-specification release rate. The two are different quantities; later scripts (`experiment_risk.py`) make that distinction their thesis, while the README's tablet table and the website use the interval-miss rate under the name "mis-release exposure".

## 5. Current state of the research directory

- Working tree: `README.md`, `conformal_core.py`, `data_tablet.py`, `validate_core.py`, `artifact/release-layer.html` modified and uncommitted; 17 experiment scripts and 14 result JSONs untracked; last commit touching the directory is 4645879 (2026-07-17). Results carry no version or hash.
- The current README (707 lines) does not retract the tablet drift numbers; it restates them at one more decimal and adds that the gate "drives mis-release down by withdrawing volume, not by improving what it still ships". It retracts the earlier release-yield headline ("89% at a verified >= 90%" -> "86.9% at a proved 90%" via full-conformal ridge) and records twenty-two further corrections (RCPS bound, deployed-model certificate, comparator budgets, MSC leakage in the bake-off, reference-noise argument, oracle bound, exchangeability).
- Code review concerns ranked major: (M1) headline coverage reported on the non-exchangeable official split (random re-split drops RRCM coverage 95.0% -> 90.5%); (M2) "exact 90%" labels are conditional on hyperparameters selected from the same 155 labels, and the caveat is applied only to RRCM; (M3) three error-rate definitions share names; (M4) no uncertainty on any headline number; (M5) README prose stale relative to JSONs in five places; (M6) the "two sites" are the same tablets on two instruments; (M7) one shift type only, no sensor-fault, drift, or label-noise tests, no model card.
- Public surfaces: `telo-web/src/data/research.js` stores `shiftGated: 3` (percent) and the research page says the layer holds mis-release "near 3%"; the stored value is 0.74%. The origin of 3% is undetermined (corn gated rates are 4.4% and 3.5%). The site also states every hyperparameter is selected by cross-validation on calibration data alone, which is not true of `N_PLS` in the tablet script.

## 6. Gap against the protocol's required benchmark (section 9.3)

| Requirement | Status | Evidence |
|---|---|---|
| Grouped external validation by instrument | exists | tablet and corn instrument swaps |
| by site / lot / time | missing | no metadata in either public dataset; "two sites" are two instruments |
| Calibration-transfer baselines (DS, PDS, SST, SBC, EPO) | exists | `calibration_transfer.py`, `experiment_transfer.py` |
| Standardization / domain adaptation (di-PLS, GCT-PLS) | exists | `experiment_dipls.py` |
| Conformal baselines (MAPIE, crepes) | exists | `benchmark_release.py` |
| Mandatory-hold baseline | exists as a trivial row | coverage 1.0, yield 0; no time or cost model |
| Risk-coverage curve | partial | `experiment_operating.py`, split configuration only; error axis is coverage miss, not OOS release |
| Operational cost-coverage curve | exists | recal cost vs n; reference tablets needed |
| Unknown-shift stress tests (wavelength shift, baseline drift, gain, gradual drift) | missing | |
| Sensor faults, missing metadata, label-noise injection | missing | observational gross-residual analysis only |
| Repair with small verified assay sets | exists | n = 9 restores 90.1% coverage at 48.3 mg width |
| Bootstrap / repeated-trial uncertainty on headline rows | partial | RMSE CIs in the bake-off only |
| Model card and claims table | missing | README section 8 is the nearest analogue |
| Version pinning of results | partial | `uv.lock` pins libraries; JSONs untracked, unhashed |

## 7. Consequences for the feasibility study

1. The release-assurance submodel starts at R0 for every strategy. R3 stays disabled; its gate G15 is UNCERTAIN.
2. Where an R2 (shadow) or R3 parameterization is needed for scenario analysis, the released fraction (0.011), conditional coverage (0.305-0.326), and false-hold behavior come from `tablet_summary.json` with the manifest recorded, tagged tier 5 for the target chemistry, and reported with the intervals above.
3. A near-total-abstention layer produces no release-time benefit in the simulation by construction (fallback testing applies to every abstained batch). The task's requirement that such a system "show little or no operational release-time benefit even if its unconditional wrong-release exposure is low" is a test, not a hope.
4. The separate benchmark package (phase 4 of the plan) must add: grouped splits with synthetic lot/time structure where real metadata does not exist and an explicit statement that it is synthetic; stress tests (wavelength shift, baseline drift, gain, gradual drift, sensor faults, label noise); bootstrap intervals on every headline row; one error-rate vocabulary; a model card; results pinned to a commit and hash.
5. Public text should be corrected: 615 not 654; 0.7% not 3%; "interval-miss rate" not "mis-release"; hyperparameter-selection statement qualified. These are recorded in `CLAIMS_REGISTER.csv` (C001-C007) for the author to act on; this study does not edit `telo-web`.
