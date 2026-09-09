# Elicitation worksheet

A working document for use during a live conversation, not a form to fill in afterwards. It holds the scripts, the
card, and the five rules that decide whether forty-five minutes of someone's time turns into evidence: ask for a range
before a number, keep disagreement instead of averaging it, log the tier the answer actually earns, mark anything
that contradicts a frozen snapshot, and close by asking what they would attack first.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** No interview has been held. Model behaviour named in the
interviewer-only sections is behaviour under evidence tier 5 (illustrative) inputs and describes the model, not
sterile-injectable manufacturing. Nothing here asserts a regulatory position, a partner, a customer or a review.

**What may be shown to the interviewee:** section 5's blank card, and the parameter definition and units from
section 11. **Interviewer only:** everything else, in particular the "what it can reverse" column, which quotes
model results that may not leave this repository.

---

## 1. Before the call, five minutes

1. Assign the interview id now, format `INT-YYYY-NNN`, and write it at the top of the page. The record will live at
   `data/interview_evidence/<id>.json`.
2. Choose at most five parameter cards, from section 11, ordered by decision value. A sixth answer in a
   forty-five-minute call is worse than no answer, because it will be rushed and will still be logged.
3. Blank the study's own low, base and high on every card. They are shown only after the person's first answer
   (section 3, rule A1).
4. Have the person's role module open (`modules/*.md`) and the closing question written out (section 9).
5. Check the do-not-show list (section 12) against whatever is on your screen.

**Consent, before anything else.** Role, organization type, years of directly relevant experience, whether the
conversation may be recorded, whether quotes may be used, and whether attribution is by role only or by name.
Default is role only. Nobody becomes a partner, advisor, validator or reviewer here, and saying so out loud at the
start makes the rest of the call easier.

## 2. The forty-five minutes: the one published timetable

**This table is the only timetable in the package.** The email asks for forty-five minutes, `guide_core.md` is
titled for forty-five, and every module's `Length:` line is the whole call rather than a tail after the core guide.
Three documents used to carry three different budgets for the same slot, which is how a thirty-minute ask became a
fifty-to-sixty-minute instrument.

| Minutes | What happens |
|---|---|
| 0-4 | Consent, interview id, attribution, recording. Who you are and who you work for, in one sentence (`guide_core.md` section 2) |
| 4-7 | The opening statement: the model was built to test whether distributed capacity beats the alternatives, it says no, every input behind that no is a placeholder, and you are here to find out which half is wrong |
| 7-12 | **The two questions asked of everyone** (`guide_core.md` section 4, rows 1 and 2). What actually stops supply from responding first; which number from their own domain is furthest from reality |
| 12-32 | Three to five parameter cards, using the range script in section 3, run inside the role module |
| 32-40 | The rest of the role module probes |
| 40-45 | The close (section 9), both parts; permission for one follow-up; one sentence on where their answers go |

A sixth parameter card in a forty-five-minute call is worse than no answer, because it will be rushed and will still
be logged. The one fixed part is the close: the last five minutes belong to section 9 whatever else was cut.

Two standing rules for the whole call. Do not correct the interviewee, even when they are wrong about what the model
does; note it and handle it in the follow-up email. Do not defend an assumption while they are attacking it, because
the attack is the deliverable.

## 3. Asking for a range rather than a number

The order matters more than the wording. Asking the middle first pulls the ends toward it, and showing our numbers
first pulls everything toward ours.

**A1. Units and entity level first.** "Before the number: per site or per network, per year or per batch, and for
which presentation?" A range against the wrong entity level is not a wide answer, it is a wrong one, and most
apparent disagreement between two experts turns out to be this (section 7, rule D2).

**A2. High end.** "What is the highest it could plausibly be?"

**A3. Low end, middle, and the confidence.** "What is the lowest it could plausibly be?" Then: "What is your best
guess?" Then: **"How confident are you, as a percentage, that the truth lies between your low and your high?"**
Record that percentage in `claims[].range_confidence_pct`.

*Why the wording changed.* The script used to ask for "a value you would be surprised to see exceeded, say once in
ten years" and the card then recorded the answer as the 90th percentile. Those are different objects: an exceedance
frequency is not a quantile of the quantity, and the gap is largest for exactly the parameter that matters most, a
rare multi-site event rate (`common_cause_events_per_year`, base 0.1 over 0.02 to 0.3, where "once in ten years" and
"the 90th percentile" are not the same number). Asking for the bounds and then asking how much of the mass they think
sits inside them records what was actually elicited, and lets two ranges given at different confidences be put on one
scale before either enters a sweep.

