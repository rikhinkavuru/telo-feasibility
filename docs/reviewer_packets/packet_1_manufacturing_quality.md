# Review packet 1: Sterile-injectable manufacturing and quality

Reviewer id `reviewer_1` (`protocol/protocol.yaml` `independent_review`); queue id HA-30. You can reject the
process and cost assumptions, and rejecting them is the point.

**Status: not sent. No review has been completed.**

**How long this takes.** Full review: about four hours, most of it in sections 2, 6 and 7. **If you have one
hour: read section 2, answer section 7, and stop.** That is a complete and useful review. Reading code is
optional throughout this packet; section 3 item 4 exists for people who want it, and the mechanisms you need
are stated in plain English in section 2 and section 6.1. No compensation is offered, and we say so before you
spend the time.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every input named below is evidence tier 5
(illustrative) except four release components. Nothing here is a statement about sterile-injectable
manufacturing in the world, and nothing here is legal or regulatory advice. All sixteen regulatory gates are
UNCERTAIN with no reviewer, so no strategy carries a favourable decision class. No interview, partner,
customer, pilot or regulatory opinion is asserted, because none has occurred. Reviewing this is not advising,
endorsing, or partnering, and it will never be described as any of those.

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

**(b) The battery is re-run on the fixed engine and the cost and service numbers below are replaced.** This
condition is not met.

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
that question is answered. Distributed owned nodes meet the frozen service target in no region of any recorded
range of any swept input, on either product, and giving them the same inventory freedom that makes the
alternatives feasible does not rescue them (`docs/design_space/feasibility_regions.md` section 6 family 1, and
section 8). So this packet no longer asks whether distributed manufacturing is a good idea.

It asks two things. Attack the claim in section 2. Then give numbers, with ranges, for section 7. Because 87 of
91 parameters are illustrative, an opinion about architecture changes nothing in this model and a measured
number changes a great deal. A range is a better answer than a point estimate, and "I do not know, and here is
who would" is a useful answer.

---

## 2. The claim you are asked to attack

> Under the model's process and cost inputs, a small owned aseptic node is dominated on both service and cost by
> contracting campaigns at already-registered US lines, and the release layer is not the reason. In the model,
> for an aseptically filled aqueous small-molecule solution in a glass vial, the release hold is computed as the
> maximum of the concurrent components plus serial QA review, so sterility incubation is the critical path and
> removing the entire chemical queue removes 2 of 16 days. That concurrency structure is an assumption we wrote,
> not a measurement, and section 6.1 says why we distrust it.

Where each half lives:

- **The release half.** `ManufacturingSite.release_time_days` in `src/telo_feasibility/schemas.py` takes the
  maximum of the concurrent components and adds anything recorded under `qa_review_serial`. The components are
  assembled in `src/telo_feasibility/strategies.py` (the `components` dict) from `config/global.yaml`:
  sterility 14 (low 14, high 18), environmental monitoring 7 (5, 7), assay 5 (1, 7), endotoxin 2 (0, 3), QA
  review serial 2 (0, 4). Sterility is the argmax at every corner of that box, because the concurrent chemical
  maximum tops out at 7 against sterility's low of 14
  (`docs/design_space/bottleneck_decomposition.md` sections 6.6 and 6.7).
- **The cost and service half.** Cost per delivered unit at the starting designs is about 41 and 43 USD for
  the two owned-node strategies against about 14 for the contracted campaign network in the same table, and
  owned nodes lose about 29% of the measured window to commissioning, which is roughly 520 capacity-weighted
  days of 1826, against 0% to about 9% for the contracted designs
  (`docs/design_space/os_only_and_virtual_network.md` section 3.2). These are engine outputs, quoted here at two
  significant figures; the inputs behind them carry no precision at all, and the artifact prints them to six
  decimal places only because that is what the engine emits.

