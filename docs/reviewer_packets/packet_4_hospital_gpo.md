# Review packet 4: Hospital pharmacy, GPO, wholesaler

Reviewer id `reviewer_4` (`protocol/protocol.yaml` `independent_review`); queue id HA-33. You can reject the
demand, inventory and contract assumptions, and rejecting them is the point.

**Status: not sent. No review has been completed.**

**How long this takes.** Full review: about three hours. **If you have one hour: read section 2, answer
section 7, and stop.** Reading code is optional throughout this packet; section 3 item 4 exists for people who
want it, and the three mechanisms you need are stated in plain English in section 2 and in the box below. No
compensation is offered, and we say so before you spend the time.

**The three mechanisms, in plain English.**

| mechanism | how the model does it |
|---|---|
| The release clock | A batch is held for the longest of four tests that all start at fill (sterility 14 days, environmental monitoring 7, assay 5, endotoxin 2), then a further 2 days of quality review. So the hold is 16 days and sterility decides it. |
| Regional replenishment | Each region reorders when its position falls to lane time plus one day, and orders up to safety-stock days plus lane days. That rule is one we wrote; the daily order-up-to alternative is the thing HA-40 would replace it with. |
| Fill rate | An order counts as filled if it is delivered within 7 days of the day it was placed; anything later is charged as a miss to the day it was placed. So the headline service number is closer to a weekly service level than to an annual fill rate. |

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every demand, inventory, cost and price input in this
model is evidence tier 5 (illustrative): 87 of 91 parameters. Nothing here is a statement about
sterile-injectable supply in the world, a recommendation to a purchaser, or legal or regulatory advice. All
sixteen regulatory gates are UNCERTAIN, so no strategy carries a favourable decision class. No interview,
partner, customer, pilot, purchaser or regulatory opinion is asserted, because none has occurred. Reviewing
this is not advising, endorsing, partnering, or agreeing to buy anything, and it will never be described as any
of those. Nothing in this packet is an offer or a solicitation.

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

Three of those are directly about the things this packet asks you to judge: the replenishment rule, the free
opening inventory, and whether an allocation right does anything at all. The numbers below still predate all
three fixes.

**(b) The battery is re-run on the fixed engine and every service and cost number below is replaced.** This
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
that question is answered, and the answer is that building regional plants does not beat those alternatives
anywhere in any recorded range. The surviving shape is a single approved presentation bought as contracted
campaigns from lines that already exist, with a deep positioned finished-goods tier, sold as ordinary units.

So this packet no longer asks what you think of distributed manufacturing. It asks two things. Attack the claim
in section 2. Then give numbers, with ranges, for section 7. Because every input is illustrative, an opinion
about architecture changes nothing in this model and a measured number changes a great deal. A range beats a
point estimate, and "I do not know, and here is the role that does" is a useful answer.

One thing is worth saying plainly. The package's own reading of the public record is that no US hospital
system, GPO or state has been found paying a standing reservation fee for sterile generic capacity, and the
package treats that as "assume the answer is no until a purchaser says otherwise" rather than as proof. You are
one of the few people who can say whether that reading is right.

---

## 2. The claim you are asked to attack

Two halves, both attackable.

> **On supply.** For a presentation whose demand exceeds the saleable capacity serving it, inventory cannot
> close the gap. A full year of safety stock with daily base-stock review leaves the status quo on sodium
> bicarbonate 8.4% at a fill rate of about 0.87 with tail probability 0.00, and at twice base demand no strategy
> of the twenty meets the service target in any of the 18 reversal cells on either product.
>
> **On price.** At an assumed 18.00 USD per unit, only two of the strategies that meet the service target keep
> their required committed share below 1.0. Five of the thirteen service-feasible strategy-product cells move
> from commercially possible to impossible as the price falls from break-even to 18.00 USD.

These are engine outputs, quoted at two significant figures. The inputs behind them carry no precision at all;
the artifacts print six decimal places only because that is what the engine emits.

