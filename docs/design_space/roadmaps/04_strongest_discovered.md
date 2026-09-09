# Roadmap candidate 4: the strongest architecture discovered in this review

Deliverable 20 of `../ASSIGNMENT.md` (Phase F), fourth of four candidates.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result quoted here is behaviour of the engine under tier-5 illustrative
inputs and is not a statement about sterile-injectable manufacturing in the world. All sixteen regulatory gates in `config/regulatory_gates.yaml`
(G01 to G16, the sixteenth added under revision R007) are UNCERTAIN with no reviewer and no review date, `eligibility` is NO_CONCLUSION for all
twenty strategies (`../../results/design_space/ds_post_R008/summary.json`, `meta.eligibility`), and no favourable decision class is assigned below.
503B is a time-varying legal state and never a durable pathway. No interview, partner, customer, purchaser or reviewer exists; every organisation
named is a published third party cited by source id. Nothing here is legal or regulatory advice.

## 0. Which architecture was chosen, and why

The strongest architecture in this review is **contracted campaign capacity at already-registered US aseptic lines, paired with a deep positioned
finished-goods tier, monetised by ordinary unit sales**. Two configured strategies carry that shape and **the evidence does not separate them, so
both are carried**: S11 (bright-stock campaign offtake, family 5) and S16 (reserve-triggered campaign network on contracted registered capacity,
family 8). Four measurements chose them. Of twenty strategies only five meet the frozen target (mean fill at or above 0.99 in at least 90 percent
of runs) on both products, and these are two of the five (`../feasibility_regions.md` section 4, `ds_post_R008/dominance.csv`, 40 paired runs).
Both sit on both cost-service frontiers: S11 at 14.86M USD/yr on norepinephrine (fill 0.9950, p_meet 0.95) and 15.71M on sodium bicarbonate
(0.9970, 0.925); S16 at 15.89M (0.9967, 0.90) and 16.48M (0.9972, 0.925). Of the five they are the only two whose required committed share stays
below 1.0 at an assumed 18.00 USD per unit: S11 0.798 and 0.599, S16 0.845 and 0.632, against S13 1.091 and 0.820, S12 1.235 and 0.928, S9 1.460
and 1.097 (same file, section 3 row 1; 18.00 USD is an assumption, not evidence). And both buy capacity that exists, so both lose 0.0000 of the
measured window to commissioning where the distributed-node comparators lose 0.2872 (`../product_architecture_matching.md` section 3.3). That fourth measurement must not be
read at face value. `simulation._commissioning_window_loss` excludes reserved sites (`simulation.py:696-699`), and S16's two contracted lines each carry
`commissioning_days` 540, which is 29.57% of the measured window and during which they cannot make commercial product (`../os_only_and_virtual_network.md`
section 3.2 note; `../inventory_capacity_hybrids.md` section 2 item 5). Only S11's zero is a real zero. A second caveat belongs beside it: S16's
norepinephrine cell meets the tail requirement at `p_meet` exactly 0.90 on 40 paired runs, one binomial standard error (0.047) from failing it, so that
verdict is inside noise and should be re-evaluated at higher n before it is used to choose between S11 and S16.

What separates the two is small and points both ways. S11 is cheaper by about 1.0M USD/yr on norepinephrine and 0.8M on sodium bicarbonate in the
same evaluation. S16 is the only architecture in the battery with a documented shape in all nine `ContractTerms` fields, and it is still not
contractable, because a shape is not a signature (`../os_only_and_virtual_network.md` section 4.1). S16 also holds the only claim in this family a
run supports at all, "supported by the model under illustrative inputs" (`../falsification_register.csv` data row 22), while all three S11 rows are
`untested` and S11's capacity-matched control was never run (data row 9). Against that, S16's distinguishing coupling is inert in the engine
(MD-23, MD-24), and S11's postponement content is expected to be zero by construction, because MD-15 runs one presentation, one market and one
labeler, so the unlabeled pool and the finished-goods pool are the same object. Both readings rest on the same open defects. Read the pair as one
architecture in two contracting forms, and treat the choice between them as an open question that HA-13, HA-21 and HA-36 decide.