Ways to kill it that would count: environmental monitoring does not run concurrent with incubation at a real
site; QA review is a queue with a variable arrival rate rather than a 2-day serial constant; assay does not
start until incubation reads out; the release clock does not start at fill; a marketed aseptically filled
product releases before day 14 by a route the model does not carry; or the cost ledger is missing a line large
enough to move the ordering.

---

## 3. Read in this order

1. `docs/design_space/strategic_synthesis.md`, the answer to the governing objective and sections 1 and 2.
   Twelve pages. It is the whole argument and the fastest way to see what you are attacking.
2. `config/global.yaml`, the release block (`sterility_incubation_days` through `qa_review_days`), the
   disruption block, and the node block (`node_commissioning_days`, `capacity_expansion_days`,
   `second_source_qualification_days`, `reserved_capacity_activation_days`, `reserved_capacity_fee_fraction`,
   `node_scale_fraction`, `node_capital_scale_exponent`, `node_fixed_cost_scale_exponent`). Every value carries
   `evidence_tier` and `source_locator`. Read the source locators; most of them say "study placeholder".
3. `config/products/sodium_bicarbonate_8_4_50ml.yaml` and `config/products/norepinephrine_1mgml_4ml.yaml`,
   the twenty parameters each. These are the batch, yield, uptime, cycle, changeover, capital, fixed QA,
   validation and testing inputs.
4. **Optional, code.** `src/telo_feasibility/schemas.py`, `ManufacturingSite` and `release_time_days`. Then
   `src/telo_feasibility/strategies.py`, the node scaling block (`node_scale`, `cap_exp`, `fix_exp`) and the
   release-component assembly. Then `src/telo_feasibility/production.py`, `SiteRuntime`, for how a batch runs,
   how a deviation restarts it, and how a degraded line is stretched.
5. `docs/design_space/bottleneck_decomposition.md` section 6.6 and 6.7 (the release pole) and section 7 (the
   defect register).
6. `docs/regulatory/approved_generic_cmo_map.md` for what the package believes about the two presentations,
   including the unresolved sterilization route for sodium bicarbonate 8.4%.

Result artifacts, in order:

| Artifact | What it is |
|---|---|
| `results/simulation/sim_post_R008/summary.json` | paired baseline, 20 strategies, both products, n = 100, master seed 20260901 |
| `results/design_space/ds_post_R008/dominance.csv` | cost against service at each strategy's optimized design, 40 paired runs |
| `results/design_space/contract_conditions_sim_post_R008.csv` | the cost decomposition; fixed plus resilience cost is 81.0% to 93.7% of annual cost for all eight comparators |
| `results/ablation/abl_post_R008/summary.json` | 42 ablation configs at n = 60; keys are `<config>|<product>|<strategy>` |
| `results/figures/design_space_ds_post_R008_*_dominance.png` | the frontier plots, each with a `.meta.txt` naming its run |
| `results/manifests/*.json` | protocol version and hash, config hashes, git commit, seed, n_runs for every run above |

Every run made before 2026-09-03 is superseded for quantitative use. Do not read `abl_20260902_phaseA`,
`sim_20260902T043039Z`, or `opt_20260902T043854Z` as current.

---

## 4. Reproduction that works today

```
cd ~/telo/feasibility
uv sync --all-extras
uv run python -m telo_feasibility.cli status           # which definition-of-finished gates remain open
uv run python -m telo_feasibility.cli protocol verify   # source-document hashes
make check                                              # ruff, mypy --strict, full test suite
```

The last recorded gate run is `results/manifests/test_report.json`: 243 passed, 0 failed, 0 skipped,
2026-09-06T02:59:55Z. Re-read that file at send time and quote whatever it then holds. If `make check`
fails, the tree is mid-change.

Seconds:

```
uv run python scripts/run_deterministic.py --reconcile
uv run python scripts/run_simulation.py --runs 20 --strategies S0,S5,S11,S16 --run-id review_check
```

The release question directly, as an ablation. `loo:` removes a mechanism, `addin:` adds only that mechanism to
an otherwise quiet world, and the two bracket its contribution:

