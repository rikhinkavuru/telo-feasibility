# Roadmap candidate 2: OS-first, manufacturer later

Assignment Phase F, deliverable 20, candidate 2 of four. Prepared 2026-09-05.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input behind every model result quoted here is evidence tier 5 (illustrative), so those results are the behaviour of a model under those inputs and not statements about sterile-injectable manufacturing in the world. All sixteen regulatory gates in `config/regulatory_gates.yaml` (G01 to G16, G16 added under revision R007) carry status UNCERTAIN with no reviewer and no review date; UNCERTAIN is never PASS, and no strategy here receives a favorable decision class. Nothing here is legal or regulatory advice. No interview, customer, partner, reviewer or regulatory opinion is asserted; none has occurred. 503B appears nowhere in this roadmap as a durable pathway. Where the package has no basis for a number, this file says so rather than supplying one.

## 0. The verdict first: this is a bridge, not a destination

Two independent readings in this package say the same thing about a manufacturing operating system.

The prior-art review puts "the manufacturing OS in any of its eight sub-forms" on its does-not-survive list (`prior_art_review.md` section 6, closing paragraph). Six of the eight are `already_implemented` in its novelty matrix: the eBR and MES wedge (F2-S01, F2-S05, F2-S04, F2-S07, F2-S12, F2-S09, F2-S13, F2-S71); deviation and CAPA orchestration and QMS workflow (F2-S15, F2-S16, F2-S23, F2-S24, F2-S25, F2-S29); sensor interoperability and data lineage (F2-S21, F2-S22, F2-S17, F2-S26); multivariate drift monitoring, whose falsifier the matrix records as "nothing; it exists" (F2-S20, F2-S17, F2-S19, F2-S18); cross-site process intelligence within one owner (F2-S14, F2-S09, F2-S71); and hospital and GPO shortage-response coordination (F2-S33, F2-S35, F2-S37, F2-S38, F2-S43, F2-S44). Emerson already ships the furthest an OS goes toward release, immediate release once exceptions close (LPMS-S03, LPMS-S26).

The engine finds the levers non-binding. Phase A puts deviation and rejection in the "measured but not binding" set (`architecture_taxonomy.md` section 1 preamble), and the perfect-OS ablation in `results/ablation/abl_post_R008/attribution.csv` (n = 60, 40 cells) moves mean fill by +0.001771 on average and +0.008638 at its best cell, flips 3 of 40 feasibility verdicts, all three from inside 1.3 binomial standard errors of the requirement, and costs 4.9x to 33.9x its own operational saving at the declared OS prices (`os_only_and_virtual_network.md` section 3.1). That ablation zeroes deviations, rejections and yield variance together, so it is an upper bound on an upper bound.

So this roadmap is written as a bridge. **What the bridge carries:** cash from a narrow measurement product; the buyer relationships and the plant data the manufacturing questions need (HA-11, HA-13, HA-20 to HA-25); and a corrected public record. **Where it lands:** the contracted-campaign-plus-positioned-inventory shape the synthesis names strongest, carried by S11 and S16 (roadmap 4), of which roadmap 3's S16 is one form; these are the designs that clear the frozen target under illustrative inputs (`os_only_and_virtual_network.md` section 3.2; `strategic_synthesis.md` section 5). **What it is not:** a claim that software revenue funds a plant, which nothing in this package models. **When to stop:** the observable events in section 12. A bridge with no landing is a software company, and this package cannot say whether that is a good one, because the engine has no revenue side at all (`os_only_and_virtual_network.md` section 2.1).

## 1. What the company is on day one and what it is not

It is a measurement and decision-support vendor. It sells one function, stop-the-line drift detection with a distribution-free limit on the industry's own statistic, plus the hold-decision workflow around it (`release_assurance_followup.md` section 4, items 2 and 3). It owns no site, holds no application, and makes no disposition.

It is not any of the following, each with its reason.

