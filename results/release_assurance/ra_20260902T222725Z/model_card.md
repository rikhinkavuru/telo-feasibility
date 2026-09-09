# Model card: conservative release gate on public NIR tablet spectra

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

## Intended use
Research evidence that a conventional PLS calibration fails under instrument shift and that a conformal novelty gate can detect the shift and decline to certify. Not for batch release, not evidence on any sterile injectable, not a validated method.

## Data
IDRC 2002 NIR tablet shootout (frozen as source S28, sha256 129a32ec9e19...): 155 calibration and 460 test tablets measured on two instruments; assay (mg) as reference. No lot, time, operator, or site metadata exist; synthetic groups are index blocks.

## Method
SNV, PLS with a fixed 8 components (repository reproduction mode) without per-wavelength standardization (scale=False) on a 105-tablet training partition, split-conformal interval at alpha = 0.1 on the remaining calibration tablets, 1-NN novelty gate with conformal p-value threshold 0.1; 50 random partitions; bootstrap 95% intervals over partitions.

## Metrics that travel together (test instrument = shift)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| released_fraction | 0.915 [0.905, 0.926] (seeds 50) | 0.303 [0.260, 0.347] (seeds 50) |
| abstention_fraction | 0.085 [0.075, 0.095] (seeds 50) | 0.697 [0.651, 0.737] (seeds 50) |
| unconditional_wrong_release | 0.074 [0.065, 0.085] (seeds 50) | 0.046 [0.036, 0.055] (seeds 50) |
| conditional_error_among_released | 0.081 [0.071, 0.092] (seeds 50) | 0.160 [0.137, 0.185] (seeds 50) |
| empirical_coverage | 0.903 [0.890, 0.914] (seeds 50) | 0.768 [0.733, 0.799] (seeds 50) |
| false_hold_rate | 0.069 [0.061, 0.078] (seeds 50) | 0.669 [0.622, 0.712] (seeds 50) |
| r2 | 0.859 [0.853, 0.864] (seeds 50) | 0.735 [0.702, 0.763] (seeds 50) |

Pooled shifted-instrument counts: released 6971 of 23000 tablet-evaluations.

## Risk-coverage curve (shifted instrument, gate threshold sweep)

| threshold | released | conditional error | unconditional exposure | operational cost (relative) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.232 | 0.232 | 11.602 |
| 0.01 | 1.000 | 0.232 | 0.232 | 11.602 |
| 0.02 | 0.818 | 0.210 | 0.174 | 8.865 |
| 0.05 | 0.597 | 0.188 | 0.112 | 5.988 |
| 0.1 | 0.303 | 0.160 | 0.046 | 2.977 |
| 0.2 | 0.124 | 0.154 | 0.018 | 1.774 |
| 0.3 | 0.063 | 0.143 | 0.009 | 1.389 |
| 0.5 | 0.014 | 0.096 | 0.002 | 1.080 |

## Baselines and repair (shifted instrument, no gate)

