# Correction after revisions R009 to R011

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every number here is engine behaviour under evidence
tier 5 inputs. All sixteen regulatory gates are UNCERTAIN, eligibility is NO_CONCLUSION for every strategy, and no
favourable decision class is assigned.

Written 2026-09-06. This document corrects `strategic_synthesis.md` and `feasibility_regions.md`, which were written
against runs that predate revisions R009, R010 and R011. Read it before quoting either.

## What changed in the model

| Revision | Defect | What it changed |
|---|---|---|
| R009 | NEW-1 | Opening inventory is purchased and charged once at production unit value, into a new `opening_inventory` ledger field. It used to be handed to every design for nothing, and it scaled with the design's own stock policy, so a deep-stock architecture received its stock free. |
| R010 | MD-3, MD-12 | Every frozen comparator now searches the same inventory space the design-space strategies declare: safety stock 30 to 365 days, the daily base-stock review as a binary, site finished-goods days and material target days. The old spaces are kept as `LEGACY_DESIGN_SPACES` so earlier runs stay reproducible. |
| R010 | MD-11 | The optimizer's tie-break on infeasible points now requires an improvement to exceed a noise band derived from the screen size before it counts. It had been buying large cost increases for fill differences inside Monte Carlo noise. |
| R011 | MD-1 | Pipeline cover is separated from safety and cycle cover, so shortening a lead time no longer shrinks the buffer. |
| R011 | NEW-2 | Regions can carry differing criticality weights and minimum guarantees, and the guarantee now reaches the allocator. With identical regions three of the four allocation policies remain one function, which is arithmetic rather than a defect. |
| R011 | MD-23, MD-24 | Any batch restarts a reserved line's readiness clock, and a take-or-pay commitment buys priority in the region sourcing order, so a volume commitment finally has a service channel. |

## Why this document exists rather than an edit in place

The optimization that followed the fixes ran at 10 search runs and 40 final runs rather than 20 and 100, to finish in
reasonable time. At 40 runs the binomial standard error at the requirement is 0.047, and fourteen cells changed
feasibility classification with most of them sitting inside that band. Attributing the change to the fixes would have
been unsafe, so every incumbent design was re-evaluated at 100 paired runs without re-searching
(`scripts/reevaluate_optima.py`, results in `results/design_space/reeval_post_R009.json`). That isolates the cause: a
design that changes classification at full resolution changed because of the design, not the screen.

Three of forty cells changed classification at full resolution. The fixes did the work. Sixteen of forty, however,
sit within one standard error of the requirement, so for two fifths of the set the feasible line is genuinely fuzzy
and any single cell's verdict should be read as provisional.

## The verified feasible set

Fourteen of forty cells meet the frozen target at 100 paired runs. Cells marked borderline sit within one standard
error of the tail requirement.

| Product | Strategy | Family | Cost USD/yr | Mean fill | P(meet) | Borderline |
|---|---|---|---|---|---|---|
| norepinephrine | S11 bright-stock campaign offtake | postponement | 15.2M | 0.9952 | 0.900 | yes |
| norepinephrine | S19 maintained switching package | upstream-first | 15.9M | 0.9943 | 0.920 | yes |
| norepinephrine | S2 dual source plus contracts | **frozen comparator** | 18.0M | 0.9989 | 0.960 | no |
| norepinephrine | S17 rotating prequalified campaigns | warm standby | 18.4M | 0.9975 | 1.000 | no |
| norepinephrine | S13 contracted base plus rotated surge | virtual network | 18.8M | 0.9964 | 0.900 | yes |
| sodium bicarbonate | S17 rotating prequalified campaigns | warm standby | 19.4M | 0.9960 | 0.900 | yes |
| norepinephrine | S5 distributed nodes | **frozen comparator** | 20.0M | 0.9963 | 0.940 | no |
| norepinephrine | S6 nodes plus release layer | **frozen comparator** | 21.0M | 0.9963 | 0.940 | no |
| sodium bicarbonate | S12 contracted registered capacity | virtual network | 21.5M | 0.9967 | 0.920 | yes |
| norepinephrine | S8 acquired registered line | telo architectures | 22.5M | 0.9964 | 0.910 | yes |
| norepinephrine | S9 dual source plus key-starting-material tier | upstream-first | 23.3M | 0.9975 | 0.920 | yes |
| norepinephrine | S14 cooperative-financed second source | public-private | 23.9M | 0.9964 | 0.920 | yes |
| sodium bicarbonate | S18 dual committed supply, distinct sources | contracts | 24.2M | 0.9977 | 0.930 | no |
| sodium bicarbonate | S9 dual source plus key-starting-material tier | upstream-first | 24.6M | 0.9987 | 0.940 | no |

## What this corrects in the synthesis

**Three statements are now wrong and are withdrawn.**

First, `strategic_synthesis.md` section 1 says the distributed owned nodes meet the frozen target in no region of any
recorded range of any swept input, on either product. That is no longer true. For norepinephrine S5 and S6 meet it at
a tail probability of 0.940, which is not a borderline result, at 20.0M and 21.0M. What made them infeasible before
was in part the unequal search space closed by R010: they had been denied the inventory freedom their competitors
were given. They remain infeasible for sodium bicarbonate, whose plant is capacity-short by construction.

Second, the same document treats it as settled that no frozen comparator meets the target. Dual sourcing meets it for
norepinephrine at 0.960, the second-highest tail probability in the set, and the distributed nodes meet it as well.
Three of the eight original comparators now clear on at least one product.

Third, the claim that bright-stock postponement and the reserve-triggered contracted network are the strongest shape
does not survive for sodium bicarbonate. Once opening inventory is charged rather than given, S11 falls to a tail
probability of 0.630 and S16 to 0.780 on that product. Both had been carrying roughly 1.2 million free units, about
five years of the structural capacity gap, inside a five-year window. S11 survives for norepinephrine and is the
cheapest feasible cell in the set, but it is borderline.

## What survives, and what is now the better answer

Two architectures meet the target on **both** products: rotating prequalified campaigns across three registered
third-party fill lines (S17), and dual finished-dose sourcing with an explicit key-starting-material tier (S9). No
other strategy in the battery, frozen or new, clears both. S17 is the cheaper of the two on both products and returns
the only tail probability of 1.000 anywhere in the set.

That is a narrower and more defensible answer than the one the synthesis gives. The earlier answer was a shape, buy
registered capacity and position stock. The shape survives, but its cheapest expressions were partly an artifact of
free inventory, and what actually clears both products is the version that keeps several already-registered lines
warm by rotating real campaigns through them, or the version that pays for genuine source independence up to the
starting material.

The direction of the original thesis is still not rescued. Distributed nodes clear only for the product that is not
capacity-short, they cost 20.0M against 18.4M for rotating campaigns and 18.0M for plain dual sourcing, and the
release-layer variant S6 costs 1.0M more than S5 for identical service, which is the same result the study has
returned throughout.

## What must be re-run before any of this is final

The battery after R009 completed only its first two stages. The tau 0.98 optimization, the ablation, the interaction
study, the feasibility conditions, the figures and the contract table were not re-run, so every threshold and every
condition in `feasibility_regions.md` still describes the pre-R009 engine. The conditions are the part of that
document most likely to move, because charging for opening inventory changes the shelf-life and changeover margins
directly.

Until those runs land, use this document for the feasible set and the ranking, and treat `feasibility_regions.md`
sections 2 to 7 and `strategic_synthesis.md` sections 5 to 9 as superseded on any point where they disagree with it.
