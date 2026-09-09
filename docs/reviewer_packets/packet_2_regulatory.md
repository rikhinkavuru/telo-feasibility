# Review packet 2: Generic-drug CMC or 503B regulatory

Reviewer id `reviewer_2` (`protocol/protocol.yaml` `independent_review`); queue ids HA-31 (assign a status to
every gate) and HA-23 (the professional reading behind the change-control category). You can reject the pathway
map and every gate status, and rejecting them is the point.

**Status: not sent. No review has been completed.**

**How long this takes.** Full review: about six hours, most of it in the sixteen gate statuses. **If you have
one hour: read section 2, answer the HA-23 row in section 7, and stop.** A single sourced reading of the G07
reporting category is worth more than a general assessment of the approach. Reading code is optional; section 3
item 3 exists for people who want it, and what a gate status does to a strategy is stated in plain English in
section 2. No compensation is offered. A sixteen-gate written opinion with rationale and qualification is
billable consulting work, and asking for it unpaid is a real reason to decline; if that is the reason, say so
and we will record it.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** All sixteen gates in `config/regulatory_gates.yaml`
are UNCERTAIN with no reviewer and no review date. UNCERTAIN is never PASS, `regulatory.evaluate_all` returns
NO_CONCLUSION for every strategy, and no favourable decision class is assigned anywhere in the package. 503B is
a time-varying legal state and never a durable pathway. Every document in the package carries the label
"preliminary regulatory analysis; not legal advice", and this packet does too. No interview, partner, customer,
pilot or regulatory opinion is asserted, because none has occurred. Reviewing this is not advising, endorsing,
or partnering, and it will never be described as any of those.

Paths are relative to `~/telo/feasibility/` unless they begin with `../`.

---

## 0. Sequencing: do not send this packet yet

*Internal note to the author. Delete this whole section before the packet is sent; the same gate is stated
in full in `docs/reviewer_packets/README.md` section 1.*

Two things have to be true first.

**(a) The open defects that carry the ranking are fixed. This condition is now met.** Revisions R009, R010
and R011, all dated 2026-09-05, land every one of them in code: NEW-1 (opening inventory seeded with no ledger
charge) under R009; MD-3 and MD-12 (a hard-coded regional review rule, and search spaces that were not matched
across architectures) and MD-11 (an optimizer tie-break with no Monte Carlo standard error tolerance) under
R010; MD-1 (the material buffer is a function of the lead time, fixed with a stated residual), NEW-2
(allocation rights inert), MD-23 (an exercise cadence that is nearly unmeasurable) and MD-24 (take-or-pay with
no service channel) under R011. NEW-3 (no readiness-decay hazard) is not addressed by them and stays open, as
do MD-5, MD-8, MD-15, MD-17, MD-18, MD-22 and MD-25. Each fix carries a test named for its id in
`tests/integration/test_ranking_defect_fixes.py`. Statuses: `docs/design_space/bottleneck_decomposition.md`
section 7, "Status after revisions R009 to R011".

**(b) The battery is re-run on the fixed engine.** This condition is not met. The gate statuses themselves do
not depend on the engine, but the lead times you are asked to price do: which architectures survive, and
therefore which reporting categories matter, is a post-fix question.

Only condition (b) is outstanding. A post-fix paired simulation exists
(`results/simulation/sim_post_R009/`, manifest 2026-09-06T03:02:03Z, 20 strategies, both products,
n = 100, at the illustrative baseline designs), but the optimization, ablation, design-space, matched-space,
figures and contract table have not been re-run on the fixed engine: `results/optimization/opt_20260906T032432Z/`
is an empty directory with that run still in flight. Every number below is therefore still a pre-R009 number.
Check `results/manifests/` for a completed post-R011 battery and confirm `make check` is green before sending.

---

## 1. What changed, and what this packet now asks for

The study was designed around one question: under what conditions does distributed regional capacity beat
safety stock, dual sourcing, reserved contract capacity, or added central capacity. Under the model's inputs
that question is answered, and the surviving shape is not a plant. It is a single approved presentation
supplied from US aseptic lines that are already registered and already inspected, bought as contracted
campaigns, paired with positioned finished-goods inventory
(`docs/design_space/strategic_synthesis.md`, answer to the governing objective).

