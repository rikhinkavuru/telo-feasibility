# Outreach templates

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** No interview has been held. Every model result named in the
interviewer-only notes below is behaviour of the engine under evidence tier 5 (illustrative) inputs and describes the
model, not sterile-injectable manufacturing. All sixteen gates in `config/regulatory_gates.yaml` are UNCERTAIN, so
nothing here states or implies a regulatory position. 503B is a time-varying legal state and never a durable pathway.
Nobody contacted through these templates is a partner, customer, advisor, reviewer or validator.

## What changed, and why the old opening is retired

The study was designed to answer one question: under what conditions does distributed regional capacity beat safety
stock, dual sourcing, reserved contract capacity, or more capacity at an existing plant. Under the inputs the model
carries today that question is answered, and the answer is that distributed capacity is dominated in every recorded
range on both modelled products, and that giving it the same inventory freedom that makes the alternatives feasible
does not rescue it (`../design_space/feasibility_regions.md` sections 6 and 8).

The previous templates opened by asking people to help settle that question. They now ask people to help settle a
different one, because the honest position is this: the model says no, every input behind that no is a placeholder
the author wrote, and nobody outside this repository has checked either half. The opening claim in every template
below is therefore **"a pre-registered model was built to test whether distributed manufacturing beats the
alternatives, it says no, and I am trying to find out whether the inputs are wrong or the model is before I
publish."** That is a real reason for a practitioner to give forty-five minutes. It also changes what the
conversation is for: since every input is tier 5, the value of the call is in the numbers and categories it produces,
not in opinions about architecture.

**Four things changed again on 2026-09-06.** The affiliation is now disclosed in the first message, always (rule 9).
Every body names why this person was contacted, offers the two-question email version with the questions written out,
and offers to send the whole question set in advance for employer clearance. The ask is forty-five minutes, which is
what the instrument actually runs. And the attachment is the role **handout** in `modules/handouts/`, never the
module, because the modules carry model results in three of their six columns and section K forbids putting any model
output in an email.

## Rules that bind every template

1. **At most 220 words. No sentence over 25 words**, except a sentence that is a list introduced by a colon, where
   the cap is 45. The old rule was "exactly five sentences", which held the content constant and forced it into 36 to
   44 word sentences against a house voice of short ones. Measured on the current bodies: 202 to 220 words, 14 to 16
   sentences, mean sentence length 13.2 to 15.4. The cap is 220 rather than 170 because rules 9, 10 and 11 each add a
   sentence that is not optional; that is a deliberate trade, and it is recorded rather than hidden.
2. **No pitch.** No product, no raise, no roadmap, no company positioning, no request for an introduction, no ask to
   try anything.
3. **Nothing implied.** No partnership, endorsement, customer, pilot, review, or regulatory opinion, before or after
   the call. Claim-discipline wording is in `protocol/protocol.yaml` `claim_discipline`; "partnered with" after an
   interview is on its forbidden list, and the permitted form is "interviewed [role or organization type] and revised
   X assumption".
4. **No study numbers.** No cost, fill rate, break-even price, ranking, frontier or figure appears in an email. The
   verdict is stated as model behaviour under stated assumptions, never as a fact about the world. One thing is
   permitted, because it is the reason the question is being asked: how much a named input moves the model's own
   answer, said plainly and said as a property of the model.
5. **Answerable, and placed.** Every question asked must be answerable from the person's own work, and the interviewer
   must be able to say on the call where the answer enters the model and which result it can reverse. The "Buys" line
   under each template holds that mapping; it is interviewer-only and is not sent.
6. **Ranges beat point estimates.** Say so in the email, and mean it (`elicitation_worksheet.md` section 3).
7. **Role-only attribution** unless the person authorizes their name in writing.
8. **One follow-up, then stop.** Section I.
9. **Affiliation is disclosed in the first message, always.** Who the sender is, and who they work for, in the
   sender's own first two sentences. The permitted wording is the `allowed_external_wording` column of
   `CLAIMS_REGISTER.csv` row C015, quoted exactly: "software in development for sterile drug manufacturing, or: a
   release-decision support layer", never paired with "automates the release decision" (C010). Templates D, E and F
   reach process engineers, CDMO commercial leads and quality staff at firms that are potential suppliers or
   competitors, and are asking for installed capital, reservation pricing and deviation rates. Not naming the
   affiliation there is a material omission, and it is also the first thing any recipient wants to know.
