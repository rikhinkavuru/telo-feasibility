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
| released_fraction | 0.919 [0.910, 0.927] (seeds 50) | 0.563 [0.525, 0.602] (seeds 50) |
| abstention_fraction | 0.081 [0.073, 0.090] (seeds 50) | 0.437 [0.397, 0.476] (seeds 50) |
| unconditional_wrong_release | 0.061 [0.054, 0.069] (seeds 50) | 0.152 [0.135, 0.169] (seeds 50) |
| conditional_error_among_released | 0.067 [0.059, 0.076] (seeds 50) | 0.284 [0.253, 0.319] (seeds 50) |
| empirical_coverage | 0.927 [0.916, 0.938] (seeds 50) | 0.722 [0.695, 0.748] (seeds 50) |
| false_hold_rate | 0.075 [0.069, 0.081] (seeds 50) | 0.438 [0.391, 0.484] (seeds 50) |
| r2 | 0.907 [0.905, 0.909] (seeds 50) | 0.774 [0.760, 0.788] (seeds 50) |

Pooled shifted-instrument counts: released 12953 of 23000 tablet-evaluations.

## Risk-coverage curve (shifted instrument, gate threshold sweep)

| threshold | released | conditional error | unconditional exposure | operational cost (relative) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.278 | 0.278 | 13.893 |
| 0.01 | 1.000 | 0.278 | 0.278 | 13.893 |
| 0.02 | 0.901 | 0.273 | 0.247 | 12.468 |
| 0.05 | 0.757 | 0.274 | 0.208 | 10.639 |
| 0.1 | 0.563 | 0.284 | 0.152 | 8.054 |
| 0.2 | 0.410 | 0.305 | 0.117 | 6.459 |
| 0.3 | 0.290 | 0.326 | 0.088 | 5.101 |
| 0.5 | 0.122 | 0.349 | 0.039 | 2.826 |

## Baselines and repair (shifted instrument, no gate)

| Configuration | empirical coverage | unconditional wrong release |
|---|---|---|
| shift_ds_n15 | 0.847 [0.826, 0.867] (seeds 50) | 0.153 [0.134, 0.173] (seeds 50) |
| shift_ds_n30 | 0.848 [0.833, 0.862] (seeds 50) | 0.152 [0.138, 0.167] (seeds 50) |
| shift_ds_n50 | 0.823 [0.804, 0.841] (seeds 50) | 0.177 [0.159, 0.197] (seeds 50) |
| shift_instrument_std_n15 | 0.865 [0.850, 0.878] (seeds 50) | 0.135 [0.122, 0.149] (seeds 50) |
| shift_instrument_std_n30 | 0.877 [0.869, 0.884] (seeds 50) | 0.123 [0.115, 0.131] (seeds 50) |
| shift_instrument_std_n50 | 0.879 [0.871, 0.887] (seeds 50) | 0.121 [0.113, 0.128] (seeds 50) |
| shift_mandatory_hold | 0.722 [0.695, 0.748] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.860 [0.852, 0.870] (seeds 50) | 0.140 [0.130, 0.149] (seeds 50) |
| shift_no_gate | 0.722 [0.696, 0.748] (seeds 50) | 0.278 [0.252, 0.305] (seeds 50) |
| shift_pds_n15 | 0.830 [0.814, 0.848] (seeds 50) | 0.170 [0.153, 0.186] (seeds 50) |
| shift_pds_n30 | 0.892 [0.883, 0.901] (seeds 50) | 0.108 [0.098, 0.117] (seeds 50) |
| shift_pds_n50 | 0.896 [0.888, 0.903] (seeds 50) | 0.104 [0.097, 0.112] (seeds 50) |
| shift_repaired_quantile_n15 | 0.928 [0.910, 0.945] (seeds 50) | 0.072 [0.055, 0.091] (seeds 50) |
| shift_repaired_quantile_n3 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n30 | 0.867 [0.856, 0.877] (seeds 50) | 0.133 [0.122, 0.145] (seeds 50) |
| shift_repaired_quantile_n5 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n50 | 0.869 [0.862, 0.876] (seeds 50) | 0.131 [0.124, 0.137] (seeds 50) |
| shift_repaired_quantile_n9 | 0.896 [0.870, 0.919] (seeds 50) | 0.104 [0.081, 0.129] (seeds 50) |
| shift_slope_bias_n15 | 0.861 [0.853, 0.870] (seeds 50) | 0.139 [0.131, 0.147] (seeds 50) |
| shift_slope_bias_n30 | 0.864 [0.857, 0.872] (seeds 50) | 0.136 [0.128, 0.144] (seeds 50) |
| shift_slope_bias_n5 | 0.839 [0.820, 0.855] (seeds 50) | 0.161 [0.146, 0.179] (seeds 50) |
| shift_slope_bias_n50 | 0.863 [0.855, 0.872] (seeds 50) | 0.137 [0.129, 0.144] (seeds 50) |
| shift_slope_bias_n9 | 0.855 [0.845, 0.866] (seeds 50) | 0.145 [0.135, 0.157] (seeds 50) |

## Stress tests (home spectra with synthetic faults)

