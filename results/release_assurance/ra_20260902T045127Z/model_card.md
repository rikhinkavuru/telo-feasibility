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
| shift_mandatory_hold | 0.410 [0.326, 0.494] (seeds 50) | 0.000 [0.000, 0.000] (seeds 50) |
| shift_mean_centering | 0.841 [0.830, 0.852] (seeds 50) | 0.159 [0.147, 0.171] (seeds 50) |
| shift_no_gate | 0.410 [0.330, 0.490] (seeds 50) | 0.590 [0.507, 0.673] (seeds 50) |
| shift_pds_n15 | 0.722 [0.692, 0.752] (seeds 50) | 0.278 [0.245, 0.308] (seeds 50) |
| shift_pds_n30 | 0.886 [0.872, 0.900] (seeds 50) | 0.114 [0.101, 0.128] (seeds 50) |
| shift_pds_n50 | 0.912 [0.901, 0.923] (seeds 50) | 0.088 [0.076, 0.100] (seeds 50) |
| shift_repaired_quantile_n15 | 0.931 [0.916, 0.945] (seeds 50) | 0.069 [0.055, 0.085] (seeds 50) |
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
