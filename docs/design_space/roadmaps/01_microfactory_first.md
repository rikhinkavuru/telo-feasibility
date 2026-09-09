# Roadmap candidate 1: current microfactory-first

Assignment Phase F, deliverable 20, candidate 1 of 4. Prepared 2026-09-05.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result below is behaviour of the engine under evidence tier 5 (illustrative) inputs, not a statement about the world.
All sixteen gates in `config/regulatory_gates.yaml` (G01 to G16) are UNCERTAIN with no reviewer and no date; UNCERTAIN is never PASS, so no strategy receives a favorable decision class.
Nothing here is legal or regulatory advice. 503B is a time-varying state, never a durable pathway. No interview, partner, customer, purchaser, review or regulatory opinion is asserted,
because none has occurred. Nominally separate sites are not assumed independent.

## Opening: the honest position of this roadmap

This is the roadmap for the architecture the package's own evidence rejects most clearly. It is written because a founder committed to that path needs it written, not because the evidence
supports it. Prior art puts owned distributed microplants on the list of shapes that do not survive: occupied in pilot and failed in every funded federal analogue (`prior_art_review.md`
section 6, closing paragraph). The pilot is On Demand Pharmaceuticals with Germfree at North Mississippi Health Services, about 12,000 prefilled syringes in six months from December 2023
under 503A, absent from FDA's outsourcing-facility table as of 8/28/2026 (F1-S40, F1-S43, F1-S16). The analogues are CIADM, where a 2018 joint review found two of three sites with none of
their capacity used and the third at 7 percent, terminated November 2021 (F7-S01, F3-S7); FFMN, whose outcome is unknown because no retrospective exists (F7-S02); and UK VMIC, about GBP 200M
for a facility that never opened its doors (F3-S59, F7-S24). The one novelty-matrix row describing this exact architecture is `uncertain`, regulated in proposal only, with no operating
instance anywhere (F1-S01, F1-S21, F1-S28).

The model agrees, on a mechanism rather than a score. At the frozen target (mean fill at or above 0.99, tail probability at or above 0.90) the optimizer returns `optimal` for none of the
eight frozen comparators on either product, zero of sixteen cells (`opt_20260903T220534Z`; `feasibility_regions.md` section 4). S5 and S6 are the worst: closest fill 0.865052 on sodium
bicarbonate and 0.980253 on norepinephrine, dominated by 16 and 17 other strategies on both products (`os_only_and_virtual_network.md` section 3.2). S6 is numerically identical to S5 on
service because `release_time_factor` is inert in the stochastic engine (MD-18), and costs 2,256,966 USD/yr more per product for that identity (`sim_post_R008/summary.json`). The
fair-comparison check found the comparators searched over a narrower inventory space than the design-space strategies (MD-12), and added central capacity S4 becomes `optimal` on both
products once searched over the same space, at 20.0M and 23.7M USD/yr against 37.8M and 38.6M; the distributed nodes are the group it does not rescue, norepinephrine S5 reaching 0.9950 and
0.85 and still missing, sodium bicarbonate S5 costing more rather than less (`feasibility_regions.md` section 8, `matched_20260905`). The failure is not exotic: switch capacity shortfall and
commissioning delay off by hand and sodium bicarbonate S5 moves from fill 0.866856 with `p_meet` 0.00 to 0.997499 with 0.983 at 50,768,486 USD/yr, while S16 reaches 0.999999 at 17,383,193
USD/yr in the same arm (`abl_post_R008_pairs/summary.json`). It is broken by having to build the capacity, and it is still about three times as expensive after that is removed by hand.

## What would have to be true for it to work

1. **The presentation is capacity-short in the world, not only in the scaffold.** The capacity mode exists in the model only for sodium bicarbonate, `status_quo_utilization` 1.245 against
   norepinephrine's 0.778, from three tier-5 numbers (NF-3); the leave-one-out fill delta for capacity is +0.05138 against +0.00039 (`product_architecture_matching.md` section 3.3). HA-11,
   HA-13.
2. **Building is not the disqualifier.** S5 and S6 lose 0.287211 of the measured window to commissioning, 524.4 capacity-weighted days of 1826, against 0.000 to 0.090 for contracted designs,
   and sweeping `node_commissioning_days` over 365 to 1095 days returns `infeasible_everywhere` for S2, S4, S5, S6 and S7 on both products (`os_only_and_virtual_network.md` section 3.2). The
   founder needs a clock that range does not contain.
