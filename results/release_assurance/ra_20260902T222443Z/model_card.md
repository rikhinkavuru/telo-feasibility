# Model card: conservative release gate on public NIR tablet spectra

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

## Intended use
Research evidence that a conventional PLS calibration fails under instrument shift and that a conformal novelty gate can detect the shift and decline to certify. Not for batch release, not evidence on any sterile injectable, not a validated method.

## Data
IDRC 2002 NIR tablet shootout (frozen as source S28, sha256 129a32ec9e19...): 155 calibration and 460 test tablets measured on two instruments; assay (mg) as reference. No lot, time, operator, or site metadata exist; synthetic groups are index blocks.

## Method
SNV, PLS with a fixed 8 components (repository reproduction mode) with per-wavelength standardization (scale=True) on a 105-tablet training partition, split-conformal interval at alpha = 0.1 on the remaining calibration tablets, 1-NN novelty gate with conformal p-value threshold 0.1; 50 random partitions; bootstrap 95% intervals over partitions.

## Metrics that travel together (test instrument = shift)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| released_fraction | 0.931 [0.923, 0.939] (seeds 50) | 0.010 [0.001, 0.027] (seeds 50) |
| abstention_fraction | 0.069 [0.062, 0.077] (seeds 50) | 0.990 [0.974, 0.999] (seeds 50) |
| unconditional_wrong_release | 0.071 [0.062, 0.082] (seeds 50) | 0.006 [0.001, 0.014] (seeds 50) |
| conditional_error_among_released | 0.077 [0.066, 0.088] (seeds 50) | 0.609 [0.272, 0.881] (seeds 7) |
| empirical_coverage | 0.909 [0.896, 0.922] (seeds 50) | 0.410 [0.328, 0.493] (seeds 50) |
| false_hold_rate | 0.054 [0.048, 0.061] (seeds 50) | 0.990 [0.973, 1.000] (seeds 50) |
| r2 | 0.876 [0.871, 0.880] (seeds 50) | 0.111 [-0.183, 0.349] (seeds 50) |

Pooled shifted-instrument counts: released 229 of 23000 tablet-evaluations.

## Risk-coverage curve (shifted instrument, gate threshold sweep)

| threshold | released | conditional error | unconditional exposure | operational cost (relative) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.590 | 0.590 | 29.480 |
| 0.01 | 1.000 | 0.590 | 0.590 | 29.480 |
| 0.02 | 0.431 | 0.641 | 0.263 | 13.719 |
| 0.05 | 0.091 | 0.650 | 0.064 | 4.106 |
| 0.1 | 0.010 | 0.609 | 0.006 | 1.279 |
| 0.2 | 0.002 | 0.308 | 0.001 | 1.024 |
| 0.3 | 0.000 | 0.167 | 0.000 | 1.002 |
| 0.5 | 0.000 | nan | 0.000 | 1.000 |

## Baselines and repair (shifted instrument, no gate)

| Configuration | empirical coverage | unconditional wrong release |
|---|---|---|
| shift_ds_n15 | 0.844 [0.819, 0.866] (seeds 50) | 0.156 [0.134, 0.178] (seeds 50) |
| shift_ds_n30 | 0.826 [0.809, 0.844] (seeds 50) | 0.174 [0.157, 0.192] (seeds 50) |
| shift_ds_n50 | 0.777 [0.755, 0.798] (seeds 50) | 0.223 [0.204, 0.245] (seeds 50) |
| shift_instrument_std_n15 | 0.808 [0.791, 0.824] (seeds 50) | 0.192 [0.175, 0.210] (seeds 50) |
| shift_instrument_std_n30 | 0.825 [0.811, 0.838] (seeds 50) | 0.175 [0.162, 0.188] (seeds 50) |
| shift_instrument_std_n50 | 0.831 [0.820, 0.843] (seeds 50) | 0.169 [0.158, 0.181] (seeds 50) |
| shift_mandatory_hold | 0.410 [0.326, 0.494] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.841 [0.830, 0.852] (seeds 50) | 0.159 [0.147, 0.171] (seeds 50) |
| shift_no_gate | 0.410 [0.330, 0.490] (seeds 50) | 0.590 [0.507, 0.673] (seeds 50) |
| shift_pds_n15 | 0.722 [0.692, 0.752] (seeds 50) | 0.278 [0.245, 0.308] (seeds 50) |
| shift_pds_n30 | 0.886 [0.872, 0.900] (seeds 50) | 0.114 [0.101, 0.128] (seeds 50) |
| shift_pds_n50 | 0.912 [0.901, 0.923] (seeds 50) | 0.088 [0.076, 0.100] (seeds 50) |
| shift_repaired_quantile_n15 | 0.931 [0.916, 0.945] (seeds 50) | 0.069 [0.055, 0.085] (seeds 50) |
| shift_repaired_quantile_n3 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n30 | 0.894 [0.879, 0.908] (seeds 50) | 0.106 [0.092, 0.120] (seeds 50) |
| shift_repaired_quantile_n5 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n50 | 0.899 [0.887, 0.910] (seeds 50) | 0.101 [0.090, 0.113] (seeds 50) |
| shift_repaired_quantile_n9 | 0.910 [0.883, 0.933] (seeds 50) | 0.090 [0.067, 0.117] (seeds 50) |
| shift_slope_bias_n15 | 0.827 [0.814, 0.840] (seeds 50) | 0.173 [0.159, 0.185] (seeds 50) |
| shift_slope_bias_n30 | 0.834 [0.820, 0.848] (seeds 50) | 0.166 [0.153, 0.180] (seeds 50) |
| shift_slope_bias_n5 | 0.792 [0.767, 0.812] (seeds 50) | 0.208 [0.188, 0.232] (seeds 50) |
| shift_slope_bias_n50 | 0.837 [0.825, 0.848] (seeds 50) | 0.163 [0.150, 0.175] (seeds 50) |
| shift_slope_bias_n9 | 0.817 [0.800, 0.832] (seeds 50) | 0.183 [0.166, 0.200] (seeds 50) |

