# Feasibility regions (Phase E)

> **Superseded in part, 2026-09-06.** Revisions R009 to R011 changed the feasible set. Read
> `docs/design_space/post_R009_correction.md` first; where it disagrees with this document, it wins.
> Three statements below are withdrawn there: that distributed nodes meet the target nowhere, that no
> frozen comparator meets it, and that bright-stock postponement is the strongest shape for both products.


Assignment deliverables 11 and 12: the parameter region in which each architecture passes the service target, is not
dominated, and carries a contractable break-even volume, reported as conditions rather than as scores.

Prepared 2026-09-04. **PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every input behind every number below is
evidence tier 5 (illustrative), so every result in this file is behaviour of the model under provisional assumptions
and none of it is a statement about the world. Regulatory gates stay UNCERTAIN; `eligibility` is NO_CONCLUSION for all
twenty strategies in every run quoted here, so no strategy is presented as permitted, and nothing here is legal or
regulatory advice. Artifacts: `results/design_space/ds_post_R008/` (`thresholds.csv`, `dominance.csv`, `reversal.json`,
`contract_scenarios.csv`, `summary.json`); the matched-service optimizer runs `opt_20260903T220534Z` at the frozen
target and `opt_20260903T231408Z_tau0.98` at tau 0.98; the paired baseline `results/simulation/sim_post_R008/`
(n = 100); `results/design_space/contract_conditions_sim_post_R008.csv` with `src/telo_feasibility/contracting.py`;
figures under `../../results/figures/design_space_ds_post_R008_*`. Every run made before 2026-09-03 is superseded for
quantitative use and none is quoted here.

---

## 1. Method

**The feasibility predicate is service only.** `design_space_analysis.evaluate` marks a point feasible when mean fill
rate is at or above tau and the tail probability `p_meet = P(fill >= tau)` is at or above q, with tau = 0.99 and
q = 0.90 (`ds_post_R008/summary.json` `meta.tau`, `meta.q`). Cost enters nowhere in that test. Three consequences run
through this whole file: a purely economic input can never cross the boundary (section 2, no-crossing list), a
strategy can sit on the cost-service frontier while failing the target (S15 on both products), and every commercial
threshold in section 3 has to come from `contracting.py` rather than from a simulated crossing.

**Bisection.** For each of 20 strategies x 2 products x 12 inputs, `design_space_analysis.threshold` evaluates the
strategy at the input's recorded low and at its recorded high, and only if those two disagree does it bisect for five
steps. Each evaluation is 20 paired runs on common random numbers at the strategy's own optimized design from
`opt_20260903T220534Z`. That is 480 rows and at most seven evaluations per row. The reported crossing is the midpoint
of the final bracket, so its resolution is the recorded range divided by 64, and both bracketing evaluations are kept
in the `evaluations` column of `thresholds.csv`.

**What monotonicity is assumed.** Bisection assumes the feasibility indicator is monotone in the swept input over the
recorded range. The two endpoints are always evaluated and always reported, so a non-monotone response shows up as a
direction that contradicts the mechanism rather than being hidden. It does show up: `raw_material_lead_time` returns
`feasible_above` in 5 of its 7 crossings, meaning the strategy meets the target at a *longer* API lead time and fails
at a shorter one. That is defect MD-1 (`bottleneck_decomposition.md` section 7), still open: the material order-up-to
level and reorder point are `(target_days + lead) x daily demand`, so cutting the lead cuts the buffer. No maximum API
lead time is claimed here for that reason.

**Why a condition is stated only where feasibility changes inside the range.** A row whose two endpoints agree carries
no information about where a boundary is, only that none was met between the recorded low and the recorded high. Those
rows are reported in section 2 as no crossing inside the recorded range, split into feasible everywhere and infeasible
everywhere, and are never restated as conditions.

**Run counts and what they imply.** Threshold grid: 20 paired runs per evaluation. Dominance: 40 paired runs at each
strategy's optimized design. Reversal: 27 cells per product, **10 paired runs** and 20 strategies per cell, because
`scripts/run_design_space_analysis.py` passes `runs=list(range(max(args.runs // 4, 2)))` and the run used 40; every
`p_meet` in `reversal.json` is a multiple of 0.1 across all 1,080 strategy-cell values, which is the granularity of
10 runs. The binomial standard error of `p_meet` at q = 0.90 is 0.067 at 20 runs, 0.047 at 40 and **0.095 at 10**
(MD-16). Eleven cells whose threshold-grid verdict and 40-run base verdict disagree are named in section 2.3, with
the measured spread of each; they are not uniformly inside noise. Read every crossing as located to about one bracket
plus one standard error, not to the digits printed, and read every reversal cell in section 5 as resolved to no
better than one run, which is 0.1 of the tail probability.

**Every region below is conditioned on a design the search could not move further.** 111 of the 150 design variables
across the 40 optimizer cells sit exactly on a search bound (74%; `opt_20260903T220534Z`, best or best_grid;
`inventory_capacity_hybrids.md` section 3.1 works the same count through for ten of those cells). Sections 2, 4 and 5
all evaluate at those designs, so a threshold, a dominance row or a reversal cell reports where the box ends as much
as where the architecture sits.

---

## 2. Conditions, per product

Recorded ranges swept (low, base, high), from the parameter records:

