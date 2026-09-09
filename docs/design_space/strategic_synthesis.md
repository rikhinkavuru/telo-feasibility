# Strategic synthesis (deliverable 24, and the assignment's final answer)

> **Superseded in part, 2026-09-06.** Revisions R009 to R011 changed the feasible set. Read
> `docs/design_space/post_R009_correction.md` first; where it disagrees with this document, it wins.
> Three statements below are withdrawn there: that distributed nodes meet the target nowhere, that no
> frozen comparator meets it, and that bright-stock postponement is the strongest shape for both products.


Prepared 2026-09-05. Deliverable 24 of `ASSIGNMENT.md`, answering its twelve closing questions in order.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result in this document is the behaviour of the engine under evidence tier 5 (illustrative) inputs. It is not a statement about
sterile-injectable manufacturing in the world, not a recommendation to a purchaser, and not a finding. 87 of 91 parameters are marked illustrative (`make status`, DF09, in
`definition_of_finished_status.md` section 1). All sixteen regulatory gates in `config/regulatory_gates.yaml` are UNCERTAIN with no reviewer and no review date; the set moved from fifteen to sixteen
when revision R007 added G16 (`protocol/revisions.csv` R007). UNCERTAIN is never PASS, `eligibility` is NO_CONCLUSION for all twenty strategies (`results/design_space/ds_post_R008/summary.json`,
`meta.eligibility`), and no favourable decision class is assigned anywhere below. 503B is a time-varying legal state and never a durable pathway. Nothing here is legal or regulatory advice. No
interview, partner, customer, purchaser, reviewer or regulatory opinion is asserted, because none has occurred. Nominally separate sites are not assumed independent. Every novelty statement carries a
prior-art source id or says that none was found.

---

## Answer to the governing objective

The strongest intervention this evidence supports is not a plant Telo builds. It is a single approved presentation supplied from US aseptic lines that are already registered and already inspected,
bought as contracted campaigns rather than constructed, paired with a deep positioned finished-goods tier, and monetised by ordinary unit sales rather than by any readiness or availability payment.
Two configured strategies carry that shape, S11 (bright-stock campaign offtake) and S16 (reserve-triggered campaign network on contracted registered capacity), and this package cannot separate them:
both sit on both cost-service frontiers, both meet the frozen target on both products, and they are the only two of the five designs that meet it on both whose required committed share stays below 1.0
at an assumed 18.00 USD per unit (`feasibility_regions.md` sections 3 and 4). That result is provisional in a way that matters. It rests on an engine that seeds opening inventory free of charge
(NEW-1), on a hard-coded regional review rule the protocol never specifies (MD-3), and on search spaces that were not matched across architectures (MD-12); when four comparators were re-optimized over
one common inventory space, added central capacity became feasible on both products and the cost gap narrowed to about a third (`feasibility_regions.md` section 8). So the honest ranking is a shape,
not a strategy id: buy or contract registered capacity, position stock, sell units. Three pieces of decision-critical evidence separate the candidates inside that shape and decide whether it is a
business at all: the true demand denominator and installed capacity for the exact presentation (HA-11), a price and committed volume a purchaser with authority will actually sign (HA-36, HA-24), and
the reporting category for adding a third-party sterile fill site to an approved application (HA-23, then HA-31). Until those land, the defensible statement is narrower than any architecture: the
distributed-microplant thesis fails in this model for reasons that are mostly not about distribution, and no architecture in the battery is contractable today.

---

## 1. What failed in the original thesis?

Four things, and they failed for different reasons.

**The release layer.** Conventional release in the engine is the maximum of the parallel components plus serial QA, so at base it is max(sterility 14, environmental monitoring 7, assay 5, endotoxin 2)
plus 2, which is 16 days. Zeroing the entire chemical queue removes exactly 2 of those days, 12.5% (`bottleneck_decomposition.md` section 6.6). In the post-R008 ablation the release queue is worth a
leave-one-out mean fill delta of +0.00074 on norepinephrine and +0.00033 on sodium bicarbonate, and the sterility hold +0.00248 and +0.00136 (`product_architecture_matching.md` section 3.3). A fully
validated release layer saves zero days while sterility binds (`tests/integration/test_extremes.py::test_full_release_assurance_saves_no_days_when_sterility_binds`). The claim register records the
public form of this claim as contradicted by the company's own analysis (`CLAIMS_REGISTER.csv` C009).

**The distributed owned nodes.** S5 and S6 meet the frozen target in no region of any recorded range of any swept input, on either product (`feasibility_regions.md` section 6, family 1). On sodium
bicarbonate S5 is dominated by 16 strategies and S6 by 17 (`feasibility_regions.md` section 4). They lose 0.287211 of the measured window to commissioning, which is 524.4 capacity-weighted days of
1826, while every contracted design loses 0.000000 to 0.090273, the highest being S12's contracted base, and the reserve-triggered and rotating designs 0.000000 to 0.044420
(`os_only_and_virtual_network.md` section 3.2). Their cost per delivered unit at the starting designs is 40.6039 and 42.6897 USD against 14.4671 for S16 in the same table; S16's 13.1807 USD/unit is
its optimized design in `opt_20260903T220534Z`, which is a different evaluation.