- Not a manufacturer, not an ANDA holder, not a quality unit. 21 CFR 211.22(a) puts approve-or-reject authority in the customer's own quality control unit (LPMS-S20).
- Not release automation. `CLAIMS_REGISTER.csv` C010 records "Telo automates the release decision" and "certifies pharmaceutical batches in real time" as contradicted, and the claim-discipline table in `protocol/protocol.yaml` forbids "Our AI automates release".
- Not "the operating system for sterile drug manufacturing". C015 is contradicted by the company's own deck brief (`funding/deck-prompt.md:61`, which instructs: do not call it a manufacturing OS) and unsupported as a description of an existing product. Allowed wording is a stage qualifier or "release-decision support layer" (`public_claims_corrections.md` C015 row).
- Not a shortage intervention on day one. Release-time mechanisms do not limit service for either configured product in this model (candidate NF-6, `results/manifests/nonobvious_finding_candidates.json`).

## 2. First product or product class, with the matching evidence and the reason

The evidence separates two candidates cleanly and picks the second.

**Rejected: release prediction.** Under an instrument change the calibration's coverage falls to 0.41 to 0.77 and the units the gate still releases carry 16 to 61 percent conditional error; the gate's confidence does not rank correctness among released units (E-AURC 0.15 to 0.26 on shift); at alpha 0.10 and the illustrative costs it costs 125,230 to 150,815 USD per batch on the home instrument against 30,082 USD to test every batch, and breaks even only if a wrong release costs under about 0.37 to 0.45 M USD; and the certificate a quality unit needs scales with reference units, needing 199 units for a 1.5 percent bound, 299 for 1.0 percent and 598 for 0.5 percent at delta 0.05 with zero observed losses, against 155 reference tablets in hand (`release_assurance_followup.md` sections 3.1, 3.2, 3.5, 4). For an aseptically filled injectable it also removes about zero days from the hold, because the 14-day sterility incubation is the critical path (test `test_full_release_assurance_saves_no_days_when_sterility_binds`; candidate NF-2).

**Chosen: stop-the-line drift detection, with the mandatory-hold documentation workflow around it.** The PCA Q residual under a conformal limit detects the instrument change completely at a 2 percent false-hold rate on clean batches (run E, tuned threshold 0.04, home abstention 0.02; the threshold is tuned on the family it is scored on, and the Q statistic was itself chosen on the evaluation instrument, which `release_assurance_followup.md` section 2 records as leakage item d2, an unmeasured optimism in the abstention headline), and the same threshold transfers to every harmful synthetic fault (`release_assurance_followup.md` sections 3.4, 4). The incumbent parametric Jackson-Mudholkar limit on the same statistic fires at 18.68 percent at detection 1.000 while claiming 5 percent, against 4.35 percent for the conformal limit at detection 0.990 (`gate_summary.json:detectors`). That gap is the only measured product advantage in the package, and it is measured against one of four stored limits on the same statistic: `Box g*chi2` gives 5.03 percent false alarm at detection 0.9988 and the empirical percentile 6.33 percent at 0.9933, so the advantage is over the Jackson-Mudholkar calibration specifically and not over the class. The workflow half enters the network model as scenario R1, documentation and orchestration benefit only, bounded by `qa_review_days` (base 2 days, tier 5) (`protocol/protocol.yaml`, release_assurance scenarios).

Novelty rests on the limit and on the disposition framing, not on drift monitoring. The monitoring half is `already_implemented` (Sartorius SIMCA-online, LPMS-S13). "Validated model-driven mandatory hold as the disposition mechanism" is `uncertain`, with no vendor found selling one under the FDA AI credibility framework or draft Annex 22 (F2-S57, F2-S48).

What the evidence cannot pick is the buyer segment: generic sterile manufacturer, CDMO, or 503B operator. Section 13 names what would settle it.

## 3. First customer and the first measurable value delivered to them

No customer exists and none may be asserted. `docs/interviews/` holds infrastructure only, and HA-20 to HA-25 are all open. The prior-art falsifier for the crowded wedge names the segment worth testing first: a sterile or 503B segment no listed vendor serves and where Korber's small-site product does not ship (F2-S01). Firms already in enforcement are a second candidate and a poor one, because that buyer is distressed and episodic (competitive landscape 4.5).