| column | parameter | range (norepinephrine) | range (sodium bicarbonate) |
|---|---|---|---|
| demand | `product.annual_demand_units` | 500,000 / 900,000 / 1,800,000 per yr | 600,000 / 1,200,000 / 2,400,000 per yr |
| batches | `product.batches_per_site_year_nominal` | 30 / 45 / 70 per site-yr | 30 / 45 / 70 per site-yr |
| sterility d | `global.sterility_incubation_days` | 14 / 14 / 18 d | 14 / 14 / 18 d |
| shelf mo | `product.shelf_life_months` | 12 / 24 / 30 mo | 12 / 24 / 36 mo |
| API lead | `product.material_lead_time_days` | 30 / 90 / 240 d | 30 / 90 / 240 d |
| cc rate | `global.common_cause_events_per_year` | 0.02 / 0.1 / 0.3 per yr | 0.02 / 0.1 / 0.3 per yr |
| suppl rate | `global.supplier_disruptions_per_supplier_year` | 0.05 / 0.2 / 0.6 per supplier-yr | 0.05 / 0.2 / 0.6 per supplier-yr |
| activation d | `global.reserved_capacity_activation_days` | 7 / 21 / 60 d | 7 / 21 / 60 d |
| changeover d | `product.changeover_days` | 1 / 3 / 10 d | 1 / 3 / 10 d |

How to read a cell. `<=7.61 (73%)` means: feasible while that input is at or below 7.61 in the units above, and the
feasible side covers 73% of the recorded low-to-high range. `>=21.3 (48%)` means feasible while the input is at or
above 21.3, covering 48% of the range. `all` means feasible across the whole recorded range (no crossing). `none`
means infeasible across the whole recorded range (no crossing). Figures:
`../../results/figures/design_space_ds_post_R008_norepinephrine_1mgml_4ml_feasibility.png` and
`../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_feasibility.png`.

### 2.1 Norepinephrine 1 mg/mL 4 mL

| S | demand | batches | sterility d | shelf mo | API lead | cc rate | suppl rate | activation d | changeover d |
|---|---|---|---|---|---|---|---|---|---|
| S0 | none | none | none | none | none | none | none | none | none |
| S1 | none | >=48.1 (55%) | none | none | none | none | none | none | none |
| S2 | none | none | none | none | none | none | none | none | none |
| S3 | <=0.64M (11%) | none | <=14.6 (14%) | all | >=85.8 (73%) | all | <=0.385 (61%) | <=19.4 (23%) | none |
| S4 | none | none | none | none | none | none | none | none | none |
| S5 | none | none | none | none | none | none | none | none | none |
| S6 | none | none | none | none | none | none | none | none | none |
| S7 | none | none | none | none | none | none | none | none | none |
| S8 | <=0.64M (11%) | >=43.1 (67%) | all | >=21.3 (48%) | all | <=0.191 (61%) | <=0.282 (42%) | all | <=7.61 (73%) |
| S9 | <=1.09M (45%) | >=35.6 (86%) | all | all | all | all | all | all | <=8.45 (83%) |
| S10 | <=0.60M (8%) | none | <=15.6 (39%) | >=16.8 (73%) | >=59.5 (86%) | <=0.138 (42%) | <=0.454 (73%) | all | <=7.61 (73%) |
| S11 | <=1.09M (45%) | >=36.9 (83%) | all | >=12.3 (98%) | all | <=0.173 (55%) | <=0.471 (77%) | all | <=9.58 (95%) |
| S12 | <=0.93M (33%) | >=44.4 (64%) | <=17.4 (86%) | all | >=33.3 (98%) | <=0.138 (42%) | <=0.557 (92%) | all | <=8.45 (83%) |
| S13 | <=0.89M (30%) | >=38.1 (80%) | <=15.7 (42%) | all | all | <=0.156 (48%) | all | all | <=7.61 (73%) |
| S14 | none | none | <=15.1 (27%) | >=19.6 (58%) | all | <=0.138 (42%) | <=0.282 (42%) | all | <=4.52 (39%) |
| S15 | <=0.68M (14%) | >=60.6 (23%) | <=14.3 (8%) | >=22.4 (42%) | none | <=0.112 (33%) | none | all | none |
| S16 | <=0.93M (33%) | >=43.1 (67%) | all | all | none | <=0.138 (42%) | <=0.437 (70%) | all | <=6.48 (61%) |
| S17 | <=0.97M (36%) | all | all | all | all | all | all | all | all |
| S18 | <=0.97M (36%) | none | <=17.9 (98%) | >=14.5 (86%) | <=210.5 (86%) | <=0.191 (61%) | <=0.334 (52%) | all | <=8.45 (83%) |
| S19 | <=0.89M (30%) | >=43.1 (67%) | <=16.3 (58%) | all | <=158.0 (61%) | <=0.112 (33%) | <=0.265 (39%) | all | <=5.64 (52%) |

### 2.2 Sodium bicarbonate 8.4% 50 mL