3. **Node capital falls far enough to change the ledger.** Fixed and resilience cost is 81.0% to 93.7% of annual cost across the eight comparators
   (`results/design_space/contract_conditions_sim_post_R008.csv`, `fixed_share_of_cost`), and removing capital cuts cost per delivered unit by 46.8% to 55.5%
   (`bottleneck_decomposition.md` section 6.15, the `loo:capital_cost` ablation; that section's runs are pre-R004 and superseded for quantitative use). NF-7's own
   81% to 95% is computed on the pre-R004 run `sim_20260902T043039Z` and is superseded for quantitative use. S5's break-even
   is 40.5821 USD per unit and S6's 42.6666 (`os_only_and_virtual_network.md` section 4), against USP's 74% of shortage sterile injectables priced below 15 USD per unit and 44% below 5, n =
   61 (F12-S14), and the repository's own norepinephrine price of 1.47 USD Big4 and 4.52 USD FSS (NF-7).
4. **A purchaser pays for readiness, in writing.** Zero of the 42 Phase B candidates is contractable today (`product_architecture_matching.md` section 3.5), no US health system, GPO or state
   has been found paying a standing reservation fee for sterile generic capacity (F3-S28), and family 7's standing instruction is to assume no until a purchaser says otherwise (F7 section
   9).
5. **Several presentations share the node.** The pooling threshold is 5.08 comparable presentations per node for sodium bicarbonate and 4.82 for norepinephrine, the ratio of S0's to S5's
   fixed quality cost per delivered unit (`bottleneck_decomposition.md` section 8, a pre-R004 run and superseded for quantitative use); California reached the same shape at 20 to 40 products (F13-S18). The engine cannot test it (MD-15, one
   product per network), and sharing fixed quality cost is a cost lever with no feasibility content here: `fixed_qa_labor_per_node` changes the preferred strategy in zero of 27 reversal
   cells per product, with fill and `p_meet` identical to the digit across its three levels (`feasibility_regions.md` section 5).
6. **A registration instrument exists for a fleet.** 21 CFR Part 207 treats units at different locations as separate establishments. The DME proposed rule would allow a hub plus distributed
   units under one quality unit, but it is proposed, requires a single legal entity and excludes contract units (F1-S01, F14-S02, Lrepo-S2), and gate G13's own note says the base case must
   not depend on it becoming final.

## 1. What the company is on day one, and what it is not

It is a regulatory and quality organisation with a product screen, a site plan and no site. It holds or has contracted for an approved application, employs the quality unit that will perform
the non-delegable disposition, and has a validation programme it has not run. It is not a manufacturer: no site is registered and no batch exists. It is not a software company; the protocol
forbids an operating-system effect on release time or capacity, and the perfect-OS ablation is worth at best about three cents per delivered unit against an OS charge of 0.32 to 2.56 USD per
delivered unit at sodium bicarbonate S17, four sites at the declared low of 100,000 and high of 800,000 USD per site-year against 1,249,852 delivered units
(`os_only_and_virtual_network.md` sections 2.1, 3.1). It is not a release-automation company: a fully validated chemical release layer saves zero days while the 14-day
sterility incubation binds (NF-2), and zeroing the whole chemical, endotoxin, environmental-monitoring and QA queue moves mean fill by at most 0.003 (NF-6, computed on the pre-R004 run `abl_20260902_phaseA` and superseded for quantitative use; the post-R008
leave-one-out equivalent for the release queue is +0.00074 on norepinephrine and +0.00033 on sodium bicarbonate, `product_architecture_matching.md` section 3.3).
It is not a 503B business and may
not become one durably: no injectable is on the bulks list (L503B-S02), FDA does not read backorders as clinical need (L503B-S07), and the `StrategyDesign` validator rejects `pathway=503b`
with `durable=true`.

## 2. First product or product class