The first measurable value is false holds avoided: 4.35 percent at detection 0.990 for the conformal limit against 18.68 percent at detection 1.000 for the parametric one, with `Box g*chi2` on the same statistic at 5.03 percent and detection 0.9988, on the frozen public data (`gate_summary.json:detectors`, quoted in `release_assurance_followup.md` section 4), restated per hundred clean batches on the customer's own lots. The two headline rates are not at matched detection, and the classical limit a buyer is most likely to raise is the Box one rather than the parametric one. It is measurable in shadow mode (scenario R2, predictions and alerts do not control release) without touching a disposition, and it must travel with the full metric set the protocol names, including the risk-coverage curve, false-hold rate, conditional error among released, and uncertainty intervals (`protocol/protocol.yaml` `metrics_that_travel_together`).

The value is not shortage days avoided and must not be sold as such. The perfect-OS ablation's largest single cell saves 5.6241 shortage days per year from a base of 50.527, and its mean fill effect over 40 cells is +0.001771 (`os_only_and_virtual_network.md` section 3.1).

## 4. Data-access strategy

**What the company needs.** Real lots, real drift, real operators and the target chemistry, with instrument, lot, operator and time metadata; the synthetic families and index-block groups in the frozen public data test none of them (`release_assurance_followup.md` section 5). It also needs the two inputs that price the workflow half, the true deviation rate per batch and the investigation duration at node scale, both tier 5 with `source_locator` "study placeholder" (`config/global.yaml`, `deviation_rate_per_batch` 0.005 / 0.02 / 0.08 and `investigation_duration_days` 7 / 21 / 60), and a sourced wrong-release cost to replace `wrong_release_cost_usd` (base 2,000,000 USD, tier 5), whose ratio to the testing cost decides the sign of the cost conclusion.

**Who holds it.** The customer's quality unit and its historian. Data-lineage vendors already sit in that path (AVEVA PI, Scitara DLX, Aizon Unify, Leucine edge connectors, L7 ontology: F2-S21, F2-S22, F2-S17, F2-S26), so access is a negotiation with an incumbent present, not an open field.

**What it must give to get it.** A validatable product the customer can defend to an inspector, and acceptance that records the software writes are GMP records: Warning Letter 320-26-58 applies 21 CFR 211.22(c) to AI-generated GMP records, which `architecture_taxonomy.md` incompatibility 15 states as a liability transferred to the buyer (F2-S52, LPMS-S21). The concrete first ask is shadow-mode access to historical spectral, environmental-monitoring, deviation and lot metadata at one site, for a fixed-fee study, with the disposition untouched and the data rights written down. Data rights are not representable in the engine at all (`os_only_and_virtual_network.md` section 3.2), so they are a contract question this package cannot score.

## 5. Regulatory exposure

**Day one.** None of the sixteen gates attaches to a vendor that owns no site and holds no application. Every gate in `config/regulatory_gates.yaml` maps to manufacturing strategies (G01 to G07, G13 and G14 to owned or contracted sites; G15 to S6 alone; G16 to S9, S18, S19). Day-one regulatory exposure is the customer's, which is the reason the product must stay decision support.

**Hard, meaning no reviewer's opinion relaxes them.** 21 CFR 211.22(a), the disposition stays with the customer's quality unit (LPMS-S20). 21 CFR 211.22(c), machine-written records are GMP records (F2-S52). No analytical or statistical method removes the sterility attribute; only the process route does (`architecture_taxonomy.md` incompatibility 3; F11-S02, F11-S03, F11-S41). EU GMP Annex 17 section 3.10 forbids substituting end-product testing once real-time release testing fails or trends toward failure, so an abstention cannot be filed as a fall-back to the laboratory (`release_assurance_followup.md` section 4, item 1, last bullet).

**Stays UNCERTAIN until a qualified reviewer answers.** G15, release model within a validated state of control with drift handling defined, status UNCERTAIN, reviewer null, legal basis naming FDA's January 2025 AI credibility draft guidance and EU GMP Annex 17 and draft Annex 22. The final status of that guidance and of Annex 22 is HA-16. The acceptable role of a model in a GMP quality system is HA-22. The filing form of abstention and the reading of a model-driven mandatory hold are HA-23, reviewed by HA-31. Until HA-31 assigns a status with a name and a date, every report carries "preliminary regulatory analysis; not legal advice".

