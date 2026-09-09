# Interview target matrix

Re-ranked 2026-09-05; statuses and two role rows corrected 2026-09-06. Status values: `not contacted`,
`contacted`, `contacted_no_reply`, `scheduled`, `complete` (with interview id), `declined`.
`contacted_no_reply` was added because a person emailed twice with no answer was previously recorded as
`not contacted`, which is indistinguishable from a person never written to and produces a third message against
the one-follow-up rule (`outreach_templates.md` section I).
**Every row is `not contacted`. No interview has been held, and none is in progress.** Zero against a 25 to 30 target
(DF18, `../design_space/definition_of_finished_status.md`).

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result quoted in this file is behaviour of the
engine under evidence tier 5 (illustrative) inputs: 87 of 91 parameters are illustrative and 0 are missing (DF09).
None of it is a statement about sterile-injectable manufacturing. All sixteen gates in `config/regulatory_gates.yaml`
are UNCERTAIN with no reviewer and no review date, and `eligibility` is NO_CONCLUSION for all twenty strategies, so no
architecture named below is presented as permitted. 503B is a time-varying legal state and never a durable pathway.
Nothing here records a partnership, customer, pilot, review or regulatory opinion, because none exists. Every
counterparty named anywhere in this package is a published third party cited by source id.

---

## 1. Why this file was re-ranked

The earlier version ordered roles by the protocol's own list, which was written when the study's open question was
whether distributed regional capacity can beat safety stock, dual sourcing, reserved contract capacity or added
central capacity. Under the inputs now in the model that question has an answer. Owned distributed nodes "meet the
target in no region of any recorded range on either product"
(`../design_space/feasibility_regions.md` section 6, family 1), and the fair-comparison correction does not rescue
them: "Under illustrative inputs, in this model, distributed manufacturing is not made feasible by giving it the
inventory freedom that makes the alternatives feasible" (same file, section 8). What the model prefers instead is a
shape rather than a strategy id: contract capacity that is already registered and inspected, position a deep
finished-goods tier, sell units.

Because every input behind that is illustrative, the value of a conversation now sits almost entirely in the numbers
and categories it produces. So roles are ranked here by the decision value of the human-action rows they can close,
taking the ranked queue in `../audits/07_human_action_queue.md` section 1 and the value-of-information reading in
`../design_space/strategic_synthesis.md` section 11 as the ordering. Queue ranks are given in brackets after each id.

How to read the ranking. It orders evidence, not people, and one good conversation in a low-ranked role can be worth
more than a weak one at the top. The queue's own ranks 1 to 4 are privacy and sign-off items that no interview can
close, so the highest interview-closable rank is 5. The decision values quoted below measure the model's sensitivity
to an input, which is not evidence that the input matters in the world.

---

## 2. Roles, ranked by decision value