The evidence names one candidate weakly and cannot yet defend it. **Sodium bicarbonate 8.4% 50 mL** is the only configured presentation both currently in shortage and fully sized: snapshot
S01 (FDA shortage export, 2026-09-02) gives 15 current and 19 total rows over 9.51 years, 19 applications, 12 Orange Book applicants, bulks status `not_included`, aqueous small molecule in a
standard vial, gates PG1 and PG2 PASS (`product_architecture_matching.md` section 3.1). It is the only configured presentation whose modelled utilization exceeds 1.0, the sole condition
under which the capacity mode this architecture addresses exists. Two cautions: 1.245 is a derived tier-5 number; and the two configured product files are near-clones on several axes (WB-26),
so most apparent product discrimination in the runs is not evidence. The EDA-funded End-to-End Commercialization Project, led by Civica with Phlow and Occam, does not
target this presentation: its four named medicines are ketamine, midazolam, norepinephrine and succinylcholine, and no source in this package places sodium
bicarbonate inside a federally funded end-to-end programme (F13-S24).

Ruled out: norepinephrine 1 mg/mL 4 mL has 0 shortage rows in S01 and 23 Orange Book applicants, does not fit the capacity-first archetype on its own text, and the public claim naming it was
retracted internally (C008); acetazolamide fails PG2 as a lyophilized product; sterile water has 1 application and 0 Orange Book applicants but PG8 is UNCERTAIN because diluent volumes are
very large for a micro node. **What would decide it.** Furosemide 10 mg/mL is the most shortage-persistent candidate, 30 current and 33 total rows over 6.40 years, but PG1 is UNCERTAIN
because the fill volume is not fixed, so no batch size, no capacity and no architecture can be sized for it. Four answers settle the choice: real utilization (HA-11), line capacity and batch
size (HA-13, HA-21), sterilization route (HA-34), and substitution difficulty, UNCERTAIN for all six candidates, which decides what a miss costs (HA-35). Furosemide's own inclusion is HA-03,
its status check HA-18.

## 3. First customer and the first measurable value

There is no customer. The package contains no interview, letter, term sheet or commitment, and none may be asserted. A founder would have to construct one named purchaser, a health system,
IDN or GPO, signing a committed volume with a stated price, term, activation condition, allocation rights and failure-to-supply remedy (HA-36; acceptable evidence is a signed term sheet or a
written statement from a person with authority, and marketing material is not acceptable). The first measurable value would be delivered units against that commitment plus the buyer's
avoided shortage-response cost, and this package cannot price the second: its only quantified buyer-side figure is a national aggregate, hospital shortage-management labour rising from 8.6M
hours to 20.2M hours and from 359M to 894M USD (LSD-S11B). What is measurable today runs the other way. At an assumed 18.00 USD per unit several architectures need more than 1.0 of saleable
capacity committed to cover fixed and resilience cost (`feasibility_regions.md` section 3 row 1), and S5 is not among the thirteen strategy-product cells that reach the service target at
all.

## 4. Data-access strategy

| data needed | who holds it | what must be given for it |
|---|---|---|
| Utilization and demand per presentation (HA-11) | hospitals, GPOs, wholesalers | a contracting relationship or paid data agreement; CMS Part B is an outpatient proxy missing inpatient injectables |
| Line capacity, batch size, changeover, media-fill cadence (HA-13, HA-21) | line owners, equipment vendors, process engineers | a purchase process or paid engineering study; no US sterile fill-finish rate card is public |
| API, vial, stopper quotes and lead times (HA-12) | suppliers | qualified purchase intent; an alternate API source must issue a Type II DMF letter of authorisation (G16) |
| Release-time decomposition, deviation rates, validation replication and wrong-release cost (HA-22) | quality, CMC, microbiology, validation professionals | interviews with named roles, logged with qualification and date |
| Sterilization route (HA-34) | ANDA chemistry reviews and inspection reports, neither public | a qualified reviewer's knowledge with date and basis; label scraping is ruled out and returned nothing for furosemide |
| Price, term and remedy (HA-24, HA-36) | GPO, wholesaler, IDN contracting leads | a real commercial conversation, and acceptance that price is not reimbursement and is not inferred from ASP |

Presentation-level shortage duration (ASHP bulletins, HA-10) and the USP chapters behind the release components (HA-17) are copyrighted and paywalled, so both need licences and a manual
retrieval note. The one dataset this architecture generates and owns is its own node process and release data. Its value is cross-site equivalence evidence for gate G14, and the landscape's
reading of that asset is blunt: an evidence method and a filing artefact, not a company, and Veeva or MasterControl can ship equivalence monitoring inside their existing multi-site models
the day the first applicant needs it (`competitive_landscape.md` section 4.4).

