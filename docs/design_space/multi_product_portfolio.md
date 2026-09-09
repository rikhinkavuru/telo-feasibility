# Multi-product portfolio analysis (deliverable 15, assignment family 6)

## 1. Question and banner

PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS. Every input behind every number here is tier 5 (illustrative),
so every result is the behaviour of this model under provisional assumptions and not a statement about the world. All
applicable regulatory gates stay UNCERTAIN, and UNCERTAIN is never PASS (`results/manifests/sim_post_R008.json`,
`gate_outcomes.S10` = G01 to G07, G13, G14). Nothing here asserts an interview, partner, customer, quote or review.

The question, narrower than the assignment's family 6 heading: when a design attributes only part of a host site's
capacity and part of its fixed and capital cost to this product, what happens to cost per delivered unit, to
utilization and to feasibility, and what must a purchaser commit for such a node to cover its fixed cost?

Two configured designs declare shares below 1 (`config/strategies/design_space.yaml`).

| strategy | sites below 1.0 | `portfolio_capacity_share` | `portfolio_fixed_cost_share` | other |
|---|---|---|---|---|
| S10 "split tenancy across two independent multi-product hosts" (the configured name; see the note below on what "independent" does not mean here) | `shared_suite_1` (R3), `shared_suite_2` (R4) | 0.20 | 0.20 | `validation_multiplier` 5.0 at both, which undoes the share so each host pays one full product-specific validation |
| S17 rotating prequalified campaign network | `cmo_R2`, `cmo_R3`, `cmo_R4` | 0.50 | 0.50 | reserved lines |

**The two hosts are not independent in this engine, and "independent" in S10's name is a description of ownership,
not of failure.** `config/strategies/design_space.yaml` declares three common-cause groups on all three of S10's site
plans: `cc_vial_1`, `cc_stopper_1` and `cc_quality`. `shared_suite_1` carries cc_api_1, cc_vial_1, cc_cdmo_1,
cc_geo_R3, cc_stopper_1, cc_quality; `shared_suite_2` carries cc_api_2, cc_vial_1, cc_cdmo_2, cc_geo_R4,
cc_stopper_1, cc_quality; `central` carries cc_api_1, cc_vial_1, cc_geo_R1, cc_stopper_1, cc_quality. Only the API
tier and the geography differ. That is what section 3.5's binding conditions measure: the tightest supplier condition
in the whole grid sits on this design because a vial and a stopper source and one disposition function span all three
sites.

Every other site plan in S0 to S19 sits at 1.0. S17's fixed-cost share is inert: under MD-14 (revision R004) a
reserved line Telo does not own carries no capital, fixed operations or validation, only its reservation fee, and
building the strategy confirms `site_capital_usd` = 0 at all three lines with a 1,493,972 USD/yr fee each. S10 is the
only configured design where portfolio accounting is live on both axes, so it carries this work.

## 2. What the model can and cannot represent for this family

The two fields enter at exactly four places in `src/telo_feasibility/strategies.py`: line 477 (`batches_per_year =
nominal_batches * scale / bsf * plan.capacity_share`), line 485 (capital), line 492 (fixed operations) and line 498
(validation). That is the whole mechanism, and it is an attribution rule, not a portfolio. The engine runs one product
per network (`simulation.run_paired`, defect MD-15), so a portfolio here is a share of one node's capacity and fixed
cost attributed to this product and the other products exist only as the arithmetic that produced the share. Absent,
in the order it bites:

1. **Product-to-product changeover.** `changeover_days` is added to every batch on a single-product line
   (`production.py:80`), so it is a same-product setup; the `changeover_burden` row in `thresholds.csv` maps to it and
   is not the family 6 changeover.
2. **Cleaning validation and campaign length.** Annex 15 chapter 10 makes campaign length the basis of cleaning
   validation (10.9) and forces worst-case re-assessment when a product is added (10.10) (F6-S04). Neither is a cost
   object or a time cost here.
