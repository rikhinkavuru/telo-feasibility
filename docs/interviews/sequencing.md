# Sequencing: what goes out first, and what waits

Written 2026-09-05. Companion to `target_matrix.md` (who), `outreach_templates.md` (what to send) and
`../reviewer_packets/README.md` section 1 (the packet gate, stated there in full).

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result named below is behaviour of the engine
under evidence tier 5 inputs. All sixteen regulatory gates are UNCERTAIN with no reviewer. Every row of
`target_matrix.md` reads "not contacted": zero interviews against a 25 to 30 target (DF18) and zero of three
independent reviews (DF19). Nothing here records a partnership, customer, pilot, review or regulatory opinion.

## 1. Settled by the founder before any outreach at all

Three decisions, not three pieces of work. Nothing below starts until each is recorded with a date in `DECISIONS.md`.

- **The revisions sign-off (HA-02, queue rank 4).** The thresholds (fill rate 0.99, tail confidence 0.90, shortage-day
  0.95, recovery window 30 days) and every protocol revision to date. The queue row names R000 to R008 because it was
  written before R009, R010 and R011 landed on 2026-09-05; the sign-off has to cover those three as well. DF01 fails
  until it exists. Signing after seeing results converts a pre-specified threshold into a chosen one, and every
  feasibility verdict an interviewer might quote is stated against tau 0.99 and q 0.90, with a feasible set that
  changes at 0.98.
- **The product decision (HA-03, rank 17).** Whether furosemide 10 mg/mL joins the longlist, and at which exact fill
  volume. Until it is decided, the only permitted answer to "which product is this about" is the C008 wording,
  beachhead under revision. An elicited demand or batch number for a presentation nobody has selected may enter no
  configuration at all, which wastes the conversation and the interviewee.
- **The contact-list relocation (HA-08, rank 3).** The lists move to `~/telo-private/`, with the ignore rules, the
  `.gitleaks.toml` rule and a pre-commit hook demonstrated to block a seeded address. Outreach generates more contact
  data than exists today, and the control that already failed was convention. HA-06 (visibility) and HA-07 (history)
  are ranks 1 and 2 and stand on their own; HA-08 is the one that has to be in place before new names arrive.

## 2. The distinction the rest of this note rests on

**Input interviews ask for facts about the world.** A demand denominator, a replenishment rule, a reservation fee, a
changeover time, a reporting category, a sterilization route. Their value does not depend on the model being right, on
the ranking being stable, or on any strategy id surviving. If every architecture in the battery were withdrawn
tomorrow, a real order-up-to level from a real stocking point would still be worth exactly what it was worth. That is
why they can start as soon as section 1 is settled, and why the field kit asks for numbers rather than for opinions
about architecture.

**Reviewer packets ask a qualified expert to attack the model.** Their value depends entirely on the model being the
one the author intends to defend. The protocol requires three completed reviews
(`protocol.yaml` `independent_review.minimum_completed`; DF19), the pool qualified to give one is small, and a review
is a much larger ask than a call. Sending a comparison whose defects are already written down in the author's own
register spends that goodwill on findings that are already in the file, and it invites a reviewer to argue with a
result that is going to be withdrawn anyway.

## 3. What gates the packets

Both conditions in `../reviewer_packets/README.md` section 1 have to hold.

**(a) The defects that carry the ranking are fixed. This condition is met.** NEW-1 (opening inventory seeded free of charge, scaling with the
design's own stock policy), MD-3 (the hard-coded regional review rule), MD-12 (search spaces not matched across
architectures), MD-11 (optimizer tie-break with no Monte Carlo standard error tolerance), MD-1 (material order-up-to
level coupled to the lead time, so cutting a lead cuts the buffer), NEW-2 (allocation rights inert), MD-23 (exercise
cadence nearly unmeasurable on a frequently activated line) and MD-24 (take-or-pay with no service channel).
Revisions R009, R010 and R011, all dated 2026-09-05, land every one of those in code. NEW-3 (no readiness-decay
hazard) is not addressed by them and stays open, as does MD-15 (one product per network), the largest unquantified
distortion in the cost comparison. Both belong in the packet as stated limits rather than as surprises.