## 5. Regulatory exposure

Applying on day one to an owned distributed network: G01 to G07 (approved-CMO block) and G13, G14 (distributed block). G15 attaches only to S6, and R3 cannot be enabled unless G15 is PASS.
G08 to G12 are the 503B block, reachable only through a responder site that may be a bridge and never the architecture. G16 attaches only to designs declaring a second API or container
source. Hard on their face: G03 (product, process and cleaning validation) and G04 (aseptic processing or terminal sterilization validated), both `hard_feasibility`, and G01 (application
ownership or binding CMO relationship, `exclude_if_fail`); each ends the architecture rather than delaying it. Lead-time gates are G02, G07, G13; G06 caps inventory and node economics; G14
carries `no_fleet_claim`, so no fleet-level equivalence or rerouting claim is permitted until it passes.

All stay UNCERTAIN until HA-31 assigns a status with a name, date and rationale; today every `reviewer` and `review_date` field is null. Two are unresolvable by search rather than diligence:
G13 rests on a proposed rule, G14 on an unresolved question, since no FDA framework grants automatic cross-site equivalence. Two further readings bear directly on this architecture and stay
UNCERTAIN: whether an approved parametric release programme can extend to a second site or autoclave, given that FDA's generic-drug sterility FAQ ties the abbreviated route to the identical
facility, autoclave, container-closure, parameters and load patterns (F11-S46), and whether a spoke can operate with no resident quality-unit staff under a hub quality unit (Lrepo-S2,
Lreg-S6).

## 6. Capital requirement, and its basis