**The operating system.** A perfect-OS ablation, which zeroes every deviation, every rejection and all yield variance, moves mean fill by +0.001771 averaged over 40 cells, at most +0.008638, and flips
3 of 40 feasibility verdicts, all three from inside 1.3 binomial standard errors of the requirement. It saves at most 40,684 USD per year against an OS charge of 600,000, a ratio of 14.7x, and up to
33.9x at four sites (`os_only_and_virtual_network.md` section 3.1). The prior-art review puts the manufacturing OS on its does-not-survive list in all eight sub-forms (`prior_art_review.md` section 6,
closing paragraph).

**The beachhead and the public record.** The frozen FDA shortage export shows 0 rows for norepinephrine and 33 for furosemide since 2020-04-07 (`HANDOFF.md` section 2), and the original
norepinephrine-to-epinephrine pick is recorded as retracted internally (`CLAIMS_REGISTER.csv` C008). Fourteen register rows are unsupported, contradicted or retracted: C001, C007, C008, C009, C010,
C012, C013, C015, C016, C017, C018, C023, C024, C025 (`definition_of_finished_status.md` section 1, DF22).

## 2. Which failures were structural?

Structural here means the mechanism holds at every point of every declared range, which is the definition `bottleneck_decomposition.md` section 1 sets for itself.

1. **Mass balance.** A network whose saleable capacity is below demand cannot be stocked out of the deficit. A full year of safety stock with daily base-stock review leaves sodium bicarbonate S0 at
  fill 0.869115 with `p_meet` 0.00 (`results/ablation/abl_post_R008/summary.json`, key `bounds:ss365+base_stock|sodium_bicarbonate_8_4_50ml|S0`, `fill_rate.mean` 0.8691151834025985, n = 60; the
  pre-R004 run reported 0.856140 and is superseded for quantitative use). At twice base demand no strategy of the twenty meets the target in any of the 18 reversal cells on either product
  (`feasibility_regions.md` section 5). This is the one region of the map where the answer does not depend on which architecture is chosen.
2. **The sterility pole for the aseptic archetype.** 14 days is the argmax of the parallel release set at every corner of the declared release box, because the concurrent chemical maximum tops out at
  7 against sterility's low of 14 (`bottleneck_decomposition.md` sections 6.6 and 6.7). No analytical or statistical method removes the attribute; only the process route does
  (`architecture_taxonomy.md` incompatibilities 2 and 3, F11-S02, F11-S03, F11-S41).
3. **Capacity that must be built cannot serve the days before it exists.** The arithmetic is structural. How many days that is was an artifact until R008 (see section 3).
4. **Non-independence of the topology.** Every S0 to S7 plan carries `cc_api_1` or shares `cc_vial_1`, and every site takes `api_1`, `vial_1` and `stopper_1` except S2's second source
  (`bottleneck_decomposition.md` section 8). Adding sites cannot reduce supplier exposure. The consequence is not structural: the common-cause rate reverses the S2 verdict inside its own declared 0.02
  to 0.3 range.
5. **Regulatory constraints that no design choice reaches.** Batch disposition is non-delegable under 21 CFR 211.22(a), an extramural facility is an extension of the manufacturer under 21 CFR
  200.10(b), and a quality agreement cannot delegate CGMP responsibility (F3-S41, F3-S42, F3-S43). One quality unit across units requires one legal entity and the proposed rule excludes contract units
  (`architecture_taxonomy.md` incompatibility 7). No injectable is on the 503B bulks list, FDA does not read backorders as clinical need, and the copy rule ends the product line when the listing ends
  (incompatibility 4; L503B-S02, L503B-S07, L503B-S03).
6. **A commercial failure that is not proved structural but is unrefuted.** Zero of the 42 generated candidates is contractable today (`novel_architectures.md` section 1). No US hospital system, GPO
  or state has been found paying a standing reservation fee for sterile generic capacity (F3-S28), and FDA's own task force records that most generic manufacturers cannot afford redundant capacity
  (F7-S16). That is an absence of evidence, and the package treats it as "assume no until a purchaser says otherwise" rather than as proof (HA-38 fallback).

## 3. Which failures were caused only by illustrative inputs or by model artifacts?

Named by their register ids in `bottleneck_decomposition.md` section 7 and `novel_architectures.md` section 5.

