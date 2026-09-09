# Architecture taxonomy

Assignment deliverable 1. Companion to `morphological_matrix.csv` (deliverable 2), which holds 18 dimensions and
130 options with a source id or an explicit "no external precedent found" on every row. This file says how those
options map onto the fourteen assignment families and onto the Phase A binding mechanisms, which combinations are
barred, and the rule set that decides what enters the Generate stage.

Prepared 2026-09-03. **PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every quantitative statement here is
model behaviour under tier-5 inputs, not a finding. Revisions R004 and R005 landed on 2026-09-03, so every run made
before that date is superseded for quantitative use; the mechanism conclusions in
`bottleneck_decomposition.md` sections 4, 7 and 8 are what this file designs against, not the numbers. Nothing here
is legal or regulatory advice, and no regulatory gate is treated as passed.

**Phase A mechanism vocabulary.** Binding on service: capacity shortfall, insufficient surge headroom, inventory
timing, common-cause failures, supplier concentration, contract insufficiency, regulatory unavailability,
commissioning delay. Binding on cost only: fixed quality cost (24.1% to 33.0% of annual cost), replicated validation
cost (4.7% to 18.0%), low utilization. Measured but not binding: release queue, sterility-related delay (the argmax
of the release set, consequence small), deviation and rejection, demand variance, demand covariance, API lead time,
component lead time. Artifacts: MD-1 to MD-25 in section 7 of the decomposition.

---

## 1. Families, mechanisms, and what the engine can represent

"Representable now" is about `schemas.py` and `strategies.py` as they stand after R005: what a `StrategyDesign` with
`site_plans`, `extra_suppliers` and the documented design variables can express without new code.