## Stress tests (home spectra with synthetic faults)

| Fault | released fraction | unconditional wrong release |
|---|---|---|
| home_label_noise_5mg | 0.928 [0.919, 0.936] (seeds 50) | 0.028 [0.024, 0.032] (seeds 50) |
| stress_baseline_offset | 0.931 [0.923, 0.938] (seeds 50) | 0.071 [0.061, 0.082] (seeds 50) |
| stress_baseline_slope | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_dead_channels | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_gain | 0.931 [0.924, 0.939] (seeds 50) | 0.071 [0.061, 0.082] (seeds 50) |
| stress_gradual_drift | 0.931 [0.923, 0.939] (seeds 50) | 0.071 [0.061, 0.082] (seeds 50) |
| stress_noise | 0.008 [0.004, 0.013] (seeds 50) | 0.005 [0.002, 0.008] (seeds 50) |
| stress_spikes | 0.133 [0.095, 0.176] (seeds 50) | 0.065 [0.046, 0.085] (seeds 50) |
| stress_wavelength_shift | 0.240 [0.198, 0.286] (seeds 50) | 0.237 [0.194, 0.281] (seeds 50) |

## Selective prediction (gate confidence = conformal p-value; error = interval miss)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| aurc | 0.069 [0.060, 0.078] (seeds 50) | 0.587 [0.498, 0.672] (seeds 50) |
| e_aurc | 0.063 [0.056, 0.071] (seeds 50) | 0.232 [0.203, 0.259] (seeds 50) |
| aurc_oracle | 0.006 [0.004, 0.008] (seeds 50) | 0.355 [0.271, 0.443] (seeds 50) |

## Held-out shift-type protocol (threshold tuned for 90% detection on the row family; cells = released fraction on the column family)

| tuned on | threshold | home abstention | wavelength_shift | baseline_offset | baseline_slope | gain | noise | spikes | dead_channels | gradual_drift | instrument |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wavelength_shift | 0.17 | 0.12 | 0.07 | 0.88 | 0.00 | 0.88 | 0.00 | 0.04 | 0.00 | 0.88 | 0.00 |
| baseline_offset | 0.50 | 0.50 | 0.00 | 0.50 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 |
| baseline_slope | 0.02 | 0.01 | 0.81 | 0.99 | 0.00 | 0.99 | 0.29 | 0.68 | 0.00 | 0.99 | 0.43 |
| gain | 0.50 | 0.50 | 0.00 | 0.50 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 |
| noise | 0.04 | 0.03 | 0.61 | 0.97 | 0.00 | 0.97 | 0.03 | 0.44 | 0.00 | 0.97 | 0.05 |
| spikes | 0.12 | 0.08 | 0.19 | 0.92 | 0.00 | 0.92 | 0.00 | 0.07 | 0.00 | 0.92 | 0.00 |
| dead_channels | 0.02 | 0.01 | 0.81 | 0.99 | 0.00 | 0.99 | 0.29 | 0.68 | 0.00 | 0.99 | 0.43 |
| gradual_drift | 0.50 | 0.50 | 0.00 | 0.50 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 |
| instrument | 0.04 | 0.03 | 0.61 | 0.97 | 0.00 | 0.97 | 0.04 | 0.44 | 0.00 | 0.97 | 0.02 |

In-family released 0.19; out-of-family released 0.38 (worst 0.99).

## Operational cost curves in USD (illustrative cost inputs)

False hold 30,082 USD (testing 30,000 + 82 delay carrying on a 30,000 USD batch); with investigation 50,082; wrong release 2,000,000 (tier 5); implied ratio 66.5 vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.

### home instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.091 | 181,652 | 181,652 | 331,206 |
| 0.01 | 0.000 | 0.091 | 181,652 | 181,652 | 331,206 |
| 0.02 | 0.010 | 0.087 | 174,641 | 174,836 | 341,721 |
| 0.05 | 0.028 | 0.081 | 161,960 | 162,511 | 363,096 |
| 0.1 | 0.069 | 0.071 | 144,155 | 145,530 | 394,326 |
| 0.2 | 0.146 | 0.060 | 125,272 | 128,199 | 424,916 |
| 0.3 | 0.255 | 0.050 | 108,015 | 113,112 | 446,748 |
| 0.5 | 0.495 | 0.030 | 75,422 | 85,328 | 501,715 |

### shifted instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.590 | 1,179,217 | 1,179,217 | 51,021 |
| 0.01 | 0.000 | 0.590 | 1,179,217 | 1,179,217 | 51,021 |
| 0.02 | 0.569 | 0.263 | 543,123 | 554,508 | 49,273 |
| 0.05 | 0.909 | 0.064 | 155,247 | 173,420 | 42,966 |
| 0.1 | 0.990 | 0.006 | 41,348 | 61,149 | 51,796 |
| 0.2 | 0.998 | 0.001 | 31,075 | 51,041 | 97,767 |
| 0.3 | 1.000 | 0.000 | 30,161 | 50,156 | 180,493 |
| 0.5 | 1.000 | 0.000 | 30,082 | 50,082 | inf |

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