| id | what it did to the result | status |
|---|---|---|
| MD-3 | the hard-coded regional reorder rule decided 8 of 16 Phase A cells at +0.82% cost; S15's sodium bicarbonate advantage disappears when the rule reverts (`inventory_capacity_hybrids.md` section 3.3) | deferred by design for S0-S7 |
| MD-4 | opening lots stamped at half a 24-month shelf life expired on day 365, the first measured day, which made larger safety stock read as harmful and invalidated every pre-R004 safety-stock conclusion | fixed, R004 |
| MD-7 | `capacity_factor` rescaled an existing plant instantly while identical capacity added as a new site waited 730 days | fixed, R004 |
| MD-6 | capital, fixed operations and validation accrued for sites that did not exist yet | fixed, R004 |
| MD-14 | a reserved line was charged full capital and then a reservation fee on top; S3's annual cost fell about 40% on the fix | fixed, R004 |
| MD-17 | three commissioning-family parameters sat at 365 days, which is also `warm_up_days`, so any lead at or below a year cost nothing inside the measured window | fixed, R008 |
| MD-1, MD-2 | the material order-up-to level and reorder point are `(target_days + lead) x daily demand`, so `api_lead_time` and `component_lead_time` measure buffer depth and carry the wrong sign in 13 and 14 of 16 cells; 5 of 7 threshold crossings return `feasible_above` and no maximum API lead time is claimed (`feasibility_regions.md` section 3 row 5) | MD-2 fixed R005; MD-1 open |
| MD-11, MD-12 | the optimizer tie-break has no MCSE tolerance and the search spaces were not matched; the statement that no frozen comparator meets the frozen target was an artifact of that, and added central capacity meets it once searched fairly (`feasibility_regions.md` section 8; NF-9) | open |
| MD-15 | one product per network, so every portfolio and postponement claim is an accounting proxy and the pooling threshold of 5.08 and 4.82 comparable presentations per node is untestable (both figures come from a pre-R004 run and are superseded for quantitative use) | open, recorded as scope |
| MD-19, MD-20, MD-21 | a common-cause group on a supplier was structurally inert; the deterministic screen dropped reserved sites and charged no fee; the fee accrued before the line existed | fixed, R007 |
| MD-22 to MD-25 | screen common-impact not comparable across arms; exercise cadence nearly unmeasurable on frequently activated lines; take-or-pay has no service channel; a shared OS carries hazard with no cost line under R0 | open |
| NEW-1 | opening inventory is seeded with no ledger charge and scales with the design's own stock policy; on sodium bicarbonate that is 1,200,000 units covering 5.08 years of a 236,100 units/yr structural gap over a five-year window, and S15 delivers 121.8% of its own annual saleable capacity (`inventory_capacity_hybrids.md` section 3.3) | open |
| NEW-2 | allocation rights are inert everywhere; all four `allocation_policy` values collapse to proportional | open |
| NEW-3 | no readiness-decay hazard, so exercising a line buys production volume and not reliability | open |

Two input artifacts belong beside these. The two products differ mainly through one derived tier-5 number, `status_quo_utilization` 1.245 against 0.778, and audit item WB-26 records the two dossiers
as near-clones on several axes, so most apparent product discrimination in this package is not evidence (`bottleneck_decomposition.md` section 8; `product_architecture_matching.md` section 2). And
five assignment failure modes bind nowhere at all: API lead time, component lead time as named, demand variance, demand covariance, and deviation or rejection (`bottleneck_decomposition.md` section
4).

## 4. What interventions were explored, including the ones rejected and why?

The morphological matrix holds 18 dimensions and 130 options, each with a source id or an explicit "no external precedent found" (`architecture_taxonomy.md` preamble). Fourteen families produced 42
candidates. Twelve were configured as S8 to S19; thirty were not (`novel_architectures.md` sections 2 and 4).

Configured: S8 acquired registered line; S9 dual source with an honest key-starting-material tier; S10 split tenancy across two hosts; S11 bright-stock campaign offtake; S12 contracted
registered-capacity base; S13 contracted base plus rotated surge plus reserve; S14 cooperative-financed registered second source; S15 capacity-adequate presentation with positioned inventory and no
plant; S16 reserve-triggered campaign network; S17 rotating campaign network; S18 dual committed supply with contract-mandated distinct API and container sources; S19 maintained switching package with
an exercised standby line. Six of the twelve are instruments rather than businesses: S9, S10, S12, S15, S18 and part of S13 (`novel_architectures.md` section 1).

