# Definition-of-finished status (deliverable 22)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every model result named below is behavior under
tier-5 illustrative inputs and describes the model, not sterile-injectable manufacturing. All sixteen regulatory
gates in `config/regulatory_gates.yaml` are UNCERTAIN, so no strategy carries a favorable decision class. 503B is a
time-varying legal state in this package and never a durable pathway.

Written 2026-09-05. The output in section 1 was produced at 2026-09-05T05:54Z from the package root.

---

## 1. The status command and its output, verbatim

```
$ cd ~/telo/feasibility && make status
uv run python -m telo_feasibility.cli status
PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS
definition of finished: 9/22 complete

DF01 ---- protocol version frozen
      protocol v1.0.0 status=frozen; revisions pending sign-off: ['R000', 'R001', 'R002', 'R003', 'R004', 'R005', 'R006', 'R007', 'R008']
DF02 PASS five-product dated screen complete
      screen_manifest.json candidates=6, dated snapshots=True
DF03 ---- [human] two exact product presentations selected
      selection.json selected=0
DF04 ---- product dossiers complete
      complete dossiers=0
DF05 ---- all eight strategies represented
      strategies in simulation manifests: ['S0', 'S1', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
DF06 PASS strategies optimized to matched service targets
      optimization summaries=6
DF07 PASS approved-generic/CMO and 503B pathways separated
      decision maps present=[True, True]
DF08 ---- [human] material regulatory gates reviewed by a qualified expert
      reviewed 0/16; UNCERTAIN: ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
DF09 ---- no material illustrative input remains
      illustrative=87, missing=0 of 91 parameters
DF10 ---- [human] direct or expert-validated input distributions documented
      same evidence as DF09 plus distribution records
DF11 PASS deterministic model reconciles with workbook
      results/deterministic/reconciliation.json ok=True
DF12 PASS stochastic simulation passes all tests
      test_report.json={'generated_at': '2026-09-03T22:02:21.007228+00:00', 'passed': 230, 'failed': 0, 'skipped': 0, 'crn_test_passed': True, 'common_cause_test_passed': True, 'mass_balance_property_passed': True, 'exit_code': 0}; simulation manifests=3
DF13 PASS common random numbers implemented
      requires test_report.json crn_test_passed
DF14 PASS common-cause failures represented
      requires test_report.json common_cause_test_passed
DF15 ---- historical backcasts complete
      backcast comparisons=0 (need >= 4 episode classes)
DF16 PASS global and structural sensitivity complete
      results/sensitivity/summary.json present=True
DF17 PASS decision-reversal and value-of-information analyses complete
      decision_reversal.json and voi.json present=True
DF18 ---- [human] real interview evidence logged
      completed interviews logged=0 (target 25-30)
DF19 ---- [human] at least three qualified independent reviews completed
      completed reviews=0
DF20 ---- [human] public code, data dictionary, assumptions, model cards, run manifest, revision log, and limitations released
      public_release.json=absent
DF21 ---- at least one non-obvious result identified
      nonobvious_finding.json=absent
DF22 ---- [human] external claims do not exceed evidence
      claims register rows unsupported/contradicted/retracted: ['C001', 'C007', 'C008', 'C009', 'C010', 'C012', 'C013', 'C015', 'C016', 'C017', 'C018', 'C023', 'C024', 'C025']
```

---

## 2. The headline, stated plainly

**Nine of twenty-two tests are complete.** That is one fewer than the ten recorded in `HANDOFF.md` line 20 at the end
of session 1. Nothing in the package got worse. DF05 moved from PASS to incomplete because its criterion is an
equality on a count of strategy ids, and Phase D added twelve strategies. Section 4 gives the detail.

**Thirteen tests are incomplete. Eleven of them cannot be closed by any amount of code.** They wait on a founder
decision, a dataset a person has to buy or request, an interview, a qualified regulatory or operations reviewer, or an
authorization. The two exceptions are DF05, which waits only on a two-line change to `reporting.finished_status`, and
DF15, which waits on a glob fix plus a fourth backcast episode class that itself needs a human-acquired source.