| family | mechanisms it can address | mechanisms it cannot | representable in the engine now |
|---|---|---|---|
| 1 Existing Telo architectures | capacity shortfall; insufficient surge headroom; inventory timing (stock nearer demand) | commissioning delay (it creates it, 730 d); common-cause failures (every node shares `cc_api`, `cc_vial`, `cc_os`, `cc_quality`); supplier concentration; fixed quality and replicated validation cost (it multiplies both); sterility-related delay | **yes**. S0-S6 frozen, plus the S8+ generic builder. Missing: nothing structural; MD-8 (node capacity quadratic in `capacity_factor`) must be closed before `capacity_factor` enters a node search space |
| 2 OS-only | deviation and rejection; investigation duration | every binding mechanism. The protocol forbids an OS effect on release time or capacity, and a shared OS version is itself a common-cause group | **partial**. `deviation_rate_factor`, `investigation_duration_factor` only. Missing: a QA-labour cost channel the OS could reduce, any revenue side, and a multi-owner entity |
| 3 Virtual manufacturing network | commissioning delay (registered capacity, 0.000000 delta, 21 d rather than 730 d); capacity shortfall; insufficient surge headroom; contract insufficiency; fixed quality and validation cost (borne by the partner) | supplier concentration and common-cause failures where partners share API, container or geography; regulatory unavailability | **partial to yes**. `cdmo_reserved` site plans with `activation_lead_days`, `activation_failure_probability`, `take_or_pay_fraction`, `reserved_site_owned=0`. Missing: a per-partner qualification state (a site is usable or not), data rights, channel conflict |
| 4 Hub-and-spoke | fixed quality cost; replicated validation cost; commissioning delay (spokes are simpler) | capacity shortfall on its own; sterility-related delay; common-cause failures (the hub is a new single point) | **partial**. A hub is representable only as an `extra_supplier` with a lead time. Missing: bulk hold time and expiry, hub capacity limit, transport of intermediate as a failure mode, a shared quality unit as a cost object rather than a per-site multiplier |
| 5 Postponement | demand variance; demand covariance; inventory timing | capacity shortfall; commissioning delay; sterility-related delay | **no**. MD-15 (one product per network) blocks it. Missing: multi-SKU demand, an intermediate inventory stage with its own expiry, a labeling step |
| 6 Multi-product portfolio | low utilization; fixed quality cost; replicated validation cost | any service mechanism for the product in shortage | **partial**. `portfolio_capacity_share` and `portfolio_fixed_cost_share` attribute a share of capacity and fixed cost, which is an accounting proxy. Missing: several products in one run, changeover, cleaning validation, campaign sequencing, correlated shortages across the portfolio |
| 7 Warm standby and prequalified capacity | insufficient surge headroom; contract insufficiency; commissioning delay (if already prequalified) | chronic capacity shortfall; fixed quality cost (it adds it); common-cause failures | **yes**. `reserved`, `reserved_site_owned`, `exercise_batches_per_year`, `activation_failure_probability`, `activation_threshold_days`, `campaign_batches`. Missing: readiness decay when a line is not exercised, and requalification lead after a lapse |
| 8 Inventory-capacity hybrids | inventory timing; insufficient surge headroom; capacity shortfall (partly); component and material availability | commissioning delay; regulatory unavailability; the cost blocks | **yes**. `safety_stock_days`, `site_fg_days`, `region_base_stock`, `region_reorder_point_days`, `material_target_days`, `material_reorder_days`. Missing: a shared reserve entity with allocation rights; MD-1 is unfixed, so material buffers still scale with the lead time |
| 9 Upstream-first | supplier concentration; common-cause failures on the API group; component and material availability | capacity shortfall; commissioning delay; regional inventory timing; the cost blocks | **partial**. `independent_api_supplier`, `second_source_exists_at_t0`, `component_lead_fraction`, `extra_suppliers`. Missing: a multi-tier graph (key starting material behind API), per-component supplier capacity, and a mid-run switching policy that consumes `qualification_lead_time_days` |
| 10 Contracts and procurement | contract insufficiency; low utilization | every physical mechanism | **partial**. `ContractTerms` names the nine required fields and `contract_requirement` derives premium, break-even price, committed volume, take-or-pay share and implied utilization. Only `take_or_pay_fraction` touches the simulation. Missing: a payer entity, default risk, and allocation rights beyond the four `allocation_policy` values |
| 11 Terminal sterilization and release route | sterility-related delay; release queue (neither binds in Phase A) | capacity shortfall; commissioning delay; inventory timing; common-cause failures; the cost blocks | **partial**. `ReleaseScenario` R0-R3 over the frozen release-component vector. Missing: sterilization route as a product attribute, a parametric-release scenario distinct from R3, per-site parametric validity, and a reformulation lead time for route conversion |
| 12 Product selection | indirectly all of them, most sharply capacity shortfall (through `status_quo_utilization`), regulatory unavailability (503B eligibility) and sterility-related delay (through route) | nothing by itself; it is a selection layer over the other thirteen | **partial**. Two product dossiers exist and WB-26 records they are near-clones on several axes, so most apparent product discrimination in the run is not evidence. The matching model is not built |
| 13 Public-private infrastructure | contract insufficiency; low utilization; capital requirement | every physical mechanism | **no**. Missing: a funder entity, grant capital as a distinct cost line, and programme eligibility as a time-varying gate |
| 14 Mobile and modular | commissioning delay (claimed); capacity shortfall | sterility-related delay; common-cause failures; the cost blocks | **partial**. `commissioning_days` per site plan is the only handle. Missing: a mobility clock, requalification after movement, and registration state per unit. Family 14's own verdict is that the release clock restarts after a move, which makes mobility slower than shipped inventory |

**Reading of the table.** Only four families reach a binding service mechanism cleanly in the engine as it stands:
3 (virtual network, on commissioning delay and capacity), 7 (warm standby, on surge headroom and contract
insufficiency), 8 (inventory-capacity hybrids, on inventory timing and surge headroom) and 1 (existing architectures,
on capacity, at the cost of commissioning and both cost blocks). Families 2, 10 and 13 reach no physical mechanism at
all; families 5 and 6 reach only cost; family 11 reaches a mechanism that Phase A says does not bind, with the single
exception of route conversion, which removes rather than compresses it.

---

