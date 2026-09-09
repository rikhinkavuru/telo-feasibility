# Inventory-capacity hybrids: does holding stock substitute for holding capacity?

Deliverable 16 of `docs/design_space/ASSIGNMENT.md` (Phase B family 8, Phase D, Phase E).

## 1. Question and banner

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input behind every run quoted here is tier 5 (illustrative), so everything below is model behavior under those inputs and nothing below is a statement about sterile-injectable manufacturing in the world. All sixteen regulatory gates in `config/regulatory_gates.yaml` (G01 to G16) are UNCERTAIN, so `eligibility` is `NO_CONCLUSION` for all twenty strategies (`results/design_space/ds_post_R008/summary.json` `meta.eligibility`) and no design here can receive a favorable decision class.

The question is narrow and internal: **inside this engine, how much safety stock buys the same tail service as how much reserved or expandable capacity, what does each side cost, and where does the answer come from the model rather than from the design?**

| id | what it is | stock levers | capacity levers |
|---|---|---|---|
| S13 | contracted base supply plus rotated reserved surge plus reserve inventory (`virtual_network`) | `safety_stock_days` 30-365, `site_fg_days` 30-180, `region_base_stock` | `capacity_factor` 0.9-1.3 scaling all three declared sites; firm second source at 365 d; one reserved CDMO line |
| S15 | capacity-adequate buffer-payable presentation, inventory only, no new plant (`product_selection`) | `safety_stock_days` 30-365, `site_fg_days` 5-180, `material_target_days` 30-180, `region_base_stock` | none; one incumbent line at status-quo scale |
| S16 | reserve-triggered campaign network on contracted registered capacity (`inventory_capacity_hybrids`) | `safety_stock_days` 10-365, `region_base_stock` | two contracted lines at scale 0.6, 540 d qualification, `campaign_batches` 1-12, `activation_threshold_days` 3-90 |
| S1 | frozen comparator "Additional safety stock" | `safety_stock_days`, `site_fg_days` 5-60, `material_target_days` | none |
| S4 | frozen comparator "Additional centralized capacity" | `safety_stock_days` 10-120 | `capacity_factor` 0.8-2.5 plus a second built site at 730 d |

S11 (postponement), S17 (warm standby) and S19 (upstream-first) also pair stock with reserved capacity and appear in the tables below, but are not analysed leg by leg here. Sources: `config/strategies/design_space.yaml`, `config/strategies/illustrative_baseline.yaml`, and the `bounds` block of each `results/optimization/opt_20260903T220534Z/<product>__<strategy>.json`.

**Coverage against the six variants the assignment names for family 8**, stated so the gaps are visible rather than silent:

| assignment variant | carried by | analysed leg by leg here |
|---|---|---|
| regional stock plus centralized expansion | S13 (regional stock plus `capacity_factor` on three declared sites); S1 and S4 as the frozen split of the same pair | yes, sections 3.1 and 3.3 |
| strategic inventory plus reserved capacity | S16 (regional stock plus two contracted lines with an activation trigger); S13's reserved CDMO leg | yes, sections 3.3 and 3.4 |
| dual sourcing plus regional inventory | S9 and S18, both of which search `safety_stock_days`, `material_target_days` and `region_base_stock` alongside a second finished-dose or contract-mandated source | **no.** The joint design is not run here; the two legs are reported separately in `feasibility_regions.md` section 6 (families 9 and 10) |
| distributed nodes plus a shared national reserve | **no configured strategy.** `prior_art_review.md` records the position as `novel_combination (uncertain)` with no implementer found (F8-S01, F8-S03, F8-S08, F8-S33), and the engine has no national reserve object distinct from regional stock (MD-15 forbids pooling across presentations) | no |
| rotating hospital inventory plus prequalified emergency campaigns | S16 is the campaign half; the rotation half has no representation, because the engine has no third-party holder, no consignment and no FEFO exchange with a customer's shelf (item 3 below) | half, section 3.3 |
| API and component reserves plus finished-product inventory | S19 (`material_target_days` plus an exercised standby line); the material half is present in every design through `material_target_days` | **no.** MD-1 puts the wrong sign on the material lead, so the upstream half of a reserve cannot be priced (item 1 below) |

## 2. What the model can and cannot represent for this family

**Can.** Regional order-up-to under two review rules; site finished-goods and raw-material targets; explicit lot expiry with FEFO issue and a measured `expiry_rate`; a carrying charge on finished and raw stock; reserved lines with an activation trigger, a 21-day activation lead, an activation failure probability, an exercise cadence, a reservation fee and take-or-pay; commissioning and expansion clocks that start at the first measured day (R008).

**Cannot, and each one bites this family.**

