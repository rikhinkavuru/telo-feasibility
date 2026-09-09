# Model card: conservative release gate on public NIR tablet spectra

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

## Intended use
Research evidence that a conventional PLS calibration fails under instrument shift and that a conformal novelty gate can detect the shift and decline to certify. Not for batch release, not evidence on any sterile injectable, not a validated method.

## Data
IDRC 2002 NIR tablet shootout (frozen as source S28, sha256 129a32ec9e19...): 155 calibration and 460 test tablets measured on two instruments; assay (mg) as reference. No lot, time, operator, or site metadata exist; synthetic groups are index blocks.

## Method
SNV, PLS with 5-fold-CV-selected components without per-wavelength standardization (scale=False) on a 105-tablet training partition, split-conformal interval at alpha = 0.1 on the remaining calibration tablets, 1-NN novelty gate with conformal p-value threshold 0.1; 50 random partitions; bootstrap 95% intervals over partitions.

## Metrics that travel together (test instrument = shift)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| released_fraction | 0.919 [0.910, 0.927] (seeds 50) | 0.561 [0.523, 0.602] (seeds 50) |
| abstention_fraction | 0.081 [0.073, 0.090] (seeds 50) | 0.439 [0.398, 0.477] (seeds 50) |
| unconditional_wrong_release | 0.061 [0.054, 0.070] (seeds 50) | 0.155 [0.137, 0.172] (seeds 50) |
| conditional_error_among_released | 0.067 [0.059, 0.076] (seeds 50) | 0.290 [0.256, 0.327] (seeds 50) |
| empirical_coverage | 0.928 [0.916, 0.939] (seeds 50) | 0.717 [0.685, 0.746] (seeds 50) |
| false_hold_rate | 0.076 [0.069, 0.083] (seeds 50) | 0.441 [0.393, 0.486] (seeds 50) |
| r2 | 0.908 [0.906, 0.910] (seeds 50) | 0.774 [0.760, 0.788] (seeds 50) |

Pooled shifted-instrument counts: released 12906 of 23000 tablet-evaluations.

## Risk-coverage curve (shifted instrument, gate threshold sweep)

| threshold | released | conditional error | unconditional exposure | operational cost (relative) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.283 | 0.283 | 14.170 |
| 0.01 | 1.000 | 0.283 | 0.283 | 14.170 |
| 0.02 | 0.901 | 0.279 | 0.252 | 12.703 |
| 0.05 | 0.753 | 0.280 | 0.211 | 10.797 |
| 0.1 | 0.561 | 0.290 | 0.155 | 8.204 |
| 0.2 | 0.405 | 0.310 | 0.119 | 6.521 |
| 0.3 | 0.291 | 0.332 | 0.091 | 5.274 |
| 0.5 | 0.123 | 0.351 | 0.040 | 2.898 |

## Baselines and repair (shifted instrument, no gate)

