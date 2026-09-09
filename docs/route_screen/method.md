# Sterilization-route screen: method

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS. NOT LEGAL ADVICE.** No statement here has been reviewed by a qualified sterile-manufacturing, microbiology or generic-drug CMC professional. This file defines the screen. It is written before any evidence is gathered so the classification rules cannot be fitted to the answers. Output register: `docs/route_screen/determinations.md`, not yet written.

**Post-hoc amendments, 2026-09-06.** This file was written before evidence gathering so the rules could not be fitted to the answers, and that ordering is preserved by recording every later change here rather than editing silently. Three kinds of change were made on 2026-09-06 after an audit of the completed pass: (a) corrections of fact in quoted figures and quoted sources, which change no rule; (b) one addition to the evidence hierarchy in section 3, tier **E7**, registration and listing metadata, ceiling `unknown`, leads only. E7 is strictly tightening: it caps a class that had no row and was at risk of being read at E5. It cannot raise any determination; (c) one explicit exception clause in section 5 item 2 for fill-volume families, which was being relied on in practice and was not written down. No rule was loosened and no determination was raised.

Prior art: `../design_space/prior_art/11_terminal_sterilization_release.md` (source ids `F11-Sxx`) and `../design_space/prior_art_review.md` sections 6.1 and 7 item 11. Human action: **HA-34** (`../audits/07_human_action_queue.md` rank 13). Candidates: `../../config/longlist.yaml`, six presentations. Frozen snapshots usable as evidence: S01, S01B, S06, S07, S15, S16, S17, S18.

---

## 1. The question, and what it is worth

**Question.** For each longlist presentation, by what route is the currently marketed US product rendered sterile? Not the molecule, not the shortage. The route, per presentation, per application holder.

**Why it is the binding question.** The study computes hold time as `release_assurance.conventional_release_days` = `max(parallel components) + serial QA`. At base (`config/global.yaml`): sterility 14, environmental monitoring 7, assay 5, endotoxin 2, serial QA 2, so `max(14, 7, 5, 2) + 2 = 16` days. Zeroing the entire chemical queue removes **2 of those 16 days, 12.5%**, and those 2 days are the serial QA term alone: assay and endotoxin remove exactly zero at every point in their declared ranges, because the concurrent chemical maximum tops out at 7 against sterility's low of 14 (`../design_space/bottleneck_decomposition.md` section 6.6). Gate `G15` in full still saves zero days, because `REDUCIBLE_COMPONENTS = {"assay"}`. The pole is sterility and nothing on the chemical side reaches it.

**What a terminal route removes, and what it does not.** Only the process route reaches the pole, through gate `G04`, never `G15`. On the terminal branch with an approved parametric release program the USP `<71>` component is removed outright: the load monitor substitutes for the laboratory test under 21 CFR 211.167(a) [F11-S02; F11-S03]. The new pole is `max(EM 7, bioburden, assay 5, endotoxin 2) + QA 2`, which is 9 days at base *if* the new per-batch bioburden component is 7 days or less. It has no value in the model today and must be elicited, not assumed. So the prize is at most about 7 days, and only if environmental monitoring is not itself limiting. What does **not** fall away on any branch: environmental and personnel monitoring review, which FDA calls an essential element of the batch release decision [F11-S01 XII; F11-S04 10.10]; per-batch pre-sterilization bioburden, which parametric release specifically requires [F11-S04 10.3, 10.4]; endotoxin; assay, identity and strength [F11-S09]; particulate and visual inspection [F11-S04 8.30]; container-closure integrity [F11-S04 8.22]; and serial QA disposition [F11-S01 XII].