**The only basis in this package is a tier-5 illustrative parameter.** The parameter id is `product.capital_usd_per_site`: base 40,000,000 USD, low 15,000,000, high 100,000,000,
`evidence_tier: 5`, `confidence: low`, `validation_status: illustrative`, `source_locator "06_Product_A!B19:D19"` (sodium bicarbonate) and `"07_Product_B!B19:D19"` (norepinephrine), noted
"Not scaled by node size in the workbook (WB-04)". S5 declares `sites: 4` (`config/strategies/illustrative_baseline.yaml`) and the run reports five owned sites
(`os_only_and_virtual_network.md` section 3.2), so four declared nodes at the tier-5 base would be 160,000,000 USD of node capital while the run charges five owned
sites. That 160,000,000 appears in no results artifact; the only capital figure the engine produces is `ledger_capital_annualized`, 23,115,997 USD/yr for S5 against
S0's 6,703,202 (`results/simulation/sim_post_R008/summary.json`). It is arithmetic over an illustrative parameter, not a costed plan, and because
capital is not scaled by node size every S5 and S6 cost figure in this package is an upper bound of unknown tightness. Two constraints on using it: sweeping `capital_usd_per_site` from 15M
to 100M produces no feasibility crossing in any of the 40 cells, because the predicate is service only (`feasibility_regions.md` section 2.3); and the ledger is dominated by fixed cost, 81.0% to 93.7% of annual cost post-R008
(`results/design_space/contract_conditions_sim_post_R008.csv`; NF-7's own 81% to 95% is pre-R004 and superseded for quantitative use).

External anchors, none of them a Telo estimate: Civica Petersburg at 140M USD for one plant that had not begun commercial manufacture as of the last confirmed public statement (F13-S41,
LNPM-S07); California HCAI's 100M to 300M USD initially plus 20M to 50M annually (F13-S18); single-site builds at 132M (Jubilant, LCDM-S6), 100M (GRAM, LCDM-S5) and 200M (Curia, LCDM-S8).
CONTINUUS's own board is the sentence a founder must answer: "We've tried applying this model to generics, and it just doesn't work at their price points" (F1-S45, F1-S59, F1-S46).

## 7. Milestones

| horizon | milestone | evidence that it was reached |
|---|---|---|
| 6 mo | Gates reviewed rather than left UNCERTAIN by default: a qualified generic-drug/CMC professional assigns a status to G01 to G07, G13, G14 | those rows in `config/regulatory_gates.yaml` carry a non-null `reviewer` and `review_date` with a rationale (HA-31, HA-23); today all are null |
| 6 mo | Product locked on real features; public surfaces corrected and the exposure closed | `product_features.csv` `sterilization_route` non-empty (HA-34); HA-03, HA-18, HA-11 closed; `CLAIMS_REGISTER.csv` C001 to C025 updated; HA-04, HA-06, HA-07, HA-08 done with dates |
| 12 mo | Capital and cost leave tier 5 | the `capital_usd_per_site`, `fixed_qa_labor_usd_per_site_year` and variable-materials records carry an evidence tier below 5 with a named source (HA-12, HA-13, HA-14) |
| 12 mo | One purchaser signed, and the application route settled | `ContractTerms.missing()` empty and `contracting.minimum_contracted_utilization` below 1.0 at the signed price (HA-36, HA-24); an executed quality and technical agreement with an ANDA holder, or an ANDA of the company's own, meeting G01 |
| 24 mo | First node registered and inspected, first released commercial batch | an establishment registration under 21 CFR Part 207; an FDA inspection classification; the site named in the application under the reporting category a reviewer assigned (G02, G07); a batch disposition record signed by the quality unit with PPQ and media-fill reports closing G03 and G04 |
| 60 mo | Nodes two and three at the pooling threshold, and the network covers its fixed cost | at least about 5 comparable presentations per node (`bottleneck_decomposition.md` section 8), each with its own process validation and media fills; a contract row whose required committed share is below 1.0 at the signed price; network fixed quality cost per delivered unit at or below the incumbent's |

The 24-month row is faster than every documented US analogue here and the founder should say so out loud. Leiters bought a 110,000 sq ft plant in February 2022, registered it in July 2022,
and FDA still recorded it as not yet inspected 4.2 years later (L503B-S01, L503B-S21). Civica Petersburg ran more than 1,600 days with 140M USD and pre-committed hospital demand and was
still pending FDA approval on its 2025 fact sheet (F13-S41, F1-S57). The fastest case anywhere is White Raven at 18 months to GMP certification on a purchased SA25 workcell, in Europe, for a
startup CDMO, which is not a US ANDA (LAMD-S15); purchase-to-GMP for the fill hardware alone is 12 to 15 months for an SA25 (LAMD-S14).

## 8. Hiring: the roles that gate the next milestone

1. **Generic-drug CMC or 503B regulatory professional** (HA-23, HA-31). Gates every milestone, because no gate leaves UNCERTAIN without a named reviewer and no favorable decision class
   exists until one does. Nothing substitutes.
2. **Head of quality who will own disposition.** 21 CFR 211.22(a) and FDA's 2016 quality agreements guidance make disposition non-delegable and state that quality agreements cannot delegate
   statutory responsibilities (F3-S41, F3-S42, F3-S43). Gates G03, G04 and the registration.
3. **Sterile process and validation engineers** (HA-21). Gate batch size, changeover, media-fill cadence and node capital, the 12-month milestone's inputs.
4. **Microbiology and environmental-monitoring lead** (HA-22). The 14-day sterility incubation is the argmax of the release set, and an EM review is a mandatory element of the release
   decision whatever the route (F11-S04, F11-S01).
5. **Commercial contracting lead for GPO and IDN** (HA-24, HA-36). The contract gates the capital, not the reverse.

## 9. Partnership dependencies

| partner | what they must agree to | status |
|---|---|---|
| ANDA holder, unless Telo files its own | naming the node in the application, a quality and technical agreement, and that the agreement cannot delegate statutory responsibility | G01, G02, G07 UNCERTAIN; F3-S41 to F3-S43 |
| API supplier and any second source | supply terms; for a second source a Type II DMF letter of authorisation plus identity and suitability testing of the alternate lots | G16 UNCERTAIN; 21 CFR 211.84, 211.94; F9-S12 |
| Vial and stopper suppliers | a qualified container-closure system for the presentation | G06 UNCERTAIN. Every S0 to S7 site draws `api_1`, `vial_1` and `stopper_1`, so four nodes on one supplier set are not four independent sites (`bottleneck_decomposition.md` section 8) |
| Isolator or workcell vendor; contract testing laboratory | delivery and installation qualification; release testing under a quality agreement, which a hub lab serving distributed production may perform | hardware novelty cannot be claimed (F1-S48, F1-S49, F1-S70, F6-S41); 21 CFR 207.1, 211.22; F4-S3, F4-S24 |
| Purchaser (GPO, IDN, health system) | committed volume, price, term, activation condition, allocation rights, default risk, failure-to-supply remedy | none exists; HA-36 open. HHS records that erosion of failure-to-supply clauses in GPO contracts may be associated with drug shortages (F10-S10) |

## 10. Moat, and whether it is defensible

It is not defensible on the evidence in this package. Pruning rule P5 keeps an architecture on the "does not survive" list only with an explicit argument against the cited evidence, quoted
and answered (`architecture_taxonomy.md` section 3), and the package contains none. The **plant** is not a moat: no entrant in owned small-scale sterile capacity is differentiated by the
plant (`competitive_landscape.md` section 2.10), the hardware is bought (F1-S48, F1-S49, F1-S70), and the 2005-priority patent claiming prevalidated modular GMP facilities built near the
approval authority and shipped to the customer is Ceased (F14-S59). The **release layer** is not a moat: PAT and in-line spectroscopic measurement of chemical CQAs is 22-year-old prior art
(F11-S07, F11-S08, F11-S30), multivariate drift detection ships from Sartorius, Aizon, Basetwo and Quartic (F2-S20, F2-S17, F2-S19), and an AI or conformal layer positioned as removing the
sterility hold is classified already refuted rather than novel (F11-S02, F11-S03, F11-S41). The **regulatory position** is what is left: distributed nodes with a validated analytical-release
component for sterile injectables is `novel_combination`, elements existing separately with no source combining them (F1-S69, F1-S62, F1-S05, LR-S01), and the owned DME network is
`uncertain` with no operating instance (F1-S01, F1-S21, F1-S28). Both depend on an instrument that does not exist: the DME rule is proposed, requires a single legal entity and excludes
contract units (F14-S02, Lrepo-S2), and CDER has granted zero advanced-manufacturing-technology designations from five requests with both determinations negative (LAMD-S01). Against that,
the government has funded this exact thesis: EQUIP-A-Pharma with four performers, eight drugs and an explicit goal of a real-time digital regulatory approval framework (LGOV-S12, LAMD-S04),
ODP's modular unit inside a hospital (LGOV-S14), DEKA's point-of-care unit sent to FDA (LGOV-S16) and a BARDA solicitation naming distributed manufacturing systems (LGOV-S23), which the
landscape reads as crowded rather than novel.

## 11. Channel conflict

Three GPOs cover over 90% of US hospitals and often focus on the lowest price as the sole criterion (LSIM-S20); Vizient alone serves more than 65% of US acute care providers on a 140 billion
USD contract portfolio (LSD-S11). Selling outside that channel means selling against it; selling inside it means competing on price, which is what the channel optimises. Both large GPOs
already run committed-volume and buffer programmes and Premier co-invested in Exela with offtake, so a GPO is channel, funder of a competing ANDA and price-setter at once (LNPM-S18,
LNPM-S19, F13-S23). If Telo manufactures under a partner's application the partner is the incumbent supplier of the same presentation, the Civica label-and-NDC-over-Xellia's-ANDA shape
(F4-S18), and allocation rights sit with the partner. A hospital-hosted node puts Telo inside the customer's plant and licence, and the only US pilot of that shape ran under 503A (F1-S40,
F1-S43). If the company also sells software to sterile manufacturers, its software customers are the firms whose lines its plants compete with, and a record-generating product carries
inspection exposure for the customer after Warning Letter 320-26-58 applied 21 CFR 211.22(c) to AI-generated GMP records (F2-S52). None of this is scored anywhere: data rights, channel
conflict and commercial control are not represented in the engine (`os_only_and_virtual_network.md` section 3.2).