| # | Role | Target | Human-action ids this role closes | The result it could reverse, quoted from the artifact | Status |
|---|---|---|---|---|---|
| 1 | Hospital pharmacy, IDN supply chain, and the demand-analytics owner who holds the utilization data | 8 | HA-11a [5] (the demand denominator only; see section 3a), HA-40 [6], HA-35 [20], HA-20 [21], HA-43 [22]; reviewer track HA-33 [24] | HA-11 carries "46 of 138 crossings in `../design_space/feasibility_regions.md` section 7 item 1, the only axis whose reversal map has a region where nothing qualifies" (queue HA-11). A denominator above the ceiling ends the shape outright: "HA-11 returning a demand denominator above the architecture's ceiling removes it outright" (`../design_space/strategic_synthesis.md` section 7), and the ceilings are 1.09M and 1.19M units per year for S11 and 0.93M and 1.25M for S16 (`../design_space/feasibility_regions.md` sections 2.1 and 2.2). At twice base demand "No strategy of the twenty meets the target in any of those 18 cells at any common-cause rate or QA cost" (same file, section 5). HA-40 carries the largest artifact in Phase A: "the hard-coded regional reorder rule decides **8 of 16 cells at +0.82% cost**", and the review rule alone moves P(fill >= 0.99) from **0.28 to 1.00 for both S0 and S1** on norepinephrine, and the comparators are feasible in 0 of 16 cells with the frozen rule against 11 of 16 with daily review (`results/ablation/abl_post_R008/summary.json`, configs `bounds:ss365` and `bounds:ss365+base_stock`, n = 60). The 0.56-to-0.90 and 0.65-to-0.94 figures quoted here until 2026-09-06 came from the superseded pre-R004 ablation run and must not be repeated; queue HA-40 and MD-3's register row still carry them | not contacted (0/8) |
| 2 | Sterile manufacturing and process engineering, with fill-finish engineering vendors and a CDMO commercial lead | 6 | HA-13 [7] commercial half, HA-21 [8], HA-41 [18]; HA-12 [23] and the vendor-estimate half of HA-13 as quotations, see section 7; reviewer track HA-30 [25] | HA-13 decides whether any cost figure in the package means anything: "fixed and resilience cost is **81.0% to 93.7% of annual cost** for all eight comparators ... Every absolute cost in this package is a statement about the scaffold until this lands" (queue HA-13). HA-21 decides service as well as cost: "`product.changeover_days` produces 20 crossings, and three of the five strategies feasible on both products lose the target inside 6.5 days of changeover, one at 3.39 days against a 3-day base" (queue HA-21), and the five designs that meet the target on both products need at or above **35.6 to 44.4** batches per site-year (`../../results/design_space/ds_post_R008/thresholds.csv`, `batches_per_site_year` rows: S9 35.6 and 40.6, S11 36.9 and 44.4, S12 44.4 and 44.4, S13 38.1 and 43.1, S16 43.1 and 43.1) | not contacted (0/6) |
| 3 | **Purchaser with budget and contracting authority**: IDN pharmacy or supply-chain executive, GPO contracting lead, or a state or federal programme officer (new role, see section 3) | 3 | HA-36 [9], HA-38 [15], and the price and take-or-pay half of HA-24 [10] | HA-36 decides whether any design is a business: every row of `../design_space/inventory_capacity_hybrids.md` section 4 reads "not contractable, stated" because "`ContractTerms.missing()` returns `price_required_usd_per_unit` for every design" (queue HA-36; the source line is at `../design_space/inventory_capacity_hybrids.md` line 182). HA-24's price term moves "five of the thirteen strategy-product cells that meet the service target ... from commercially possible to impossible as the price falls from break-even to 18.00 USD" (queue HA-24). HA-38 decides the capacity leg outright: "HA-38 returning 'nobody funds standing availability' leaves every capacity-carrying design unfunded by construction" (`../design_space/strategic_synthesis.md` section 7), against a recorded precedent where "two of three sites used none of their capacity and the third 7%, about 4M USD per year of task orders against a stated ready-state requirement of 30M to 60M (F8-S09, F7-S01)" (queue HA-38) | not contacted (0/3) |
| 4 | Generic-drug and 503B regulatory, CMC | 4 | HA-23 [12], HA-34 [13], HA-42 [19]; reviewer track HA-31 [11] | HA-23 removes the contracted family's central advantage if it comes back the wrong way: "if it is a prior-approval supplement with a preapproval inspection, **S12's 365-day leg does not exist** and the virtual-network family loses its central advantage over building" (queue HA-23). HA-31 gates every decision class: "Until a status is assigned, all sixteen gates are UNCERTAIN, no strategy can receive a favorable class, and `regulatory` returns NO_CONCLUSION for any strategy no gate names" (queue HA-31). HA-34 decides whether the one surviving intervention on the binding constraint exists: "whether family 11 exists as an intervention at all, and whether the 14-day sterility pole is a constant or a design variable" (queue HA-34), for the point `../design_space/prior_art_review.md` section 6.1 makes: "Of the interventions collected across the fourteen families, this is the only one that acts on the binding release constraint itself rather than on components that are not binding" | not contacted (0/4) |
| 5 | GPO, wholesaler, distributor | 3 | HA-24 [10] demand-visibility, allocation and transport half, HA-11a [5] and HA-40 [6] at the wholesaler echelon, HA-43 [22]; reviewer track HA-33 [24] | It is the second and independent source for the denominator that decides the map (HA-11a, above), and the only source for the transport and allocation inputs. HA-43 sets the window inside which the metric forgives a miss, which is an open defect: "`fill_rate` forgives anything delivered within `backorder_window_days` = 7 and charges the rest to its origin day", and its "sign is not monotone in the window: +0.016160 at norepinephrine S7, -0.005881 at sodium S0" (MD-5, `../design_space/bottleneck_decomposition.md` section 7) | not contacted (0/3) |
| 6 | Drug-supply economist, operations researcher, or reliability engineer holding multi-site event data | 2 | HA-39 [14], HA-25 [28]; reviewer track HA-32 [26] | HA-39 collapses or holds the feasible set: "20 crossings; at base demand the feasible set collapses from 11 strategies to 3 on norepinephrine and from 10 to 2 on sodium bicarbonate as the rate rises from 0.02 to 0.3", and common-cause dependence "carries the largest non-artifact EVPPI in `results/sensitivity/voi.json`, 1,150,473 USD/yr against 1,016,954 for capacity utilization" in a run that is superseded and must not be quoted as current (queue HA-39). HA-25 reaches the comparison itself, which has already changed once: "it is not true that no frozen comparator meets the frozen target. Added central capacity meets it for both products once it is searched over the same inventory space" (`../design_space/feasibility_regions.md` section 8) | not contacted (0/2) |
| 7 | Quality, CMC, microbiology, validation | 4 | HA-22 [16], the route half of HA-34 [13] shared with role 4; HA-14 [27] as a quotation, see section 7 | It holds the sharpest condition in the whole grid: "norepinephrine S15 and sodium bicarbonate S11 lose the target 0.31 d above the 14 d sterility incubation base" (`../design_space/feasibility_regions.md` section 2.3). HA-22 also bounds the OS case: "At the declared low corner (0.005 per batch) the perfect-OS bound above shrinks by roughly a factor of four" (`../design_space/os_only_and_virtual_network.md` section 6.1 item 2). What it cannot reverse is stated in section 5 below, and is the reason this role ranks last rather than third | not contacted (0/4) |
| 8 | Manufacturing quality or IT budget owner at a generic sterile-injectable firm or a CDMO, as a software buyer (recorded, no slots this cycle, see section 3) | 0 | HA-37 [29] | **Reverses nothing today.** The queue states it plainly: "none today. It needs a revenue side in `economics.py` before the answer changes any number", and its decision value is "whether the OS-first roadmap can be costed at all" (queue HA-37). The engine prices an operating system as a cost of 100k to 800k USD per site-year and has no revenue side | not contacted (0/0) |

