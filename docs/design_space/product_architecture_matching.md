# Product-architecture matching results (deliverable 13)

## 1. Question and banner

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every strategy result below is model behavior under tier-5
illustrative inputs, not a statement about sterile-injectable manufacturing in the world, a recommendation, or a
product selection. Regulatory gates stay UNCERTAIN; UNCERTAIN is never PASS. No interview, partner, customer,
purchaser or reviewer exists; every organisation named is a published third party cited by source id. Runs made
before 2026-09-03 are superseded for quantitative use and are labelled where quoted.
The assignment (Phase B family 12, Phase D, Phase E) asks for algorithmic product-architecture matching: given a
candidate presentation's features, which architecture families are in play and which are ruled out. Three questions
are kept separate here: which features exist today per presentation; what the post-R008 engine says about the two
presentations that have configurations; and what matching rules would apply once the missing features exist.
**This document does not select a product.** Selection is reserved to the founder under HA-03 and
definition-of-finished test DF03. The architecture taxonomy already records this family's status:
"The matching model is not built" (`architecture_taxonomy.md` section 1, family 12).

## 2. What the model can and cannot represent for this family

- **Two presentations out of six carry a configuration, and they are near-clones.** `config/products/` holds only
  `sodium_bicarbonate_8_4_50ml` and `norepinephrine_1mgml_4ml`; the other four have a dossier from frozen snapshots
  and nothing else, so no simulation, optimization or threshold here speaks about them. Audit item WB-26 records
  `07_Product_B` as a near-clone of `06_Product_A`: they differ in `annual_demand_units` (900,000 against 1,200,000)
  and `units_per_batch` (30,000 against 25,000) and agree on shelf life and material lead time. Most apparent product
  discrimination in this package is that one demand-to-capacity ratio, itself a tier-5 number.
- **The engine has no sterilization-route attribute at all.** `ReleaseScenario` R0-R3 acts on a release-component
  vector; there is no product field for terminal versus aseptic, no parametric-release scenario distinct from R3, no
  per-site parametric validity, no reformulation lead time (`architecture_taxonomy.md` family 11). The design-space
  `release_time` axis in `ds_post_R008/thresholds.csv` runs low 14.0, base 14.0, high 18.0, so it can only measure
  release getting slower. Every release-time threshold below is an upper bound on tolerable delay, not a valuation
  of route conversion. Separately, defect MD-15 blocks the multi-product and postponement families from being
  modelled as portfolios, so S10 and S11 run with one presentation carrying the whole line; their cost is an upper
  bound and their matching claims are weaker than their strategy profiles suggest.

## 3. Results

### 3.1 Feature table

Built by `telo_feasibility.product_architecture.load_product_features` and `write_features_csv`, written to
`results/design_space/product_features.csv` (28 columns, with the per-field evidence map). Evidence ids are
frozen snapshots: S01 FDA shortage export `2ea0ff3bb44c`, S14 503B bulks list `7f00a4d2672a`, S16 Drugs@FDA
`52e1277513bc`, S17 Orange Book `caaa826d4ba7`, S18 DailyMed (per candidate), S19 CMS Part B `986deefa094d`; flags
come from `config/longlist.yaml`, gates from the dossiers. All six are non-controlled small molecules in a standard
vial, none cold-chain intensive, cytotoxic, a biologic, a suspension or a drug-device combination. The S19 Part B row
count is 0 or 1 for every candidate and carries no discrimination, so no rule below uses it. Data-partial screen
scores (`dossier.json`, weight covered 0.45 for all six): sterile water 2.25, sodium bicarbonate and furosemide 1.65,
acyclovir and acetazolamide 0.75, norepinephrine 0.65.

| candidate | role | shortage now | rows cur/total | yrs since first | apps (ANDA/NDA) | OB applicants | 503B bulks | DailyMed inj. | aq / lyo | PG1 / PG2 | hard gate | demand [u/yr] | shelf [mo] | u/batch | lead [d] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sodium_bicarbonate_8_4_50ml | current/recurrent candidate | yes | 15 / 19 | 9.51 | 19 (16/3) | 12 | not_included | 24 | yes / no | PASS / PASS | UNCERTAIN | 1,200,000 | 24 | 25,000 | 90 |
| norepinephrine_1mgml_4ml | resolved comparator | no | 0 / 0 | none | 26 (22/4) | 23 | absent | 31 | yes / no | PASS / PASS | UNCERTAIN | 900,000 | 24 | 30,000 | 90 |
| furosemide_10mgml_vial | reserve (repo scorecard pick) | yes | 30 / 33 | 6.40 | 37 (27/10) | 28 | absent | 31 | yes / no | UNCERTAIN / PASS | UNCERTAIN | absent | absent | absent | absent |
| sterile_water_for_injection_vial | include only if scale works | yes | 21 / 21 | 4.77 | 1 (1/-) | 0 | absent | 38 | yes / no | UNCERTAIN / PASS | UNCERTAIN | absent | absent | absent | absent |
| acyclovir_sodium_50mgml_vial | reserve | no | 0 / 0 | none | 22 (21/1) | 14 | absent | 1 | yes / no | UNCERTAIN / PASS | UNCERTAIN | absent | absent | absent | absent |
| acetazolamide_500mg_vial | out-of-archetype comparator | no | 0 / 0 | none | 10 (9/1) | 9 | absent | 8 | no / yes | PASS / **FAIL** | FAIL (PG2) | absent | absent | absent | absent |