```
uv run python scripts/run_ablation.py --runs 60 --opt-run opt_20260903T220534Z \
  --only base,loo:sterility_delay,loo:release_queue,addin:sterility_delay,addin:release_queue \
  --run-id review_release
```

The test that states the release claim as an executable assertion:

```
uv run pytest tests/integration/test_extremes.py::test_full_release_assurance_saves_no_days_when_sterility_binds -q
```

Long runs, with wall times from the recorded runs on the author's machine: optimization 4113 s, ablation over
all 42 configs 10014 s, design-space 6574 s, matched-space check 3706 s. The `--opt-run` default on
`run_ablation.py` and `run_design_space_analysis.py` is superseded; always pass
`--opt-run opt_20260903T220534Z` or the id of the post-fix run.

---

## 5. Known model defects. Skip these

These are already recorded. Finding them again costs you time and tells us nothing. Full register with measured
effects: `docs/design_space/bottleneck_decomposition.md` section 7, including the appended "Status after
revisions R009 to R011" table. Defects fixed under R004 to R008 carry a test named for the id in
`tests/integration/test_model_defect_fixes.py`; those fixed under R009 to R011 carry theirs in
`tests/integration/test_ranking_defect_fixes.py`. The ones that touch process, cost and capacity:

| id | defect | status |
|---|---|---|
| MD-6 | capital, fixed operations and validation accrued for sites that did not exist yet | fixed, R004 |
| MD-7 | `capacity_factor` rescaled an existing plant instantly while identical new-site capacity waited 730 days | fixed, R004 |
| MD-14 | a reserved line was charged full capital and then a reservation fee on top | fixed, R004 |
| MD-9 | the utilization denominator excluded reserved and 503B sites while their output stayed in the numerator | fixed, R005 |
| MD-13 | the node count was capped at the region count, so node redundancy could not be tested | fixed, R005 |
| MD-19 | a common-cause group declared on a supplier was structurally inert at every parameter value | fixed, R007 |
| MD-20 | the deterministic screen dropped reserved sites from capacity and charged no reservation fee | fixed, R007 |
| MD-21 | the reservation fee and take-or-pay accrued before the reserved line existed | fixed, R007 |
| MD-8 | node capacity is quadratic in `capacity_factor`, since batch size and batches per year both scale | open, latent while `capacity_factor` is out of the node design space |
| MD-17 | three commissioning parameters take the value 365, which is also `warm_up_days`, so a lead at or below a year costs nothing inside the measured window | open |
| MD-18 | `release_time_factor` is a frozen design variable the stochastic engine never reads | open |
| MD-22 | `common_impact_factor` is derived from topology for the new strategies and hand-set for the frozen ones, so the two arms of the deterministic screen are not comparable | open |
| MD-23 | a campaign batch substituted for an exercise batch one for one, so an exercise cadence was nearly unmeasurable on a frequently activated line | fixed, R011 |
| MD-25 | the shared-operating-layer cost is charged only outside the base release scenario, so a declared shared-OS common-cause group carries hazard with no cost line | open |
| NEW-1 | opening inventory was seeded with no ledger charge | fixed, R009 |
| NEW-3 | no readiness-decay hazard, so exercising a line buys production volume and not reliability | open |

Two more things are recorded choices rather than defects, and are stated here so you do not report them as
bugs. First, the deterministic replica keeps the workbook's serial sum of lead, changeover, cycle, release and
delivery, while the stochastic engine takes the maximum of concurrent release components plus serial QA; that
split is recorded in `docs/audits/04_requirements_matrix_notes.md`, "Eq. 5 overlap". Second, the engine models
one product per network with equal regional shares (MD-15), so every multi-product and changeover-sharing
argument in the package is an accounting proxy.

---

## 6. The three things the author most suspects are wrong here