That moves the regulatory questions to the centre. If adding a third-party sterile fill site to an approved
application is a prior approval supplement with a preapproval inspection rather than a scheduling delay, the
surviving shape loses its main advantage and the ranking changes. The package cannot answer that from public
documents, and it says so (`docs/design_space/prior_art_review.md` section 7).

So this packet asks two things. Attack the claim in section 2. Then assign a status to each of the sixteen
gates, with your name, the date and your rationale, so DF08 can move from zero reviewed.

---

## 2. The claim you are asked to attack

> Every regulatory constraint that would stop the surviving architectures is modelled as a lead time or a cap
> rather than as a bar. In particular, adding a named third-party sterile fill site to an approved application
> is treated as a scheduling delay (gate G07, treatment `lead_time`, with
> `second_source_qualification_days` base 365 days), not as a change whose category decides whether the
> architecture exists at all.

Where it lives. `config/regulatory_gates.yaml` holds sixteen gates, each with `treatment`, `model_effect`,
`legal_basis`, `applies_to_strategies`, `status`, `reviewer` and `review_date`. `src/telo_feasibility/
regulatory.py` turns a status plus a treatment into an eligibility and a model effect. The treatments in use
are `exclude_if_fail`, `lead_time`, `hard_feasibility`, `cap`, `dynamic_state`, `region_restriction`,
`no_fleet_claim` and `fallback_conventional`.

The sixteen gates as they stand:

| id | pathway | name | treatment |
|---|---|---|---|
| G01 | approved_cmo | Application ownership or binding CMO relationship | exclude_if_fail |
| G02 | approved_cmo | Manufacturing site in approved application; establishment registered and drug listed | lead_time |
| G03 | approved_cmo | Product, process and cleaning validation completed | hard_feasibility |
| G04 | approved_cmo | Aseptic processing or terminal sterilization validated | hard_feasibility |
| G05 | approved_cmo | Analytical methods transferred and validated | hard_feasibility |
| G06 | approved_cmo | Stability and container-closure evidence supports shelf life | cap |
| G07 | approved_cmo | Change-control category and FDA submission identified | lead_time |
| G08 | 503b | Outsourcing facility registered annually and CGMP-compliant | exclude_if_fail |
| G09 | 503b | Bulk substance eligible at compounding, distribution and dispensing dates | dynamic_state |
| G10 | 503b | Product not barred as essentially a copy | dynamic_state |
| G11 | 503b | Stability, BUD and sterility controls supported | cap |
| G12 | 503b | State licensure and distribution permissions mapped | region_restriction |
| G13 | distributed | Each unit or site registration and listing approach is supportable | lead_time |
| G14 | distributed | Cross-site comparability protocol accepted for the product | no_fleet_claim |
| G15 | release_assurance | Release model within a validated state of control with drift handling defined | fallback_conventional |
| G16 | approved_cmo | Alternate component, container-closure and API source qualified and authorised | lead_time |

G16 was added by protocol revision R007, taking the set from fifteen to sixteen.

Ways to kill the claim that would count: G07 is a prior approval supplement with a preapproval inspection for
the change as described, and 365 days is the wrong order of magnitude; the category depends on the receiving
site's inspection state in a way a single lead time cannot represent; G02 and G07 are the same event and
double-count or under-count the delay; a gate that is modelled as a lead time or a cap is actually a bar; or
the eight treatments are the wrong abstraction and a binary gate cannot represent how any of this works.

---

## 3. Read in this order

1. `docs/design_space/strategic_synthesis.md`, the answer to the governing objective plus sections 2 item 5,
   9 and 10. Section 2 item 5 lists the constraints the package believes no design choice reaches, and those
   are the ones most worth your disagreement.
2. `config/regulatory_gates.yaml`, all sixteen entries, including `legal_basis`, `legal_basis_type`,
   `sources`, `notes` and the empty `reviewer` and `review_date` fields you are being asked to fill.