### 3.2 What each presentation's features support and rule out

Support and exclusion mean consistent, or not, with the architecture's declared `product_archetype` in `config/strategies/design_space.yaml`. They are not performance claims.

| candidate | families its features support | families its features rule out | why |
|---|---|---|---|
| sodium_bicarbonate_8_4_50ml | S8 telo_architectures, S9/S19 upstream_first, S10 multi_product, S11 postponement, S12/S13 virtual_network, S14 public_private, S16 inventory_capacity_hybrids, S17 warm_standby, S18 contracts_procurement | S15 product_selection. S7 conditional, not ruled out | On the FDA list now with 15 current rows over 9.51 years, so it meets every "in shortage or recurrent" archetype. Its bulks status is `not_included` (88 FR 20531), so G09 rests on the shortage predicate alone and S7 is eligible only while the presentation stays listed: the run gives `p503b_eligible_days` 1,222.6 of 1,826, against 405.7 for norepinephrine. S15 requires a presentation NOT currently in shortage, since the CMS buffer payment will not fund a newly established buffer of a medicine in shortage (LSD-S3, F12-S08) |
| norepinephrine_1mgml_4ml | S9, S10, S11, S12, S13, S16, S17, S18, S19, and S15 conditionally (CMS 86-list membership is not held) | S8 and S14, on their own archetype text; S7 has no eligibility basis at t0 | Not on the list (0 rows in S01, 0 in S01B) and bulks `absent`, so S7 turns on only if the presentation is listed later. S8's archetype says demand at or above installed capacity and states plainly that norepinephrine does not fit; S14 requires "in shortage or with recurrent shortage history". 23 Orange Book applicants is the least concentrated supplier structure among the configured presentations, and furosemide is less concentrated still at 28 applicants over 37 applications; either way this weakens every second-source argument |
| furosemide_10mgml_vial | the same set as sodium bicarbonate, with S7 conditional on staying listed | S15, in shortage now | The most shortage-persistent candidate in the set: 30 current and 33 total rows, 6.40 years, and the only one whose S01 reason list includes a GMP-compliance reason and an inactive-ingredient shortage. Also the most crowded: 37 applications and 28 Orange Book applicants. PG1 is UNCERTAIN because the fill volume is not fixed, so no batch size, no capacity and no architecture can be sized. Its inclusion is HA-03, unresolved |
| sterile_water_for_injection_vial | S11 postponement and S10 multi_product in principle (one undifferentiated bulk in a common container is exactly the postponement case) | every owned-plant family at the modelled node scale; S15 | 1 application and 0 Orange Book applicants is the most concentrated structure in the set and the strongest supplier-concentration case, but PG8 is UNCERTAIN with the note that diluent volumes are very large relative to a micro node. The workbook flagged the scale mismatch and the longlist admits it only "if scale can be represented meaningfully" |
| acyclovir_sodium_50mgml_vial | S9, S10, S11, S12, S13, S16, S17, S18, S19, S15 conditionally | S8, S14 (not in shortage); S7 (no eligibility basis at t0) | 0 shortage rows and 14 applicants. Its 1 DailyMed injectable title against 22 applications is a data inconsistency in the snapshot join, not a market fact, and it should be resolved before the presentation is scored |
| acetazolamide_500mg_vial | none as configured | every family in this package | PG2 FAIL: lyophilized, so it violates the first archetype (aqueous small-molecule solution in a standard vial) that every one of the twelve design-space strategies declares. It is in the longlist as an out-of-archetype control and behaves as one |

### 3.3 Model results for the two configured presentations

Fill and cost come from `results/simulation/sim_post_R008/summary.json` `by_strategy["<product>|<strategy>"]` at
n = 100; `p_meet` is `meets_fill_rate.mean`, whose binomial standard error near q = 0.90 is about 0.030. The sharpest
product-architecture interaction is the ablation, as leave-one-out mean fill deltas over all 20 strategies:

| factor | norepinephrine (capacity-adequate) | sodium bicarbonate (capacity-short) | ratio |
|---|---|---|---|
| capacity_shortfall | +0.00039 | +0.05138 | 132x |
| commissioning_delay | +0.00269 | +0.01741 | 6.5x |
| inventory_timing | +0.00535 | +0.00997 | 1.9x |
| common_cause | +0.00264 | +0.00868 | 3.3x |
| sterility_delay / release_queue | +0.00248 / +0.00074 | +0.00136 / +0.00033 | 0.5x / 0.4x |
| supplier_concentration | +0.00416 | +0.00271 | 0.7x |

Source: `results/ablation/abl_post_R008/attribution.csv`, `loo_delta_fill_rate`, averaged per product over the 20
strategy rows. Which mechanism binds is a property of the product, not of the architecture: on a capacity-short
presentation capacity dominates by two orders of magnitude, while on a capacity-adequate one inventory timing and
supplier concentration are the largest terms and capacity is the smallest. The interaction study makes the same point
as a gate rather than a gradient (`results/ablation/abl_post_R008_pairs/summary.json`, `fill_rate.mean` at n = 60):

| cell | base | inventory + commissioning off | capacity + inventory off |
|---|---|---|---|
| sodium bicarbonate S0 | 0.7204 | 0.7198 | 0.9774 |
| sodium bicarbonate S15 | 0.9398 | 0.9398 | 1.0000 |
| norepinephrine S0 | 0.9814 | 0.9933 | 0.9936 |
| norepinephrine S15 | 0.9886 | 0.9999 | 0.9999 |

On the capacity-short presentation, switching off inventory timing and commissioning together moves fill by -0.0006
and -0.0000: inventory cannot repair a mass-balance deficit. On the capacity-adequate presentation the same pair is
worth +0.0119 and +0.0113. This is the matching rule the model actually supports today, and it is why the same
architecture lands in different places on the two presentations (`sim_post_R008/summary.json`, as configured):

| strategy | family | norepinephrine fill / p_meet | sodium bicarbonate fill / p_meet | commissioning fraction lost |
|---|---|---|---|---|
| S0 status quo | comparator | 0.9442 / 0.13 | 0.7157 / 0.00 | 0.0000 |
| S15 inventory-first, no plant | product_selection | 0.9928 / 0.87 | 0.7593 / 0.00 | 0.0000 |
| S11 bright-stock postponement | postponement | 0.9993 / 0.99 | 0.9599 / 0.18 | 0.0000 |
| S17 rotating campaign network | warm_standby | 1.0000 / 1.00 | 0.9967 / 0.91 | 0.0000 |
| S13 base plus surge plus reserve | virtual_network | 1.0000 / 1.00 | 0.9924 / 0.75 | 0.0444 |
| S5 distributed microplants | comparator | 0.9784 / 0.51 | 0.8624 / 0.00 | 0.2872 |

S15 is the clearest case: a no-plant, inventory-only architecture reaches 0.9928 mean fill on the capacity-adequate
presentation and 0.7593 on the capacity-short one, at almost identical cost per delivered unit (13.71 against 13.68
USD, `contract_conditions_sim_post_R008.csv`). Every distributed-plant design pays a commissioning fraction: S5 and
S6 lose 28.72 percent of the measured window, S4 19.99, S18 14.56, S13 4.44, while S11, S15, S16, S17 and S19 lose
nothing because they buy or contract capacity that already exists. At the frozen target the optimizer reaches
`optimal` on 6 of 20 strategies for norepinephrine (S9, S11, S12, S13, S16, S17) and 7 of 20 for sodium bicarbonate
(S9, S10, S11, S12, S13, S16, S18) (`opt_20260903T220534Z/summary.json`), which is what the `feasible` column of
`ds_post_R008/dominance.csv` gives independently and what `feasibility_regions.md` section 4 reports; at tau = 0.98
the counts are 7 and 7 (`opt_20260903T231408Z_tau0.98/summary.json`), the norepinephrine addition being the frozen
reserved-capacity comparator S3, which is the decision-relevant part, and the sodium bicarbonate change being S17 in
and S11 out. It never reaches feasible on S0, S1, S4, S5, S6 or S7 for either.
Figures: `../../results/figures/design_space_ds_post_R008_<product>_feasibility.png` and the matching
`_dominance.png`, for both product ids.

### 3.4 Demand thresholds, the one matching rule the model can already state

`ds_post_R008/thresholds.csv` bisects `capacity_utilization` (parameter `product.annual_demand_units`) to the demand
at which each strategy stops meeting the frozen target. Every row is `feasible_below`, so the number is a demand
ceiling. The search runs at n = 20, so the binomial standard error on `p_meet` is about 0.067 and any ceiling within
roughly 5 percent of the base is inside noise.