## 12. Failure conditions, as observable events

1. A qualified reviewer records FAIL on G01, G03, G04 or G13 in `config/regulatory_gates.yaml` (HA-31).
2. HA-34 returns "aseptically processed" for the chosen presentation. The 14-day sterility hold is then a constant, route conversion is unavailable, and the only intervention in the sweep
   that acts on the binding release constraint is gone (`prior_art_review.md` section 6.1).
3. The DME rule is withdrawn, or finalised with the single-legal-entity and contract-unit exclusions intact, so a fleet cannot register as one establishment (F1-S01, F14-S02).
4. HA-11 returns a real utilization below 1.0, so the capacity mode this architecture exists to solve does not exist (`product_architecture_matching.md` section 3.3); or it returns demand at
   or above the architecture's ceiling, and no strategy of the twenty meets the target in any of the 18 highest-demand reversal cells, at 1,800,000 and 2,400,000 units per year
   (`feasibility_regions.md` section 5).
5. HA-13 returns a node capital quote at or above the 100,000,000 USD high bound, or a date putting first released batch beyond the 730-day base commissioning; or HA-36 returns no signed
   committed volume, or a price at which the required committed share exceeds 1.0 of saleable capacity (`contracting.minimum_contracted_utilization`).
6. A Form 483 or warning letter at the first node. PharMEDium is the documented case of replicated aseptic-quality failure across sites under one quality organisation, ending in a consent
   decree and closure five years after a 2.6 billion USD purchase (F4-S7, F4-S8, F4-S9). Teligent is the closest analogue to a Telo-scale line in the collected material, where site
   compliance rather than line capacity decided whether any product could launch (F6-S35).
