# Core interview guide (45 minutes)

Rewritten 2026-09-05; length and question set corrected 2026-09-06. Use with `elicitation_worksheet.md` for
ranges and the one published timetable, the role module in `modules/`, and `revision_workflow.md` for what
happens afterwards.

**Forty-five minutes is the ask, in the email and here.** The previous version asked for thirty and ran fifty to
sixty, because three documents carried three different budgets for the same slot. The single timetable is
`elicitation_worksheet.md` section 2, and every module's `Length:` line is now the whole call, not a tail after
this guide.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Everything this guide asks you to describe is the behaviour
of a model under evidence tier 5 inputs: 87 of 91 parameters are illustrative. Nothing in it is a finding about
sterile-injectable manufacturing, and nothing in it is legal or regulatory advice. All sixteen regulatory gates are
UNCERTAIN with no reviewer, so no architecture is presented as permitted. No interview has been held.

---

## 1. What changed in this guide, and why

The previous version opened by saying the study asks whether regional sterile-injectable capacity can beat safety
stock, dual sourcing or reserved contract capacity. Under the inputs now in the model, that question has an answer, so
opening with it asks people to settle something already settled and collects opinions where the study is short of
numbers.

The answer, stated the way it should be stated out loud: owned distributed nodes "meet the target in no region of any
recorded range on either product" (`../design_space/feasibility_regions.md` section 6, family 1),
and giving them the same inventory freedom that makes the alternatives feasible does not rescue them (same file,
section 8). What the model prefers is a shape rather than a strategy: buy or contract aseptic capacity that is already
registered and inspected, position a deep finished-goods tier, sell units
(`../design_space/strategic_synthesis.md`, answer to the governing objective).

Say the qualifications out loud too. An experienced person will guess at most of them anyway, and the study is worth
more if they are on the table. The engine seeds opening inventory free of charge (NEW-1), which flatters every
inventory-led design. The regional review rule is hard-coded and decides 8 of 16 Phase A cells (MD-3). The
search spaces were not matched across architectures (MD-12), and when four comparators were re-optimized over one
common inventory space, "Added central capacity meets it for both products once it is searched over the same
inventory space", cutting the gap to "a third, not an order of magnitude"
(`../design_space/feasibility_regions.md` section 8).

The rejection framing is kept, because it is the strongest thing in the old guide. No interview has been held, so
nothing in this file has been tested in use. The person is asked to reject, not to approve.

---

## 2. The frame, said out loud (about 90 seconds)

Say this, or something close to it, in your own words. Do not improve it into a pitch.

> This is a pre-registered feasibility study of sterile-injectable shortage response. It was built to ask whether
> regional production capacity can beat safety stock, dual sourcing, reserved contract capacity or simply adding
> capacity at an existing plant. Under the numbers currently in the model it does not, in any range I have recorded.
> What the model prefers instead is dull: contract capacity that is already registered and already inspected, hold a
> deep positioned stock of finished goods, and sell units.
>
> The reason I am not asking you whether you agree with that is that almost every number behind it is illustrative.
> Eighty-seven of ninety-one inputs are placeholders I wrote to make the engine run, and they are marked as
> placeholders. So the model is a tested scaffold with placeholder inputs, and my job today is to take your numbers
> instead of mine, and to find out what the model has wrong.
>
> I should say who I am before I ask you anything. I am [name], and I work on software in development for sterile
> drug manufacturing, a release-decision support layer. This is research, there is nothing to buy or sell here, and
> I am telling you the affiliation up front because I am about to ask you about your own line economics.
>
> Nothing about this conversation is a partnership, an endorsement, a pilot, a customer relationship or a regulatory
> opinion, and I will not describe it as any of those. You will be cited by role and organization type only, unless
> you tell me in writing that I may use more. I am not selling anything and there is nothing to buy.

The affiliation sentence is not optional and is not softened. Its wording is the `allowed_external_wording` column
of `CLAIMS_REGISTER.csv` row C015, quoted exactly, and it may never be paired with "automates the release decision"
(C010). Templates D, E and F reach process engineers, CDMO commercial leads and quality staff at firms that are
potential suppliers or competitors, and asking those people for installed capital, reservation pricing and deviation
rates without naming the affiliation is a material omission.

If the person is a purchaser with signing authority, add: I am not asking for a commitment, an intent or a term sheet,
and I have nothing to supply. I want to know what a real agreement of this kind looks like and what it would cost.