The rejections carry the information. The OS replenishment layer scored highest of the software candidates at 9.28 and was rejected under pruning rules P2 and P5, because its whole measured effect is
the MD-3 artifact and every adjacent standalone vendor was acquired rather than scaled (LogicStream, Lumere, Trulla). The OS activation layer was rejected under P6, because the product is an
allocation right and the engine has none (NEW-2). Plain committed-volume offtake was rejected under P5: it is Civica, Vizient, Premier and HealthTrust with no stated reason Telo beats them, and none
of the four contracts with a pre-approval manufacturer. Anchor tenancy with divertible slots was rejected because the diversion right may not be purchasable at any price, which is what industry
refused at CIADM for fear of displacement (F7-S01). Hub-and-spoke with held sterile bulk failed on two independent kills: EMA expects refiltration if bulk is not filled within 24 hours (F5-S16) and
the engine lets a spoke hold about 62 days of formulated bulk. The multi-holder pool fails on law before economics (F5-S33, F2-S63). Terminal-route conversion is already falsified for one of the two
modelled products, because autoclaving sodium bicarbonate at 121 C produced sodium dawsonite crystals from aluminium leached out of the glass (F11-S31). Mobile and modular architectures fail because
21 CFR Part 607 contains no mobile provision and the qualification and release clock restarts after a move, which is slower than shipping inventory (F14-S01, F14-S02, family 14's own verdict). The DME
modular fleet scored lowest at 3.30, rejected because gate G14's treatment is `no_fleet_claim` while UNCERTAIN, which removes the pooled-validation and shared-quality-unit savings that are its whole
economic case, and because its registration instrument is a proposal. The separate consolidated acquired DME network scored 6.18 and was rejected on the word search: the proposed rule's text contains
no occurrence of "sterile", "aseptic", "503B", "outsourcing facilit" or "real-time release" (F1-S01). The two-part capacity option was rejected under P4 with affirmative negative evidence: Emergent held a 542,750,000 USD federal capacity reservation and separately
sold four commercial aseptic fill lines for about 30 million (F7-S04, LCDM-S10).

## 5. What architecture currently appears strongest?

The contracted-campaign-plus-positioned-inventory shape, carried by S11 and S16, which this package does not separate.

Of twenty strategies, five meet the frozen target (mean fill at or above 0.99 in at least 90% of runs) on both products: S9, S11, S12, S13 and S16 (`feasibility_regions.md` section 4,
`ds_post_R008/dominance.csv`, 40 paired runs). The frontiers, cheapest first, as mean annual cost / mean fill / `p_meet` / meets target:

- Norepinephrine: S15 12.58M / 0.9925 / 0.825 / no; S11 14.86M / 0.9950 / 0.95 / yes; S16 15.89M / 0.9967 / 0.90 / yes; S17 18.20M / 0.9972 / 1.00 / yes; S9 23.23M / 1.0000 / 1.00 / yes.
- Sodium bicarbonate: S1 12.67M / 0.7591 / 0.00 / no; S15 13.16M / 0.9412 / 0.125 / no; S11 15.71M / 0.9970 / 0.925 / yes; S16 16.48M / 0.9972 / 0.925 / yes; S12 22.40M / 0.9976 / 0.95 / yes; S9
  24.40M / 0.9997 / 1.00 / yes.

At an assumed 18.00 USD per unit, which is an assumption and not evidence, only S11 (0.798 norepinephrine, 0.599 sodium bicarbonate) and S16 (0.845, 0.632) keep their required committed share below
1.0; S13 needs 1.091 and 0.820, S12 1.235 and 0.928, S9 1.460 and 1.097 (`feasibility_regions.md` section 3 row 1). Both buy capacity that already exists, so both lose 0.0000 of the measured window to
commissioning (`product_architecture_matching.md` section 3.3). For S16 that zero is a metric artifact rather than a property: `_commissioning_window_loss` excludes reserved sites, and its two
contracted lines carry `commissioning_days` 540, 29.57% of the measured window (`os_only_and_virtual_network.md` section 3.2). One of the service verdicts also sits on the requirement rather than
above it: S16 on norepinephrine meets the tail at `p_meet` exactly 0.90 on 40 paired runs, one binomial standard error (0.047) from failing, so that cell is inside noise and should be re-evaluated at
higher n before it is used to separate S11 from S16.

What separates them is small and points both ways. S16 is the only architecture with a documented shape in all nine `ContractTerms` fields, and it is still not contractable, because a shape is not a
signature (`os_only_and_virtual_network.md` section 4.1). S16 also holds the only claim in this family that a run supports at all (`falsification_register.csv` data row 22), while all three S11 rows
are untested and S11's capacity-matched control was never run. Against that, S16's distinguishing coupling is inert in the engine (MD-23, MD-24), and S11's postponement content is expected to be zero
by construction, because MD-15 leaves one presentation, one market and one labeler, so the unlabeled pool and the finished-goods pool are the same object.

Three qualifications belong in the same breath. The advantage is partly an accounting gift (NEW-1). The comparison with the frozen comparators was not matched, and re-optimizing four of them over one
common inventory space makes added central capacity meet the target on both products, at 20.0M and 23.7M USD/yr against 37.8M and 38.6M under its declared space, leaving S11 and S16 cheaper by about a
third rather than by an order of magnitude (`feasibility_regions.md` section 8). And both ledgers carry the incumbent plant's capital of 6,703,202 USD/yr, identical to S0 (MD-14 residual), so neither
figure is a Telo-only cost (`os_only_and_virtual_network.md` section 2.2).

Distributed owned nodes are the one group the fair-comparison correction does not rescue. Given the same inventory freedom, norepinephrine S5 improves from 0.9801 and 0.58 to 0.9950 and 0.85 at 20.0M
against 35.4M, and still misses; sodium bicarbonate S5 reaches 0.9883 and 0.58 and costs more, not less (`feasibility_regions.md` section 8).

## 6. Under what exact conditions does it work?

Conditions, not scores. Each is the bisected crossing at 20 paired runs, so each carries a binomial standard error near 0.067 on `p_meet` and is located to about one bracket plus one standard error
(`feasibility_regions.md` section 1).

**S11.** Norepinephrine: annual demand at or below 1.09M units, batches at or above 36.9 per site-year, shelf life at or above 12.3 months, common-cause rate at or below 0.173 per group-year,
per-supplier disruption rate at or below 0.471, changeover at or below 9.58 days, release time and activation latency unbounded inside their ranges. Sodium bicarbonate: demand at or below 1.19M,
batches at or above 44.4, sterility incubation at or below 14.3 days (8% of the range, so 0.31 days above base), shelf life at or above 19.9 months, common-cause at or below 0.182, supplier rate at or
below 0.402, activation latency at or below 27.7 days, changeover at or below 3.39 days against a 3-day base (`feasibility_regions.md` sections 2.1 and 2.2).

**S16.** Norepinephrine: demand at or below 0.93M, batches at or above 43.1, common-cause at or below 0.138, supplier rate at or below 0.437, changeover at or below 6.48 days. The API-lead cell for
that pair reads `none` in `feasibility_regions.md` section 2.1, which is not a condition but the MD-1 sign defect showing through; no API-lead condition is stated for any architecture (section 3 row
5). Sodium bicarbonate:
demand at or below 1.25M, batches at or above 43.1, sterility at or below 16.6 days, common-cause at or below 0.173, supplier rate at or below 0.591, activation latency at or below 22.73 days against
a 21-day base, changeover at or below 5.64 days (same sections). The sodium bicarbonate demand ceiling of 1,246,875 sits 3.9% above the base of 1,200,000, which is inside the interval a real
utilization measurement would carry (`inventory_capacity_hybrids.md` section 3.5).

**Commercial conditions.** S16 needs 0.887 of realized sodium bicarbonate demand and 0.902 of norepinephrine demand committed to break even at its own break-even price of 13.18 and 16.94 USD per unit
(`inventory_capacity_hybrids.md` section 4). The price at which the required committed share reaches exactly 1.0 is 11.26 USD per unit for sodium bicarbonate S11 and 14.60 for norepinephrine S11. For
context, USP reports that 74% of sterile injectables in shortage price below 15 USD per unit and 44% below 5, n = 61 (F12-S14), and under illustrative costs the status quo itself needs 14.26 USD per
unit on norepinephrine to break even (`feasibility_regions.md` section 3). No price a purchaser will pay is known for either presentation.

**Conditions that do not bind.** Fixed QA cost per node crosses nothing between 1.5M and 6.0M USD per site-year, node capital nothing between 15M and 100M, and the global commissioning sweep nothing
between 365 and 1095 days; the third of those says more about the sweep's reach than about robustness (`feasibility_regions.md` section 2.3). Fixed QA cost changes the preferred strategy in zero of 27
reversal cells per product (section 5).

## 7. What evidence could overturn that conclusion?

**In-model, needing no person.** Charge opening inventory at variable materials plus conversion on day 0 (NEW-1) and re-run; every inventory-led design in the battery is flattered by it today. Give
the frozen comparators the same inventory search space and the same review rule (MD-12, MD-3); this has already changed one verdict (`feasibility_regions.md` section 8). Link activation failure to
exercise cadence and add a requalification lead (NEW-3, MD-23); until then S16's readiness coupling has no run behind it and S17 is routine contracted supply wearing a standby label. Give take-or-pay
a service channel (MD-24). Decouple the material buffer from the lead time (MD-1). Plumb allocation rights (NEW-2). Extend the commissioning metric to reserved sites, since S16 reports 0.000 window
loss while both its contracted lines cannot make commercial product for 540 of 1826 measured days (`inventory_capacity_hybrids.md` section 2 item 5).

**Human evidence.** HA-11 returning a demand denominator above the architecture's ceiling removes it outright. HA-36 or HA-24 returning a price below break-even removes the commercial case. HA-23
returning "prior approval supplement with a preapproval inspection" for a third-party sterile fill site removes S12's 365-day leg and weakens the whole contracted family
(`os_only_and_virtual_network.md` section 6.2 item 1). HA-38 returning "nobody funds standing availability" leaves every capacity-carrying design unfunded by construction. HA-34 returning "aseptic"
for every candidate closes family 11 permanently.

**Pre-declared falsifiers already written.** Two of three CDMOs declining to sell bright stock, or G07 coming back as CBE-30 or a prior approval supplement, removes S11 (`falsification_register.csv`
data rows 10 and 11). A contract found coupling reserve depletion to a pre-qualified campaign trigger withdraws S16's novelty claim (data row 24). An operating pooled bright-stock service for US
generic injectables withdraws S11's novelty class (`novel_architectures.md`, S11). The register carries 33 claim rows: 24 untested, 6 falsified in the model, 3 supported under illustrative inputs.

## 8. What should Telo build first?

Not a plant, and not a product. The first build is the evidence and the corrections, in this order.

1. **Close the live privacy exposure.** One command makes the repository private (HA-06). The exposure covers 29 people with addresses in `outreach/lab-contacts.md` and up to 18 more in
  `outreach/facilities.md` (`privacy_remediation_plan.md` section 1).
2. **Fix the defects that carry the ranking, then re-run the battery.** NEW-1, MD-3 and MD-12, NEW-2, NEW-3 with MD-23, MD-24, MD-1. This is code plus protocol revisions and needs no person. Until it
  lands, no cost or service comparison between a deep-stock design and a capacity design in this package is sound (`inventory_capacity_hybrids.md` section 6 item 1).
3. **Buy the three inputs that decide the regions.** Utilization and installed capacity per presentation (HA-11), node and reserved-capacity cost with batch, campaign and changeover data (HA-13,
  HA-21), and contract terms with a price from a person with authority (HA-36, HA-24).
4. **Get the regulatory categories in writing.** G07's reporting category first (HA-23), then statuses for all sixteen gates with a named reviewer and a date (HA-31).
5. **Then, and only then, the commercial build:** one approved presentation, one application or label, one quality unit, one contracted campaign at a registered US line, and a positioned
  finished-goods tier, sold as units. The comparators say the timeline will be long: Civica Petersburg took more than 1,600 days from construction start with pre-committed demand and was still pending
  approval (F13-S41, F13-S27, F13-S28), and a registered 110,000 square foot sterile plant bought in February 2022 was still recorded by FDA as not yet inspected 4.2 years later (L503B-S01,
  L503B-S21).

If a technical product is wanted before any of that, the one function this evidence supports is stop-the-line drift detection with a distribution-free limit on the industry's own statistic. The PCA Q
residual under a conformal limit holds false on clean batches at 4.35% at detection 0.990, against 18.68% at detection 1.000 for the parametric Jackson-Mudholkar limit on the same statistic, which
claims 5% (`research/conformal/results/gate_summary.json`, `detectors`; `release_assurance_followup.md` section 4 item 2). Two caveats travel with it. The statistic was chosen on the instrument it is
evaluated on, so the abstention headline carries an unmeasured optimism (`release_assurance_followup.md` section 2, leakage item d2), and the 2% false-hold figure quoted elsewhere for this gate is at
a threshold tuned on the family it is scored on. And two other classical limits on the same statistic sit near parity in the same stored artifact, `Box g*chi2` at 5.03% and detection 0.9988 and the
empirical percentile at 6.33% and 0.9933, so the measured advantage is over one incumbent calibration and not over the class. That is a hold decision, not a release decision.

## 9. What should Telo explicitly not build yet?

- **Owned distributed microplants.** They meet the target in no region of any recorded range, they are the group the fair-comparison correction does not rescue, and prior art records them as occupied
  in pilot and failed in every funded federal analogue: Civica slipped with no commercial batch as of August 2025 (F1-S56, F1-S58), CONTINUUS took 69.3M USD and never commissioned (F1-S45), and On
  Demand Pharmaceuticals reached a 503A pilot of about 12,000 syringes (F1-S40).
- **A manufacturing OS as the flagship.** Worth about three cents per delivered unit at best against a charge of 0.32 to 2.56 USD per unit at sodium bicarbonate S17, four sites at the declared low of 100,000 and high of 800,000 USD per site-year against 1,249,852 delivered units (`os_only_and_virtual_network.md` section 3.1). The engine
  has no revenue side, so this package cannot say whether a software company built on it is a good business; it can say the operational value is small.
- **Anything positioned as automated release.** The register records "Telo automates the release decision" and "certifies pharmaceutical batches in real time" as contradicted (C010). Abstention is
  never release, and EU GMP Annex 17 section 3.10 makes the high-abstention behaviour hard to file as a release method.
- **A 503B core.** It is a time-varying legal state. Making the listing permanent is the forbidden world that produced the only two feasible S7 cells in Phase A (`bottleneck_decomposition.md` section
  6.17).
- **Mobile, modular, or a DME fleet claim.** No US registration instrument exists today, and G14's treatment is `no_fleet_claim` while UNCERTAIN.
- **Any design whose first revenue is a readiness or availability payment.** Assume no until a purchaser says otherwise (HA-38 fallback; F3-S28, F7-S16). CIADM is the recorded outcome: two of three
  sites used none of their capacity and the third 7%, on about 4M USD per year of task orders against a stated ready-state requirement of 30M to 60M (F8-S09, F7-S01).
- **A multi-product portfolio node.** The pooling threshold is explicit and untestable here, 5.08 comparable presentations per node for sodium bicarbonate and 4.82 for norepinephrine, and MD-15 makes
  the cost case an accounting proxy. The base rate is also against multi-site filings: of about 900 sterile-injectable ANDAs approved 2000 to 2011, 11 referenced more than one finished-dose facility
  (F6-S37).
- **A second presentation, or a product selection.** The honest output of a matching model over this longlist today is a partition into capacity-short and capacity-adequate and nothing finer
  (`product_architecture_matching.md` section 6 item 5). Selection is reserved to HA-03 and DF03.

## 10. What claim can Telo truthfully make today?

Only the `allowed_external_wording` column of `CLAIMS_REGISTER.csv`, quoted exactly. The usable set:

- On the company (C010): "in a public-benchmark methods study, our shift detector abstained under instrument drift; prospective product/site validation is the next step (protocol claim_discipline
  wording)".