Total target **30**, which is the top of the protocol's declared 25 to 30. Count only completed conversations with
logged evidence in `data/interview_evidence/<id>.json` at `status: complete`.

---

## 3. The seventh role, and why the software buyer is an eighth rather than part of it

`../design_space/definition_of_finished_status.md` DF18 records that the design-space work "identified three interview
roles that had no queue row: the OS buyer (**HA-37**), the purchaser of standing availability (**HA-38**), and the
regional stocking point whose replenishment rule decides 8 of 16 Phase A cells (**HA-40**)". All three now have queue
rows. None had a row in this matrix. The third of them needs no new role: HA-40's holder is a planner "at an IDN, GPO
or wholesaler (the HA-20 pool)", which is inside roles 1 and 5 already, and it is named in both.

**The purchaser is a seventh role.** The six original roles are defined by function. None of them is defined by
authority to commit money, and none of them reaches a state or federal programme officer, whom HA-38 names. The
distinction is not cosmetic: HA-24 asks a category manager what a premium looks like, and HA-36 asks a signatory
whether they would sign one, at what volume, term, price and failure-to-supply remedy. The model treats those as
different objects. HA-24 feeds a price argument; HA-36 feeds all nine `ContractTerms` fields, and until they are
filled every design in the battery is recorded "not contractable, stated". The role also carries a guardrail the other
six do not need, which is the second reason to write it down separately: a conversation with someone who can sign is
the one most easily mistaken for selling. See section 4.

