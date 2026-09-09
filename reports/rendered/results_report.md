# Telo feasibility study: results report (auto-built 2026-09-06T13:09:54.588691+00:00)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Protocol v1.0.0. Central question: Under what product, demand, regulatory, and operating conditions can distributed regional capacity reduce sterile-injectable shortages more cost-effectively than additional safety stock, dual sourcing, reserved contract capacity, or additional centralized capacity?

## Definition-of-finished status

```
PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS
definition of finished: 9/22 complete

DF01 ---- protocol version frozen
      protocol v1.0.0 status=frozen; revisions pending sign-off: ['R000', 'R001', 'R002', 'R003', 'R004', 'R005', 'R006', 'R007', 'R008', 'R009', 'R010', 'R011']
DF02 PASS five-product dated screen complete
      screen_manifest.json candidates=6, dated snapshots=True
DF03 ---- [human] two exact product presentations selected
      selection.json selected=0
DF04 ---- product dossiers complete
      complete dossiers=0
DF05 ---- all eight strategies represented
      strategies in simulation manifests: ['S0', 'S1', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
DF06 PASS strategies optimized to matched service targets
      optimization summaries=9
DF07 PASS approved-generic/CMO and 503B pathways separated
      decision maps present=[True, True]
DF08 ---- [human] material regulatory gates reviewed by a qualified expert
      reviewed 0/16; UNCERTAIN: ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
DF09 ---- no material illustrative input remains
      illustrative=87, missing=0 of 91 parameters
DF10 ---- [human] direct or expert-validated input distributions documented
      same evidence as DF09 plus distribution records
DF11 PASS deterministic model reconciles with workbook
      results/deterministic/reconciliation.json ok=True
DF12 PASS stochastic simulation passes all tests
      test_report.json={'generated_at': '2026-09-06T02:59:55.905034+00:00', 'passed': 243, 'failed': 0, 'skipped': 0, 'crn_test_passed': True, 'common_cause_test_passed': True, 'mass_balance_property_passed': True, 'exit_code': 0}; simulation manifests=4
DF13 PASS common random numbers implemented
      requires test_report.json crn_test_passed
DF14 PASS common-cause failures represented
      requires test_report.json common_cause_test_passed
DF15 ---- historical backcasts complete
      backcast comparisons=0 (need >= 4 episode classes)
DF16 PASS global and structural sensitivity complete
      results/sensitivity/summary.json present=True
DF17 PASS decision-reversal and value-of-information analyses complete
      decision_reversal.json and voi.json present=True
DF18 ---- [human] real interview evidence logged
      completed interviews logged=0 (target 25-30)
DF19 ---- [human] at least three qualified independent reviews completed
      completed reviews=0
DF20 ---- [human] public code, data dictionary, assumptions, model cards, run manifest, revision log, and limitations released
      public_release.json=absent
DF21 ---- at least one non-obvious result identified
      nonobvious_finding.json=absent
DF22 ---- [human] external claims do not exceed evidence
      claims register rows unsupported/contradicted/retracted: ['C001', 'C007', 'C008', 'C009', 'C010', 'C012', 'C013', 'C015', 'C016', 'C017', 'C018', 'C023', 'C024', 'C025']
```

## Strategies optimized to the frozen service target (tau = 0.99, q = 0.9)

Run `opt_20260902T043854Z`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. 

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible | - | - | closest 0.988 | - | - |
| norepinephrine_1mgml_4ml | S1 | infeasible | - | - | closest 0.989 | - | - |
| norepinephrine_1mgml_4ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.6, "independent_api_supplier": 1.0, "safety_stock_days": 120.0, "material_target_days": 105.0} | 18,364,888 (4,434) | 0.993 | 0.84 | 19.65 |
| norepinephrine_1mgml_4ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 2.0, "safety_stock_days": 78.75} | 24,794,805 (4,257) | 0.993 | 0.86 | 26.56 |
| norepinephrine_1mgml_4ml | S4 | infeasible_at_full_n | {"capacity_factor": 1.65, "safety_stock_days": 120.0, "material_target_days": 180.0} | 31,690,480 (3,729) | 0.993 | 0.86 | 33.92 |
| norepinephrine_1mgml_4ml | S5 | infeasible | - | - | closest 0.992 | - | - |
| norepinephrine_1mgml_4ml | S6 | infeasible | - | - | closest 0.992 | - | - |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.725 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.733 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.95, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 161.25} | 24,490,523 (6,269) | 0.993 | 0.89 | 19.66 |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.25, "activation_threshold_days": 45.0, "campaign_batches": 6.0, "safety_stock_days": 120.0} | 33,011,171 (5,955) | 0.993 | 0.86 | 26.51 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible | - | - | closest 0.995 | - | - |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.895 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.99.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.99.png)

## Strategies optimized to a SENSITIVITY service target (tau = 0.98, q = 0.9)

Run `opt_20260902T050443Z_tau0.98`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. This run varies the threshold as a pre-registered sensitivity; it does not replace the frozen target.

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible_at_full_n | {"safety_stock_days": 90.0, "site_fg_days": 60.0, "material_target_days": 142.5} | 12,709,801 (7,243) | 0.982 | 0.71 | 13.78 |
| norepinephrine_1mgml_4ml | S1 | infeasible_at_full_n | {"safety_stock_days": 113.75, "site_fg_days": 60.0, "material_target_days": 180.0} | 12,708,527 (7,026) | 0.985 | 0.78 | 13.73 |
| norepinephrine_1mgml_4ml | S2 | optimal | {"capacity_factor": 0.6, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 30.0} | 18,356,820 (5,646) | 0.989 | 0.91 | 19.72 |
| norepinephrine_1mgml_4ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 1.0, "safety_stock_days": 120.0} | 24,738,777 (4,310) | 0.986 | 0.83 | 26.69 |
| norepinephrine_1mgml_4ml | S4 | infeasible_at_full_n | {"capacity_factor": 1.33125, "safety_stock_days": 120.0, "material_target_days": 105.0} | 28,000,022 (4,144) | 0.990 | 0.89 | 30.06 |
| norepinephrine_1mgml_4ml | S5 | infeasible_at_full_n | {"sites": 4.0, "node_scale": 0.15, "safety_stock_days": 90.0, "material_target_days": 180.0} | 37,006,659 (6,371) | 0.990 | 0.85 | 39.76 |
| norepinephrine_1mgml_4ml | S6 | infeasible_at_full_n | {"sites": 4.0, "node_scale": 0.15, "safety_stock_days": 90.0, "material_target_days": 180.0} | 39,268,555 (6,371) | 0.990 | 0.85 | 42.19 |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.725 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.733 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | optimal | {"capacity_factor": 1.0666666666666667, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 30.0} | 26,066,318 (8,156) | 0.992 | 0.94 | 20.93 |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 4.0, "safety_stock_days": 92.5} | 25,821,485 (6,953) | 0.987 | 0.84 | 20.88 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible_at_full_n | {"capacity_factor": 1.65, "safety_stock_days": 120.0, "material_target_days": 180.0} | 32,754,669 (5,765) | 0.992 | 0.85 | 26.34 |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.895 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.98.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.98.png)

## Strategies optimized to the frozen service target (tau = 0.99, q = 0.9)

Run `opt_20260903T181601Z`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. 

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible | - | - | closest 0.988 | - | - |
| norepinephrine_1mgml_4ml | S1 | infeasible | - | - | closest 0.989 | - | - |
| norepinephrine_1mgml_4ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.6, "independent_api_supplier": 1.0, "safety_stock_days": 120.0, "material_target_days": 105.0} | 18,040,073 (4,412) | 0.993 | 0.84 | 19.31 |
| norepinephrine_1mgml_4ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 4.0, "safety_stock_days": 65.0} | 17,349,860 (4,214) | 0.994 | 0.93 | 18.56 |
| norepinephrine_1mgml_4ml | S4 | infeasible | - | - | closest 0.995 | - | - |
| norepinephrine_1mgml_4ml | S5 | infeasible | - | - | closest 0.992 | - | - |
| norepinephrine_1mgml_4ml | S6 | infeasible | - | - | closest 0.992 | - | - |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.727 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.757 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.95, "independent_api_supplier": 0.0, "safety_stock_days": 78.75, "material_target_days": 67.5} | 24,003,181 (7,386) | 0.991 | 0.8 | 19.31 |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.4, "activation_threshold_days": 45.0, "campaign_batches": 6.0, "safety_stock_days": 120.0} | 21,392,082 (5,909) | 0.993 | 0.86 | 17.18 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible | - | - | closest 0.990 | - | - |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.896 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.99.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.99.png)

## Strategies optimized to a SENSITIVITY service target (tau = 0.98, q = 0.9)

Run `opt_20260903T182509Z_tau0.98`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. This run varies the threshold as a pre-registered sensitivity; it does not replace the frozen target.

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible_at_full_n | {"safety_stock_days": 90.0, "site_fg_days": 60.0, "material_target_days": 142.5} | 12,734,414 (7,208) | 0.982 | 0.71 | 13.80 |
| norepinephrine_1mgml_4ml | S1 | infeasible_at_full_n | {"safety_stock_days": 323.125, "site_fg_days": 60.0, "material_target_days": 180.0} | 12,565,575 (6,509) | 0.983 | 0.73 | 13.59 |
| norepinephrine_1mgml_4ml | S2 | optimal | {"capacity_factor": 0.6, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 30.0} | 18,007,150 (5,617) | 0.989 | 0.91 | 19.34 |
| norepinephrine_1mgml_4ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 1.0, "safety_stock_days": 120.0} | 17,269,389 (4,078) | 0.985 | 0.83 | 18.65 |
| norepinephrine_1mgml_4ml | S4 | infeasible_at_full_n | {"capacity_factor": 1.0125000000000002, "safety_stock_days": 120.0, "material_target_days": 105.0} | 22,965,117 (4,733) | 0.988 | 0.81 | 24.73 |
| norepinephrine_1mgml_4ml | S5 | infeasible_at_full_n | {"sites": 4.0, "node_scale": 0.15, "safety_stock_days": 90.0, "material_target_days": 180.0} | 35,531,362 (6,353) | 0.990 | 0.85 | 38.18 |
| norepinephrine_1mgml_4ml | S6 | infeasible_at_full_n | {"sites": 4.0, "node_scale": 0.15, "safety_stock_days": 90.0, "material_target_days": 180.0} | 37,681,829 (6,353) | 0.990 | 0.85 | 40.49 |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.727 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.757 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | optimal | {"capacity_factor": 1.0666666666666667, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 30.0} | 25,507,272 (8,013) | 0.992 | 0.94 | 20.49 |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 3.0, "safety_stock_days": 78.75} | 18,385,797 (7,103) | 0.987 | 0.82 | 14.86 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible | - | - | closest 0.990 | - | - |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.936 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.896 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.98.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.98.png)

## Strategies optimized to the frozen service target (tau = 0.99, q = 0.9)