Three qualifications belong in the same breath. The advantage is partly an accounting gift: opening inventory is seeded free (NEW-1), which at the
sodium bicarbonate designs is 1,200,000 units, covering 5.08 years of that network's 236,100 units/yr structural gap over a five-year window
(`../inventory_capacity_hybrids.md` section 3.3). The comparison with the frozen comparators was not matched, and re-optimizing four of them over
one common inventory space makes added central capacity (S4) meet the target on both products at 20.0M and 23.7M USD/yr, leaving S11 at 15.7M and
S16 at 16.5M cheaper by a third rather than an order of magnitude (`../feasibility_regions.md` section 8). Both ledgers also carry the incumbent
plant's capital, 6,703,202 USD/yr, identical to S0 (MD-14 residual), so neither figure is a Telo-only cost.

## 1. What the company is on day one, and what it is not

On day one it holds or labels one approved application for one presentation, runs one quality unit, buys campaigns at registered third-party US
aseptic lines, holds positioned finished-goods inventory, and sells finished vials. It owns no new plant and builds nothing; for S16 the two contracted lines still carry a 540-day qualification lead that the engine's commissioning metric does not charge.
It is not five things this review rejected. Not an owner of distributed microplants: prior art records them as occupied in pilot and failed in
every funded federal analogue (`../prior_art_review.md` section 6), and S5 and S6 meet the target in no region of any recorded range of any
swept input on either product (`../feasibility_regions.md` section 6). Not a software vendor: the manufacturing OS is on the does-not-survive list in all eight sub-forms, and a perfect-OS ablation is worth at
best about three cents per delivered unit against an OS cost of 0.32 to 2.56 USD per unit at sodium bicarbonate S17, four sites at the declared low of
100,000 and high of 800,000 USD per site-year against 1,249,852 delivered units (`../os_only_and_virtual_network.md` section 3.1). Not a
release-automation company: chemical real-time release saves zero days while the 14-day sterility incubation binds
(`../release_assurance_followup.md` section 4), and the function this evidence supports is stop-the-line drift detection. Not a 503B operator: no
injectable is on the bulks list, FDA does not read backorders as clinical need, and the copy rule ends the line when the listing ends (L503B-S02,
L503B-S07, L503B-S03). Not mobile or modular: the qualification clock restarts after a move, which is slower than shipping inventory.

## 2. First product or product class

The archetype both designs declare is an aqueous small-molecule solution in a standard vial, non-controlled, not lyophilized, not cold-chain
intensive (`../product_architecture_matching.md` section 3.1). Inside it the evidence supports one partition and nothing finer: capacity-short
presentations, where capacity dominates every other mechanism by two orders of magnitude (leave-one-out mean fill delta +0.05138 against +0.00039),
and capacity-adequate ones, where inventory timing and supplier concentration lead (section 3.3, same file).

**The evidence cannot pick the presentation.** Only two of six longlist candidates carry a configuration, and audit item WB-26 records them as
near-clones differing mainly in `annual_demand_units` (1,200,000 against 900,000) and `units_per_batch` (25,000 against 30,000), both tier 5, so
most apparent product discrimination here is that one ratio. What is snapshot evidence: sodium bicarbonate 8.4% 50 mL is on the FDA shortage list
now, 15 current rows of 19 over 9.51 years, and is not on the 503B bulks list; furosemide 10 mg/mL is the most shortage-persistent candidate at 30
current rows of 33 over 6.40 years but has no configuration, no fixed fill volume (PG1 UNCERTAIN) and an unresolved longlist status; norepinephrine
has 0 shortage rows and 23 Orange Book applicants, the least concentrated supplier structure among the configured presentations, though furosemide is less
concentrated still at 28 applicants over 37 applications; and norepinephrine is one of the four medicines the EDA-funded Civica, Phlow and Occam
End-to-End Commercialization Project names, with ketamine, midazolam and succinylcholine (F13-S24). What would pick one: **HA-11** with **HA-13** and **HA-21**, because utilization and
installed capacity decide which side of the partition a presentation falls on and where it sits against the ceilings in section 12; **HA-34**
(sterilization route, obtainable only from an ANDA or NDA chemistry review, an inspection report naming the cycle, or a named reviewer, never from
a label); **HA-10**; **HA-03**.

## 3. First customer and first measurable value

