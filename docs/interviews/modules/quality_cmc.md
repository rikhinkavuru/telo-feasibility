# Module: quality, CMC, microbiology and validation

Roles: quality-unit head, CMC lead, microbiologist, or validation lead at a sterile-injectable manufacturer or a CDMO.
Queue items this module settles: HA-22, HA-34, HA-14, and the quality half of HA-30. Length: the whole call is 45 minutes and this module has about 28 of them; the one published timetable is
`../elicitation_worksheet.md` section 2. Run the parameter cards inside the module, not before it.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value in the "Now" column is a model input, not a
measurement, and everything in the last column is behaviour of the engine under those inputs. Nothing here asserts a
partnership, endorsement, customer, pilot or regulatory opinion, because none exists.

**Claim discipline, which governs this module in particular.** Nothing in this conversation may state or imply that a
model releases product, certifies a batch, or shortens a sterility hold. Abstention is never release. The protocol
fixes a list that no release-assurance layer removes: sterility assurance, endotoxin, mandatory compendial or
product-specific testing, quality-unit disposition, deviation investigations, validation and change control. The
study's release-assurance evidence is a methods proof on public near-infrared tablet data, not on a sterile injectable
and not on any Telo data. Do not paraphrase it beyond the allowed wording in `../../../CLAIMS_REGISTER.csv`.

**Why the questions changed.** In the model, conventional release is the maximum of the parallel components plus serial
quality review, which is 16 days at base. Zeroing the entire chemical queue removes 2 of those 16 days, 12.5%, while
sterility incubation binds. So this module stopped asking how to shorten chemical testing. It asks instead for the
component structure, the deviation and closure behaviour that drives the queue, and the process route, which is the one
thing found across fourteen architecture families that acts on the binding constraint itself.

**Question 2 is a document task first and an interview second.** HA-34 is the enabling input for the one
intervention found across fourteen families that acts on the binding release constraint, and it has almost no
answerable population as an interview question, because the source that settles it is confidential to its holder.
Fetch it instead: the reference product's approval package on Drugs@FDA (the chemistry review's sterility-assurance
section), a redacted establishment inspection report or Form 483 for the named site, and the USP monograph's
sterility requirement. Label text is not acceptable evidence in any of these; it does not carry the route. Ask a
person only about products they have personally worked on.

**How to run it.** Ask for the range before revealing the "Now" column. Ranges beat point estimates.

## Questions

| # | Question | Lands on | Now (declared range) | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | For an aseptically filled aqueous solution, what does the release clock actually look like: which tests start when, which run in parallel, and what is serial after the last result? | `sterility_incubation_days`; `environmental_monitoring_days`; `assay_days`; `endotoxin_days`; `qa_review_days` (HA-22) | sterility 14 days (14 to 18, evidence tier 1); environmental monitoring 7 (5 to 7); assay 5 (1 to 7); endotoxin 2 (0 to 3); quality review 2 (0 to 4) | days per component, plus an explicit parallel and serial map | If the components are not parallel in practice, the release model is wrong in structure and not only in value. The sharpest conditions in the whole grid sit on this axis: two cells lose the service target 0.31 days above the 14-day base |
| 2 | **For products you have personally worked on**, is the marketed product terminally sterilized or aseptically processed, and how do you know? If terminal, what is the cycle? | `ProductFeatures.sterilization_route`, a product attribute that does not exist yet (HA-34) | no value. The route is not published per presentation in any US or EU label reviewed | a category (terminal, aseptic) with the basis stated, for products in their own experience only. **Do not ask them to state the route for a third party's marketed product**: the document that would settle it is generally confidential to its holder, so the person who could cite it is the person who may not | Whether the process-route family exists as an intervention at all, and whether 14 days is a constant or a design variable. It is the only intervention found across fourteen families that acts on the binding release constraint rather than on components that do not bind. One negative is already on record: autoclaving sodium bicarbonate at 121 C produced sodium dawsonite crystals from aluminium leached out of the glass (F11-S31) |
| 3 | What fraction of batches raises a deviation that has to be closed before disposition? | `deviation_rate_per_batch` (HA-22) | 0.02 per batch (0.005 to 0.08) | a range, with the scope named (all deviations, or only those that hold disposition) | At the low end of the declared range the bound on what a perfect process can buy shrinks by roughly a factor of four |
| 4 | How long does such an investigation take to closure, and what does one cost? | `investigation_duration_days`; `investigation_cost_usd` | 21 days (7 to 60); 20,000 USD (5,000 to 80,000) | two ranges | The variance of the release queue, and the cost side of every quality mechanism in the battery |
| 5 | What fraction of batches is rejected at disposition, and for what reasons? | `batch_rejection_rate` | 0.01 per batch (0.002 to 0.04) | a range plus the leading causes | Deviation and rejection bind nowhere in the current decomposition. A surprising answer here would be a finding about the model's blind spot rather than a change in ranking, which is worth knowing either way |
| 6 | What does release testing cost per batch, at a contract laboratory and in house? | `product.testing_usd_per_batch` (HA-14) | 30,000 USD per batch (10,000 to 100,000) | a range with the panel named | The denominator of the release-benchmark break-even. At 2,000,000 USD per wrong release and 30,000 USD per batch of testing, a certified out-of-specification bound has to sit below 1.5% before the cost curve favours a gate at all |
| 7 | What does one wrong release decision cost a manufacturer, all in? | `wrong_release_cost_usd` (HA-22) | 2,000,000 USD (200,000 to 20,000,000) | a range, with the basis named (recall records, field corrections, out-of-specification investigations) | The sign of the release-benchmark cost curve. Until this lands the package reports that curve as a break-even ratio rather than as a dollar figure |
| 8 | What does qualifying a second site actually cost and replicate, and what can legitimately be shared? | `product.validation_usd_one_time`; the `validation_factor` design variable | 4,000,000 USD one time (1,000,000 to 12,000,000) | a range in USD plus a list of what replicates per site | The fixed-cost block behind every multi-site design. The legal half of the sharing question is in `regulatory.md` |
| 9 | **In your quality system today, what is the most a statistical model may do ahead of a disposition decision?** | gate G15; release scenarios R0 to R3 in `protocol/protocol.yaml` (HA-22; HA-31 assigns the gate status) | G15 is UNCERTAIN with no reviewer, so the release-assurance scenario stays at conventional release everywhere | a category (no role, monitoring only, shadow-mode decision support, validated release component) plus the conditions each would require | Whether the release-assurance scenario can ever be anything other than conventional release in this package. **The other half of the old question, what evidence a pre-declared abstention would need before it could be filed as an exclusion rather than as a fallback to the laboratory, is not asked.** Nobody has filed one: a model-driven mandatory hold has no confirmed regulatory form today and no vendor selling one was found, so the question asks a practitioner to speculate outside their own work. It is recorded as an open question against G15 instead |

## What was dropped, and why

- **Reference standards and per-site stability programme costs.** No parameter carries them separately; they sit inside
  fixed quality labour and validation, so an answer would have nowhere to land. Break them out only if question 8 shows
  they are large.
- **The old question about what an AI release layer may and may not touch.** Replaced by question 9, which asks the same
  thing inside the claim-discipline table and without implying that such a layer exists as a product.
- **Any question about shortening chemical release.** Under the model, removing the entire chemical queue saves 2 of 16
  release days while sterility binds, and a fully validated release layer saves zero days in the extreme-case test.
  Question 2 replaces it, because the process route is the only path that moves the pole.