| Configuration | empirical coverage | unconditional wrong release |
|---|---|---|
| shift_ds_n15 | 0.845 [0.825, 0.866] (seeds 50) | 0.155 [0.135, 0.176] (seeds 50) |
| shift_ds_n30 | 0.852 [0.837, 0.866] (seeds 50) | 0.148 [0.134, 0.163] (seeds 50) |
| shift_ds_n50 | 0.826 [0.807, 0.844] (seeds 50) | 0.174 [0.156, 0.192] (seeds 50) |
| shift_instrument_std_n15 | 0.864 [0.850, 0.878] (seeds 50) | 0.136 [0.123, 0.151] (seeds 50) |
| shift_instrument_std_n30 | 0.877 [0.869, 0.885] (seeds 50) | 0.123 [0.115, 0.131] (seeds 50) |
| shift_instrument_std_n50 | 0.880 [0.873, 0.887] (seeds 50) | 0.120 [0.113, 0.127] (seeds 50) |
| shift_mandatory_hold | 0.717 [0.685, 0.746] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.861 [0.853, 0.870] (seeds 50) | 0.139 [0.130, 0.147] (seeds 50) |
| shift_no_gate | 0.717 [0.686, 0.746] (seeds 50) | 0.283 [0.256, 0.315] (seeds 50) |
| shift_pds_n15 | 0.827 [0.812, 0.845] (seeds 50) | 0.173 [0.154, 0.189] (seeds 50) |
| shift_pds_n30 | 0.894 [0.885, 0.903] (seeds 50) | 0.106 [0.097, 0.115] (seeds 50) |
| shift_pds_n50 | 0.897 [0.889, 0.904] (seeds 50) | 0.103 [0.095, 0.111] (seeds 50) |
| shift_repaired_quantile_n15 | 0.927 [0.910, 0.944] (seeds 50) | 0.073 [0.055, 0.091] (seeds 50) |
| shift_repaired_quantile_n3 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n30 | 0.866 [0.854, 0.877] (seeds 50) | 0.134 [0.122, 0.147] (seeds 50) |
| shift_repaired_quantile_n5 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n50 | 0.869 [0.862, 0.875] (seeds 50) | 0.131 [0.125, 0.138] (seeds 50) |
| shift_repaired_quantile_n9 | 0.894 [0.867, 0.919] (seeds 50) | 0.106 [0.083, 0.134] (seeds 50) |
| shift_slope_bias_n15 | 0.863 [0.855, 0.871] (seeds 50) | 0.137 [0.129, 0.145] (seeds 50) |
| shift_slope_bias_n30 | 0.865 [0.859, 0.873] (seeds 50) | 0.135 [0.127, 0.142] (seeds 50) |
| shift_slope_bias_n5 | 0.844 [0.825, 0.858] (seeds 50) | 0.156 [0.142, 0.173] (seeds 50) |
| shift_slope_bias_n50 | 0.864 [0.857, 0.872] (seeds 50) | 0.136 [0.128, 0.143] (seeds 50) |
| shift_slope_bias_n9 | 0.856 [0.847, 0.867] (seeds 50) | 0.144 [0.134, 0.155] (seeds 50) |

## Stress tests (home spectra with synthetic faults)

| Fault | released fraction | unconditional wrong release |
|---|---|---|
| home_label_noise_5mg | 0.922 [0.915, 0.929] (seeds 50) | 0.019 [0.017, 0.021] (seeds 50) |
| stress_baseline_offset | 0.919 [0.910, 0.928] (seeds 50) | 0.061 [0.053, 0.070] (seeds 50) |
| stress_baseline_slope | 0.507 [0.476, 0.541] (seeds 50) | 0.068 [0.061, 0.076] (seeds 50) |
| stress_dead_channels | 0.349 [0.249, 0.448] (seeds 50) | 0.233 [0.159, 0.311] (seeds 50) |
| stress_gain | 0.919 [0.910, 0.927] (seeds 50) | 0.061 [0.054, 0.070] (seeds 50) |
| stress_gradual_drift | 0.919 [0.910, 0.926] (seeds 50) | 0.061 [0.053, 0.070] (seeds 50) |
| stress_noise | 0.727 [0.683, 0.765] (seeds 50) | 0.370 [0.346, 0.394] (seeds 50) |
| stress_spikes | 0.858 [0.840, 0.876] (seeds 50) | 0.327 [0.311, 0.344] (seeds 50) |
| stress_wavelength_shift | 0.495 [0.471, 0.520] (seeds 50) | 0.494 [0.469, 0.519] (seeds 50) |

## Selective prediction (gate confidence = conformal p-value; error = interval miss)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| aurc | 0.066 [0.058, 0.074] (seeds 50) | 0.303 [0.266, 0.343] (seeds 50) |
| e_aurc | 0.062 [0.055, 0.068] (seeds 50) | 0.249 [0.224, 0.274] (seeds 50) |
| aurc_oracle | 0.004 [0.003, 0.005] (seeds 50) | 0.054 [0.042, 0.068] (seeds 50) |

