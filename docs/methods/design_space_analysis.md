# Feasibility conditions, dominance, and reversal maps: methods

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Code: `src/telo_feasibility/design_space_analysis.py`; driver
`scripts/run_design_space_analysis.py`; figures `scripts/build_design_space_figures.py`.
Results under `results/design_space/<run_id>/`. Contract arithmetic that turns these
results into commercial conditions is in `src/telo_feasibility/contracting.py`.

## Feasibility as a condition, not a score

A strategy is feasible when mean fill reaches the protocol's target and the share of runs
meeting it reaches the tail confidence. Both come from `protocol.yaml`; neither is set here.
`threshold()` sweeps one named input between its recorded low and high values and bisects
for the crossing, reporting:

* the two endpoint evaluations, always, so a response that does not change feasibility
  inside the recorded range is visible as `feasible_everywhere` or `infeasible_everywhere`
  rather than reported as a spurious threshold;
* the crossing and the bracket that contains it, when the endpoints disagree;
* every evaluation performed, so the search can be audited.

Bisection assumes the feasibility indicator is monotone in the input between the endpoints.
That assumption is not verified inside the routine; it is bounded by always reporting both
endpoints and the full evaluation list, and it is why a condition is only ever stated over
the recorded range of a parameter that carries provenance.

The inputs are the protocol's mandatory sensitivity set plus eleven the design-space
questions need (commissioning, activation latency, reservation fee, operating-system cost,
node capital, validation cost, testing cost, batches per site-year, common-cause impact,
supplier and site failure durations). Each maps to one parameter that already carries
provenance, so a condition is always expressed in the units of a real model input.

## Dominance

`dominance()` marks a strategy dominated when another costs no more and serves at least as
well on both mean fill and tail probability, with at least one strict improvement. The
caller supplies an absolute cost tolerance for Monte Carlo noise. The tolerance is a noise
band, not a preference: inside it a rival dominates only by serving better, and a rival that
is merely cheaper by less than the band does not dominate at all. The frontier is the set of
undominated strategies, reported alongside eligibility so that a strategy on the frontier
whose gates are UNCERTAIN is never read as a recommendation.

## Reversal maps

`reversal_map()` evaluates every strategy over a grid of two or three inputs and records the
cheapest feasible strategy per cell, or `None` where no strategy qualifies. A change of the
preferred strategy across the grid is a decision reversal; a region of `None` is where the
whole comparison stops being informative. Grid resolution is three levels per axis by
default, so a reversal between grid points is not located, only bracketed.

## Commercial conditions

`contracting.contract_requirement()` converts a simulated annual cost into the terms a
strategy needs: the resilience premium per delivered unit against a reference strategy, the
break-even price, the committed volume whose contribution margin covers fixed and
resilience cost (protocol Eq. 6), the share of capacity that volume represents (take-or-pay),
and the implied utilization. When no price is supplied the break-even price is used and the
result says so, because at that price the committed volume equals delivered volume by
construction and the number carries no information. Prices, reimbursement, and production
cost stay separate arguments; nothing here infers a price from a cost.

`ContractTerms` holds the nine questions a resilience contract must answer (payer,
purchaser, beneficiary, term, committed volume, activation condition, allocation rights,
default risk, price required) and reports which are unanswered, so a strategy is never
presented as contractable by omission.

## Precision and cost

Threshold bisection costs `2 + steps` evaluations per input and strategy, each of
`threshold_runs` paired runs. The default 20 runs give a tail probability resolution of
0.05, which is coarse against a 0.90 requirement: a threshold located with 20 runs should be
read as a bracket, and the driver records the run count in the run manifest so a reader can
see it. Dominance and reversal use the larger `--runs` batch.

## Reading a condition that runs the wrong way

Some crossings point in the direction a reader does not expect. In the first frozen-strategy
run, sodium bicarbonate S3 is feasible while the raw-material lead time is at or above 151
days, not below it. That is the material policy behaving correctly rather than a defect: the
order-up-to level covers demand over the lead time plus the target days of supply, so a
longer lead time raises the order-up-to level and the site holds more component stock. The
condition is therefore about the size of the buffer, not about the speed of resupply, and it
now carries a cost because raw-material stock accrues the inventory carrying rate (revision
R003). Any condition whose direction surprises should be read the same way, by looking at
which policy the parameter enters, before it is reported as a finding.

## What the method cannot do

It locates conditions in the model's parameter space, not in the world's. Every input swept
here is tier 5 except the four sourced release components, so a condition such as "feasible
while commissioning stays under N days" says what the model does, and becomes a statement
about Telo only when the inputs are replaced with evidence. The maps also hold every other
input at its base value, so a condition is conditional on that base, and interactions
between two swept inputs appear only in the reversal maps.