7. The presentation leaves the FDA shortage list while a 503B bridge is still load-bearing; sodium bicarbonate's modelled eligible window is 1,222.6 of 1,826 days and the copy rule ends the
   line when the listing ends (`product_architecture_matching.md` section 3.2; L503B-S03). Or a competing federally funded consortium reaches the same presentation first. The EDA-funded Civica/Phlow/Occam project names ketamine, midazolam,
   norepinephrine and succinylcholine rather than sodium bicarbonate, so this is a general condition and not one this package evidences for the chosen presentation (F13-S24).

## 13. Evidence required before advancing past the first gate

| evidence | human action |
|---|---|
| Status, with name and date, for G01 to G07, G13, G14 on the chosen presentation | HA-31, HA-23 |
| Sterilization route, from an ANDA chemistry review, an inspection report naming the cycle, or a named reviewer | HA-34 |
| Utilization and demand denominator per presentation; node capital and qualification from a vendor estimate; line capacity, batch rate, changeover | HA-11, HA-13, HA-21 |
| Supplier quotes and lead times for API, vials, stoppers, seals, labels, packaging; contract laboratory price list | HA-12, HA-14 |
| Release-time decomposition, deviation rates, validation replication cost, a sourced wrong-release cost | HA-22 |
| Committed volume, price, term and remedy from a person with authority | HA-36, HA-24, HA-20 |
| Substitution difficulty per presentation, which decides what a miss costs; furosemide's role and a primary-source shortage check | HA-35, HA-03, HA-18 |
| Primary text of the DME proposed rule and its docket; USP chapter text behind the release components | HA-15, HA-17 |
| Founder sign-off on the frozen thresholds before any result is read as a decision; independent reviews of process and cost, gates, model structure, demand and contracts | HA-02, HA-30, HA-31, HA-32, HA-33 |
| Public-claim corrections and the privacy remediation, which gate any external use of this work | HA-04, HA-06, HA-07, HA-08 |

## 14. What this roadmap cannot answer with the current package

- **Whether owned nodes are ever feasible.** Every input behind every number here is tier 5, marked `illustrative` with `confidence: low` (`feasibility_regions.md` section 7). The regions
  locate the model, not the world.
- **Whether four nodes are more independent than one plant.** Every S0 to S7 topology shares at least one common-cause group and one supplier set (`architecture_taxonomy.md` section 2 item
  14).
- **What a node actually costs, and whether a portfolio rescues it.** Capital and fixed cost are not scaled by node size (WB-04), so each smaller node carries a full central-plant capital
  and fixed cost and every S5 and S6 cost figure is an upper bound. MD-15 runs one product per network, changeover and cleaning validation are absent, and the 5-presentation pooling
  threshold is an arithmetic ratio rather than a simulated result.
- **Whether distribution helps at all.** The engine splits national demand across four regions by a fixed rule and PG5 is UNCERTAIN for all six candidates, so the geographic case for
  distribution is an artifact of that split (`product_architecture_matching.md` section 3.5).
- **Whether route conversion is available, and how the commercial axes score.** There is no sterilization-route attribute and no parametric release scenario in the engine, and data rights,
  channel conflict and commercial control are not represented in either direction (`architecture_taxonomy.md` section 1 family 11).
- **Whether the comparison is fair in both directions.** The matched-space check ran four strategies at 40 final runs, and the symmetric test has not been run (`feasibility_regions.md`
  section 8).
- **Whether anyone will pay for readiness.** No purchaser evidence exists anywhere in the package (F3-S28; `prior_art_review.md` section 7 items 17 and 18).