**The software buyer is a separate eighth role, not part of the seventh.** Four reasons, and any one of them is
sufficient.

1. Opposite sides of the market. The purchaser buys a vial from a manufacturer. The OS buyer sits inside a
   manufacturer or a CDMO and buys software out of a quality or IT budget. A person who can commit a health system's
   drug spend has no authority over a CDMO's software budget.
2. Different model entry. HA-36 and HA-38 enter `contracting.py` and the reservation-fee and take-or-pay ledger in
   `simulation.step8_costs`. HA-37 enters nothing: "no model field exists today" (queue HA-37).
3. Different decision value. The purchaser row can reverse a result now. The OS row cannot until the engine has a
   revenue side, and the operational value it would be sold against is small in this model: the perfect-OS ablation
   moves mean fill by +0.001771 averaged over 40 cells (`../design_space/os_only_and_virtual_network.md` section
   3.1).
4. Different standing in the prior-art review, which puts "the manufacturing OS in any of its eight sub-forms" on
   its does-not-survive list (`../design_space/prior_art_review.md` section 6, closing paragraph). Merging it into
   the purchaser row would hide that.

Role 8 therefore carries zero slots this cycle and stays in the table so the gap is visible rather than dropped. It
becomes worth slots when `economics.py` has a revenue side, and not before.

---

## 3a. Why HA-11 is split into HA-11a and HA-11b

The queue's HA-11 asks two things in one row: "what is the national and regional utilization of each longlist
presentation in units per year, and what installed capacity serves it?" This matrix used to assign both halves to
role 1. Only the first half is answerable by that role.

- **HA-11a, the demand denominator.** A hospital, IDN or GPO analytics owner holds purchase history. It is an
  interview question for roles 1 and 5, it is queue rank 5, and it is the highest-decision-value evidence item any
  interview can close.
- **HA-11b, installed capacity serving the presentation.** Nobody on the demand side holds this. It sits with
  manufacturers, with FDA establishment registration and drug listing, with DQSA section 506C notifications, or with
  a commercial data vendor. It is an evidence-acquisition task, not a conversation, and the only interview half of it
  is line rates from role 2 (`modules/manufacturing.md` questions 1 and 2). Asking a pharmacy director for installed
  aseptic capacity gets an impression, which logs at tier 5 and changes nothing.

Both halves are still needed and both still feed `config/products/*.yaml` and `demand.py`. Splitting them stops one
of the two from being asked of a person who cannot answer it, and stops a tier-5 impression being logged as though
it were the answer.

## 4. Guardrail on role 3

No term sheet is shown, offered or discussed. Nothing is signed, and no follow-on commercial contact is implied. The
outreach and the opening both state that no commitment is sought and that the study cannot supply anything. A
purchaser's answer is logged as an elicited range or a stated term, never as an intent, an interest, a pipeline entry
or a letter. The protocol's attribution rule governs: "never call interviewees partners, validators, or advisors
without authorization" (`protocol/protocol.yaml` `interview_program.attribution_rule`), and the claim-discipline table
forbids "'Partnered with' after an interview". If a purchaser volunteers a commitment, it is recorded as a claim
needing written confirmation, and it changes no model input until the writing exists.

---

## 5. What each role must be able to reject, and what it feeds