**Two honesty notes on the size of the prize, stated here so the screen is not oversold.** First, the study's own ablation ranks the sterility component third order: it flips 4 of 16 cells and never ranks above 3rd of 17 in any cell (`bottleneck_decomposition.md` sections 6.6, 6.7). The inventory contrast that used to be quoted here as "13 of 16 cells feasible with the hold fully intact" is corrected and labelled: `bounds:ss365+base_stock` reaches feasible in **11 of 16** on run `abl_post_R008`; the 13-of-16 figure came from the pre-R004 run `abl_20260902_phaseA`, which `bottleneck_decomposition.md` line 473 marks as "pre-R004 and must be regenerated before it is used again" and MD-3 corrects downward on 2026-09-06. **Every ablation figure quoted in this file is superseded for quantitative use pending re-run after R004, R005 and R008**; they are carried as ranking evidence, not as measurements. Second, FDA has **proposed** pricing the route in *dating* rather than cycle time. The instrument is 503B Appendix B Table D, and it is **revised draft guidance, nonbinding, and stamped "Draft - Not for Implementation" on every page** [F11-S45]; it is not in-force policy, and its own falsifier is recorded in the parent prior-art note: a final version that changes Table D removes the lever. As drafted, Table D gives 6 days at controlled room temperature for aseptic product released without a completed sterility test, against 14 days for terminally sterilized product on a validated indicator-monitored cycle, and 28 days for either route with a completed passing test [F11-S45]. The route more than doubles at-risk dating with no test. A model holding beyond-use date constant while varying release time is answering the wrong question for the 503B archetype.

So the screen's decision value is not "how many days does this save". It is **whether family 11 exists as an intervention at all for a given presentation, and whether the 14-day pole is a constant or a design variable** (HA-34, decision-value column).

---

## 2. Determination categories and the confidence ladder

**Unit of determination.** One presentation-holder pair: active ingredient, strength, container type and fill volume, under one named application holder. Route is a property of a manufacturing process at a site under an application. It is never a property of a molecule and never of a shortage listing.

| category | definition |
|---|---|
| `terminally_sterilized_moist_heat` | the filled, sealed final container is subjected to a validated moist-heat (steam) cycle as the sterilizing step for the drug product. Sterilizing filtration upstream of fill does not change this: the test is whether the sealed final container is sterilized. |
| `terminally_sterilized_other` | same final-container test, by dry heat, ionising radiation or gas. **Record the modality**, because US parametric release under CPG 490.200 is moist heat only and expressly excludes filtration, radiation, dry heat and ethylene oxide [F11-S02], while EU Annex 17 permits moist heat, dry heat and ionising radiation and excludes gas [F11-S05; F11-S06]. |
| `aseptically_filled` | sterility is achieved by sterilizing filtration and/or component sterilization followed by aseptic assembly, with no validated sterilization of the sealed final container. A post-fill heat step that is a bioburden-reduction treatment rather than a validated sterilization cycle stays here, with the treatment recorded in a note. |
| `lyophilized` | aseptically filled into partially stoppered containers and freeze-dried [F11-S16]. Separate because its release vector carries residual moisture and cake inspection on top of the aseptic vector, and because no terminal route applies. |
| `unknown` | nothing above is supported at `weakly_inferred` or better, including the case where two lines contradict and neither is `established`. |

**Confidence ladder.** Applies to the determination, not to the source.

| level | requirement |
|---|---|
| `established` | an explicit route statement for **this** presentation-holder pair in a primary document of record: the sterility-assurance section of an approved application's chemistry review, an FDA establishment inspection report naming the cycle, an EPAR or national public assessment report quality section, a pharmacopoeial monograph directing the route, or label text making an affirmative route statement. A verbatim quote is required where the source is text. |
| `strongly_inferred` | no explicit statement, but **two or more independent lines** of primary evidence converge and no primary evidence contradicts. The row must name each line and state why it is independent of the others. |
| `weakly_inferred` | one line of indirect evidence, or converging lines that are not independent of each other. |
| `unknown` | below that. |

**Reconciliation with HA-34.** HA-34 states "Label text is not acceptable: it does not carry the route". That rule is about what labels *do*: no US or EU label reviewed across family 11 states the route, so silence in a label is not evidence in either direction. It is not a rule that an affirmative label statement would be worthless. A label affirmatively naming the sterilization method for that presentation reaches `established`; a silent label contributes nothing. A statement about the drug substance, a component or a diluent is not a statement about the drug product.

**Row contents.** Presentation, application holder and application number, determination, confidence, evidence (source id plus verbatim quote for text sources), falsifier, document date, and a `contradicted` flag.

---

## 3. Evidence hierarchy, and the ceiling each tier can reach