- On positioning (C015): "software in development for sterile drug manufacturing, or: a release-decision support layer; never paired with 'automates the release decision'".
- On what exists (C023): "Telo is building ...; tier features stated as planned scope; designed to fit FDA's PAT framework, with no product-specific validation yet".
- On the dataset (C001): "615 tablets (155 calibration, 460 test) from the IDRC 2002 NIR shootout, each measured on two spectrometers; a further 40-tablet validation file ships with the data and is
  unused".
- On the drift result (C005): "under the repository pipeline (8 PLS components with per-wavelength standardization) the gate cut interval-miss exposure on the second instrument from 58% to about 0.7%
  by abstaining on 99% of tablets; under a standard pipeline (cross-validated components, no standardization) it released 56% of shifted tablets with 29% conditional error; in neither case is this
  release, it is stop-the-line detection".
- On release time for injectables (C009): "for aseptically filled injectables, chemical real-time release does not shorten the release hold while the 14-day sterility incubation is the critical path;
  it shortens the hold for oral solid dose; the candidate value for injectables is an assured beyond-use date and distribution radius, which is unvalidated".
- On the product pick (C008): "beachhead under revision: the original norepinephrine/epinephrine pick was withdrawn after primary-source checks (2026-07-16); furosemide 10 mg/mL is the current
  candidate pending a primary-source shortage check; candidate presentations are screened in this study".