| # | Role | Must be able to reject | Parameters and model entry point |
|---|---|---|---|
| 1 | Hospital pharmacy / IDN supply chain / demand analytics | the demand denominator and its regional split, the regional replenishment rule, days of supply actually held, allocation and substitution practice, the backorder window, and the premise that anyone would hold a positioned finished-goods tier. **Not installed capacity:** that is HA-11b and this role does not hold it | `product.annual_demand_units`, regional shares, `region_base_stock`, `region_reorder_point_days`, `target_safety_stock_days`, `backorder_window_days`, allocation policy, criteria `clinical_criticality` and `demand_contract_fit`. Entry: `config/products/*.yaml`, `demand.py`, the region policy block in `strategies.build_strategy` |
| 2 | Sterile manufacturing / process engineering / fill-finish vendor / CDMO commercial | batch size and batches per site-year, campaign length, OEE, changeover, restart after a deviation, node capital and fixed operating cost, the reservation fee and what it covers, minimum campaign size, and the elapsed time from decision to first released batch | `units_per_batch`, `batches_per_site_year_nominal`, `uptime_fraction`, `changeover_days`, `production_cycle_days`, `capital_usd_per_site`, `node_scale_fraction`, `node_commissioning_days`, `capacity_expansion_days`, reservation fee, criterion `manufacturing_fit`. Entry: `config/products/*.yaml`, `config/strategies/design_space.yaml`, `production.py` |
| 3 | Purchaser with budget and contracting authority | the 18.00 USD per unit price assumption, the committed volume and term, the failure-to-supply remedy, allocation rights, and the existence of any payment for standing availability separate from units shipped | all nine `ContractTerms` fields: payer, purchaser, beneficiary, term, committed volume, activation condition, allocation rights, default risk, price. Entry: `contracting.py`; the reservation-fee and take-or-pay ledger in `simulation.step8_costs` |
| 4 | Generic-drug / 503B regulatory, CMC | the pathway map, the G07 reporting category and its lead time, 503B transitions, cross-site and shared-quality-unit claims, and the sterilization route recorded for each presentation | gates G01 to G16, `second_source_qualification_days`, `node_commissioning_days`, `bud_503b_days`, `ProductFeatures.sterilization_route`. Entry: `config/regulatory_gates.yaml`, the activation leads in `config/strategies/design_space.yaml` |
| 5 | GPO / wholesaler / distributor | demand visibility and where inventory sits by echelon, allocation rules under shortage, transport times and emergency premiums, resilience premiums as they appear in contracts today, and how long an order stays a backorder | `distribution_usd_per_unit`, `delivery_days`, `emergency_transport_premium`, `reserved_capacity_fee_fraction`, `backorder_window_days`, criterion `demand_contract_fit`. Entry: `economics.py`, `allocation.py`, the fill-rate metric definition in `simulation.step5_serve` |
| 6 | Economist / operations researcher / reliability engineer | the dependence structure, the comparator optimization and its unmatched search spaces, the calibration, the recovery definition, and the welfare boundary | `global.common_cause_events_per_year` with duration and impact fraction, `demand_autocorrelation`, optimization method, recovery definition. Entry: `disruptions.py`, the common-cause groups in `strategies.build_strategy`, `optimization.DESIGN_SPACES` |
| 7 | Quality / CMC / microbiology / validation | the release-time decomposition and what runs in parallel, deviation and rejection rates, investigation duration, validation replication across sites, and the acceptable role for a model in a GMP decision | `sterility_incubation_days`, `environmental_monitoring_days`, `assay_days`, `endotoxin_days`, `qa_review_days`, `deviation_rate_per_batch`, `batch_rejection_rate`, `investigation_duration_days`, `validation_usd_one_time`, `fixed_qa_labor_usd_per_site_year`, gates G03 to G06 and G15 |
| 8 | Software buyer (OS) | the number of sites on one contract, the annual contract value per site, and the spend it would displace | no model field exists. It needs a revenue side in `economics.py` first |

**Why role 7 ranks last.** The model says the release queue is not where the constraint is: "zeroing the whole
chemical queue removes exactly 2 days, 12.5%" of a 16-day hold
(`../design_space/bottleneck_decomposition.md` section 6.6). A fully validated release layer saves zero days while
sterility binds, and the package holds a test of that name
(`tests/integration/test_extremes.py::test_full_release_assurance_saves_no_days_when_sterility_binds`). The synthesis
records that "five assignment failure modes bind nowhere at all", and deviation or rejection is one of them
(`../design_space/strategic_synthesis.md` section 3, on `../design_space/bottleneck_decomposition.md` section 4).