**A4. Widen once.** "What would have to be true for the real number to sit outside the range you just gave me?" If
they answer easily and plausibly, the range is too narrow: go back to A2 and A3 with what they just said, and set
`claims[].widened` true. Do this once, not twice.

**A5. Only now, show ours.** "Mine says low X, base Y, high Z. What would have to be true for that to be right?"
Record their reaction in `claims[].our_range_reaction`, and record whether they moved.

**A6. Direction.** "What makes it higher in practice, and what makes it lower?" Two fields,
`claims[].direction_higher` and `claims[].direction_lower`. The conditioning variable is often worth more than the
number.

**When they refuse a range.** Record the point estimate as the base, then ask A2 and A3 once more as "highest
plausible" and "lowest plausible". If they still refuse, log the point with `confidence: "low"` and the rationale
"point estimate offered, range declined". Do not invent bounds around a point. An invented bound is indistinguishable
from evidence three months later.

**When the answer is "it depends".** That is the best answer in the file. Write the conditioning variable down as its
own line, ask for the range under each condition, and flag it in `follow_up` as a possible structural sensitivity
rather than a single input.

**When the number arrives instantly and round.** "About twenty percent" given in half a second is a heuristic, not a
measurement. Ask what it is a fraction of, and over what reference class, and record the answer to that question as
part of the rationale. If the reference class does not exist, the tier drops (section 6, rule T4).

**Never.** Do not offer a number and ask them to confirm it. Do not read out another interviewee's range. Do not ask
a question whose answer requires them to speculate outside their own work; if it does, that is a different person's
question, and the queue in `../audits/07_human_action_queue.md` says whose.

## 4. Naming where the answer goes

Say it out loud, per parameter, in one sentence: the field it lands in, and the result it can move. "That number goes
into the demand file and it decides whether the capacity shortage the model assumes is real at all." This is a rule,
not a courtesy. A question whose model entry point cannot be named in one sentence should not be asked, because
nothing will be done with the answer.

## 5. The parameter card

One card per parameter. Every row has its own field in `evidence_log_schema.json`, so transcription is mechanical
rather than interpretive. Nine fields were added to the schema on 2026-09-06 for exactly this reason: five card rows
used to collapse into free-text `rationale`, one row had no field at all, and the tier-4 test named a field the
schema did not carry.

| Field | Entry | Schema target |
|---|---|---|
| parameter_id | | `claims[].parameter_id` |
| definition read aloud, in their words back to you | | `claims[].parameter_definition_readback` |
| units confirmed (A1) | | `claims[].units` |
| entity level confirmed (A1: site, network, batch, event, year, group, supplier, order) | | `claims[].entity_level` |
| lowest plausible (A3) | | `claims[].low` |
| best guess (A3) | | `claims[].base` |
| highest plausible (A2) | | `claims[].high` |
| confidence that the truth lies between low and high, as a percentage (A3) | | `claims[].range_confidence_pct` |
| widened after A4? | | `claims[].widened`, and what moved in `claims[].rationale` |
| our low/base/high, shown at A5, and their reaction | | `claims[].our_range_reaction` |
| what makes it higher (A6) | | `claims[].direction_higher` |
| what makes it lower (A6) | | `claims[].direction_lower` |
| confidence, high / medium / low, and why | | `claims[].confidence` |
| basis: personally observed / read in a document / impression | | `claims[].basis`, which drives the tier, section 6 |
| rationale, verbatim | | `claims[].rationale` |
| disagreement, or "no other interviewee has answered this yet" | | `claims[].disagreement` |
| contradicts: snapshot, interview or claim tokens | | `claims[].contradicts` |
| the closing attack on this parameter, if there was one | | `claims[].challenge` |
| document they could share | | `documents_provided` |
| model change, or the reason for none | | `claims[].model_change`, `code_change`, `revision_id` |
| open thread | | `claims[].follow_up` |

`parameter_definition_readback` and `challenge` are two different things and used to share one field. The readback is
the definition in their words at the start of the card; the challenge is the attack at the close (section 9, rule
C2). A claim row opened by the close carries `challenge` with `low`, `base` and `high` null, and `n/a` in `units` and
`entity_level`.

Verbatim means verbatim. A paraphrased rationale cannot be audited later, and the rationale is usually the part that
changes the model.

## 6. The evidence tier the answer earns