1. **One order-up-to policy for two different things.** Raw material and finished goods both run on `(target_days + lead) x daily demand` with no lot sizing against a whole-batch draw. Defect MD-1 is open, so the material buffer scales with the lead time and shortening a lead can reduce service. The sign is not stable across cells, which is worse than a wrong sign everywhere: at the optimized designs `loo:api_lead_time` moves fill *down* in five of the six cells of S13, S15 and S16 (sodium S13 -0.000742, S15 -0.001858, S16 -0.000952; norepinephrine S13 -0.001020, S16 -0.000149) and *up* in the sixth (norepinephrine S15 +0.000385), and the two frozen comparators split by product as well (sodium S1 -0.004752, S4 -0.000349; norepinephrine S1 +0.002575, S4 +0.001141; `results/ablation/abl_post_R008/attribution.csv`). A lead-time factor with no guaranteed sign cannot price the upstream half of a reserve.
2. **Shelf life is one number per product**, 24 months for both dossier products. No stability by presentation, no shelf-life extension, no lot-specific extended use dates.
3. **No rotation with a hospital or wholesaler.** No third-party holder, no consignment, no FEFO exchange with a customer's shelf, and no purchased-finished-goods price line, so S15's cost is the incumbent's production cost rather than Telo's cost of goods (its own `notes`; `falsification_register.csv` row S15-3).
4. **Opening stock is free.** `simulation._seed_initial_inventory` seeds `safety_stock_days x daily demand` at every region and `site_fg_days x daily site demand` at every non-reserved site with no ledger charge. At `safety_stock_days` 365 that is 1,200,000 units for sodium bicarbonate and 900,000 for norepinephrine, a full year of mean demand, at t0. R004 fixed how those cohorts are dated (MD-4); it did not charge for them.
5. **The commissioning metric misses contracted lines and expansions.** `simulation._commissioning_window_loss` skips reserved and 503B sites and reads `available_from_day` only, not `expansion_available_day`. S16 reports `capacity_days_lost_to_commissioning_fraction` 0.000 while both its contracted lines cannot make commercial product for 540 of the 1826 measured days (29.6%).
6. **Take-or-pay has no service channel** (MD-24, open): it enters `step8_costs` only.
7. **The exercise cadence is nearly unmeasurable on frequently activated lines** (MD-23, open), and `activation_failure_probability` is a per-plan constant with no link to cadence, so S16's readiness claim has no run behind it.
8. **One product per network and equal regional shares** (MD-15), so no pooling of a reserve across presentations.

## 3. Results