Run `opt_20260903T220534Z`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. 

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible | - | - | closest 0.988 | - | - |
| norepinephrine_1mgml_4ml | S1 | infeasible | - | - | closest 0.989 | - | - |
| norepinephrine_1mgml_4ml | S2 | infeasible | - | - | closest 0.995 | - | - |
| norepinephrine_1mgml_4ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 1.0, "safety_stock_days": 65.0} | 17,335,600 (3,899) | 0.992 | 0.82 | 18.59 |
| norepinephrine_1mgml_4ml | S4 | infeasible | - | - | closest 0.989 | - | - |
| norepinephrine_1mgml_4ml | S5 | infeasible | - | - | closest 0.980 | - | - |
| norepinephrine_1mgml_4ml | S6 | infeasible | - | - | closest 0.980 | - | - |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| norepinephrine_1mgml_4ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 30.0} | 22,311,160 (5,007) | 0.995 | 0.87 | 23.84 |
| norepinephrine_1mgml_4ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 197.5, "material_target_days": 30.0, "region_base_stock": 1.0} | 23,230,390 (4,108) | 0.999 | 0.99 | 24.72 |
| norepinephrine_1mgml_4ml | S10 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 53.125, "material_target_days": 123.75} | 17,473,071 (4,855) | 0.992 | 0.83 | 18.73 |
| norepinephrine_1mgml_4ml | S11 | optimal | {"site_fg_days": 85.83333333333334, "safety_stock_days": 365.0, "region_base_stock": 0.0, "material_target_days": 30.0} | 14,857,064 (5,964) | 0.994 | 0.94 | 15.89 |
| norepinephrine_1mgml_4ml | S12 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 169.58333333333334, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 18,454,935 (6,122) | 0.998 | 0.95 | 19.66 |
| norepinephrine_1mgml_4ml | S13 | optimal | {"safety_stock_days": 141.66666666666669, "region_base_stock": 0.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 18,626,636 (3,294) | 0.996 | 0.91 | 19.89 |
| norepinephrine_1mgml_4ml | S14 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "capacity_factor": 1.05, "site_fg_days": 66.66666666666666} | 23,671,734 (4,402) | 0.992 | 0.78 | 25.39 |
| norepinephrine_1mgml_4ml | S15 | infeasible_at_full_n | {"safety_stock_days": 344.0625, "site_fg_days": 92.5, "material_target_days": 105.0, "region_base_stock": 0.0} | 12,569,122 (8,289) | 0.990 | 0.73 | 13.50 |
| norepinephrine_1mgml_4ml | S16 | optimal | {"safety_stock_days": 143.125, "activation_threshold_days": 3.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 15,890,651 (7,943) | 0.997 | 0.93 | 16.94 |
| norepinephrine_1mgml_4ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 24.0, "campaign_batches": 1.0} | 18,193,995 (2,952) | 0.997 | 0.97 | 19.41 |
| norepinephrine_1mgml_4ml | S18 | infeasible_at_full_n | {"safety_stock_days": 320.625, "site_fg_days": 63.333333333333336, "material_target_days": 161.25, "region_base_stock": 0.0} | 22,655,375 (3,631) | 0.996 | 0.87 | 24.19 |
| norepinephrine_1mgml_4ml | S19 | infeasible_at_full_n | {"safety_stock_days": 155.625, "material_target_days": 30.0, "activation_threshold_days": 10.0, "region_base_stock": 1.0} | 15,793,218 (9,361) | 0.994 | 0.87 | 16.91 |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.727 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.757 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible | - | - | closest 0.959 | - | - |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.25, "activation_threshold_days": 45.0, "campaign_batches": 4.0, "safety_stock_days": 120.0} | 20,026,811 (6,041) | 0.992 | 0.81 | 16.11 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible | - | - | closest 0.951 | - | - |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.865 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.865 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.896 | - | - |
| sodium_bicarbonate_8_4_50ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 105.0} | 23,363,417 (8,539) | 0.990 | 0.7 | 18.82 |
| sodium_bicarbonate_8_4_50ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,399,282 (11,711) | 1.000 | 0.98 | 19.47 |
| sodium_bicarbonate_8_4_50ml | S10 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 32.5, "material_target_days": 105.0} | 18,498,686 (17,970) | 0.995 | 0.9 | 14.83 |
| sodium_bicarbonate_8_4_50ml | S11 | optimal | {"site_fg_days": 197.5, "safety_stock_days": 365.0, "region_base_stock": 1.0, "material_target_days": 30.0} | 15,714,623 (16,070) | 0.997 | 0.94 | 12.57 |
| sodium_bicarbonate_8_4_50ml | S12 | optimal | {"capacity_factor": 1.1, "safety_stock_days": 309.1666666666667, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 22,387,024 (17,515) | 0.998 | 0.95 | 17.88 |
| sodium_bicarbonate_8_4_50ml | S13 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "capacity_factor": 0.9, "site_fg_days": 123.75} | 19,334,584 (9,185) | 0.996 | 0.9 | 15.48 |
| sodium_bicarbonate_8_4_50ml | S14 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "capacity_factor": 1.05, "site_fg_days": 137.5} | 24,836,190 (7,414) | 0.993 | 0.81 | 19.96 |
| sodium_bicarbonate_8_4_50ml | S15 | infeasible | - | - | closest 0.939 | - | - |
| sodium_bicarbonate_8_4_50ml | S16 | optimal | {"safety_stock_days": 365.0, "activation_threshold_days": 61.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 16,475,242 (6,046) | 0.997 | 0.94 | 13.18 |
| sodium_bicarbonate_8_4_50ml | S17 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 45.0, "campaign_batches": 1.0} | 19,127,163 (4,266) | 0.996 | 0.88 | 15.32 |
| sodium_bicarbonate_8_4_50ml | S18 | optimal | {"safety_stock_days": 187.5, "site_fg_days": 180.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 23,973,297 (6,897) | 0.999 | 0.95 | 19.14 |
| sodium_bicarbonate_8_4_50ml | S19 | infeasible | - | - | closest 0.920 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.99.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.99.png)

## Strategies optimized to a SENSITIVITY service target (tau = 0.98, q = 0.9)

Run `opt_20260903T231408Z_tau0.98`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. This run varies the threshold as a pre-registered sensitivity; it does not replace the frozen target.

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible_at_full_n | {"safety_stock_days": 90.0, "site_fg_days": 60.0, "material_target_days": 142.5} | 12,734,412 (7,208) | 0.982 | 0.71 | 13.80 |
| norepinephrine_1mgml_4ml | S1 | infeasible_at_full_n | {"safety_stock_days": 323.125, "site_fg_days": 60.0, "material_target_days": 180.0} | 12,565,573 (6,510) | 0.983 | 0.73 | 13.59 |
| norepinephrine_1mgml_4ml | S2 | infeasible_at_full_n | {"capacity_factor": 1.0666666666666667, "independent_api_supplier": 0.0, "safety_stock_days": 120.0, "material_target_days": 105.0} | 23,883,410 (3,947) | 0.989 | 0.83 | 25.69 |
| norepinephrine_1mgml_4ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 1.0, "safety_stock_days": 120.0} | 17,273,784 (3,890) | 0.986 | 0.9 | 18.63 |
| norepinephrine_1mgml_4ml | S4 | infeasible | - | - | closest 0.989 | - | - |
| norepinephrine_1mgml_4ml | S5 | infeasible | - | - | closest 0.980 | - | - |
| norepinephrine_1mgml_4ml | S6 | infeasible | - | - | closest 0.980 | - | - |
| norepinephrine_1mgml_4ml | S7 | infeasible | - | - | closest 0.963 | - | - |
| norepinephrine_1mgml_4ml | S8 | infeasible_at_full_n | {"safety_stock_days": 337.08333333333337, "region_base_stock": 0.0, "site_fg_days": 30.0, "material_target_days": 123.75} | 22,133,025 (3,958) | 0.986 | 0.84 | 23.87 |
| norepinephrine_1mgml_4ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 155.625, "material_target_days": 30.0, "region_base_stock": 1.0} | 23,201,059 (4,188) | 0.998 | 0.98 | 24.73 |
| norepinephrine_1mgml_4ml | S10 | infeasible_at_full_n | {"safety_stock_days": 342.8125, "region_base_stock": 0.0, "site_fg_days": 32.5, "material_target_days": 123.75} | 17,373,806 (4,057) | 0.987 | 0.85 | 18.72 |
| norepinephrine_1mgml_4ml | S11 | optimal | {"site_fg_days": 57.91666666666667, "safety_stock_days": 365.0, "region_base_stock": 0.0, "material_target_days": 30.0} | 14,801,475 (5,160) | 0.990 | 0.94 | 15.90 |
| norepinephrine_1mgml_4ml | S12 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 169.58333333333334, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 18,454,935 (6,122) | 0.998 | 0.97 | 19.66 |
| norepinephrine_1mgml_4ml | S13 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 18,412,764 (3,185) | 0.988 | 0.9 | 19.82 |
| norepinephrine_1mgml_4ml | S14 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "capacity_factor": 1.05, "site_fg_days": 38.33333333333333} | 23,598,080 (4,587) | 0.988 | 0.87 | 25.41 |
| norepinephrine_1mgml_4ml | S15 | infeasible_at_full_n | {"safety_stock_days": 365.0, "site_fg_days": 180.0, "material_target_days": 30.0, "region_base_stock": 0.0} | 12,575,472 (13,365) | 0.988 | 0.82 | 13.54 |
| norepinephrine_1mgml_4ml | S16 | optimal | {"safety_stock_days": 98.75, "activation_threshold_days": 3.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 15,868,201 (7,467) | 0.995 | 0.93 | 16.96 |
| norepinephrine_1mgml_4ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 24.0, "campaign_batches": 1.0} | 18,193,995 (2,952) | 0.997 | 0.99 | 19.41 |
| norepinephrine_1mgml_4ml | S18 | infeasible_at_full_n | {"safety_stock_days": 365.0, "site_fg_days": 63.333333333333336, "material_target_days": 30.0, "region_base_stock": 0.0} | 22,585,913 (4,287) | 0.990 | 0.86 | 24.26 |
| norepinephrine_1mgml_4ml | S19 | infeasible_at_full_n | {"safety_stock_days": 113.75, "material_target_days": 30.0, "activation_threshold_days": 38.33333333333333, "region_base_stock": 1.0} | 15,782,406 (8,316) | 0.991 | 0.87 | 16.95 |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.727 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.757 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible | - | - | closest 0.959 | - | - |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 45.0, "campaign_batches": 6.0, "safety_stock_days": 65.0} | 18,413,827 (6,835) | 0.988 | 0.85 | 14.86 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible | - | - | closest 0.951 | - | - |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible | - | - | closest 0.865 | - | - |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible | - | - | closest 0.865 | - | - |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.896 | - | - |
| sodium_bicarbonate_8_4_50ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 67.5} | 23,331,796 (8,084) | 0.989 | 0.8 | 18.82 |
| sodium_bicarbonate_8_4_50ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 323.125, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,363,716 (11,291) | 0.998 | 0.93 | 19.48 |
| sodium_bicarbonate_8_4_50ml | S10 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 46.25, "material_target_days": 30.0} | 18,405,292 (19,262) | 0.993 | 0.91 | 14.78 |
| sodium_bicarbonate_8_4_50ml | S11 | infeasible_at_full_n | {"site_fg_days": 365.0, "safety_stock_days": 306.6666666666667, "region_base_stock": 0.0, "material_target_days": 105.0} | 15,498,913 (8,753) | 0.989 | 0.82 | 12.51 |
| sodium_bicarbonate_8_4_50ml | S12 | optimal | {"capacity_factor": 1.1, "safety_stock_days": 281.25, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 22,366,640 (17,176) | 0.997 | 0.94 | 17.90 |
| sodium_bicarbonate_8_4_50ml | S13 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "capacity_factor": 0.9, "site_fg_days": 123.75} | 19,334,584 (9,185) | 0.996 | 0.95 | 15.48 |
| sodium_bicarbonate_8_4_50ml | S14 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "capacity_factor": 1.05, "site_fg_days": 123.33333333333333} | 24,806,413 (7,866) | 0.990 | 0.83 | 19.98 |
| sodium_bicarbonate_8_4_50ml | S15 | infeasible | - | - | closest 0.939 | - | - |
| sodium_bicarbonate_8_4_50ml | S16 | optimal | {"safety_stock_days": 365.0, "activation_threshold_days": 32.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 16,418,680 (5,993) | 0.994 | 0.91 | 13.18 |
| sodium_bicarbonate_8_4_50ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 24.0, "campaign_batches": 4.0} | 19,107,224 (5,087) | 0.992 | 0.93 | 15.36 |
| sodium_bicarbonate_8_4_50ml | S18 | optimal | {"safety_stock_days": 187.5, "site_fg_days": 180.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 23,973,297 (6,897) | 0.999 | 0.97 | 19.14 |
| sodium_bicarbonate_8_4_50ml | S19 | infeasible | - | - | closest 0.920 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.98.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.98.png)

