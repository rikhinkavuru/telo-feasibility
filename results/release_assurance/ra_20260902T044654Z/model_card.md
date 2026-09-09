# Model card: conservative release gate on public NIR tablet spectra

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

## Intended use
Research evidence that a conventional PLS calibration fails under instrument shift and that a conformal novelty gate can detect the shift and decline to certify. Not for batch release, not evidence on any sterile injectable, not a validated method.

## Data
IDRC 2002 NIR tablet shootout (frozen as source S28, sha256 129a32ec9e19...): 155 calibration and 460 test tablets measured on two instruments; assay (mg) as reference. No lot, time, operator, or site metadata exist; synthetic groups are index blocks.

## Method
SNV, PLS with 5-fold-CV-selected components on a 105-tablet training partition, split-conformal interval at alpha = 0.1 on the remaining calibration tablets, 1-NN novelty gate with conformal p-value threshold 0.1; 50 random partitions; bootstrap 95% intervals over partitions.

## Metrics that travel together (test instrument = shift)

| Metric | Home instrument | Shifted instrument |
|---|---|---|
| released_fraction | 0.919 [0.910, 0.927] (seeds 50) | 0.561 [0.523, 0.602] (seeds 50) |
| abstention_fraction | 0.081 [0.073, 0.090] (seeds 50) | 0.439 [0.398, 0.477] (seeds 50) |
| unconditional_wrong_release | 0.061 [0.054, 0.070] (seeds 50) | 0.155 [0.137, 0.172] (seeds 50) |
| conditional_error_among_released | 0.067 [0.059, 0.076] (seeds 50) | 0.290 [0.256, 0.327] (seeds 50) |
| empirical_coverage | 0.928 [0.916, 0.939] (seeds 50) | 0.717 [0.685, 0.746] (seeds 50) |
| false_hold_rate | 0.076 [0.069, 0.083] (seeds 50) | 0.441 [0.393, 0.486] (seeds 50) |

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
| shift_mandatory_hold | 0.717 [0.685, 0.746] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.861 [0.853, 0.870] (seeds 50) | 0.139 [0.130, 0.147] (seeds 50) |
| shift_no_gate | 0.717 [0.686, 0.746] (seeds 50) | 0.283 [0.256, 0.315] (seeds 50) |
| shift_pds_n15 | 0.827 [0.812, 0.845] (seeds 50) | 0.173 [0.154, 0.189] (seeds 50) |
| shift_pds_n30 | 0.894 [0.885, 0.903] (seeds 50) | 0.106 [0.097, 0.115] (seeds 50) |
| shift_pds_n50 | 0.897 [0.889, 0.904] (seeds 50) | 0.103 [0.095, 0.111] (seeds 50) |
| shift_repaired_quantile_n15 | 0.927 [0.910, 0.944] (seeds 50) | 0.073 [0.055, 0.091] (seeds 50) |
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

## Limitations

- Instrument is the only real group; lot and time groups are SYNTHETIC index blocks and test nothing about real lots or time.
- Wrong release here means the certified interval missed the reference assay; it is not an out-of-specification release rate.
- Repair curves reuse calibration tablets re-measured on the shifted instrument; they never touch the test set.
- PLS components are chosen by 5-fold CV on the training partition of each seed (the repository's fixed N_PLS=8 is not reproduced).
- No Telo data, no target chemistry, no prospective validation; this supports stop-the-line detection claims only.

## Claims table

| Claim | Allowed |
|---|---|
| Detects this instrument shift and abstains | yes, as measured above |
| Automates batch release | no |
| Useful operational coverage under shift | no (see released fraction on the shifted instrument) |
| Evidence on the target drug chemistry | no |
| Prospective product/site validation | no |
| Replaces sterility assurance or any mandatory test | no |