10. **Say why this person.** One clause naming the actual reason they were contacted. The bracketed placeholder in
    every body is filled in before sending, or the message is not sent.
11. **Always offer the cheap alternative.** The two-question email version, with the two questions written out in
    full, and the offer to send the whole question set in advance so it can be cleared with an employer. Clearing
    questions before speaking is the norm in a regulated industry, and not offering it is a reason to not reply
    rather than a reason to decline.
12. **Subject lines cap at 45 characters, hook first.** A 94-character subject truncates in every mail client before
    its hook, and internal vocabulary ("sixteen gates", "comparator harness") means nothing outside this repository.

## Which template, which role, which log

`role_category` is the enum in `evidence_log_schema.json`. Queue ids are from `../audits/07_human_action_queue.md`.

| Template | Role | Logs as `role_category` | Queue ids it is trying to close | Handout attached |
|---|---|---|---|---|
| A | Hospital pharmacy or supply-chain leader | `hospital_pharmacy_supply_chain` | HA-20, HA-35, HA-43, HA-11a | `modules/handouts/hospital_gpo.md` |
| B | Demand, inventory or distribution planning owner at an IDN, GPO or wholesaler | `gpo_wholesaler_distributor` | HA-11a, HA-40 | `modules/handouts/distribution.md` |
| C | GPO, wholesaler or IDN contracting lead, or a purchaser with budget authority | `gpo_wholesaler_distributor` | HA-38, HA-36, HA-24 | `modules/handouts/purchaser.md` |
| D | Sterile manufacturing or process engineer | `sterile_manufacturing_process` | HA-21, HA-41 | `modules/handouts/manufacturing.md` |
| E | CDMO commercial lead, or cleanroom and fill-finish engineering vendor | `sterile_manufacturing_process` | HA-13 | none; scope paragraph only |
| F | Quality, CMC, microbiology or validation professional | `quality_cmc_microbiology_validation` | HA-22, HA-42 | `modules/handouts/quality_cmc.md` |
| G | Generic-drug or 503B regulatory professional | `generic_drug_or_503b_regulatory` | HA-23, and HA-34 in part | `modules/handouts/regulatory.md` |
| H | Operations researcher, reliability engineer or drug-supply economist | `drug_supply_economics_operations_research` | HA-39, HA-25 | `modules/handouts/operations_research.md` |

Template E is a request for a budgetary estimate rather than an interview. It is not counted toward the interview
target in `target_matrix.md`, and a vendor figure is logged as a dated estimate at a stated scope, not as elicitation.

HA-31, the sixteen gate statuses, is not on template G's list. It is a written reviewer deliverable made once through
`../reviewer_packets/packet_2_regulatory.md`, not an interview ask (`sequencing.md` wave 4).

---

## A. Hospital pharmacy or supply-chain leader

**Subject:** My shortage model says my own idea fails

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because your role covers purchasing and allocation for this
presentation [say the actual reason]. I built a pre-registered model to test whether regional sterile-injectable
capacity beats safety stock, dual sourcing, reserved contract capacity, or more central capacity. Under the
assumptions it carries today it loses to all four. Every input in it is a placeholder I wrote myself. So I cannot
yet tell whether the inputs are wrong or the model is. I am asking for forty-five minutes of numbers and
categories. Ranges beat single numbers. If a call is not possible, two answers by email would still change the
model: how many days of supply you hold for a named presentation, and how long an unfilled order stays open before
the demand is lost. I can send the whole question set in advance if you need it cleared internally. Answers are
logged under your role and organization type only, unless you authorize your name in writing. Nothing here will be
described as a partnership, an endorsement, or a review.