## Strategies optimized to the frozen service target (tau = 0.99, q = 0.9)

Run `opt_20260906T032432Z`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. 

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | infeasible_at_full_n | {"safety_stock_days": 30.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 12,895,541 (17,093) | 0.987 | 0.85 | 13.90 |
| norepinephrine_1mgml_4ml | S1 | infeasible_at_full_n | {"safety_stock_days": 30.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 12,895,541 (17,093) | 0.987 | 0.85 | 13.90 |
| norepinephrine_1mgml_4ml | S2 | optimal | {"capacity_factor": 0.6, "independent_api_supplier": 0.0, "safety_stock_days": 197.5, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 18,032,783 (8,514) | 0.999 | 0.95 | 19.20 |
| norepinephrine_1mgml_4ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 34.5, "campaign_batches": 4.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 5.0, "material_target_days": 67.5} | 17,228,420 (3,931) | 0.994 | 0.85 | 18.42 |
| norepinephrine_1mgml_4ml | S4 | infeasible_at_full_n | {"capacity_factor": 0.8, "safety_stock_days": 113.75, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 20,171,341 (14,250) | 0.993 | 0.85 | 21.60 |
| norepinephrine_1mgml_4ml | S5 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 197.5, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 19,996,483 (12,847) | 0.996 | 0.925 | 21.36 |
| norepinephrine_1mgml_4ml | S6 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 197.5, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 20,989,289 (12,847) | 0.996 | 0.925 | 22.42 |
| norepinephrine_1mgml_4ml | S7 | infeasible_at_full_n | {"capacity_factor": 1.05, "safety_stock_days": 30.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 15,812,948 (19,317) | 0.988 | 0.85 | 17.03 |
| norepinephrine_1mgml_4ml | S8 | infeasible_at_full_n | {"safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "site_fg_days": 30.0, "material_target_days": 30.0} | 22,448,079 (7,157) | 0.995 | 0.875 | 23.98 |
| norepinephrine_1mgml_4ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 113.75, "material_target_days": 113.75, "region_base_stock": 1.0} | 23,276,894 (5,640) | 0.997 | 0.9 | 24.82 |
| norepinephrine_1mgml_4ml | S10 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 60.0, "material_target_days": 180.0} | 17,755,950 (6,612) | 0.994 | 0.875 | 18.98 |
| norepinephrine_1mgml_4ml | S11 | optimal | {"site_fg_days": 30.0, "safety_stock_days": 15.0, "region_base_stock": 0.0, "material_target_days": 105.0} | 15,191,425 (14,011) | 0.996 | 0.925 | 16.21 |
| norepinephrine_1mgml_4ml | S12 | infeasible_at_full_n | {"capacity_factor": 0.8, "safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 18,505,387 (9,050) | 0.993 | 0.8 | 19.80 |
| norepinephrine_1mgml_4ml | S13 | optimal | {"safety_stock_days": 85.83333333333334, "region_base_stock": 0.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 18,799,933 (9,292) | 0.998 | 0.95 | 20.03 |
| norepinephrine_1mgml_4ml | S14 | optimal | {"safety_stock_days": 85.83333333333334, "region_base_stock": 1.0, "capacity_factor": 1.05, "site_fg_days": 38.33333333333333} | 23,887,778 (8,348) | 0.997 | 0.9 | 25.48 |
| norepinephrine_1mgml_4ml | S15 | infeasible_at_full_n | {"safety_stock_days": 197.5, "site_fg_days": 92.5, "material_target_days": 105.0, "region_base_stock": 0.0} | 12,817,645 (11,938) | 0.989 | 0.75 | 13.79 |
| norepinephrine_1mgml_4ml | S16 | infeasible_at_full_n | {"safety_stock_days": 98.75, "activation_threshold_days": 32.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 15,926,272 (11,287) | 0.995 | 0.825 | 17.02 |
| norepinephrine_1mgml_4ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 45.0, "campaign_batches": 1.0} | 18,393,073 (4,363) | 0.998 | 1.0 | 19.60 |
| norepinephrine_1mgml_4ml | S18 | optimal | {"safety_stock_days": 231.875, "site_fg_days": 63.333333333333336, "material_target_days": 161.25, "region_base_stock": 0.0} | 22,824,371 (6,206) | 0.997 | 0.9 | 24.34 |
| norepinephrine_1mgml_4ml | S19 | optimal | {"safety_stock_days": 113.75, "material_target_days": 71.875, "activation_threshold_days": 24.166666666666664, "region_base_stock": 1.0} | 15,896,741 (9,559) | 0.996 | 0.925 | 16.97 |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.924 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.924 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.95, "independent_api_supplier": 1.0, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 24,004,187 (12,210) | 0.995 | 0.85 | 19.24 |
| sodium_bicarbonate_8_4_50ml | S3 | infeasible_at_full_n | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 3.0, "campaign_batches": 1.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 92.5, "material_target_days": 30.0} | 18,380,840 (23,179) | 0.992 | 0.8 | 14.77 |
| sodium_bicarbonate_8_4_50ml | S4 | infeasible_at_full_n | {"capacity_factor": 1.0125000000000002, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 48.75, "material_target_days": 30.0} | 23,990,071 (19,322) | 0.995 | 0.875 | 19.22 |
| sodium_bicarbonate_8_4_50ml | S5 | infeasible_at_full_n | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 32,024,370 (35,064) | 0.997 | 0.875 | 25.62 |
| sodium_bicarbonate_8_4_50ml | S6 | infeasible_at_full_n | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 33,751,807 (35,064) | 0.997 | 0.875 | 27.00 |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.943 | - | - |
| sodium_bicarbonate_8_4_50ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 105.0} | 23,672,661 (10,404) | 0.991 | 0.8 | 19.05 |
| sodium_bicarbonate_8_4_50ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,636,340 (17,192) | 0.999 | 0.975 | 19.66 |
| sodium_bicarbonate_8_4_50ml | S10 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 46.25, "material_target_days": 30.0} | 18,620,829 (27,992) | 0.992 | 0.875 | 14.97 |
| sodium_bicarbonate_8_4_50ml | S11 | infeasible_at_full_n | {"site_fg_days": 365.0, "safety_stock_days": 248.33333333333334, "region_base_stock": 0.0, "material_target_days": 30.0} | 15,885,153 (13,997) | 0.988 | 0.775 | 12.82 |
| sodium_bicarbonate_8_4_50ml | S12 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 21,462,545 (27,915) | 0.996 | 0.925 | 17.18 |
| sodium_bicarbonate_8_4_50ml | S13 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 19,635,225 (11,658) | 0.993 | 0.875 | 15.76 |
| sodium_bicarbonate_8_4_50ml | S14 | infeasible_at_full_n | {"safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "capacity_factor": 1.05, "site_fg_days": 123.33333333333333} | 25,164,748 (7,863) | 0.996 | 0.85 | 20.15 |
| sodium_bicarbonate_8_4_50ml | S15 | infeasible | - | - | closest 0.917 | - | - |
| sodium_bicarbonate_8_4_50ml | S16 | infeasible_at_full_n | {"safety_stock_days": 365.0, "activation_threshold_days": 32.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 16,669,049 (8,458) | 0.994 | 0.85 | 13.37 |
| sodium_bicarbonate_8_4_50ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 45.0, "campaign_batches": 4.0} | 19,420,920 (6,388) | 0.996 | 0.925 | 15.54 |
| sodium_bicarbonate_8_4_50ml | S18 | infeasible_at_full_n | {"safety_stock_days": 187.5, "site_fg_days": 180.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,172,177 (14,750) | 0.996 | 0.85 | 19.36 |
| sodium_bicarbonate_8_4_50ml | S19 | infeasible | - | - | closest 0.883 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.99.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.99.png)

## Strategies optimized to the frozen service target (tau = 0.99, q = 0.9)

Run `opt_20260906T043357Z`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. 

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | optimal | {"safety_stock_days": 281.25, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 12,908,926 (13,320) | 0.995 | 0.9166666666666666 | 13.82 |
| norepinephrine_1mgml_4ml | S1 | optimal | {"safety_stock_days": 281.25, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 12,908,926 (13,320) | 0.995 | 0.9166666666666666 | 13.82 |
| norepinephrine_1mgml_4ml | S2 | optimal | {"capacity_factor": 0.6, "independent_api_supplier": 0.0, "safety_stock_days": 197.5, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 18,027,927 (9,502) | 0.999 | 0.95 | 19.22 |
| norepinephrine_1mgml_4ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 3.0, "campaign_batches": 4.0, "safety_stock_days": 30.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 17,477,920 (8,947) | 0.995 | 0.9 | 18.70 |
| norepinephrine_1mgml_4ml | S4 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 197.5, "region_base_stock": 1.0, "site_fg_days": 136.25, "material_target_days": 30.0} | 20,175,060 (9,040) | 0.998 | 0.95 | 21.53 |
| norepinephrine_1mgml_4ml | S5 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 180.0} | 20,041,723 (12,857) | 0.997 | 0.95 | 21.39 |
| norepinephrine_1mgml_4ml | S6 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 180.0} | 21,034,529 (12,857) | 0.997 | 0.95 | 22.45 |
| norepinephrine_1mgml_4ml | S7 | optimal | {"capacity_factor": 1.05, "safety_stock_days": 281.25, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 15,830,052 (14,306) | 0.996 | 0.9333333333333333 | 16.93 |
| norepinephrine_1mgml_4ml | S8 | optimal | {"safety_stock_days": 113.75000000000001, "region_base_stock": 1.0, "site_fg_days": 30.0, "material_target_days": 48.75} | 22,431,114 (5,537) | 0.996 | 0.9166666666666666 | 23.98 |
| norepinephrine_1mgml_4ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 113.75, "material_target_days": 113.75, "region_base_stock": 1.0} | 23,276,869 (4,517) | 0.997 | 0.9166666666666666 | 24.85 |
| norepinephrine_1mgml_4ml | S10 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 60.0, "material_target_days": 180.0} | 17,746,435 (6,039) | 0.994 | 0.85 | 19.01 |
| norepinephrine_1mgml_4ml | S11 | optimal | {"site_fg_days": 30.0, "safety_stock_days": 44.16666666666667, "region_base_stock": 1.0, "material_target_days": 30.0} | 15,149,742 (11,717) | 0.995 | 0.9333333333333333 | 16.22 |
| norepinephrine_1mgml_4ml | S12 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 169.58333333333334, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 18,530,888 (8,393) | 0.997 | 0.9 | 19.78 |
| norepinephrine_1mgml_4ml | S13 | optimal | {"safety_stock_days": 85.83333333333334, "region_base_stock": 0.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 18,788,605 (7,498) | 0.997 | 0.95 | 20.06 |
| norepinephrine_1mgml_4ml | S14 | optimal | {"safety_stock_days": 85.83333333333334, "region_base_stock": 1.0, "capacity_factor": 1.05, "site_fg_days": 38.33333333333333} | 23,884,750 (7,459) | 0.996 | 0.9166666666666666 | 25.54 |
| norepinephrine_1mgml_4ml | S15 | optimal | {"safety_stock_days": 281.25, "site_fg_days": 121.66666666666667, "material_target_days": 180.0, "region_base_stock": 0.0} | 12,870,880 (9,389) | 0.996 | 0.9166666666666666 | 13.76 |
| norepinephrine_1mgml_4ml | S16 | optimal | {"safety_stock_days": 187.5, "activation_threshold_days": 3.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 15,999,380 (12,142) | 0.998 | 0.95 | 17.07 |
| norepinephrine_1mgml_4ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 3.0, "campaign_batches": 4.0} | 18,383,557 (3,862) | 0.997 | 0.95 | 19.64 |
| norepinephrine_1mgml_4ml | S18 | infeasible_at_full_n | {"safety_stock_days": 98.75, "site_fg_days": 63.333333333333336, "material_target_days": 105.0, "region_base_stock": 0.0} | 22,816,291 (8,131) | 0.995 | 0.8333333333333334 | 24.41 |
| norepinephrine_1mgml_4ml | S19 | optimal | {"safety_stock_days": 113.75, "material_target_days": 71.875, "activation_threshold_days": 24.166666666666664, "region_base_stock": 1.0} | 15,879,590 (10,386) | 0.994 | 0.9166666666666666 | 17.02 |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.925 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.925 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | infeasible_at_full_n | {"capacity_factor": 0.95, "independent_api_supplier": 1.0, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 23,997,452 (12,717) | 0.995 | 0.85 | 19.26 |
| sodium_bicarbonate_8_4_50ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 3.0, "campaign_batches": 1.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 18,485,569 (22,869) | 0.996 | 0.9166666666666666 | 14.82 |
| sodium_bicarbonate_8_4_50ml | S4 | optimal | {"capacity_factor": 1.0125000000000002, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 92.5, "material_target_days": 30.0} | 24,044,313 (19,533) | 0.998 | 0.95 | 19.23 |
| sodium_bicarbonate_8_4_50ml | S5 | optimal | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 31,976,051 (36,781) | 0.996 | 0.9 | 25.63 |
| sodium_bicarbonate_8_4_50ml | S6 | optimal | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 33,703,487 (36,781) | 0.996 | 0.9 | 27.02 |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.966 | - | - |
| sodium_bicarbonate_8_4_50ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 105.0} | 23,660,733 (10,680) | 0.991 | 0.7666666666666667 | 19.06 |
| sodium_bicarbonate_8_4_50ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,633,109 (16,504) | 0.999 | 0.9666666666666667 | 19.68 |
| sodium_bicarbonate_8_4_50ml | S10 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 32.5, "material_target_days": 105.0} | 18,743,794 (22,426) | 0.995 | 0.9166666666666666 | 15.05 |
| sodium_bicarbonate_8_4_50ml | S11 | optimal | {"site_fg_days": 253.33333333333334, "safety_stock_days": 365.0, "region_base_stock": 1.0, "material_target_days": 30.0} | 16,108,783 (20,634) | 0.998 | 0.95 | 12.89 |
| sodium_bicarbonate_8_4_50ml | S12 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 21,446,962 (22,881) | 0.997 | 0.9333333333333333 | 17.18 |
| sodium_bicarbonate_8_4_50ml | S13 | infeasible_at_full_n | {"safety_stock_days": 309.1666666666667, "region_base_stock": 1.0, "capacity_factor": 0.9, "site_fg_days": 105.0} | 19,631,858 (10,872) | 0.992 | 0.8166666666666667 | 15.81 |
| sodium_bicarbonate_8_4_50ml | S14 | infeasible_at_full_n | {"safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "capacity_factor": 1.05, "site_fg_days": 123.33333333333333} | 25,157,231 (9,669) | 0.996 | 0.85 | 20.17 |
| sodium_bicarbonate_8_4_50ml | S15 | infeasible | - | - | closest 0.915 | - | - |
| sodium_bicarbonate_8_4_50ml | S16 | optimal | {"safety_stock_days": 365.0, "activation_threshold_days": 61.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 16,717,481 (8,188) | 0.996 | 0.9166666666666666 | 13.40 |
| sodium_bicarbonate_8_4_50ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 45.0, "campaign_batches": 4.0} | 19,414,445 (4,874) | 0.996 | 0.9166666666666666 | 15.57 |
| sodium_bicarbonate_8_4_50ml | S18 | optimal | {"safety_stock_days": 187.5, "site_fg_days": 180.0, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,179,253 (10,812) | 0.997 | 0.9 | 19.36 |
| sodium_bicarbonate_8_4_50ml | S19 | infeasible | - | - | closest 0.890 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.99.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.99.png)

## Strategies optimized to a SENSITIVITY service target (tau = 0.98, q = 0.9)

Run `opt_20260906T054704Z_tau0.98`. Eligibility is NO_CONCLUSION for every strategy while gates are UNCERTAIN, so no favorable decision class can be assigned. This run varies the threshold as a pre-registered sensitivity; it does not replace the frozen target.

| Product | Strategy | Status | Best design | Mean annual cost [USD/yr] (MCSE) | Mean fill [fraction] | P(meet) | Cost per delivered unit [USD] |
|---|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 12,874,066 (16,253) | 0.989 | 0.9 | 13.86 |
| norepinephrine_1mgml_4ml | S1 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 12,874,066 (16,253) | 0.989 | 0.9 | 13.86 |
| norepinephrine_1mgml_4ml | S2 | optimal | {"capacity_factor": 0.6, "independent_api_supplier": 1.0, "safety_stock_days": 281.25, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 105.0} | 17,972,694 (8,252) | 0.994 | 0.9 | 19.25 |
| norepinephrine_1mgml_4ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 39.75, "campaign_batches": 3.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 5.0, "material_target_days": 30.0} | 17,207,554 (6,088) | 0.990 | 0.9166666666666666 | 18.51 |
| norepinephrine_1mgml_4ml | S4 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 30.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 180.0} | 20,229,672 (11,403) | 0.994 | 0.9 | 21.68 |
| norepinephrine_1mgml_4ml | S5 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 19,954,749 (14,413) | 0.993 | 0.9 | 21.38 |
| norepinephrine_1mgml_4ml | S6 | optimal | {"sites": 1.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 20,947,555 (14,413) | 0.993 | 0.9 | 22.45 |
| norepinephrine_1mgml_4ml | S7 | optimal | {"capacity_factor": 1.05, "safety_stock_days": 281.25, "region_base_stock": 0.0, "site_fg_days": 136.25, "material_target_days": 105.0} | 15,774,488 (14,022) | 0.993 | 0.9166666666666666 | 16.92 |
| norepinephrine_1mgml_4ml | S8 | optimal | {"safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "site_fg_days": 30.0, "material_target_days": 30.0} | 22,447,523 (6,804) | 0.995 | 0.9333333333333333 | 24.02 |
| norepinephrine_1mgml_4ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 113.75, "material_target_days": 71.875, "region_base_stock": 1.0} | 23,254,382 (5,188) | 0.996 | 0.9333333333333333 | 24.86 |
| norepinephrine_1mgml_4ml | S10 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 60.0, "material_target_days": 30.0} | 17,659,018 (8,105) | 0.991 | 0.9 | 18.97 |
| norepinephrine_1mgml_4ml | S11 | optimal | {"site_fg_days": 30.0, "safety_stock_days": 15.0, "region_base_stock": 1.0, "material_target_days": 30.0} | 15,142,909 (12,760) | 0.994 | 0.95 | 16.23 |
| norepinephrine_1mgml_4ml | S12 | optimal | {"capacity_factor": 0.8, "safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 18,498,695 (8,433) | 0.995 | 0.9 | 19.79 |
| norepinephrine_1mgml_4ml | S13 | optimal | {"safety_stock_days": 337.08333333333337, "region_base_stock": 0.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 18,607,277 (3,611) | 0.990 | 0.9333333333333333 | 20.00 |
| norepinephrine_1mgml_4ml | S14 | optimal | {"safety_stock_days": 141.66666666666669, "region_base_stock": 0.0, "capacity_factor": 1.05, "site_fg_days": 66.66666666666666} | 23,850,209 (7,754) | 0.994 | 0.9166666666666666 | 25.54 |
| norepinephrine_1mgml_4ml | S15 | infeasible_at_full_n | {"safety_stock_days": 197.5, "site_fg_days": 121.66666666666667, "material_target_days": 105.0, "region_base_stock": 0.0} | 12,837,970 (12,963) | 0.990 | 0.85 | 13.81 |
| norepinephrine_1mgml_4ml | S16 | optimal | {"safety_stock_days": 98.75, "activation_threshold_days": 46.5, "campaign_batches": 1.0, "region_base_stock": 1.0} | 15,922,905 (8,825) | 0.996 | 0.95 | 17.02 |
| norepinephrine_1mgml_4ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 3.0, "campaign_batches": 4.0} | 18,383,557 (3,862) | 0.997 | 0.9833333333333333 | 19.64 |
| norepinephrine_1mgml_4ml | S18 | optimal | {"safety_stock_days": 209.6875, "site_fg_days": 48.75, "material_target_days": 67.5, "region_base_stock": 0.0} | 22,746,490 (4,798) | 0.994 | 0.9166666666666666 | 24.35 |
| norepinephrine_1mgml_4ml | S19 | optimal | {"safety_stock_days": 92.8125, "material_target_days": 71.875, "activation_threshold_days": 10.0, "region_base_stock": 1.0} | 15,858,584 (10,143) | 0.992 | 0.9 | 17.04 |
| sodium_bicarbonate_8_4_50ml | S0 | infeasible | - | - | closest 0.925 | - | - |
| sodium_bicarbonate_8_4_50ml | S1 | infeasible | - | - | closest 0.925 | - | - |
| sodium_bicarbonate_8_4_50ml | S2 | optimal | {"capacity_factor": 1.0666666666666667, "independent_api_supplier": 0.0, "safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 25,459,686 (10,966) | 0.995 | 0.9666666666666667 | 20.42 |
| sodium_bicarbonate_8_4_50ml | S3 | optimal | {"reserved_capacity_fraction": 0.1, "activation_threshold_days": 39.75, "campaign_batches": 6.0, "safety_stock_days": 197.5, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 30.0} | 18,376,831 (10,997) | 0.993 | 0.9 | 14.78 |
| sodium_bicarbonate_8_4_50ml | S4 | optimal | {"capacity_factor": 1.0125000000000002, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 92.5, "material_target_days": 30.0} | 24,044,313 (19,533) | 0.998 | 0.95 | 19.23 |
| sodium_bicarbonate_8_4_50ml | S5 | optimal | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 31,976,051 (36,781) | 0.996 | 0.95 | 25.63 |
| sodium_bicarbonate_8_4_50ml | S6 | optimal | {"sites": 3.0, "node_scale": 0.15, "safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 180.0, "material_target_days": 67.5} | 33,703,487 (36,781) | 0.996 | 0.95 | 27.02 |
| sodium_bicarbonate_8_4_50ml | S7 | infeasible | - | - | closest 0.966 | - | - |
| sodium_bicarbonate_8_4_50ml | S8 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "site_fg_days": 105.0, "material_target_days": 105.0} | 23,660,733 (10,680) | 0.991 | 0.8666666666666667 | 19.06 |
| sodium_bicarbonate_8_4_50ml | S9 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 323.125, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,568,695 (16,115) | 0.997 | 0.9333333333333333 | 19.68 |
| sodium_bicarbonate_8_4_50ml | S10 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "site_fg_days": 60.0, "material_target_days": 30.0} | 18,635,950 (23,502) | 0.993 | 0.9166666666666666 | 14.98 |
| sodium_bicarbonate_8_4_50ml | S11 | infeasible_at_full_n | {"site_fg_days": 365.0, "safety_stock_days": 277.5, "region_base_stock": 0.0, "material_target_days": 67.5} | 15,907,046 (11,428) | 0.987 | 0.7833333333333333 | 12.87 |
| sodium_bicarbonate_8_4_50ml | S12 | optimal | {"capacity_factor": 1.0, "safety_stock_days": 365.0, "region_base_stock": 1.0, "fixed_cost_factor": 0.6} | 21,446,962 (22,881) | 0.997 | 0.9333333333333333 | 17.18 |
| sodium_bicarbonate_8_4_50ml | S13 | infeasible_at_full_n | {"safety_stock_days": 365.0, "region_base_stock": 1.0, "capacity_factor": 0.9, "site_fg_days": 30.0} | 19,618,962 (10,946) | 0.991 | 0.85 | 15.82 |
| sodium_bicarbonate_8_4_50ml | S14 | infeasible_at_full_n | {"safety_stock_days": 141.66666666666669, "region_base_stock": 1.0, "capacity_factor": 1.05, "site_fg_days": 95.0} | 25,101,612 (10,353) | 0.991 | 0.8333333333333334 | 20.22 |
| sodium_bicarbonate_8_4_50ml | S15 | infeasible | - | - | closest 0.915 | - | - |
| sodium_bicarbonate_8_4_50ml | S16 | infeasible_at_full_n | {"safety_stock_days": 365.0, "activation_threshold_days": 32.0, "campaign_batches": 1.0, "region_base_stock": 1.0} | 16,656,987 (7,946) | 0.991 | 0.8666666666666667 | 13.42 |
| sodium_bicarbonate_8_4_50ml | S17 | optimal | {"safety_stock_days": 365.0, "region_base_stock": 0.0, "activation_threshold_days": 45.0, "campaign_batches": 1.0} | 19,368,991 (6,453) | 0.992 | 0.9 | 15.60 |
| sodium_bicarbonate_8_4_50ml | S18 | infeasible_at_full_n | {"safety_stock_days": 276.25, "site_fg_days": 63.333333333333336, "material_target_days": 30.0, "region_base_stock": 1.0} | 24,134,342 (10,778) | 0.994 | 0.8666666666666667 | 19.39 |
| sodium_bicarbonate_8_4_50ml | S19 | infeasible | - | - | closest 0.890 | - | - |

![frontier](results/figures/frontier_norepinephrine_1mgml_4ml_tau0.98.png)


![frontier](results/figures/frontier_sodium_bicarbonate_8_4_50ml_tau0.98.png)

## Paired simulation (baseline illustrative designs, not optimized)

100 common-random-number runs per strategy. Paired differences vs S0 with Monte Carlo standard errors:

| Product | Strategy | d cost/unit [USD] | d fill [fraction] | d shortage days [d/yr] |
|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S1 | +0.05 (0.02) | -0.010 (0.001) | +45.5 (1.3) |
| norepinephrine_1mgml_4ml | S10 | +4.72 (0.05) | +0.038 (0.003) | -39.2 (2.1) |
| norepinephrine_1mgml_4ml | S11 | +2.35 (0.06) | +0.052 (0.004) | -62.7 (2.6) |
| norepinephrine_1mgml_4ml | S12 | +9.48 (0.05) | +0.039 (0.004) | -38.9 (2.1) |
| norepinephrine_1mgml_4ml | S13 | +7.19 (0.06) | +0.053 (0.004) | -63.1 (2.6) |
| norepinephrine_1mgml_4ml | S14 | +11.29 (0.05) | +0.049 (0.004) | -60.7 (2.4) |
| norepinephrine_1mgml_4ml | S15 | -0.44 (0.05) | +0.045 (0.003) | -57.9 (2.0) |
| norepinephrine_1mgml_4ml | S16 | +2.82 (0.06) | +0.046 (0.004) | -57.6 (2.3) |
| norepinephrine_1mgml_4ml | S17 | +6.28 (0.07) | +0.053 (0.004) | -63.1 (2.6) |
| norepinephrine_1mgml_4ml | S18 | +10.22 (0.06) | +0.052 (0.004) | -62.3 (2.6) |
| norepinephrine_1mgml_4ml | S19 | +2.78 (0.04) | +0.043 (0.003) | -56.4 (2.2) |
| norepinephrine_1mgml_4ml | S2 | +13.17 (0.06) | +0.041 (0.003) | -45.4 (2.4) |
| norepinephrine_1mgml_4ml | S3 | +6.39 (0.04) | +0.029 (0.003) | -10.1 (2.0) |
| norepinephrine_1mgml_4ml | S4 | +15.25 (0.05) | +0.035 (0.003) | -31.8 (2.1) |
| norepinephrine_1mgml_4ml | S5 | +32.39 (0.10) | +0.032 (0.003) | -35.0 (2.2) |
| norepinephrine_1mgml_4ml | S6 | +34.85 (0.10) | +0.032 (0.003) | -35.0 (2.2) |
| norepinephrine_1mgml_4ml | S7 | +4.82 (0.03) | +0.008 (0.001) | -15.9 (1.1) |
| norepinephrine_1mgml_4ml | S8 | +9.67 (0.05) | +0.046 (0.003) | -58.6 (2.4) |
| norepinephrine_1mgml_4ml | S9 | +13.17 (0.06) | +0.044 (0.004) | -57.5 (2.5) |
| sodium_bicarbonate_8_4_50ml | S1 | -0.07 (0.02) | +0.000 (0.001) | +0.6 (0.4) |
| sodium_bicarbonate_8_4_50ml | S10 | +1.78 (0.04) | +0.182 (0.002) | -130.5 (3.6) |
| sodium_bicarbonate_8_4_50ml | S11 | -1.18 (0.04) | +0.239 (0.002) | -207.2 (2.7) |
| sodium_bicarbonate_8_4_50ml | S12 | +5.54 (0.05) | +0.189 (0.002) | -139.9 (2.6) |
| sodium_bicarbonate_8_4_50ml | S13 | +2.27 (0.06) | +0.273 (0.003) | -258.6 (1.3) |
| sodium_bicarbonate_8_4_50ml | S14 | +6.37 (0.06) | +0.231 (0.003) | -220.2 (0.9) |
| sodium_bicarbonate_8_4_50ml | S15 | -0.68 (0.04) | +0.043 (0.002) | -64.2 (2.2) |
| sodium_bicarbonate_8_4_50ml | S16 | +0.02 (0.05) | +0.194 (0.003) | -185.6 (1.0) |
| sodium_bicarbonate_8_4_50ml | S17 | +1.25 (0.06) | +0.277 (0.003) | -263.5 (0.7) |
| sodium_bicarbonate_8_4_50ml | S18 | +5.81 (0.07) | +0.217 (0.004) | -206.6 (1.6) |
| sodium_bicarbonate_8_4_50ml | S19 | +2.10 (0.04) | +0.066 (0.002) | -57.5 (1.3) |
| sodium_bicarbonate_8_4_50ml | S2 | +7.80 (0.06) | +0.228 (0.003) | -207.3 (0.9) |
| sodium_bicarbonate_8_4_50ml | S3 | +2.04 (0.04) | +0.250 (0.002) | -190.0 (1.4) |
| sodium_bicarbonate_8_4_50ml | S4 | +9.56 (0.06) | +0.216 (0.003) | -176.5 (1.1) |
| sodium_bicarbonate_8_4_50ml | S5 | +26.13 (0.08) | +0.145 (0.003) | -136.4 (0.7) |
| sodium_bicarbonate_8_4_50ml | S6 | +28.22 (0.08) | +0.145 (0.003) | -136.4 (0.7) |
| sodium_bicarbonate_8_4_50ml | S7 | +3.84 (0.08) | +0.052 (0.004) | -17.3 (0.9) |
| sodium_bicarbonate_8_4_50ml | S8 | +5.24 (0.06) | +0.224 (0.003) | -214.0 (0.6) |
| sodium_bicarbonate_8_4_50ml | S9 | +7.95 (0.06) | +0.225 (0.003) | -214.8 (0.8) |

## Sensitivity and value of information

Product sodium_bicarbonate_8_4_50ml; designs from optimization run opt_20260902T043854Z; 6 runs per scenario.

Inputs whose sweep changes the preferred strategy: ['capacity_utilization', 'release_time', 'yield', 'uptime', 'demand_cv', 'common_cause_dependence', 'batch_size', 'changeover_burden', 'deviation_rejection_rate', 'site_failure_rate', 'investigation_duration']

| Input | Sobol total-order index |
|---|---|
| capacity_utilization | 0.000 |
| release_time | 0.000 |
| fixed_qa_labor_per_node | 0.114 |
| demand_cv | 0.000 |
| raw_material_lead_time | 0.000 |
| common_cause_dependence | 0.000 |
| shelf_life | 0.000 |
| node_scale | 0.859 |

EVPI on annual cost: 4,757,494 USD/yr. EVPPI by input: capacity_utilization 1,016,954, release_time 0, fixed_qa_labor_per_node 0, demand_cv 0, raw_material_lead_time 1,477,355, common_cause_dependence 1,150,473, shelf_life 0, node_scale 0

![feasibility map](results/figures/feasibility_map.png)

![tornado](results/figures/tornado_S5.png)

## Backcasts

| Episode | Observed | Simulated longest episode [d] | Consistent | Bottleneck (sim vs observed) | Mismatches |
|---|---|---|---|---|---|
| sodium_bicarbonate_2017_ongoing | >= 3472 d, ongoing | 1826 | True | capacity below demand (chronic) vs Demand increase for the drug; Discontinuation of the manufacture of the drug; Other | none |
| furosemide_2020_ongoing | >= 2339 d, ongoing | 1826 | True | capacity below demand (chronic) vs Demand increase for the drug; Discontinuation of the manufacture of the drug; Other; Requirements related to complying with good manufacturing practices; Shortage of an inactive ingredient component | none |
| sterile_water_2021_ongoing | >= 1744 d, ongoing | 1826 | True | capacity below demand (chronic) vs Demand increase for the drug; Discontinuation of the manufacture of the drug; Other | none |
| site_failure_template | not documented | - | - | - | episode not yet documented from primary sources |

## Design-space strategies (S8+)

Added by the 2026-09 design-space assignment. S0-S7 are unchanged and are guarded by `tests/regression/test_frozen_strategies.py`. Gate status is UNCERTAIN for every strategy, so none can receive a favorable decision class.

| Strategy | Name | Family | Sites | Pathway | Durable | Regulatory owner | Falsification test |
|---|---|---|---|---|---|---|---|
| S8 | Acquired registered line, two sites, split API and geography | telo_architectures | central, second_source | approved_cmo | True | Telo, as ANDA holder, for both sites. Each site holds its own establishment registration under 21 CFR Part 207 as it stands today. No distributed-establishment instrument is used, so nothing here depends on the DME proposed rule (F1-S01). | External: ask three owners of currently inspected US aseptic fill lines for an asking price and a realistic date for adding the line to an existing ANDA. The architecture fails if the price per unit of annual capacity is not materially below the 132M USD new-line-and-building anchor (F1-S51), or if the date is not materially inside node_commissioning_days (730 d). Internal: run this design against frozen S2 and S4 at n = 100 with matched inventory variables; if the fill advantage over S2 is inside the paired MCSE, this is dual sourcing relabelled, not an architecture. Commercial: if no GPO or IDN will sign a multi-year committed volume at or above the modelled break-even price, ContractTerms stays incomplete and the architecture is reported as not contractable. |
| S9 | Dual finished-dose source with an explicit key-starting-material tier | upstream_first | central, second_source | approved_cmo | True | The ANDA holder for both sites. Adding the second site is a prior approval supplement under 21 CFR 314.70(b)(2)(iii); a facility not in the original ANDA defaults to the inspection path, which is the 10-month GDUFA III clock (F9-S11, F9-S12). Gate G07 governs. | Run the matched-membership control: an identical design in which cc_ksm_api_1 is split into cc_ksm_api_1 (central, api_src_a) and cc_ksm_api_2 (second_source, api_src_b), so the group count is unchanged and only the sharing differs. If p_meet is unchanged inside its binomial standard error, the key-starting-material tier does not matter in this model and USP's concentration finding is irrelevant to the engine. If the shared version fails where the split version passes, then every dual-sourcing result in the package was produced by an unrepresented correlation and must be restated. |
| S10 | Split tenancy across two independent multi-product hosts | multi_product_portfolio | central, shared_suite_1, shared_suite_2 | approved_cmo | True | Telo holds the application and lists both sites. Two site additions means two change-control packages under 21 CFR 314.70 and two facility evaluations, both UNCERTAIN under gate G07 (F6-R02, F3-S44, F3-S45). Woodcock and Wosinska found only 11 of about 900 sterile-injectable ANDAs approved 2000-2011 referenced more than one finished-dose facility, so a deliberately two-sited generic is unusual (F6-S37). | Run the paired comparison against a single-host control at matched chronic capacity. The control is an internal variant of this design, not a separate configured strategy: collapse shared_suite_1 and shared_suite_2 into one host in R3 at portfolio_capacity_share 0.4, portfolio_fixed_cost_share 0.4 and validation_multiplier 2.5 (so it pays exactly one full product-specific validation), keeping central, the suppliers, the group declarations and every design variable identical, so both arms add 0.40 nominal-site-equivalents. The earlier wording named an anchor-tenancy sibling strategy that is not configured anywhere and the test was therefore untestable as written. If p_meet does not improve, the second quality-unit share and the second full validation buy nothing and concentration wins. Then run the decisive ablation: move shared_suite_2 back to api_supplier api_1 with group cc_api_1. If the advantage disappears, the mechanism was API independence, not site independence, and this belongs to family 9. Evidence-side: if no second US host will take a 20 percent tenancy of a full line for a low-price generic, the architecture has no counterparties; the base rate is about 1 percent of sterile-injectable ANDAs (F6-S37). |
| S11 | Bright-stock campaign offtake with a national undifferentiated reserve | postponement | central, reserved_cdmo | approved_cmo | True | The ANDA or NDA holder remains the application owner (G01). Telo is either that holder or its contract labeler and relabeler; 21 CFR 207.1 defines relabel and relabeler and folds contract packers and contract labelers into manufacturer, so Telo's finishing operation registers and lists in its own right (F5-S12). Whether Telo registers as relabeler or as contract manufacturer is UNCERTAIN (F5 section 5). | Run a capacity-matched control with the same reserved_cdmo line and the same exercise cadence, but with site_fg_days at its low bound, safety_stock_days high, delivery_days 5 (no finish penalty) and region_base_stock 0 (frozen review rule). If this design does not beat that control on mean fill and on p_meet by more than the MCSE at n = 100, the postponement content is zero and the whole gain is the campaign offtake, which belongs to family 7 or 8, not here. Evidence kill: ask a named CDMO whether it will sell filled, capped, cap-coded, unlabeled units to a third-party labeler under a campaign supply agreement, and at what minimum campaign size and term. A no from two of three CDMOs kills the architecture regardless of what the model says. |
| S12 | Contracted registered-capacity supply base | virtual_network | central, second_source, cdmo_r2 | approved_cmo | True | Telo as ANDA or NDA holder, or Telo as labeler under a partner ANDA. G01 is UNCERTAIN either way. The distributed-manufacturing-establishment registration route is not available: the proposed rule requires one management and a single quality unit and the repository reads it as excluding unaffiliated contract manufacturers (F3-R4), a secondary read that stays UNCERTAIN until counsel checks the affiliation language. | Model test: run this candidate against frozen S2 (dual source, the only strategy that cleared at tau 0.98 pre-R004) on the post-R004/R005 battery under matched design variables. If it does not reach S2's p_meet at a lower annual cost for both products, it adds nothing over dual sourcing and is dropped. Evidence test, outside the model: if no candidate US partner already fills a similar approved presentation in the same container type with a satisfactory CGMP inspection for that operation, every site-product pair is a prior-approval supplement with a possible pre-approval inspection (F3-S45 VI.A, VI.B.1, VI.B.2, VI.B.4) and the 365-day leg does not exist, which removes the family's central advantage over building. |
| S13 | Contracted base supply plus rotated reserved surge plus reserve inventory | virtual_network | central, second_source, reserved_cdmo | approved_cmo | True | Telo as application holder or labeler; each site-product pair in the application before it can supply. The DME route is unavailable to an unaffiliated network (F3-R4). | Ablate the three legs one at a time on the post-R004/R005 battery, matched design variables, both products. If removing the rotated reserved surge leaves p_meet inside its binomial standard error, the family's distinctive leg does nothing and this candidate collapses into frozen S2 plus frozen S1, which are already comparators and cheaper to explain. If removing the firm second source does the same, the whole architecture is an inventory strategy and should be reported as one. Evidence tests: the F3-S45 site-change reading for a real partner list, and whether a comparability protocol naming an alternate aseptic site for a generic sterile injectable has ever been accepted (F3-S46, F9-S37, prior-art review open question 2). |
| S14 | Cooperative-financed registered second source with committed offtake | public_private | central, second_source | approved_cmo | True | Telo or the cooperative holds or is named in the ANDA. The acquired site enters the application through a site-transfer supplement under 21 CFR 314.70, category and duration unresolved (G07). | Commercial: compute minimum_contracted_utilization for the acquired site at a price a GPO will state in writing. If the committed share needed to cover fixed and resilience cost exceeds the share the cooperative will commit, or exceeds 1.0 of saleable capacity, the architecture is dead at that price. Regulatory: a qualified reviewer states the reporting category and expected duration of the site-transfer supplement for an acquired registered plant. If it is not materially below node_commissioning_days of 730, this collapses into the same commissioning failure as the build architectures and should be dropped in favour of S2 with a contract attached. |
| S15 | Capacity-adequate buffer-payable presentation (inventory-first, no new plant) | product_selection | central | approved_cmo | True | The existing application holder; Telo is not a manufacturer here. The gate mapping still assigns G01-G07 because the architecture depends entirely on the incumbent's application, registration, validation and stability state, none of which Telo controls. | Modelling: run against S1 and S0 under matched bounds with region_base_stock forced to 0. If the advantage disappears when the review rule reverts to the frozen one, the whole result is MD-3 and the architecture has no content beyond a model artifact. Commercial: ask three eligible hospitals (100 beds or fewer, not part of a chain) whether their cost report would accept a Telo-held buffer as a contractual arrangement with an intermediary under 42 CFR 412.113(g), and what they would pay for the service. A no on either kills the revenue mechanism while leaving the inventory result intact as an argument for someone else's balance sheet. |
| S16 | Reserve-triggered campaign network on contracted registered capacity | inventory_capacity_hybrids | central, reserved_cdmo, reserved_cdmo_b | approved_cmo | True | The ANDA holder, whether that is Telo or a partner; each contracted line has to be named in the application before it can make commercial product (G01, G02, G07). All three are UNCERTAIN, so the 540-day lead is a placeholder for a regulatory duration nobody has confirmed, not an approval. | In the model, after the R004 and R005 re-runs: if this architecture at its best searched design does not beat frozen S3 on p_meet by more than two binomial standard errors at matched annual cost, the trigger-plus-exercise coupling adds nothing and the architecture collapses to S3. A second, sharper test: set exercise_batches_per_year to 0 and re-run; if service and cost are unchanged except for the removed exercise output, the readiness claim is untestable in the engine as it stands. In the world: a GPO, nonprofit or government contract in which reserve depletion below a stated threshold triggers a pre-qualified campaign at a named site would move the sub-idea from novel_combination to already_implemented (F8 section 7, row 5). |
| S17 | Rotating prequalified campaign network across three registered CMO fill lines | warm_standby | central, cmo_R2, cmo_R3, cmo_R4 | approved_cmo | True | One application holder. Every contracted line must be named in the approved application before t0; this is the decisive design choice in the family, because a site added at activation carries a supplement review and possibly a preapproval inspection and then shortens nothing (F7-S14, F7-S31). | Three tests, any one of which kills it. (a) Regulatory: a qualified CMC reviewer states the reporting category for adding a third-party sterile fill-finish site to an approved ANDA, and whether any approved ANDA lists three or more US sterile fill sites for one presentation (needs Module 3.2.P.3 tables that are not public). If the answer is prior-approval supplement with preapproval inspection at each site, the architecture is dominated by simply expanding the incumbent plant. (b) Commercial: a named CMO quotes four campaigns per year with a priority call. If no CMO will sell allocation rights at any price, the design has no supply side. (c) Model: rerun with exercise_batches_per_year = 0 at all three lines, and separately move activation_failure_probability across its range. If fill moves with the exercise volume and not with the failure probability, the mechanism is production volume rather than readiness and the architecture must be re-justified as distributed routine contracted supply rather than as standby. |
| S18 | Dual committed supply with contract-mandated distinct API and container sources | contracts_procurement | central, second_source | approved_cmo | True | Each partner ANDA holder. Adding a second container-closure system is a stability and container-closure change on the holder's application, not a labeling change. | Structural: run head to head against frozen S2 with independent_api_supplier = 1 at matched service after the R004 and R005 re-runs, then re-run with second_source moved back onto vial_1 (dropping cc_vial_2). If the tail probability does not move by more than the binomial standard error on p_meet that MD-16 now reports, contract-mandated container independence buys nothing measurable and the architecture collapses into S2 with extra validation cost. A second ablation drops the supplier-held buffer (site_fg_days to 30, material_target_days to 60) to separate the source-independence effect from the inventory effect. Commercial: the only quantified failure-to-supply result is conditional on a 30 percent price increase travelling with it (F10-S33), so the architecture is falsified commercially if no purchaser will pay that increase. |
| S19 | Maintained alternate-source switching package with an exercised standby line | upstream_first | central, second_source | approved_cmo | True | The ANDA holder. Telo holds no application. The switching package is filed by the holder as a comparability protocol under 21 CFR 314.70(e), synonymous with an ICH Q12 PACMP (F9-S8, F9-S13, F9-S37). Telo prepares and maintains it and the validation data behind it. Gate G07 governs and stays UNCERTAIN. | Run three paired designs identical except for second_source.activation_lead_days at 386, 201 and 51 days, each the sum of a regulatory clock and the engine's reserved_capacity_activation_days base of 21 (365 = second_source_qualification_days base; 180 = the GDUFA III standard PAS clock without an inspection, F9-S11; 30 = CBE-30 under an approved comparability protocol, F9-S37). If the difference in p_meet at the frozen tail requirement is inside its binomial standard error at the run count used, the switching package is worth nothing in this model and the architecture dies. Secondary: split cc_ksm_api_1 into two groups with the same group count and different membership; if service is unchanged, the honest upstream correlation is not load-bearing. Tertiary, external and decisive for novelty: a single published comparability protocol pre-authorising an alternate aseptic site or API supplier for a generic sterile injectable moves the classification to already_implemented. |

## Failure decomposition by ablation (run `abl_post_R004`)

100 common-random-number runs per configuration; designs optimized:opt_20260903T181601Z; tau = 0.99, q = 0.9. Status-quo utilization: sodium_bicarbonate_8_4_50ml 1.24, norepinephrine_1mgml_4ml 0.78. A mechanism binds when switching it off alone raises the tail probability.

| Product | Strategy | base fill | base P(meet) | quiet fill | mechanisms that raise P(meet) by >= 0.05 when removed |
|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | 0.983 | 0.56 | 1.000 | inventory_timing (+0.34), site_failures (+0.24), lost_sales_window (+0.20), common_cause (+0.19), sterility_delay (+0.10), material_buffer (+0.10), supplier_concentration (+0.08), release_queue (+0.07), demand_covariance (+0.07), surge_headroom (+0.06) |
| norepinephrine_1mgml_4ml | S1 | 0.985 | 0.65 | 1.000 | inventory_timing (+0.29), site_failures (+0.20), lost_sales_window (+0.13), common_cause (+0.11) |
| norepinephrine_1mgml_4ml | S2 | 0.993 | 0.84 | 1.000 | lost_sales_window (+0.11), commissioning_delay (+0.11), inventory_timing (+0.09), site_failures (+0.08), common_cause (+0.08), horizon_10y (+0.07), sterility_delay (+0.06), capacity_shortfall (+0.06) |
| norepinephrine_1mgml_4ml | S3 | 0.994 | 0.93 | 1.000 | contract_insufficiency (+0.06) |
| norepinephrine_1mgml_4ml | S4 | 0.992 | 0.81 | 1.000 | commissioning_delay (+0.18), inventory_timing (+0.17), lost_sales_window (+0.12), site_failures (+0.10), supplier_concentration (+0.07), sterility_delay (+0.07), material_buffer (+0.07), horizon_10y (+0.07), common_cause (+0.06) |
| norepinephrine_1mgml_4ml | S5 | 0.990 | 0.72 | 1.000 | commissioning_delay (+0.27), supplier_concentration (+0.11), material_buffer (+0.11), site_failures (+0.09), lost_sales_window (+0.08), common_cause (+0.06), horizon_10y (+0.05) |
| norepinephrine_1mgml_4ml | S6 | 0.990 | 0.72 | 1.000 | commissioning_delay (+0.27), supplier_concentration (+0.11), material_buffer (+0.11), site_failures (+0.09), lost_sales_window (+0.08), common_cause (+0.06), horizon_10y (+0.05) |
| norepinephrine_1mgml_4ml | S7 | 0.957 | 0.21 | 1.000 | regulatory_unavailability (+0.73), lost_sales_window (+0.27), inventory_timing (+0.26), supplier_concentration (+0.14), material_buffer (+0.14), sterility_delay (+0.10), site_failures (+0.10), common_cause (+0.07) |
| sodium_bicarbonate_8_4_50ml | S0 | 0.721 | 0.00 | 1.000 | capacity_shortfall (+0.15) |
| sodium_bicarbonate_8_4_50ml | S1 | 0.755 | 0.00 | 1.000 | capacity_shortfall (+0.32) |
| sodium_bicarbonate_8_4_50ml | S2 | 0.991 | 0.80 | 1.000 | capacity_shortfall (+0.18), lost_sales_window (+0.15), commissioning_delay (+0.11), site_failures (+0.09), common_cause (+0.08), sterility_delay (+0.07), inventory_timing (+0.07) |
| sodium_bicarbonate_8_4_50ml | S3 | 0.993 | 0.86 | 1.000 | lost_sales_window (+0.11), inventory_timing (+0.11), contract_insufficiency (+0.11), sterility_delay (+0.08), site_failures (+0.08), supplier_concentration (+0.06), material_buffer (+0.06) |
| sodium_bicarbonate_8_4_50ml | S4 | 0.987 | 0.72 | 1.000 | commissioning_delay (+0.27), site_failures (+0.09), supplier_concentration (+0.08), material_buffer (+0.08), horizon_10y (+0.08), capacity_shortfall (+0.08), lost_sales_window (+0.05) |
| sodium_bicarbonate_8_4_50ml | S5 | 0.932 | 0.00 | 1.000 | commissioning_delay (+0.99), capacity_shortfall (+0.80) |
| sodium_bicarbonate_8_4_50ml | S6 | 0.932 | 0.00 | 1.000 | commissioning_delay (+0.99), capacity_shortfall (+0.80) |
| sodium_bicarbonate_8_4_50ml | S7 | 0.868 | 0.19 | 1.000 | regulatory_unavailability (+0.76), capacity_shortfall (+0.26), inventory_timing (+0.10) |

![ablation heatmap](results/figures/ablation_abl_post_R004_norepinephrine_1mgml_4ml_heatmap_p_meet.png)

![ablation heatmap](results/figures/ablation_abl_post_R004_sodium_bicarbonate_8_4_50ml_heatmap_p_meet.png)

### Interaction study (run `abl_20260902_phaseA_pairs`)

Mechanisms switched off together. A strategy that clears the target only when two mechanisms are removed is limited by both, and one that clears with either is limited by whichever is cheaper to fix.

| Configuration | Product | S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 |
|---|---|---|---|---|---|---|---|---|---|
| base | sodium_bicarbonate_8_4_50ml | 0.00 | 0.00 | 0.89 | 0.86 | 0.79 | 0.00 | 0.00 | 0.19 |
| base | norepinephrine_1mgml_4ml | 0.56 | 0.65 | 0.84 | 0.86 | 0.86 | 0.72 | 0.72 | 0.21 |
| capacity_shortfall+inventory_timing | sodium_bicarbonate_8_4_50ml | 0.64 | 0.97* | 0.99* | 0.99* | 0.98* | 0.87 | 0.87 | 0.84 |
| capacity_shortfall+inventory_timing | norepinephrine_1mgml_4ml | 0.91* | 0.95* | 0.93* | 0.94* | 0.98* | 0.77 | 0.77 | 0.49 |
| capacity_shortfall+commissioning_delay | sodium_bicarbonate_8_4_50ml | 0.42 | 0.50 | 0.99* | 0.88 | 1.00* | 0.99* | 0.99* | 0.45 |
| capacity_shortfall+commissioning_delay | norepinephrine_1mgml_4ml | 0.59 | 0.64 | 0.95* | 0.88 | 0.99* | 0.99* | 0.99* | 0.22 |
| inventory_timing+commissioning_delay | sodium_bicarbonate_8_4_50ml | 0.00 | 0.00 | 0.99* | 0.95* | 0.99* | 0.99* | 0.99* | 0.29 |
| inventory_timing+commissioning_delay | norepinephrine_1mgml_4ml | 0.90* | 0.94* | 0.99* | 0.94* | 1.00* | 0.99* | 0.99* | 0.47 |
| capacity_shortfall+inventory_timing+commissioning_delay | sodium_bicarbonate_8_4_50ml | 0.64 | 0.97* | 0.99* | 0.99* | 0.99* | 0.99* | 0.99* | 0.84 |
| capacity_shortfall+inventory_timing+commissioning_delay | norepinephrine_1mgml_4ml | 0.91* | 0.95* | 0.99* | 0.94* | 1.00* | 0.99* | 0.99* | 0.49 |

Cells are P(fill >= tau); an asterisk marks a configuration that meets both the mean and the tail requirement.

## Feasibility conditions and dominance (run `ds_post_R009`)

Bisection over 5 steps on 20 paired runs per input; dominance on 40 paired runs at tau = 0.99, q = 0.9. A condition is stated only where feasibility changes inside the input's recorded low-to-high range.

| Product | Strategy | Mean cost [USD/yr] | Mean fill | P(meet) | Meets target | Dominated by |
|---|---|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | 12,928,698 | 0.996 | 0.93 | True | S15 |
| norepinephrine_1mgml_4ml | S1 | 12,928,698 | 0.996 | 0.93 | True | S15 |
| norepinephrine_1mgml_4ml | S2 | 18,032,783 | 0.999 | 0.95 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S3 | 17,492,925 | 0.996 | 0.93 | True | S15;S16;S7 |
| norepinephrine_1mgml_4ml | S4 | 20,181,579 | 0.996 | 0.93 | True | S11;S13;S15;S16;S17;S2;S3;S5;S7 |
| norepinephrine_1mgml_4ml | S5 | 20,063,580 | 0.998 | 0.97 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S6 | 21,056,386 | 0.998 | 0.97 | True | S5 |
| norepinephrine_1mgml_4ml | S7 | 15,847,847 | 0.997 | 0.95 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S8 | 22,431,137 | 0.997 | 0.90 | True | S13;S15;S16;S17;S2;S5;S6;S7 |
| norepinephrine_1mgml_4ml | S9 | 23,276,894 | 0.997 | 0.90 | True | S13;S15;S16;S17;S2;S5;S6 |
| norepinephrine_1mgml_4ml | S10 | 17,755,950 | 0.994 | 0.88 | False | S0;S1;S11;S15;S16;S19;S3;S7 |
| norepinephrine_1mgml_4ml | S11 | 15,162,396 | 0.996 | 0.95 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S12 | 18,538,581 | 0.996 | 0.88 | False | S15;S16;S17;S2;S3;S7 |
| norepinephrine_1mgml_4ml | S13 | 18,799,933 | 0.998 | 0.95 | True | S16;S2 |
| norepinephrine_1mgml_4ml | S14 | 23,887,778 | 0.997 | 0.90 | True | S13;S15;S16;S17;S2;S5;S6;S9 |
| norepinephrine_1mgml_4ml | S15 | 12,885,420 | 0.998 | 0.93 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S16 | 16,006,112 | 0.998 | 0.95 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S17 | 18,389,486 | 0.997 | 1.00 | True | none (on the frontier) |
| norepinephrine_1mgml_4ml | S18 | 22,807,279 | 0.993 | 0.78 | False | S0;S1;S10;S11;S12;S13;S15;S16;S17;S19;S2;S3;S4;S5;S6;S7;S8 |
| norepinephrine_1mgml_4ml | S19 | 15,896,741 | 0.996 | 0.93 | True | S11;S15;S7 |
| sodium_bicarbonate_8_4_50ml | S0 | 13,417,427 | 0.923 | 0.00 | False | none (on the frontier) |
| sodium_bicarbonate_8_4_50ml | S1 | 13,417,427 | 0.923 | 0.00 | False | none (on the frontier) |
| sodium_bicarbonate_8_4_50ml | S2 | 24,004,187 | 0.995 | 0.85 | False | S11;S12;S16;S17;S3 |
| sodium_bicarbonate_8_4_50ml | S3 | 18,498,913 | 0.997 | 0.95 | True | S11;S16 |
| sodium_bicarbonate_8_4_50ml | S4 | 24,059,938 | 0.998 | 0.95 | True | S11 |
| sodium_bicarbonate_8_4_50ml | S5 | 32,024,370 | 0.997 | 0.88 | False | S11;S16;S3;S4;S9 |
| sodium_bicarbonate_8_4_50ml | S6 | 33,751,807 | 0.997 | 0.88 | False | S11;S16;S3;S4;S5;S9 |
| sodium_bicarbonate_8_4_50ml | S7 | 16,570,717 | 0.966 | 0.35 | False | S11 |
| sodium_bicarbonate_8_4_50ml | S8 | 23,672,661 | 0.991 | 0.80 | False | S10;S11;S12;S13;S16;S17;S3 |
| sodium_bicarbonate_8_4_50ml | S9 | 24,636,340 | 0.999 | 0.97 | True | none (on the frontier) |
| sodium_bicarbonate_8_4_50ml | S10 | 18,753,188 | 0.995 | 0.93 | True | S11;S16;S3 |
| sodium_bicarbonate_8_4_50ml | S11 | 16,119,916 | 0.998 | 0.95 | True | none (on the frontier) |
| sodium_bicarbonate_8_4_50ml | S12 | 21,462,545 | 0.996 | 0.93 | True | S11;S16;S17;S3 |
| sodium_bicarbonate_8_4_50ml | S13 | 19,645,936 | 0.994 | 0.88 | False | S10;S11;S16;S17;S3 |
| sodium_bicarbonate_8_4_50ml | S14 | 25,164,748 | 0.996 | 0.85 | False | S11;S12;S16;S17;S3;S4;S9 |
| sodium_bicarbonate_8_4_50ml | S15 | 13,386,952 | 0.914 | 0.00 | False | none (on the frontier) |
| sodium_bicarbonate_8_4_50ml | S16 | 16,724,488 | 0.998 | 0.95 | True | S11 |
| sodium_bicarbonate_8_4_50ml | S17 | 19,420,920 | 0.996 | 0.93 | True | S11;S16;S3 |
| sodium_bicarbonate_8_4_50ml | S18 | 24,172,177 | 0.996 | 0.85 | False | S11;S12;S16;S17;S3;S4 |
| sodium_bicarbonate_8_4_50ml | S19 | 16,363,619 | 0.893 | 0.00 | False | S0;S1;S11;S15 |

| Product | Strategy | Input | Condition | Recorded range |
|---|---|---|---|---|
| norepinephrine_1mgml_4ml | S0 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.05e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S0 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 16.8 | 12 to 30 |
| norepinephrine_1mgml_4ml | S0 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S0 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S0 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S1 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.05e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S1 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 16.8 | 12 to 30 |
| norepinephrine_1mgml_4ml | S1 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S1 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S1 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S2 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.67e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S2 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 105 | 30 to 240 |
| norepinephrine_1mgml_4ml | S2 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S2 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S3 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.05e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S3 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 125 | 30 to 240 |
| norepinephrine_1mgml_4ml | S3 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.156 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S3 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.282 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S3 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S3 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S4 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.67e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S4 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 145 | 30 to 240 |
| norepinephrine_1mgml_4ml | S4 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.191 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S4 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.557 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S4 | commissioning_days (global.node_commissioning_days) | feasible while commissioning_days <= 924 | 365 to 1.1e+03 |
| norepinephrine_1mgml_4ml | S4 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S4 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 9.58 | 1 to 10 |
| norepinephrine_1mgml_4ml | S5 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.27e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S5 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 19.6 | 12 to 30 |
| norepinephrine_1mgml_4ml | S5 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 40.6 | 30 to 70 |
| norepinephrine_1mgml_4ml | S5 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S6 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.27e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S6 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 19.6 | 12 to 30 |
| norepinephrine_1mgml_4ml | S6 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 40.6 | 30 to 70 |
| norepinephrine_1mgml_4ml | S6 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S7 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.05e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S7 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 17.3 | 12 to 30 |
| norepinephrine_1mgml_4ml | S7 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.182 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S7 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S7 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S8 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 6.42e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S8 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 85.8 | 30 to 240 |
| norepinephrine_1mgml_4ml | S8 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0856 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S8 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.11 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S8 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 49.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S9 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 6.42e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S9 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0681 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S9 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 51.9 | 30 to 70 |
| norepinephrine_1mgml_4ml | S10 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.01e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S10 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 12.3 | 12 to 30 |
| norepinephrine_1mgml_4ml | S10 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.138 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S10 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.385 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S10 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S10 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S11 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.01e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S11 | release_time (global.sterility_incubation_days) | feasible while release_time <= 17.2 | 14 to 18 |
| norepinephrine_1mgml_4ml | S11 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.138 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S11 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.488 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S11 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 38.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S11 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| norepinephrine_1mgml_4ml | S12 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 8.86e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S12 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0681 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S12 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.557 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S12 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 48.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S13 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.05e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S13 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.138 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S13 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 38.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S14 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 6.83e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S14 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0769 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S14 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.162 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S14 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 50.6 | 30 to 70 |
| norepinephrine_1mgml_4ml | S15 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.67e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S15 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 15.7 | 12 to 30 |
| norepinephrine_1mgml_4ml | S15 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.156 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S15 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.488 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S15 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 39.4 | 30 to 70 |
| norepinephrine_1mgml_4ml | S15 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S16 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.01e+06 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S16 | release_time (global.sterility_incubation_days) | feasible while release_time <= 17.9 | 14 to 18 |
| norepinephrine_1mgml_4ml | S16 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 105 | 30 to 240 |
| norepinephrine_1mgml_4ml | S16 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.182 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S16 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.385 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S16 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S16 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| norepinephrine_1mgml_4ml | S17 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.27e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S17 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 8.45 | 1 to 10 |
| norepinephrine_1mgml_4ml | S18 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 8.05e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S18 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 79.2 | 30 to 240 |
| norepinephrine_1mgml_4ml | S18 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0769 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S18 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 66.9 | 30 to 70 |
| norepinephrine_1mgml_4ml | S19 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.27e+05 | 5e+05 to 1.8e+06 |
| norepinephrine_1mgml_4ml | S19 | release_time (global.sterility_incubation_days) | feasible while release_time <= 16.1 | 14 to 18 |
| norepinephrine_1mgml_4ml | S19 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 92.3 | 30 to 240 |
| norepinephrine_1mgml_4ml | S19 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.112 | 0.02 to 0.3 |
| norepinephrine_1mgml_4ml | S19 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.282 | 0.05 to 0.6 |
| norepinephrine_1mgml_4ml | S19 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| norepinephrine_1mgml_4ml | S19 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 4.52 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S0 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.02e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S0 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 54.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S1 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.02e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S1 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 54.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S2 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.25e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S2 | release_time (global.sterility_incubation_days) | feasible while release_time <= 17.9 | 14 to 18 |
| sodium_bicarbonate_8_4_50ml | S2 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 22.1 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S2 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 204 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S2 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.191 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S2 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.385 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S2 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S2 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S3 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.25e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S3 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 16.1 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S3 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 204 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S3 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.402 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S3 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 44.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S3 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 4.52 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S4 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.25e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S4 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 13.9 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S4 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 145 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S4 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.199 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S4 | commissioning_days (global.node_commissioning_days) | feasible while commissioning_days <= 855 | 365 to 1.1e+03 |
| sodium_bicarbonate_8_4_50ml | S4 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 44.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S4 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S5 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S5 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 17.6 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S5 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 112 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S5 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S5 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.127 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S5 | commissioning_days (global.node_commissioning_days) | feasible while commissioning_days <= 741 | 365 to 1.1e+03 |
| sodium_bicarbonate_8_4_50ml | S5 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 41.9 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S5 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 4.52 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S6 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S6 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 17.6 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S6 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 112 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S6 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S6 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.127 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S6 | commissioning_days (global.node_commissioning_days) | feasible while commissioning_days <= 741 | 365 to 1.1e+03 |
| sodium_bicarbonate_8_4_50ml | S6 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 41.9 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S6 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 4.52 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S7 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.13e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S7 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 48.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S8 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S8 | release_time (global.sterility_incubation_days) | feasible while release_time <= 14.8 | 14 to 18 |
| sodium_bicarbonate_8_4_50ml | S8 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 23.6 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S8 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 178 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S8 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.138 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S8 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.282 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S8 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S8 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S9 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.3e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S9 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 12.4 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S9 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 125 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S9 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.182 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S9 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.385 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S9 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 40.6 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S9 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 7.61 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S10 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S10 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 12.4 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S10 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 132 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S10 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.103 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S10 | supplier_concentration (global.supplier_disruptions_per_supplier_year) | feasible while supplier_concentration <= 0.213 | 0.05 to 0.6 |
| sodium_bicarbonate_8_4_50ml | S10 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S10 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S11 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.25e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S11 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 18.4 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S11 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 224 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S11 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.182 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S11 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S11 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S12 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S12 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 12.4 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S12 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.103 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S12 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S12 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S13 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S13 | release_time (global.sterility_incubation_days) | feasible while release_time <= 14.7 | 14 to 18 |
| sodium_bicarbonate_8_4_50ml | S13 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 13.9 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S13 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 178 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S13 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.121 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S13 | activation_latency_days (global.reserved_capacity_activation_days) | feasible while activation_latency_days <= 39.3 | 7 to 60 |
| sodium_bicarbonate_8_4_50ml | S13 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 44.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S13 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 3.39 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S14 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.13e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S14 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0419 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S14 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 48.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S15 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.66e+05 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S15 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 54.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S16 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.25e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S16 | shelf_life (product.shelf_life_months) | feasible while shelf_life >= 12.4 | 12 to 36 |
| sodium_bicarbonate_8_4_50ml | S16 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 119 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S16 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.173 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S16 | activation_latency_days (global.reserved_capacity_activation_days) | feasible while activation_latency_days <= 32.7 | 7 to 60 |
| sodium_bicarbonate_8_4_50ml | S16 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 43.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S16 | changeover_burden (product.changeover_days) | feasible while changeover_burden <= 6.48 | 1 to 10 |
| sodium_bicarbonate_8_4_50ml | S17 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.19e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S17 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.182 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S17 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 44.4 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S18 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 1.13e+06 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S18 | raw_material_lead_time (product.material_lead_time_days) | feasible while raw_material_lead_time <= 59.5 | 30 to 240 |
| sodium_bicarbonate_8_4_50ml | S18 | common_cause_dependence (global.common_cause_events_per_year) | feasible while common_cause_dependence <= 0.0681 | 0.02 to 0.3 |
| sodium_bicarbonate_8_4_50ml | S18 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 48.1 | 30 to 70 |
| sodium_bicarbonate_8_4_50ml | S19 | capacity_utilization (product.annual_demand_units) | feasible while capacity_utilization <= 9.09e+05 | 6e+05 to 2.4e+06 |
| sodium_bicarbonate_8_4_50ml | S19 | batches_per_site_year (product.batches_per_site_year_nominal) | feasible while batches_per_site_year >= 59.4 | 30 to 70 |

![design space](results/figures/design_space_ds_post_R009_norepinephrine_1mgml_4ml_dominance.png)

![design space](results/figures/design_space_ds_post_R009_norepinephrine_1mgml_4ml_feasibility.png)

![design space](results/figures/design_space_ds_post_R009_norepinephrine_1mgml_4ml_reversal_fixed_qa_labor_per_node1.5e+06.png)

![design space](results/figures/design_space_ds_post_R009_norepinephrine_1mgml_4ml_reversal_fixed_qa_labor_per_node3e+06.png)

![design space](results/figures/design_space_ds_post_R009_norepinephrine_1mgml_4ml_reversal_fixed_qa_labor_per_node6e+06.png)

![design space](results/figures/design_space_ds_post_R009_sodium_bicarbonate_8_4_50ml_dominance.png)

![design space](results/figures/design_space_ds_post_R009_sodium_bicarbonate_8_4_50ml_feasibility.png)

![design space](results/figures/design_space_ds_post_R009_sodium_bicarbonate_8_4_50ml_reversal_fixed_qa_labor_per_node1.5e+06.png)

![design space](results/figures/design_space_ds_post_R009_sodium_bicarbonate_8_4_50ml_reversal_fixed_qa_labor_per_node3e+06.png)

![design space](results/figures/design_space_ds_post_R009_sodium_bicarbonate_8_4_50ml_reversal_fixed_qa_labor_per_node6e+06.png)

## Limitations

- Every numeric input except four release components is tier 5 (illustrative). Nothing here is a finding about Telo or any product.
- All 15 regulatory gates are UNCERTAIN; no favorable decision class is possible.
- No interviews or independent reviews have been completed.
- The release-assurance benchmark evidence supports shift detection and abstention only.