Tiers are defined in `protocol/protocol.yaml` `evidence_tiers`. The tier is a property of the evidence, never of the
person's seniority.

| Tier | What earns it here |
|---|---|
| 1 | An official record they point us to, after **we** fetch it and it enters `data/raw_snapshots/` with its date. Their pointer is not tier 1; the snapshot is. |
| 2 | A document, extract or record they actually hand over, with terms written down. |
| 3 | Peer-reviewed empirical work they name, once read. |
| 4 | Qualified expert elicitation, with all five required fields present: role, experience, confidence, rationale, disagreement. The protocol names those five (`protocol/protocol.yaml` `evidence_tiers`); in the record, role and experience are the top-level `role_category` and `relevant_experience_years`, and `disagreement` is the `claims[].disagreement` field added to the schema on 2026-09-06, always paired with a `contradicts` token on both records (rule D3). |
| 5 | Everything else, including anything below. |

**T1.** A tier-4 record missing any one of the five required fields logs at tier 5 until the missing field is
obtained. The protocol's five are role, experience, confidence, rationale and disagreement; in the record they are
`role_category`, `relevant_experience_years`, `claims[].confidence`, `claims[].rationale` and
`claims[].disagreement`. Absence of disagreement is a valid entry ("no other interviewee has answered this yet"); a
blank is not. Every substantive disagreement recorded in that field is also recorded as a `contradicts` token on
both records, per rule D3, because the field carries the substance and the token makes it greppable.

**T2.** An answer outside the person's own direct experience stays tier 5 no matter who gives it. Ask plainly: "have
you seen this number yourself, or is it an impression from the market?" Record the answer in the basis field. Senior
people give confident answers about neighbouring domains and those answers are worth exactly tier 5.

**T3.** A number recalled from a document they cannot share is tier 4 with confidence at most medium. It is not tier
2. Tier 2 needs the document. If they read it aloud from the file during the call, it is still tier 4, and it opens a
`follow_up` asking whether the document can be shared and under what terms.

**T4.** A round number with no reference class behind it (section 3) logs at tier 5 with the rationale recording that
the reference class was asked for and not available.

**T5.** No tier is ever upgraded without a new artifact. Two people saying the same thing does not make either
statement tier 3; it makes a stronger tier-4 pair, which is recorded as agreement, not as a promotion.

**T6.** Every value that replaces a tier-5 placeholder needs its parameter record updated in full: value, tier,
`source_ids` including the interview id, `access_date`, `confidence`, `validation_status`, and
`outputs_it_can_reverse`. Then `revision_workflow.md`.

## 7. Disagreement between two experts

The instruction is simple and it is violated by accident: **never average, never pick, never quietly drop the
outlier.**

**D1. Both survive as separate rows.** Each interviewee's claim stays under their own interview id with their own
range and rationale. Nothing is merged. The synthesis reports "n of m interviewees; the ranges were X and Y", not a
mean.

**D2. Test for a definitions problem first.** Non-overlapping ranges are more often a units, entity-level or
time-basis mismatch than a substantive conflict: per site against per network, per batch against per year, nominal
against realized, one presentation against a class. Check A1 for both records before recording a substantive
disagreement. If it is a definitions problem, the finding is that the parameter is ambiguously defined, and the fix
is to the definition, not to the number.

**D3. Record it on both sides.** Write the substance into `claims[].disagreement` on each record, and add a
`contradicts` token to each naming the other: `interview:INT-2026-004#common_cause_events_per_year`. A disagreement
recorded on only one side disappears the moment that record is superseded.

**D4. Widen, then declare.** The parameter's low and high widen to cover the union of both ranges. If the union
brackets a threshold crossing in `../design_space/feasibility_regions.md`, the disagreement is decision-relevant: it
becomes a declared structural sensitivity, every affected result is reported under both readings, and no ranking that
flips between them is quoted anywhere.

**D5. Escalate rather than adjudicate.** When a disagreement is decision-relevant, the resolution is a third
qualified interviewee or a document, not the interviewer's judgment. Open the queue row and say so in the record.

**D6. Say so on the call.** "Someone else in your role gave me a different range, and I am keeping both." Never name
them, never quote their number, and never invite a reconciliation on the spot. The other person is not there to
defend their answer.

## 8. When an answer contradicts a frozen snapshot

Frozen snapshots live under `data/raw_snapshots/<source_id>/<date>/<file>` and are registered in
`config/sources.yaml`. They are the study's tier-1 and tier-2 record. A live answer that conflicts with one is
valuable and is also the easiest thing in this process to get wrong.