| tier | evidence | ceiling |
|---|---|---|
| E1 | approved-application chemistry review sterility-assurance section; FDA establishment inspection report naming the autoclave cycle; EPAR or national public assessment report quality section; pharmacopoeial monograph for the product directing the route | `established` |
| E2 | label, SmPC or product monograph text making an affirmative route statement for that presentation | `established` |
| E3 | the holder's own published technical statement about that presentation, or about the named platform the source says it is filled on | `strongly_inferred` |
| E4 | a patent held by that presentation's holder claiming the route for that formulation, linked to a marketed presentation | `strongly_inferred` |
| E5 | peer-reviewed or regulatory literature describing the route for the product class generally | `weakly_inferred` |
| E6 | reasoning from container type, excipient profile, pH, thermal-stability chemistry, F0 arithmetic, or the existence of an autoclavable competitor product | `weakly_inferred` |
| E7 | registration and listing metadata: SPL establishment business-operation codes (STERILIZE, NCI C84382), NDC and listing fields, Orange Book fields | **`unknown`, contributes leads only** |

**On E7, added 2026-09-06.** This class was not anticipated when the file was written and `evidence_01_labels_and_approvals.md` section 4 recommended adding it. A STERILIZE registration names an establishment performing a sterilization operation on a finished NDC. It does not name the modality and does not distinguish sterilization of the sealed final container from sterilization of components, containers or bulk, so it does not discriminate between any two of the five categories and cannot reach even `weakly_inferred` *for a category*. It is a lead-generation instrument. A row may cite it to say where to look; a row may never count it as one of the converging lines that `strongly_inferred` requires.

**Rules, non-negotiable.**

1. **Inference never reaches `established`.** The ceiling of the highest tier cited is the ceiling of the determination. Two E4 lines do not make an E1. No number of E6 lines beats `weakly_inferred`, because container, excipient, pH and stability are all consequences of the same formulation chemistry and are therefore not independent of one another.
2. **`established` requires text or a document of record, never a chain of reasoning.**
3. **Absence rule.** Silence in a label is not evidence. Never record "no route stated, therefore aseptic".
4. **Platform rule.** A statement that a platform is aseptic (E3) establishes the platform, not the presentation, unless the source names the presentation as being on that platform.
5. **Patent rule.** A granted claim shows a route was reduced to practice, not that any marketed product is made that way. A patent alone can never overturn an `established` determination.
6. **Contradiction rule.** Any primary evidence contradicting a determination drops it to `unknown` pending resolution. The contradiction is recorded in the row, not resolved by preference.
7. **Currency rule.** A route can change by supplement with no public trace. Every row carries the date of the document, not the date it was read.
8. **Quote rule.** Every text source carries a verbatim quote and a source id: `F11-Sxx`, or a snapshot id plus the file read, or a URL with an access date for anything newly fetched.

---

## 4. The decision the screen feeds

**If the determination is terminal (moist heat), at `established` or `strongly_inferred`.**

*What changes in the model, conditional on a parametric release approval.* `sterility_incubation_days` (14/14/18) goes to 0 for released batches; a new `sterility_sample_transit_days` for a node without its own sterility suite goes to 0; the pole becomes `max(EM, bioburden, assay, endotoxin) + serial QA`, 9 days at base against 16. `ProductFeatures.sterilization_route` (`src/telo_feasibility/product_architecture.py`) is set and a parametric-release `ReleaseScenario` becomes evaluable, which is what makes the route rules in `../design_space/product_architecture_matching.md` section 3.6 executable rather than aspirational.

*What parametric release would require.* All four systems FDA enumerates: sterilization process validation and control, verification by load monitors, a validated container-closure system, an effective quality system [F11-S02]. Filed as a prior approval supplement under 21 CFR 314.70, 601.12 or 514.8(b)(2), approved before implementation [F11-S02; F11-S03]. Specification and certificate of analysis amended to state that parametric release is used in lieu of sterility testing [F11-S46]. A written acknowledgement that a sterility test will not be used to overrule a parametric failure; the ratchet is one-way in both instruments [F11-S03; F11-S05 4.18].

*What stays, and what is added.* Stays: the full non-sterility release vector in section 1, plus per-batch bioburden and load-monitor review by two independent systems [F11-S04 10.4; F11-S05 4.17], both fixed quality cost per node. Added: an autoclave as a unit operation, with capital, footprint, cycle time and load scheduling, which is a capacity mechanism the model does not have; a different `G04` qualification programme (cycle validation, load mapping, biological indicator studies) in place of media fills [F11-S06; F11-S19]; and Annex 1's requirement of a sterility test per sub-batch for terminally sterilized product [F11-S04 10.6 note]. Whether per-load monitors satisfy the sub-batch rule under parametric release is **UNCERTAIN** and is a question for HA-31.