- On the Phlow figure (C014): "Phlow's 2020 HHS/BARDA contract shows $696.7 M on USASpending (75A50120C00092, checked 2026-09-01); the announced ceiling including options was $812 M".

C007's website form, "holding mis-release near 3%", must be withdrawn rather than qualified in place: no tablet key equals 3%, the value is corn protein on changed sensor mp6, and the website figure
pairs tablet numbers with corn numbers. The row itself is not removed, and its allowed wording may be quoted exactly like the rest:

- On the drift result across both datasets (C007): "tablets: the gate cut interval-miss exposure from 58% to 0.7% by abstaining on 99% of shifted tablets (home: 8.6% ungated, 6.6% gated); corn
  protein: exposure fell from 99% to 3.5-4.4% on the changed sensors; never mix the two datasets in one figure" (`public_claims_corrections.md` C007 row and section 3, which list only "near 3%" and
  `shiftGated: 3` under Remove).

The rule on feasibility-model results has two parts and both bind. **No model result may be stated as a finding about the world, in any setting**, because every input behind it is tier 5. **Model behaviour under
stated illustrative assumptions may be described to a named interviewee or reviewer inside this study process**, which is what `../interviews/guide_core.md` section 2, `../interviews/field_kit.md` and the four
reviewer packets do, **and it may not appear on any public, promotional or fundraising surface, in any email, or in any document sent ahead of a conversation.** Corrected 2026-09-06: this sentence previously
stated the prohibition in an absolute form that forbade the interview and reviewer programme itself, which is a programme the same package requires. The narrower form was already the operative one at
`../reviewer_packets/README.md` section 7, and `../interviews/guide_core.md` section 7 now carries the identical wording. Nothing in `protocol.yaml` `claim_discipline` changes, because the absolute form was
never in the protocol.