| strategy | norepinephrine ceiling (base 900,000) | sodium bicarbonate ceiling (base 1,200,000) |
|---|---|---|
| S0, S1, S2, S4, S5, S6, S7 | none, infeasible at every value | none, infeasible at every value |
| S3, S8 / S10 / S14 | 642,188 (0.71x) / 601,563 (0.67x) / none | 1,190,625 (0.99x) for all four |
| S9 / S11 | 1,089,063 (1.21x) both | 1,359,375 (1.13x) / 1,190,625 (0.99x) |
| S12, S16 / S13 | 926,563 (1.03x) / 885,938 (0.98x) | 1,246,875 (1.04x) both |
| S15 | 682,813 (0.76x) | 1,078,125 (0.90x) |
| S17 / S18 / S19 | 967,188 (1.07x) / 967,188 (1.07x) / 885,938 (0.98x) | 1,021,875 (0.85x) / 1,190,625 (0.99x) / 1,021,875 (0.85x) |

No architecture survives a doubling of demand: in `ds_post_R008/reversal.json`, which runs at 10 paired runs per cell
because the driver takes `runs // 4`, at 1,800,000 units/yr for norepinephrine and 2,400,000 for sodium bicarbonate
`preferred` is null and `feasible` is empty in all nine cells. An empty feasible set at n = 10 is the one reading in
that map the low run count does not weaken, since every one of the twenty strategies fails in every one of the
eighteen cells; the preference statements that follow are resolved to no better than one run each (SE 0.095).
The preferred architecture moves with demand (sodium bicarbonate: S15 at 600,000, S11 at 1,200,000; norepinephrine:
S11 or S15 at 500,000, S1 or S15 at 900,000, S3 once common-cause dependence reaches 0.30), while
`fixed_qa_labor_per_node` never changes it at any of its three levels in any of the 18 cells: fixed QA cost is a cost
lever with no feasibility content.

### 3.5 The features that are absent, and why no rule can use them yet

Three of the features the assignment names are columns of `product_features.csv` and are empty in all six rows
(`sterilization_route`, `substitution_difficulty`, `contractability`); a fourth, regional demand heterogeneity, has
no column at all, because the engine splits national demand across four regions by a fixed rule. Three more that
family 12 names are neither used as a rule nor listed below in earlier drafts and are added here. None is derivable
from a frozen snapshot in this package. **No rule in this document uses any of them; none can be written until a
person supplies them.**

| absent feature | why it is absent | what it would gate |
|---|---|---|
| sterilization route (terminal vs aseptic) | approved US and EU labelling does not disclose it. Family 11 tried the HPRA public assessment report, three UK SmPCs, two Canadian monographs and two DailyMed labels for furosemide alone and found no statement; the Hospira sodium bicarbonate 8.4% label does not state it either. Telo's own `regulatory/approved_generic_cmo_map.md` records the route for sodium bicarbonate 8.4% as unresolved (F11-S44) | whether family 11 route conversion plus parametric release is available at all, and therefore whether the 14-day sterility pole is a fixed constraint or a design variable |
| substitution difficulty | PG6 is UNCERTAIN for all six: "presentation-specific substitution behavior must be described by clinicians or pharmacists", and no public dataset carries it | how much a service failure costs, and whether a shortage of this presentation is a clinical event or an inconvenience. Nothing in the objective currently separates the two |
| contractability | zero of the 42 Phase B candidates is contractable today; `ContractTerms.missing()` returns five to nine unanswered fields for the modal candidate and six for S8. No US hospital system, GPO or state has been found paying a standing readiness fee for sterile generic capacity (F3-S28) | whether any architecture with a committed-volume or availability revenue mechanism is a business rather than a simulation |
| regional demand heterogeneity (no column in the CSV) | the engine splits national demand across four regions by a fixed rule; PG5 is UNCERTAIN for all six candidates and CMS Part B is an outpatient proxy that misses inpatient essential injectables | whether a distributed or hub-and-spoke topology has any advantage over a single site plus logistics |
| demand volatility (no column in the CSV) | the engine carries a demand process, but the feature table holds one `annual_demand_units` scalar per configured presentation and no per-presentation volatility, and no public source gives one at presentation level | whether a stock-led family (S15, S16, S11) or a capacity-led family applies, since the value of a buffer is set by variability rather than by the mean. **HA-11** |
| equipment fit (no column in the CSV) | no fill-volume, line-format or batch-size feature exists for four of the six candidates; furosemide's PG1 is UNCERTAIN precisely because the fill volume is not fixed | whether a presentation can fill a registered line at all, and therefore whether S10 multi-product tenancy is required rather than optional. **HA-13**, **HA-21** |
| common component compatibility (no column in the CSV) | `standard_vial` in `config/longlist.yaml` is a longlist flag, not a qualified container-closure commonality claim; prior art records the criterion as `uncertain` with no public dataset (F12-S10, F12-S13) | whether one qualified vial and stopper system can serve several presentations, which is the whole premise of the postponement and standardized-container families |

