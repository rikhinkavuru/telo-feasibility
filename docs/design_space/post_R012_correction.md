# Correction after the post-R011 battery of 2026-09-10

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every number here is engine behaviour under evidence
tier 5 inputs. All sixteen regulatory gates are UNCERTAIN, eligibility is NO_CONCLUSION for every strategy, and
no favourable decision class is assigned.

Written 2026-09-23. This document supersedes the feasible-set figures in `post_R009_correction.md`,
`strategic_synthesis.md`, `feasibility_regions.md`, `reports/memo/`, `reports/executive_summary/` and
`reports/docket_comment/`. Read it before quoting any of them.

## 1. What produced the change

The full battery finally ran on the fixed engine, overnight on 2026-09-10: optimization
`opt_20260910T012608Z`, simulation `sim_20260910T033418Z`, ablation `abl_20260910T033500Z`, design space
`ds_20260910T063609Z`, matched space `matched_20260910T113900Z.json`. This is condition (b) of
`docs/reviewer_packets/README.md` section 1, which had been the only thing holding the reviewer packets.

Every figure previously quoted came from one of two weaker sources. The optimization behind them predates
R010, the revision that gave every frozen comparator the same inventory search space the design-space
strategies declare for themselves. The `reeval_post_R009.json` figures then took each cell's **existing
incumbent design** and re-evaluated it at 100 paired runs *without re-searching*, which was the right way to
separate a fix effect from screen noise but does not search the corrected space.

So the earlier numbers answer a narrower question than the new ones: they measure old designs at higher
resolution, not the best design available inside the corrected space.

## 2. What changed, and why it changed in one direction

Eleven of forty cells moved from infeasible to feasible. **None moved the other way.** That asymmetry is the
signature of a search-space change rather than a defect: every strategy was given more freedom, so more cells
found a design that meets the target, and none could lose one it already had.

| product | cells that became feasible |
|---|---|
| norepinephrine 1 mg/mL 4 mL | S4, S8, S12, S16 |
| sodium bicarbonate 8.4% 50 mL | S3, S4, S10, S11, S14, S16, S18 |

The feasible set is now **24 of 40 cells**, against 14 of 40 in the post-R009 re-evaluation.

## 3. The claims this retracts

**R-1. "Only two architectures meet the target on both products."** Withdrawn. Eight do: S4, S9, S11, S12,
S14, S16, S17 and S18. The sentence appears in `strategic_synthesis.md`, in the memo conclusion, and in the
executive summary.

**R-2. "Fourteen of forty cells meet the frozen target."** Withdrawn, replaced by twenty-four of forty.

**R-3. "Sixteen of forty sit within one standard error of the requirement."** Withdrawn. At n = 100 the
binomial standard error at q = 0.90 is 0.030, and eleven of forty now sit inside that band: S3, S11, S13, S18
and S19 on norepinephrine, and S5, S6, S10, S12, S16 and S17 on sodium bicarbonate. Two fifths of the verdicts
were provisional before; slightly more than a quarter are now.

**R-4. The characterisation filed in the FDA docket comment.** The comment states that where the incumbent
plant is capacity-short, the configurations meeting the service requirement "buy campaigns on lines already
registered and inspected, with positioned finished-goods inventory." On the capacity-short product that set
now also contains **S4, additional centralized capacity**, at 24.1 million USD per year with P(meet) = 0.95.
Building centrally is not buying campaigns. The sentence is incomplete as filed, and it cannot be amended: a
submitted docket comment is a fixed public record. This is recorded here so the correction exists in the
study's own register, and so any future filing or reviewer packet states it correctly.

## 4. What survived, and is now better supported than before

**Owned distributed nodes still fail on the product that is actually capacity-short.** S5 returns
`infeasible_at_full_n` on sodium bicarbonate at P(meet) = 0.88, and S6, the release-assurance variant, returns
the same 0.88. They now fail having been given the *full* matched inventory space, which is the fairest test
the package has run. On the product that is not capacity-short both clear the bar, S5 at 20.0 and S6 at 21.0
million USD per year, which remains the honest and narrow form of the result.

**Adding a validated release layer to those nodes still buys nothing.** S6 tracks S5 to four decimals of mean
fill on both products while costing about a million USD per year more.

**Buying still beats building, on cost.** The cheapest feasible cell on each product is S11, bright-stock
campaign offtake, at 15.2 and 16.1 million USD per year. S4 clears the target on both products but costs 20.2
and 24.1 million, so the conventional answer works and is not cheap.

## 5. What this does not resolve

Nothing here adds a single elicited input. All 87 tier-5 parameters are still placeholders chosen by the
author, no interview has been completed against a target of 25 to 30, and no independent expert review exists
against a required three. A wider search over invented numbers finds better designs inside an invented world.
The correct reading of section 2 is that the comparison is now fair, not that the answer is now true.

## 6. Actions this forces

1. Reviewer packets: refresh every number from `results/manifests/battery_digest_opt_20260910T012608Z.md`
   before any packet is sent. Condition (b) is met; the packets are now stale rather than blocked.
2. Memo, executive summary and strategic synthesis: replace the feasible-set figures and the two-architecture
   sentence.
3. Interactive simulator: the surface at `results/design_space/simulator_surface.json` predates this battery
   and its feasibility shading is stale. Regenerate or label it.
4. Docket comment: no action possible on the filed copy. R-4 stands as the record.