**(b) The battery is re-run on the fixed engine and every number in the packets is replaced.** Optimize, simulate,
ablate, design-space, matched-space, figures, contract table. This condition is not met today, and it is now the only
thing holding the packets. A post-fix paired simulation does exist: `results/simulation/sim_post_R009/`, manifest
2026-09-06T03:02:03Z, 20 strategies, both products, n = 100, at the illustrative baseline designs. Everything else is
still pre-R009. The newest design-space artifacts are `results/design_space/ds_post_R008/` and `matched_20260905.json`,
and `results/optimization/opt_20260906T032432Z/` is an empty directory with that run still in flight. Until a
completed post-R011 optimization and the battery that hangs off it exist, every number a reviewer would receive is a
pre-R009 number.

Check `results/manifests/` for a run dated after the fixes and confirm `make check` is green before anything is sent.

## 4. Order of contact for the input interviews

**Wave 1, immediately after section 1.** The demand-analytics owner and the regional stocking planner, HA-11a and
HA-40, the top two interview-closable items in the queue. One pool carries both: hospital pharmacy, IDN supply chain,
GPO and wholesaler. HA-11a can end the preferred shape outright, since a denominator above the architecture's ceiling
removes it, so it is worth knowing before anyone spends time on cost. **HA-11b, the installed capacity serving the
presentation, is not in this wave and is not an interview at all**: it is an evidence-acquisition task against FDA
establishment registration and drug listing, the ANDA and RLD holder set, DQSA section 506C notifications or a
commercial data vendor (`target_matrix.md` section 3a). It can run in parallel with everything else, because it
consumes no interview slot.

**Wave 1b, in parallel.** The operations researcher or reliability engineer holding multi-site event data, HA-39. It
touches no other pool, so it costs nothing to run alongside wave 1.

**Wave 2.** Sterile manufacturing and process engineers, fill-finish engineering vendors, a CDMO commercial lead:
HA-21 and HA-13. Every absolute cost in the package is scaffold until these land, so this wave is what makes any cost
sentence sayable. Vendor quotations are documents, not interviews, and are counted separately.

**Wave 3.** The purchaser with signing authority: HA-38 first, then HA-36 and HA-24. Run `modules/purchaser.md`,
which exists as of 2026-09-06 and asks them in that order; HA-38 changes what a price answer means, so it cannot be
appended to a price question. After wave 2, because the question is what a real agreement costs and covers, and
arriving without a batch, campaign and fee vocabulary wastes the role with the shortest patience. It is also the role
that can end the commercial case in one sentence.

**Wave 4.** Generic-drug and 503B regulatory, CMC: HA-23, and the part of HA-34 a person can answer. HA-34 is a
document task first: fetch the reference product's Drugs@FDA chemistry review, an establishment inspection report and
the USP monograph before asking anyone, and then ask only about products they have personally worked on
(`modules/quality_cmc.md` question 2). Deliberately last among input interviews, because this pool is also the
reviewer pool for HA-31. Decide before contacting a person whether they are an input source or a
reviewer, and do not spend the same person twice: HA-23 is one category question answerable in a call, HA-31 is
sixteen gate statuses in writing with qualification, rationale and date.

The same overlap runs through wave 1 and reviewer HA-33, and wave 2 and reviewer HA-30. Where one person could serve
either role, the reviewer ask is the larger one, is made once, and is made only after section 3 clears.

## 5. The packets themselves

Four exist and none is sent: manufacturing and quality, regulatory, operations research, hospital and GPO. Three
completed reviews satisfy the protocol; the fourth is optional. Send them together rather than staggered, so every
reviewer attacks the same run, and log each under `../reviewer_packets/reviews/` with qualification, issues raised,
decisions taken and the model change that followed. A logo or a quote is not validation, and no reviewer becomes an
advisor, endorser or partner by reviewing.