3. **Optional, code.** `src/telo_feasibility/regulatory.py`, so you can see exactly what a status does to a
   strategy. It is short. In plain English: a gate is PASS, FAIL, UNCERTAIN or NOT_APPLICABLE; a FAIL on an
   `exclude_if_fail` or `hard_feasibility` gate removes the strategy, a FAIL or UNCERTAIN on a `lead_time` gate
   adds days before the site can supply, a `cap` gate limits shelf life or inventory, and anything not PASS
   leaves the strategy at NO_CONCLUSION.
4. `docs/regulatory/approved_generic_cmo_map.md` and `docs/regulatory/503b_shortage_response_map.md`.
5. `docs/design_space/prior_art_review.md` section 4 (regulatory basis), section 6 (six unoccupied
   intervention points, four of which are unoccupied because of a barrier rather than an oversight), and
   section 7, which lists ten regulatory questions the document sweep could not resolve. Those ten are, in
   effect, the interview.
6. `docs/design_space/architecture_taxonomy.md`, incompatibilities 2, 3, 4 and 7.
7. `CLAIMS_REGISTER.csv`, so you can see which of our own public statements we have already recorded as
   contradicted, and check that this packet does not repeat them.

Result artifacts, in order:

| Artifact | What it is |
|---|---|
| `results/design_space/ds_post_R008/summary.json`, `meta.eligibility` | NO_CONCLUSION for all twenty strategies, which is what UNCERTAIN produces |
| `results/deterministic/` | the deterministic screen, which is where gate lead times and caps bite first |
| `results/design_space/ds_post_R008/thresholds.csv` | the conditions each architecture needs; the activation-latency and qualification rows are the ones your categories price |
| `results/manifests/*.json` | protocol version and hash, config hashes, gate outcomes recorded per run |

Every run made before 2026-09-03 is superseded for quantitative use.

---

## 4. Reproduction that works today

**Optional.** Nothing in your review depends on running any of this. It is here so that nothing in the packet
has to be taken on trust.

```
cd ~/telo/feasibility
uv sync --all-extras
uv run python -m telo_feasibility.cli status           # DF08 prints reviewed 0/16 and lists every UNCERTAIN gate
uv run python -m telo_feasibility.cli protocol verify   # source-document hashes
make check
```

The last recorded gate run is `results/manifests/test_report.json`: 243 passed, 0 failed, 0 skipped,
2026-09-06T02:59:55Z. Re-read that file at send time and quote whatever it then holds.

To see what a status change does, and only if you want to, edit a `status` field in
`config/regulatory_gates.yaml` on a scratch branch and re-run the deterministic screen and the eligibility
summary:

```
uv run python scripts/run_deterministic.py --reconcile
uv run pytest tests/unit/test_configs_and_regulatory.py -q
```

Nothing in the package assumes the answer will be favourable. If a gate you assign turns an architecture off,
that is the correct behaviour and it is what the gates exist for.

---

## 5. Known model defects and known bad claims. Skip these

Already recorded. Full model-defect register with measured effects:
`docs/design_space/bottleneck_decomposition.md` section 7, including the appended "Status after revisions R009
to R011" table. The ones that touch the regulatory layer:

| id | defect | status |
|---|---|---|
| MD-18 | `release_time_factor` is a frozen design variable the stochastic engine never reads, so the strategy built to test a reduced release layer is numerically identical to the one without it | open |
| MD-15 | one product per network, one presentation, one market, one labeler, so every portfolio, postponement and shared-filing argument is an accounting proxy | open, recorded as scope |
| MD-22 | the deterministic screen's common-impact input is derived from topology for some strategies and hand-set for others, so the two arms are not comparable | open |
| MD-25 | the shared-operating-layer cost is charged only outside the base release scenario, so a shared quality or software layer carries hazard with no cost line | open |
| NEW-2 | allocation rights were inert; all four allocation policies collapsed to proportional, so any right a contract or a shortage rule would confer had no channel | fixed, R011: regions may now carry criticality weights and a minimum guarantee, and the guarantee reaches the allocator. With identical regions three of the four policies still return the same fill, which is arithmetic, and the default keeps regions identical |
| MD-20, MD-21 | the deterministic screen dropped reserved sites and charged the reservation fee before the line existed | fixed, R007 |