The customer class the evidence supports is a purchaser of finished vials under a multi-year committed volume: a health system, an IDN, or a GPO
programme of the kind Civica, Premier ProvideGx, Vizient NES and HealthTrust SIMS already run (F10-S01, F10-S05, F10-S06, F10-S08). That class is
chosen by elimination. Prior-art open question 17 finds no US hospital system, GPO or state that has ever paid a standing reservation fee for
sterile generic capacity (F3-S28), and the two largest funded analogues ended with the sites leaving the business (CIADM; the USD 542,750,000
Emergent capacity reservation, F7-S04, LCDM-S35, LCDM-S10). First revenue therefore has to be an ordinary unit sale. No customer exists: zero of
the 42 Phase B candidates is contractable, and `price_required_usd_per_unit` is a model output rather than a price anyone has offered
(`../os_only_and_virtual_network.md` section 4.1).

First measurable value, as the buyer would observe it: units delivered against the committed volume, days of supply held at the buyer's own
stocking points, and a failure-to-supply remedy exercised or not. The in-model proxies are fill rate and P(fill >= 0.99), which are model behaviour
and not evidence of value. Expect the risk to be compliance rather than capability: HHS records that erosion of failure-to-supply clauses in GPO
contracts may be associated with shortages (F10-S10), a competing programme's comparison implies 30 to 50 percent contract compliance (F10-S09),
and under 15 percent of one GPO's members' generic injectable purchases went through its shortage programme (F10-S15).

## 4. Data-access strategy

| Data needed | Who holds it | What must be given for it | Id |
|---|---|---|---|
| Utilization per presentation, national and regional | hospitals, GPOs, wholesalers; CMS Part B is an outpatient proxy only | committed volume or a paid licence; nothing in this package establishes what a holder will accept | HA-11 |
| Line capacity, batch rate, changeover, minimum campaign size, what a reservation fee covers | CDMOs and engineering vendors; no public US sterile fill-finish rate card, minimum order value or reservation fee exists in 313 landscape sources | a paid feasibility or tech-transfer engagement and a quality agreement, which cannot delegate CGMP responsibility (F3-S41) | HA-13, HA-21 |
| API, vial, stopper and label quotes; release-testing prices; shortage duration; USP `<71>`, `<72>`, `<73>`, `<1071>`, `<1223>` text | suppliers; contract laboratories; ASHP and USP, both paywalled | a qualification programme and volume; test volume; subscriptions with manual retrieval under site terms, not redistributable | HA-12, HA-14, HA-10, HA-17 |
| Sterilization route per presentation | an ANDA or NDA chemistry review, an inspection report, or a qualified reviewer | professional engagement | HA-34 |
| Contract terms: payer, purchaser, term, volume, activation, allocation, default, price | GPO, wholesaler or IDN contracting leads | a term-sheet negotiation | HA-36, HA-24, HA-33 |

Two limits. The engine has no per-partner data record, no ownership of process or release data and no control right over a partner's calendar, so
**data rights, channel conflict and commercial control are unscored by every run in this package** (`../os_only_and_virtual_network.md` section
3.2). And a record-generating software product is a liability here rather than an asset: FDA applied 21 CFR 211.22(c) to AI-generated GMP records
in Warning Letter 320-26-58 (F2-S52), so an OS that writes records transfers inspection exposure to the customer.

## 5. Regulatory exposure

Both designs are mapped to **G01 to G07** (application ownership or a binding CMO relationship; site in the approved application with registration
and listing; product, process and cleaning validation; aseptic processing or terminal sterilization validated; analytical methods transferred;
stability and container-closure support; change-control category identified) and to **G13 and G14**, because both replicate manufacture of one
product across two or more sites. G08 to G12 do not apply, because neither uses a 503B responder site; G15 does not apply, because both run release
scenario R0 and claim no release-assurance component; G16 reaches S9, S18 and S19, not these two (`config/regulatory_gates.yaml`, R006 and R007).