One more belongs here though the assignment does not name it: membership of the CMS FY2025 IPPS 86-medicine
essential-medicines list, which S15's archetype makes gate two of three. The package holds no snapshot of it.
**Sterilization route is the highest-value unresolved input in the whole sweep**, for a specific reason: of the
interventions collected across the fourteen families, process-route conversion is the only one that acts on the
release constraint itself rather than on components that are not binding (`prior_art_review.md` section 6.1; family
11 section 9). The mechanism is neither novel nor in dispute. FDA has accepted parametric release for moist-heat
terminally sterilized drug products since 1985 (F11-S02, F11-S03), USP `<1222>` covers it, and EU Annex 17 section
4.3 extends it to radiation (F11-S05). What does not exist is the data: no source asks route as a design variable,
and the route is not published per marketed presentation in any US or EU label reviewed, so there is no dataset to
screen a longlist against (F11 section 9, F12-S13 area).

**What it would take to obtain it.** Three routes work: the sterility-assurance section of a US ANDA or NDA chemistry
review for the exact presentation; an FDA establishment inspection report naming the autoclave cycle at the site; or
a qualified reviewer's direct knowledge. Label scraping is ruled out, tried at scale for furosemide and returning
nothing, because approved labelling for this class does not carry the route. Two indirect furosemide signals are
insufficient: a DailyMed establishment listing naming "sterilize" as a business operation, which separates nothing,
and a pending Chinese application (CN103371967A) describing a 121 C terminal cycle, which is not a US approval. The
chemistry prior points terminal for a simple alkaline aqueous solution in glass at pH 8.0 to 9.3 (F11-S48) and FDA,
EMA and Annex 1 all make terminal sterilization the default where the product tolerates it (F11-S01, F11-S04,
F11-S06, F11-S15), but a prior is not a source. Filed below as **HA-34**.

### 3.6 The matching rule set to apply once the features exist

Proposed, not applied. Thresholds from a run artifact are model-internal and inherit tier-5 inputs; those marked
"to be set" cannot be derived from anything this package holds.