| S | demand | batches | sterility d | shelf mo | API lead | cc rate | suppl rate | activation d | changeover d |
|---|---|---|---|---|---|---|---|---|---|
| S0 | none | none | none | none | none | none | none | none | none |
| S1 | none | none | none | none | none | none | none | none | none |
| S2 | none | none | none | none | none | none | none | none | none |
| S3 | <=1.19M (33%) | none | <=14.4 (11%) | all | none | <=0.112 (33%) | none | <=19.4 (23%) | none |
| S4 | none | none | none | none | none | none | none | none | none |
| S5 | none | none | none | none | none | none | none | none | none |
| S6 | none | none | none | none | none | none | none | none | none |
| S7 | none | none | none | none | none | none | none | none | none |
| S8 | <=1.19M (33%) | >=43.1 (67%) | <=14.8 (20%) | >=23.6 (52%) | >=230.2 (5%) | <=0.112 (33%) | <=0.316 (48%) | all | <=6.48 (61%) |
| S9 | <=1.36M (42%) | >=40.6 (73%) | all | all | all | all | all | all | <=8.45 (83%) |
| S10 | <=1.19M (33%) | >=43.1 (67%) | all | >=12.4 (98%) | all | <=0.103 (30%) | <=0.213 (30%) | all | <=6.48 (61%) |
| S11 | <=1.19M (33%) | >=44.4 (64%) | <=14.3 (8%) | >=19.9 (67%) | all | <=0.182 (58%) | <=0.402 (64%) | <=27.7 (39%) | <=3.39 (27%) |
| S12 | <=1.25M (36%) | >=44.4 (64%) | all | all | all | <=0.173 (55%) | all | all | <=5.64 (52%) |
| S13 | <=1.25M (36%) | >=43.1 (67%) | all | >=13.1 (95%) | all | <=0.103 (30%) | all | all | <=7.61 (73%) |
| S14 | <=1.19M (33%) | >=43.1 (67%) | <=15.9 (48%) | >=22.1 (58%) | >=66.1 (83%) | <=0.138 (42%) | <=0.282 (42%) | all | <=6.48 (61%) |
| S15 | <=1.08M (27%) | >=54.4 (39%) | none | none | none | none | none | none | none |
| S16 | <=1.25M (36%) | >=43.1 (67%) | <=16.6 (64%) | all | all | <=0.173 (55%) | <=0.591 (98%) | <=22.7 (30%) | <=5.64 (52%) |
| S17 | <=1.02M (23%) | >=44.4 (64%) | <=15.3 (33%) | all | none | <=0.156 (48%) | <=0.316 (48%) | all | <=4.52 (39%) |
| S18 | <=1.19M (33%) | >=43.1 (67%) | all | all | all | <=0.138 (42%) | <=0.557 (92%) | all | <=6.48 (61%) |
| S19 | <=1.02M (23%) | >=54.4 (39%) | none | none | none | none | none | none | none |

### 2.3 No crossing inside the recorded range

Three of the twelve swept inputs produce zero crossings in all 40 cells, so no condition is stated on any of them:
`product.fixed_qa_labor_usd_per_site_year` (1.5M to 6.0M USD per site-year), `global.node_commissioning_days`
(365 to 1095 d) and `product.capital_usd_per_site` (15M to 100M USD). For each of the three, the same 13
norepinephrine cells (S3, S8 to S19) and 11 sodium bicarbonate cells (S3, S8 to S14, S16, S17, S18) are feasible
across the whole range, and the remaining 7 and 9 cells are infeasible across the whole range. Two of the three are
cost-only inputs and cannot cross a service-only predicate by construction; the third, commissioning days, bites on
almost nothing here because the swept global applies only to a site plan that sets no `commissioning_days` of its own
(`strategies.py:153-155`), and its recorded low of 365 d is also `warm_up_days` (MD-17, open).

Counting the whole grid: 202 of 480 rows are infeasible everywhere, 140 are feasible everywhere, 101 are feasible
below a crossing and 37 feasible above one. Every S0 to S7 cell except S1 and S3 on norepinephrine and S3 on sodium
bicarbonate is infeasible across every recorded range of every input.

**Eleven disagreements with the 40-run base call.** Eleven cells are infeasible at base on 40 runs yet return
`feasible everywhere` on at least one input at 20 runs: norepinephrine S3, S8, S10, S14, S15, S18 and S19, and sodium
bicarbonate S3, S8, S14 and S17. All eleven carry base `p_meet` between 0.80 and 0.875 against q = 0.90, but they are
not all inside noise, and the measured spread at 40 runs (SE 0.047) is: 0.875 at norepinephrine S8 and S19, 0.5 SE
below q; 0.85 at norepinephrine S10 and S18 and sodium bicarbonate S3 and S17, 1.1 SE; 0.825 at norepinephrine S15
and sodium bicarbonate S14, 1.6 SE; and 0.80 at norepinephrine S3 and S14 and sodium bicarbonate S8, 2.1 SE. The two
0.875 cells are a tie. For the five cells at 0.825 and below, 1.6 to 2.1 standard errors out, the 20-run
`feasible everywhere` verdict is a low-n artifact rather than a tie, and the 40-run base call should be preferred.
None of the eleven is treated as feasible anywhere in this file.

**Sharpest conditions in the set.** The tightest are on release time: norepinephrine S15 and sodium bicarbonate S11
lose the target 0.31 d above the 14 d sterility incubation base, and S3 loses it at 0.56 d and 0.44 d. The tightest
demand condition is norepinephrine S10 at 0.60M units per year, 8% of the recorded range; the tightest changeover
condition is sodium bicarbonate S11 at 3.39 d against a 3 d base. The loosest cell is norepinephrine S17, feasible
across the entire recorded range of eight of the nine inputs, with only demand binding at or below 0.97M per year.