## 6. Capital requirement, with its basis

**The package holds no basis for this roadmap's capital requirement, and the number should not be invented.** The engine prices an OS only as a cost a manufacturer pays: `os_integration_usd_per_site_year` (`config/global.yaml:614`), low 100,000, base 300,000, high 800,000 USD per site-year, `evidence_tier: 5`, `validation_status: illustrative`, `source_locator: "study placeholder"`. That is the parameter id, and it is neither Telo's build cost nor a price Telo can charge. In every run in this package it is charged at 0.00, because `os_integration` applies only outside scenario R0 and every design-space strategy is R0 (`os_only_and_virtual_network.md` section 2.1).

The only external anchors are third-party and few: SimplerQMS publishes a 17,500 USD per year floor for 15 users including validation and migration (competitive landscape 2.7, LQBR-S14 to LQBR-S16), and Kneat's FY2025 ARR of CAD 74.1M is the only audited size figure in the category (LPMS-S10). Competitive landscape open question 8 states plainly that no price for what an MES or eQMS costs a two-to-five-person node exists anywhere in its sources. The capital requirement is therefore UNKNOWN here, and it is an elicitation item rather than a search item.

## 7. Milestones at 6, 12, 24 and 60 months

The 24- and 60-month milestones are unmodelled. The engine has no software revenue line, no customer entity, no seat or site count outside Telo's own network, no contract value and no churn (`os_only_and_virtual_network.md` section 2.1).