**6.1 The release-time structure, not the release-time numbers.** The four component values carry the only
non-illustrative evidence in the model: sterility is tier 1 from USP `<71>`, and environmental monitoring,
assay and endotoxin are tier 4 from an internal memo. That memo is `~/telo/regulatory/release-constraints.md`, one level above this package. One of
its citations is recorded in `CLAIMS_REGISTER.csv` as C025, contradicted by the frozen primary source, so treat
its tier-4 values as unverified and tell us if any of the three is wrong. The structure around them is not evidenced at all. The
engine assumes all four start together at fill, run concurrently, and are followed by a fixed 2-day serial QA
review. If EM sampling is read on a different clock, if assay cannot start until incubation reads out, if QA
review is a queue rather than a constant, or if the components are not simultaneous at a real site, then the
16-day figure and the 2-day chemical saving are both wrong, and the whole argument that sterility is the pole
has to be re-derived. The claim register records the public wording of the release-time claim as contradicted
by the company's own analysis, and that wording is not repeated here.

**6.2 The node cost ledger, and specifically the scaling exponents.** A regional node is built by scaling the
incumbent line: `node_scale_fraction` 0.35 (0.15 to 0.6), capital 40,000,000 USD per site (15M to 100M) scaled
by exponent 0.6 (0.5 to 0.8), fixed QA labour 3,000,000 USD per site-year (1.5M to 6.0M) scaled by exponent 0.8
(0.6 to 1.0), validation 4,000,000 USD one-time (1M to 12M). The exponents are the load-bearing part and their
source locator reads "study placeholder (engineering rule of thumb; needs vendor estimates HA-13)". Fixed plus
resilience cost is 81.0% to 93.7% of annual cost for all eight comparators, so almost every absolute cost in
this package is a statement about those placeholders. The specific question: does a regional node's fixed
quality cost scale with capacity at all, or is a quality unit, a microbiology lab and an environmental
monitoring programme close to a fixed cost regardless of how small the line is? If the exponent is 1.0, or if
it is effectively 0, the node case changes direction.

**6.3 Commissioning, campaign cadence and changeover.** `node_commissioning_days` is 365 low, 730 base, 1095
high, from trade-press cleanroom build times with no regulatory tail. `second_source_qualification_days` is
180 / 365 / 730. `reserved_capacity_activation_days` is 7 / 21 / 60. `changeover_days` is 1 / 3 / 10 and
`batches_per_site_year_nominal` is 30 / 45 / 70, at uptime 0.85 and yield 0.96. Two consequences the author
distrusts. The five architectures that meet the target on both products need batches at or above 35.6 to
44.4 per site-year (`results/design_space/ds_post_R008/thresholds.csv`, `batches_per_site_year` rows: S9 35.6
and 40.6, S11 36.9 and 44.4, S12 44.4 and 44.4, S13 38.1 and 43.1, S16 43.1 and 43.1), against a base of 45 and
a low of 30, so their feasibility sits near the bottom of an illustrative range. And the surviving designs require any site supplying the
presentation, contracted lines included, to hold at or above 43.1 batches per site-year
(`results/design_space/ds_post_R008/thresholds.csv`, `batches_per_site_year` rows for S16), which is a
scheduling claim about somebody else's plant that nobody has checked. It is a site rate, not a campaign count
on a contracted line: `campaign_batches` sits at its lower bound in all four S16 cells
(`docs/design_space/inventory_capacity_hybrids.md` section 3). MD-17 sits on top of this: the low end of the
commissioning range coincides with the warm-up boundary, so part of the measured commissioning effect is an
artifact of where the measurement window starts.

---

## 7. The numbers we are actually buying

Answer what you can. A range with a basis beats a point estimate. Say "I do not know" where you do not, and
name the role that would. Every row says where the answer enters the model.