---

## 3. The eleven thresholds the assignment names

| # | threshold | value from these runs | where it comes from |
|---|---|---|---|
| 1 | minimum contracted utilization | at an assumed 18.00 USD per unit: norepinephrine S11 0.798, S16 0.845, S17 1.008, S13 1.091, S12 1.235, S9 1.460; sodium bicarbonate S11 0.599, S16 0.632, S10 0.720, S13 0.820, S12 0.928, S18 0.963, S9 1.097. A value above 1.0 means the design cannot cover fixed and resilience cost even if every saleable unit is committed | `contracting.minimum_contracted_utilization`, called with `fixed_and_resilience_cost_usd` = `fixed_share_of_cost` x `annual_cost_usd` and `capacity_units_per_year` from `contract_conditions_sim_post_R008.csv`, `contribution_margin_usd_per_unit` = price minus per-unit variable cost, where per-unit variable cost is `variable_materials_usd_per_unit` + `variable_conversion_usd_per_unit` = 0.55 + 0.60 = **1.15 USD** (norepinephrine) and 0.60 + 0.60 = **1.20 USD** (sodium bicarbonate), so at the assumed 18.00 USD price the margin passed is **16.85** and **16.80 USD per unit**. Corrected 2026-09-06: the earlier wording read as though 1.15 and 1.20 were the margin, which they are not; reproducing the 0.798 in this row needs 16.85 against fixed-and-resilience cost 12,651,572 and capacity 940,451, while 1.15 returns 11.698. The 18.00 USD price is an assumption, not evidence |
| 2 | maximum fixed QA cost per node | not determined by the service test: no cell crosses between 1.5M and 6.0M USD per site-year. Commercially, `contracting.maximum_fixed_cost_per_site` at 18.00 USD per unit with half of a strategy's saleable capacity committed carries 7.92M USD per year on norepinephrine (0.5 x 940,451 units, S11) and 10.51M on sodium bicarbonate (0.5 x 1,251,055 units, S1), against total fixed and resilience cost of 10.47M to 42.32M USD per year across the twenty strategies. The commercial figure is a **network** ceiling despite the function's name, because `maximum_fixed_cost_per_site` returns contribution margin times committed volume and the volume passed is network-wide; no per-node commercial ceiling is determined by these runs | `thresholds.csv` (`fixed_qa_labor_per_node` rows) and `contracting.maximum_fixed_cost_per_site` on the same inputs as row 1 |
| 3 | maximum release time | sterility incubation days, per cell: from 14.31 d (norepinephrine S15, sodium bicarbonate S11) to 17.94 d (norepinephrine S18). Ten of forty cells hold across the whole 14 to 18 d range | `thresholds.csv`, `release_time` rows |
| 4 | minimum shelf life | months, per cell: 12.28 (norepinephrine S11) to 22.41 (norepinephrine S15); 12.38 (sodium bicarbonate S10) to 23.63 (sodium bicarbonate S8). Thirteen of forty cells hold across the whole range | `thresholds.csv`, `shelf_life` rows |
| 5 | maximum API lead time | **not determined by these runs.** Five of the seven crossings return `feasible_above`, meaning feasibility improves at a longer lead, which is defect MD-1 (the material buffer is proportional to the lead). The two `feasible_below` values that exist, 210.5 d (norepinephrine S18) and 158.0 d (S19), are not interpretable while the sign is wrong | `thresholds.csv`, `raw_material_lead_time` rows; MD-1 in `bottleneck_decomposition.md` section 7 |
| 6 | minimum supplier independence | two axes. Common-cause event rate at or below 0.103 to 0.191 per group-year in the 20 cells that cross; per-supplier disruption rate at or below 0.213 to 0.591 per supplier-year in the 16 cells that cross. Norepinephrine S9 and S17 hold across both full ranges | `thresholds.csv`, `common_cause_dependence` and `supplier_concentration` rows |
| 7 | minimum portfolio size | **not determined by these runs.** No portfolio-size input is swept, and the engine runs one product per network (MD-15), so portfolio effects enter only as the accounting shares `portfolio_capacity_share` and `portfolio_fixed_cost_share` | `ds_post_R008/summary.json` `meta.inputs`; MD-15 |
| 8 | maximum changeover burden | days, per cell: 3.39 (sodium bicarbonate S11) to 9.58 (norepinephrine S11), against a 3 d base. Twenty of forty cells cross inside the 1 to 10 d range | `thresholds.csv`, `changeover_burden` rows |
| 9 | required take-or-pay percentage | **not determined by the service test**, and the reason is structural: fill is bit-identical across take-or-pay fractions 0.00, 0.25, 0.50, 0.75 and 1.00 for all ten swept cells while annual cost rises monotonically (norepinephrine S17: 17.98M to 20.21M USD per year at identical fill 0.996743 and `p_meet` 1.00). That is MD-24. The commercial requirement is row 1: the committed share that covers fixed and resilience cost | `ds_post_R008/contract_scenarios.csv`; MD-24 |
| 10 | minimum risk-coverage performance | **not determined by these runs.** Every design-space strategy runs release scenario R0, so no release-assurance gate is exercised anywhere in this battery, and gate G15 is not PASS | `config/strategies/design_space.yaml`; `ds_post_R008/summary.json` `meta.eligibility` (NO_CONCLUSION for all twenty) |
| 11 | maximum activation latency | reserved-capacity activation days: 19.42 d (S3, both products), 22.73 d (sodium bicarbonate S16), 27.70 d (sodium bicarbonate S11). The other 20 feasible cells hold across the whole 7 to 60 d range | `thresholds.csv`, `activation_latency_days` rows |