Four conversations are still worth holding. The one quality number the grid is acutely sensitive to is the sterility
incubation itself, and the deviation rate is the input that would shrink the OS bound by a factor of four. The role is
not demoted for being unimportant in practice. It is demoted because this model has already found its own answer
insensitive to most of what this role supplies, and a conversation that cannot move a result is worth less than one
that can.

---

## 6. Count allocation, and the protocol constraint

Protocol v1.0.0 `interview_program.targets` declares six roles with per-role minima and maxima and
`total_target: [25, 30]`. The allocation above keeps every one of those six inside its declared band:

| role | protocol band | allocated | position in band |
|---|---|---|---|
| hospital pharmacy / supply chain | 6 to 8 | 8 | maximum |
| sterile manufacturing / process | 5 to 6 | 6 | maximum |
| quality / CMC / microbiology / validation | 4 to 5 | 4 | minimum |
| generic-drug or 503B regulatory | 3 to 4 | 4 | maximum |
| GPO / wholesaler / distributor | 2 to 3 | 3 | maximum |
| drug-supply economics / operations research | 2 to 3 | 2 | minimum |
| purchaser with contracting authority | not in the protocol | 3 | new |

The reasoning, stated rather than implied.

1. **Hospital and IDN takes the maximum of 8** because it is the only role that carries both of the two
   highest-value evidence items, HA-11a at queue rank 5 and HA-40 at rank 6, and because those two need different
   people. HA-11a needs an analytics owner who can export utilization; HA-40 needs a stocking-point or distribution
   planner who knows the review policy and the order-up-to level; HA-20, HA-35 and HA-43 need pharmacy leaders. That is
   at least three kinds of person before any redundancy.
2. **Manufacturing takes the maximum of 6** because HA-13 and HA-21 also name different people, an engineering vendor
   or CDMO commercial lead for capital and reservation price against line engineers for batch, campaign and
   changeover, and because 81.0% to 93.7% of annual cost in every comparator rests on what they say.
3. **The new purchaser role takes 3**, one for each of the three purchaser types HA-38 names: an IDN executive, a GPO
   contracting lead, and a state or federal programme officer. Fewer than three lets one refusal decide a question
   whose fallback is a hard assumption, "assume no until a purchaser says otherwise"
   (`../design_space/strategic_synthesis.md` section 2 item 6). Three is a floor for that, not a sample.
4. **Regulatory takes the maximum of 4** because HA-23 wants more than one independent reading of the same reporting
   category before an activation lead is changed, and HA-34 is a separate question that needs a route reading per
   presentation. HA-31 is not counted here; see the note below.
5. **GPO takes the maximum of 3** because the demand denominator needs a second source that is not the hospital side,
   and because HA-24's non-price half and HA-43 come only from this echelon.
6. **Operations research sits at its minimum of 2, and that is the weakest part of this allocation.** HA-39 is queue
   rank 14 and outranks HA-22 at rank 16, so on decision value a third operations-research conversation is worth more
   than the fourth quality conversation. It does not get one because the total is capped at 30 and the quality
   minimum of 4 is set by the frozen protocol. The trade is named so it can be taken deliberately: if a revision
   lowers the quality minimum to 3, the freed slot should go to operations research, and specifically to the
   reliability-engineer variant HA-39 names, who is a different person from the drug-supply economist.
7. **Quality sits at its protocol minimum of 4** for the reason given at the end of section 5.

**Two arithmetic notes on the protocol itself, recorded rather than fixed here.** The six declared maxima sum to 29,
so the declared total of 30 was not reachable under six roles; it becomes reachable with the seventh. And the six
declared minima sum to 22, below the declared total minimum of 25, so the protocol's floor was already only reachable
by exceeding some role's minimum.