**S1. Do not correct them on the call, and do not discard the answer.** Both reflexes destroy the information. Ask
one neutral question instead: "the record I have says something different, can I read it to you and get your
reading?" Then record both.

**S2. Mark it on the card.** `contradicts` token format, so the strings are greppable:

- snapshot: `snapshot:S07/2026-09-01/fda_aseptic_processing_2004.pdf`
- another interview: `interview:INT-2026-004#parameter_id`
- a claim-register row: `claim:C009`

Record with it the exact snapshot line or value, and their statement verbatim.

**S3. Assign one of four dispositions, and do not resolve it on the call.**

| Disposition | What it means | What happens next |
|---|---|---|
| `snapshot_stale` | Their operational present postdates the snapshot | Re-fetch the source, new dated snapshot, keep both |
| `our_extraction_wrong` | The snapshot is fine and our reading of it is not | Correct the extraction, and check every document that cites it |
| `different_object` | They are describing a neighbouring thing: another presentation, another site class, another legal status | Fix the question, not the number |
| `genuine_conflict` | Both stand as recorded | Queue row, and a declared uncertainty until a third source settles it |

**S4. `our_extraction_wrong` is not hypothetical.** `CLAIMS_REGISTER.csv` C025 is exactly that case: an internal
memo attributed a sentence to a section of the 2004 FDA aseptic processing guidance, the frozen snapshot S07 was
extracted, and the sentence is not there and the section says close to the opposite. Assume the person may be right
about our reading of our own source.

**S5. A live answer never overwrites a snapshot.** A tier-4 statement does not replace a tier-1 record. It opens the
re-check. If the re-check confirms the interviewee, the snapshot is superseded by a new dated snapshot and the
supersession is logged; the old one stays on disk.

**S6. Contradicting a model result is not this.** Model results are tier-5 behaviour, not records. If someone says
the model's conclusion is wrong, that is section 9, not section 8.

## 9. The close: which single assumption would you attack first

Ask it last, ask it once, then stop talking and write.

> "Last question, and it is the one I most want. Of everything I have described, which single assumption would you
> attack first, and what would you use instead?"

Then, only after they have finished:

> "What evidence would settle that, and who holds it?"

**C1. Do not defend the assumption.** If they have misunderstood what the model does, note it and correct it in the
follow-up email. Arguing converts the most valuable ninety seconds of the call into a debate about the interviewer.

**C2. Verbatim, into `notes`.** If the attack names a parameter, it also opens a claim row with `challenge` filled
and `low`, `base` and `high` null, so it is visible in the record even though it carries no number.

**C3. Log repeats.** Record it even when three people have already said the same thing. Repetition across independent
interviewees is the only convergence signal available while n is small, and it is lost if the fourth is not written
down.

**C4. An attack on something the model does not contain is a finding.** It becomes a `follow_up` and a candidate row
in the model-defect register (`../design_space/bottleneck_decomposition.md` section 7) or in the human-action queue.
Several entries in those registers exist because the model was silent where it should not have been, including an
allocation right that is inert everywhere and a contract coupling with no service channel.

**C5. Close the loop out loud.** One sentence: where their answers go, what result they can move, and that they will
see the record before anything is published. They gave up forty-five minutes; they are owed the knowledge that it did
something.

## 10. Within twenty-four hours

1. Transcribe into `data/interview_evidence/<id>.json` against `evidence_log_schema.json`, with
   `status: "pending_confirmation"`. The parameter cards transcribe field by field; nothing is summarized.
2. Send the record, or the part of it that quotes them, back to the interviewee for correction. Do this before any
   model change, not after. Promote to `status: "complete"` on their reply, or after a stated wait of ten working
   days recorded in `notes`. **DF18 counts records at `complete` only**, so a record that has not been back to the
   interviewee does not yet count as an interview.
3. Run `revision_workflow.md`: accept, partial or reject per claim with a one-line rationale, then the parameter
   record, then `protocol/revisions.csv` if it is decision-relevant, then `make check` and the affected analysis.
4. Update `target_matrix.md` status and, if the interview closed or opened one, the row in
   `../audits/07_human_action_queue.md`.
5. If the answer moved a result, say which one and by how much in the revision row. If it moved nothing, say that
   too; a well-run interview that changes no number is still evidence about the parameter's confidence.

## 11. Priority parameter cards, by role (interviewer only)

