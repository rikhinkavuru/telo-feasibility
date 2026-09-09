# Module: generic-drug, CMC and 503B regulatory

Roles: a regulatory professional who has filed post-approval changes for sterile injectables, or a 503B regulatory
specialist for question 3. Queue items this module settles: HA-23 first, then HA-42. HA-31, HA-15 and HA-16 are
**not** settled here; see "What this module no longer asks" below. Length: the whole call is 45 minutes and this module has about 28 of them; the one published timetable is
`../elicitation_worksheet.md` section 2. If only question 1 is in scope, the call is 20 minutes.

**PRELIMINARY REGULATORY ANALYSIS; NOT LEGAL ADVICE.** This module asks for a professional reading, not an opinion
about Telo. Nothing said here is or implies agency engagement, a pre-submission, an endorsement, a partnership or a
customer relationship, because none exists. All sixteen gates are UNCERTAIN today with no reviewer and no review date.
UNCERTAIN is never treated as PASS, and a gate status counts only when a named qualified reviewer records it with a
date and a rationale. "UNCERTAIN, and here is the evidence that would settle it" is a good answer.

**Why this module leads with question 1.** The reporting category for adding a third-party sterile fill site to an
approved application is the single answer that changes the most in this package after the gate review itself. The
study's strongest shape is contracted campaigns at registered lines rather than a plant that gets built, and that shape
depends on an activation leg whose length is exactly this question.

## Questions

| # | Question | Lands on | Now (declared range) | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | Adding a named third-party sterile fill site to an approved ANDA for this presentation: what reporting category is that, does it carry a preapproval inspection, and what review and implementation time would you plan for? | gate G07 (change-control category); `second_source_qualification_days`; the activation leads in `config/strategies/design_space.yaml` (HA-23) | G07 UNCERTAIN. Second-source qualification 365 days (180 to 730) | a category from annual report, CBE-0, CBE-30, prior-approval supplement; yes or no on a preapproval inspection with the reason; a lead time as a range in days. Cite the basis (21 CFR 314.70 and the FDA post-approval changes guidance) | If it is a prior-approval supplement with a preapproval inspection, the 365-day activation leg the contracted-network design relies on does not exist, and the contracted family loses its central advantage over building. Three rows of the falsification register turn on this one category |
| 2 | May one quality unit perform batch disposition for several registered sites under one application? May several sites share one filing, and what must each site still hold of its own? | 21 CFR 211.22(a); fixed quality labour per site; the `validation_factor` and the `cc_quality` common-cause group (HA-42) | the model replicates a full quality unit per site and shares nothing | yes or no with the reason, plus a list of what must stay site-resident | The only lever on two cost blocks that carry 24% to 33% and 4.7% to 18% of annual cost and that no service mechanism touches. The base rate is against it: of about 900 sterile-injectable ANDAs approved 2000 to 2011, 11 referenced more than one finished-dose facility (F6-S37) |
| 3 | For 503B: what is the shortage-list predicate at the compounding, distribution and dispensing dates, what happens to stock on hand when a listing resolves, and what beyond-use date is supportable? | gates G09 and G10; `shortage_list_resolution_rate_per_year`; `shortage_list_relisting_rate_per_year`; `bud_503b_days` (HA-17 supplies the compendial text) | resolution hazard 0.3 per year (0.1 to 1.0); relisting 0.1 per year (0.02 to 0.4); beyond-use date 90 days (45 to 180). All illustrative | categories for each predicate, plus a beyond-use date in days | The 503B comparator. The model treats the listing as a state that switches off, and treating it as permanent is the forbidden assumption that produced the only two feasible 503B cells in the Phase A screen |
| 4 | Before a second API or container-closure source can be used, what has to be in place, and how long does that take? | gate G16 (21 CFR 211.84 and 211.94, plus a Type II drug master file letter of authorisation); `second_source_qualification_days` (HA-23) | G16 UNCERTAIN, added under revision R007 on 2026-09-03 | a lead time range in days plus the records required | Three designs declare a second API or container source and none of them prices the switching lead, so their upstream advantage is currently free |

### What this module no longer asks, and where each went

- **The sixteen gate statuses (HA-31) are not asked on a call.** They are a written deliverable: sixteen statuses
  with qualification, rationale and date, which is `../../reviewer_packets/packet_2_regulatory.md`. If this person
  is qualified and willing, make that ask separately, once, after the sequencing gate clears. `../sequencing.md`
  wave 4 is explicit that HA-23 is one category question answerable in a call while HA-31 is not, and that the same
  person must not be spent twice. The gate list below is kept for context, so the interviewer can see what G07 sits
  inside.
- **Registration and listing across sites (old question 4, gate G13, HA-15)** and **cross-site equivalence (old
  question 5, gate G14)** moved into packet 2, where they are asked of a reviewer who has the gate table in front of
  them.
- **The final status of FDA's January 2025 AI credibility draft guidance and of EU GMP Annex 22 (old question 8,
  gate G15, HA-16)** is a document task, not a question. Fetch both into `data/raw_snapshots/` with a date. A status
  fetched by us is tier 1; the same status recalled by a person is tier 4, and it costs an expensive slot.

### The sixteen gates, for context

| id | name | model treatment |
|---|---|---|
| G01 | Application ownership or binding CMO relationship | exclude the strategy if FAIL |
| G02 | Site in the approved application; establishment registered and drug listed | adds lead time |
| G03 | Product, process and cleaning validation complete | hard feasibility |
| G04 | Aseptic processing or terminal sterilization validated | hard feasibility |
| G05 | Analytical methods transferred and validated | hard feasibility |
| G06 | Stability and container-closure evidence supports the shelf life | caps inventory and shelf life |
| G07 | Change-control category and FDA submission identified | adds lead time (question 1) |
| G08 | Outsourcing facility registered annually and CGMP compliant | exclude if FAIL (503B only) |
| G09 | Bulk substance eligible at compounding, distribution and dispensing dates | time-varying state (503B only) |
| G10 | Product not barred as essentially a copy | time-varying state (503B only) |
| G11 | Stability, beyond-use date and sterility controls supported | cap (503B only) |
| G12 | State licensure and distribution permissions mapped | region restriction (503B only) |
| G13 | Each site's registration and listing approach is supportable | adds lead time; moved to packet 2 |
| G14 | Cross-site comparability protocol accepted for the product | no fleet claim; moved to packet 2 |
| G15 | Release model within a validated state of control, drift handling defined | falls back to conventional release; its two source documents are a snapshot task, not a question |
| G16 | Alternate component, container-closure and API source qualified and authorised | adds lead time (question 4) |

## What was dropped, and why

- **Four questions left the module on 2026-09-06**, and the reasons are in "What this module no longer asks" above:
  the sixteen gate statuses (a written reviewer deliverable, not a call), registration and listing across sites and
  cross-site equivalence (both moved into packet 2), and the final status of the two documents behind G15 (a
  snapshot task). The module went from eight questions in a thirty-minute tail to four inside a forty-five-minute
  call, which is the first version of it that fits in the time it asks for.
- **The distributed-manufacturing proposed rule** is not asked here for a second reason as well as the move: the
  protocol forbids a base case that depends on a proposed rule becoming final in a preferred form, so its answer can
  only add a branch and never a verdict.
- **Nothing else was dropped.** The reporting category still comes first, because it is the single answer that
  changes the most in this package after the gate review itself.
