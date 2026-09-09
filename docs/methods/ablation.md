# Failure decomposition by ablation: methods

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Code: `src/telo_feasibility/ablation.py`; script `scripts/run_ablation.py`; figures
`scripts/build_ablation_figures.py`; tables `scripts/build_bottleneck_tables.py`. Results
under `results/ablation/<run_id>/`. Findings from the first run are in
`docs/design_space/bottleneck_decomposition.md`; this file describes the method only.

## What a factor is

A `Factor` is one named failure mechanism plus the overrides that switch it off. Overrides
are applied through the same provenance-carrying parameter records the rest of the study
uses (`sensitivity.set_base`), never as ad hoc numbers, so a switched-off mechanism is
always a stated parameter value and shows up in the run manifest.

Three kinds:

| kind | meaning | enters the quiet set |
|---|---|---|
| `mechanism` | a real process that can degrade service (capacity, demand, supply, quality, dependence, contract, regulatory, time) | yes |
| `cost` | changes cost only and by construction cannot change service | no |
| `structure` | a modelling choice rather than a mechanism (measurement window, evaluation horizon, review rule) | no |

A factor may also be `loo_only`, which excludes it from the quiet set because switching it
on in a world where nothing else fails would have nothing to act on. `material_buffer` is
the only one: raw-material stockouts cannot occur when no supplier is ever disrupted.

`capacity_shortfall` is the one factor with a computed override. It raises nominal batches
per site-year until the status-quo plant runs at 75% utilization, because the illustrative
inputs put sodium bicarbonate's plant above 100% and a plant that cannot meet mean demand
makes every other mechanism unobservable.

## The two experiments

For each product and strategy the harness runs, on one common-random-number batch:

* **base**: every mechanism on, the world the study normally simulates.
* **leave-one-out** (`loo:<factor>`): base with one mechanism switched off. The improvement
  is that mechanism's marginal contribution *given every other mechanism*.
* **quiet_all**: every mechanism factor switched off at once.
* **add-one-in** (`addin:<factor>`): quiet with one mechanism switched back on. The damage
  is that mechanism's contribution *in isolation*.

Leave-one-out and add-one-in are the two ends of the Shapley averaging order, so for a
monotone response their absolute deltas bracket the Shapley attribution. The harness
reports both and their bracket rather than a single attributed share, because with
interacting mechanisms a single share would hide the disagreement. Where the two deltas
differ materially the mechanisms interact, and the factorial configurations
(`--pairs f1,f2,...`) measure the interaction directly.

Two bound-extension configurations sit outside the factor scheme: `bounds:ss365` raises
safety stock to a year, and `bounds:ss365+base_stock` adds the base-stock review rule.
They exist to separate a genuine infeasibility from an optimizer search-bound artifact.

## Pairing and precision

Every configuration draws its exogenous world from the same master seed and run indices, so
a configuration difference is a mechanism difference and not a sampling difference. Entity
draws are keyed by entity id and batch ordinal, so switching a mechanism off does not
perturb the draws of entities it does not touch. The summary reports the Monte Carlo
standard error of every mean; a delta smaller than the standard errors it is built from is
not evidence of anything, and the decomposition document is required to say so where it
matters.

Tail probability `P(fill >= tau)` is a proportion over runs, so its resolution is 1/N. With
the standard 100 runs a change of 0.01 is one run.

## Outputs

| file | content |
|---|---|
| `results.csv` | one row per configuration, product, strategy, and run: every metric, the cost ledger, network capacity, and utilization (not tracked in git; regenerated from the manifest) |
| `summary.json` | `meta` (factors, configurations, designs, thresholds, status-quo utilization, eligibility) and `by_key` for `<config>|<product>|<strategy>`: means with MCSE, tail probabilities at the frozen and the 0.98 target, fill percentiles, and feasibility |
| `attribution.csv` | one row per product, strategy, and factor: base value, leave-one-out and add-one-in deltas and shares for fill, tail probability, shortage days, unmet units, and cost, plus the Shapley bracket on fill |
| run manifest | protocol version and hash, config hashes, seeds, N, gate outcomes, git state |

## What the method cannot do

It measures mechanisms that exist in the model. A mechanism the engine does not represent
(campaign scheduling across products, relocation of a mobile unit, a second inventory stage
for postponement) cannot appear as a factor, and its absence is not evidence that it does
not matter. It also inherits every input: with tier-5 values the ranking of mechanisms is a
property of those values, which is why the decomposition document reports what would change
the ranking rather than presenting the ranking as a finding.