| feature | threshold | architecture implication | evidence needed |
|---|---|---|---|
| status-quo utilization (national demand / installed registered saleable capacity) | at or above 1.0, versus below about 0.9 | at or above 1.0: capacity-first families only (S8, S9, S12, S13, S14, S18), and inventory-only designs are excluded, since the pair study moves sodium bicarbonate S15 by -0.0000 when inventory timing and commissioning are both removed. Below 0.9: inventory-first families in play (S15, S16, S11), and S15 reaches 0.9928 fill with no plant | installed saleable capacity per presentation, which no public source carries. HA-11 (utilization) plus HA-13 (line capacity) |
| annual demand against the architecture's own ceiling | the `capacity_utilization` ceilings in section 3.4; no architecture survives 2x base demand | rules out every architecture in the battery above the ceiling, including all twelve design-space designs | a demand denominator that is not tier 5. HA-11 |
| annual demand against minimum committed volume | 0.56M to 2.25M units/yr at an illustrative 20 USD/unit (section 4) | rules out any multi-site architecture whose minimum committed volume exceeds what the presentation can sell. 9 of 20 architectures fail this on norepinephrine and 3 of 20 on sodium bicarbonate | a price a purchaser will pay, which is HA-11 or HA-24. Price is not reimbursement and is not inferred from ASP |
| sterilization route | terminally sterilizable | family 11 route conversion available; the 14-day sterility pole becomes a design variable rather than a constant, and parametric release under CPG 490.200 becomes reachable. Aseptic-only rules the family out entirely | **HA-34**. ANDA chemistry review, inspection report naming the cycle, or a qualified reviewer |
| sterilization route portability | a parametric release programme extends to a second site or autoclave | if it does not, parametric release is a per-node asset whose cost scales with node count like replicated process validation, which reverses the economics of every multi-site design (F11-S46) | HA-31 plus the reporting-category question in `prior_art_review.md` section 7 item 1 |
| shortage status now, recurrence and duration | on the FDA list now; recurrent or long single episodes | on the list satisfies the S14 and S8 archetypes and excludes S15, because CMS will not fund a newly established buffer of a medicine in shortage (LSD-S3). Recurrence supports every second-source and reserve family; the defensible framing is duration and response cost, not incidence, since FDA reports 55 new shortages in CY2023, 15 in CY2024 and 4 in CY2025 (LSIM-S21) | S01 snapshot, already held, so the status half is evaluable today. Duration needs ASHP presentation-level bulletins, HA-10 |
| application-holder count and Orange Book applicants | fewer than about 5 applicants | supports upstream-first and supplier-concentration families (S9, S19). Above about 20, a second finished-dose source adds little independence and the design becomes hard to distinguish from the incumbent market | S16 and S17 snapshots, already held. The rule's own threshold is to be set: nothing in this package calibrates it |
| shelf life | at or above the strategy's own floor: 12.3 (S11) to 22.4 (S15) months for norepinephrine, 12.4 (S10) to 23.6 (S8) for sodium bicarbonate (`thresholds.csv`, `shelf_life`, `feasible_above`) | short-dated presentations rule out every deep-reserve design: at their optimized norepinephrine designs S11 and S17 hold 365 safety-stock days and S15 holds 344.1 (`abl_post_R008/summary.json` `meta.design_variables`). 365 is the upper `safety_stock_days` search bound in both blocks (S11 [15, 365], S17 [10, 365]), so that figure reports where the box ends and not what the design prefers; 111 of the 150 design variables in this run sit on a bound | labelled expiry per presentation, obtainable from DailyMed. Not yet extracted into the feature table |
| batch size and minimum campaign; material lead time | batch size to be set. Material lead crosses in seven of the forty cells. Two are `feasible_below`, 210.5 days on S18 and 158.0 on S19 for norepinephrine; the other five crossings come back `feasible_above` (S3 85.8, S10 59.5, S12 33.3 on norepinephrine; S8 230.2, S14 66.1 on sodium bicarbonate), which is the wrong sign for a lead-time constraint and should be read as MD-1 plus n = 20 noise, not as a rule. The remaining 33 cells are `feasible_everywhere` or `infeasible_everywhere` | batch size governs whether a presentation can fill a registered line at all, and so whether S10 multi-product tenancy is required rather than optional. Long-lead API rules out designs whose response depends on starting a campaign rather than shipping stock | HA-13 and HA-21 for batch size, with MD-15 closed before a portfolio can be modelled; supplier quotes, HA-12, for lead time. The threshold sweep also needs re-running at n = 100 before this row is used |
| substitution difficulty; regional demand heterogeneity | to be set | substitution governs the cost of a service miss and therefore the target itself, and nothing in the objective currently separates a critical from a substitutable presentation. Regional heterogeneity governs whether a distributed topology beats one site plus logistics; without it every regional result is an artifact of the fixed four-region split | HA-20 (clinicians, pharmacy); HA-11 and HA-24 (regional demand) |
| contractability | `ContractTerms.missing()` empty | a technically feasible architecture with unanswered contract fields is not feasible. Zero of 42 candidates passes today | HA-20, HA-24, HA-33 |

## 4. Commercial conditions

Computed through `src/telo_feasibility/contracting.py` from the package root. Inputs passed: `annual_cost_usd` and
`served_units` from `sim_post_R008/summary.json`; `fixed_and_resilience_cost_usd` as the sum of the
`ledger_capital_annualized`, `ledger_fixed_site_operations`, `ledger_product_site_launch`,
`ledger_resilience_contracts` and `ledger_os_integration` means; `variable_cost_usd_per_unit` as
`variable_materials_usd_per_unit + variable_conversion_usd_per_unit` from `config/products/` (1.15 and 1.20, tier 5);
`capacity_units_per_year` as delivered divided by mean fill; horizon 5 years. Price is not evidence, so three
illustrative prices were swept across the run's break-even range (13.17 to 49.11 USD/unit); the sweep is derived here
from the named artifacts and is not itself stored as a run artifact.
`minimum_contracted_utilization` at 20 USD/unit, the share of network capacity that must be sold under contract:

| architecture | norepinephrine (cap 940,184 units/yr) | sodium bicarbonate (cap 1,251,363 units/yr) |
|---|---|---|
| S0 status quo | 0.591 | 0.445 |
| S15 inventory-first | 0.591 | 0.446 |
| S11 postponement | 0.714 | 0.535 |
| S17 rotating campaign | 0.901 | 0.676 |
| S8 acquired second line | 1.123 | 0.844 |
| S5 distributed microplants | 2.260 | 1.698 |