Two cautions on row 1. First, at the break-even price the required share
(`min_contracted_utilization_at_break_even` in `contract_conditions_sim_post_R008.csv`) runs 0.6325 to 0.9384 across
the forty rows, and 0.8003 to 0.9366 across the thirteen cells that meet the service target. It is *not*
committed-equals-delivered: delivered volume equals fixed cost divided by margin only if the ledger held nothing but
fixed cost and a per-unit variable cost, and `annual_total_cost` also carries quality testing, failure waste and
inventory logistics. Sodium bicarbonate S0 is the clearest case: 10,473,595 / (14.4320 - 1.20) = 791,533 committed
against 895,647 delivered and 1,251,363 of capacity, which is 0.6325 while its fill is 0.7157. The column that *is*
fill by construction is `implied_utilization`, which equals `fill_rate.mean` to the last digit in every row (sodium
bicarbonate S16, 0.9117403837294629 against 0.9117403837294628). Second, the price floor at which the required share reaches
exactly 1.0 is 14.60 USD per unit for norepinephrine S11 and 25.74 for S9, and 11.26 for sodium bicarbonate S11 and
19.63 for S9. For context on where those sit, USP reports that 74% of sterile injectables in shortage price below
15 USD per unit and 44% below 5 USD, n = 61 (F12-S14). Under illustrative costs the status quo S0 itself needs
14.26 USD per unit (norepinephrine) to break even, so the whole cost model sits at or above the top of that band and
no conclusion about affordability should be drawn until real cost and price evidence replaces it (HA-11, HA-24).

---

## 4. Dominance

Counts at the frozen target (tau = 0.99, q = 0.90), from `opt_20260903T220534Z/summary.json` status `optimal` and
confirmed by the `feasible` column of `dominance.csv`: **zero of the eight frozen strategies S0 to S7 meet it on
either product.** Six of the twelve design-space strategies meet it on norepinephrine (S9, S11, S12, S13, S16, S17)
and seven on sodium bicarbonate (S9, S10, S11, S12, S13, S16, S18); five meet it on both (S9, S11, S12, S13, S16).

Frontier, cheapest first, as mean annual cost / mean fill / `p_meet` / meets target
(`dominance.csv`, 40 paired runs; figures
`../../results/figures/design_space_ds_post_R008_norepinephrine_1mgml_4ml_dominance.png` and
`../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_dominance.png`):

- Norepinephrine: S15 12.58M / 0.9925 / 0.825 / no; S11 14.86M / 0.9950 / 0.95 / yes; S16 15.89M / 0.9967 / 0.90 / yes;
  S17 18.20M / 0.9972 / 1.00 / yes; S9 23.23M / 1.0000 / 1.00 / yes.
- Sodium bicarbonate: S1 12.67M / 0.7591 / 0.00 / no; S15 13.16M / 0.9412 / 0.125 / no; S11 15.71M / 0.9970 / 0.925 /
  yes; S16 16.48M / 0.9972 / 0.925 / yes; S12 22.40M / 0.9976 / 0.95 / yes; S9 24.40M / 0.9997 / 1.00 / yes.

Being on the frontier is not the same as being feasible: S15 on both products and S1 on sodium bicarbonate hold the
cheap end of the frontier while failing the target, which is what a cost-service frontier with a service-only
feasibility predicate looks like.