## 2. Incompatibilities between options

Hard constraints only. Each carries a source id or a CFR or Annex citation. A combination listed here is not a
trade-off to be priced; it is unavailable until the cited evidence changes.

1. **Parametric release with a multi-site network.** FDA's generic-drug sterility FAQ ties the abbreviated route to
   the identical facility, autoclave, container-closure, parameters and load patterns (F11-S46). So route option
   "terminal moist heat with parametric release" combined with any distributed topology is UNCERTAIN at best, and if
   parametric release is a per-site asset its cost scales with node count like replicated process validation.
2. **Container-closure integrity testing cannot substitute for the release sterility test.** FDA's 2008 guidance
   bounds the substitution to stability protocols (F11-S14). No release-assurance option may claim it.
3. **No analytical or statistical method removes the sterility attribute.** Only the process route does
   (F11-S02, F11-S03, F11-S41). Any AI or conformal layer stays decision support; abstention is never release.
4. **503B is never durable.** No injectable is on the 503B bulks list (L503B-S02); FDA "does not interpret supply
   issues, such as backorders, to be within the meaning of 'clinical need'" (L503B-S07); the copy rule ends the
   product line when the shortage listing ends (L503B-S03). The engine enforces this: the `StrategyDesign` validator
   rejects `pathway=503b` with `durable=true`.
5. **Beta-lactams and penicillins cannot share a facility with other products.** 21 CFR 211.42(d) and FDA's
   beta-lactam guidance (F6-S01, F6-S10). Cytotoxics and high-potency products are bounded by HBEL carryover limits
   and Annex 15 chapter 10 cleaning validation (F6-S04, F6-S07, F6-S08). Product-class option "cytotoxic or
   high-potency" is therefore incompatible with portfolio options above one family.
6. **Sterile-filtered bulk cannot be held indefinitely.** EMA expects refiltration if bulk is not filled within
   24 hours (F5-S16). Inventory option "bulk or unlabeled intermediate held as the buffer" combined with hub-and-spoke
   topology needs a validated multi-day hold, which prior art could not find for any approved aqueous injectable
   (F5-S10, F5-S13, prior-art review section 7 item 3).
7. **One quality unit across units requires one legal entity.** The DME framework requires an approved application, a
   preapproval inspection, one management, a unified pharmaceutical quality system and a single legal entity as
   registrant, and the proposed rule excludes contract units (L503B-S06, LQBR-S25, LAMD-S25, Lrepo-S2). So regulatory
   option "one quality unit spans every unit" is incompatible with third-party-owned topologies and with leased suites
   inside other companies' plants.
8. **A mobile unit has no US registration instrument today.** 21 CFR Part 607 contains no mobile provision and the
   DME rule is proposed, not final (F14-S01, F14-S02, F14-S68). Facility option "trailer or container mobile
   cleanroom" combined with "Telo holds the application" has no legal vehicle; the DEA mobile narcotic treatment rule
   is the only codified US precedent and it is a different agency (F14-S12).
9. **Concentrates are a documented hazard, not a free pooling form.** Joint Commission and FDA label rules restrict
   them and ASHP conservation guidance treats them as a risk (F5-S22, F5-S23, F5-S24, F5-S51).
10. **Pooled unlabeled inventory across several application holders has no operating instance.** Late labeling itself
    is permitted under 21 CFR 211.130(b) since 1978 (F5-S08); the multi-holder pool is not (F5-S31, F5-S33).
11. **Readiness payments are legally unpriced.** Availability payments and resilience premiums are gated on four
    counsel questions: anti-kickback treatment, antitrust after the 2023 withdrawal of the joint-purchasing safety
    zone, 340B and Medicaid inflation-rebate mechanics, and whether an availability payment untied to quantity is
    procurable under FAR Part 16 (prior-art review section 7 item 9, from F10 section 9 item 11).
12. **Multi-owner capacity coordination is an antitrust problem first.** HDA names the Sherman Act and DOJ/FTC
    monitoring, and reports the federal control tower has no two-way communication (F2-S63, F2-S64, F3-S19).