**What this answers.** Minimum economic scale is a product feature crossed with an architecture, and it separates
the two presentations more sharply than service does. At 20 USD/unit, 9 of 20 architectures need more committed
volume than the norepinephrine network can produce (minimum utilization above 1.0) against 3 of 20 for sodium
bicarbonate, purely because the larger presentation spreads the same fixed cost over more units.
`contracting.maximum_fixed_cost_per_site` called with the **whole** of base demand committed, which is a 100 percent
take-or-pay assumption and the loosest possible one, carries 16,965,000 USD/yr (900,000 x 18.85) and 22,560,000
(1,200,000 x 18.80) of fixed and resilience cost at 20 USD/unit. Both are **network** ceilings despite the function's
name, because the function returns contribution margin times committed volume and the volume passed is network-wide.
Against S5's modelled network fixed and resilience cost of 40,066,431 USD/yr they are 2.4x and 1.8x short; S5's
per-site figure is 8,013,286 USD/yr across five site plans, which is less than either ceiling, so the comparison
only holds at the network level. At the 50 percent commitment `feasibility_regions.md` section 3 row 2 uses, the
ceilings halve.
**What this does not answer.** Price, and therefore all of them. Every figure above is a break-even derived from the
run or an illustrative sweep value. The landscape review found no published rate card, minimum order value,
reservation fee or per-unit price anywhere in 313 sources for US sterile fill-finish, 503B product, enterprise QMS,
MES, shortage-data platforms or modular hardware; the only two public prices in the evidence base are a QMS
subscription and an ASHP individual subscription (LQBR-S14, LSD-S7). Contract terms are private: committed-volume,
failure-to-supply and reservation terms are undisclosed in both Premier releases (LSIM-S18, LSIM-S19) and Vizient's
FAQ (LNPM-S19), and the per-batch price is redacted in the SEC exhibit of the largest US capacity reservation
(F7-S04). Payer, purchaser, beneficiary, term, activation condition, allocation rights and default risk are
unanswered for every architecture here.

## 5. Prior art and landscape position

Product-level shortage-risk scoring is occupied and patented (USP Medicine Supply Map and Vulnerable Medicines List,
Premier US12598146B2 and US12718960B2, Trulla/SpendMend US11983666B2: F12-S13, F12-S14, F12-S24, F12-S25, F12-S26),
as is government criticality listing that gates money (FDA EO 13944, ASPR/ARMI, the CMS 86-medicine buffer list, the
EU Union list: F12-S02, F12-S08, F12-S11, F12-S12) and committee-based selection by a nonprofit manufacturer (Civica:
F12-S27, F12-S28). Manufacturability screening by dosage form exists only as a 2016 WHO working draft scoring sterile
forms as unfavourable for start-up manufacture (F12-S32).

Two positions are recorded unoccupied, each with a withdrawal test. Release-time decomposition as a selection
criterion is **scientifically_novel**: no source ranks candidates by the decomposition of release time into
sterility, environmental monitoring, endotoxin, assay and QA components; withdrawn by a paper, patent or vendor
method that does (F12-S13, F12-S15, F12-S20, F12-S21). Algorithmic product-architecture matching, shortage risk
crossed with node economics, is **novel_combination**: the shortage-risk half is USP/Vizient/Premier/IQVIA and the
manufacturability half a WHO draft, and no source combines them with node cost and capacity; withdrawn by a published
or productised model doing both (F12-S24, F12-S25, F12-S32). Sterilization route, shelf life, batch size, fixed-cost
burden, minimum economic scale, regional heterogeneity and container-closure commonality as selection criteria are
**uncertain**, with no public dataset for any (F12-S10, F12-S13, F12-S15, F12-R04).
Landscape position. Supplier-risk intelligence is strong and federally funded (Exiger holds the top unrestricted
position on a 10-year, 919M USD GSA vehicle and has mapped the Essential Medicines list, LSD-S17, LSD-S18), but the
review's reading is that all of it answers "where is it made now" and none of it answers "who could make it by when"
(LSD section 5.1). That gap is where a matching model would sit. Against it: three GPOs cover over 90 percent of US
hospitals (LSIM-S20), Vizient serves more than 65 percent of US acute care providers on a 140B USD contract portfolio
(LSD-S11), and both large GPOs already run committed-volume and buffer-inventory programs.

## 6. What is weak, and what would change the answer

1. **The product discrimination in section 3.3 is one tier-5 ratio.** Both configured presentations come from the
   same workbook family (WB-26), and the capacity-short versus capacity-adequate split reduces to
   `annual_demand_units` 1,200,000 against 900,000 and `units_per_batch` 25,000 against 30,000, none of it evidence.
   If the real demand denominator moves either presentation across its ceiling in section 3.4, the ranking changes;
   **HA-11** is the single input that would settle it. The ceilings are themselves n = 20 estimates with a binomial
   standard error on `p_meet` near 0.067, so ceilings within 5 percent of the base are inside noise and must not be
   read as ordered. Applying that rule to every crossing rather than to a subset, the cells inside it are S12 and S16
   (926,563, +2.95%), S13 and S19 (885,938, -1.56%) on norepinephrine, and S3, S8, S10, S11, S14 and S18
   (1,190,625, -0.78%) together with S12, S13 and S16 (1,246,875, +3.91%) on sodium bicarbonate: thirteen of the
   twenty-five crossings in the column. Re-running at n = 100 needs no person.
