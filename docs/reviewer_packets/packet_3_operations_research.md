# Review packet 3: Operations research and simulation

Reviewer id `reviewer_3` (`protocol/protocol.yaml` `independent_review`); queue id HA-32. You can reject the
model structure, the optimization and the uncertainty methods, and rejecting them is the point.

**Status: not sent. No review has been completed.**

**How long this takes.** Full review: about eight hours, most of it in the code and the run artifacts. **If you
have one hour: read section 2 and section 6, and tell us which of the three doubts is the real one.** This is
the one packet where reading code is not optional, because the machinery is the object under review. No
compensation is offered, and we say so before you spend the time.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input is evidence tier 5
(illustrative) except four release components: 87 of 91 parameters. Nothing here is a statement about
sterile-injectable manufacturing in the world, and nothing here is legal or regulatory advice. All sixteen
regulatory gates are UNCERTAIN, so no strategy carries a favourable decision class. No interview, partner,
customer, pilot or regulatory opinion is asserted, because none has occurred. Reviewing this is not advising,
endorsing, or partnering, and it will never be described as any of those.

This is the packet where the model's own machinery is on trial, so it carries the complete defect register
rather than a filtered one.

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

**(b) The battery is re-run on the fixed engine and every ranking number below is replaced.** Optimize,
simulate, ablate, design-space, matched-space, figures. This condition is not met.

This matters more for this packet than for any other, because the machinery under review is the machinery that
was changed. Only condition (b) is outstanding. A post-fix paired simulation exists
(`results/simulation/sim_post_R009/`, manifest 2026-09-06T03:02:03Z, 20 strategies, both products,
n = 100, at the illustrative baseline designs), but the optimization, ablation, design-space, matched-space,
figures and contract table have not been re-run on the fixed engine: `results/optimization/opt_20260906T032432Z/`
is an empty directory with that run still in flight. Every number below is therefore still a pre-R009 number.
Check `results/manifests/` for a completed post-R011 battery and confirm `make check` is green before sending. Do not send a packet whose ranking is about to
change.

---

## 1. What changed, and what this packet now asks for

The study was designed around one question: under what conditions does distributed regional capacity beat
safety stock, dual sourcing, reserved contract capacity, or added central capacity. Under the model's inputs
that question is answered. That is not the interesting part for you. The interesting part is that the answer
was already corrected once by a methods fix, and might be corrected again.

The package originally reported that no frozen comparator met the frozen service target. That statement was
wrong, and it was wrong for a methods reason: the comparators searched safety stock to 90 or 120 days with no
daily base-stock review, while the newer strategies searched to 365 days with the review as a binary variable.
Re-optimizing four strategies over one common inventory space made added central capacity feasible on both
products, at roughly 60 percent of its declared-space cost, and narrowed the cost gap from an order of
magnitude to about a third (`docs/design_space/feasibility_regions.md` section 8, run `matched_20260905`).

That is one methods defect found by the author. This packet exists because there are probably more.

---

## 2. The claim you are asked to attack

> Five of twenty strategies meet the frozen service target on both products, two of them sit on both
> cost-service frontiers, and that ordering is a property of the architectures rather than of the search space,
> the free opening inventory, the tie-break rule, or the run counts.

The frozen target is mean fill rate at or above tau = 0.99 with tail probability
`p_meet = P(fill >= tau)` at or above q = 0.90. Cost enters the feasibility predicate nowhere. The frontiers,
cheapest first, at 40 paired runs on each strategy's optimized design from `opt_20260903T220534Z`:

- Norepinephrine: S15 12.58M / 0.9925 / 0.825 / no; S11 14.86M / 0.9950 / 0.95 / yes; S16 15.89M / 0.9967 /
  0.90 / yes; S17 18.20M / 0.9972 / 1.00 / yes; S9 23.23M / 1.0000 / 1.00 / yes.
- Sodium bicarbonate: S1 12.67M / 0.7591 / 0.00 / no; S15 13.16M / 0.9412 / 0.125 / no; S11 15.71M / 0.9970 /
  0.925 / yes; S16 16.48M / 0.9972 / 0.925 / yes; S12 22.40M / 0.9976 / 0.95 / yes; S9 24.40M / 0.9997 / 1.00 /
  yes.

Ways to kill it that would count: the ordering is an artifact of the free opening inventory; the ordering is an
artifact of unmatched search spaces and survives only because the symmetric test was never run; the run counts
cannot resolve differences of this size; the optimizer is not finding the designs it claims to find; the
bisection is invalid because the response is not monotone; the common-random-number pairing does not actually
pair across architectures with different site counts; or the feasibility predicate itself is the wrong
decision rule.