Hardest on day one is **G07**, the reporting category. S11's entire cost advantage rests on adding a labeling and secondary-packaging site being
the minor change FDA's 2004 guidance describes for a site with a satisfactory CGMP inspection for that operation (F5-S14); the pre-declared test
says that if the category is CBE-30 or a prior approval supplement, the design collapses to frozen S3 with a longer lead
(`../falsification_register.csv` data row 11). The same question reaches S16's contracted fill sites, where the carve-out gives CBE-30 only for a
move into an aseptic area already making similar approved products in the same container type with a satisfactory inspection (F3-S44, F3-S45).
**G02** carries the GDUFA III clock: six months for a standard supplement without a preapproval inspection, ten with, and a facility not in the
original application defaults to the inspection path (F9-S11, F9-S12). **G03 and G04** are per line and per product, with media fills at
qualification, after significant modification and twice yearly per line per shift (F7-S12, F7-S13, F6-S11). Batch disposition is non-delegable
under 21 CFR 211.22(a), an extramural facility is an extension of the manufacturer under 21 CFR 200.10(b), and a quality agreement cannot delegate
CGMP responsibility (F3-S41, F3-S42, F3-S43), so both designs declare one quality unit spanning their sites as a shared common-cause group.

All of it **stays UNCERTAIN until HA-31 assigns a status with a name, a date and a rationale**, reviewed against HA-23. As of the report auto-built
2026-09-04, 0 of 16 gates are reviewed and the definition-of-finished list stands at 9 of 22 (`../../reports/rendered/results_report.md`, DF08).
G13's basis is a proposed rule (FR doc 2026-14073) whose own note says the base case must not depend on it becoming final.

## 6. Capital requirement

**This package cannot state a capital requirement, and its only basis is a tier-5 illustrative parameter: `product.capital_usd_per_site`, swept
15,000,000 to 100,000,000 USD per site with no feasibility crossing in any of its 40 cells, because the feasibility predicate is service only** (480 is the
whole threshold grid, which contains 138 crossings; `../feasibility_regions.md` sections 2.3 and 7).
Modelled annual network cost at the optimized designs is 16,475,242 USD/yr for S16 on sodium bicarbonate and 15,890,651 on norepinephrine
(`../inventory_capacity_hybrids.md` section 3.1), with S11 at 15.71M and 14.86M in the dominance evaluation. Neither is Telo's capital nor a
Telo-only cost: both ledgers carry the incumbent plant's capital (MD-14 residual); contracted lines carry no capital even though a reservation fee
excludes tech transfer, development and lot release testing (F7-S04); there is no CDMO margin; the opening position is unbilled (NEW-1).

External anchors, none of them a Telo number: 25M USD for a line inside an existing plant (F1-S53); 132M USD for a new line and building (F1-S51);
about 30M USD for four commercial aseptic fill lines in a distressed sale (LCDM-S10); 25M USD for a validated 503B expansion (L503B-S19);
California's estimate of 100M to 300M initial plus 20M to 50M annually, after which the state declined to build (F13-S18, F13-S19).

## 7. Milestones

| When | Milestone | Evidence it was reached |
|---|---|---|
| 6 mo | The defects that carry this result are closed and the battery is re-run: NEW-1 (charge opening inventory), NEW-2 (allocation), NEW-3 and MD-23 (readiness decay), MD-1 (material buffer coupled to lead time), MD-3 (regional review rule), MD-12 (matched search spaces), MD-24 (take-or-pay with a service channel), and extending `_commissioning_window_loss` to reserved sites so S16's 540-day qualification lead stops reading 0.0000 | run manifests under `../../results/manifests/`, and a dominance table showing whether S11 and S16 keep the frontier once opening stock is charged and the comparators search the same inventory space |
| 6 mo | The three inputs that decide the regions leave tier 5, and gate review begins | parameter records for demand, capacity and price carrying a dated source at tier 4 or better (HA-11, HA-13, HA-21, HA-24), `make status` counting the illustrative total down from 87 of 91, and DF08 off 0 of 16 with a named reviewer and date on each row (HA-31, HA-23) |
| 12 mo | A purchaser commits volume | a signed term sheet stating price, term, committed units, activation condition, allocation rights and the failure-to-supply remedy (HA-36); `ContractTerms.missing()` returns empty for the first time |
| 12 mo | A registered US line commits campaign slots, and for S11 agrees to sell bright stock to a third-party labeler | an executed supply agreement and quality agreement; the pre-declared falsifier is two of three CDMOs declining (`../falsification_register.csv` data row 10) |
| 12 mo | The G07 category is determined in writing for this presentation | a written regulatory assessment naming the category and the expected elapsed days (data row 11) |
| 24 mo | First commercial batch made at a contracted registered line under the application and disposed by Telo's quality unit | the batch record, the disposition record and the establishment listing naming the site. Comparators say this is optimistic: Civica Petersburg took more than 1,600 days with pre-committed demand and 140M USD and was still pending approval (F13-S41, F13-S27, F13-S28); a 110,000 sq ft registered plant bought in February 2022 was still recorded as not yet inspected 4.2 years later (L503B-S01, L503B-S21) |
| 60 mo | Committed volume covers fixed and resilience cost | delivered units against committed units. The model asks for 0.887 (sodium bicarbonate) and 0.902 (norepinephrine) of realized annual demand for S16 at its own break-even price (`../inventory_capacity_hybrids.md` section 4), or 0.845 (norepinephrine) and 0.632 (sodium bicarbonate) for S16 and 0.798 and 0.599 in the same order for S11 at an assumed 18.00 USD per unit. Purchase orders are the evidence; model output is not |