| Configuration | empirical coverage | unconditional wrong release |
|---|---|---|
| shift_ds_n15 | 0.857 [0.838, 0.876] (seeds 50) | 0.143 [0.124, 0.162] (seeds 50) |
| shift_ds_n30 | 0.831 [0.814, 0.849] (seeds 50) | 0.169 [0.152, 0.186] (seeds 50) |
| shift_ds_n50 | 0.768 [0.744, 0.790] (seeds 50) | 0.232 [0.210, 0.255] (seeds 50) |
| shift_instrument_std_n15 | 0.829 [0.812, 0.844] (seeds 50) | 0.171 [0.156, 0.189] (seeds 50) |
| shift_instrument_std_n30 | 0.853 [0.840, 0.864] (seeds 50) | 0.147 [0.136, 0.159] (seeds 50) |
| shift_instrument_std_n50 | 0.864 [0.852, 0.874] (seeds 50) | 0.136 [0.126, 0.147] (seeds 50) |
| shift_mandatory_hold | 0.768 [0.734, 0.798] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.839 [0.825, 0.852] (seeds 50) | 0.161 [0.147, 0.175] (seeds 50) |
| shift_no_gate | 0.768 [0.735, 0.799] (seeds 50) | 0.232 [0.203, 0.267] (seeds 50) |
| shift_pds_n15 | 0.706 [0.669, 0.741] (seeds 50) | 0.294 [0.261, 0.331] (seeds 50) |
| shift_pds_n30 | 0.900 [0.888, 0.911] (seeds 50) | 0.100 [0.089, 0.112] (seeds 50) |
| shift_pds_n50 | 0.929 [0.919, 0.937] (seeds 50) | 0.071 [0.062, 0.080] (seeds 50) |
| shift_repaired_quantile_n15 | 0.923 [0.902, 0.942] (seeds 50) | 0.077 [0.057, 0.098] (seeds 50) |
| shift_repaired_quantile_n3 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n30 | 0.909 [0.897, 0.922] (seeds 50) | 0.091 [0.079, 0.102] (seeds 50) |
| shift_repaired_quantile_n5 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n50 | 0.910 [0.902, 0.918] (seeds 50) | 0.090 [0.081, 0.098] (seeds 50) |
| shift_repaired_quantile_n9 | 0.913 [0.889, 0.934] (seeds 50) | 0.087 [0.064, 0.111] (seeds 50) |
| shift_slope_bias_n15 | 0.817 [0.801, 0.832] (seeds 50) | 0.183 [0.167, 0.199] (seeds 50) |
| shift_slope_bias_n30 | 0.831 [0.816, 0.846] (seeds 50) | 0.169 [0.155, 0.185] (seeds 50) |
| shift_slope_bias_n5 | 0.772 [0.750, 0.793] (seeds 50) | 0.228 [0.206, 0.249] (seeds 50) |
| shift_slope_bias_n50 | 0.835 [0.821, 0.848] (seeds 50) | 0.165 [0.151, 0.178] (seeds 50) |
| shift_slope_bias_n9 | 0.805 [0.785, 0.824] (seeds 50) | 0.195 [0.177, 0.216] (seeds 50) |

## Stress tests (home spectra with synthetic faults)

| Fault | released fraction | unconditional wrong release |
|---|---|---|
| home_label_noise_5mg | 0.914 [0.905, 0.922] (seeds 50) | 0.030 [0.025, 0.035] (seeds 50) |
| stress_baseline_offset | 0.915 [0.905, 0.926] (seeds 50) | 0.074 [0.064, 0.084] (seeds 50) |
| stress_baseline_slope | 0.369 [0.320, 0.421] (seeds 50) | 0.053 [0.038, 0.070] (seeds 50) |
| stress_dead_channels | 0.006 [0.000, 0.015] (seeds 50) | 0.004 [0.000, 0.012] (seeds 50) |
| stress_gain | 0.915 [0.904, 0.924] (seeds 50) | 0.074 [0.065, 0.085] (seeds 50) |
| stress_gradual_drift | 0.915 [0.904, 0.925] (seeds 50) | 0.074 [0.064, 0.084] (seeds 50) |
| stress_noise | 0.279 [0.235, 0.325] (seeds 50) | 0.132 [0.111, 0.154] (seeds 50) |
| stress_spikes | 0.674 [0.641, 0.705] (seeds 50) | 0.255 [0.234, 0.277] (seeds 50) |
| stress_wavelength_shift | 0.428 [0.393, 0.463] (seeds 50) | 0.427 [0.392, 0.461] (seeds 50) |

## Selective prediction (gate confidence = conformal p-value; error = interval miss)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| aurc | 0.068 [0.059, 0.078] (seeds 50) | 0.185 [0.159, 0.213] (seeds 50) |
| e_aurc | 0.062 [0.054, 0.070] (seeds 50) | 0.146 [0.129, 0.163] (seeds 50) |
| aurc_oracle | 0.006 [0.005, 0.008] (seeds 50) | 0.039 [0.027, 0.054] (seeds 50) |

## Held-out shift-type protocol (threshold tuned for 90% detection on the row family; cells = released fraction on the column family)