---

## 3. Read in this order

1. `docs/architecture/design.md`. The nine-step daily order, the mass-balance identity, the entity roster, and
   the common-random-number scheme. Section 4 is the roster that is supposed to keep pairing valid across
   strategies with different site counts.
2. `docs/methods/simulation.md`, `optimization.md`, `ablation.md`, `design_space_analysis.md`,
   `sensitivity.md`. Short, one per mechanism.
3. `docs/design_space/feasibility_regions.md` section 1 (method, run counts, what monotonicity is assumed, and
   the statement that 111 of 150 design variables sit exactly on a search bound) and section 8 (the correction).
   Section 1 is the most self-critical page in the package and the fastest way to find where to push.
4. Code, in dependency order: `src/telo_feasibility/rng.py` (`RunStreams`), `simulation.py` (the daily loop and
   the cost step), `inventory.py`, `suppliers.py`, `production.py`, `allocation.py`, `disruptions.py`,
   `economics.py`, then `optimization.py`, `design_space_analysis.py`, `ablation.py`, `sensitivity.py`.
5. `docs/design_space/bottleneck_decomposition.md` sections 2.2 (why leave-one-out and add-one-in bracket a
   contribution), 2.3 (common random numbers, N and Monte Carlo standard error) and 7 (the register).
6. `protocol/protocol.yaml`. The thresholds, the horizon, the warm-up, the welfare boundary and the comparator
   freeze are decision rules, not estimates, and changing one needs a `protocol/revisions.csv` row.

Result artifacts, in order:

| Artifact | What it is |
|---|---|
| `results/simulation/sim_post_R008/summary.json` | paired baseline, 20 strategies, 2 products, n = 100, master seed 20260901 |
| `results/optimization/opt_20260903T220534Z/` | the optimized designs everything downstream evaluates at; 20 search runs, 100 final runs |
| `results/design_space/ds_post_R008/thresholds.csv` | 480 rows: 20 strategies x 2 products x 12 inputs, with both bracketing evaluations kept in the `evaluations` column |
| `results/design_space/ds_post_R008/dominance.csv` | cost against service at 40 paired runs |
| `results/design_space/ds_post_R008/reversal.json` | 27 cells per product at 10 paired runs, 20 strategies per cell |
| `results/design_space/matched_20260905.json` | the fair-comparison correction, 4 strategies, 12 search runs, 40 final runs |
| `results/ablation/abl_post_R008/summary.json` | 42 configs at n = 60; keys `<config>|<product>|<strategy>`; config ids listed in section 4 |
| `results/sensitivity/` | one-way, global (Sobol and PRCC), structural, decision-reversal, value of information |
| `results/manifests/*.json` | protocol version and hash, config hashes, git commit and dirty flag, seed, n_runs per run |

Every run made before 2026-09-03 is superseded for quantitative use. `results/sensitivity/voi.json` is
superseded and its numbers must not be quoted as current: it covers one product and strategies S0 to S7 only,
at 6 runs per scenario, on designs from a superseded optimization run.

---

## 4. Reproduction that works today

```
cd ~/telo/feasibility
uv sync --all-extras
uv run python -m telo_feasibility.cli status
uv run python -m telo_feasibility.cli protocol verify
make check                                              # ruff, mypy --strict, full test suite
```

The last recorded gate run is `results/manifests/test_report.json`: 243 passed, 0 failed, 0 skipped,
2026-09-06T02:59:55Z. Re-read that file at send time and quote whatever it then holds. The suite
includes the properties you would want to check first:

```
uv run pytest tests/integration/test_reproducibility.py -q        # common random numbers, run-to-run identity
uv run pytest tests/integration/test_extremes.py -q               # the Appendix C extreme cases
uv run pytest tests/integration/test_model_defect_fixes.py -q     # one test per fixed defect, named by id
uv run pytest tests/unit/test_sensitivity_methods.py -q
```

Seconds:

```
uv run python scripts/run_deterministic.py --reconcile
uv run python scripts/run_simulation.py --runs 20 --strategies S0,S5,S11,S16 --run-id review_check
```

Long runs, with wall times from the recorded runs on the author's machine:

```
uv run python scripts/optimize_strategies.py --search-runs 20 --final-runs 100          # 4113 s
uv run python scripts/run_simulation.py --runs 100                                       # 20 strategies, 2 products
uv run python scripts/run_ablation.py --runs 60 --opt-run opt_20260903T220534Z           # 10014 s, 42 configs
uv run python scripts/run_design_space_analysis.py --opt-run opt_20260903T220534Z        # 6574 s
uv run python scripts/run_matched_space_check.py --strategies S1,S4,S5,S6                # 3706 s
uv run python scripts/run_sensitivity.py                                                 # Sobol, PRCC, structural, reversal, VOI
make figures
```

The `--opt-run` default on `run_ablation.py` and `run_design_space_analysis.py` is `opt_20260902T043854Z`,
which is superseded. Always pass `--opt-run` explicitly.

Targeted ablation. The 42 config ids are `base`, `quiet_all`, `bounds:ss365`, `bounds:ss365+base_stock`, and
`loo:` and `addin:` for each of `api_lead_time`, `capacity_shortfall`, `commissioning_delay`, `common_cause`,
`component_lead_time`, `contract_insufficiency`, `demand_covariance`, `demand_variance`,
`deviation_rejection`, `inventory_timing`, `regulatory_unavailability`, `release_queue`, `site_failures`,
`sterility_delay`, `supplier_concentration`, `surge_headroom`, plus six cost factors that have a `loo:` arm
only (`capital_cost`, `fixed_quality_cost`, `horizon_10y`, `lost_sales_window`, `material_buffer`,
`replicated_validation_cost`):

```
uv run python scripts/run_ablation.py --runs 60 --opt-run opt_20260903T220534Z \
  --only base,quiet_all,loo:capacity_shortfall,addin:capacity_shortfall --run-id review_ablation
```

`--designs baseline` runs the same configs at the illustrative baseline designs instead of the optimized ones,
which is the cleanest way to separate an architecture effect from a search effect.

---

## 5. The complete defect register. Skip all of it