## 8. Hiring, by the milestone each role gates

1. **A named head of quality with disposition authority.** Gates the 24-month batch and every contracted-site release (21 CFR 211.22(a), F3-S42).
2. **A generic-drug CMC or sterile regulatory professional** (HA-23, HA-31). Gates the 6-month gate review and the 12-month G07 determination;
   without it every gate stays UNCERTAIN and no strategy can receive a favourable decision class.
3. **A commercial contracting lead with GPO or IDN access** (HA-24, HA-33, HA-36). Gates the 12-month term sheet, and so the architecture, which is
   recorded today as not contractable, stated.
4. **A sterile manufacturing or process engineer** (HA-21). Gates campaign size, changeover and capacity evidence; S11 loses the target on sodium
   bicarbonate at 3.39 days of changeover against a 3-day base, the tightest changeover condition in the grid.
5. **A modeller** to close NEW-1 to NEW-3 and MD-1, MD-3, MD-12, MD-23, MD-24. Gates the 6-month re-run and needs no counterparty.

None of these people exists in this package, and no interview or review has occurred.

## 9. Partnership dependencies

| Partner | What they must agree to | What the evidence says |
|---|---|---|
| Application holder, or the seller of an ANDA | naming each contracted line in the application and carrying the change-control filing (G01, G02, G07) | landscape open question 3 asks whether any US CDMO currently makes a shortage-list drug under a third party's ANDA; nothing found answers it |
| Registered US aseptic fill line | campaign slots, an activation lead, an exercise cadence, take-or-pay, and priority when Telo calls | the one disclosed US CDMO capacity agreement runs the other way, with annual committed capacity obligations on the CDMO and no minimum purchase obligation on the customer (LCDM-S14); industry refused co-tenancy at CIADM for fear of displacement (F7-S01, F3-S19); merchant US aseptic capacity is going captive (LCDM-S1, LCDM-S9, LCDM-S10) |
| For S11 only: a CDMO selling filled, capped, cap-coded unlabeled units, plus a labeling and secondary-packaging site | bright-stock supply to a third-party labeler, at a site with a satisfactory CGMP inspection for that operation | no CDMO is known to sell bright stock to a third-party labeler for US shortage generics (F5 section 9); late labeling itself is codified since 1978 (F5-S08) and sold as a service (F5-S46, F5-S47) |
| Purchaser, and every contracted site | multi-year committed volume with a failure-to-supply remedy; a quality agreement that does not delegate CGMP responsibility, with acceptance of Telo's disposition | such programmes exist and their terms are private in every source read (LSIM-S18, LSIM-S19, LNPM-S19); FDA's quality-agreements guidance states the delegation is not available (F3-S41) |

## 10. Moat, and why it is weak

The physical shape is occupied. Contracted registered capacity plus a six-month buffer is what Civica operates across 14 manufacturer partners and
77 drugs (F3-S25, LNPM-S03), what Vizient NES Reserve sells across more than 180 NDCs with no up-front investment and no programme fee (LNPM-S19),
and what Premier ProvideGx contracts (LSIM-S19). Reserved third-party capacity paid a standby fee is the most thoroughly implemented sub-idea in
the design space, with published government prices (F3-S3, F7-S04).