---

## 3. Why you are asking to be rejected

Say it plainly: the most useful forty-five minutes are the ones where something breaks. There are four things available to
reject, and it helps to name them.

1. **A number.** Any input in the person's domain. A range beats a point estimate, and a range with a reason beats a
   range.
2. **A mechanism.** Something the engine does not represent at all, or represents backwards.
3. **The shape.** Contracted registered capacity plus positioned stock. Why it fails in practice.
4. **The question.** That the study is asking about the wrong thing entirely.

Say that the model has already been wrong once in a way that changed its own answer, and quote it: "One statement
made earlier in this session is wrong and is corrected here: it is not true that no frozen comparator meets the
frozen target" (`../design_space/feasibility_regions.md` section 8). It costs nothing to say, it is true, and it shows
that a disagreement gets written down rather than argued with.

---

## 4. The three questions asked of everyone

Only three things are universal: two questions at the front and the close at the end. Each names where its answer
enters the model, and each is answerable by any qualified interviewee without access to anything they do not have.
Everything else belongs to a role module, because it is not answerable by most roles.

| # | Question | Where the answer enters |
|---|---|---|
| 1 | During a shortage, what actually stops supply from responding first, and what gets blamed incorrectly? | Which constraint the engine has to carry at all. A mechanism named here that the engine lacks becomes a model-defect register entry (`../design_space/bottleneck_decomposition.md` section 7) or a new comparator id, not a parameter change |
| 2 | Which number from your own domain is furthest from reality in this study, and what range would you use instead? Give me your range before I show you mine. | The named parameter record: value, tier 4, `source_ids` including the interview id, via `elicitation_worksheet.md`. A `protocol/revisions.csv` row if it is decision-relevant |
| 3 | The close, section 9 of `elicitation_worksheet.md`, in two parts. "Which single assumption would you attack first, and what would you use instead?" Then: "If that conclusion held, what would change in your own work, and what would you need to see before changing it?" | No parameter. Part one opens a claim row with `challenge` filled and no numbers, or a model-defect row. Part two tests whether the study answers a decision anyone actually makes |

**Where the other three went, and why.** The previous version declared six questions universal. Three of them were
not answerable by most roles, and one of those read as sales qualification.

- **"What makes the preferred shape fail in practice?"** moved into the modules that can answer it, and it names a
  mechanism rather than a preference. If it names a mechanism no configured design carries, it becomes a row in
  `../design_space/falsification_register.csv` and, if it needs a new architecture, the one free strategy id, S20.
  S20 is the last id `schemas.StrategyId` admits; a second new architecture needs the enum extended under a protocol
  revision.
- **"Which nominally separate sites, suppliers or lanes fail together, at what rate, for how long, losing what
  fraction of capacity?"** moved verbatim into `modules/operations_research.md`, where questions 1 and 2 already ask
  it. It is HA-39, and `sequencing.md` wave 1b routes it to one role: the operations researcher or reliability
  engineer holding multi-site event data. A microbiologist cannot answer it and should not be asked.
- **"What cost, elapsed time or compliance activity do outsiders leave out?"** moved into
  `modules/manufacturing.md` and `modules/quality_cmc.md`, which already ask for the specific costs and lead times
  (HA-13, HA-21, HA-41) rather than for the category.
- **"Who would have to pay for it, and out of which budget?"** moved into `modules/purchaser.md` and template C only.
  Asked of a microbiologist or a process engineer it is a question about somebody else's authority, and asked of a
  purchaser it is HA-38, which is the single answer this package most wants. It is not asked in passing.

Then the role module. `modules/hospital_gpo.md`, `modules/manufacturing.md`, `modules/quality_cmc.md`,
`modules/regulatory.md`, `modules/distribution.md`, `modules/operations_research.md`, `modules/purchaser.md`. Each
module declares its own length, and that length is the whole call rather than a tail after this guide. The module
carries most of the conversation; run the parameter cards inside it, per `elicitation_worksheet.md` section 2.

A note on the earlier citation. This file used to attribute these questions to "protocol Appendix D questions 38-43".
No Appendix D exists in `protocol/protocol.yaml`, and the pointer resolves to nothing. The questions are the study's
own and are cited as such here. `README.md` in this directory carried the same pointer and was corrected in the same
pass.

---

## 5. The seven numbers this study is short of