**Buys (interviewer only, not sent).** `backorder_window_days` (HA-43) and the substitution and allocation
categories (HA-35, HA-20) enter `simulation.step5_serve` and `allocation.py`. `backorder_window_days` is the metric
definition MD-5 records as non-monotone, so the fill-rate measure itself is unsettled until this lands. **Attach
`modules/handouts/hospital_gpo.md`**, never `modules/hospital_gpo.md`, which carries model results in three of its
six columns.

## B. Demand, inventory or distribution planning owner

**Subject:** Two inputs decide a shortage model

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because you own demand or replenishment planning for injectables [say
the actual reason]. I built a pre-registered model to test whether regional sterile-injectable capacity beats
safety stock, dual sourcing, reserved capacity, or more central capacity. It says no, under placeholder inputs I
wrote. Two inputs move that result more than anything else, and neither exists in my file. The replenishment rule
in the model is one I hard-coded and cannot source. It decides the answer in half the cases I have tested. If
forty-five minutes is not possible, two answers by email would still change the model: the units per year your data
shows for one exact presentation, and the review frequency and order-up-to level a regional stocking point actually
runs. A stated range is enough. An anonymized extract is better. I can send the questions in advance for internal
clearance. Attribution is by role and organization type unless you authorize otherwise, and nothing here is a
partnership or an endorsement.

**Buys.** `product.annual_demand_units` and regional shares (HA-11a) enter `config/products/*.yaml` then
`demand.py` and the deterministic screen; utilization is the one derived number separating the two modelled
products. `region_base_stock` and `region_reorder_point_days` (HA-40) enter the region policy block in
`strategies.build_strategy` and close MD-3, the largest artifact in the Phase A decomposition. The installed-capacity
half of the old HA-11 is HA-11b and is not asked here: it is an evidence-acquisition task against FDA establishment
registration and listing, not something a planner holds. **Attach `modules/handouts/distribution.md`** plus the blank
elicitation cards, with our low, base and high left blank.

## C. Contracting lead or purchaser with budget authority

**Subject:** Nothing to sell: what a contract looks like

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. There is no term sheet and nothing I can supply. I am writing to you because you hold
contracting or budget authority for injectables [say the actual reason]. I built a pre-registered model to test
whether regional sterile-injectable capacity beats the ordinary alternatives. It says no, on inputs that are all
placeholders. The designs that survive at all survive only if somebody signs a committed volume at a price. I have
no price evidence of any kind. If forty-five minutes is not possible, two answers by email would still change the
model: does your organization ever pay for standing availability of a generic injectable separately from the units
it ships, and what price per unit could you actually sign. My working assumption is that nobody pays for standing
availability. I would like to be told plainly if that is wrong. Ranges and refusals are both useful. I can send the
questions in advance. Nothing about this will be called a partnership, a customer relationship, or a commitment.

**Buys.** The nine `ContractTerms` fields and `price_required_usd_per_unit` (HA-36, HA-24) enter
`contracting.contract_requirement`; every design in the package reads "not contractable, stated" until they land. The
availability answer (HA-38) has no field in the engine yet and its recorded fallback is "assume no". **Attach
`modules/handouts/purchaser.md`.** Do not attach any break-even price, or any other number, from the study. Run
`modules/purchaser.md` on the call, and read its guardrail before dialling.

## D. Sterile manufacturing or process engineer

**Subject:** Batch, campaign and changeover reality

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because you have run or commissioned a small aseptic fill line [say
the actual reason]. I built a pre-registered model to test whether distributed regional sterile capacity beats
safety stock, dual sourcing, reserved capacity, or more central capacity. It says the distributed version loses
everywhere I have looked. The inputs are all placeholders I invented. Before I publish that I want line numbers
from someone who has run one: batch size, batches per year, campaign length, changeover days, uptime, and restart
time after a deviation. I would also like the elapsed time from a decision to build to the first released batch,
split four ways. If forty-five minutes is not possible, two answers by email would still change the model: batches
per year and changeover days on a small aseptic vial line. Ranges with the conditions attached beat single numbers.
I can send the questions in advance. Your role only, unless you authorize your name, and nothing here is a
partnership, an endorsement, or a review.