**Protocol status of this proposal.** Adding a seventh role changes `protocol/protocol.yaml`
`interview_program.targets`, which is frozen at v1.0.0. Under `../../CLAUDE.md` that needs a `protocol/revisions.csv` row
and a version bump, and neither exists. Until one does, the protocol's six-role allocation stands and the row for
role 3 is a proposal. The delta a revision would carry is small and is stated in full: add
`{role: purchaser_contracting_authority, min: 3, max: 3}`, leave the six existing bands untouched, and leave
`total_target` at [25, 30]. Nothing else in the protocol changes.

---

## 7. What does not count toward the total

- **Quotations are not interviews.** HA-12 (supplier commercial contacts for API, vials, stoppers, seals, labels and
  packaging), HA-14 (contract laboratory price list for release testing) and the vendor half of HA-13 (a budgetary
  estimate for an installed and qualified line) are procurement asks. What they produce is a document, which is tier 2
  evidence, not tier 4 qualified expert elicitation. They are named against roles 2 and 7 as work to do, and they do
  not count against DF18's 25. `outreach_templates.md` template E treats its vendor request the same way. The
  commercial half of HA-13, what a reservation agreement costs, what the fee covers and the minimum campaign size, is
  elicitation from a CDMO commercial lead and does count.
- **Independent reviews are a separate track.** HA-30, HA-31, HA-32 and HA-33 are the reviewers required by
  `protocol/protocol.yaml` `independent_review` and counted by DF19, not DF18. HA-31 appears in role 4's row at queue
  rank 11 because the same qualification pool supplies it, and an interview cannot close it: it needs a written
  opinion with a named reviewer, a qualification, a date, the issues, the decisions and the model changes that
  followed. Whether one person may serve as both an interviewee and an independent reviewer is not decided in this
  file, and it should be settled before anyone is approached twice.
- **A conversation with no directly relevant experience does not count**, per the protocol's counting rule, however
  useful it was.
- **An incomplete evidence log does not count.** The record has to exist at
  `data/interview_evidence/<interview_id>.json` with `status: complete` and every field the schema requires.
  **DF18 counts records at `complete` only** (`reporting.py` counts exactly that value). A record is written at
  `status: pending_confirmation` within 24 hours, sent to the interviewee for correction, and promoted to `complete`
  on their reply or after a stated wait (`elicitation_worksheet.md` section 10). A conversation held but not
  confirmed is not yet an interview for counting purposes, and the schema now carries the intermediate state so the
  difference is visible rather than assumed.

---

## 8. Outreach status, and two loose ends

All rows are `not contacted`, and no outreach has been sent.

`outreach_templates.md` was rewritten in the same pass as this file and carries eight templates, A to H, whose
role mapping matches the ranking here: A and B for role 1, C for role 3, D and E for role 2, F for role 7, G for
role 4, H for role 6. Role 5's echelon is reached through templates B and C rather than through a template of its
own. Each template attaches the role **handout** in `modules/handouts/`, never the module: the modules are the
interviewer's copy and quote model results in three of their six columns.

Two loose ends that neither file can close on its own.

1. **Closed 2026-09-06: `modules/purchaser.md` now exists.** It is written from the field kit's purchaser cards,
   the two contracting questions that were in `modules/hospital_gpo.md`, the allocation and resilience-premium
   questions in `modules/distribution.md`, and template C's body, with section 4 above as its preamble. It asks
   HA-38 first and alone, then price, committed volume, term and failure-to-supply remedy, then allocation rights,
   because a yes on standing availability changes what every later question means. Its handout is
   `modules/handouts/purchaser.md`.
2. **`evidence_log_schema.json` has no `role_category` value for role 3.** The enum holds the protocol's six values,
   so a purchaser interview logs today as `gpo_wholesaler_distributor`, which is what `outreach_templates.md` template
   C records. Adding a value is the same revision as adding the role, and until it lands the count for role 3 cannot
   be read off the logs by category alone.