## Held-out shift-type protocol (threshold tuned for 90% detection on the row family; cells = released fraction on the column family)

| tuned on | threshold | home abstention | wavelength_shift | baseline_offset | baseline_slope | gain | noise | spikes | dead_channels | gradual_drift | instrument |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wavelength_shift | 0.47 | 0.47 | 0.12 | 0.53 | 0.09 | 0.53 | 0.20 | 0.33 | 0.07 | 0.53 | 0.13 |
| baseline_offset | 0.50 | 0.49 | 0.11 | 0.51 | 0.08 | 0.51 | 0.19 | 0.31 | 0.06 | 0.51 | 0.12 |
| baseline_slope | 0.45 | 0.44 | 0.14 | 0.56 | 0.10 | 0.56 | 0.22 | 0.37 | 0.07 | 0.56 | 0.15 |
| gain | 0.50 | 0.49 | 0.11 | 0.51 | 0.08 | 0.51 | 0.19 | 0.31 | 0.06 | 0.51 | 0.12 |
| noise | 0.49 | 0.48 | 0.12 | 0.52 | 0.09 | 0.52 | 0.19 | 0.33 | 0.06 | 0.52 | 0.13 |
| spikes | 0.50 | 0.49 | 0.11 | 0.51 | 0.08 | 0.51 | 0.19 | 0.31 | 0.06 | 0.51 | 0.12 |
| dead_channels | 0.23 | 0.22 | 0.39 | 0.78 | 0.40 | 0.78 | 0.57 | 0.69 | 0.10 | 0.78 | 0.46 |
| gradual_drift | 0.50 | 0.49 | 0.11 | 0.51 | 0.08 | 0.51 | 0.19 | 0.31 | 0.06 | 0.51 | 0.12 |
| instrument | 0.48 | 0.47 | 0.12 | 0.53 | 0.09 | 0.53 | 0.20 | 0.33 | 0.07 | 0.53 | 0.13 |

In-family released 0.27; out-of-family released 0.31 (worst 0.78).

## Operational cost curves in USD (illustrative cost inputs)

False hold 30,082 USD (testing 30,000 + 82 delay carrying on a 30,000 USD batch); with investigation 50,082; wrong release 2,000,000 (tier 5); implied ratio 66.5 vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.

### home instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.072 | 144,957 | 144,957 | 415,050 |
| 0.01 | 0.000 | 0.072 | 144,957 | 144,957 | 415,050 |
| 0.02 | 0.012 | 0.070 | 140,012 | 140,251 | 425,664 |
| 0.05 | 0.038 | 0.066 | 132,957 | 133,710 | 439,227 |
| 0.1 | 0.081 | 0.061 | 125,230 | 126,857 | 450,145 |
| 0.2 | 0.144 | 0.056 | 115,543 | 118,418 | 463,180 |
| 0.3 | 0.231 | 0.047 | 101,297 | 105,917 | 490,380 |
| 0.5 | 0.495 | 0.029 | 73,581 | 83,478 | 517,814 |

### shifted instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.283 | 566,783 | 566,783 | 106,151 |
| 0.01 | 0.000 | 0.283 | 566,783 | 566,783 | 106,151 |
| 0.02 | 0.099 | 0.252 | 507,155 | 509,136 | 107,508 |
| 0.05 | 0.247 | 0.211 | 429,432 | 434,372 | 107,349 |
| 0.1 | 0.439 | 0.155 | 323,811 | 332,588 | 108,690 |
| 0.2 | 0.595 | 0.119 | 254,948 | 266,851 | 102,749 |
| 0.3 | 0.709 | 0.091 | 203,941 | 218,123 | 95,833 |
| 0.5 | 0.877 | 0.040 | 107,239 | 124,770 | 91,831 |

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