3. **Cross-contamination control and product-family segregation**, a hard gate in the world and absent here: 21 CFR
   211.42(c) and (d), 21 CFR 211.67 (F6-S01, F6-S02), the EMA HBEL guideline and its 2018 Q&A (F6-S07, F6-S08), EU GMP
   Chapters 3 and 5 (F6-S05, F6-S06).
4. **Minimum campaign size.** FDA's 2004 aseptic guidance sets a media-fill starting point of 5,000 to 10,000 units
   and, for batches under 5,000, a media fill at least equal to the maximum batch size (F6-S11). No source gives a
   minimum economic campaign size (F6 section 9) and no parameter exists.
5. **Correlated shortages across the portfolio.** An event removes this product's attributed share; the other 80
   percent of the host is invisible, so the correlation the architecture creates cannot be scored.
6. **Shared QC laboratory queueing.** Release components are per product and never contend; FDA's draft RMP guidance
   names laboratory availability as a vulnerability (F6-S12).

`bottleneck_decomposition.md` section 7 records MD-15 as "scope, and the largest unquantified distortion in the cost
comparison"; `architecture_taxonomy.md` line 35 marks family 6 coverage partial for the same reason. Both known biases
point one way and neither is quantified. Cost per delivered unit at a portfolio node is biased low, because the node
pays a share of fixed cost and nothing for the changeover, cleaning validation, media fills and scheduling that made
the share possible; tail risk is biased low, because a plant-level event is modelled as removing one product rather
than a whole tenancy. Nothing in section 3 corrects for either. Separately, a ledger convention (MD-14 residual,
recorded in S10's `capital_requirement` field) charges `central`'s full capital, fixed operations and validation to
this network, so S10's absolute cost is not a Telo-only cost.

## 3. Results

The paired simulation runs each strategy at its configured design variables; the ablation, dominance, threshold and
reversal runs use the optimized designs from `opt_20260903T220534Z` (`meta.designs`). All runs are post-R008, master
seed 20260901, five measured years after a 365 d warm-up. S9 (dual finished-dose source, two full sites) is the
matched comparison: it adds capacity the way S10 does, at full share.

### 3.1 Paired simulation, configured designs

`results/simulation/sim_post_R008/summary.json`, `by_strategy["<product>|<strategy>"]`, `n_runs` 100.

| product | strategy | `fill_rate.mean` (mcse) | `meets_fill_rate.mean` | `cost_per_delivered_unit.mean` (mcse) | `annual_total_cost.mean` | `capacity_days_lost_to_commissioning_fraction.mean` |
|---|---|---|---|---|---|---|
| norepinephrine | S0 | 0.94422 (0.00455) | 0.13 | 14.291 (0.062) | 12,662,901 | 0.0000 |
| norepinephrine | S10 | 0.98525 (0.00212) | 0.63 | 18.960 (0.037) | 17,563,887 | 0.0551 |
| norepinephrine | S9 | 0.99131 (0.00199) | 0.78 | 27.418 (0.059) | 25,554,634 | 0.0999 |
| sodium bicarbonate | S0 | 0.71574 (0.00394) | 0.00 | 14.465 (0.068) | 12,925,986 | 0.0000 |
| sodium bicarbonate | S10 | 0.89849 (0.00434) | 0.00 | 16.228 (0.069) | 18,259,848 | 0.0551 |
| sodium bicarbonate | S9 | 0.94175 (0.00239) | 0.00 | 22.408 (0.054) | 26,473,027 | 0.0999 |

The commissioning column follows from the share: both S10 hosts and S9's second source declare the same 365 d lead,
but the R008 clock starts at the first measured day and the metric is capacity-weighted, so S10 loses 0.0551 of the
window against S9's 0.0999 because a smaller share of network capacity is waiting.

### 3.2 Utilization and cost per unit

`results/ablation/abl_post_R008/summary.json`, `by_key["base|<product>|<strategy>"]`, `n_runs` 60, at the optimized
designs. `capacity_utilization` is throughput over the capacity attributed to this product (post MD-9), so at S10 the
denominator is the 0.20 shares, not the host lines. S0 reads 0.7971 utilization at 13.833 USD per unit
(norepinephrine) and 0.9343 at 14.372 (sodium bicarbonate).

| product | strategy | `capacity_utilization` (mcse) | `cost_per_delivered_unit` (mcse) | `fill_rate` (mcse) |
|---|---|---|---|---|
| norepinephrine | S9 | 0.4259 (0.0008) | 24.758 (0.042) | 0.99873 (0.00127) |
| norepinephrine | S10 | 0.5837 (0.0009) | 18.740 (0.025) | 0.99241 (0.00091) |
| sodium bicarbonate | S9 | 0.6821 (0.0009) | 19.483 (0.026) | 0.99979 (0.00016) |
| sodium bicarbonate | S10 | 0.9362 (0.0022) | 14.846 (0.029) | 0.99506 (0.00220) |

Against the matched full-share design, attributing 20 percent of two host lines moves attributed utilization from
0.4259 to 0.5837 (norepinephrine) and 0.6821 to 0.9362 (sodium bicarbonate) and cost per delivered unit from 24.758 to
18.740 and 19.483 to 14.846 USD per unit, both cost gaps far outside their MCSEs, while service falls by 0.00632 and
0.00473 fill, about five and about two times the larger MCSE in each pair.

### 3.3 Which cost block moves, and which does not

Ledger means from the same simulation keys; the same magnitudes appear as `loo_delta_annual_total_cost` for
`fixed_quality_cost`, `capital_cost` and `replicated_validation_cost` in
`results/ablation/abl_post_R008/attribution.csv`.

| block (USD/yr) | S0 | S10 | S9 | note |
|---|---|---|---|---|
| `ledger_fixed_site_operations.mean` | 3,119,412 | 3,919,594 | 6,653,536 | shared: two hosts add 0.80M, not 3.53M |
| `ledger_capital_annualized.mean` | 6,703,202 | 9,307,128 | 14,524,709 | shared |
| `ledger_product_site_launch.mean` | 650,982 | 1,952,945 | 1,952,945 | not shared: S10 pays what two full sites pay |

The validation row is the design's own choice: `validation_multiplier` 5.0 exactly undoes the 0.20 share, because each
product on a line needs its own process validation and media fills (F6-S11, F6-S04). Sharing quality staff and capital
is cheap in this model; sharing validation is not on offer. The same split appears in
`results/design_space/ds_post_R008/reversal.json` as a slope: at base demand and base common-cause rate, the cost
difference between `fixed_qa_labor_per_node` 6,000,000 and 1,500,000 divided by the 4,500,000 span gives the
site-equivalents of fixed QA labour this product carries, which is S0 1.040, S16 1.274, S10 1.307, S13 1.309, S17
1.713, S9 1.917, S2 3.337. S10 carries about a third of a site-equivalent more than the status quo while running two
extra registered sites. The mechanism has no service channel. Across all six S10 cells that differ only in
`fixed_qa_labor_per_node`, fill and p_meet are identical to the digit (norepinephrine at base demand and base common
cause 0.99262 and 0.80 at all three values, sodium bicarbonate 0.99521 and 0.90), so sharing fixed quality cost can
move cost and can never move feasibility here. The superseded sensitivity layer agrees structurally
(`results/sensitivity/summary.json`, `evppi.fixed_qa_labor_per_node` = 0.0; that run is dated 20260902T045142Z, covers
S0 to S7 only, and is superseded for quantitative use).

### 3.4 Feasibility, dominance and reversal

`results/design_space/ds_post_R008/dominance.csv` at tau 0.99, q 0.90, with the optimizer records from
`opt_20260903T220534Z` and `opt_20260903T231408Z_tau0.98`.

| product | `feasible` | `on_frontier` | `dominated_by` | optimizer at tau 0.99 | at tau 0.98 |
|---|---|---|---|---|---|
| norepinephrine S10 | False | False | S11; S16; S19 | `infeasible_at_full_n`, fill 0.99179, p_meet 0.83 | `infeasible_at_full_n`, 0.98676, 0.85 |
| sodium bicarbonate S10 | True | False | S11; S16 | `optimal`, cost 18,498,686, fill 0.99490, p_meet 0.90 | `optimal`, 18,405,292, 0.99334, 0.91 |

Sodium bicarbonate S10 clears at `p_meet` exactly 0.90 on the 100-run confirmation, zero runs of margin against a
binomial standard error of 0.030, so `optimal` here means an incumbent cleared the requirement once, not that it is
separated from it. The 40-run dominance evaluation of the same design gives 0.925, half a standard error of margin at
SE 0.047, and the 60-run ablation base gives 0.9167 (mcse 0.0357). That design also sits on two of its four search
bounds, `safety_stock_days` at the 365-day ceiling and `region_base_stock` at 1, so it is a corner of the box as well
as a feasible point (`opt_20260903T220534Z/sodium_bicarbonate_8_4_50ml__S10.json`).

Across all 54 cells of the decision-reversal grid (27 per product over demand, common-cause rate and fixed QA labour,
at 10 paired runs per cell, because the driver takes `runs // 4` of the 40 used for dominance)
S10 is never the preferred strategy; preferred entries are S11 in 12 cells, S15 in 15, S3 in 6, S1 in 3 and none in
18. S10 is in the feasible set in 3 of 27 norepinephrine and 15 of 27 sodium bicarbonate cells. At n = 10 the
binomial standard error on `p_meet` at q = 0.90 is 0.095 and one run moves the tail probability by 0.1, so those
membership counts are resolved to no better than one run per cell.

### 3.5 Feasibility conditions for S10

`results/design_space/ds_post_R008/thresholds.csv`, columns `threshold` and `direction`.

| input (`parameter_id`) | norepinephrine | sodium bicarbonate |
|---|---|---|
| `capacity_utilization` (`product.annual_demand_units`) | feasible below 601,563 u/yr | feasible below 1,190,625 u/yr |
| `fixed_qa_labor_per_node` (`product.fixed_qa_labor_usd_per_site_year`) | feasible everywhere, 1.5M to 6.0M | feasible everywhere |
| `node_capital` (`product.capital_usd_per_site`) | feasible everywhere, 15M to 100M | feasible everywhere |
| `common_cause_dependence` (`global.common_cause_events_per_year`) | feasible below 0.1381 | feasible below 0.1031 |
| `supplier_concentration` (`global.supplier_disruptions_per_supplier_year`) | feasible below 0.4539 | feasible below 0.2133 |
| `changeover_burden` (`product.changeover_days`) | feasible below 7.61 d | feasible below 6.48 d |
| `batches_per_site_year` (`product.batches_per_site_year_nominal`) | infeasible everywhere | feasible above 43.1 |
| `release_time` (`global.sterility_incubation_days`) | feasible below 15.5625 d | feasible everywhere, 14 to 18 d |
| `shelf_life` (`product.shelf_life_months`) | feasible above 16.78 mo | feasible above 12.375 mo |
| `raw_material_lead_time` (`product.material_lead_time_days`) | feasible above 59.53 d, the wrong sign (MD-1) | feasible everywhere |
| `activation_latency_days` (`global.reserved_capacity_activation_days`) | feasible everywhere, 7 to 60 d | feasible everywhere |
| `commissioning_days` (`global.node_commissioning_days`) | feasible everywhere, 365 to 1095 d | feasible everywhere |

All twelve swept inputs are listed. The last five were absent from an earlier draft of this table; the two
`feasible_everywhere` sweeps at the bottom say more about the sweep's reach than about the design, because both S10
hosts declare their own `commissioning_days` of 365 and S10 has no reserved site, so neither global reaches it.
**Shelf life** is worth stating explicitly because the assignment's family 6 list names it: the engine carries one
shelf-life number per product, 24 months for both dossier products, with no stability by presentation and no
lot-specific extended dating (MD-15's sibling limitation, section 2 item 2 of `inventory_capacity_hybrids.md`), so
the family's shelf-life question resolves here to a per-cell threshold on a single scalar and never to a portfolio
effect.

The two inputs the portfolio mechanism is meant to relieve, fixed QA labour and node capital, are feasible everywhere
and never binding; the binding conditions are demand, common-cause rate and supplier concentration, none of which the
mechanism touches. The `changeover_burden` row is a same-product batch setup, not campaign changeover. Figures, all
under `../../results/figures/`: `design_space_ds_post_R008_norepinephrine_1mgml_4ml_dominance.png`,
`design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_dominance.png`,
`design_space_ds_post_R008_norepinephrine_1mgml_4ml_reversal_fixed_qa_labor_per_node3e+06.png`,
`ablation_abl_post_R008_norepinephrine_1mgml_4ml_S10_fill_rate.png` and
`ablation_abl_post_R008_sodium_bicarbonate_8_4_50ml_S10_fill_rate.png`.

## 4. Commercial conditions

### 4.1 Network level

Source: `results/design_space/contract_conditions_sim_post_R008.csv`, built by `scripts/build_contract_table.py` from
`sim_post_R008`.

| product | strategy | `break_even_price_usd_per_unit` | `fixed_share_of_cost` | `resilience_premium_usd_per_unit` vs S0 | `committed_units_for_fixed_cost` | `min_contracted_utilization_at_break_even` |
|---|---|---|---|---|---|---|
| norepinephrine | S10 | 18.9545 | 0.8643 | 5.2890 | 852,574 | 0.9065 |
| norepinephrine | S9 | 27.4094 | 0.9052 | 13.8274 | 880,872 | 0.9366 |
| sodium bicarbonate | S10 | 16.1987 | 0.8313 | 4.7318 | 1,012,068 | 0.8067 |
| sodium bicarbonate | S9 | 22.3977 | 0.8738 | 11.4616 | 1,091,211 | 0.8694 |

### 4.2 Node level, with `contracting.minimum_contracted_utilization`

Computed in a Python heredoc from the package root. Inputs passed, all from configuration and the built runtime:
`discount_rate` 0.10 and `capital_economic_life_years` 10, so CRF 0.162745; `contribution_margin_usd_per_unit` = price
minus variable materials plus conversion cost, 1.15 per unit for norepinephrine and 1.20 for sodium bicarbonate;
`fixed_and_resilience_cost_usd` = CRF x (site capital + site validation) + site fixed operations;
`capacity_units_per_year` = `batches_per_year` x `uptime_fraction` x `batch_size_units` x `yield_fraction`. One S10
host (`shared_suite_1`, a 0.20 tenancy) has capital 8,000,000, validation 4,000,000 and fixed operations 600,000, so
2,552,945 USD/yr against 220,320 u/yr (norepinephrine) or 183,600 (bicarbonate); `central` has 10,473,595 USD/yr
against 1,156,680 and 963,900 u/yr.

| product | node | price [USD/unit] | where the price comes from | min contracted utilization |
|---|---|---|---|---|
| norepinephrine | `shared_suite_1` | 18.95 | network break-even, 4.1 | 0.6508 |
| norepinephrine | `shared_suite_1` | 12.74 | the price at which this node needs exactly 100 percent | 1.0000 |
| norepinephrine | `shared_suite_1` | 4.52 | FSS non-Big4 vial price proxy in the product config header | 3.4384 |
| norepinephrine | `central` | 18.95 / 4.52 | as above | 0.5086 / 2.6869 |
| sodium bicarbonate | `shared_suite_1` | 16.20 / 15.10 | network break-even / the price needing exactly 100 percent | 0.9271 / 1.0000 |

The same call on the norepinephrine run ledger reproduces the network row: fixed and resilience cost 15,179,667 USD/yr
(sum of `ledger_capital_annualized`, `ledger_fixed_site_operations`, `ledger_product_site_launch`,
`ledger_resilience_contracts`, `ledger_os_integration`) against 940,504 u/yr gives 0.9065 at break-even, 1.4876 at
12.00 and 4.7893 at 4.52 USD per unit. Above 1.0 means no committed volume covers the fixed cost, because the network
cannot make enough units. Which price is plausible? The only price evidence in the package for either presentation is
the norepinephrine 4 mL vial FSS proxy of 1.47 USD (Big4) and 4.52 USD, in the header of
`config/products/norepinephrine_1mgml_4ml.yaml` from `research/beachhead-verification.md`; it is a price proxy, not a
cost and not a willingness to pay, and sodium bicarbonate has no equivalent. At 4.52 USD a 0.20 tenancy would have to
sell 3.44 times its attributed capacity to cover its own fixed cost. The landscape agrees from the other side: HHS
attributes the problem to "prices for generic drugs that are driven to levels so low that they create insufficient
incentives for redundancy or resilience-oriented manufacturing" (F6-S18) and FDA's root-cause report states that "Most
generic manufacturers cannot afford to support redundant capacity" (F7-S16). On this evidence the break-even prices of
18.95 and 16.20 USD per unit are not plausible at today's prices for these presentations, a statement about this model
plus one price proxy and not about the market.

### 4.3 The contract questions, answered and unanswered

S10's `contracting_requirement` profile field names the instrument, two tolling agreements plus one offtake, and
answers six of the nine terms: payer Telo for manufacture, purchaser the GPO or health system, beneficiary hospitals,
activation condition none because both hosts run continuously, allocation rights none needed, and default risk each
host's compliance state independently. **That last field overstates what the configuration declares.** The model puts
`cc_vial_1`, `cc_stopper_1` and `cc_quality` across both hosts and `central` (section 1), so the two hosts are not
independent in this engine, and section 3.5 shows the consequence: the binding conditions for S10 are the
common-cause rate and the per-supplier disruption rate, the latter the tightest supplier condition in the whole grid.
Whether two unaffiliated hosts default independently in the world is a separate question that no run here answers;
falsification register data row 7 is its untested test. `ContractTerms.missing()` returns `term_years`, `committed_units_per_year` and
`price_required_usd_per_unit`; until a purchaser answers those three the design is not contractable and the model's
break-even price is not a price. Take-or-pay does not apply, since S10 has no reserved capacity and appears in 0 of
the 50 rows of `ds_post_R008/contract_scenarios.csv`.

## 5. Prior art and landscape position

Multi-product sterile plants sharing quality staff, equipment and utilities are the industry default and are
already_implemented two to three orders of magnitude above a Telo tenancy: Fresenius Kabi Melrose Park at 250 products
and over 160 million vials a year across six aseptic lines plus a five-line expansion (F6-S26); Hikma at over 180
injectable products (F6-S27); Gland at 28 lines (F6-S28, F6-S29); Pfizer Rocky Mount at nearly 50 medicines (F6-S25).
No company publishes products per line. The family 6 dossier's own [inference] from the Fresenius disclosure is 23 to
40 products per line-year, so 2.5 to 4.3 percent of a line per product on average, which makes a 20 percent tenancy a
large one by that benchmark and cuts against assuming a host would sell it. The constraints the model omits are
settled law and guidance: 21 CFR 211.42(c) and (d) on defined areas and separate facilities for penicillin and 21 CFR
211.67(a) to (c) on cleaning shared equipment (F6-S01, F6-S02); FDA's 2013 beta-lactam guidance, which says
manufacturers "generally should utilize separate facilities" for non-penicillin beta-lactams (F6-S10); 21 CFR
211.113(b) with FDA's 2004 aseptic guidance section IX on media fills (F6-S11); EU GMP Annex 15 chapter 10 sections
10.1, 10.2, 10.6, 10.8, 10.9, 10.10, 10.13 and 10.14 (F6-S04); EU GMP Chapter 3 section 3.6 and Chapter 5 sections
5.17 to 5.22 (F6-S05, F6-S06); the EMA HBEL guideline and its 2018 Q&A (F6-S07, F6-S08). Two readings stay UNCERTAIN:
no source shows FDA accepting HBEL-based carryover limits in place of the historical criteria (F6 section 9), and the
reporting category for adding a sterile fill-finish site to an approved application is gate G07 (F6-R02, F3-S44,
F3-S45).

The failure record is what makes the missing correlation material. Akorn's trustee recalled all within-expiry product
because the quality programme had ceased (F6-S24); Intas Sanand's data-integrity findings and Import Alert 66-40
removed an oncology portfolio (F6-S22); PharMEDium's four-site network under one quality organization was cut to two
sites by consent decree (F6-S34, F6-S44); Pfizer Rocky Mount put roughly 50 medicines on allocation after a warehouse
loss (F6-S25); GAO found four of six facility-shutdown shortages came from one manufacturer's single facility
(F6-S14); Teligent's small injectable line never launched because a site warning letter blocked its pre-approval
inspection (F6-S35). On position, `novel_architectures.md` classifies S10 as novel_combination, withdrawn if a
generic sterile injectable is found that deliberately maintains matched tenancies at two unaffiliated multi-product
hosts for resilience rather than capacity. The base rate is against it: of about 900 sterile-injectable ANDAs approved 2000 to
2011, Woodcock and Wosinska found only 11, just over 1 percent, referencing more than one finished-dose facility
(F6-S37). Shortage-risk-weighted portfolio selection for a small multi-product node is the one sub-idea family 6
records as uncertain, possibly novel_combination, with no company or paper doing it (F6-S30, F6-S20, F6-S39). Two
candidates resting entirely on portfolio pooling, `anchor_tenancy_divertible_slots` and `PS_A_portfolio_family`, were
rejected at configuration for the reason measured here, that the cost claim is unmeasurable in this engine.

## 6. What is weak, and what evidence would change the answer

| # | Weakness | Why it matters | Evidence that would change the answer | Human action |
|---|---|---|---|---|
| 1 | One product per network (MD-15). The cost advantage in 3.2 is an attribution, not a measurement. | The largest unquantified distortion in the cost comparison, and it flatters S10 in both cost and tail risk. | The model extension in 6.1, then a re-run. | none (in-model); HA-21, HA-22 for its parameters |
| 2 | No changeover, cleaning-validation, media-fill or campaign-size cost against the shared line. | These are the real costs of being multi-product and all are zero here. | Commercial changeover distributions, dirty and clean hold times, a cleaning-validation calendar for a generic sterile line. None public; only vendor claims exist (F6-S41, F6-S42). | HA-21, HA-22 |
| 3 | No cross-product correlation: a plant event removes one product, not a portfolio. | It removes the risk the architecture creates, so the tail is optimistic by an unknown amount. | An engine gap first, then a site-level quality-event rate conditioned on quality state, which FDA's own analysis argues for (F6-S13). | none (in-model); HA-22 |
| 4 | No purchaser and no price. The break-even prices of 18.95 and 16.20 USD per unit have nothing behind them. | Section 4 shows the whole commercial case turns on this. A technically feasible node without contractable demand is not feasible. | A GPO or health-system answer on term, committed volume and price for a resilience-differentiated generic. | HA-11, HA-24, HA-20 |
| 5 | No host will necessarily sell a 20 percent tenancy. | Without a counterparty the design has no commercial existence at any modelled cost. | Tenancy quotes from two candidate US sterile fill-finish hosts; no US rate card is public. | HA-13, HA-21 |
| 6 | Gate G07 and every other applicable gate are UNCERTAIN. | Two site additions means two change-control packages under 21 CFR 314.70 and two facility evaluations. If each is a prior-approval supplement with a pre-approval inspection, the lead time and the cost are both wrong. | A regulatory professional assigning the category, plus whether any approved ANDA lists two US sterile fill sites for one presentation. | HA-23, HA-31 |
| 7 | `central`'s full capital, fixed operations and validation are charged to this ledger (MD-14 residual). | S10's absolute cost is not a Telo-only cost, so rankings against designs with other ownership shapes are not clean. | A labelled companion design with `capital_multiplier`, `fixed_cost_multiplier` and `validation_multiplier` 0.0 on `central`, or a per-site ownership flag. | none (in-model) |
| 8 | The S10 falsification tests are unfinished. Rows are cited by **data-row index**, the row's position among the 33 claim rows with the header counted as no row, which is the convention `feasibility_regions.md` section 7 uses. Data row 6 is provisional on an n = 25 pre-R008 run with no manifest; data rows 7 and 8 are untested. | The design exists to price independence and that price has not been measured at full n inside the battery. | Re-run the internal single-host control (one host at shares 0.4, `validation_multiplier` 2.5) at n >= 100 with a manifest, then the api_1 ablation. | none (in-model); HA-13, HA-21 for data row 8 |

### 6.1 The exact model extension a real portfolio analysis needs

1. **Multi-product runs.** `run_paired` takes a list of products sharing one site roster, with a demand process,
   inventory policy and release queue per product and shared site runtimes.
2. **A line time budget.** Replace per-site `batches_per_year` with an allocation of line days across products plus a
   sequence-dependent `changeover_hours_product`, distinct from the per-batch `changeover_days`, covering
   decontamination, line clearance and cleaning verification.
3. **Campaign constraints and per-product-per-line qualification.** `campaign_max_batches` from cleaning validation
   (Annex 15 10.9, F6-S04) and `campaign_min_batches` from media-fill economics (F6-S11); then
   `product_qualification_days` and `validation_cost_per_product_line` replacing the flat `validation_factor`,
   conditioned on site quality state (F6-S35).
4. **A shared QC laboratory queue** so `qa_review_days` and `assay_days` contend across products (F6-S12), and
   **cross-product demand correlation**.
5. **A product-family compatibility matrix** forbidding co-location of penicillins and beta-lactams and gating
   cytotoxics, hormones and high-potency compounds behind dedicated-line cost (F6-S01, F6-S10, F6-S07, F6-S26).
6. **A plant-level common-cause group** over every product at that node, capacity impact near 1.0 for the documented
   event classes, event rate conditioned on site quality state rather than facility count (F6-S13, F6-S14, F6-S22,
   F6-S24, F6-S25).

Rough build cost, an engineering estimate and not evidence. Items 1, 2 and 6 change the simulation loop, the capacity
model and the disruption model at once and invalidate the frozen S0 to S7 digests, so they need a protocol revision, a
re-capture of `tests/regression/frozen_digests_s0_s7.json` and a re-run of the whole battery. Estimate 6 to 10
person-weeks for items 1, 2, 3, 5 and 6, 2 to 3 more for item 4, and 25 to 40 new unit and integration tests. Compute is not the constraint but is not free: the design-space run alone took 6,573.9 s wall
(`ds_post_R008/summary.json`, `meta.wall_time_s`) at one product per network, and a P-product engine scales roughly
linearly in P. The larger cost is not code. Items 2, 3 and 6 need numbers no public source provides: commercial
changeover and cleaning-validation timelines, minimum economic campaign size, per-product-line validation cost, and a
site-level quality-event rate. Building it without them would replace one unquantified distortion with tier-5
parameters that look like a portfolio model. The honest sequence is HA-21 and HA-22 first, then the engine.