All figures are post-R008; every run made before 2026-09-03 is superseded and none is quoted. The binomial standard error of `p_meet` near q = 0.90 is 0.030 at n = 100 (optimization), 0.039 at n = 60 (ablation), 0.047 at n = 40 (dominance), 0.067 at n = 20 (the optimizer's screen and the threshold bisection) and 0.095 at n = 10 (the reversal map, which the driver runs at `runs // 4`).

### 3.1 Where the optimizer landed, and which variables sat on a bound

Frozen target (tau = 0.99, q = 0.90), `results/optimization/opt_20260903T220534Z/`. `H` = at upper bound, `L` = at lower bound. `region_base_stock` is a two-point integer, so it is at a bound by construction; it is marked but not counted as an artifact.

| product | strategy | status | design (best, else best_grid) | fill | p_meet | cost USD/yr |
|---|---|---|---|---|---|---|
| sodium | S1 | infeasible (n=20) | ss=365 H, fg=60 H, mat=180 H | 0.757266 | 0.00 | 12,669,241 |
| sodium | S4 | infeasible (n=20) | capf=2.5 H, ss=120 H, mat=180 H | 0.950635 | 0.00 | 38,144,769 |
| sodium | S13 | optimal (n=100) | ss=365 H, rbs=1 H, capf=0.9 L, fg=123.75 | 0.996385 | 0.90 | 19,334,584 |
| sodium | S15 | infeasible (n=20) | ss=365 H, fg=180 H, mat=180 H, rbs=1 H | 0.938653 | 0.10 | 13,157,250 |
| sodium | S16 | optimal (n=100) | ss=365 H, act=61, camp=1 L, rbs=1 H | 0.996974 | 0.94 | 16,475,242 |
| norepi | S1 | infeasible (n=20) | ss=113.75, fg=60 H, mat=180 H | 0.989009 | 0.80 | 12,753,933 |
| norepi | S4 | infeasible (n=20) | capf=2.5 H, ss=10 L, mat=180 H | 0.988673 | 0.60 | 37,844,159 |
| norepi | S13 | optimal (n=100) | ss=141.67, rbs=0 L, capf=0.9 L, fg=30 L | 0.995759 | 0.91 | 18,626,636 |
| norepi | S15 | infeasible at full n (n=100) | ss=344.06, fg=92.5, mat=105, rbs=0 L | 0.990056 | 0.73 | 12,569,122 |
| norepi | S16 | optimal (n=100) | ss=143.125, act=3 L, camp=1 L, rbs=1 H | 0.997419 | 0.93 | 15,890,651 |

**Bound-hugging, stated plainly.** 28 of the 36 design variables above sit exactly on a search bound; excluding the six `region_base_stock` entries, 22 of 30 do. That is a search artifact, not a result:

- `safety_stock_days` is at its 365-day upper bound in four of ten cells (sodium S1, S13, S15, S16) and at some bound in six of ten, the other two being sodium S4 at its own 120-day ceiling and norepinephrine S4 at the 10-day floor. That 365-day bound is half the 730-day shelf life rather than an evidence-based limit, so any claim of the form "the design wants a year of stock" is a claim about where the box ends.
- `capacity_factor` is at its **lower** bound (0.9) for S13 on both products and at its **upper** bound (2.5) for S4 on both. S13's search is buying its way out of capacity; S4's is buying capacity it cannot use in time.
- `campaign_batches` is at its lower bound (1) for S16 on both products at both service targets. The reserved-capacity lever is turned all the way down.
- S16 has neither `site_fg_days` nor `capacity_factor` in its search block, so it cannot buy always-on capacity at all; its only capacity lever is campaign size on two lines that do not exist until day 905.
- S1 and S4 were screened at n = 20 only, because neither produced a feasible incumbent to confirm at n = 100, so their rows are not comparable at face value with the n = 100 rows beside them.

**Two feasibility verdicts sit inside their own noise.** Sodium S13 reads `p_meet` exactly 0.90, zero runs of margin; norepinephrine S13 reads 0.91, one run, 0.35 SE; S16 reads 0.94 (1.7 SE) and 0.93 (1.2 SE). The same designs at n = 60 (`abl_post_R008` `by_key["base|..."]`) return sodium S13 `p_meet` 0.8667 (`p_meet_mcse` 0.0439) and `feasible` **false**, sodium S16 0.9000 (mcse 0.0387) and true. "Optimal" means an incumbent cleared the requirement on one 100-run confirmation, not that it is separated from the requirement.

### 3.2 Both service targets

At tau = 0.98 (`results/optimization/opt_20260903T231408Z_tau0.98/summary.json`) the family does not change shape: S13 and S16 clear on both products, S15 on neither, S1 and S4 on neither.

| product | S1 | S4 | S13 | S15 | S16 |
|---|---|---|---|---|---|
| sodium, tau 0.99 | infeasible | infeasible | optimal, 0.90 | infeasible | optimal, 0.94 |
| sodium, tau 0.98 | infeasible | infeasible | optimal, 0.95 | infeasible, closest fill 0.938653 | optimal, 0.91 |
| norepi, tau 0.99 | infeasible | infeasible | optimal, 0.91 | infeasible at full n, 0.73 | optimal, 0.93 |
| norepi, tau 0.98 | infeasible at full n, 0.73 | infeasible | optimal, 0.90 | infeasible at full n, 0.82 | optimal, 0.93 |

Relaxing the mean-fill target moves sodium S16's tail probability *down* (0.94 to 0.91) because the optimizer re-selects a different cheapest incumbent. The comparison is between two searches, not two worlds.

### 3.3 The substitution, measured

The clean surface is S13, where `capacity_factor` and `safety_stock_days` are searched jointly on one topology. Reading the n = 20 grid at `region_base_stock` = 1 and `site_fg_days` = 105 for sodium bicarbonate (`sodium_bicarbonate_8_4_50ml__S13.json` `evaluations`), with capacity from `ablation.network_capacity_units_per_year`:

**Selection rule for the table**, stated because the answer depends on it: each row is the *lowest* `safety_stock_days` at that `capacity_factor` whose evaluation reaches `p_meet` 0.90, taken over every evaluation in the file regardless of search stage. The right-hand columns give the cheapest 0.90 point at the same `capacity_factor` for comparison, and it is not always the same design.

| capacity_factor | always-on units/yr | lowest safety stock days reaching p_meet 0.90 | cost USD/yr at that point | cheapest 0.90 point instead | its cost USD/yr |
|---|---|---|---|---|---|
| 0.9 | 1,115,370 | 309.17 (refine1) | 19,377,083 | 365.00 (grid) | 19,335,544 |
| 1.1 | 1,363,230 | 141.67 | 21,813,000 | 141.67 | 21,813,000 |
| 1.3 | 1,611,090 | 30.00 | 24,086,980 | 141.67 (p_meet 0.95) | 24,002,180 |

**The exchange rate.** Under the minimum-stock rule, moving `capacity_factor` from 0.9 to 1.1 adds 247,860 units/yr of always-on nameplate plus 64,260 of contracted nameplate and substitutes for 309.17 - 141.67 = 167.50 days of regional safety stock at equal tail probability. 167.50 days of sodium demand is about 550,700 units of standing stock against 312,120 units/yr of added nameplate, so **about 1.8 units of standing finished-goods stock substitute for one unit per year of added nameplate**, and the stock route costs 2,435,917 USD/yr less. Read the same step off the grid stage alone, which is what an earlier draft of this table did, and the substitution is 223.33 days, 2.35 units per unit-year and a cost gap of 2,477,456 USD/yr; the difference between 1.8 and 2.35 is one refine-stage evaluation, and the two 0.90 readings at 309.17 and 365.00 days are tied inside one binomial standard error of 0.067 at n = 20. The next step (1.1 to 1.3) substitutes for only 111.67 more days, so under this rule the rate halves over one grid step and must not be extrapolated; under a cheapest-design rule the third row moves to 141.67 days and that halving disappears entirely.

**On the reserved-capacity lever proper the exchange rate is zero at the chosen operating point.** In S16 the only capacity variable is `campaign_batches`. At the optimizer's own `activation_threshold_days` of 61 days for sodium with `region_base_stock` = 1, raising `campaign_batches` from 1 to 12 moves `p_meet` by exactly 0.00 at every stock level (0.30 at ss=187.5, 0.70 at 276.25, 0.90 at 365, identical for camp 1, 5, 8 and 12). At a 3-day trigger the same 11 extra batches move `p_meet` 0.15 to 0.65, which against a stock slope of 0.001127 per day is about 40 days of safety stock per campaign batch. So the answer to "how many days of stock buy what one unit of reserved capacity buys" is **between 0 and about 40 days per campaign batch, and 0 at the design the optimizer selected**. A campaign batch recurs at every activation while stock is a standing position, so the two are not directly commensurable in units; the zero at the selected design is the finding, and it is why `campaign_batches` sits at its lower bound in all four S16 cells.

**The review rule, not the stock level, moves the tail.** Same S16 sodium grid at `activation_threshold_days` 61 and `campaign_batches` 1: with `region_base_stock` = 0 (frozen reorder rule) `p_meet` is 0.00 at all five stock levels including 365 days; with `region_base_stock` = 1 it runs 0.00, 0.00, 0.30, 0.70, 0.90. The same pattern holds for S15 sodium at `site_fg_days` 180 and `material_target_days` 180: rbs=0 gives fill 0.789019 and `p_meet` 0.00 at ss=365, rbs=1 gives 0.938653 and 0.10. This is defect MD-3, a hard-coded rule the protocol never specifies and the frozen comparators cannot use. Under `falsification_register.csv` row S15-1 the pre-declared threshold is met: **S15's sodium advantage disappears when the review rule reverts to the frozen one, so on that product the architecture has no content beyond a model artifact.** On norepinephrine it partly survives (rbs=0, ss=365, fg=180, mat=180 gives `p_meet` 0.90 at n=20).

**Where the service comes from on the capacity-short product.** Capacity computed with `ablation.network_capacity_units_per_year` at the optimized designs:

| product | strategy | always-on units/yr | reserved nameplate units/yr | demand units/yr | annual gap | free opening regional stock |
|---|---|---|---|---|---|---|
| sodium | S0 | 963,900 | 0 | 1,200,000 | 236,100 | 202,740 |
| sodium | S1 | 963,900 | 0 | 1,200,000 | 236,100 | 1,200,000 |
| sodium | S15 | 963,900 | 0 | 1,200,000 | 236,100 | 1,200,000 |
| sodium | S16 | 963,900 | 1,101,600 | 1,200,000 | 236,100 | 1,200,000 |
| sodium | S13 | 1,115,370 | 289,170 | 1,200,000 | 84,630 | 1,200,000 |
| norepi | S16 | 1,156,680 | 1,321,920 | 900,000 | none | 352,911 |

S16's always-on capacity is byte-identical to S0's, and its contracted lines cannot make commercial product until day 905 of a 2191-day horizon, so over the first 540 measured days S16 *is* S0 plus a free opening position of one year of demand. That position covers 5.08 years of the 236,100 units/yr structural gap against a 5-year window. The corroborating number is `capacity_utilization` at the optimized designs: `abl_post_R008` `by_key["base|sodium_bicarbonate_8_4_50ml|S15"].capacity_utilization.mean` = 1.2180, so S15 delivers 121.8% of its own annual saleable capacity over five years, which is only possible by draining an opening position it was never charged for. Said plainly: **on the capacity-short product a material part of this family's measured advantage is an accounting gift, not an architecture.**

### 3.4 The price of each side

Inventory side. Expiry at the **optimized** designs is near zero everywhere in this family (n = 60, `abl_post_R008` `by_key["base|..."].expiry_rate.mean`): sodium S13 0.000000, S15 0.000000, S16 0.000000; norepinephrine S13 0.000632, S15 0.000000, S16 0.002272. That is not evidence that a deep buffer is cheap. It is evidence that the search avoided the corner where expiry is paid. At the **configured** designs (`sim_post_R008`), where deep stock meets adequate capacity under a daily base-stock review, expiry reaches 8.6% at norepinephrine S11 (0.086401, mcse 0.001670) and 12.4% at S17 (0.124132), against 4.8% at S13 and 2.4% at S16; sodium bicarbonate reads exactly 0.000000 in nine of the ten cells named in this document's tables and 0.000171 at S17 (mcse 0.000068, `ledger_failure_waste` 269 USD/yr), because a capacity-short network rarely holds stock long enough to age it; the one sodium bicarbonate cell outside those ten with any expiry is the 503B comparator S7 at 0.001814. The charge is understated regardless: expired units hit `ledger_failure_waste` at variable production cost (1.20 USD/unit sodium, 1.15 norepinephrine), so norepinephrine S13's 4.76% expiry costs 60,469 USD/yr on a 20.1M ledger. Carrying cost is small: `ledger_inventory_logistics.mean` is 437,098 USD/yr at sodium S13, 375,848 at S16 and 231,452 at S15 against 207,796 at S0, at `inventory_carrying_rate` 0.20 per year, which is 2.1% of S13's annual cost.

Capacity side, sweeping `take_or_pay_fraction` 0.0 to 1.0 at the optimized designs, n = 20 (`ds_post_R008/contract_scenarios.csv`):

| product | strategy | cost at 0.0 | cost at 1.0 | delta USD/yr | delta USD/unit | fill across sweep | p_meet across sweep |
|---|---|---|---|---|---|---|---|
| sodium | S16 | 16,023,285 | 16,936,104 | +912,819 | +0.73 | 0.997308, identical | 0.90, identical |
| sodium | S13 | 19,203,949 | 19,612,189 | +408,240 | +0.33 | 0.997143, identical | 0.90, identical |
| norepi | S16 | 15,373,394 | 16,423,137 | +1,049,743 | +1.12 | 0.997996, identical | 0.90, identical |
| norepi | S13 | 18,490,554 | 18,960,030 | +469,476 | +0.50 | 0.996660, identical | 0.95, identical |

The reservation fee is `reserved_capacity_fee_fraction` 0.30 of the line's notional annual cost (`config/global.yaml`), accruing only while the line exists (R007, MD-21). The whole contracted line item is `ledger_resilience_contracts.mean` 2,845,865 USD/yr at sodium S16 and 1,564,908 at sodium S13, against 3,618,121 at the frozen S3 comparator. **The instrument that pays for readiness buys exactly zero service in this engine.** That is MD-24, and it is why take-or-pay was removed from the S11 and S13 search blocks rather than optimized to zero.

### 3.5 Dominance, feasibility conditions, reversal

Dominance at n = 40 (`ds_post_R008/dominance.csv`; `../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_dominance.png` and `../../results/figures/design_space_ds_post_R008_norepinephrine_1mgml_4ml_dominance.png`): S16 is on the cost-service frontier for **both** products; S13 for **neither**, dominated by S11 and S16 on sodium and by S17 on norepinephrine; S15 is on both frontiers while infeasible on both, which is what the frontier definition does with a cheap design that never clears the tail.

Feasibility conditions (`ds_post_R008/thresholds.csv`, bisection at n = 20, so each boundary carries a 0.067 binomial standard error):

| condition | S13 sodium | S16 sodium | S13 norepi | S16 norepi |
|---|---|---|---|---|
| max annual demand | 1,246,875 | 1,246,875 | 885,938 | 926,563 |
| min batches per site-year | 43.125 | 43.125 | 38.125 | 43.125 |
| max common-cause events per group-year | 0.103 | 0.173 | 0.156 | 0.138 |
| max supplier disruption rate | feasible everywhere | 0.591 | feasible everywhere | 0.437 |
| min shelf life (months) | 13.125 | feasible everywhere | feasible everywhere | feasible everywhere |
| max raw-material lead (days) | feasible everywhere | feasible everywhere | feasible everywhere | infeasible everywhere |
| max activation latency (days) | feasible everywhere | 22.73 | feasible everywhere | feasible everywhere |
| max fixed QA cost per node | feasible everywhere | feasible everywhere | feasible everywhere | feasible everywhere |

Three readings. The demand headroom is thin: sodium's 1,246,875 sits 3.9% above the base of 1,200,000, inside the interval a real utilization measurement would carry. S16 sodium's activation-latency threshold of 22.73 days sits essentially on the base value of 21 days, so the design has no margin on the one lead time that distinguishes contracted from built capacity. Norepinephrine S13's 885,938 lies *below* its own base demand of 900,000 while the same design is `feasible` at base in the n = 40 dominance run; the bisection path is non-monotone (`p_meet` 0.95 at 865,625, 0.80 at 906,250, 0.85 at 987,500), so that threshold is noise, not a condition.

Decision reversal (`ds_post_R008/reversal.json`, 27 cells per product over demand, common-cause rate and fixed QA cost, **n = 10 paired runs per cell**, because `scripts/run_design_space_analysis.py` passes `runs=args.runs // 4` and the run used 40 for dominance; every `p_meet` in the artifact is a multiple of 0.1, which is the granularity of 10 runs). The binomial standard error at q = 0.90 and n = 10 is **0.095**, so one run is 0.1 of the tail probability and a one-strategy change in a feasible set is one run. Across all 54 cells the cheapest feasible design is S15 in 15, S11 in 12, S3 in 6, S1 in 3, and nothing is feasible in 18. **Neither S13 nor S16 is ever the cheapest feasible design in any cell**, though both are feasible in most; at n = 10 that statement is resolved to no better than one run per cell. Preference also reverses on the dependence axis: at sodium demand 1,200,000 the preferred design is S11 at common-cause rates 0.02 and 0.1 and S3 at 0.3, where only S3 and S9 stay feasible at all. Figure: `../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_reversal_fixed_qa_labor_per_node3e+06.png`.

### 3.6 The pre-declared falsification tests this run can answer

- **S16 claim 1** (register data row 22), "beats frozen S3 by more than two binomial standard errors at matched annual cost": not falsified **on the n = 100 optimizer records**, which is not the run the test names. Sodium `p_meet` 0.94 against S3's 0.81, a difference of 0.13 against an independent-sample standard error of 0.046, so 2.8 SE, at 3,551,569 USD/yr **less** than S3; norepinephrine 0.93 against 0.82, 2.4 SE, at 1,444,949 USD/yr less. Common random numbers make the paired standard error smaller than the one used, so that much is the conservative reading. **The declared matched-annual-cost form of the test was not run**, and the 40-run dominance evaluation of the same designs gives sodium 0.925 against S3's 0.85, a gap of 0.075 that is inside two standard errors at n = 40 (SE 0.047). The register row records both facts in its `result_pointer`; the row stands on the higher-n run alone.
- **S15 claim 1** (register data row 19): falsified on sodium bicarbonate, not falsified on norepinephrine (section 3.3). The register's status for that row is the blanket "falsified in the model", which is the sodium half; the product split belongs in it. The norepinephrine "not falsified" reading rests on an n = 20 grid point with a 0.067 standard error whose n = 100 confirmation in the same run directory returned `p_meet` 0.73 (`opt_20260903T220534Z`, `norepinephrine_1mgml_4ml|S15`, `infeasible_at_full_n`), which section 6 item 6 records; read it as unresolved rather than as a pass.
- **S13 claim 1** (leg-by-leg ablation of the rotated reserved surge, the firm second source and the review rule) has no run: the ablation battery carries the Phase A factor list, not a leg list. The nearest proxy, `loo:contract_insufficiency`, moves sodium S13's `p_meet` by +0.0167 at n = 60 against a standard error of 0.039, which resolves nothing. **S13's distinctive leg remains untested.**

## 4. Commercial conditions

Computed with `src/telo_feasibility/contracting.py` at the **optimized** designs, run from the package root. Inputs passed: `annual_cost_usd` and `mean_cost_per_unit` from `opt_20260903T220534Z`; `delivered_units_per_year` = `mean_cost / mean_cost_per_unit`; `capacity_units_per_year` = `delivered / mean_fill` (the `scripts/build_contract_table.py` convention); `variable_cost_usd_per_unit` = `variable_materials` + `variable_conversion` (1.20 sodium, 1.15 norepinephrine); `reference_annual_cost_usd` = the S0 best_grid cost in the same run (12,928,316 sodium, 12,766,470 norepinephrine); `fixed_and_resilience_cost_usd` carried over from `sim_post_R008` for the same product and strategy. That carry-over is exact for S15 and S16, whose optimized designs change no cost-bearing structural variable, and approximate for S13, whose `capacity_factor` moves 1.0 to 0.9.

| product | strategy | break-even price USD/unit | resilience premium vs S0 USD/unit | share of demand that must be committed | max fixed+resilience cost at 50% committed USD/yr |
|---|---|---|---|---|---|
| sodium | S1 | 13.37 | -0.27 | 0.688 | 7,614,499 |
| sodium | S15 | 11.20 | +0.19 | 0.837 | 6,257,690 |
| sodium | S16 | 13.18 | +2.84 | 0.887 | 7,510,377 |
| sodium | S13 | 15.48 | +5.13 | 0.965 | 8,950,160 |
| sodium | S4 | 31.90 | +21.09 | 0.645 | 19,308,048 |
| norepi | S15 | 13.50 | -0.21 | 0.902 | 5,807,002 |
| norepi | S16 | 16.94 | +3.33 | 0.902 | 7,425,174 |
| norepi | S13 | 19.89 | +6.26 | 0.981 | 8,812,199 |
| norepi | S4 | 40.60 | +26.90 | 0.669 | 18,596,778 |

**Answered.** The capacity-carrying hybrids S13 and S16 need a resilience premium of 2.84 to 6.26 USD per delivered unit over the status quo and 89% to 98% of realized annual demand under commitment (S16 0.887 sodium and 0.902 norepinephrine, S13 0.965 and 0.981) to break even at their own break-even price. The inventory-only S15 is a different design and belongs in a different sentence: its premium is +0.19 on sodium bicarbonate and -0.21 on norepinephrine, and its committed share is 0.837 and 0.902. The pure-capacity comparator needs 21 to 27 USD per unit, an order of magnitude more. The take-or-pay sweep prices the capacity side directly at 0.33 to 1.12 USD per unit to move take-or-pay from nothing to full, for no service.

**Not answered, and these decide it.** No price anyone will pay is known, so `ContractTerms.missing()` returns `price_required_usd_per_unit` for every design here and all of them are recorded as **not contractable, stated**. Two labelling defects travel with the table: the `capacity_units_per_year` the script computes is `delivered / fill`, which is realized demand, so `implied_utilization` is numerically identical to `fill_rate` in every row of `results/design_space/contract_conditions_sim_post_R008.csv` (sodium S16 0.9117403837294629 against `fill_rate.mean` 0.911740), and the "minimum contracted utilization" is therefore a share of demand, not of installed capacity. And with no supplied price the break-even price is used, so committed volume equals delivered volume by construction, which the CSV's own `notes` column states on every row.

## 5. Prior art and landscape position

The stock leg is occupied. Six-month buffer inventory is sold today by Civica against committed volume of about 50% for three to ten years (F8-S14, F10-S01, LNPM-S03) and by Vizient NES Reserve with no up-front investment and no programme fee across more than 180 NDCs (LNPM-S19, F10-S05). Regional stock plus central expansion is classified `already_implemented` in the cross-family novelty matrix (F8-S10, F8-S11, F8-S13, F8-S32), as are upstream API plus finished-dose reserves (F8-S12, F8-S33, F8-S06, F9-S18) and government-mandated stockholding outside the US (F8-S32, F8-S33, F8-S34). Paid third-party holding of rotating stock is `already_implemented` through DLA Warstopper and the SNS vendor-managed inventory contracts, and the SNS programme was terminated in 2017 as not cost-effective, with the recorded lesson that rotation works only where the commercial market can absorb the reserve before expiry (F8-S03, F10-S24). S15's revenue mechanism rests on the CMS FY2025 IPPS buffer payment, which reaches only hospitals of 100 beds or fewer not part of a chain, about 500 hospitals, and does not pay for a buffer newly established while the medicine is in shortage (F8-S16, F8-S17, LSD-S3, F12-S08).

The capacity leg is occupied on the government side and empty on the commercial side. Reserved CDMO capacity has published government prices (F7-S04, LGOV-S28), and the most fully documented failure in the collected material is CIADM: two of three sites with none of their capacity used and the third at 7%, about 4M USD per year of task orders against a stated ready-state requirement of 30M to 60M, one site terminated after cross-contamination, none meeting the surge goal (F8-S09, F7-S01). No US hospital system, GPO or state was found to have paid a standing reservation fee for sterile generic capacity (F3-S28, prior-art open question 17), and FDA's Drug Shortages Task Force records that most generic manufacturers cannot afford to support redundant capacity (F7-S16).

What is unoccupied is the **coupling**. Prior-art section 6.4 records campaign rotation across several prequalified sites as a network scheduling policy with no found instance, and the novelty matrix lists "rotating hospital inventory linked to a pre-committed emergency campaign trigger" as `novel_combination (uncertain)`, the halves existing separately with nothing linking depletion to a campaign trigger (F8-S17, F8-S32, F8-S33, F8-S09, F8-S44). That is S16's claim and the only novelty claim this family can make. It is weak on its own terms: the moat is contractual rather than technical, a GPO can write the same contract, three GPOs cover more than 90% of US hospitals and Vizient alone serves more than 65% of acute-care providers (LSIM-S20, LSD-S11), and coordination across independent owners is an antitrust question before it is a product (F2-S63, F2-S64).

## 6. What is weak, and what evidence would change the answer

Ordered by how much of the family's result each carries.

1. **Free opening inventory.** Every design here is handed `safety_stock_days x daily demand` at t0 with no charge, a full year of demand at the chosen designs. On sodium bicarbonate that covers 5.08 years of the network's own structural gap over a 5-year window, and S15 delivers 121.8% of its annual saleable capacity as a result. **Change it by** charging opening units at variable materials plus conversion on day 0 and re-running the battery. In-model, no human input. Until it lands, no cost or service comparison between a deep-stock design and a capacity design in this package is sound.
2. **The regional review rule (MD-3).** `region_base_stock` decides the sodium result outright for S15 and S16. The rule is hard-coded, unspecified by the protocol, unavailable to the frozen comparators, and backed by no config parameter. **Change it with** evidence on what replenishment review policy and order-up-to level real regional stocking points run: **HA-40** (queue rank 6; HA-20 is the source pool), reviewed by **HA-33**.
3. **Raw and finished goods share one policy and MD-1 is open**, so the material buffer scales with the lead time and `api_lead_time` carries the wrong sign in every cell of this family. The upstream half of a reserve, which families 8 and 9 both depend on, cannot be priced here. **Change it by** decoupling the order-up-to level from the lead time under its own revision and re-optimizing; supplier lead-time and price evidence is **HA-12**, reserved-capacity and node cost evidence is **HA-13**.
4. **Shelf life is one number and there is no rotation partner.** No stability by presentation, no consignment, no hospital-shelf FEFO exchange, no purchased-finished-goods price line, and expired units charged at production cost. A buffer held on someone else's balance sheet, which is what Civica and Vizient actually sell, cannot be represented at all. **Change it with** whether an eligible hospital would accept a third-party-held buffer on its cost report under 42 CFR 412.113(g) and what it would pay (**HA-20**, **HA-33**), and a wholesale acquisition or transfer price for the presentation (**HA-11**, **HA-24**).
5. **The capacity side is either inert or invisible.** Take-or-pay changes no service quantity (MD-24); the exercise cadence is unmeasurable on frequently activated lines (MD-23); `activation_failure_probability` has no link to cadence; and the commissioning metric excludes contracted lines, so S16 reports 0.000 window loss while both its lines are unavailable for 29.6% of the measured window. **Change it by** adding a readiness-decay hazard as a function of days since the last qualified batch plus a requalification lead on failure (the decay rate itself is **HA-21** and **HA-22**), and by extending `_commissioning_window_loss` to reserved sites and to `expansion_available_day` (in-model).
6. **Search bounds and screen size.** 22 of 30 non-binary design variables sit on a bound; the 365-day stock bound is half the shelf life rather than evidence; S16 can search neither `capacity_factor` nor `site_fg_days`; and each cell's incumbent is chosen by minimum cost on a 20-run screen whose binomial standard error near q = 0.90 is 0.067 (MD-11, open). Norepinephrine S15 is the visible casualty: nine grid cells at `region_base_stock` = 1 and `safety_stock_days` = 365 read `p_meet` 1.00 on the 20-run screen and none was ever confirmed, because the cheapest screen-feasible design was a `region_base_stock` = 0 point reading 0.90 at 12,585,215 USD/yr against 13,009,610 for the otherwise identical rbs = 1 point, and it then returned 0.73 at n = 100. **Change it by** widening the bounds, adding `capacity_factor` and `site_fg_days` to S16, raising the screen to n >= 60, and giving the tie-break an MCSE tolerance under its own revision. All in-model.
7. **No value of information for this family.** `results/sensitivity/` is built on `opt_20260902T043854Z`, covers sodium bicarbonate and S0 to S7 only, and predates every fix in R004 to R008, so it is superseded and no number from it is quoted here. The EVPPI ranking that would say whether demand, the review rule or reserved-line readiness is worth measuring first **does not exist for S11 to S19**. Re-running it is in-model and is the highest-leverage missing artifact for this deliverable.
8. **Two ledger conventions still misstate who pays.** Reserved lines carry no capital, fixed operations or validation on Telo's ledger (R004, MD-14), which understates them because a reservation fee excludes tech transfer, process and analytical development and lot release testing (F7-S04); and the incumbent central site's full capital and fixed cost is charged to the network even where Telo owns nothing (MD-14 residual). No cost ranking in section 4 should be quoted until a labelled Telo-only companion design is run with `capital_multiplier`, `fixed_cost_multiplier` and `validation_multiplier` at 0.0 on the incumbent line. **Change it by** running that companion design, which is in-model and needs no person, and by obtaining what a reservation fee does and does not cover at a named US line, which needs one: **HA-13**, **HA-21**.

**One human-dependent item in this family had no queue entry when this section was written; it is now HA-38, rank 15.** Nobody has been asked whether a purchaser will fund standing availability for a civilian generic injectable separately from units shipped. Prior-art open question 17 and family 7's standing instruction both say to assume the answer is no until a purchaser says otherwise, and without it the entire capacity leg of every design here is unfunded by construction. It is recorded in `../audits/07_human_action_queue.md` as **HA-38** at rank 15, beside **HA-24** and **HA-33**, with the model entry point `ContractTerms.price_required_usd_per_unit` and the reversible result every row of section 4.