Two narrow positions survive prior art, and both are contractual. For S16, coupling reserve depletion below a stated days-of-supply threshold to a
pre-qualified campaign at a named site is `novel_combination (uncertain)`: the halves exist separately and nothing was found linking them (F8-S17,
F8-S32, F8-S09, F8-S44), withdrawn by one GPO, nonprofit or government contract doing it (`../falsification_register.csv` data row 24). For S11,
pairing a pooled unlabeled position with a campaign offtake is `novel_combination`, withdrawn if an operating pooled bright-stock service for US
generic injectables is found.

**The prior-art reason it is not defensible: a GPO can write the same contract.** Three GPOs cover over 90 percent of US hospitals (LSIM-S20),
Vizient serves more than 65 percent of acute-care providers on a 140 billion USD portfolio (LSD-S11), and pruning rule P5 requires a stated reason
Telo beats the named incumbent, which the evidence does not supply. Campaign rotation across prequalified sites is listed as unoccupied (prior art
6.4), but its enabling condition is allocation rights over independent owners' calendars, a Sherman Act question before it is a product (F2-S63).

## 11. Channel conflict

Three, none priced anywhere in this package. **With the buyer's own programmes.** Selling through a GPO means competing on the criterion the
channel optimizes, price (LSIM-S20); selling around it means selling against Vizient's buffer offer, which carries no programme fee (LNPM-S19).
**With the contracted line.** The priority call that makes a reserved slot worth anything displaces the partner's other customers, which is what
industry refused at CIADM and what BARDA's own RFI names as a deterrent (F7-S01, F3-S19); allocation rights are inert in the engine (NEW-2), so
every service number here is computed as if that conflict did not exist. **With the application holder.** A Telo label over a partner's application
competes with the partner's own, which is the Civica shape (F3-S23, F3-S25), and consolidation has already removed counterparties: the largest 503B
bought its shortage-analytics vendor and a GPO took equity in a manufacturer with offtake attached (LSD-S15, LSIM-S18).

## 12. Failure conditions, as observable events

1. **HA-11 returns a demand denominator above the architecture's ceiling.** Ceilings, at n = 20 with a binomial standard error near 0.067 on
   `p_meet`: S11 1,089,063 units/yr (norepinephrine) and 1,190,625 (sodium bicarbonate); S16 926,563 and 1,246,875, three of the four inside noise
   (`../product_architecture_matching.md` section 3.4). At twice base demand none of the twenty meets the target in any of the 18 cells.
2. **No purchaser signs at or above the break-even price.** S16's break-even is 13.18 USD per unit (sodium bicarbonate) and 16.94 (norepinephrine)
   (`../inventory_capacity_hybrids.md` section 4); USP reports 74 percent of sterile injectables in shortage priced below 15 USD per unit and 44
   percent below 5, n = 61 (F12-S14).
3. **Two of three CDMOs decline bright stock, or G07 comes back CBE-30 or a prior approval supplement**, either of which removes S11
   (`../falsification_register.csv` data rows 10 and 11); or **a contract is found coupling reserve depletion to a campaign trigger**, which
   withdraws S16's novelty claim (data row 24). The architecture may still be right in that case; the position is not.
4. **The re-run with opening inventory charged and matched search spaces removes the frontier position**, which is partly visible already, since
   matched-space S4 meets the target on both products (`../feasibility_regions.md` section 8).
5. **A margin disappears on a single input.** S11 loses the target on sodium bicarbonate 0.31 days above the 14-day sterility base and at 3.39 days
   of changeover against a 3-day base; S16 loses it at 22.73 days of activation latency against a 21-day base (same file, sections 2.2 and 2.3).
6. **A contracted line enters enforcement**, since compliance state persists across inspection cycles and survives changes of ownership (LCDM-S2,
   LCDM-S7, LSIM-S5), or **the presentation leaves the FDA shortage list**, which ends any 503B bridge (L503B-S03). Note that the CMS essential-medicines
   buffer payment runs the other way: it excludes medicines already in shortage, so it is unavailable while the presentation is listed and only becomes
   reachable once the presentation leaves the list, and then only for hospitals of 100 beds or fewer that are not part of a chain (LSD-S3).