Every row below is already recorded, with a measured effect, in
`docs/design_space/bottleneck_decomposition.md` section 7 (MD-1 to MD-25, including the appended "Status after
revisions R009 to R011" table) and `docs/design_space/novel_architectures.md` section 5 (NEW-1 to NEW-3).
Defects fixed under R004 to R008 carry a test named for the id in
`tests/integration/test_model_defect_fixes.py`; the eight fixed under R009 to R011 carry theirs in
`tests/integration/test_ranking_defect_fixes.py`. Finding any of these again costs you time and tells us
nothing. The status column below is current as of 2026-09-06; the numbers elsewhere in this packet are not,
because the battery has not been re-run.

| id | defect | status |
|---|---|---|
| MD-1 | material order-up-to and reorder point were `(target_days + lead) x daily demand`, so cutting a lead cut the buffer; the API lead factor had no guaranteed sign | fixed, R011, with a stated residual: under a forced outage a shorter lead can still show marginally more stockouts, which is a property of the disruption model |
| MD-2 | the reorder point was never lot-sized against a whole-batch draw, so the store could stall below one batch | fixed, R005 |
| MD-3 | the regional review rule was hard-coded as `reorder_days = lane_days + 1.0`; the alternative shipped unused. Decisive in 8 of 16 Phase A cells | fixed, R010: every frozen comparator now searches the same inventory space, `region_base_stock` included, as a binary |
| MD-4 | opening lots were stamped at half shelf life, which at 24 months is day 365, the first measured day, so more safety stock read as harmful | fixed, R004; invalidated every pre-R004 safety-stock conclusion |
| MD-5 | `fill_rate` forgives anything delivered inside a 7-day backorder window and charges the rest to its origin day; the sign is not monotone in the window | deferred; a metric-definition question for the protocol |
| MD-6 | capital, fixed operations and validation accrued for sites that did not exist yet | fixed, R004 |
| MD-7 | `capacity_factor` rescaled an existing plant instantly while identical capacity added as a new site waited 730 days | fixed, R004 |
| MD-8 | node capacity is quadratic in `capacity_factor`, because batch size and batches per year both scale | open, latent while `capacity_factor` is out of the node design space |
| MD-9 | the utilization denominator excluded reserved and 503B sites while their output stayed in the numerator | fixed, R005 |
| MD-10 | a Shapley bracket printed 0.0 where a factor had no add-one-in arm and nothing had been measured | fixed, R005 |
| MD-11 | the infeasible tie-break was `min(-mean_fill, mean_cost)` with no Monte Carlo standard error tolerance, on a 20-run screen whose binomial standard error at q = 0.90 is 0.067; one strategy paid +9.26M USD/yr for +0.00004 fill | fixed, R010: the tie-break ranks on fill only where the difference exceeds a noise band derived from the screen size, then on cost, and the band is recorded on the optimization record |
| MD-12 | omitted search dimensions, and search spaces not matched across architectures | fixed, R010, for the inventory space; `LEGACY_DESIGN_SPACES` keeps the old boxes so earlier runs stay reproducible. Stage-1 grid counts are endpoints only |
| MD-13 | the node count was capped at the region count, so redundancy could not be tested | fixed, R005 |
| MD-14 | a reserved line was charged full capital and then a reservation fee on top | fixed, R004 |
| MD-15 | one product per network, equal regional shares; two strategies numerically identical | open, recorded as scope; the largest unquantified distortion in the cost comparison |
| MD-16 | `p_meet` carried no reported uncertainty while feasibility was decided on it | fixed, R005; it now carries its binomial standard error |
| MD-17 | three commissioning parameters take the value 365, which is also `warm_up_days`, so a lead at or below a year costs nothing inside the measured window | open |
| MD-18 | `release_time_factor` is a frozen design variable the stochastic engine never reads | open |
| MD-19 | a common-cause group declared on a supplier was structurally inert at every parameter value | fixed, R007 |
| MD-20 | the deterministic screen dropped reserved sites from capacity and charged no reservation fee | fixed, R007 |
| MD-21 | the reservation fee and take-or-pay accrued before the reserved line existed | fixed, R007 |
| MD-22 | the deterministic screen's common-impact input is topology-derived for some strategies and hand-set for others | open |
| MD-23 | a campaign batch substituted for an exercise batch one for one, so an exercise cadence was nearly unmeasurable on a frequently activated line | fixed, R011: readiness is time since the last qualified batch, so any batch restarts the clock |
| MD-24 | take-or-pay entered cost only and changed no service quantity, so an optimizer drove it to its lower bound | fixed, R011: a take-or-pay commitment orders committed lines ahead of uncommitted ones in a region's sourcing list |
| MD-25 | the shared-operating-layer cost is charged only outside the base release scenario, so a declared shared-OS group carries hazard with no cost line | open |
| NEW-1 | opening inventory was seeded with no ledger charge and scaled with the design's own stock policy | fixed, R009: the units seeded on day zero are charged once at the production unit value into an `opening_inventory` ledger field |
| NEW-2 | allocation rights were inert; all four `allocation_policy` values collapsed to proportional | fixed, R011, with the honest finding stated: regions may now carry differing criticality weights and a minimum guarantee, and the guarantee reaches the allocator, but with identical regions three of the four policies return the same fill to nine decimals, which is arithmetic and not a defect. The default keeps regions identical |
| NEW-3 | no readiness-decay hazard, so exercising a line buys production volume and not reliability | open |

---

## 6. The three things the author most suspects are wrong here

**6.1 The ranking is bought rather than earned.** Three mechanisms pointed the same way and all three favoured the
inventory-led designs that win in the numbers below. NEW-1 seeded opening inventory with no ledger charge and
sized it from the design's own stock policy, so a design that chose deep stock was handed that stock for free;
on one product that is 1,200,000 units covering 5.08 years of a 236,100 units per year structural gap over a
five-year window, and one strategy delivered 121.8% of its own annual saleable capacity. MD-12 gave the newer
strategies a wider inventory search space than the frozen comparators, and correcting that on four strategies
already flipped one verdict. MD-11 let the tie-break buy a fill gain far inside the noise with a large cost
increase. All three are fixed in code under R009 and R010, and **none of the numbers in this packet has been
re-run on the fixed engine**, so the ranking you are reading is the one those three mechanisms produced.
The specific question for you: is there any way to separate architecture from search freedom and from seeding
in a design of this kind, other than running every architecture over one common space with a charged opening
position, and is the symmetric test (narrowing the newer strategies to the comparators' space) the right
completion or is there a better one?

**6.2 The evidence is thinner than the digits suggest.** The reversal map runs at 10 paired runs per cell, and
every `p_meet` in all 1,080 strategy-cell values is a multiple of 0.1, which is exactly that granularity; the
binomial standard error of `p_meet` at q = 0.90 is 0.095 at 10 runs, 0.067 at 20 and 0.047 at 40. Several
reported verdicts sit exactly on the requirement: one strategy meets the tail at `p_meet` exactly 0.90 on 40
paired runs, one standard error from failing, and the matched-space correction produced two results at exactly
0.90. Eleven cells have a threshold-grid verdict that disagrees with their 40-run base verdict. And 111 of the
150 design variables across the 40 optimizer cells sit exactly on a search bound, which means a threshold, a
dominance row and a reversal cell all report where the box ends as much as where the architecture sits. The
question: what run counts, what variance-reduction beyond common random numbers, and what sequential rule would
make a feasibility verdict at a 0.90 tail requirement actually decidable at this cost per run?

**6.3 The uncertainty machinery may not transfer to this response.** Four specific doubts. Bisection assumes
the feasibility indicator is monotone in the swept input, and it demonstrably is not: `raw_material_lead_time`
returns `feasible_above` in 5 of its 7 crossings, meaning the strategy meets the target at a longer API lead
time and fails at a shorter one, which is MD-1 showing through, and no maximum API lead time is claimed for
that reason. Sobol indices are computed on a paired response under common random numbers, and it is not obvious
that the variance decomposition means what it usually means once the noise is shared across designs. The
value-of-information layer uses regression-based expected value of partial perfect information, and its stored
run is superseded; worse, its top-ranked channel is the same MD-1 artifact, so the ordering should be read as
"fix MD-1", not as "measure supplier lead times first". And the common-random-number scheme has to pair
strategies with different site counts through a universal entity roster; if that roster is not actually
achieving pairing across architectures, every paired contrast in the package is weaker than reported.

---

## 7. What we are actually buying

This is the one packet where the deliverable is a judgement rather than a number, because the objects under
review are methods. Even so, two categories of number would change what we do:

| Queue id | What is needed | Enters at |
|---|---|---|
| HA-25 | Comparator optimization design, dependence structure, calibration, and the welfare boundary of the study | `optimization.py`, `disruptions.py`, the protocol's welfare boundary |
| HA-39 | The annual rate at which events remove more than one nominally independent site or supplier at once, their duration and capacity impact | `common_cause_events_per_year`, `common_cause_duration_days`, `common_cause_capacity_impact` |

HA-39 is here as well as in packet 1 because the dependence structure is a modelling choice before it is a
measurement, and because the axis is decisive: it produces 20 crossings and the feasible set collapses from 11
strategies to 3 on one product and from 10 to 2 on the other across its declared range. If you think the
Beta-distributed capacity-impact model with Poisson group events is the wrong structure, say so, and say what
you would use.

Ranges are acceptable and preferred throughout.

---

## 8. Current limitations, stated before you find them

- Every input is illustrative, so no absolute cost, break-even price or capital requirement in the package is
  a statement about the world.
- The engine models one product per network with equal regional shares (MD-15).
- The two product dossiers are near-clones on several axes and differ mainly through one derived illustrative
  number, so most apparent product discrimination is not evidence.
- The backcasts are weak: three ongoing shortages of one class against a requirement of four episode classes.
- `docs/audits/05_inconsistencies.md`; `docs/audits/04_requirements_matrix.csv` status column;
  `reports/appendices/limitations.md`; `reports/appendices/reproducibility.md`.
- Nine of twenty-two definition-of-finished tests pass, and eleven of the thirteen incomplete ones cannot be
  closed by any amount of code. The modelling has run ahead of the evidence.

---

## 9. The form the review should take

Write it however you like. We convert it into `docs/reviewer_packets/reviews/<review_id>.json` with the schema in
`docs/reviewer_packets/reviews/README.md`, and we send you the converted file to correct before it is counted. Per issue we need:

1. **The issue**, tied to a file, a function, a run artifact, or a line of the claim in section 2.
2. **What you would do instead**: the method, the run count, the estimator, or the design change, with a
   citation if there is one.
3. **What it changes if you are right**: which result you expect to move, and whether you expect the sign or
   only the magnitude to change.
4. **Cost**: roughly what the fix costs in compute or in redesign, so we can order the work.
5. **Confidence**, in your own terms.

We record our decision against each issue, accepted, partially accepted, or rejected, with the rationale and
the exact model change, and append a row to `docs/reviewer_packets/reviews/revision_log.csv`. Rejections get the same written
rationale as acceptances. Where an issue changes a decision rule rather than a number, the fix also needs a
`protocol/revisions.csv` row and a version bump, and we will say so in the decision.

Please also say plainly: **what in this package you would refuse to sign your name to.** A review that
establishes that the ranking cannot be decided at these run counts, or that the search invalidates the
comparison, is a complete and successful review, and is the most useful outcome available here.

Attribution is by role and organisation type only unless you authorise more in writing. Nothing you say will be
described as a partnership, an endorsement, a customer relationship, a pilot, or a regulatory opinion.