13. **No free instant capacity.** Since R004 any `capacity_factor` above the status-quo scale of 1.05 is an expansion
    and waits `capacity_expansion_days` (365 d, tier 5). Node-size option "expansion of the incumbent line" cannot be
    combined with a claim of day-zero surge; `instant_expansion` exists only for a labelled sensitivity.
14. **Nominally separate sites are not independent.** Every S0-S7 topology shares at least one common-cause group and
    one supplier set, and since R005 a second node in one region joins that region's geography group. Topology option
    "two sites inside one region" may not be counted as redundancy across regions.
15. **Records a machine writes are still GMP records.** Warning Letter 320-26-58 applies 21 CFR 211.22(c) to
    AI-generated GMP records (F2-S52). Any OS option that generates records carries inspection exposure for the
    customer, which is a liability, not a feature.
16. **Reimbursement is not manufacturing cost.** CMS pays eligible hospitals of 100 beds or fewer, outside a chain,
    for a six-month buffer (LSD-S3). Inventory option "rotating hospital inventory funded by the CMS buffer payment"
    funds the buyer's stock, not the maker's readiness, and may not be priced off ASP.

---

## 3. Pruning rule set for the Generate stage

An architecture is a selection of one option per dimension. The rules below are applied in order; the first failure
rejects, and the reason is recorded in `falsification_register.csv` rather than discarded.

- **P1 Binding-mechanism test.** Keep only if the architecture changes at least one mechanism Phase A records as
  binding on service: capacity shortfall, insufficient surge headroom, inventory timing, common-cause failures,
  supplier concentration, contract insufficiency, regulatory unavailability, commissioning delay. An architecture
  that reaches only fixed quality cost, replicated validation cost or low utilization is kept for the cost objective
  and must be labelled as a cost architecture, never as a service one.
- **P2 No artifact-only architectures.** Reject if the whole effect runs through a known model defect, above all
  MD-3 (the frozen regional review rule), MD-5 (the 7-day backorder window), MD-6 (site accrual and horizon
  censoring, fixed in R004), MD-7 (free instant expansion, fixed in R004), MD-11 (the optimizer tie-break),
  MD-17 (three commissioning-family parameters coincident with `warm_up_days`, which bears directly on every
  commissioning claim this taxonomy credits to families 1, 3 and 7), MD-18 (`release_time_factor` inert in the
  stochastic engine, which is why S6 is numerically identical to S5), MD-23 (a banked campaign batch blocks an
  exercise batch, so an exercise cadence is measurable only on a rarely activated line) and MD-24
  (`take_or_pay_fraction` has no service channel, so a cost-minimising optimizer removes it). An architecture may
  be kept if its effect is shown to survive the fix; the pre-2026-09-03 runs cannot show that, so the re-run
  comes first.
- **P3 Prohibition screen.** Reject on any of: an assumed gate PASS; a loosened `tau` or `q`; a tail risk not
  reported; 503B as a durable core; a release component reduced below the frozen value outside a labelled and
  validated rapid-micro scenario; abstention counted as release; a price inferred from a cost or from reimbursement;
  independence claimed where common-cause groups are shared; a fabricated interview, partner, customer or review.
- **P4 Contractability screen.** Every kept architecture fills `ContractTerms`: payer, purchaser, beneficiary, term,
  committed volume, activation condition, allocation rights, default risk, price required. Fields left `None` are
  reported by `missing()`. An architecture with an incomplete contract row is not ranked feasible; it is recorded as
  "not contractable, stated", which is the honest verdict for every readiness-payment design in the current evidence
  base (F3-S28, F7-S16, F10-S24).
- **P5 Prior-art screen.** An architecture the cross-family review classifies `already_implemented` is kept only with
  a stated reason Telo beats the named incumbent, and the incumbent's source id travels with it. An architecture on
  the "does not survive" list (owned distributed microplants, mobility as a response mechanism, the manufacturing OS
  in any of its eight sub-forms, warm standby as an owned asset, standalone upstream diversification, any AI or
  conformal layer positioned as removing the sterility hold) is kept only with an explicit argument against the cited
  evidence, quoted and answered.