*The third state, which is not optional to model.* Terminal route **without** parametric release keeps the 14-day component, adds the autoclave, and adds the sub-batch multiplication. At small autoclave loads that is worse on release time and QC labour than aseptic fill. The screen's output must never be read as "terminal is better"; it decides only whether the parametric branch is reachable.

*The dating lever.* Set `bud_503b_days` from Table D as a lookup on route by test-completion by storage condition, not as a scalar [F11-S45]. Carry the status with the number: Table D is **revised draft guidance, nonbinding, not for implementation**, and it applies only inside the 503B state, which `../../CLAUDE.md` treats as time-varying and never a permanent pathway. It is not a lever for the approved-application architectures, where parametric release is the mechanism. Falsifier, already recorded in the parent prior-art note: a final version of the guidance that changes Table D removes it.

**If the determination is aseptic.** Nothing falls away. `sterility_incubation_days` stays at 14/14/18 and remains the argmax at every corner of the release box. Family 11 does not exist as an intervention for that presentation. The only remaining route to the pole is a validated rapid microbiological method under USP `<1223>`, which is a **method substitution, not a removal**: the test still exists, still gates release, and still has to finish [F11-S01 X.D; F11-S24]. Any RMM at or below 7 days delivers exactly the environmental-monitoring floor and no more, which is the result Novartis published: 14 days to a 5-day method gave a 7-day release [F11-S28]. Chemical release assurance under `G15` removes assay only, and assay sits under EM which sits under sterility, so it removes zero days. That answer does not depend on the determination; it is already the model's answer and the screen does not change it.

**If the determination is lyophilized.** The release vector lengthens (residual moisture, cake and meltback inspection) [F11-S16] and no terminal route applies. Excluded from family 11 by construction; acetazolamide is the declared out-of-archetype comparator in `config/longlist.yaml`.

**What the screen must not output.** Convertibility. "This aseptic product could be terminally sterilized" is a reformulation and container-qualification programme, not a determination. The screen records the current route and stops.

---

## 5. What the screen cannot do

1. **A route does not transfer between manufacturers.** Norepinephrine is the worked case: Baxter's premix is aseptically filled on a platform Baxter itself describes as aseptic-fill [F11-S33] and its FDA summary review confirms USP `<71>` release testing [F11-S20], while Sun Pharma holds US11197838B2, whose granted claim 1 reads "A ready to infuse stable parenteral dosage form consisting essentially of: a. norepinephrine or its pharmaceutically acceptable salt at a concentration ranging from 10 to 75 micrograms/ml of norepinephrine base; b. at least one sulfite antioxidant; c. at least one ion chelator; and d. sodium chloride, wherein the dosage form is an aqueous solution and was terminally sterilized by autoclaving" [F11-S32, fetched 2026-09-06]. Provenance correction, 2026-09-06: the sentence "an infusion container filled with an aqueous solution of norepinephrine ... wherein the said solution is stable and can be terminally sterilized by autoclaving", which this screen previously called a granted claim, is from the summary of the invention. Rule 5 below turns on that distinction. The claimed 10 to 75 micrograms/mL is an infusion concentration, so the patent does not speak to the 1 mg/mL vial at all. Same molecule, two routes. A molecule-level answer is wrong for both.
2. **A route does not transfer between presentations of one manufacturer.** Fill volume, container material, headspace and preservative status all change the thermal and container arguments.
   *Exception clause, added 2026-09-06 because the pass relied on one and had not written it down.* Several fill volumes of one strength under one application may be carried in a single row **only** as an explicitly declared load family: the row must name the NDCs, state that it is an assumption rather than a finding, and carry its own falsifier ("a showing that the largest fill is validated on a different cycle or line from the smallest").    `config/longlist.yaml` leaving a fill unfixed is a reason the study has no single fill to model. It is not evidence that the fills share a cycle. Where a row uses this clause it says so; `evidence_01_labels_and_approvals.md` limitation 7 is the general statement of the practice and is now governed by this clause.