The 18.00 USD is an assumption written by the author, not evidence, and no price a purchaser would pay is known
for either presentation. For context only: USP reports that 74% of sterile injectables in shortage price below
15 USD per unit and 44% below 5, n = 61. The service target is mean fill rate at or above 0.99 with tail
probability at or above 0.90, over five measured years after a 365-day warm-up.

Ways to kill it that would count: the demand denominator is wrong, so the capacity deficit is not real; fill
rate against a modelled order stream is not the metric a hospital or a wholesaler experiences; the assumed unit
price is off by enough to change which designs are viable; nobody signs multi-year committed volume for a
generic injectable at any price; or the whole framing of "committed share" is not how these agreements work.

---

## 3. Read in this order

1. `docs/design_space/strategic_synthesis.md`, the answer to the governing objective plus sections 6, 9 and 10.
   Section 6 is the conditions list and section 9 is what the package says not to build.
2. `config/products/sodium_bicarbonate_8_4_50ml.yaml` and `config/products/norepinephrine_1mgml_4ml.yaml`.
   The rows that matter to you: `annual_demand_units` (1,200,000 and 900,000 base; ranges 600,000 to 2,400,000
   and 500,000 to 1,800,000), `target_safety_stock_days` (30 / 60 / 180), `shelf_life_months` (12 / 24 / 36
   sodium bicarbonate; 12 / 24 / 30 norepinephrine), `distribution_usd_per_unit`, `delivery_days`,
   `expiry_scrap_fraction`.
3. `config/global.yaml`: `demand_cv` (0.08 / 0.15 / 0.30), `demand_autocorrelation`,
   `demand_seasonality_amplitude`, `demand_shock_multiplier` and its arrival rate and duration,
   `demand_shock_all_regions_probability`, `backorder_window_days` (3 / 7 / 30), `emergency_transport_days`
   and premium, `inventory_carrying_rate`. Read the `source_locator` lines; most say "study placeholder".
4. **Optional, code.** `src/telo_feasibility/demand.py`, `inventory.py`, `allocation.py`, and the regional
   policy block in `strategies.py`. Then `src/telo_feasibility/contracting.py`, which is where the committed
   share, the break-even price and the contract terms live. The plain-English version of all three mechanisms
   is in the box at the top of this packet.
5. `docs/design_space/feasibility_regions.md` section 3 (the eleven thresholds, including the commercial rows)
   and sections 2.1 and 2.2 (the demand ceilings).
6. `docs/design_space/inventory_capacity_hybrids.md` sections 3.3, 3.5 and 4, which is where the inventory
   arithmetic and the break-even prices sit, and where the free-opening-inventory problem is quantified.

Result artifacts, in order:

| Artifact | What it is |
|---|---|
| `results/simulation/sim_post_R008/summary.json` | paired baseline, 20 strategies, both products, n = 100 |
| `results/design_space/ds_post_R008/dominance.csv` | annual cost against fill rate and tail probability at each strategy's optimized design |
| `results/design_space/ds_post_R008/contract_scenarios.csv` | the contract scenarios, including take-or-pay |
| `results/design_space/contract_conditions_sim_post_R008.csv` | required committed share and break-even price per strategy and product |
| `results/design_space/ds_post_R008/thresholds.csv` | the demand, shelf-life and disruption ceilings each architecture needs |
| `results/ablation/abl_post_R008/summary.json` | includes `bounds:ss365` and `bounds:ss365+base_stock`, the full-year safety-stock bounds behind the supply half of the claim |
| `results/figures/design_space_ds_post_R008_*_dominance.png` | the cost against service plots, each with a `.meta.txt` naming its run |

Every run made before 2026-09-03 is superseded for quantitative use.

---

## 4. Reproduction that works today

You are not expected to run anything. It is here so that nothing in the packet has to be taken on trust.