**Buys.** `units_per_batch`, `batches_per_site_year_nominal`, `uptime_fraction`, `product.changeover_days` and the
deviation restart (HA-21) enter `config/products/*.yaml` and `production.py`; changeover produces twenty threshold
crossings in the design-space sweep. The commissioning split (HA-41) enters `node_commissioning_days` and
`capacity_expansion_days`, where MD-17 records three parameters colliding with the warm-up boundary. **Attach
`modules/handouts/manufacturing.md`.**

## E. CDMO commercial lead, or cleanroom and fill-finish vendor

**Subject:** Budgetary basis, no project behind it

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because you price installed aseptic capacity [say the actual reason].
I need a budgetary basis rather than a proposal. There is no project, no site, no timeline and nothing to buy. The
study compares building small aseptic capacity against contracting capacity that already exists. Every cost figure
in it today is a placeholder I invented, and cost is where the comparison is decided. What I am asking for is
scoped and dated: installed and qualified capital for a small aseptic vial line, annual fixed operating cost, and
the qualification timeline. Then, for an existing registered line: what a reserved-capacity agreement costs per
year, what the fee covers, and the minimum campaign size. A range with your assumptions attached is more useful
than a precise number. I will record it as your estimate at your stated scope and date, not as a quotation. I will
not describe your company as a partner, a supplier or a participant.

**Buys.** `capital_usd_per_site`, fixed operations, validation cost, `reserved_capacity_fee_fraction`,
`node_commissioning_days` and `capacity_expansion_days` (HA-13). Fixed and resilience cost is the large majority of
annual cost for every comparator, so every absolute cost in the package is a statement about the scaffold until this
lands. Ask for the reservation fee in **dollars per year**, not as a fraction of anything; the model's fraction is
derived afterwards. Send no attachment except the scope paragraph.

## F. Quality, CMC, microbiology or validation professional

**Subject:** Is my release decomposition naive?

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. Nothing here is presented as automating, certifying or replacing a release decision. I am
writing to you because you work on release, validation or microbiology for sterile injectables [say the actual
reason]. I built a pre-registered model of sterile-injectable supply to test whether distributed capacity beats the
ordinary alternatives. It says no, under inputs that are all placeholders. The part I least trust is the release
decomposition I wrote. In the model the release hold is the maximum of the parallel components plus serial quality
review. I want to know whether that structure is right or naive. I am also asking for the numbers underneath it:
deviation rate per batch, investigation duration, batch rejection frequency, and what a second site must replicate.
If forty-five minutes is not possible, two answers by email would still change the model: your deviation rate per
batch, and whether those tests really do run in parallel from the fill. I can send the questions in advance.
Role-only attribution unless you authorize your name.

**Buys.** `sterility_incubation_days`, `environmental_monitoring_days`, `assay_days`, `endotoxin_days`,
`qa_review_days`, `deviation_rate_per_batch`, `investigation_duration_days`, `validation_factor` and
`wrong_release_cost_usd` (HA-22), plus the one-quality-unit question (HA-42). Claim discipline is tight here: C009,
C010, C015 and C025 in `CLAIMS_REGISTER.csv` may not be repeated in any form, abstention is never release, and the
only permitted description of the software is the `allowed_external_wording` column, which is exactly the affiliation
sentence in the body above. **Attach `modules/handouts/quality_cmc.md`.**

## G. Generic-drug or 503B regulatory professional

**Subject:** Adding a fill site: which reporting category

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because you have filed post-approval changes for sterile injectables
[say the actual reason]. I built a pre-registered model of sterile-injectable supply to test whether distributed
capacity beats the ordinary alternatives. It says no, on inputs that are all placeholders. So I am asking qualified
people to attack it. Its sixteen regulatory gates are all uncertain with no reviewer, so no design in it can be
called permitted. The single question that moves the most is this. Is adding a named third-party sterile fill site
to an approved application a CBE-30-class change, or a prior-approval supplement with a preapproval inspection? If
forty-five minutes is not possible, that one answer by email, with the basis you rely on, would change the model on
its own. I can send the questions in advance for employer clearance. Your answer is recorded as one qualified
professional's reading, with your qualification and the date. It is never legal advice, never an FDA position, and
never validation of this pathway map.