Ask only what the person can answer. This is the priority order from
`../design_space/strategic_synthesis.md` section 11 and the ranked queue in `../audits/07_human_action_queue.md`.
Walking away with one of these, as a range with a reason, is a successful interview.

1. **True annual demand for the exact presentation.** HA-11a. Enters `config/products/*.yaml`, then `demand.py`. It
   accounts for 46 of 138 crossings and is the only axis whose reversal map has a region where nothing qualifies.
   *The installed capacity that serves the presentation is HA-11b and is not an interview question.* A hospital, IDN
   or GPO analytics owner holds purchase history; installed aseptic capacity per presentation sits with
   manufacturers, with FDA establishment registration and drug listing, with DQSA section 506C notifications, or with
   a commercial data vendor. HA-11b is an evidence-acquisition task, and the only interview half of it is line rates
   from role 2.
2. **The replenishment review policy and order-up-to level a real regional stocking point runs.** HA-40. Enters the
   region policy block in `strategies.build_strategy`. The hard-coded rule it replaces decides 8 of 16 Phase A cells.
3. **Node and reserved-capacity cost, with batch, campaign and changeover data.** HA-13 and HA-21. Enters
   `config/products/*.yaml` and `config/strategies/design_space.yaml`. Fixed and resilience cost is 81.0% to 93.7% of
   annual cost in every comparator, so every absolute cost is a statement about the scaffold until this lands.
4. **A price and a committed volume a purchaser with authority would sign, and whether anyone funds standing
   availability at all.** HA-36, HA-24, HA-38. Enters `contracting.py` and the reservation-fee ledger in
   `simulation.step8_costs`. Every design currently reads "not contractable, stated".
5. **The reporting category for adding a third-party sterile fill site to an approved application.** HA-23, then
   HA-31 for all sixteen gates. Enters `config/regulatory_gates.yaml` G07 and the activation leads. A prior-approval
   supplement with a preapproval inspection removes S12's 365-day leg.
6. **A multi-site disruption rate, duration and impact fraction.** HA-39. Enters `disruptions.py`. At base demand the
   feasible set collapses from 11 strategies to 3 on norepinephrine and from 10 to 2 on sodium bicarbonate as the rate
   rises across its declared range.
7. **The sterilization route per presentation, terminal or aseptic, and the cycle if terminal.** HA-34. Enters a
   product route attribute and a parametric-release scenario. It is the enabling data for the only intervention found
   across fourteen families that acts on the binding release constraint rather than on components that do not bind
   (`../design_space/prior_art_review.md` section 6.1).

---

## 6. How to take an answer

- **Consent first, in the first two minutes.** Role, organization type, whether attribution is authorized, whether
  quotes may be used, whether you may record. Assign and record the interview id from `data/interview_evidence/`,
  format `INT-YYYY-NNN`.
- **Ask for the range before showing yours.** Anchoring is the main way this kind of elicitation goes wrong. Ask for
  the 10th percentile, the median and the 90th, or for a low, a likely and a high, whichever the person is comfortable
  with. Show the domain's page in `../../ASSUMPTIONS.md` afterwards, never before.
  `elicitation_worksheet.md` sets the exact order and the parameter card; follow it rather than improvising.
- **Ranges are the preferred answer, not a fallback.** A wide honest range is more useful than a confident point, and
  the sensitivity analysis is built to carry width.
- **Rate questions need three numbers**: how often, for how long, and how much capacity is lost.
- **Record the rationale verbatim.** What would make it higher, what would make it lower, and why they are confident
  or not.
- **Never average across people silently.** Keep every range separately and let the disagreement show as a
  `contradicts` token on both records plus a widened sensitivity range, per `elicitation_worksheet.md` rule D3. The
  protocol's fifth tier-4 field is named `disagreement`; in the record schema it is carried by `contradicts` and by
  the `disagreement` field added to `claims[]` on 2026-09-06, and worksheet rule T1 says how they map.
- **Log within 24 hours**, per `evidence_log_schema.json`: every parameter challenged, the range offered, the
  confidence, the rationale, contradictions with other evidence, and the exact model change or the reason for no
  change. Then `revision_workflow.md`. A purchaser interview logs under `gpo_wholesaler_distributor`, because the
  schema's `role_category` enum has no purchaser value yet (`target_matrix.md` section 8).
- **Close with:** may we follow up once, and may we cite you by role. If the person is willing to reject the
  assumptions in writing, that is the independent-review track (HA-30 to HA-33), it is a separate and larger ask, and
  it should be made as one.

