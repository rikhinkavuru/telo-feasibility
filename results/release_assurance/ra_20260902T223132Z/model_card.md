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
| released_fraction | 0.930 [0.920, 0.939] (seeds 50) | 0.000 [0.000, 0.001] (seeds 50) |
| abstention_fraction | 0.070 [0.061, 0.080] (seeds 50) | 1.000 [0.999, 1.000] (seeds 50) |
| unconditional_wrong_release | 0.063 [0.054, 0.072] (seeds 50) | 0.000 [0.000, 0.001] (seeds 50) |
| conditional_error_among_released | 0.068 [0.058, 0.078] (seeds 50) | 0.667 [0.400, 1.000] (seeds 3) |
| empirical_coverage | 0.928 [0.916, 0.939] (seeds 50) | 0.717 [0.684, 0.745] (seeds 50) |
| false_hold_rate | 0.065 [0.057, 0.074] (seeds 50) | 1.000 [0.999, 1.000] (seeds 50) |
| r2 | 0.908 [0.906, 0.910] (seeds 50) | 0.774 [0.760, 0.788] (seeds 50) |

Pooled shifted-instrument counts: released 11 of 23000 tablet-evaluations.

## Risk-coverage curve (shifted instrument, gate threshold sweep)

| threshold | released | conditional error | unconditional exposure | operational cost (relative) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.283 | 0.283 | 14.170 |
| 0.01 | 1.000 | 0.283 | 0.283 | 14.170 |
| 0.02 | 0.443 | 0.354 | 0.134 | 7.260 |
| 0.05 | 0.088 | 0.466 | 0.030 | 2.423 |
| 0.1 | 0.000 | 0.667 | 0.000 | 1.013 |
| 0.2 | 0.000 | nan | 0.000 | 1.000 |
| 0.3 | 0.000 | nan | 0.000 | 1.000 |
| 0.5 | 0.000 | nan | 0.000 | 1.000 |

## Baselines and repair (shifted instrument, no gate)