**Claims already withdrawn or corrected.** Do not spend time telling us these are wrong; we know, and the
register records it. `CLAIMS_REGISTER.csv` rows C009, C010, C015 and C023 cover the public statements about
release time, automated release, product positioning and what currently exists. Their wording is not repeated
in this packet and may not be repeated anywhere. Row C025 records that an internal memo
attributed a sentence to section XI.B of the 2004 aseptic guidance that is not in the guidance. The register
also records that the sterility-is-the-critical-path conclusion does not depend on that sentence: the 14-day
pole comes from USP `<71>` incubation and from samples being drawn during the fill. We are telling you this
because it is our own extraction error and you should assume there are others, not because the pole is
unsupported.

---

## 6. The three things the author most suspects are wrong here

**6.1 G07's category, and whether a category can be a lead time at all.** Everything in the surviving shape
runs through it. The package treats adding a named third-party sterile fill site to an approved application as
a delay of `second_source_qualification_days` (180 / 365 / 730, source locator "study placeholder; gate G07
lead time to be elicited"). If the honest answer is a prior approval supplement with a preapproval inspection,
one contracted strategy loses its 365-day leg outright and the whole contracted family weakens
(`docs/design_space/os_only_and_virtual_network.md` section 6.2 item 1). The author also suspects the modelling
shape is wrong even if the number is right, because the category plausibly depends on the receiving site's
CGMP compliance state at implementation, and a fixed lead time cannot carry that.

**6.2 The legal and technical basis for treating sterility incubation as an unremovable pole.** The engine
holds every batch for the maximum of the concurrent release components, and sterility at 14 days is the argmax
at every corner of the declared box. Its basis is USP `<71>` incubation, recorded at evidence tier 1; the
internal memo that also discusses it carries a separate misattribution recorded as C025, and we would like you
to check the tier-1 basis rather than take the memo's word for anything. Three specific questions. Does USP `<71>` plus current FDA expectations actually require the incubation to
complete before release for an aseptically filled aqueous small-molecule solution? Is there any marketed US
aseptically filled small-molecule injectable releasing on a rapid microbiological method rather than the
compendial test, and if so under what filing? And can an approved parametric release programme extend to a
second site or a second autoclave, or is it a per-site and per-autoclave asset? The third question decides
whether process-route conversion is an intervention at all, and it is the only intervention found across
fourteen prior-art families that acts on the binding constraint rather than on components that are not binding
(`docs/design_space/prior_art_review.md` section 6.1).

**6.3 One quality unit across several registered sites, and the 503B state machine.** Every multi-site design
in the battery implicitly assumes a disposition arrangement the package has never had checked: may one quality
unit perform batch disposition for several registered sites under one application, may several sites share one
filing, and what must each site still hold of its own (queue id HA-42)? The package's current reading is that
batch disposition is non-delegable, that an extramural facility is an extension of the manufacturer, and that a
quality agreement cannot delegate CGMP responsibility, but that reading is ours, not a professional's. On the
503B side, gates G09 and G10 model the bulks-list eligibility and the essentially-a-copy bar as a dynamic
state, with `shortage_list_resolution_rate_per_year` and `shortage_list_relisting_rate_per_year` turning the
pathway on and off. Is that state machine faithful to how 503B(a)(2) and 503B(a)(5) actually operate, including
what happens to a product line when a listing ends?

---

## 7. What we are actually buying

The primary deliverable is HA-31: a status for each of the sixteen gates, with your name, the date and your
rationale. The statuses available are the ones in `config/regulatory_gates.yaml`. UNCERTAIN is a legitimate
answer and stays UNCERTAIN in the model, which means the affected strategies stay ineligible. Please do not
soften an UNCERTAIN into a PASS to be helpful; a PASS you would not defend is worse for us than an honest
UNCERTAIN.

Alongside that:

| Queue id | What is needed | Enters at |
|---|---|---|
| HA-23 | Is adding a named third-party sterile fill site to an approved application a CBE-30-class change or a prior approval supplement with a preapproval inspection? Plus 503B transitions and cross-site claims | gate G07 category; the activation and qualification lead used by the contracted strategies |
| HA-34 | For each candidate presentation, is the marketed product terminally sterilized or aseptically processed, and for terminal products what is the cycle | `ProductFeatures.sterilization_route`; whether the release pole is a constant or a design variable |
| HA-42 | May one quality unit perform disposition for several registered sites under one application, may several sites share one filing, and what must each site still hold | fixed QA labour per site; `validation_factor`; the shared-quality common-cause group |
| HA-31 | The sixteen gate statuses with reviewer and date | `config/regulatory_gates.yaml` `status`, `reviewer`, `review_date`; DF08 |

Ranges are acceptable and preferred. "Between 6 and 18 months depending on inspection state" is a better answer
than a single number, and it is representable: every lead-time input in the model carries a low, base and high.

The ten unresolved regulatory questions in `docs/design_space/prior_art_review.md` section 7 are open to you as
well. Any one of them answered with a citation is worth more than a general assessment of the approach.

---

## 8. Current limitations, stated before you find them

- Zero of sixteen gates are reviewed. DF08 is open and every decision class in the package depends on it.
- `docs/audits/05_inconsistencies.md`; `docs/audits/04_requirements_matrix.csv` status column;
  `reports/appendices/limitations.md`.
- The 503B pathway is modelled as a time-varying state driven by two illustrative rates. Neither rate has a
  source.
- The prior-art sweep records its own blind spots in `docs/design_space/prior_art_review.md` section 1.4, and
  several families record their exhaustive negatives as unverified.
- Nine of twenty-two definition-of-finished tests pass, and eleven of the thirteen incomplete ones cannot be
  closed by code.

---

## 9. The form the review should take

Write it however you like. We convert it into `docs/reviewer_packets/reviews/<review_id>.json` with the schema in
`docs/reviewer_packets/reviews/README.md`, and we send you the converted file to correct before it is counted. Two parts.

**Part one, the gate table.** For each of G01 to G16: your status, your rationale, and the documents you rely
on. We record your statuses and rationales against a role-only reviewer id. Your name goes into
`config/regulatory_gates.yaml` only if you authorise it in writing after seeing the file, and we will tell you
at that point whether the repository is public; repository visibility and commit-history exposure are both
still open items in our own queue (HA-06 and HA-07). If you will not be named, we log your statuses as an
unnamed professional reading that does not close DF08. That is an acceptable outcome and we would rather have
it than a name you did not intend to give.

We can send you the gate table on its own, ahead of the packet, so it can be cleared with an employer before
you start. Ask, and it goes out as one page.

**Part two, per issue.**

1. **The issue**, tied to a gate id, a treatment, or a line of the claim in section 2.
2. **What you would use instead**: a category, a lead time with a range, a citation, or a named role who would
   know.
3. **What it changes if you are right**: which strategy or which result you expect to move.
4. **Confidence**, in your own terms, and whether you are speaking from filings you have made or from a reading
   of the statute and guidance.

We record our decision against each issue, accepted, partially accepted, or rejected, with the rationale and
the exact model change, and append a row to `docs/reviewer_packets/reviews/revision_log.csv`. Rejections get the same written
rationale as acceptances.

Please also say plainly: **what in this package you would refuse to sign your name to.** A review that turns
several gates to FAIL and removes architectures is a complete and successful review.

Attribution is by role and organisation type only unless you authorise more in writing, with one exception you
should decide on before you start. The gate table in section 9 part one is recorded with a named reviewer and a
date in `config/regulatory_gates.yaml`, because a gate status counts for nothing without one, and that file is
published with the package. If you will not be named, say so and we will log your statuses as an unnamed
professional reading that does not close DF08; that is an acceptable outcome and we would rather have it than a
name you did not intend to give. Nothing you say will be
described as a partnership, an endorsement, a customer relationship, a pilot, a regulatory clearance, or an
agency position. Your review is a professional reading logged in a research package, and the package will
continue to carry the label "preliminary regulatory analysis; not legal advice".