---

## 7. What not to say

This section is the claim-discipline table in `protocol/protocol.yaml` plus the rows of `CLAIMS_REGISTER.csv` that are
recorded as contradicted. It applies to the conversation, the outreach note, the follow-up, and anything you show on
screen.

**The four claims that may not be repeated at all.**

- **C009.** Not "real-time release replaces a two-week lab hold". The register records it as contradicted by the
  study's own analysis. Allowed wording, exactly: "for aseptically filled injectables, chemical real-time release does
  not shorten the release hold while the 14-day sterility incubation is the critical path; it shortens the hold for
  oral solid dose; the candidate value for injectables is an assured beyond-use date and distribution radius, which is
  unvalidated".
- **C010.** Not "automates the release decision", not "certifies pharmaceutical batches in real time", not
  "FDA-ready", not "regulator validated", not "partnered with". Allowed wording, exactly: "in a public-benchmark
  methods study, our shift detector abstained under instrument drift; prospective product/site validation is the next
  step". The register tags that sentence as the protocol claim-discipline form.
- **C015.** Not "the operating system for sterile drug manufacturing" and not "the moat is the operating system".
  Allowed wording, exactly: "software in development for sterile drug manufacturing, or: a release-decision support
  layer; never paired with 'automates the release decision'".
- **C025.** Do not quote the sentence attributed to FDA's 2004 aseptic guidance section XI.B about the sterility test
  being an essential element. It is not in the guidance. The 14-day pole does not depend on it: it comes from USP
  <71> incubation and from samples drawn during the fill.

**From the claim-discipline table.** Do not say "distributed manufacturing solves shortages". The permitted form is
that the model found a bounded feasibility region, or found distributed capacity dominated, under stated assumptions.
Do not call a CMS figure a manufacturing cost; it is a utilization or reimbursement proxy and cost is estimated
separately. Do not say "partnered with" after an interview; the permitted form is "Interviewed [role/organization
type] and revised X assumption".

**The rules that cover everything else.**

- **No model number is a finding.** You may say "under illustrative inputs the model does X". You may not say "we
  found that X" or quote a cost, a break-even price or a capital requirement as a fact about the world. The rule has
  two parts and both bind. **No model result may be stated as a finding about the world, in any setting.** **Model
  behaviour under stated illustrative assumptions may be described to a named interviewee or reviewer inside this
  study process**, which is what the frame in section 2, the field kit and the reviewer packets do, **and it may not
  appear on any public, promotional or fundraising surface, in any email, or in any document sent ahead of a
  conversation.** An earlier version of this bullet, and the same sentence at
  `../design_space/strategic_synthesis.md` section 10, stated the prohibition in an absolute form that forbade the
  interview and reviewer programme itself. Both texts were corrected on 2026-09-06 and they now agree. The narrower
  form was already the operative one in `../reviewer_packets/README.md` section 7.
- **No regulatory opinion, in either direction.** All sixteen gates are UNCERTAIN and UNCERTAIN is never PASS. Do not
  say a pathway is available, and do not say it is closed. 503B is a time-varying legal state, never a durable
  pathway.
- **No relationship is asserted.** Not a partner, not an advisor, not a validator, not a customer, not a pilot, not a
  reviewer, unless the person has authorized it in writing. Every company named in this study is a published third
  party cited by source id.

**On the product.** If asked which product this is about, the beachhead is under revision. Allowed wording, exactly:
"beachhead under revision: the original norepinephrine/epinephrine pick was withdrawn after primary-source checks
(2026-07-16); furosemide 10 mg/mL is the current candidate pending a primary-source shortage check; candidate
presentations are screened in this study".

**If you are unsure whether a sentence is allowed**, do not say it and note the question. The register's
`allowed_external_wording` column is the whole permitted vocabulary, quoted exactly, and a sentence that is not in it
has not been checked.

---

## 8. What counts as a completed interview

All four, or it is not counted against the 25 to 30 target in `target_matrix.md` and DF18:

1. The person has directly relevant experience for the role they were counted under.
2. Consent and attribution permissions are recorded.
3. The evidence log exists at `data/interview_evidence/<interview_id>.json` at `status: complete`.
4. Every challenged parameter carries the range offered, the confidence, the rationale, and either the model change or
   the stated reason there was none.

Vendor quotations and price lists are documents, not interviews. Independent reviews are a separate track counted by
DF19. Both are recorded in `target_matrix.md` section 7.