| Configuration | empirical coverage | unconditional wrong release |
|---|---|---|
| shift_ds_n15 | 0.845 [0.825, 0.866] (seeds 50) | 0.155 [0.135, 0.176] (seeds 50) |
| shift_ds_n30 | 0.852 [0.837, 0.866] (seeds 50) | 0.148 [0.134, 0.163] (seeds 50) |
| shift_ds_n50 | 0.826 [0.807, 0.844] (seeds 50) | 0.174 [0.156, 0.192] (seeds 50) |
| shift_instrument_std_n15 | 0.864 [0.850, 0.878] (seeds 50) | 0.136 [0.123, 0.151] (seeds 50) |
| shift_instrument_std_n30 | 0.877 [0.869, 0.885] (seeds 50) | 0.123 [0.115, 0.131] (seeds 50) |
| shift_instrument_std_n50 | 0.880 [0.873, 0.887] (seeds 50) | 0.120 [0.113, 0.127] (seeds 50) |
| shift_mandatory_hold | 0.717 [0.685, 0.747] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.861 [0.853, 0.870] (seeds 50) | 0.139 [0.130, 0.147] (seeds 50) |
| shift_no_gate | 0.717 [0.685, 0.746] (seeds 50) | 0.283 [0.254, 0.313] (seeds 50) |
| shift_pds_n15 | 0.827 [0.811, 0.845] (seeds 50) | 0.173 [0.157, 0.190] (seeds 50) |
| shift_pds_n30 | 0.894 [0.885, 0.903] (seeds 50) | 0.106 [0.096, 0.115] (seeds 50) |
| shift_pds_n50 | 0.897 [0.890, 0.905] (seeds 50) | 0.103 [0.095, 0.111] (seeds 50) |
| shift_repaired_quantile_n15 | 0.927 [0.909, 0.944] (seeds 50) | 0.073 [0.056, 0.088] (seeds 50) |
| shift_repaired_quantile_n3 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n30 | 0.866 [0.853, 0.877] (seeds 50) | 0.134 [0.122, 0.147] (seeds 50) |
| shift_repaired_quantile_n5 | 1.000 [1.000, 1.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_repaired_quantile_n50 | 0.869 [0.863, 0.875] (seeds 50) | 0.131 [0.124, 0.138] (seeds 50) |
| shift_repaired_quantile_n9 | 0.894 [0.867, 0.917] (seeds 50) | 0.106 [0.083, 0.132] (seeds 50) |
| shift_slope_bias_n15 | 0.863 [0.855, 0.871] (seeds 50) | 0.137 [0.129, 0.144] (seeds 50) |
| shift_slope_bias_n30 | 0.865 [0.858, 0.872] (seeds 50) | 0.135 [0.127, 0.142] (seeds 50) |
| shift_slope_bias_n5 | 0.844 [0.825, 0.858] (seeds 50) | 0.156 [0.141, 0.174] (seeds 50) |
| shift_slope_bias_n50 | 0.864 [0.857, 0.872] (seeds 50) | 0.136 [0.128, 0.143] (seeds 50) |
| shift_slope_bias_n9 | 0.856 [0.844, 0.866] (seeds 50) | 0.144 [0.134, 0.154] (seeds 50) |

## Stress tests (home spectra with synthetic faults)

| Fault | released fraction | unconditional wrong release |
|---|---|---|
| home_label_noise_5mg | 0.927 [0.914, 0.938] (seeds 50) | 0.019 [0.016, 0.022] (seeds 50) |
| stress_baseline_offset | 0.930 [0.921, 0.939] (seeds 50) | 0.063 [0.055, 0.072] (seeds 50) |
| stress_baseline_slope | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_dead_channels | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_gain | 0.930 [0.920, 0.939] (seeds 50) | 0.063 [0.055, 0.071] (seeds 50) |
| stress_gradual_drift | 0.930 [0.921, 0.939] (seeds 50) | 0.063 [0.054, 0.071] (seeds 50) |
| stress_noise | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_spikes | 0.000 [0.000, 0.000] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| stress_wavelength_shift | 0.001 [0.000, 0.002] (seeds 50) | 0.001 [0.000, 0.001] (seeds 50) |

## Selective prediction (gate confidence = conformal p-value; error = interval miss)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| aurc | 0.054 [0.047, 0.062] (seeds 50) | 0.313 [0.279, 0.350] (seeds 50) |
| e_aurc | 0.051 [0.044, 0.057] (seeds 50) | 0.259 [0.234, 0.281] (seeds 50) |
| aurc_oracle | 0.004 [0.003, 0.005] (seeds 50) | 0.054 [0.042, 0.068] (seeds 50) |

## Held-out shift-type protocol (threshold tuned for 90% detection on the row family; cells = released fraction on the column family)

| tuned on | threshold | home abstention | wavelength_shift | baseline_offset | baseline_slope | gain | noise | spikes | dead_channels | gradual_drift | instrument |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wavelength_shift | 0.05 | 0.02 | 0.02 | 0.98 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.98 | 0.01 |
| baseline_offset | 0.50 | 0.51 | 0.00 | 0.49 | 0.00 | 0.49 | 0.00 | 0.00 | 0.00 | 0.49 | 0.00 |
| baseline_slope | 0.03 | 0.01 | 0.22 | 0.99 | 0.02 | 0.99 | 0.00 | 0.00 | 0.00 | 0.99 | 0.15 |
| gain | 0.50 | 0.51 | 0.00 | 0.49 | 0.00 | 0.49 | 0.00 | 0.00 | 0.00 | 0.49 | 0.00 |
| noise | 0.02 | 0.00 | 0.54 | 1.00 | 0.36 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.44 |
| spikes | 0.02 | 0.00 | 0.54 | 1.00 | 0.36 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.44 |
| dead_channels | 0.02 | 0.00 | 0.54 | 1.00 | 0.36 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.44 |
| gradual_drift | 0.50 | 0.51 | 0.00 | 0.49 | 0.00 | 0.49 | 0.00 | 0.00 | 0.00 | 0.49 | 0.00 |
| instrument | 0.04 | 0.02 | 0.07 | 0.98 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.98 | 0.02 |

In-family released 0.17; out-of-family released 0.35 (worst 1.00).

## Operational cost curves in USD (illustrative cost inputs)

False hold 30,082 USD (testing 30,000 + 82 delay carrying on a 30,000 USD batch); with investigation 50,082; wrong release 2,000,000 (tier 5); implied ratio 66.5 vs legacy 50. Holding every batch costs one false hold per batch; break-even is the wrong-release cost below which the gate beats that.

### home instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.072 | 144,957 | 144,957 | 415,050 |
| 0.01 | 0.000 | 0.072 | 144,957 | 144,957 | 415,050 |
| 0.02 | 0.003 | 0.072 | 143,663 | 143,729 | 417,706 |
| 0.05 | 0.015 | 0.070 | 140,441 | 140,734 | 423,448 |
| 0.1 | 0.070 | 0.063 | 127,764 | 129,169 | 445,195 |
| 0.2 | 0.183 | 0.050 | 105,676 | 109,335 | 490,741 |
| 0.3 | 0.292 | 0.039 | 87,750 | 93,596 | 539,259 |
| 0.5 | 0.513 | 0.024 | 62,476 | 72,736 | 622,828 |

### shifted instrument

| threshold | abstention | exposure | cost USD/batch | with investigation | break-even wrong-release USD |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.283 | 566,783 | 566,783 | 106,151 |
| 0.01 | 0.000 | 0.283 | 566,783 | 566,783 | 106,151 |
| 0.02 | 0.557 | 0.134 | 284,854 | 296,002 | 99,331 |
| 0.05 | 0.912 | 0.030 | 87,870 | 106,110 | 87,606 |
| 0.1 | 1.000 | 0.000 | 30,589 | 50,580 | 55,151 |
| 0.2 | 1.000 | 0.000 | 30,082 | 50,082 | inf |
| 0.3 | 1.000 | 0.000 | 30,082 | 50,082 | inf |
| 0.5 | 1.000 | 0.000 | 30,082 | 50,082 | inf |

## Limitations

- Instrument is the only real group; lot and time groups are SYNTHETIC index blocks and test nothing about real lots or time.
- Wrong release here means the certified interval missed the reference assay; it is not an out-of-specification release rate.
- Repair curves reuse calibration tablets re-measured on the shifted instrument; they never touch the test set.
- PLS components are chosen by 5-fold CV on the training partition of each seed (the repository's fixed N_PLS=8 is not reproduced).
- No Telo data, no target chemistry, no prospective validation; this supports stop-the-line detection claims only.
- Gate statistic: q_residual; component selection: train_cv.
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