3. **A negative is not a ceiling and a positive elsewhere is not a floor.** Sodium bicarbonate is the recorded negative: autoclaving at 121 C produced sodium dawsonite crystals from aluminium leached out of the glass vial [F11-S31]. That is a container and chemistry failure for one presentation, not a law about the molecule.
4. **Parametric release may be a per-site and per-autoclave asset, not a company-level one.** FDA's QbR FAQ conditions its abbreviated filing route on the *identical* facility, autoclave, container-closure system, critical process parameters and load patterns [F11-S46]. It does not address whether an approved programme extends to a second site, and no source read in family 11 settles it. If it does not travel, its cost scales with node count like replicated process validation, which reverses the economics of every multi-site design. The screen cannot resolve this. It is `prior_art_review.md` section 7 item 1 and belongs to HA-31.
5. **The document that would settle most rows is confidential to its holder**, so the person who can cite it is generally the person who may not. That is why HA-34 exists and why the expected modal determination is `unknown`. The count of unknowns is a result, not a failure of the search.
6. **The screen does not make the pole matter.** Even removed entirely, the sterility component is third order in the study's own ablation: it flips 4 of 16 cells and never ranks above 3rd of 17. Inventory alone (`bounds:ss365+base_stock`) reaches feasible in 11 of 16 cells with the hold fully intact on run `abl_post_R008`; the 13-of-16 figure this file previously carried is the pre-R004 run and is superseded. Both figures are superseded for quantitative use pending re-run.
7. **The 14-day figure is itself carried by a repository memo and vendor sources, not by a fetched copy of USP `<71>`**, which is paywalled (family 11 section 9). The arithmetic in section 1 inherits that weakness.

---

## 6. Falsification protocol

Every determination row carries its own falsifier. These are the category-level defaults; a row may state a narrower one, never a weaker one.

| determination and confidence | what overturns it | where it lands |
|---|---|---|
| any category at `established` | a later approval document, inspection record or label revision for the same presentation-holder naming a different route, or a supplement changing it | the new route, at the confidence its own evidence supports |
| any category at `established` | a showing that the quoted text refers to the drug substance, a component, a diluent, or a different presentation | `unknown` |
| `terminally_sterilized_moist_heat` at `strongly_inferred` | any single primary document stating the presentation is aseptically filled | `aseptically_filled` |
| `terminally_sterilized_moist_heat` at `strongly_inferred` | a showing that the converging lines are not independent, for example both tracing to one platform brochure | `weakly_inferred` |
| `terminally_sterilized_other` | a document naming moist heat instead | moist heat, and US parametric release becomes reachable where it was not [F11-S02] |
| `terminally_sterilized_other` | a document showing the modality is gas | unchanged category; parametric release unavailable in both US and EU [F11-S02; F11-S06] |
| `aseptically_filled` at `established` | an FDA review or inspection record naming a validated terminal cycle for that presentation. A patent alone does not overturn it | terminal, at `established` |
| `aseptically_filled` at `strongly_inferred` | evidence that the "aseptic" statement described a platform rather than this presentation | `unknown` |
| `lyophilized` | a document describing a ready-to-use solution presentation under the same application | the category applies per presentation, not per application; open a new row |
| `unknown` | E1 or E2 evidence closes it to `established`; E3 to E6 close it to `strongly_inferred` or `weakly_inferred` and never to `established` | as stated |

**Falsifiers for the screen as a whole.**

- A published mapping of shortage-list injectables to sterilization route, or an ANDA holder, CDMO or consultancy offering route conversion as a service, falsifies the unoccupied claim in `prior_art_review.md` section 6.1 and makes this screen a duplicate rather than a new asset.
- A primary source showing CPG 490.200 has been withdrawn, or that FDA no longer accepts the load-monitor substitution under 211.167(a), removes the decision the screen feeds [F11-S02].
- An FDA statement that an approved parametric release programme extends to a second site or autoclave without its own submission moves the mechanism from per-node to company-level and raises the screen's value; the opposite statement lowers it (section 5 item 4).
- A fetched copy of USP `<71>` reading other than "not less than 14 days" changes the arithmetic in section 1.

**Recording rule.** Falsification events are written into the determination row with their date. Counts by confidence level are reported before and after any revision. **No determination is ever silently upgraded**, and no row moves up the ladder without a new source id and a new quote.