- **P6 Representability screen.** If section 1 marks the family `partial` or `no` for the mechanism the architecture
  claims, the architecture does not enter the run battery on that claim. It goes to the falsification register with
  the exact missing engine feature named, and either the feature is built with tests or the claim is dropped.
- **P7 Dominance.** Reject an architecture dominated on both service and cost by a frozen comparator under matched
  design variables, and only after the R004/R005 re-runs. Dominance measured on superseded runs is not evidence.
- **P8 Common-cause honesty.** Any architecture claiming site independence lists the groups its sites actually share
  (`cc_api`, `cc_vial`, `cc_os`, `cc_quality`, `cc_geo_*`). An unshared group needs a reason, not an assumption.
- **P9 Novelty discipline.** No novelty claim without a prior-art source id, or an explicit "no external precedent
  found (search: <family note>)" naming the note that searched.
- **P10 Instrument availability.** An architecture whose first revenue depends on an instrument that does not exist
  today (a final DME rule, an AMT designation, an availability payment, a published comparability protocol covering
  an alternate aseptic site) is kept only as a conditional branch, with the instrument written as an explicit gate
  and its status left UNCERTAIN.

Applied to the matrix, P1 to P3 alone eliminate whole columns: every OS option except the internal-control one fails
P1; every mobility option fails P5; every release-assurance option except rapid micro and parametric release fails P1
because release does not bind; and every readiness-payment contracting option fails P4 until a purchaser answers.
What survives P1 to P10 clusters into four shapes, which Phase D will instantiate as S8+: buy registered capacity
rather than build it; joint inventory and reserved-capacity design; share the quality unit and the filing across
sites; and convert the process route so the sterility hold is removed rather than compressed.

---

## 4. Open questions

1. Whether a parametric release programme can extend to a second site or a second autoclave, and under what reporting
   category (F11-S46). If it cannot, route conversion is a single-site intervention and the whole distributed thesis
   loses its one surviving release lever.
2. The sterilization route of every candidate presentation. Not disclosed on US or EU labels; the prior-art sweep
   calls it the highest-value unresolved input in fourteen families (prior-art review section 7 item 11).
3. Whether a comparability protocol has ever pre-authorized an alternate aseptic site for a generic sterile injectable
   (F9-S37, F3-S46, F3-S47).
4. Whether any approved ANDA or NDA for an aqueous small-molecule injectable lists bulk preparation and aseptic
   filling at different sites. Family 4 calls this its single most decision-relevant gap and the answer sits in
   Module 3.2.P.3 tables that are not public.
5. Whether a spoke can operate with no resident quality-unit staff under a hub quality unit, and where the release
   decision legally occurs (Lrepo-S2, Lreg-S6).
6. Whether any US purchaser will pay a standing reservation fee for sterile shortage-generic capacity, and at what
   price on a $1.47 vial. Family 7 says the design-space review should assume no until a purchaser says otherwise
   (F3-S28, F7-S16).
7. The replenishment review policy and order-up-to level real regional stocking points run. It decides 8 of 16 cells
   at about +0.82% cost and is currently a hard-coded rule the protocol never specifies (MD-3).
8. Installed capacity and true demand for the exact presentation, which decides whether the capacity mode exists at
   all and which of the two products is representative.
9. Whether a shared quality unit and a shared filing are permissible across registered sites. This is the only lever
   on the 24.1% to 33.0% and 4.7% to 18.0% cost blocks that no service mechanism touches.
10. Engine work this taxonomy names as missing and does not yet have: multi-product runs with changeover
    (families 5, 6), a hub with hold time and capacity (family 4), a per-partner qualification state (families 3, 7),
    a sterilization-route attribute and a parametric scenario (family 11), a payer entity and grant capital
    (families 10, 13), and a mobility clock (family 14). Each is a precondition for testing its family, not a
    refinement of a test already possible.