Ordered by decision value from `../audits/07_human_action_queue.md` section 1. The right column quotes model
behaviour under illustrative inputs and is not shown to the interviewee.

| Queue | Parameter or field | Units, entity level | Where it enters | What it can reverse |
|---|---|---|---|---|
| HA-11a | `product.annual_demand_units`, regional shares | units/year, national and regional | `config/products/*.yaml`, then `demand.py` and the deterministic screen | 46 of 138 threshold crossings; the only axis whose reversal map has a region where nothing qualifies; whether the capacity mode exists at all. **HA-11b, the installed capacity serving the presentation, is not a card**: no interviewee on the demand side holds it, and it is an evidence-acquisition task (`target_matrix.md` section 3a) |
| HA-40 | `region_base_stock`, `region_reorder_point_days`, review frequency | days, per stocking point | region policy block in `strategies.build_strategy` | 8 of 16 Phase A cells at +0.82% cost; closes MD-3, the largest Phase A artifact |
| HA-13 | `capital_usd_per_site`, fixed operations, validation, `reserved_capacity_fee_fraction`, `node_commissioning_days`, `capacity_expansion_days` | USD, days, per site | `config/products/*.yaml`, `config/strategies/design_space.yaml` | fixed and resilience cost is 81.0% to 93.7% of annual cost for all eight comparators, so every absolute cost is a statement about the scaffold |
| HA-21 | `units_per_batch`, `batches_per_site_year_nominal`, `uptime_fraction`, `product.changeover_days`, deviation restart | units, per site-year, days | `config/products/*.yaml`, `production.py` | 20 crossings on changeover; three of the five strategies feasible on both products lose the target inside 6.5 days |
| HA-36, HA-24 | the nine `ContractTerms` fields, `price_required_usd_per_unit` | USD/unit, years, units committed | `contracting.contract_requirement` | every design reads "not contractable, stated"; five of thirteen service-feasible cells move to commercially impossible across the price range |
| HA-38 | availability payment: annual amount, response time, activation condition | USD/year | no field exists yet; reservation fee and take-or-pay ledger in `simulation.step8_costs` | the capacity leg of every capacity-carrying design; recorded fallback is "assume no" |
| HA-23, HA-31 | G07 reporting category; status for all sixteen gates with a named reviewer and date | category, status | `config/regulatory_gates.yaml`, `regulatory.evaluate_strategy` | DF08 and every decision class; a prior approval supplement with preapproval inspection removes S12's 365-day leg |
| HA-39 | `common_cause_events_per_year`, `common_cause_duration_days`, `common_cause_capacity_impact` | per year, days, fraction | `disruptions.py`, common-cause groups in `strategies.build_strategy` | 20 crossings; across the declared range the feasible set collapses on both products |
| HA-34 | `ProductFeatures.sterilization_route`, and the cycle if terminal | categorical | a product-level route attribute plus a parametric-release scenario | whether the 14-day pole is a constant or a design variable; the enabling input for the only intervention found that acts on the binding release constraint |
| HA-43 | `backorder_window_days` | days, per order | `simulation.step5_serve` | the fill-rate metric definition itself; MD-5 records its effect as non-monotone |
| HA-22 | `sterility_incubation_days`, `environmental_monitoring_days`, `assay_days`, `endotoxin_days`, `qa_review_days`, `deviation_rate_per_batch`, `investigation_duration_days`, `validation_factor`, `wrong_release_cost_usd` | days, per batch, USD | `quality.py`, `config/global.yaml`, `release_benchmark.cost_parameters` | the release decomposition; the sign of the release-benchmark cost curve |
| HA-42 | one quality unit across registered sites; what each site must still hold | categorical | the architecture incompatibility set | whether any multi-site design is legally available at all |
| HA-41 | decision to first released batch, split four ways | days | `node_commissioning_days`, `capacity_expansion_days` | MD-17, three commissioning parameters colliding with the warm-up boundary |

## 12. What never goes on a card

- A number the interviewee did not say. Not an interpolation, not a rounding, not a bound inferred from their tone.
- Our low, base or high before their first answer.
- Another interviewee's range, name or organization.
- A leading question, or a number offered for confirmation.
- A quote from the claims register's contradicted rows, C009, C010, C015 or C025, in any form, including as a premise
  in a question.
- Any wording that pairs the software with automating, certifying or replacing a release decision. Abstention is
  never release.
- Anything that would let a reader infer that a partner, customer, pilot, review or regulatory opinion exists,
  because none does.