| Queue id | What is needed | Enters at |
|---|---|---|
| HA-13 | For a small aseptic fill-finish node: installed capital, footprint, utility load, qualification timeline, annual fixed operating cost. At a named US line: what a reserved-capacity agreement costs, what the fee covers, and the minimum campaign size | `capital_usd_per_site`, `fixed_qa_labor_usd_per_site_year`, `validation_usd_one_time`, `reserved_capacity_fee_fraction`, the two scaling exponents |
| HA-21 | Batch size, campaign length, OEE, changeover days, restart time after a deviation, and the elapsed time from decision to first released batch at a small aseptic line | `units_per_batch`, `batches_per_site_year_nominal`, `uptime_fraction`, `changeover_days`, `production_cycle_days`, `investigation_duration_days` |
| HA-22 | True deviation rate per batch and investigation duration at node scale; the release-time decomposition and its concurrency; validation replication cost across sites; a sourced cost of a wrong release | `deviation_rate_per_batch`, `batch_rejection_rate`, `investigation_duration_days`, the release components, `validation_factor`, `wrong_release_cost_usd` |
| HA-41 | From the decision to build to the first commercially released batch: elapsed days split into construction, qualification, process validation, and the regulatory tail | `node_commissioning_days`, `capacity_expansion_days`, `second_source_qualification_days` |
| HA-39 | The annual rate at which events remove more than one nominally independent site or supplier at once, their duration, and the capacity impact | `common_cause_events_per_year`, `common_cause_duration_days`, `common_cause_capacity_impact` |
| HA-14 | A dated contract-laboratory price list for sterility, endotoxin, assay, particulates and container-closure integrity | `testing_usd_per_batch` |
| HA-34 | For each candidate presentation, is the marketed product terminally sterilized or aseptically processed, and for terminal products what is the cycle | `ProductFeatures.sterilization_route` |

HA-39 and HA-34 are worth flagging. The multi-site disruption rate produces 20 threshold crossings and the
feasible set collapses from 11 strategies to 3 on one product and from 10 to 2 on the other as the rate rises
across its declared range, so it is one of the two inputs a reviewer would reject first. And the sterilization
route is the enabling input for the one intervention found across fourteen prior-art families that acts on the
binding release constraint rather than on components that are not binding
(`docs/design_space/prior_art_review.md` section 6.1); if the answer is "aseptic for everything on the
longlist", that family closes permanently.

---

## 8. Current limitations, stated before you find them

- `docs/audits/05_inconsistencies.md` and `docs/audits/04_requirements_matrix.csv` (status column: 84 exist,
  66 partial, 3 missing, of 153 rows).
- `reports/appendices/limitations.md`.
- `docs/design_space/definition_of_finished_status.md`: nine of twenty-two definition-of-finished tests pass,
  and eleven of the thirteen incomplete ones cannot be closed by any amount of code.
- The two product dossiers are near-clones on several axes (audit item WB-26), and the two presentations differ
  mainly through one derived illustrative number, so most apparent product discrimination in this package is
  not evidence.

---

## 9. The form the review should take

Write it however you like. We convert it into `docs/reviewer_packets/reviews/<review_id>.json` with the schema in
`docs/reviewer_packets/reviews/README.md`, and we send you the converted file to correct before it is counted. Per issue we need:

1. **The issue**, in your words, tied to a file, a parameter or a line of the claim in section 2.
2. **What you would use instead**: a number with a range, a category, a document, or a named role who has it.
3. **What it changes if you are right**: which result you expect to move, and in which direction.
4. **Confidence**, in your own terms, and whether you are speaking from direct operating experience or from
   general knowledge of the industry.

We then record our decision against each issue, accepted, partially accepted, or rejected, with the rationale
and the exact model change, and append a row to `docs/reviewer_packets/reviews/revision_log.csv`. Rejections get the same written
rationale as acceptances. The record is public with the package.

Please also say plainly: **what in this package you would refuse to sign your name to.** That answer is worth
more than agreement, and a review that destroys the section 2 claim and attaches three numbers is a complete
and successful review.

Attribution is by role and organisation type only unless you authorise more in writing. Nothing you say will be
described as a partnership, an endorsement, a customer relationship, a pilot, or a regulatory opinion.