2. **The model and the prior-art review disagree about release time, unresolved.** Phase A and the post-R008
   ablation say the sterility delay does not bind (leave-one-out mean fill delta +0.00248 and +0.00136); the
   prior-art review says route conversion is the only intervention acting on the binding release constraint. Both can
   be true, because the sweep's `release_time` axis has no value below 14 days, so the model has never been asked
   what removing the pole is worth, and cannot be until the engine carries a route attribute and a
   parametric-release scenario distinct from R3. A model gap, not a finding.
3. **Four of six presentations cannot be modelled at all.** Every statement about furosemide, acyclovir, sterile
   water or acetazolamide rests on snapshot counts and archetype flags. Furosemide is the most shortage-persistent
   candidate (30 current rows, 6.40 years) and has no configuration, no fixed fill volume and an unresolved longlist
   status. **HA-03** and **HA-18**.
4. **The value-of-information run is superseded.** `results/sensitivity/voi.json` covers S0 to S7 only, on designs
   from `opt_20260902T043854Z`, predating R004 to R008. Its ordering (capacity, material lead time and common-cause
   dependence carry the value; release time and shelf life effectively none) agrees with the post-R008 ablation, but
   its numbers must not be quoted and it must be repeated over S0 to S19. Re-running it is in-model and needs no
   person.
5. **No presentation can be scored on the four absent features**, so no rule in section 3.6 that depends on them is
   evaluable. Today the honest output of a matching model over this longlist is a partition into capacity-short and
   capacity-adequate, and nothing finer.

### Human actions

Proposed additions to `docs/audits/07_human_action_queue.md`, continuing from the existing HA-33. Selection itself
remains reserved under HA-03 and DF03: nothing in this document chooses a product.

| id | role | exact question | field it fills | acceptable evidence | model entry point | result it could reverse | fallback |
|---|---|---|---|---|---|---|---|
| HA-34 | generic-drug CMC or sterile-manufacturing regulatory professional (the HA-23 / HA-31 pool) | For each longlist presentation, is the marketed product terminally sterilized or aseptically processed, and for terminal products what is the cycle? | `ProductFeatures.sterilization_route` | the sterility-assurance section of a US ANDA or NDA chemistry review; an FDA establishment inspection report naming the autoclave cycle; or a named reviewer's direct knowledge with date and basis. Label text is not acceptable: it does not carry the route | a new product-level route attribute plus a parametric-release scenario in `ReleaseScenario`; then the section 3.6 route rules become evaluable | whether family 11 exists as an intervention at all, and whether the 14-day sterility pole is a constant or a design variable | carry route as an uncertain input with both branches run as a labelled structural sensitivity, and state that the family is untested |
| HA-35 | clinicians and hospital pharmacy leaders (the HA-20 pool) | For each presentation, how hard is substitution in practice, and what happens clinically when it is not available? | `ProductFeatures.substitution_difficulty`; PG6 | named clinicians describing presentation-specific substitution behaviour, with role and date | the objective function: nothing currently distinguishes a critical from a substitutable miss | the service target itself, and therefore every feasibility verdict in this package | keep PG6 UNCERTAIN and report every result at the frozen tau without a criticality weight, as now |
| HA-36 | GPO, wholesaler or IDN contracting lead (the HA-24 / HA-33 pool) | For a named presentation, would you sign a multi-year committed volume, at what volume, term and price, and what is the failure-to-supply remedy? | `ContractTerms` payer, purchaser, beneficiary, term, committed volume, activation condition, allocation rights, default risk, price | a signed term sheet, or a written statement of terms from a person with authority. Marketing material is not acceptable | `contracting.contract_requirement` price argument; the minimum-committed-volume rule in section 3.6 | every minimum-economic-scale exclusion in section 4, in either direction | continue to report break-even prices and an illustrative price sweep, and mark every architecture NOT CONTRACTABLE |
| HA-03 (existing) | founder | Does furosemide 10 mg/mL join the longlist, and at which exact fill volume? | PG1; a new `config/products/` entry | a decision recorded in DECISIONS.md | `config/longlist.yaml` and a product config, then the product screen | the whole longlist ordering, since furosemide is the most shortage-persistent candidate in the set | keep furosemide as a snapshot-only reserve candidate, as now |