| Fault | released fraction | unconditional wrong release |
|---|---|---|
| home_label_noise_5mg | 0.920 [0.913, 0.928] (seeds 50) | 0.019 [0.017, 0.021] (seeds 50) |
| stress_baseline_offset | 0.919 [0.911, 0.927] (seeds 50) | 0.061 [0.054, 0.069] (seeds 50) |
| stress_baseline_slope | 0.514 [0.485, 0.543] (seeds 50) | 0.067 [0.059, 0.075] (seeds 50) |
| stress_dead_channels | 0.328 [0.237, 0.421] (seeds 50) | 0.212 [0.146, 0.292] (seeds 50) |
| stress_gain | 0.919 [0.910, 0.926] (seeds 50) | 0.061 [0.054, 0.069] (seeds 50) |
| stress_gradual_drift | 0.919 [0.910, 0.926] (seeds 50) | 0.061 [0.054, 0.069] (seeds 50) |
| stress_noise | 0.724 [0.675, 0.766] (seeds 50) | 0.369 [0.344, 0.394] (seeds 50) |
| stress_spikes | 0.854 [0.833, 0.874] (seeds 50) | 0.325 [0.311, 0.342] (seeds 50) |
| stress_wavelength_shift | 0.495 [0.469, 0.522] (seeds 50) | 0.494 [0.467, 0.520] (seeds 50) |

## Selective prediction (gate confidence = conformal p-value; error = interval miss)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| aurc | 0.066 [0.059, 0.074] (seeds 50) | 0.298 [0.265, 0.334] (seeds 50) |
| e_aurc | 0.062 [0.056, 0.068] (seeds 50) | 0.249 [0.224, 0.273] (seeds 50) |
| aurc_oracle | 0.004 [0.003, 0.005] (seeds 50) | 0.050 [0.040, 0.060] (seeds 50) |

## Held-out shift-type protocol (threshold tuned for 90% detection on the row family; cells = released fraction on the column family)

| tuned on | threshold | home abstention | wavelength_shift | baseline_offset | baseline_slope | gain | noise | spikes | dead_channels | gradual_drift | instrument |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wavelength_shift | 0.47 | 0.47 | 0.12 | 0.53 | 0.09 | 0.53 | 0.19 | 0.33 | 0.07 | 0.53 | 0.13 |
| baseline_offset | 0.50 | 0.50 | 0.11 | 0.50 | 0.08 | 0.50 | 0.18 | 0.31 | 0.06 | 0.50 | 0.12 |
| baseline_slope | 0.46 | 0.45 | 0.13 | 0.55 | 0.10 | 0.55 | 0.21 | 0.35 | 0.07 | 0.55 | 0.14 |
| gain | 0.50 | 0.50 | 0.11 | 0.50 | 0.08 | 0.50 | 0.18 | 0.31 | 0.06 | 0.50 | 0.12 |
| noise | 0.48 | 0.47 | 0.12 | 0.53 | 0.10 | 0.53 | 0.19 | 0.33 | 0.06 | 0.53 | 0.13 |
| spikes | 0.50 | 0.49 | 0.11 | 0.51 | 0.08 | 0.51 | 0.18 | 0.31 | 0.06 | 0.51 | 0.12 |
| dead_channels | 0.24 | 0.23 | 0.37 | 0.77 | 0.38 | 0.77 | 0.54 | 0.67 | 0.10 | 0.77 | 0.43 |
| gradual_drift | 0.50 | 0.50 | 0.11 | 0.50 | 0.08 | 0.50 | 0.18 | 0.31 | 0.06 | 0.50 | 0.12 |
| instrument | 0.48 | 0.48 | 0.12 | 0.52 | 0.09 | 0.52 | 0.19 | 0.32 | 0.07 | 0.52 | 0.13 |

In-family released 0.27; out-of-family released 0.31 (worst 0.77).

## Operational cost curves in USD (illustrative cost inputs)

False hold 30,082 USD (testing 30,000 + 82 delay carrying on a 30,000 USD batch); with investigation 50,082; wrong release 2,000,000 (tier 5); implied ratio 66.5 vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.

### home instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.073 | 146,609 | 146,609 | 410,373 |
| 0.01 | 0.000 | 0.073 | 146,609 | 146,609 | 410,373 |
| 0.02 | 0.012 | 0.070 | 141,325 | 141,571 | 421,595 |
| 0.05 | 0.038 | 0.066 | 133,564 | 134,314 | 437,248 |
| 0.1 | 0.081 | 0.061 | 124,798 | 126,426 | 451,702 |
| 0.2 | 0.142 | 0.056 | 115,503 | 118,353 | 463,886 |
| 0.3 | 0.232 | 0.047 | 101,509 | 106,154 | 488,676 |
| 0.5 | 0.496 | 0.029 | 73,261 | 83,176 | 519,959 |

### shifted instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.278 | 555,739 | 555,739 | 108,260 |
| 0.01 | 0.000 | 0.278 | 555,739 | 555,739 | 108,260 |
| 0.02 | 0.099 | 0.247 | 497,756 | 499,732 | 109,580 |
| 0.05 | 0.243 | 0.208 | 423,137 | 427,998 | 109,521 |
| 0.1 | 0.437 | 0.152 | 317,836 | 326,573 | 111,203 |
| 0.2 | 0.590 | 0.117 | 252,523 | 264,318 | 105,131 |
| 0.3 | 0.710 | 0.088 | 197,010 | 211,210 | 99,331 |
| 0.5 | 0.878 | 0.039 | 104,337 | 121,905 | 93,906 |

## Limitations

- Instrument is the only real group; lot and time groups are SYNTHETIC index blocks and test nothing about real lots or time.
- Wrong release here means the certified interval missed the reference assay; it is not an out-of-specification release rate.
- Repair curves reuse calibration tablets re-measured on the shifted instrument; they never touch the test set.
- PLS components are chosen by 5-fold CV on the training partition of each seed (the repository's fixed N_PLS=8 is not reproduced).
- No Telo data, no target chemistry, no prospective validation; this supports stop-the-line detection claims only.
- Gate statistic: nn; component selection: train_and_calibration_cv.
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