```
cd ~/telo/feasibility
uv sync --all-extras
uv run python -m telo_feasibility.cli status
make check
```

The last recorded gate run is `results/manifests/test_report.json`: 243 passed, 0 failed, 0 skipped,
2026-09-06T02:59:55Z. Re-read that file at send time and quote whatever it then holds.

Seconds:

```
uv run python scripts/run_deterministic.py --reconcile
uv run python scripts/run_simulation.py --runs 20 --strategies S0,S1,S11,S16 --run-id review_check
```

The safety-stock arms behind the supply half of the claim:

```
uv run python scripts/run_ablation.py --runs 60 --opt-run opt_20260903T220534Z \
  --only base,bounds:ss365,bounds:ss365+base_stock --run-id review_inventory
```

The contract table, which is the fastest way to see how required committed share moves with price:

```
uv run python scripts/build_contract_table.py
```

Longer runs are documented in `README.md` section 5 of this directory, with their wall times. The `--opt-run`
default on `run_ablation.py` and `run_design_space_analysis.py` is superseded; always pass `--opt-run`
explicitly.

---

## 5. Known model defects. Skip these

Already recorded. Full register with measured effects: `docs/design_space/bottleneck_decomposition.md`
section 7, including the appended "Status after revisions R009 to R011" table, and
`docs/design_space/novel_architectures.md` section 5. The status column is current as of 2026-09-06; the
numbers elsewhere in this packet are not, because the battery has not been re-run. The ones that touch demand,
inventory, allocation and contracting:

| id | defect | status |
|---|---|---|
| MD-4 | opening lots were stamped at half shelf life, which at 24 months is day 365, the first measured day, so more safety stock read as harmful | fixed, R004; every pre-R004 safety-stock conclusion was invalidated |
| MD-2 | the material reorder point was never lot-sized against a whole-batch draw, so a store could stall below one batch | fixed, R005 |
| MD-9 | the utilization denominator excluded reserved capacity while its output stayed in the numerator | fixed, R005 |
| MD-16 | the tail probability carried no reported uncertainty while feasibility was decided on it | fixed, R005 |
| MD-3 | the regional review rule was hard-coded as `reorder_days = lane_days + 1.0` against `target_days = safety + lane`; the alternative shipped unused. Decisive in 8 of 16 Phase A cells at +0.82% cost | fixed, R010: every frozen comparator now searches the same inventory space, `region_base_stock` included, as a binary |
| MD-5 | fill rate forgives anything delivered inside a 7-day backorder window and charges the rest to its origin day; the sign is not monotone in the window | open; a metric-definition question |
| MD-1 | the material order-up-to level was `(target days + lead) x daily demand`, so cutting a supplier lead cut the buffer and the lead-time factor had no guaranteed sign | fixed, R011, with a stated residual under a forced outage |
| MD-15 | one product per network, equal regional shares, one labeler, so every portfolio and postponement argument is an accounting proxy | open, recorded as scope |
| MD-24 | take-or-pay entered cost only and bought no service, so an optimizer drove the commitment to its lower bound | fixed, R011: a commitment now orders committed lines ahead of uncommitted ones in a region's sourcing list |
| NEW-1 | opening inventory was seeded with no ledger charge and scaled with the design's own stock policy. On one product that is 1,200,000 units against a structural gap of 236,100 units per year, and one strategy delivered 121.8% of its own annual saleable capacity | fixed, R009: the opening position is charged once at the production unit value |
| NEW-2 | allocation rights were inert; all four allocation policies collapsed to proportional | fixed, R011, with the honest finding that with identical regions three of the four still coincide; the default keeps regions identical |

---

## 6. The three things the author most suspects are wrong here