**Buys.** G07's reporting category (HA-23) enters `config/regulatory_gates.yaml` and
`regulatory.evaluate_strategy`. **HA-31, the sixteen gate statuses, is not part of this message.** It is a separate
and larger written ask, made once, through `../reviewer_packets/packet_2_regulatory.md`, after the sequencing gate
clears; `sequencing.md` wave 4 says not to spend the same person twice. `ProductFeatures.sterilization_route` (HA-34)
is a document task first: fetch the reference product's Drugs@FDA chemistry review, an establishment inspection
report, and the USP monograph, and ask a person only about products they have personally worked on. **Attach
`modules/handouts/regulatory.md`**, plus `config/regulatory_gates.yaml` and the pathway maps under `docs/regulatory/`
if they ask for them, each marked preliminary and not legal advice.

## H. Operations researcher, reliability engineer or drug-supply economist

**Subject:** Multi-site disruption rates, and my harness

I am [name]. I work on software in development for sterile drug manufacturing, a release-decision support layer.
This is research. There is nothing to buy or sell here, and I am naming the affiliation first because I am about to
ask about your own work. I am writing to you because you hold or study multi-site disruption data [say the actual
reason]. I built a pre-registered model to test whether distributed sterile-injectable capacity beats the ordinary
alternatives. It says no, under placeholder inputs. I have already found one defect: the comparators were searched
over a narrower space than the new architectures. Fixing it changed a headline. The input I most need is empirical
rather than methodological. If forty-five minutes is not possible, two answers by email would still change the
model: the annual rate at which one event removes more than one nominally independent site or supplier, and how
long such an event lasts. I would also value your view on whether a daily discrete-time engine with common random
numbers is the right comparator harness. A rate with its reference class stated is the useful form. I can send the
questions in advance. Attribution is by role unless you authorize your name.

**Buys.** `common_cause_events_per_year`, `common_cause_duration_days` and `common_cause_capacity_impact` (HA-39)
enter `disruptions.py` and the common-cause groups in `strategies.build_strategy`; across the declared range the
feasible set collapses on both products, so no strategy ranking in the package can be quoted without this range
attached. Confirm the entity level explicitly: the parameter record declares network level and the engine applies the
rate per common-cause group. The method questions are HA-25. **Attach `modules/handouts/operations_research.md`** and,
on request, `docs/architecture/design.md`.

---

## I. Follow-up (one, then stop)

Send once, seven to ten working days after the first message. Do not send a third message. If there is no reply to
the follow-up, record the contact as `contacted_no_reply` in `target_matrix.md`. Not as `declined`, because no answer
is not a refusal, and **not as `not contacted`**, because a person who has been emailed twice must be
distinguishable from a person who has never been written to. Recording a contacted person as `not contacted` is how a
third message gets sent against this file's own one-follow-up rule, and it makes the matrix's own headline count
unreadable.

**Subject:** Re: [original subject]

Following up once on the note below, and then I will leave it there. The short version is that I built a model to
test whether distributed sterile-injectable capacity beats the ordinary alternatives, it says no, and every input
behind that no is a placeholder I wrote, so I am asking practitioners to tell me which half is wrong. If forty-five
minutes is not possible, two answers by email would still change the model: [the two highest-value questions for this
role, written out in full, the same two that were in the first message]. If this is the wrong desk, I would rather
you say so than forward it, since I am not asking for introductions. No reply is a fine answer and I will not write
again.

## J. Declining gracefully

Two cases. Use the first when the person says no. Use the second when the person offers something the study cannot
accept.

### J1. When they decline

**Subject:** Re: [original subject]

Understood, and thank you for saying so directly. I will record this as declined with your role only, and I will not
contact you again about it. Nothing you said appears anywhere in the study, and nothing about this exchange will. The
study does cite published third parties by source id from public sources, so your organization may already appear
there; that is a citation of the public record and has nothing to do with you or with this note. If it becomes useful
later, my question set is short and stays open. Good luck with the year.