| Horizon | Milestone | Evidence that it was reached |
|---|---|---|
| 6 months | Public record corrected before any buyer sees it | `CLAIMS_REGISTER.csv` rows C001 to C025 move off contradicted, unsupported and retracted, and the DF22 line in `reports/rendered/results_report.md` shrinks from its current 14 rows; steps in `public_claims_corrections.md` section 4 |
| 6 months | The two in-model OS corrections run | A manifest under `results/` for an OS arm that zeroes only `deviation_rate_per_batch` and `investigation_duration_days`, and a post-R008 one-way sweep of both levers over S0 to S19 (`os_only_and_virtual_network.md` section 6.1, items 5 and 6) |
| 6 months | The buyer question is put to real people | Entries in `docs/interviews/` with role, date and the model field each conversation changed, covering HA-22 and the OS-buyer role, which is now HA-37 at queue rank 29 |
| 12 months | One paid shadow deployment (R2) on real lots at one site | An executed order, plus a metrics file on the customer's own data reporting false-hold rate at fixed detection with bootstrap intervals and the full `metrics_that_travel_together` set |
| 24 months | The tool survives an inspection cycle and a second buyer pays | No inspectional observation attributable to a record the tool wrote, plus a second executed order at a stated annual contract value per site |
| 24 months | Bridge go/no-go decided | Section 12 conditions evaluated against evidence, and section 13 items closed or explicitly abandoned |
| 60 months | Either the contracted-campaign-plus-positioned-inventory architecture carried by S11 and S16 (roadmap 4, of which roadmap 3's S16 is one form) is funded and contracted, or the company has stopped | A named counterparty in the `ContractTerms` fields that are UNANSWERED for every architecture today (`os_only_and_virtual_network.md` section 4.1), and committed utilization at or above that architecture's own threshold in the same section |

## 8. Hiring: the roles that gate the next milestone

- **To the 6-month milestones.** A quality, CMC or microbiology professional who can state the acceptable role of a model in a GMP quality system (the HA-22 role), and a generic-drug regulatory professional for the hold and abstention questions (HA-23, HA-31). These gate the product definition and not only the sale: if a model-driven hold cannot be filed, the chosen product changes.
- **To 12 months.** A computer-system-validation engineer, because the customer inherits validation and record obligations for what the vendor ships, and a field scientist who can stand the method up on someone else's instrument, since the entire measured claim is a claim about behaviour under instrument change.
- **To 24 months.** An inspection-facing quality lead who can sit with a customer during an inspection of records the tool touched.
- **Not hired on this roadmap.** Every manufacturing role. If the bridge lands, those are roadmap 3's hires.

## 9. Partnership dependencies, and what each partner must agree to

| Partner | Must agree to |
|---|---|
| The customer's quality unit | That the tool is decision support and the unit keeps disposition (21 CFR 211.22(a), LPMS-S20); that it owns the records the tool writes and the inspection exposure that follows (F2-S52, taxonomy incompatibility 15) |
| The customer's IT or its data-lineage vendor | Read access to spectral, environmental-monitoring, deviation and lot metadata, with data rights written down; incumbents already occupy this path (F2-S21, F2-S22, F2-S17, F2-S26) |
| The instrument vendor or the site's metrology function | A standardization and transfer procedure, because the measured claim is stated under instrument change |
| A qualified regulatory reviewer | To put a name and a date against the gate readings (HA-31); until then no gate moves off UNCERTAIN |

None of these is agreed. No partnership exists and none may be stated; the package's standing rule is that partners and commitments stay empty until real.

## 10. Moat, and the prior-art reason it is or is not defensible

Weak, and the sources say why.

Against: six of the eight OS sub-forms are `already_implemented` by vendors with more capital and a decade of head start (ids in section 0); Emerson ships automated release once exceptions close (LPMS-S03, LPMS-S26); every adjacent standalone vendor in the shortage and quality-data space was acquired rather than scaled (LogicStream to QuVa, LSD-S15; Lumere to GHX, F2-S41; Trulla to SpendMend, F2-S42); at least four vendors are moving into the small-site wedge, so a claim that no MES fits a small sterile node has a shrinking window (LPMS section 5.7); and an incumbent can add a calibration layer to its own agents without changing distribution (competitive landscape 4.7, counter-argument).

For, narrowly: "validated model-driven mandatory hold as the disposition mechanism" is `uncertain` with no vendor found (F2-S57, F2-S48); no AI feature in the quality category publishes an error rate, a risk-coverage curve or a stated behaviour under distribution shift (competitive landscape 4.7); and the one OS-shaped position the prior-art review records as unoccupied is 6.6, manufacturer-side capacity coordination across independent owners (F2-S63, F2-S64, F3-S19), which HDA frames as a Sherman Act and DOJ/FTC question before it is a product and which ASPR is already part-funding on the registry side (LGOV-S17, LGOV-S51). 6.6 is not a day-one product.

Stated plainly: the defensible asset here is a method and an evidence standard. Methods are publishable rather than excludable, and this wedge's own falsifier is a segment no listed vendor serves, which nobody has shown exists (F2-S01).

## 11. Channel conflict

Two kinds, and the engine scores neither. Channel conflict, data rights and commercial control are not represented in the engine at all (`os_only_and_virtual_network.md` section 3.2); they are decided by contract fields that are UNANSWERED for every architecture and by evidence nobody has supplied (HA-24, HA-33).

First, the "manufacturer later" clause is itself the conflict. A vendor that later manufactures competes with its own software customers. The nearest documented precedent runs the same way: CDMO partners refused BARDA capacity over the risk of being displaced when the government called (F7-S01). A customer who reads this roadmap will price that risk into the contract or decline it.

Second, selling drift detection to hospitals or GPOs rather than to manufacturers puts the company against the parties whose money already flows to Vizient, Premier and Bluesight (F2-S33 through F2-S39), inside a channel where three GPOs cover over 90 percent of US hospitals and optimise on price (LSIM-S20).

## 12. Failure conditions, stated as observable events

1. A customer's inspection cites a record the tool wrote or influenced. The 211.22(c) exposure has been realized (F2-S52).
2. An incumbent (Sartorius, Korber, Veeva, MasterControl) ships a distribution-free or conformal limit on the same statistic, or a buyer points out that a classical limit in the same stored file already sits at parity (`Box g*chi2`, 5.03 percent false alarm at detection 0.9988). The only measured advantage, 4.35 percent at detection 0.990 against the parametric limit's 18.68 percent at detection 1.000, is gone.
3. On the customer's own lots the tuned threshold's false-hold rate on clean batches exceeds roughly 10 percent, the cost-optimal rate at the illustrative costs, or the threshold misses a real fault family that matters (`release_assurance_followup.md` sections 3.4, 4). The public result did not transfer.
4. Six to eight conversations with the buyer role return nobody who will pay for a hold decision they must still own, or name a price below the cost of a validated deployment.
5. Twelve months pass with no shadow deployment on real lots.
6. FDA's AI guidance or EU Annex 22 finalises in a form that makes a model-driven hold unfileable, or a documented regulatory refusal appears. That is the falsifier already written into the F2-S57 and F2-S48 row.
7. The bridge has no landing: at 24 months no contracted-capacity design has a named counterparty in any `ContractTerms` field, and no purchaser has funded readiness. The evidence already leans this way, since no US purchaser has been found paying a standing reservation fee for sterile generic capacity (F3-S28, F7-S16).

## 13. Evidence required before advancing past the first gate

| Evidence | Human action |
|---|---|
| Acceptable role of a model in a GMP quality system; true deviation rate per batch and investigation duration; a sourced wrong-release cost to replace the tier-5 placeholder | HA-22, with HA-21 for site and campaign context |
| Regulatory reading of a model-driven mandatory hold, and the filing form of abstention | HA-23, reviewed by HA-31 |
| Final status of FDA's January 2025 AI credibility draft guidance and of EU GMP Annex 22 | HA-16 |
| Buyer economics: sites per contract, annual contract value per site, and what the spend displaces | **HA-37**, rank 29 in `../../audits/07_human_action_queue.md`, added in this session's queue revision after this roadmap was drafted; the row proposed in `os_only_and_virtual_network.md` section 6.1 item 1 now exists. Until it is answered the engine still has no revenue side, so the roadmap cannot be costed |
| Demand and price context for any later manufacturing step | HA-11, HA-24, HA-33, HA-20 |
| Public claims corrected before outreach begins | HA-04, extended to C001 to C025 per `public_claims_corrections.md` section 4(i)2 and section 7; that document was written before C025 was added, so the register rather than that section defines the scope, and DF22's fourteen rows include C025 |
| Contact-list exposure closed before any outreach, since outreach is this roadmap's first activity | HA-06, HA-07, HA-08 (`privacy_remediation_plan.md`) |
| Founder decisions that gate everything downstream | HA-01, HA-02, HA-05 |

## 14. What this roadmap cannot answer with the current package

1. **Whether a software company here is a good business.** The engine bounds the operational value of an OS to a manufacturing network and nothing else. It has no revenue, customer, price, contract value or churn (`os_only_and_virtual_network.md` section 2.1).
2. **The price and the buyer.** No market price exists in this package for anything, and the one OS-shaped money parameter is a cost Telo pays rather than a price Telo charges (section 6).
3. **Whether the drift result transfers to a sterile injectable line.** The frozen data have no real lots, no real drift, no real operators and not the target chemistry. The protocol's own evidence boundary says the same: a methods proof of instrument-shift detection and abstention on public spectra, and not evidence of commercial batch release, useful operational coverage, target chemistry, prospective validation or sterility assurance (`protocol/protocol.yaml` `current_evidence_boundary`).
4. **Whether the bridge lands.** Nothing here models software revenue funding or accelerating a manufacturing step. The measured operational value of a perfect OS to the network is about 0.03 USD per delivered unit against an OS charge of 0.96 USD per unit at the base price and up to about 2.56 USD at the declared high (`os_only_and_virtual_network.md` section 3.1), so the case for the bridge is entirely commercial and entirely unmodelled.
5. **Whether unoccupied position 6.6 is legal.** Multi-owner capacity coordination is an antitrust and contracting question first (F2-S63, F2-S64, F3-S19; taxonomy incompatibility 12). It needs counsel, not a model.
6. **Whether this roadmap beats the other three.** That comparison is not made here. What the package supports is narrower: the architectures that clear the frozen target under illustrative inputs are contracted and reserved ones rather than software ones, and no OS strategy has ever been simulated at all, because no configured strategy uses the `deviation_rate_factor` or `investigation_duration_factor` handles (`os_only_and_virtual_network.md` section 2.1). The landing point named in section 0 is taken from the synthesis's own answer, not from a ranking made here.