| tuned on | threshold | home abstention | wavelength_shift | baseline_offset | baseline_slope | gain | noise | spikes | dead_channels | gradual_drift | instrument |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wavelength_shift | 0.37 | 0.31 | 0.08 | 0.69 | 0.05 | 0.69 | 0.05 | 0.27 | 0.01 | 0.69 | 0.04 |
| baseline_offset | 0.50 | 0.45 | 0.04 | 0.55 | 0.02 | 0.55 | 0.02 | 0.16 | 0.01 | 0.55 | 0.01 |
| baseline_slope | 0.28 | 0.23 | 0.17 | 0.77 | 0.08 | 0.77 | 0.09 | 0.38 | 0.01 | 0.77 | 0.09 |
| gain | 0.50 | 0.45 | 0.04 | 0.55 | 0.02 | 0.55 | 0.02 | 0.16 | 0.01 | 0.55 | 0.01 |
| noise | 0.25 | 0.20 | 0.20 | 0.80 | 0.12 | 0.80 | 0.08 | 0.43 | 0.01 | 0.80 | 0.10 |
| spikes | 0.48 | 0.43 | 0.05 | 0.57 | 0.02 | 0.57 | 0.02 | 0.17 | 0.01 | 0.57 | 0.02 |
| dead_channels | 0.04 | 0.03 | 0.72 | 0.97 | 0.73 | 0.97 | 0.61 | 0.87 | 0.02 | 0.97 | 0.68 |
| gradual_drift | 0.50 | 0.45 | 0.04 | 0.55 | 0.02 | 0.55 | 0.02 | 0.16 | 0.01 | 0.55 | 0.01 |
| instrument | 0.23 | 0.19 | 0.21 | 0.81 | 0.14 | 0.81 | 0.11 | 0.43 | 0.01 | 0.81 | 0.08 |

In-family released 0.24; out-of-family released 0.34 (worst 0.97).

## Operational cost curves in USD (illustrative cost inputs)

False hold 30,082 USD (testing 30,000 + 82 delay carrying on a 30,000 USD batch); with investigation 50,082; wrong release 2,000,000 (tier 5); implied ratio 66.5 vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.

### home instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.097 | 194,522 | 194,522 | 309,293 |
| 0.01 | 0.000 | 0.097 | 194,522 | 194,522 | 309,293 |
| 0.02 | 0.011 | 0.092 | 185,112 | 185,331 | 322,027 |
| 0.05 | 0.032 | 0.086 | 172,175 | 172,811 | 340,208 |
| 0.1 | 0.085 | 0.074 | 150,815 | 152,513 | 371,342 |
| 0.2 | 0.158 | 0.063 | 131,375 | 134,543 | 399,911 |
| 0.3 | 0.239 | 0.055 | 117,018 | 121,800 | 416,839 |
| 0.5 | 0.451 | 0.037 | 86,597 | 95,609 | 452,557 |

### shifted instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.232 | 464,087 | 464,087 | 129,640 |
| 0.01 | 0.000 | 0.232 | 464,087 | 464,087 | 129,640 |
| 0.02 | 0.182 | 0.174 | 352,777 | 356,415 | 141,719 |
| 0.05 | 0.403 | 0.112 | 235,514 | 243,574 | 160,785 |
| 0.1 | 0.697 | 0.046 | 112,182 | 126,120 | 199,907 |
| 0.2 | 0.876 | 0.018 | 62,258 | 79,774 | 208,098 |
| 0.3 | 0.937 | 0.009 | 46,267 | 65,003 | 210,286 |
| 0.5 | 0.986 | 0.002 | 33,408 | 53,133 | 221,069 |

## Limitations

- Instrument is the only real group; lot and time groups are SYNTHETIC index blocks and test nothing about real lots or time.
- Wrong release here means the certified interval missed the reference assay; it is not an out-of-specification release rate.
- Repair curves reuse calibration tablets re-measured on the shifted instrument; they never touch the test set.
- PLS components are chosen by 5-fold CV on the training partition of each seed (the repository's fixed N_PLS=8 is not reproduced).
- No Telo data, no target chemistry, no prospective validation; this supports stop-the-line detection claims only.
- Gate statistic: nn; component selection: train_cv.
- AURC and E-AURC (selective prediction) use the conformal p-value as confidence and an interval miss as the error; ties broken in expectation.
- Held-out shift-type matrix: threshold tuned to reach the detection target on one family, evaluated on every other; synthetic families are generated from a separate stream.
- Operational cost curve in USD uses the study's parameter sets (tier 5 illustrative) instead of the relative 1:50 weights; the wrong-release cost is a placeholder until a recall-cost source exists.

## Claims table

| Claim | Allowed |
|---|---|
| Detects this instrument shift and abstains | yes, as measured above |
| Automates batch release | no |
| Useful operational coverage under shift | no (see released fraction on the shifted instrument) |
| Evidence on the target drug chemistry | no |
| Prospective product/site validation | no |
| Replaces sterility assurance or any mandatory test | no |