7. **The commissioning metric is extended to reserved sites and S16 stops reading 0.0000 window loss.** Its two contracted lines carry
   `commissioning_days` 540, 29.57% of the measured window (`../os_only_and_virtual_network.md` section 3.2; `../inventory_capacity_hybrids.md` section 2
   item 5). One of the four measurements that chose this pair then applies to S11 only.

## 13. Evidence required before advancing past the first gate

| Evidence | Id |
|---|---|
| Founder sign-off on the frozen thresholds (fill 0.99, q 0.90) before any result is used for a decision; whether furosemide joins the longlist and at which fill volume, with its primary-source shortage check; commit authorization | HA-02, HA-03, HA-18, HA-05 |
| Make the public repository private, then decide history remediation for the exposed contact files (29 people with addresses in one file, up to 18 more in another) and adopt the prevention controls | HA-06, HA-07, HA-08 |
| Utilization per presentation, national and regional | HA-11 |
| Node and reserved-capacity cost, reservation-fee scope, minimum campaign size; batch size, campaign, changeover, startup after deviation | HA-13, HA-21 |
| Supplier quotes; contract-laboratory release-testing prices; ASHP bulletins for shortage duration | HA-12, HA-14, HA-10 |
| Sterilization route per presentation | HA-34 |
| Contract terms from a person with authority (volume, term, price, failure-to-supply remedy), and whether any purchaser will fund standing availability separately from units shipped; assume no until one says otherwise | HA-36, HA-24, HA-33, HA-38 (queue rank 15 asks the availability question directly, with the standing fallback "assume no until a purchaser says otherwise"; proposed in `../inventory_capacity_hybrids.md` section 6) |
| Replenishment review policy and order-up-to level at real regional stocking points, which decides 8 of 16 Phase A cells | HA-40, reviewed by HA-33 (queue rank 6; HA-20 is the source pool) |
| Gate statuses with reviewer names and dates, including the G07 category; independent review of process and cost assumptions | HA-31, HA-23, HA-30 |

The in-model prerequisites carry no human-action id and block quotation of every number above: NEW-1, NEW-2, NEW-3, MD-1, MD-3, MD-12, MD-23,
MD-24 (`../novel_architectures.md` section 5; `../bottleneck_decomposition.md` section 7).

## 14. What this roadmap cannot answer with the current package

- **Price.** No published rate card, minimum order value, reservation fee or per-unit price exists in 313 landscape sources; the only two public
  prices are a QMS subscription and an individual shortage-data subscription (LQBR-S14, LSD-S7). Every commercial threshold here is a break-even
  derived from tier-5 costs.
- **Which of S11 and S16 is better**, since they sit inside the same evidence and the defects that would decide it are open in both directions; and
  **whether the postponement mechanism has any content**, since MD-15 leaves the pooling benefit nothing to act on and the control was never run.
- **Portfolio economics.** The pooling threshold is explicit and untestable here: 5.08 comparable presentations per node for sodium bicarbonate,
  4.82 for norepinephrine (`../bottleneck_decomposition.md` section 8, a pre-R004 run and superseded for quantitative use).
- **How much of S16's qualification lead the model charges.** `_commissioning_window_loss` excludes reserved sites, so S16 reports 0.000000 window
  loss while both its contracted lines carry `commissioning_days` 540, 29.57% of the measured window (`../os_only_and_virtual_network.md` section 3.2;
  `../inventory_capacity_hybrids.md` section 2 item 5). Until that metric is extended, the commissioning comparison in section 0 holds for S11 only.
- **Whether S16's norepinephrine tail verdict survives more runs.** It sits at `p_meet` exactly 0.90 on 40 paired runs, one binomial standard error
  (0.047) from failing the requirement (`ds_post_R008/dominance.csv`).
- **Capital, working capital, CDMO margin and a purchased-finished-goods price**, none of which has a channel in the engine; data rights, channel
  conflict and commercial control; and whether exercising a line keeps it ready, blocked on NEW-3 and MD-23.
- **Whether Telo beats Civica, Vizient or Premier.** No evidenced reason exists, and P5 requires one. Every regulatory category is open as well:
  all sixteen gates are UNCERTAIN and 0 of 16 reviewed.