Dominated, and by the cheapest strategy that dominates them. Every frozen build architecture is dominated on both
products: norepinephrine S4 by 15 strategies (cheapest S15 at 12.58M against S4's 37.81M), S5 by 16, S6 by 17, S2 by
10 (cheapest S11 at 14.86M against 34.08M), S7 by 11, S3 by 3, S0 by 2, S1 by 1; sodium bicarbonate S5 by 16, S6 by
17, S4 by 12, S2 by 11 (cheapest S11 at 15.71M against 35.48M), S7 by 11, S14 by 9, S8 by 7, S3 by 5, S19 by 2, S0 by
1. Among design-space strategies the dominated are norepinephrine S14 (by 12), S8 (6), S18 (4), S10 (3), S12, S13 and
S19 (1 each), and sodium bicarbonate S14, S8, S10, S13, S17, S18 and S19. S13 and S17 swap places between the
products: S17 is on the norepinephrine frontier but dominated by S11 on sodium bicarbonate, while S13 is dominated on
both.

**Does the frontier change at tau 0.98?** No dominance run exists at tau 0.98, so the comparison is limited to the
optimizer records, and a frontier computed from those uses each strategy's own separately searched design rather than
one matched evaluation. On that basis: on norepinephrine the set meeting the target grows by one, and the addition is
a frozen comparator, S3 (reserved capacity, `optimal` at 17.27M USD per year, fill 0.9863, `p_meet` 0.90), so the
statement "no frozen strategy clears" survives at 0.99 but not at 0.98. The cheap end also changes: frozen S1 joins
S15 at the frontier's foot, and S19 appears on it. On sodium bicarbonate the count stays at seven but the membership
moves, S17 in and S11 out. The S11 exit is a search artifact rather than a real reversal: a looser tau cannot lower a
tail probability at a fixed design, and the tau-0.98 search returned a cheaper design (15.50M against 15.71M) that
then failed q at full n. Read together, the frontier is stable in shape across the two targets and unstable in
membership at the margin, and the one decision-relevant change is that the reserved-capacity comparator becomes
feasible on norepinephrine at 0.98.

---

## 5. Reversal

The reversal map is a 3 x 3 x 3 grid over demand, common-cause rate and fixed QA cost per node, 27 cells per product,
preferring the cheapest strategy that meets the target, at **10 paired runs per cell** (section 1). At 10 runs one run
is 0.1 of the tail probability and the binomial standard error at q = 0.90 is 0.095, so every count below is resolved
to no better than one run and no preference flip in this section is separated from noise by these data
(`reversal.json`; figures
`../../results/figures/design_space_ds_post_R008_norepinephrine_1mgml_4ml_reversal_fixed_qa_labor_per_node3e+06.png`
and `../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_reversal_fixed_qa_labor_per_node3e+06.png`).

**Where the preferred strategy changes.** On norepinephrine, four different strategies are preferred across the map:
S11 in 6 cells, S15 in 6, S1 in 3, S3 in 3, and none in 9. The reversals run along both live axes. At the low demand
of 500,000 units per year the preferred design is S11 at common-cause rates 0.02 and 0.3 but S15 at 0.1, which is a
non-monotone flip inside one axis and should be treated as noise between two designs whose costs differ by about 2.3M
USD per year rather than as a mechanism. At base demand the preference moves from frozen S1 at the low common-cause
rate, to S15 at the base rate, to frozen S3 at the high rate, and the number of feasible strategies collapses from 11
to 3 (S3, S9, S17) as the rate rises from 0.02 to 0.3. On sodium bicarbonate the pattern is cleaner: S15 in all 9
low-demand cells, S11 in 6, S3 in 3, none in 9, with the same collapse at the high common-cause rate (13 feasible
strategies at 600,000 units per year and rate 0.02, down to 2 at base demand and rate 0.3). Both collapses are
counted at n = 10, where a strategy enters or leaves a feasible set on one run, so read 11 to 3 and 13 to 2 as the
direction of a large effect and not as a count that would repeat.

**Where no strategy qualifies.** All 9 cells at the high demand corner, on both products: 1,800,000 units per year for
norepinephrine and 2,400,000 for sodium bicarbonate. No strategy of the twenty meets the target in any of those 18
cells at any common-cause rate or QA cost. That is the mass-balance region: at twice the base demand the network
cannot be stocked out of the deficit, and it is the one region of this map where the answer does not depend on which
architecture is chosen.

**The third axis is inert.** Fixed QA cost per node changes the preferred strategy in zero of the 27 cells on either
product and the feasible set in none of them, for the reason given in section 2.3: it is a cost input and feasibility
is decided on service. This is the one reading in this section that the low run count does not weaken, because it is
an exact zero across 54 cells and follows from the structure of the predicate rather than from a count. It is the axis on which the multi-product and shared-quality-unit families claim their
advantage, and the map's answer is that in this engine that advantage cannot change a service decision.

---

## 6. Feasibility as conditions, not scores

One sentence per architecture family, using the family assignment in `novel_architectures.md` section 2.

- **Family 1, existing Telo architectures (S0 to S8).** Distributed owned nodes (S5, S6), the enlarged incumbent plant
  (S4) and frozen dual sourcing (S2) meet the target in no region of any recorded range on either product. Three
  members have a region: S1, on norepinephrine only, at 48.1 or more batches per site-year; S3, the reserved-capacity
  comparator, on both products, including activation latency at or below 19.4 d and sterility incubation within
  0.56 d and 0.44 d of its base; and S8, the acquired registered line, which meets it while demand is at or below
  0.64M units per year (norepinephrine) or 1.19M (sodium bicarbonate), shelf life is at or above 21.3 or 23.6 months,
  changeover is at or below 7.61 or 6.48 d and the common-cause rate is at or below 0.191 or 0.112 per year. S8 is
  dominated by six and seven other strategies, and none of the three meets the target at base on either product.
- **Family 3, virtual manufacturing network (S12, S13).** Meets the target on both products at base, S12 on the sodium
  bicarbonate frontier at 22.40M USD per year, while demand is at or below 0.93M / 1.25M units per year, the
  common-cause rate is at or below 0.138 / 0.173 per year and changeover is at or below 8.45 / 5.64 d; at 18.00 USD
  per unit S12 needs 1.235 of norepinephrine capacity committed, so it clears the service condition and fails the
  commercial one on that product.
- **Family 5, postponement (S11).** The cheapest feasible design on both products (14.86M and 15.71M USD per year, both
  on the frontier), feasible while demand is at or below 1.09M / 1.19M units per year, the common-cause rate is at or
  below 0.173 / 0.182 per year and changeover is at or below 9.58 / 3.39 d, and one of only two designs among the
  five that meet the target on both products whose required committed share stays below 1.0 at 18.00 USD per unit
  (0.798 and 0.599).
- **Family 6, multi-product portfolio (S10).** Meets the target on sodium bicarbonate only, while demand is at or below
  1.19M units per year, the common-cause rate is at or below 0.103 per year and the per-supplier disruption rate is at
  or below 0.213 per supplier-year, which is the tightest supplier condition in the whole grid; on norepinephrine its
  region requires demand at or below 0.60M units per year, 8% of the recorded range.
- **Family 7, warm standby (S17).** On norepinephrine it is feasible across the entire recorded range of eight of the
  nine inputs with only demand binding, at or below 0.97M units per year, and it loses 0.0000 of the measured window to
  commissioning; on sodium bicarbonate it fails at base and is dominated by S11, so the region is product-specific.
- **Family 8, inventory-capacity hybrids (S16).** Meets the target on both products and sits on both frontiers, while
  demand is at or below 0.93M / 1.25M units per year, the common-cause rate is at or below 0.138 / 0.173 per year,
  activation latency is at or below 22.7 d (sodium bicarbonate) and changeover is at or below 6.48 / 5.64 d; with S11 it
  is the other of those two designs, at 0.845 and 0.632.
- **Family 9, upstream-first (S9, S19).** S9 meets the target on both products and is the only strategy that holds on
  both across the whole common-cause and supplier-disruption ranges, but at 18.00 USD per unit it needs 1.460
  and 1.097 of capacity committed, so its region is a service region and not a commercial one. S19 meets the target on
  neither product at base; on norepinephrine it has a region requiring the common-cause rate at or below 0.112 per
  year and the supplier rate at or below 0.265 per supplier-year, and **on sodium bicarbonate no region inside the
  recorded ranges makes it feasible** except by cutting demand to 1.02M units per year or raising batches to 54.4 per
  site-year. Gate G16, alternate component, container-closure and API source qualified and authorised, applies to S9
  and S19 and stays UNCERTAIN, so the switching lead time both designs depend on is unpriced.
- **Family 10, contracts and procurement (S18).** Meets the target on sodium bicarbonate only, while demand is at or
  below 1.19M units per year and the supplier rate is at or below 0.557 per supplier-year; on norepinephrine it misses
  at base (`p_meet` 0.85) and is dominated by four. Gate G16 applies to S18 as well and stays UNCERTAIN, so the
  contract-mandated distinct API and container sources carry a qualification lead nothing here prices.
- **Family 12, product selection (S15).** **No region inside the recorded ranges makes the inventory-only design meet
  the target on sodium bicarbonate**, where its best `p_meet` is 0.125, and on norepinephrine it reaches the target
  only while demand is at or below 0.68M units per year, the common-cause rate is at or below 0.112 per year and
  sterility incubation stays within 0.31 d of its base; it is nonetheless the cheapest point on both frontiers, which
  is the cleanest illustration in this file of a frontier position that is not a feasibility statement.
- **Family 13, public-private (S14).** Meets the target on neither product at base; it has regions on both (sterility
  at or below 15.1 / 15.9 d, changeover at or below 4.52 / 6.48 d, shelf life at or above 19.6 / 22.1 months), and at
  18.00 USD per unit it needs 1.347 of norepinephrine capacity committed, so the commercial condition fails on the
  product where the service condition is hardest.
- **Families 2, 4, 11 and 14 (OS-only, hub-and-spoke, release route, mobile and modular).** No configured strategy
  exists for any of them, so no region can be stated. `architecture_taxonomy.md` section 1 records why: family 2
  reaches no physical mechanism in the engine, family 4 can represent a hub only as a supplier with a lead time,
  family 11 acts on a mechanism Phase A found not to bind, and family 14's move restarts the qualification clock.

---

## 7. What the regions depend on

Every input behind every region above is evidence tier 5, marked `illustrative` with `confidence: low` in its own
parameter record. The regions therefore locate the behaviour of the model, not the behaviour of the world, and no row
of section 2, 3 or 6 should be read as a claim about sterile-injectable manufacturing. The three inputs whose real
values would most change the picture:

1. **Annual demand for the exact presentation, and the installed capacity that serves it**
   (`product.annual_demand_units` with `product.batches_per_site_year_nominal`). Together they account for 46 of the
   138 crossings, they are the only axis on which the reversal map has a region where nothing qualifies, and they are
   the one input pair that moves every strategy in the same direction. Human actions: HA-11 (hospital, GPO or
   wholesaler utilization for each presentation, to replace the CMS Part B outpatient proxy), HA-13 and HA-21 (real
   line capacity and batch rate). This is also the screen's own open question in `bottleneck_decomposition.md` section
   8, ranked second there.
2. **The common-cause event rate** (`global.common_cause_events_per_year`, source locator "workbook
   05_Assumptions!B21:D21"). It produces 20 crossings, it is the axis along which at base demand the feasible set collapses from 11
   strategies to 3 on norepinephrine and from 10 to 2 on sodium bicarbonate as the rate rises from 0.02 to 0.3; the
   13 quoted in section 5 is measured at 600,000 units per year, not at base demand. Its own parameter record names
   `strategy_ranking` among the outputs it can reverse. Human actions: HA-25 (dependence and calibration) and HA-30.
   No queue row asked for a disruption rate directly when this was written; that row now exists as HA-39, rank 14.
3. **The price a purchaser will pay per unit.** It is not one of the swept inputs, and that is the point: it decides
   row 1 of section 3, and it moves five of the thirteen strategy-product cells that meet the service target from
   commercially possible to impossible as the price falls from break-even to 18.00 USD. Human actions: HA-24 (GPO,
   wholesaler and distributor), HA-20 (hospital pharmacy and supply chain), HA-11 for the volume it applies to.

Runner-up among the swept inputs is `product.changeover_days` (20 crossings, HA-21), which matters because three of the
five strategies feasible on both products lose the target inside 6.5 d of changeover on at least one product, and one
of them loses it at 3.39 d against a 3 d base.

**Register.** `falsification_register.csv` now carries a `result_pointer` column and a status of `untested`,
`supported by the model under illustrative inputs`, or `falsified in the model` on each of its 33 claim rows; a
trailing `BANNER` row carries the study labels and is not a claim. Rows are cited here by **data-row index**, the
row's position among the 33 claim rows, counting the header as no row. Six rows are falsified in the model (S8 row 1,
S9 rows 4 and 5, S14 row 17, S15 rows 19 and 21), three are supported under illustrative inputs (S12 row 12, S16 row
22, S17 row 25), and 24 remain untested: 12 need human evidence, 9 need a control run this battery does not contain,
2 are blocked on the engine gap MD-23 (rows 23 and 26) and 1 on the protocol gap MD-17 (row 2, whose test needs
`warm_up_days` moved off the parameter grid). The two commercial falsifications hold at any unit price below their
own floors and not above them: 25.74 and 19.63 USD per unit for S9 row 5, which section 3 gives, and 23.84 and 18.21
for S14 row 17, which appear only in the register itself. `result_pointer` names the artifact key that decides the
row, or the run or human-action id that would.

---

## 8. Fair-comparison correction (added 2026-09-05, run matched_20260905)

The dominance and threshold results above use each strategy's declared search space. Those spaces are not comparable:
the frozen comparators search safety stock to 90 or 120 days with no daily base-stock review, while every
design-space strategy declares a search to 365 days with the review as a binary variable. Model defect MD-12 records
the omission. A comparison across that gap measures search freedom as much as architecture, so
`scripts/run_matched_space_check.py` re-optimizes four strategies twice, over their declared space and over one common
inventory space, at 12 search runs and 40 final runs.

| product | strategy | declared space | matched space |
|---|---|---|---|
| norepinephrine | S1 safety stock | infeasible at full n, fill 0.9874, P 0.72, 12.7 M | infeasible at full n, fill 0.9889, P 0.85, 12.8 M |
| norepinephrine | S4 added central capacity | infeasible, fill 0.9881, P 0.67, 37.8 M | **optimal**, fill 0.9952, P 0.90, 20.0 M |
| norepinephrine | S5 distributed nodes | infeasible, fill 0.9801, P 0.58, 35.4 M | infeasible at full n, fill 0.9950, P 0.85, 20.0 M |
| norepinephrine | S6 nodes plus release layer | infeasible, fill 0.9801, P 0.58, 37.5 M | infeasible at full n, fill 0.9950, P 0.85, 21.0 M |
| sodium bicarbonate | S1 safety stock | infeasible, fill 0.7582, P 0.00, 12.7 M | infeasible, fill 0.8951, P 0.00, 13.1 M |
| sodium bicarbonate | S4 added central capacity | infeasible, fill 0.9531, P 0.00, 38.6 M | **optimal**, fill 0.9952, P 0.90, 23.7 M |
| sodium bicarbonate | S5 distributed nodes | infeasible, fill 0.8666, P 0.00, 46.7 M | infeasible, fill 0.9883, P 0.58, 64.3 M |
| sodium bicarbonate | S6 nodes plus release layer | infeasible, fill 0.8666, P 0.00, 49.0 M | infeasible, fill 0.9883, P 0.58, 67.0 M |

Three things follow.

One statement made earlier in this session is wrong and is corrected here: it is not true that no frozen comparator
meets the frozen target. Added central capacity meets it for both products once it is searched over the same
inventory space the design-space strategies were given, and it does so at roughly 60 percent of its declared-space
cost, because the optimizer reaches the tail requirement by buying inventory rather than capacity. Every winning
matched design sits at 253 to 365 days of safety stock with the base-stock review on.

The cost ranking among feasible architectures survives, but the margin narrows. Bright-stock postponement at 15.7 M
and the reserve-triggered contracted network at 16.5 M remain cheaper than added central capacity at 23.7 M for
sodium bicarbonate. That is a third, not an order of magnitude, and the contracted strategies have not been re-run
under a *narrower* space to test the symmetric question.

The distributed-node architectures are the one group the correction does not rescue. They improve sharply, from 0.58
to 0.85 tail probability for norepinephrine at 20.0 M against 35.4 M, but neither product reaches the requirement, and
for sodium bicarbonate the matched design costs more rather than less because the optimizer buys both capacity and a
year of stock. Under illustrative inputs, in this model, distributed manufacturing is not made feasible by giving it
the inventory freedom that makes the alternatives feasible.

Caveats. Four strategies were tested, not twenty, at 40 final runs rather than 100, so the tail probability carries a
binomial standard error of about 0.047 and the two 0.90 results sit exactly on the requirement. The matched space is
itself a choice: it adopts the design-space strategies' declared inventory freedom as the common standard rather than
the comparators'. The opposite test, narrowing the design-space strategies to the comparators' space, has not been run
and would be the honest completion of this check.