**6.1 The demand denominator, and the one derived number that carries most of the difference between the two
products.** `annual_demand_units` is illustrative for both presentations, and so is the installed capacity it
is compared against. The two products differ mainly through a single derived number, status-quo utilization at
1.245 against 0.778, and an internal audit records the two dossiers as near-clones on several other axes. This
input accounts for 46 of the 138 threshold crossings in the package, and it is the only axis whose reversal map
has a region where nothing qualifies. It is also uncomfortably tight: one product's demand ceiling sits 3.9%
above its base value, which is well inside the interval a real utilization measurement would carry. The
question we are asking you: what is the true national and regional utilization of a specific presentation in
units per year? The installed capacity that serves it is a separate item, and we do not expect you to hold it;
we chase that through establishment registration, listing and the holder set rather than through this
conversation. CMS Part B is an outpatient proxy that misses inpatient essential injectables, which is why the
package does not use it as a denominator.

**6.2 The replenishment rule, the opening position, and the backorder window.** Three separate things, all
placeholders, all decisive. The regional review rule was hard-coded and the protocol never specifies it, and
switching it changes 8 of 16 cells in the failure decomposition; on the post-R008 bounds ablation it moves the
status quo on norepinephrine from 0.28 to 1.00 on the tail metric, and takes the comparators from 0 of 16
feasible cells to 11 of 16. Opening inventory was seeded free and sized from the design's own policy, which
flattered every inventory-led design in the battery, and is the single largest reason the ranking below is
provisional. Both are fixed in code under R010 and R009, and **the numbers in this packet predate both fixes**.
The backorder window is 7 days, meaning an order filled within 7 days counts as filled, and its effect on the
headline metric is not even monotone, which is still open. The questions: at a
real regional stocking point for a sterile injectable, what review policy runs, at what frequency, to what
order-up-to level, and expressed in what unit? And when a sterile injectable is unavailable, how long does an
order stay a backorder before the demand is lost or substituted, and does that differ by presentation and by
customer?

**6.3 Whether any of the commercial mechanisms exist.** Two strategy ids carry this paragraph and it is
unreadable without them. **S11** is contracted campaigns at registered lines with positioned stock; **S16** is
the same shape with a reserve trigger. They are the two designs that meet the service target on both products
and sit on both cost-service frontiers.

Three doubts stacked. First, the price. 18.00 USD per unit is an assumption. Break-even prices computed at the
optimized designs are about 13 USD per unit on sodium bicarbonate and about 17 on norepinephrine for S16
(`docs/design_space/inventory_capacity_hybrids.md` section 4, computed at the optimized designs from
`opt_20260903T220534Z`); the simulation-side contract table gives about 17 and about 14 for the same strategy
(`results/design_space/contract_conditions_sim_post_R008.csv`), and the two are computed on different inputs,
which is itself worth your attention. The price at which required committed share reaches exactly 1.0 is about
11 USD per unit on sodium bicarbonate and about 15 on norepinephrine for S11, the cheaper of the two
(`docs/design_space/feasibility_regions.md` section 3). If a purchaser would not go above the current contract
price, most of the surviving designs are not businesses.

Second, the commitment. S16 needs about 0.89 of realized demand on sodium bicarbonate and about 0.90 on
norepinephrine committed to break even at its own break-even price, which is a very large share for a generic
injectable, and nothing in the package establishes that anyone signs that.

Third, allocation. Allocation rights were inert in the engine until R011 and the default still keeps every
region identical, so a claim about who gets product first during a shortage is barely modelled, and the package
does not know whether an allocation right is even a purchasable thing.

---

## 7. The numbers we are actually buying

Answer what you can, in ranges, from your own operation. Say "I do not know" where you do not, and name the
role that would. Every row says where the answer enters the model.