That distribution is the honest summary of where this package stands. The modelling work has run ahead of the
evidence. Adding engine features, strategies, or analyses will not move the count. The queue in
`../audits/07_human_action_queue.md` will.

---

## 3. The twenty-two tests

The criterion column states what `reporting.finished_status` actually measures, because several tests are narrower
than their titles. Human-action ids refer to `../audits/07_human_action_queue.md`.

| id | test | state | criterion in `reporting.finished_status` | what changed this session | what still blocks it | human action that closes it |
|---|---|---|---|---|---|---|
| DF01 | protocol version frozen | incomplete | protocol status is `frozen` and no `protocol/revisions.csv` row has "pending" in `approved_by` | six revisions were added: R003 material carrying cost, R004 and R005 the model-defect fixes, R006 the Phase D configuration of the twelve design-space strategies S8 to S19, R007 the verification-pass corrections and gate G16, R008 the commissioning clock. The pending list grew from three rows to nine | all nine revisions R000 to R008 read "pending founder sign-off" | **HA-02**, which today names only the R001 thresholds. It must be widened to cover R000 to R008, since R004, R005, R007 and R008 changed decision-relevant model behavior after the session-1 results were produced |
| DF02 | five-product dated screen complete | **PASS** | `screen_manifest.json` has at least five candidates and dated snapshot ids | nothing | none | none |
| DF03 | two exact product presentations selected | incomplete | `selection.json` lists exactly two selected presentations | `product_architecture.py` and `results/design_space/product_features.csv` now give one feature record per longlist presentation, so a selection would have a feature layer to stand on. Four decision-relevant features are still absent for every candidate | no presentation has been selected, and the features that would justify a selection are unavailable. `product_architecture_matching.md` section 5 states that the honest output over this longlist today is a partition into capacity-short and capacity-adequate and nothing finer | **HA-03** (does furosemide join the longlist, at which fill volume), **HA-18** (primary-source shortage check), **HA-34** (sterilization route), **HA-35** (substitution difficulty), **HA-36** (contractability) |
| DF04 | product dossiers complete | incomplete | exactly two presentations selected and at least two `dossier.json` files with `status: complete` | nothing on the dossiers themselves | DF03 is upstream of it; the dossiers also lack presentation-level shortage history and a demand denominator | **HA-03** first, then **HA-10** (ASHP bulletins), **HA-11** (utilization), **HA-12** (supplier quotes) |
| DF05 | all eight strategies represented | incomplete | the set of distinct strategy ids across `results/manifests/sim_*.json` has size **exactly 8** | Phase D added S8 to S19 and the simulation manifests now carry twenty ids. The eight frozen comparators S0 to S7 are all still present | the criterion, not the package. `len(strategies_seen) == 8` fails at twenty as surely as at seven | **none.** This is a code fix: test that `FROZEN_STRATEGY_IDS` is a subset of the ids seen. See section 4 |
| DF06 | strategies optimized to matched service targets | **PASS** | at least one `results/optimization/*/summary.json` exists | four optimization runs were added (`opt_20260903T181601Z`, `opt_20260903T182509Z_tau0.98`, `opt_20260903T220534Z`, `opt_20260903T231408Z_tau0.98`), taking the count from two to six, and `scripts/run_matched_space_check.py` added the matched-search-space check `results/design_space/matched_20260905.json` | none for the test. The test only counts files; it does not check that the runs are current or comparable | none |
| DF07 | approved-generic/CMO and 503B pathways separated | **PASS** | both decision maps exist under `docs/regulatory/` | nothing | none | none |
| DF08 | material regulatory gates reviewed by a qualified expert | incomplete | every gate has a `reviewer` and none is UNCERTAIN | gate G16 was added by revision R007 (component and container-closure lot qualification, plus the alternate API source's Type II DMF letter of authorization) for S9, S18 and S19. The denominator moved from fifteen to sixteen | zero of sixteen gates have a named reviewer; all sixteen are UNCERTAIN | **HA-31** assigns status with a name, date and rationale; **HA-23** supplies the professional reading. G07's reporting category is the single highest-value gate answer, since it decides whether a third-party fill site is a CBE-30-class change or a prior-approval supplement with a preapproval inspection |
| DF09 | no material illustrative input remains | incomplete | no parameter in the global set or any product set is marked `illustrative` | Phase G added one tier-5 global parameter, `wrong_release_cost_usd`, with provenance and an explicit illustrative tier. The current count is 87 illustrative of 91 parameters, 0 missing | 87 parameters have no evidence behind them, including every demand, cost, capacity, lead-time and disruption input | **HA-11**, **HA-12**, **HA-13**, **HA-14**, **HA-17**, **HA-21**, **HA-22**, and **HA-39** for the common-cause rate, which no queue row asked for before this session |
| DF10 | direct or expert-validated input distributions documented | incomplete | same as DF09, plus a non-empty parameter set | nothing beyond DF09 | a distribution is not a point estimate, and none of the 87 has an elicited or measured distribution | **HA-20** to **HA-25** for the elicitation, reviewed by **HA-30** to **HA-33** |
| DF11 | deterministic model reconciles with workbook | **PASS** | `results/deterministic/reconciliation.json` has `ok: true` | the deterministic screen gained a runtime-derived path for S8+ (`deterministic.screen_inputs`, R121). The workbook replica refuses a declared topology, so the 448 of 448 reconciliation is unchanged and still exact | none | none |
| DF12 | stochastic simulation passes all tests | **PASS** | `test_report.json` has `failed == 0` and `passed > 0`, and at least one simulation manifest exists | the suite grew from 100 tests to 230, all passing, generated 2026-09-03T22:02:21Z. New tests cover ablation, the design-space engine, warm standby and activation failure, contracting, design-space analysis, product-architecture features, the release-benchmark extensions, and 27 model-defect fixes | none for the test. It does not check that the stored report is current with the working tree | none |
| DF13 | common random numbers implemented | **PASS** | `test_report.json` `crn_test_passed` | new streams were added (`RandomStream.ACTIVATION`) without disturbing the paired-run property | none | none |
| DF14 | common-cause failures represented | **PASS** | `test_report.json` `common_cause_test_passed` | R007 (MD-19) made a supplier's daily capacity a fraction rather than a switch, so a common-cause group declared on a supplier is no longer structurally inert | none | none |
| DF15 | historical backcasts complete | incomplete | at least four files match `results/backcasts/*/comparison.json` | the three episodes were re-run after the model-defect fixes as `back_20260903T214759Z` | two things. First, the glob is one directory level too shallow: the six `comparison.json` files that exist sit at `results/backcasts/<run>/<episode>/comparison.json`, so the check counts zero. Second, even with the glob fixed there are only three distinct episodes, all ongoing shortages of the same class, which is not four episode classes. `HANDOFF.md` section 5 records the same gap | the code half needs no person. The fourth episode class needs a documented single-site failure episode, which needs **HA-10** (ASHP bulletins, the only presentation-level shortage history) and **HA-11** for the demand denominator to score it against |
| DF16 | global and structural sensitivity complete | **PASS** | `results/sensitivity/summary.json` exists | nothing. The sensitivity battery was not re-run | none for the test. See section 5: the artifact it checks is superseded | none |
| DF17 | decision-reversal and value-of-information analyses complete | **PASS** | `decision_reversal.json` and `voi.json` both exist | nothing | none for the test. See section 5 | none |
| DF18 | real interview evidence logged | incomplete | at least 25 files under `data/interview_evidence/` with `status: complete` | the design-space work identified three interview roles that had no queue row: the OS buyer (**HA-37**), the purchaser of standing availability (**HA-38**), and the regional stocking point whose replenishment rule decides 8 of 16 Phase A cells (**HA-40**) | zero interviews have been held. The infrastructure in `docs/interviews/` is complete and empty by design | **HA-20** to **HA-25**, plus **HA-35**, **HA-37**, **HA-38**, **HA-40**, **HA-43** |
| DF19 | at least three qualified independent reviews completed | incomplete | at least 3 files under `docs/reviewer_packets/reviews/` with `status: complete` | nothing. Four packets exist and none is populated | no reviewer has been engaged | **HA-30** (manufacturing and quality), **HA-31** (regulatory), **HA-32** (operations research), **HA-33** (hospital pharmacy, GPO or wholesaler) |
| DF20 | public code, data dictionary, assumptions, model cards, run manifest, revision log, and limitations released | incomplete | `results/manifests/public_release.json` has `released: true` | nothing was published, by instruction | no authorization to commit, and a live privacy exposure that must be closed before anything is published | **HA-05** (commit authorization) and **HA-01** (location and license), but **HA-06**, **HA-07** and **HA-08** come first: `github.com/rikhinkavuru/Telo` is public today and exposes contact files for 29 people in one file and up to 18 more in another |
| DF21 | at least one non-obvious result identified | incomplete | `results/manifests/nonobvious_finding.json` has a `finding` key | the candidate file grew to nine entries. NF-9 was added (the matched-search-space correction: added central capacity S4 meets the frozen target on both products once searched over a common inventory space, at 20.0 M and 23.7 M USD per year against 37.8 M and 38.6 M under its declared space). NF-8 was suspended pending the model-defect fixes | the author has not adopted a candidate. Adoption is a judgement about what the package is willing to stand behind, not a computation | **HA-44**, a new row. The author reviews `results/manifests/nonobvious_finding_candidates.json` and writes one adopted finding to `results/manifests/nonobvious_finding.json` with its evidence pointer |
| DF22 | external claims do not exceed evidence | incomplete | no `CLAIMS_REGISTER.csv` row has `evidence_status` starting with unsupported, contradicted or retracted | the register was extended from C010 to C025. C025 records a contradicted citation in the repository's own release memo. `public_claims_corrections.md` gives replacement text for every affected public sentence | fourteen rows are unsupported, contradicted or retracted, and none of the public surfaces has been edited | **HA-04**, which must be widened from four claims to the full C001 to C025 list per `public_claims_corrections.md` section 4; then **HA-05** to commit, **HA-19** to settle which Phlow figure the company quotes, and **HA-10** to fix the release-memo citation |

---

## 4. The one test that is blocked only by code

DF05 asks whether all eight strategies are represented. The check is:

```python
len(strategies_seen) == 8
```

where `strategies_seen` is the union of `strategy_ids` across `results/manifests/sim_*.json`. Phase D added S8 to
S19, so the union now has twenty members and the equality fails. Every one of the eight frozen comparators is
present, which is what the test was written to establish.

The fix is to test membership rather than cardinality: that `FROZEN_STRATEGY_IDS` is a subset of `strategies_seen`,
optionally reporting the design-space ids separately. That change is in `src/telo_feasibility/reporting.py` and
belongs with a test, not in this document. It is not made here because this session's task was to report status, and
because moving a definition-of-finished criterion is a protocol-adjacent act that should carry its own note.

DF15's first blocker is the same kind of defect. `(RESULTS / "backcasts").glob("*/comparison.json")` searches one
directory level below `results/backcasts/`, but the writer puts each comparison at
`results/backcasts/<run>/<episode>/comparison.json`. Six such files exist and the check counts zero. Fixing the glob
raises the count to six but still does not satisfy the test's intent, because those six are three episodes run twice
and the test wants four episode classes.

---

## 5. Three tests that pass on file presence rather than on current evidence

This section exists because the count of nine overstates the package in three places, and a status document that does
not say so is not useful.

1. **DF16 and DF17 check that files exist.** `results/sensitivity/summary.json`, `decision_reversal.json` and
   `voi.json` were all written on 2026-09-02, before revisions R003 to R008. They cover S0 to S7 only, on designs from
   `opt_20260902T043854Z`, and the one-way sweep behind them ran at six runs per scenario, where the `p_meet` column
   carries no information. `product_architecture_matching.md` section 5 item 4 and `inventory_capacity_hybrids.md`
   section 6 item 7 both record that these artifacts are superseded and that no number from them may be quoted. Both
   tests still read PASS. Re-running the battery over S0 to S19 on post-R008 designs is in-model work that needs no
   person, and it is the highest-leverage missing artifact in the package.
2. **DF12 checks a stored report, not the working tree.** `test_report.json` was generated 2026-09-03T22:02:21Z with
   230 passing tests. The check does not re-run anything and does not compare the report to the current code. Before
   any external use of the package, `make check` and `scripts/run_tests_report.py` should be run again.
3. **DF06 counts optimization summaries.** Six exist. The check does not ask whether they are mutually comparable,
   and `feasibility_regions.md` section 8 shows they are not: the frozen comparators searched safety stock to 90 or
   120 days while the design-space strategies searched to 365 days with a daily base-stock review, which is model
   defect MD-12. The matched-space run corrects four strategies of twenty.

---

## 6. What would actually move the count

Ranked by tests closed per action, using the priority ranks in `../audits/07_human_action_queue.md`.

| action | tests it closes or unblocks | note |
|---|---|---|
| A code change to the DF05 criterion | DF05 | the only test in the list that closes without a person. Takes minutes |
| **HA-02** widened to R000 to R008 | DF01 | one founder signature. It is also a precondition for reading any optimization result as a decision rather than as model behavior |
| **HA-31** with **HA-23** | DF08, and unblocks DF19 in part | sixteen gate statuses with a reviewer name and date. Until then no strategy can receive a favorable decision class |
| **HA-03** with **HA-18**, **HA-34**, **HA-35**, **HA-36** | DF03, then DF04 | product selection is a founder decision resting on four features nobody has supplied |
| **HA-06**, **HA-07**, **HA-08**, then **HA-05** and **HA-01** | DF20 | the privacy exposure is live today and must close before anything is published |
| **HA-04** widened to C001 to C025, with **HA-19** and **HA-10** | DF22 | fourteen register rows |
| **HA-44** | DF21 | the author adopts one of the nine candidates |
| **HA-11**, **HA-12**, **HA-13**, **HA-14**, **HA-17**, **HA-21**, **HA-22**, **HA-39** | DF09, then DF10 | 87 illustrative parameters. This is the largest single block of work in the queue and the one that decides whether any number in this package means anything |
| **HA-20** to **HA-25**, plus **HA-35**, **HA-37**, **HA-38**, **HA-40**, **HA-43** | DF18, and most of DF10 | 25 to 30 conversations |
| **HA-30** to **HA-33** | DF19 | four independent reviews |
| a glob fix plus a fourth episode class from **HA-10** and **HA-11** | DF15 | half code, half evidence |

---

## 7. The honest reading

Nine of twenty-two is not a project that is 41 percent finished. The nine that pass are the ones a coding agent can
close on its own: a dated screen, a reconciliation, a test suite, a set of runs, two documents. The thirteen that do
not pass are the ones that decide whether the package is about the world. Every gate is UNCERTAIN, 87 of 91 inputs
are illustrative, no interview has been held, no independent review has been completed, no product has been selected,
and no external claim has been reconciled with its evidence.

Nothing in this document, and nothing in this package, should be read as a finding about sterile-injectable
manufacturing until those thirteen move.