## 11. What next piece of evidence has the highest decision value?

The value-of-information run is superseded and its numbers must not be quoted as current: `results/sensitivity/voi.json` covers sodium bicarbonate and S0 to S7 only, at 6 runs per scenario on designs
from `opt_20260902T043854Z`, generated 20260902T045142Z, before revisions R004 to R008. Its ordering is EVPI 4,757,494 USD/yr on annual cost, with EVPPI 1,477,355 for raw-material lead time, 1,150,473
for common-cause dependence and 1,016,954 for capacity utilization, against approximately zero for release time, fixed QA labour per node, demand CV, shelf life and node scale. Two readings survive.
The near-zero entries agree with the post-R008 ablation and with the reversal map, where fixed QA cost changes the preferred strategy in zero of 54 cells. The top entry is an artifact channel, because
MD-1 makes the material lead a buffer-depth dial rather than a lead-time dial, so it should be read as "fix MD-1", not as "measure supplier lead times first".

Setting that against the ranked queue (`docs/audits/07_human_action_queue.md` section 1), the order by decision value is:

1. **HA-11**, utilization and installed capacity per presentation (rank 5). It accounts for 46 of 138 crossings, it is the only axis whose reversal map has a region where nothing qualifies, and it
  decides which of the two products is representative.
2. **HA-40**, the replenishment review policy and order-up-to level at real regional stocking points (rank 6). It decides 8 of 16 Phase A cells at +0.82% cost and is currently a hard-coded rule
  (MD-3).