| Queue id | What is needed | Enters at |
|---|---|---|
| HA-11a | National and regional utilization of a specific presentation in units per year | `product.annual_demand_units`, regional shares, the derived status-quo utilization |
| HA-11b | The installed capacity that serves that presentation. **Not a question for you.** It is listed so you can see we know where it has to come from: FDA establishment registration and drug listing, the ANDA and RLD holder set, DQSA section 506C notifications, or a commercial data vendor. If you happen to hold it, say so; otherwise skip the row | the capacity side of the same comparison |
| HA-40 | At a real regional stocking point, what replenishment review policy runs, at what review frequency, and to what order-up-to level | `region_base_stock`, `region_reorder_point_days` |
| HA-43 | When a sterile injectable is unavailable, how long does an order remain a backorder before the demand is lost or substituted, and does that differ by presentation and by customer | `backorder_window_days` |
| HA-20 | Days of supply actually held, allocation practice, substitution behaviour, and a challenge to the product selection | demand and inventory parameters |
| HA-24 | Demand visibility, allocation practice, transport, and what resilience premium a purchaser would actually pay | `ContractTerms.price_required_usd_per_unit`, allocation rights, take-or-pay share |
| HA-36 | For a named presentation, would you sign a multi-year committed volume, at what volume, term and price, and what is the failure-to-supply remedy | the nine `ContractTerms` fields: payer, purchaser, beneficiary, term, committed volume, activation condition, allocation rights, default risk, price |
| HA-38 | Will anyone pay for standing availability of a civilian generic injectable separately from the units shipped? If so, at what annual amount, for what committed response time, and under what activation condition | `ContractTerms`; whether any capacity-carrying design is funded at all |

HA-38 is the one the author most wants answered, and a flat "no, nobody funds that" is the most valuable
answer in this packet, because it removes a whole class of design by construction. Please do not soften it.

Nothing above asks you to commit to anything. A statement of what a purchaser would plausibly do is recorded as
exactly that, and never as a term sheet, a letter of intent, or an indication of interest.

---

## 8. Current limitations, stated before you find them

- Every demand, cost, price and inventory input is illustrative. No absolute cost, break-even price or premium
  in this package is a statement about the world.
- Zero interviews have been logged against a target of 25 to 30.
- The two presentations are near-clones on several axes and one of them failed its own beachhead verification,
  so it functions as a control rather than as a second case. Product selection is deliberately not made.
- Allocation rights were inert (NEW-2) and opening inventory was free (NEW-1). Both are fixed in code under R011
  and R009, and the numbers in this packet predate both fixes. With the default of identical regions three of the
  four allocation policies still return the same fill, which is arithmetic rather than a defect.
- The backcasts are weak: three ongoing shortages of one class against a requirement of four episode classes.
- `docs/audits/05_inconsistencies.md`; `docs/audits/04_requirements_matrix.csv` status column;
  `reports/appendices/limitations.md`.
- Nine of twenty-two definition-of-finished tests pass, and eleven of the thirteen incomplete ones cannot be
  closed by any amount of code.

---

## 9. The form the review should take

Write it however you like, including as a conversation we transcribe and send back to you. We convert it into
`docs/reviewer_packets/reviews/<review_id>.json` with the schema in `docs/reviewer_packets/reviews/README.md`, and you correct the converted file before it
is counted. Per issue we need:

1. **The issue**, in your words, tied to a number, a policy, or a line of the claim in section 2.
2. **What you would use instead**: a number with a range, a policy description, or a named role who has it.
3. **What it changes if you are right**: which result you expect to move, and in which direction.
4. **Confidence**, in your own terms, and whether you are speaking from your own operation's data, from
   general experience of the market, or from what you have been told.

We record our decision against each issue, accepted, partially accepted, or rejected, with the rationale and
the exact model change, and append a row to `docs/reviewer_packets/reviews/revision_log.csv`. Rejections get the same written
rationale as acceptances. The record is published with the package.

Please also say plainly: **what in this package you would refuse to sign your name to**, and **which of these
questions you are not the right person to answer.** A review that shows the demand denominator is wrong, or
that no purchaser signs the commitment the surviving designs need, is a complete and successful review.

Attribution is by role and organisation type only unless you authorise more in writing. Nothing you say will be
described as a partnership, an endorsement, a customer relationship, a pilot, a commitment, or an intention to
purchase.