Then set the row in `target_matrix.md` to `declined`, and if any exchange occurred, log a record with
`status: "declined"` and no `claims` entries.

*Why the wording changed.* The old version promised that "nothing about you or your organization appears anywhere in
the study, and it will not". The study names published third-party organisations by source id throughout, so that
sentence was false the moment it reached anyone working at one of them, and it was being sent in writing to a person
who had just refused.

### J2. When we must decline what they offer

Practitioners offer things the study may not take: an advisory title, a logo, a quote for a website, a confidential
document without written authorization, an introduction framed as a partnership, or a review that is really an
endorsement. Refuse in the moment, in one short paragraph, and put the refusal in the record.

**Subject:** Re: [original subject]

Thank you, and I have to turn that down. My protocol does not let me describe anyone as an advisor, a partner, a
validator or a reviewer without written authorization and a logged review, and a logo or a quote is not validation.
What I can do is record you by role, cite the specific thing you corrected, and send you the wording before anything
goes out. If you would like to be named later, that is a separate written decision and it can wait until there is
something worth being named on. Either way, the correction you gave me is already in the model.

If the offer is a confidential document, do not accept it until the terms are written down: who owns it, what may be
published from it, and what tier it earns. If the offer is an independent review, that is a different process, with
its own qualification, issue log and published model changes (`protocol/protocol.yaml` `independent_review`), and it
cannot be agreed on a call.

---

## K. What to attach, and what never to attach

**Attach.** Keep it to one page plus consent.

- **The role's handout: `modules/handouts/<role>.md`.** Three columns: the question, the units and entity level, and
  the answer form. **Never the module in `modules/`.** The modules are the interviewer's copy and carry model results
  in three of their six columns, including fill rates, break-even prices and threshold crossings, and their "Now
  (declared range)" column is the study's own low, base and high, which `elicitation_worksheet.md` section 3 says is
  shown only after the person's first answer. Attaching a module would break the "never attach" list below and
  destroy the anchoring rule in the same act.
- The elicitation cards for the specific parameters, with the study's own low, base and high left blank until after
  the person's first answer (`elicitation_worksheet.md` section 3, anchoring rule).
- One short consent and attribution paragraph: role-only by default, quotes only with permission, one follow-up
  allowed, the record shown to them before anything is published.
- On request only: `protocol/protocol.yaml` v1.0.0, so they can see the decision rules and thresholds were fixed in
  advance.
- Role-specific: `config/regulatory_gates.yaml` and `docs/regulatory/*.md` for template G, marked preliminary and
  not legal advice; `docs/architecture/design.md` for template H.

**Never attach, and never paste into an email.**

- Any model output. No cost, fill rate, tail probability, break-even price, ranking, frontier, threshold crossing or
  figure. Every one is tier-5 driven, and the package's own banner forbids external use.
- `field_kit.md`. It is the interviewer's card. It is not shown to the interviewee and it is not left behind.
- Any `modules/*.md` file. Send the handout.
- The design-space documents: `strategic_synthesis.md`, `feasibility_regions.md`, `bottleneck_decomposition.md`,
  `novel_architectures.md`, `prior_art_review.md`, and the rest of `docs/design_space/`. These are internal working
  records that quote model numbers on every page.
- `CLAIMS_REGISTER.csv`, `public_claims_corrections.md`, or any file that reads as a list of the company's own
  errors. Correct the public surfaces (HA-04) rather than mailing the audit.
- Any deck, website copy, valuation, raise, roadmap or product page. Sending one turns the message into a pitch,
  which is the thing these templates exist to avoid. The affiliation is disclosed in a sentence, not in a deck.
- The contact lists in `outreach/`. They hold personal addresses and the exposure is open until HA-06 to HA-08 are
  done.
- Any third party's name, logo or material positioned as involved, supportive or consulted.
- Any regulatory reading of ours stated as a conclusion, any wording from the C009, C010, C015 or C025 rows of the
  claims register, and anything pairing "automates the release decision" with the software.
- Another interviewee's answers, ranges or identity, before the synthesis is published with role-only attribution.
- An NDA, a term sheet, a letter of intent, a purchase order, or anything that could be read as one.