3. **HA-13 and HA-21**, node and reserved-capacity cost, reservation-fee scope, batch size, changeover and commissioning (ranks 7 and 8). Fixed and resilience cost is 81.0% to 93.7% of annual cost for
  all eight comparators (`results/design_space/contract_conditions_sim_post_R008.csv`; NF-7's own 81% to 95% is computed on the pre-R004 run and is superseded for quantitative use), so every
  absolute cost in the package is a statement about the scaffold until these land.
4. **HA-39**, the rate, duration and impact fraction of events that remove more than one nominally independent site or supplier at once (rank 14). The superseded VOI run puts common-cause dependence
  at EVPPI 1,150,473 USD/yr, above capacity utilization's 1,016,954 and behind only the raw-material lead artifact (`results/sensitivity/voi.json`). The axis produces 20 crossings, and the feasible
  set collapses from 11 strategies to 3 on norepinephrine and from 10 to 2 on sodium bicarbonate at base demand as the rate rises from 0.02 to 0.3 (`feasibility_regions.md` sections 5 and 7). Its
  queue rank of 14 sits below that decision value; the queue does not reconcile the two, and the reason to discount the EVPPI is that the run behind it is superseded, not that the axis is small.
5. **HA-36 and HA-24**, contract terms and price (ranks 9 and 10). Five of the thirteen strategy-product cells that meet the service target move from commercially possible to impossible as the price
  falls from break-even to 18.00 USD.
6. **HA-31 and HA-23**, gate statuses and the G07 reporting category (ranks 11 and 12). Zero of sixteen gates are reviewed, so no favourable decision class exists anywhere.

Ranks 1 to 3 in the queue are the privacy items and rank 4 is threshold sign-off. They reverse no model result and still come first, for the reason the queue states: the exposure is live and the first
action costs one command.

## 12. What must the user personally do, in priority order?

| # | Action | Id | What it unblocks |
|---|---|---|---|
| 1 | Make `github.com/rikhinkavuru/Telo` private today | HA-06 | closes a live exposure of 29 people's addresses. No model result. There is no fallback for an exposure that stays open |
| 2 | Authorize history remediation, or repository deletion after a private mirror | HA-07 | the file sits in 17 of 19 commit snapshots, so visibility alone does not remove it |
| 3 | Relocate the contact lists and adopt the ignore rules, secret scan and pre-commit hook | HA-08 | prevention for the outreach that HA-20 to HA-40 will generate |
| 4 | Sign off the thresholds and every revision R000 to R008, in writing, before any result is used for a decision | HA-02 | DF01. Every feasibility verdict is stated against tau 0.99 and q 0.90, and the feasible set changes at 0.98 |
| 5 | Authorize commits to `~/telo` | HA-05 | DF20, and it is a precondition for HA-07 |
| 6 | Approve the public-surface corrections across the full register, C001 to C025, not the four claims the row originally named | HA-04 | DF22, fourteen contradicted or unsupported rows |
| 7 | Obtain utilization and installed capacity per presentation | HA-11 | 46 of 138 crossings; whether the capacity mode exists at all |
| 8 | Obtain the regional replenishment policy from a named planner | HA-40 | 8 of 16 Phase A cells; MD-3 |
| 9 | Obtain node and reserved-capacity cost, and line and campaign parameters | HA-13, HA-21 | every absolute cost figure; 20 crossings on changeover |
| 10 | Obtain a multi-site disruption rate, duration and impact fraction | HA-39 | 20 crossings; the feasible set collapses from 11 strategies to 3 on norepinephrine and from 10 to 2 on sodium bicarbonate at base demand, and common-cause dependence carries EVPPI 1,150,473 USD/yr in the superseded VOI run |
| 11 | Obtain contract terms and a price from a purchaser with authority, and ask directly whether anyone funds standing availability | HA-36, HA-24, HA-38 | `ContractTerms.missing()`; every design is "not contractable, stated" until then |
| 12 | Commission the regulatory review: all sixteen gate statuses, and the G07 category in writing | HA-31, HA-23 | DF08 and every decision class in the package |
| 13 | Decide furosemide's longlist status and fill volume, and commission the primary-source shortage check | HA-03, HA-18 | DF03 and DF04; furosemide is the most shortage-persistent candidate, 30 current rows over 6.40 years |
| 14 | Obtain the sterilization route per presentation | HA-34 | whether family 11 exists as an intervention and whether the 14-day pole is a constant or a design variable |
| 15 | Adopt one non-obvious finding, or state that none is adopted | HA-44 | DF21 |
| 16 | Engage the three independent reviewers | HA-30, HA-32, HA-33 | DF19; no review counts until qualification, issues, decisions and model changes are logged |

This order differs from the queue's ranked order, and the differences are deliberate. HA-05 and HA-04 are ranks 30 and 31 there and are lifted here because HA-07 depends on HA-05 and HA-04 gates any
external use of this work, so rows 2 and 6 cannot be executed strictly top to bottom as printed: settle HA-05 before acting on HA-07. HA-39 is rank 14 in the queue and sits here at row 10 for the
EVPPI reason given in section 11.

---

## What this package does not establish

- **Every economic input is illustrative.** 87 of 91 parameters carry evidence tier 5, and 0 are missing (DF09). That includes every demand, cost, capacity, lead-time, price and disruption input. No
  absolute cost, no break-even price and no capital requirement in this package is a statement about the world.
- **No interview and no independent review has happened.** Zero interviews against a 25 to 30 target (DF18), and zero of three qualified independent reviews (DF19). Every counterparty named anywhere
  in this work is a published third party cited by source id, never a Telo relationship.
- **All sixteen regulatory gates are UNCERTAIN**, with zero reviewed (DF08). No strategy carries a favourable decision class, and `regulatory.evaluate_all` returns NO_CONCLUSION for every id.
- **The release-assurance evidence is a methods proof on public tablet data.** 615 of the 655 tablets in the IDRC 2002 NIR shootout file, two spectrometers, no real lots, no real drift, no real
  operators and not the target chemistry (`release_assurance_followup.md` sections 1.1 and 5). It says nothing about a sterile injectable, about Telo's own data, or about a validated method. The
  certificate a quality unit would need scales with reference units, not model quality: a Clopper-Pearson bound at delta = 0.05 with zero observed losses needs 199 units for 1.5%, 299 for 1.0% and 598
  for 0.5%, and the repository has 155 reference tablets.
- **The model carries open defects recorded in `bottleneck_decomposition.md` section 7 and `novel_architectures.md` section 5.** Still open: MD-1, MD-3 (deferred by design), MD-5, MD-8, MD-11, MD-12,
  MD-15, MD-18, MD-22, MD-23, MD-24, MD-25, and the three found by the Phase B sweep, NEW-1, NEW-2 and NEW-3. Every run made before 2026-09-03 is superseded for quantitative use.
- **No price evidence exists.** The landscape review found no published rate card, minimum order value, reservation fee or per-unit price for US sterile fill-finish, 503B product, enterprise QMS, MES,
  shortage-data platforms or modular hardware across 313 sources; the only two public prices are a QMS subscription and an individual shortage-data subscription (LQBR-S14, LSD-S7).
- **No evidenced reason exists that Telo beats Civica, Vizient or Premier**, and pruning rule P5 requires one (`falsification_register.csv` data row 14, status `untested`; that row names Civica only).
- **Two near-clone products are not a portfolio and not a market.** WB-26 records the dossiers as near-clones on several axes, and norepinephrine failed beachhead verification, so it functions as a
  control rather than as a second case.
- **The backcasts are weak.** Three ongoing shortages of one class, against a DF15 requirement of four episode classes, and the fourth needs a documented single-site failure episode from a source a
  person has to obtain (HA-10).
- **Nine of twenty-two definition-of-finished tests pass.** Eleven of the thirteen incomplete tests cannot be closed by any amount of code. The modelling has run ahead of the evidence, and more
  modelling will not move the count.
