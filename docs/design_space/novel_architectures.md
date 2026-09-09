# Novel architectures (deliverable 6)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input behind every design in
this document is tier 5 (illustrative). Nothing here is a finding, a recommendation, a commitment, or
evidence about the world. Regulatory gates stay UNCERTAIN; UNCERTAIN is never PASS. No interview,
partner, customer, quote, or reviewer named here exists; where a counterparty is named it is a
published third party cited by source id, never a Telo relationship.

This is the Phase B/C/D bridge document. It records all 42 architectures the family sweep generated,
what each one is, which Phase A mechanism it attacks, where it sits against the prior-art review and
the competitive landscape, its novelty class and the test that would withdraw that class, the
adversarial judge tally, and the disposition: configured as a strategy id, or rejected with the
reason. For the twelve that were configured it also records the exact engine representation and the
approximations that representation forces.

## 1. How to read this

**Provenance.** Phase B generated 42 candidate architectures across the fourteen assigned families.
Three independent adversarial judges scored each on six criteria with different weightings: a
mechanism lens (does the architecture remove a mechanism Phase A resolved as binding), a
regulatory-commercial lens (is it permittable and contractable), and an evidence-novelty lens (is the
decisive evidence obtainable and is the position defensible). `total` below is the sum of the three
weighted scores, each on a 0-5 scale, so the maximum is 15. `keeps` is how many of the three judges
put the candidate in their own top twelve.

**Why twelve.** `StrategyId` in `src/telo_feasibility/schemas.py` enumerates S0 through S20, and
S0-S7 are the frozen protocol comparators, so exactly thirteen ids exist for 42 candidates. Twelve
were configured, in judge-rank order, as S8 through S19; S20 is left free. Every candidate's own YAML
carried the placeholder id `S99`, which does not validate; renumbering was universal and is not a
differentiator between candidates.

**What "configured" does and does not mean.** It means the architecture loads through
`configs.load_design_space_strategies`, builds through `strategies.build_strategy` and runs through
`simulation.run_paired` for both product dossiers, and that its regulatory gates are named so
`regulatory.evaluate_strategy` returns NO_CONCLUSION by analysis rather than by omission. It does not
mean the architecture is good, contractable, or recommended. Six of the twelve are instruments rather
than businesses: S9, S10, S12, S15, S18 and, in part, S13 exist to falsify a claim the package
currently rests on, not to be built.

**Contractability, across the whole set.** Under the assignment's own rule (`contracting.py`
`ContractTerms`), zero of the 42 candidates is contractable today, because no candidate has a signed
counterparty and `price_required_usd_per_unit` is a model output everywhere. What separates them is
how many of the nine required fields are answerable from documented instruments. Best is S14 (one
field open, on the Premier/Exela precedent); the modal candidate leaves five to nine unanswered.
Every design whose first revenue is a standing readiness or availability payment is unpayable on
present evidence: prior-art review open question 17 finds no US hospital system, GPO or state ever
paying such a fee for sterile generic capacity (F3-S28), and the two largest funded analogues both
ended with the sites leaving the business (CIADM, and the USD 542,750,000 Emergent capacity
reservation, LCDM-S35, LCDM-S10). That single fact removes six candidates from contention
independently of anything the model says. The designs that survive it monetise through an ordinary
unit sale of finished vials.

## 2. What was configured

| id | candidate key | family | sites | judge total | keeps | what it is in one line |
|---|---|---|---|---|---|---|
| S8 | acquired_registered_line_dual_site | telo_architectures | 2 | 10.54 | 3 | buy a second already-registered, already-inspected US aseptic line instead of building one |
| S9 | ksm_honest_dual_source | upstream_first | 2 | 9.79 | 2 | frozen S2 with the shared key-starting-material tier the engine currently omits; an adversarial control |
| S10 | split_tenancy_two_hosts | multi_product_portfolio | 3 | 9.77 | 3 | the same committed volume split across two unaffiliated multi-product hosts; prices independence at matched capacity |
| S11 | bright_stock_campaign_offtake | postponement | 2 | 9.69 | 3 | hold filled, capped, unlabeled units and finish to order, fed by a campaign offtake at a registered CDMO |
| S12 | vn_registered_capacity_base | virtual_network | 3 | 9.54 | 2 | contracted registered capacity at three third-party lines, no owned asset; the Civica reference arm |
| S13 | vn_base_surge_reserve | virtual_network | 3 | 9.52 | 2 | contracted base supply plus a rotated reserved surge plus a deep reserve; a three-leg design built to be ablated |
| S14 | cooperative_registered_second_source | public_private | 2 | 9.49 | 2 | cooperative equity buys an already registered plant and committed offtake pays for it |
| S15 | PS_B_capacity_adequate_buffer | product_selection | 1 | 9.46 | 3 | no plant at all: select a capacity-adequate presentation and fix the tail with positioned inventory |
| S16 | f8_reserve_triggered_campaign | inventory_capacity_hybrids | 3 | 9.35 | 2 | reserve depletion below a days-of-supply trigger calls a pre-qualified campaign at two contracted lines |
| S17 | rotating_campaign_network | warm_standby | 4 | 9.31 | 2 | rotate real campaigns across three registered third-party lines so all stay filed and current |
| S18 | dual_committed_supply_distinct_sources | contracts_procurement | 2 | 9.27 | 3 | a committed contract that mandates distinct API *and* container sources, which frozen S2 cannot express |
| S19 | upstream_switching_package | upstream_first | 2 | 9.16 | 2 | a maintained regulator-pre-agreed switching package plus an exercised standby line |

Eleven of the twelve totals fall inside a 0.63-point band, 9.16 to 9.79, with only S8 outside it at
10.54. That clustering is not an oversight. Five of the twelve (S8, S12, S14, S18 and, in a
different wrapper, S17) are variants of one shape: a second registered finished-dose source obtained
by acquisition, contract or cooperative equity and sold under committed volume. That is what
`bottleneck_decomposition.md` section 8 instructs Phase B to do, because an architecture that buys
registered capacity rather than building it carries exactly 0.000000 commissioning delta (pre-R004 Phase A ablation `abl_20260902_phaseA`; superseded by R004, re-run required)
and a 21-day rather than 730-day lead. They should be run as one comparison arm differing in who owns the asset
and who signs the contract, not as five independent architectures.

## 3. Configured architectures

Each entry gives: family, what it is, mechanisms it addresses and leaves binding, prior-art position,
novelty class and the observation that would withdraw it, judge tally, engine representation, and the
approximations the representation forces.

### S8 - Acquired registered line, two sites, split API and geography

*Family:* telo_architectures. *Candidate key:* `acquired_registered_line_dual_site`. *Judge total
10.54, keeps 3 of 3* (the only candidate all three judges kept and ranked first or second).

**What it is.** Telo owns the ANDA and two US aseptic lines. Site 1 is the incumbent line acquired
with the application and producing on day zero. Site 2 is a second US aseptic line acquired as a
currently registered, currently inspected operating asset and added to the same application. Nothing
is built, leased or reserved. The two sites take different API suppliers and sit in different regions.

**Mechanisms addressed.** Capacity shortfall (the only structural Phase A failure), commissioning
delay (avoided rather than solved), site failures (16 of 16 resolved, 6 flips, the largest of any
factor), surge headroom, supplier concentration on API only, common cause on geography and API only.
**Left binding:** contract insufficiency, the fixed quality cost block and replicated validation
(24.1 to 33.0 percent and 4.7 to 18.0 percent of annual cost in the pre-R004 Phase A ablation,
`results/manifests/abl_20260902_phaseA.json`; superseded by R004, re-run required), low utilization,
`cc_vial_1`, `cc_stopper_1` and `cc_quality` which all still span the two sites, and release time,
which Phase A says was never binding.

**Prior-art position.** Family 1's own reading of its failure cases is that the documented failure is
not the science of small-scale production but the capital and time to reach a licensed, inspected,
commercial state: Civica slipped from 2024 to 2026 with no commercial batch as of August 2025
(F1-S56, F1-S58); CONTINUUS took 69.3M USD and never commissioned (F1-S45, F1-S23, F1-S59); ODP
reached a 503A pilot of about 12,000 syringes and is not on FDA's outsourcing-facility table
(F1-S40, F1-S43, F1-S16). All four are builds. Registered US sterile sites do change hands (LCDM-S9,
LCDM-S10, LCDM-S33, LSIM-S28, L503B-S20). Capital anchors to negotiate against: 132M USD for a new
line and building (F1-S51), 25M USD for a line inside an existing plant (F1-S52), about 30M USD for
four Camden commercial aseptic lines in a distressed sale (LCDM-S10). This is the only move in family
1 that changes the documented failure mode rather than repeating it, and it needs no regulatory
instrument that does not exist today.

**Novelty:** novel_combination. *Withdrawn if:* a generic sterile injectable company is found that
has publicly built its second source by acquiring a registered inspected line specifically for
shortage resilience under committed volume. Sagent's purchase of Athenex generic injectable assets
out of Chapter 11 (LSIM-S28) is close enough that the class is fragile.

**Judge criticism carried forward.** All three judges made the same point: the headline commissioning
advantage is currently unmeasured. MD-17 puts `second_source_qualification_days` base,
`capacity_expansion_days` and `warm_up_days` all at 365, so at the declared base the acquired site
opens on the first measured day and loses 0 percent of the measured window. A 12-run smoke check
during candidate generation gave mean fill 1.0000 at 180 d, 0.9974 at 365 d and 0.9458 at 730 d,
which is the artifact made visible. *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)* No commissioning claim may be quoted until the measurement
boundary is separated from the parameter grid. Second live risk: the acquisition target set is
thinning as merchant US aseptic sites go captive (LCDM-S1, LCDM-S10, LCDM-S30, LCDM-S33).

**Engine representation.** Two `central`-archetype site plans at `scale` 1.05 (= `STATUS_QUO_SCALE`,
so neither is an expansion and neither waits `capacity_expansion_days`). `second_source` in R3 with
`exists_at_t0: false` and `commissioning_days: 365.0`, which reuses the frozen S2 second-source id
and region so entity-keyed random streams pair the comparison. Groups: `cc_api_1`/`cc_api_2` split,
`cc_vial_1` and `cc_quality` shared, `cc_geo_R1`/`cc_geo_R3` split. `region_base_stock: 1` opts out
of the frozen review rule (MD-3). Search: `safety_stock_days`, `region_base_stock`, `site_fg_days`,
`material_target_days`.

**Approximations this representation forces.** (1) The acquired line is charged full greenfield
capital (`capital_multiplier` 1.0), which is deliberately conservative but means the acquisition
price cannot be entered as evidence; `capital_usd_per_site` is a product-level tier-5 parameter and
there is no per-site capital override. (2) MD-15: one product per network, so utilization and the
fixed-quality block cannot be relieved by a portfolio, and modelled unit cost is an upper bound.
(3) MD-17 as above. (4) MD-1 unfixed, so `material_target_days` still scales the buffer with the lead
time and part of the material search measures buffer depth rather than material policy.

### S9 - Dual finished-dose source with an explicit key-starting-material tier

*Family:* upstream_first. *Candidate key:* `ksm_honest_dual_source`. *Judge total 9.79, keeps 2 of 3.*

**What it is.** Frozen S2 rebuilt in configuration with one change: the two API suppliers sit in
distinct API groups *and* in one shared upstream group `cc_ksm_api_1` together with both sites. It is
an adversarial control on the package's only clearing strategy, not a business proposal.

**Mechanisms addressed.** Supplier concentration, specifically the branch the frozen model cannot
see: S2 gives its second source a distinct `cc_api_2` group whenever `independent_api_supplier = 1`,
which asserts independence the upstream evidence denies. Also common-cause failure (the last binding
mechanism in exactly the two S2 cells), capacity, and site failures. **Left binding:** commissioning
(365 d, and MD-17 makes it unmeasurable at that value), the two cost blocks, contract insufficiency.

**Prior-art position.** USP reports 58 percent of key starting materials sole sourced from a single
country, 41 percent from China, China as sole supplier of at least one KSM for 679 APIs, and states
that diverse API or finished-dose manufacturing offers little protection when all depend on the same
upstream source (F9-S5, F9-S7). API supplier diversification is standard practice, federally funded
through Phlow and APIIC (F9-S17, F9-S19), and is being legislated as an EU procurement criterion
(F9-S31).

**Novelty:** already_implemented. It is dual sourcing. *Withdrawn (upgraded) only if* the shared-KSM
tier turns out to be a modelling contribution nobody else makes, which is a claim about the model and
not about the world, so it is not claimed.

**Judge criticism carried forward.** Its value is entirely diagnostic and it may return nothing:
decomposition 6.12 already reports the independent and shared API branches of S2 differing by exactly
0.000000 fill in 30 of 36 matched pairs at higher `capacity_factor` (pre-R004 Phase A ablation `abl_20260902_phaseA`; superseded by R004, re-run required), so capacity may substitute
almost perfectly for supplier independence. It has no moat, doubles the fixed quality and validation
blocks, and one judge called it "the highest-information non-kept item across all 42" precisely
because it is an instrument.

**Engine representation.** Two `central` sites at `scale` 1.0 with `capacity_factor` 1.2 (so central
runs at 1.05 until day 365 under the R004 expansion rule, then at 1.2). Two declared
`extra_suppliers`, `api_src_a` and `api_src_b`, each at `lead_time_factor` 1.0, each in its own API
group and both in `cc_ksm_api_1` with both sites. Frozen S2's illustrative design variables are
reused verbatim so the read-across is clean. `cc_quality` is declared on both sites (added
2026-09-03): this design's own regulatory owner is one ANDA holder for both sites, so one quality
unit disposes both and 21 CFR 211.22(a) makes that non-delegable (F3-S41, F3-S42, F3-S43). The
earlier configuration omitted it on a separate-legal-entities rationale that contradicted its own
regulatory-owner field, which was the sharpest case in the set, because this design exists to make an
omitted correlation honest. `cc_stopper_1` and `cc_geo_R3` were added under the same pass.

**Approximations.** (1) Adding a group id adds an independent Poisson event stream at the same global
`common_cause_events_per_year`, so an honest upstream tier costs hazard as well as correlation; the
only clean control is the matched-membership run in the falsification register (same group count,
split membership). (2) `CommonCauseGroup.kind` has no key-starting-material value; `cc_ksm_api_1`
resolves to `api_supplier` only because its id contains the substring `api`. (3) A site draws each
component from exactly one supplier, so genuine dual sourcing *at one site* cannot be represented at
all; only two sites with two suppliers can. (4) MD-17.

### S10 - Split tenancy across two independent multi-product hosts

*Family:* multi_product_portfolio. *Candidate key:* `split_tenancy_two_hosts`. *Judge total 9.77,
keeps 3 of 3.*

**What it is.** Telo owns no plant. The same committed volume is split across two unaffiliated
multi-product host sites, each taking a 20 percent tenancy of a full line, each with its own quality
unit and registration. It exists to price independence at matched capacity against a single-host
sibling.

**Mechanisms addressed.** Common-cause failure (resolved in 13 of 16 Phase A cells, flips cells at
the tail), supplier concentration, capacity, commissioning, and the fixed quality cost block through
tenancy. **Left binding:** surge headroom (no reserved slot), inventory timing, contract
insufficiency, replicated validation, which this design deliberately *increases*.

**Prior-art position.** The evidence that concentration causes shortages is the strongest in the
family: GAO found four of six facility-shutdown shortages came from one manufacturer's single
facility (F6-S14); FDA staff summarised plant-level events as affecting multiple products at once
(F6-S16); USP records the risk as acute where one facility makes the entire US supply (F6-S20); Akorn,
Intas and PharMEDium are three documented instances of one site taking a whole portfolio down
(F6-S24, F6-S22). The base rate is against the design: only 11 of about 900 sterile-injectable ANDAs
approved 2000-2011 referenced more than one finished-dose facility (F6-S37).

**Novelty:** novel_combination. *Withdrawn if:* a generic sterile injectable is found that
deliberately maintains matched tenancies at two unaffiliated multi-product hosts for resilience
rather than for capacity.

**Judge criticism carried forward.** In its own smoke run it was dominated by the single-host sibling
on both service and cost (0.9436 fill at 15.68 USD/unit against 0.9834 at 15.28 *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*), because the
sibling's divertible option contributes surge capacity that two static half-tenancies do not and
because two full validations cost more than one. HHS's diagnosis cuts against the business case
directly: generic prices are driven so low that they create insufficient incentives for redundancy
(F6-S18). And the independence may be attributable to `api_2` rather than to site independence, which
is what the prescribed ablation is for.

**Engine representation.** Three site plans: the incumbent `central` at 1.05, plus `shared_suite_1`
(R3, api_1) and `shared_suite_2` (R4, api_2), each `portfolio_capacity_share` 0.20 and
`portfolio_fixed_cost_share` 0.20 with `validation_multiplier` 5.0, which undoes the 0.20 share so
each host pays one full product-specific validation (F6-S11, F6-S04). `batch_size_fraction` 1.0 keeps
each host filling full-size batches at a fifth of the cadence. Both hosts keep `vial_1` and
`stopper_1` on purpose, so the container leg of the correlation is untouched and is now declared as
`cc_stopper_1` on all three sites. `cc_quality` is also declared on all three (added 2026-09-03):
Telo's quality unit dispositions at both hosts, which is non-delegable under 21 CFR 211.22(a)
(F3-S41, F3-S42, F3-S43), so a disposition-function failure stops release from all three sites at
once. The previous `quality_owner` field asserted the opposite in the same sentence pair. Because the
whole purpose of this design is to price independence, the S10-versus-single-host paired comparison
has to be re-run with the group present; the single-host control is an internal variant of S10 (one
host at portfolio shares 0.4 and `validation_multiplier` 2.5), not a configured sibling strategy,
since no anchor-tenancy strategy exists anywhere in the package. That re-run has been done on the
post-R007 configuration with the group present: two hosts reach mean fill 0.95507 (MCSE 0.00755) at
18,612,988 USD/yr against the single host's 0.95353 (MCSE 0.00809) at 17,918,556, p_meet 0.16 in both
arms. The service difference is inside its MCSE and the second host costs 0.69M USD/yr more, so on
this engine concentration wins and the disposition stands, now for a measured reason rather than an
unregistered smoke run *(verification-pass paired run, sodium bicarbonate, master seed 20260901,
n = 25, horizon 2191 d after a 365 d warm-up, no manifest; re-run inside the Phase D battery before
quoting)*.

**Approximations.** (1) Portfolio shares are `SitePlanSpec` constants, not design variables, so the
optimizer cannot search the split ratio; it is asserted, not found. (2) The engine charges no
changeover, cleaning-validation, media-fill or campaign-scheduling cost against a tenancy, and MD-15
hides the host's other products entirely, so a host event that would remove several products at once
is scored against one. (3) `cc_stopper_1` is now declared on all three sites (2026-09-03), so container-closure
concentration is represented rather than only noted in prose. The frozen builder still gives the
`stopper_1` *supplier* no group, so this is the site-side representation only and S0-S7 do not carry
it; the comparison against them must equalise the group or report the gap, and the matched-membership
control separates the added Poisson hazard from the added correlation. (4) MD-17 applies to both
365-day host additions.

### S11 - Bright-stock campaign offtake with a national undifferentiated reserve

*Family:* postponement. *Candidate key:* `bright_stock_campaign_offtake`. *Judge total 9.69, keeps 3
of 3.*

**What it is.** Two registered lines fill into a common container and hold output as filled, capped,
cap-coded, *unlabeled* units. Telo owns the pool, the finishing operation and the NDC, and labels to
order. The second line is a campaign offtake at a registered CDMO, exercised six times a year and
callable when regional days of supply fall below a trigger.

**Mechanisms addressed.** Capacity shortfall, commissioning delay (zero: both sites exist at t0),
contract insufficiency, inventory timing. **Left binding:** common cause, supplier concentration,
surge headroom beyond the offtake, site failures, demand variance and covariance, and all three cost
blocks.

**Prior-art position.** Late labeling is codified US practice since 1978 (F5-S08) and is sold as a
service by PCI and Sharp (F5-S46, F5-S47). The regulatory asymmetry that makes the design cheap is
real and cited: FDA's 2004 guidance places a move to a different site for labeling and secondary
packaging among *minor* changes provided the site has a satisfactory CGMP inspection for that
operation, against CBE-30 or a prior approval supplement for primary packaging or aseptic processing
(F5-S14). The documented failure mode is content-to-label mismatch, with two named recalls (F5-S48,
F5-S49). No CDMO is known to sell bright stock to a third-party labeler for US shortage generics
(F5 section 9), and no US sterile fill-finish rate card, minimum order value or reservation fee is
public (landscape cdmos section 6).

**Novelty:** novel_combination, and the *combination* is what is claimed, not the postponement.
*Withdrawn if:* an operating pooled bright-stock service for US generic injectables is found.

**Judge criticism carried forward, and it is severe.** All three judges made the same point: the
postponement content is probably exactly zero by construction. With one presentation, one market and
one labeler under MD-15, the unlabeled pool and the labeled finished-goods pool are the same object,
so the risk-pooling benefit Lee and Tang derive from variant count and imperfect demand correlation
(F5-S01) has nothing to act on. Everything the run reports will be the campaign offtake plus the
review rule, and the offtake adds about 48 percent capacity to a plant that is over-utilized by
construction. The capacity-matched control in the falsification register must be run *first*. The
candidate is configured for the offtake shape, not for the postponement story.

**Engine representation.** `central` at 1.05 plus `reserved_cdmo` in R3, `cdmo_reserved` archetype,
`scale` 0.5, `exists_at_t0: true`, `reserved: true`, `exercise_batches_per_year` 6.0,
`activation_failure_probability` 0.15, `reserved_site_owned: 0` (so after R004 Telo carries only the
reservation fee plus variable and testing cost on batches actually run), `take_or_pay_fraction` 0.5.
The two-echelon inventory is `site_fg_days` 120 (the pool) against `safety_stock_days` 30 (thin
regional tier) with `region_base_stock` 1. The 5-day finishing step is folded into `delivery_days`
(5 transport + 5 finish = 10).

**Approximations.** (1) There is no intermediate inventory stage in the engine: it goes site finished
goods, lane, region stock, with no pool-then-finish-then-ship stage carrying its own lead time and
its own capacity. Folding the finish into `delivery_days` overstates transit and gives the finishing
step infinite capacity. (2) Release-time components are global for every site, so a labeling site
would re-incur the full 14-day sterility hold if it were declared as a site. (3) No design variable
scales a single declared site, so the offtake volume cannot be searched and stays a labelled
sensitivity. (4) There is no labeler dimension and no `bright_stock_offtake_fraction`, which is where
the family's actual mechanism would live. (5) NEW-1: the exercise cadence buys production, not
readiness.

### S12 - Contracted registered-capacity supply base

*Family:* virtual_network. *Candidate key:* `vn_registered_capacity_base`. *Judge total 9.54, keeps 2
of 3.*

**What it is.** Telo owns no manufacturing asset. Three third-party registered US establishments
supply under contract: the incumbent line on day 0, a CBE-30-class partner at 365 days with
independent API and container sources, and a prior-approval-supplement partner at 730 days. Telo owns
the application or label, the quality unit, the transfer packages and the inventory.

**Mechanisms addressed.** Capacity shortfall at sites that already exist, commissioning delay,
supplier concentration at one of the three sites, geography common cause. **Left binding:**
`cc_quality` spanning all three sites (a deliberate honesty choice that makes this candidate look
*worse* than frozen S2, which carries no `cc_quality`), `cc_api_1`/`cc_vial_1` across two of three,
contract insufficiency, inventory timing, both cost blocks, surge headroom (firm capacity only, no
option).

**Prior-art position.** The quality-unit constraint is not optional and is cited three ways: 21 CFR
211.22(a) (F3-S42), 21 CFR 200.10(b) treating extramural facilities as an extension of the
manufacturer (F3-S43), and FDA quality-agreements guidance stating a quality agreement cannot
delegate CGMP responsibility (F3-S41). The DME registration route is not available to an unaffiliated
network (F3-R4). The one disclosed US CDMO capacity agreement runs the wrong way: annual committed
capacity obligations on the CDMO with no minimum purchase obligation on the customer (LCDM-S14).

**Novelty:** already_implemented. It is Civica, at 14 partners and 77 products (F3-S25).
*The class is not withdrawable;* it is already at the "implemented" end.

**Judge criticism carried forward.** Pruning rule P5 requires a stated reason Telo beats the named
incumbent, and the evidence supplies none. The only differentiator offered, keeping second and third
sites filed and inspection-current, is capped by FDA's own carve-out at CBE-30 and cannot pre-clear
inspection status (F3-S46). Its own scoping run gave worse service than frozen S2 for less money
(0.9677 fill, p_meet 0.37 at 23.23M against 0.9960, 0.97 at 27.19M) *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*. One judge also measured that the
R004 ownership convention makes the same physical network cost 23.23M or 16.61M USD/yr with
bit-identical service, a 28 percent spread that is a modelling convention, so no cost ranking from
this candidate is quotable until a per-site owned boolean exists. **It is configured as the family's
reference architecture and mandatory comparator, not as a recommendation.**

**Engine representation.** Three `central`-archetype plans (`central` 1.05, `second_source` 0.30 at
365 d, `cdmo_r2` 0.20 at 730 d), one declared extra supplier `vial_2` at `lead_time_factor` 0.5, and
`cc_quality` on all three sites. `cc_os` is deliberately absent: this candidate carries no cross-site
operating system, because the cross-family review finds no OS sub-form that reaches a binding
mechanism and a shared OS version is itself a common-cause group.

**Approximations.** (1) Ownership is a property of the `reserved` flag, not of the site, so these
contracted partner sites carry full capital, fixed operations and validation as if Telo built them.
That is the 28 percent cost spread above. Minimal fix: a per-site `owned` boolean on `SitePlanSpec`
driving the same branch `reserved_site_owned` drives today. (2) No CDMO margin: unit cost at a partner
site is the product's own variable cost, so contracted manufacturing is charged at cost. (3)
`take_or_pay_fraction` applies only to reserved sites, so a firm minimum-purchase commitment at a
contracted site cannot be charged. (4) Per-site `commissioning_days` is a config constant, not a
searchable design variable, so the family's core latency claim cannot be swept. (5) MD-17 on the
365-day leg.

### S13 - Contracted base supply plus rotated reserved surge plus reserve inventory

*Family:* virtual_network. *Candidate key:* `vn_base_surge_reserve`. *Judge total 9.52, keeps 2 of 3.*

**What it is.** Three legs at once: contracted base capacity at a firm partner with independent API
and container sources, a rotated reserved surge option at a third registered site, and a deep reserve
held as regional and site stock under a daily base-stock review. It is built to be ablated leg by leg.

**Mechanisms addressed.** Capacity shortfall, inventory timing (the mechanism Phase A says fixes the
tail), surge headroom, commissioning (nothing is built), supplier concentration at the firm partner,
and part of contract insufficiency, because the largest leg is inventory and inventory is a purchase
a hospital buyer already makes rather than a readiness payment nobody has been found paying.
**Left binding:** `cc_quality` across all three sites, `cc_api_1`/`cc_vial_1` between the incumbent
and the option site, regulatory availability, both cost blocks, low utilization at the option site.

**Prior-art position.** The shape matches the only operator that ever ran this family at scale:
contracted supply paired with a six-month buffer (F3-S30, F3-S25), plus the six-month API reserve
directed for the strategic reserve (F3-S35). Those are comparator values from the world, not Telo
design values.

**Novelty:** novel_combination. *Withdrawn if:* the ablation shows the rotated surge leg contributes
nothing, in which case the design is frozen S2 plus frozen S1 and the novelty claim collapses with it.

**Judge criticism carried forward.** All three judges expect the ablation to show the gain is the
inventory leg alone. That leg sits directly on two known defects, MD-3 (the frozen review rule,
decisive in 8 of 16 cells) and MD-4 (opening-stock cohorts, fixed in R004, which invalidates every
pre-2026-09-03 safety-stock conclusion), plus the newly surfaced free-opening-inventory defect that
endows deep-stock designs with unbilled product. And the rotation leg's ablation is guaranteed to
read zero for engine reasons rather than world reasons, because no capability-decay hazard exists.

**Engine representation.** `central` 1.05 + `second_source` 0.30 at 365 d (api_2, vial_2) +
`reserved_cdmo` 0.35 (`exists_at_t0: true`, `reserved: true`, exercise 2/yr, p_fail 0.15,
`reserved_site_owned: 0`, `take_or_pay_fraction` 0.3). Inventory: `safety_stock_days` 120 searched to
365, `site_fg_days` 60, `material_target_days` 90, `region_base_stock` 1.

**Approximations.** Same ownership, margin and take-or-pay limits as S12, plus: (1) no capability
decay behind `exercise_batches_per_year`, so the rotation leg's reliability contribution is
unmeasurable; (2) MD-1 still deferred, so the 90-day material buffer scales with the lead time and
its sign is not guaranteed; (3) free opening inventory flatters this design more than any other in
the battery except S15.

### S14 - Cooperative-financed registered second source with committed offtake

*Family:* public_private. *Candidate key:* `cooperative_registered_second_source`. *Judge total 9.49,
keeps 2 of 3.*

**What it is.** A health-system cooperative or GPO-sponsored vehicle supplies equity; Telo or the
vehicle acquires an already registered sterile plant rather than building one, and committed offtake
from member hospitals pays for it. It is the only design in the batch that puts capital and committed
demand in a single instrument.

**Mechanisms addressed.** Capacity shortfall, supplier concentration, commissioning (by acquiring
rather than building), contract insufficiency, low utilization. **Left binding:** common cause on the
shared container supplier, inventory timing, the fixed quality cost block (which roughly *doubles*
here rather than being shared), replicated validation, and the site-transfer supplement category,
which is UNCERTAIN under G02 and G07.

**Prior-art position.** There is exactly one documented instrument that delivered capital and
committed demand together for US sterile injectables: Premier and eleven health systems took a
minority stake in Exela with multi-year commitments to purchase through the GPO (F13-S23). California
reached the same correction, concluding the state should partner rather than build (F13-S18).

**Novelty:** already_implemented (the ownership form). *The class is not withdrawable.*

**Judge criticism carried forward.** The 365-day site-transfer assumption carries the entire
candidate and is a tier-5 placeholder set equal to the frozen `second_source_qualification_days` base;
it is directly contradicted by the closest observed case, a 503B operator that bought a registered
110,000 square foot sterile plant in February 2022 which FDA still recorded as not yet inspected 4.2
years later (L503B-S01, L503B-S21). MD-17 separately makes 365 coincide with `warm_up_days`. P5
applies: Civica is member-owned and Premier/Exela already runs this instrument. And building or
buying capacity does not create demand, which USAntibiotics demonstrates at about five percent of the
market against capacity for 100 percent, naming the absence of long-term purchasing agreements as the
cause (F13-S31).

**Engine representation.** Two `central` sites, `central` at `scale` 1.0 x `capacity_factor` and
`second_source` in R3 at 365 d, reusing S2's second-source id and region so the comparison is paired.
`capacity_factor` is in the search space from 1.05 to 1.60 and both sites use the `central`
archetype, which avoids MD-8 (the node capacity quadratic applies only to `regional_node`); values
above 1.05 correctly incur `capacity_expansion_days`. No `cc_quality` group, because the two sites are
separate legal entities.

**Approximations.** (1) **The engine has no funder attribution on capital**, so cooperative equity is
charged to Telo. That inverts the architecture's defining commercial fact and must be corrected before
any cost ranking is quoted. Minimal fix: a per-site-plan `capital_funded_fraction`. (2)
`take_or_pay_fraction` is charged only on reserved lines, so a buyer-side volume commitment on an
owned site has no channel at all; combined with the absence of any revenue side, the commercial core
of this candidate lives entirely outside the simulation, in `contracting.contract_requirement`. (3)
`commissioning_days` is a site-plan field, not a design variable, so the transfer-lead assumption
cannot be swept. (4) `allocation_policy` `minimum_guarantee` would degrade to proportional, so
member-first allocation is unrepresentable; `proportional` is declared instead. (5) MD-17. (6) `cc_quality` is declared on both sites (added 2026-09-03). Separate legal entities is
not the question the group answers: this design's own regulatory owner brings the acquired site into
the same application by site-transfer supplement, so one holder's quality unit disposes both, which
21 CFR 211.22(a) makes non-delegable (F3-S41, F3-S42, F3-S43). `cc_stopper_1` and `cc_geo_R3` were
added under the same pass, which also removes the group-count asymmetry against S8 (the same two-site
R1/R3 shape had six groups in S8 and four in S14).

### S15 - Capacity-adequate buffer-payable presentation (inventory-first, no new plant)

*Family:* product_selection. *Candidate key:* `PS_B_capacity_adequate_buffer`. *Judge total 9.46,
keeps 3 of 3.*

**What it is.** No plant, no validation, no commissioning. Screen for a presentation whose existing
registered network is capacity-adequate, that is on the CMS 86-medicine essential list carrying the
separate IPPS buffer payment, and that is *not* currently on the FDA shortage list; then fix the tail
with positioned inventory under a daily base-stock regional review. It is the honest zero-capital
benchmark every capital-bearing design in the battery has to beat.

**Mechanisms addressed.** Inventory timing (the mode decisive in 8 of 16 Phase A cells), surge
headroom, capacity shortfall by refusing to select products where it binds, and partially common
cause and site downtime by covering outage days from stock. **Left binding:** capacity shortfall for
any product that fails gate 1 (no amount of stock fixes a mass-balance deficit), supplier
concentration, contract insufficiency (the CMS instrument funds the *buyer's* stock, not the maker's
readiness).

**Prior-art position.** Directly instantiates Phase A's own conclusion: capacity-adequate strategies
fail only the tail, and the regional review rule plus inventory level fixes the tail. The CMS
instrument is real and narrow (F12-S08, LSD-S3). The category is firmly occupied: Civica, Vizient NES
Reserve and Premier ProvideGx all hold six-month buffers, and the nonprofit landscape warns against
re-entering without a distinguishing mechanism (LNPM-S03, LNPM-S19).

**Novelty:** commercially_novel, and narrowly: the inventory operation is already_implemented; only
the CMS-buffer-payment-linked channel to small independent hospitals is unoccupied, and it is
unoccupied partly because it is small. *Withdrawn if:* any of Civica, Vizient or Premier is found
selling a buffer service into the CMS IPPS buffer-payment channel.

**Judge criticism carried forward.** The entire measured effect runs through MD-3 and MD-4 plus the
free-opening-inventory defect, so it is artifact-suspect under pruning rule P2 until the effect is
shown to survive the fixes. Its scoping run put p_meet 0.90 at n = 20, exactly on the requirement,
with a binomial standard error near 0.067, which is two runs from failing. *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)* The eligible buyer set
(hospitals of 100 beds or fewer, not part of a chain, drug not currently short) is tiny, and Vizient
already supplies the same operation with no programme fee (LNPM-S19). And **the engine has no
purchased-finished-goods price line**, so its headline cost is the incumbent's *production* cost
rather than Telo's cost of goods; a real transfer price could invert the comparison entirely.

**Engine representation.** One `central` site plan at `scale` 1.0 x `capacity_factor` 1.05, identical
to S0's topology and carried at full cost attribution so the comparison to S0 and S1 is like for
like. `safety_stock_days` 180 with `region_base_stock` 1; all four inventory variables searched. The
candidate's own profile named only G06 because Telo manufactures nothing here; the configured gate
mapping is the wider G01-G07, because the architecture is wholly dependent on the incumbent's
approved-CMO application, registration, validation and stability state, and mapping fewer gates would
make the strategy look less gated than it is.

**Approximations.** (1) No purchased-finished-goods cost line, as above; leaving the multipliers at
1.0 is the honest choice and means the cost numbers are S0's production cost. (2) Allocation policies
all collapse to proportional, so a committed-buyer-first allocation story cannot be tested. (3)
Expiry and rotation of a six-month hospital-held buffer is charged only through the product-level
`expiry_scrap_fraction`, so shelf life does not interact with buffer size and the screen's shelf-life
criterion cannot be tested. (4) Free opening inventory, which this design maximises.

### S16 - Reserve-triggered campaign network on contracted registered capacity

*Family:* inventory_capacity_hybrids. *Candidate key:* `f8_reserve_triggered_campaign`. *Judge total
9.35, keeps 2 of 3.*

**What it is.** Reserve depletion below a stated days-of-supply threshold triggers a pre-qualified
campaign at one of two contracted registered lines, each exercised twice a year, paid for by
take-or-pay rather than by a readiness fee.

**Mechanisms addressed.** Surge headroom, inventory timing, capacity shortfall partly (through
contracted rather than built capacity), contract insufficiency (the activation trigger, campaign
length and take-or-pay are the contract terms Phase A says S3 lacked), commissioning delay avoided.
**Left binding:** chronic capacity shortfall, which it does not close (its own scoping run reached
0.9729 mean fill with p_meet 0.00 on the capacity-short product at the best crude setting *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*), common
cause, supplier concentration, all three cost blocks, and G01/G02/G07, all UNCERTAIN.

**Prior-art position.** The failure mode it is built against is documented: GAO found the CIADM sites
underused, that a lack of regular manufacturing work prevented them developing the capability to
produce at scale, that one was terminated after cross-contamination, and that none met the surge goal
(F8-S09). It funds standby through committed volume, which Civica and ProvideGx demonstrably operate
(F8-S14, F8-S12, F10-S01), rather than through an availability payment nobody has been shown to pay
(F3-S28). The activation trigger is literally the engine's control law: `activation_threshold_days`
is compared against network days of supply in `simulation.step7_policies`.

**Novelty:** novel_combination. *Withdrawn if:* a GPO, nonprofit or government contract is found in
which reserve depletion below a stated threshold triggers a pre-qualified campaign at a named site
(F8 section 7, row 5).

**Judge criticism carried forward.** The distinguishing coupling is inert. The candidate ran the test
itself: setting `exercise_batches_per_year` from 2 to 0 moved norepinephrine mean fill 0.9960 to
0.9958 and left p_meet at 0.88, because `activation_failure_probability` is a constant unconnected to
the exercise cadence. Without a readiness-decay hazard the architecture cannot be distinguished from
frozen S3, and what is left once the readiness claim is removed is a take-or-pay contract on
registered capacity, which is family 3's candidate.

**Engine representation.** `central` 1.05 + two `cdmo_reserved` plans at `scale` 0.6, both
`exists_at_t0: false` with `commissioning_days` 540.0, `reserved: true`, exercise 2/yr, p_fail 0.10,
`reserved_site_owned: 0`, `take_or_pay_fraction` 0.5. 540 was chosen deliberately instead of the
365-day parameter base **because 365 equals `warm_up_days`** and would make the lead invisible
(MD-17); this is one of three candidates in the battery that dodged that boundary, and the judges
scored that as a methodological-honesty signal.

**Approximations.** (1) NEW-1, readiness decay is not modelled: a failed activation is re-requested
with the same lead, so raising p_fail changes almost nothing. Minimal fix: make the failure
probability a function of days since the last exercise or qualified campaign, and on failure apply a
requalification lead (three aseptic process simulations plus incubation) instead of repeating the same
activation lead. (2) A reserved line Telo does not own is charged zero validation (R004, MD-14), but
F7-S04 shows tech transfer, process and analytical development and lot release testing sit outside a
reservation fee and are the sponsor's cost, so the ledger understates this design. (3) No per-site
variable cost, so a CDMO price above Telo's own conversion cost cannot be expressed. (4) NEW-2,
allocation rights are inert.

### S17 - Rotating prequalified campaign network across three registered CMO fill lines

*Family:* warm_standby. *Candidate key:* `rotating_campaign_network`. *Judge total 9.31, keeps 2 of 3.*

**What it is.** Four sites, all registered and producing at t0: the incumbent plant plus three
contracted lines, each holding a 50 percent Telo capacity slice and each running four rotation
campaigns a year, so all three stay filed, exercised and current. Readiness is paid for with volume
that is actually sold.

**Mechanisms addressed.** Capacity shortfall (buys registered capacity instead of building it, so the
deficit closes on day 0), commissioning delay (zero), site failures, surge headroom, contract
insufficiency. **Left binding:** inventory timing, supplier concentration (all four sites draw api_1,
vial_1, stopper_1), common cause on `cc_quality` and `cc_os` which span all four sites by declaration,
the two cost blocks (this design pays *more*, not less), release time, and low utilization at the
reserved slices.

**Prior-art position.** Campaign rotation as a network scheduling policy for approved generic
injectables is one of the six unoccupied intervention points the prior-art review names (6.4;
F7 section 7). The competitive landscape independently names contract-linked assurance that reserved
capacity will pass inspection when called (4.1) and a contractible registry of activatable capacity
(4.2) as unoccupied, though ASPR's DS-MRN prize challenge is already funding the registry half
(LGOV-S17, LGOV-S51). The failure it answers is CIADM's: readiness was not funded and capability
decayed without regular work (F7-S01, LGOV-S11).

**Novelty:** novel_combination. *Withdrawn if:* any approved ANDA is found listing three or more US
sterile fill sites for one presentation with a maintained rotation schedule. That check needs Module
3.2.P.3 facility tables, which are not public.

**Judge criticism carried forward, and it changes the classification.** The candidate's own 2x2 shows
the mechanism is not readiness at all: holding cadence fixed and moving
`activation_failure_probability` from 0.10 to 0.35 changed mean fill by 0.0001 with p_meet unchanged,
while dropping exercise from 4/yr to 0 moved fill 0.997 to 0.985 and p_meet 1.00 to 0.50 *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*.
The entire warm-versus-cold gap is production volume. **On this engine the design is distributed
routine contracted supply wearing a standby label and must be reported that way**, unless the decay
hazard is built. The reclassification is provisional until the Phase D battery reruns it with a
manifest, but a registered paired run on the post-R007 configuration reproduces the direction: at
n = 25 on sodium bicarbonate, exercise 4/yr against 0 moves mean fill 0.99750 (MCSE 0.00084) to
0.98680 (MCSE 0.00279) and p_meet 0.92 to 0.48. The same ablation on S16 moves fill by +0.00163,
inside its own MCSE, because `exercise_due` is blocked while a campaign is banked and S16's lines are
activated often (MD-23). A second cost this design's profile did not carry: in a quiet world over a
2191-day horizon it runs 75 exercise batches on the capacity-adequate presentation and reports
`expiry_rate` 0.14901 against 0.0 for S0, so the rotation cadence is a scrap cost as well as a fee. At exercise 0 the reserve was called every 87 days, which is not standby by any reading.
Commercially, the priority call that makes the reservation worth anything is exactly what made
industry refuse BARDA capacity for fear of displacement (F7-S01, F3-S19), and the one disclosed US
CDMO capacity agreement runs the opposite way (LCDM-S14).

**Engine representation.** `central` at 1.05 plus `cmo_R2`, `cmo_R3`, `cmo_R4`, each
`cdmo_reserved`, `scale` 1.0, `exists_at_t0: true`, `reserved: true`, exercise 4/yr,
`activation_failure_probability` 0.10, `activation_lead_days` 30.0 (above the configuration base of
21 because a reservation fee buys the room and the crew, not a transferred process, F7-S04), and
`portfolio_capacity_share`/`portfolio_fixed_cost_share` 0.5. `cc_os` and `cc_quality` are declared on
all four sites because one Telo layer and one Telo quality unit span them.

**Approximations.** (1) NEW-1 again, and it is decisive here. (2) `exercise_batches_per_year` and
`activation_failure_probability` are `SitePlanSpec` constants and cannot be read from
`design_variables`, so the readiness cadence cannot enter any design space or optimizer run. (3) A
reserved site Telo does not own is charged zero validation, which is right for somebody else's
capital but wrong for Telo's own maintained transfer package. (4) `take_or_pay_fraction` is set to
0.10 rather than to the contractual commitment, because the engine charges take-or-pay as pure
additional cost and does not net it against rotation batches actually run and sold; setting it equal
to the commitment would double count. (5) The reservation fee is a fraction of a notional capital
base, while both public price points are absolute per-site-year figures (F7-S01; F7-S10, LGOV-S28).

### S18 - Dual committed supply with contract-mandated distinct API and container sources

*Family:* contracts_procurement. *Candidate key:* `dual_committed_supply_distinct_sources`. *Judge
total 9.27, keeps 3 of 3.*

**What it is.** Two registered partner lines under a single committed supply agreement whose *terms*,
not Telo's capital, buy the independence: the contract mandates that the second source runs a distinct
API source **and** a distinct container source, plus a supplier-held finished-goods buffer.

**Mechanisms addressed.** Supplier concentration, common cause on the API and container legs, contract
insufficiency, inventory timing (supplier-held finished goods and API reserve as contractual terms),
capacity shortfall partly. **Left binding:** commissioning (545 days), release time, `cc_geo_R1` and
the shared `stopper_1`, `cc_label_owner` across both sites, both cost blocks (this design increases
them), surge headroom (no reserved slot).

**Prior-art position.** This is the only clean container-independence test available, because frozen
S2's second source always shares `cc_vial_1` and the engine has therefore never had a strategy in
which the contract buys container-source independence. The instrument is documented, not invented: the
Senate Finance discussion draft requires a separately contracted secondary supplier with API and
component sources distinct from the primary's (F10-S11); HealthTrust SIMS already requires multiple
API sources or vertical integration plus geographically distinct redundant plants (F10-S08); the
supplier-held buffer is a term all three GPO programs run (F10-S05, F10-S07, F10-S08).

**Novelty:** novel_combination. *Withdrawn if:* an operating US contract is found that mandates
distinct container sources as well as distinct API sources for a generic injectable.

**Judge criticism carried forward.** Its distinctive lever attacks supplier concentration, which flips
only 3 of 16 Phase A cells, and the likely measured gain comes from the supplier-held buffer rather
than from source independence, in which case it is an inventory result in contract language. Worse,
**the outcome-based half of the contract has no representation at all**: there is no failure-to-supply
penalty channel in the engine, so the money that enforces the mandate is silently omitted while HHS
records that erosion of failure-to-supply clauses in GPO contracts may itself be associated with
shortages (F10-S10). Its declared `minimum_guarantee` allocation policy is inert. And the only
quantified failure-to-supply result available is conditional on a 30 percent price increase travelling
with it (F10-S33). Commercially the regime cuts against a new entrant: Duke-Margolis recommends a 75
percent ceiling on incentive-eligible committed volume specifically to keep part of the market
accessible to new entrants (F10-S45), and HDA argued the Senate Finance draft's volume requirements
may prevent new manufacturers from entering (F10-S36, recorded as unverified).

**Engine representation.** `central` at 1.05 (groups `cc_api_1`, `cc_vial_1`, `cc_geo_R1`,
`cc_label_owner`) plus `second_source` in R3 at `commissioning_days` 545.0 (api_2, vial_2, groups
`cc_api_2`, `cc_vial_2`, `cc_label_owner`). One declared extra supplier `vial_2`. 545 is inside the
declared `second_source_qualification_days` range and deliberately off 365 (MD-17). `stopper_1` stays
shared and is not claimed as independent, because the contract as drafted does not reach it.
`allocation_policy: minimum_guarantee` is declared to document the contract and is annotated in the
config as inert in the engine.

**Approximations.** (1) No failure-to-supply penalty channel. Minimal fix: a cost line in
`simulation.step8_costs` computed as unmet committed units times a penalty per unit, using the
backorder counters that already exist. (2) `SitePlanSpec.commissioning_days` is one literal per site,
so a second API source and a second container source cannot carry different qualification leads even
though they plainly do. (3) The cost of a second container-closure system enters only through the
site-wide `validation_factor` and `fixed_cost_factor`, both of which multiply everything at the site,
so a per-application comparative CCI, extractables-and-leachables, glass-durability and stability
programme is scaled rather than priced. (4) No per-component supplier capacity, so a container
supplier can be disrupted but never merely constrained. (5) NEW-2.

### S19 - Maintained alternate-source switching package with an exercised standby line

*Family:* upstream_first. *Candidate key:* `upstream_switching_package`. *Judge total 9.16, keeps 2 of
3.*

**What it is.** A maintained, regulator-pre-agreed switching package (a comparability protocol under
21 CFR 314.70(e), synonymous with an ICH Q12 PACMP) plus an exercised standby line at a second
registered site with an alternate qualified API source. Telo owns no plant and holds no application;
it prepares and maintains the package and the validation data behind it.

**Mechanisms addressed.** Supplier concentration, common-cause failure (the last binding mechanism in
exactly the two S2 cells), site failures, surge headroom at the tail, and commissioning avoided
entirely because both sites exist at t0. **Left binding:** chronic capacity shortfall (its own scratch
run reached 0.7993 fill with p_meet 0.00 on the capacity-short product *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*), sterility-related release
delay and every other release component, inventory timing unless the base-stock rule is kept on, both
cost blocks, and contract insufficiency, which is its weakest point.

**Prior-art position.** This is the only architecture in the batch that lands squarely on an
intervention point the cross-family prior-art review lists as *surviving*: 6.3, a maintained
regulator-pre-agreed switching package under 21 CFR 314.70(e) and ICH Q12 PACMP. The review also
bounds it honestly at about 30 days plus predictability rather than a step change, because FDA's own
carve-out caps the gain at CBE-30 rather than CBE-0 and conditions even that on the receiving site's
CGMP compliance state at implementation (F9-S37).

**Novelty:** novel_combination. *Withdrawn if:* a single published comparability protocol
pre-authorising an alternate aseptic site or API supplier for a generic sterile injectable is found.
FDA publishes no approved protocols, so this cannot be closed by search; it needs a regulatory
attorney or a Type C meeting.

**Judge criticism carried forward.** The whole architecture is one uncertain regulatory reading wide,
and that reading is prior-art open question 2. Its revenue is a readiness payment nobody has been
found paying, and family 7 instructs the review to assume the answer is no until a purchaser says
otherwise; five of nine `ContractTerms` fields are unanswered. If FDA will not pre-agree a location
change for an uninspected alternate site, the activation lead stays near 386 days and the design
delivers p_meet 0.80 on norepinephrine and 0.00 on sodium bicarbonate *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*. The
prediction is provisional until the Phase D battery reruns it with a manifest. The re-run with
`cc_quality` declared on both sites, added 2026-09-03, has been done: the three paired
`activation_lead_days` designs give fill 0.79513 (MCSE 0.00794) and p_meet 0.00 at 386 d, 0.83225
(MCSE 0.00784) and p_meet 0.00 at 201 d, and 0.97695 (MCSE 0.00566) and p_meet 0.44 at 51 d. The
switching package is worth nothing at the 180-day GDUFA III clock and something only at the CBE-30
lead an approved comparability protocol would buy (F9-S37), which is precisely the reading gate G07
leaves UNCERTAIN *(verification-pass paired run, sodium bicarbonate, master seed 20260901, n = 25,
horizon 2191 d after a 365 d warm-up, no manifest)*. One judge flagged it
explicitly as a strong technical candidate penalised on the missing payer alone.

**Engine representation.** `central` (R1, `scale` 1.0 x `capacity_factor` 1.05 = `STATUS_QUO_SCALE`,
so no expansion wait) plus `second_source` (R3, `cdmo_reserved`, `exists_at_t0: true`, `reserved:
true`, exercise 2/yr, `activation_failure_probability` 0.15, `activation_lead_days` **386.0** = the
365-day regulatory clock plus the 21-day reserved activation lead). Two declared extra suppliers
`api_src_a` and `api_src_b`, in distinct API groups and both in the shared `cc_ksm_api_1` with both
sites. `reserved_site_owned: 0`, `take_or_pay_fraction: 0.0`. **The base design deliberately assumes
NO approved comparability protocol**, because G07 is UNCERTAIN and the protocol forbids assuming
regulatory approval; the pre-agreed world is the labelled optimistic variant at 201 and 51 days, and
the difference between them is this strategy's entire value.

**Approximations.** (1) `activation_lead_days` and `activation_failure_probability` are
`SitePlanSpec` fields, not design variables, so the regulatory sweep and the reliability sweep run as
separate labelled designs rather than inside one search. (2) Exercise batches go to saleable finished
stock with no scrap or expiry path, so a batch made only to hold validation is counted as
revenue-grade output; that flatters the design and contradicts the documented refusal of
manufacturers to hold volumes they might not sell (F7-S07, F10-S25). (3) `strategies._group_kind`
has no key-starting-material kind; `cc_ksm_api_1` maps to `api_supplier` only by substring. (4) Each
group id draws its own Poisson stream at the same global rate, so adding an honest upstream tier adds
hazard as well as correlation; the matched-membership control is the only clean separation. (5) Gate
G16 covers API and component lot qualification (21 CFR 211.84, 211.94) and the Type II DMF letter of
authorisation the alternate API source must issue (F9-S12). It was added to
`config/regulatory_gates.yaml` on 2026-09-03 under revision R007 and applies to S9, S18 and S19; like
every other gate it is UNCERTAIN, so it changes no eligibility today, but the precondition is now
expressed rather than absent.
(6) The engine has no way to mark a site as third-party for cost purposes except zeroing the three
multipliers, so the reported cost is *network* cost rather than Telo's ledger.

## 4. Generated but not configured

Thirty candidates were generated and scored and are not configured. Two reasons dominate: the id
budget is thirteen and twelve were spent, and a candidate whose distinctive mechanism the engine
cannot measure separately from a known defect cannot be run honestly. Each entry below gives the
family, what it is, the mechanism it aimed at, the prior-art position by source id where the judging
record carries one, the judge tally, and the decision. **Rejection here is a decision about what to
configure now, not a claim that the architecture is wrong.** Several of these are more useful as
evidence items than as strategies, and that is said where it applies.

Where a candidate's declared novelty class was not carried into this configuration step, that is
stated rather than guessed. Where a judge stated it, it is given.

### 4.1 Just below the cut (8.0 to 9.3): configure these first if the id budget grows

**`os_only_replenishment_layer`** - OS-only. *Total 9.28, keeps 1.* A software replenishment layer
sold to hospital and regional stocking points: better review policy and order-up-to levels, no
manufacturing. **Rejected: P2 plus P5.** Its entire measured effect is the gap between two
replenishment conventions, one of which (MD-3, the frozen regional review rule) is a model artifact
the protocol never specifies and the optimizer never searched, decisive in 8 of 16 Phase A cells.
Pruning rule P2 rejects an architecture whose whole effect runs through a known defect unless the
effect survives the fix, and that has not been shown. Every adjacent standalone vendor was acquired
rather than scaled (LogicStream to QuVa, LSD-S15; Lumere to GHX, F2-S41; Trulla to SpendMend,
F2-S42), and Bluesight already fuses shortage prediction with the buyer's on-hand inventory (LSD-S14,
F2-S37). **But pursue its evidence item regardless:** what replenishment review policy and
order-up-to level real regional stocking points actually run is ranked first by decision value in the
Phase A synthesis and costs one conversation (HA-20, HA-24).

**`committed_volume_offtake`** - contracts_procurement. *Total 8.89, keeps 1.* Plain committed-volume
offtake with no source-topology mandate. **Rejected: P5, plus three engine misrepresentations.** It is
Civica, Vizient, Premier and HealthTrust with no stated reason Telo beats them, and the leader's
disclosed results are poor (48.2M USD FY2024 deficit; well under 10 percent of generic sterile
injectable sales; prices up to 2.15 times the traditional model for certain generics; members off
five-year terms in 2024). Decisively, none of the four contracts with a *pre-approval* manufacturer,
so the instrument that would de-risk building is unavailable in the sequence Telo needs it. In the
engine: `take_or_pay` is charged only inside the reserved-plan branch, so a minimum-volume commitment
on a routinely running line cannot be charged at all; there is no contract-compliance parameter, so
every run assumes 100 percent compliance against a measured 30 to 50 percent (F10-S09) and under 15
percent at one GPO (F10-S15), which is hidden tail risk the prohibitions forbid; and its declared
`minimum_guarantee` allocation policy is inert. **Its function is preserved in S18**, which is the
same instrument with the source-distinctness mandate that makes it measurable.
*Novelty as judged:* already_implemented.

**`anchor_tenancy_divertible_slots`** - multi_product_portfolio. *Total 8.8, keeps 1.* A single
anchor tenancy at one multi-product host, with an enforceable shortage-triggered right to divert slots
from the host's other tenants. **Rejected: the divertible right is the only unoccupied part and may
not be purchasable at any price.** The host must be paid to disappoint its other tenants, which is
exactly what industry refused at CIADM for fear of displacement (F7-S01), and what BARDA's own RFI
names as a deterrent (F3-S19). Every reservation instrument in the repository is either a government
contract (LCDM-S35) or a redacted innovator-CDMO agreement (LCDM-S34); no public US sterile
fill-finish rate card, minimum order value or reservation fee exists. Without the diversion right it
collapses to a plain tolling contract with no service mechanism. Its portfolio shares are
`SitePlanSpec` constants the optimizer cannot search. **S10 is its controlled comparison arm** and
carries the matched-capacity test that would have priced it.

**`acquired_regional_lines_separate_registrations`** - telo_architectures. *Total 8.69, keeps 1.*
Acquire several node-scale regional aseptic lines, each separately registered. **Rejected as an
architecture, retained as an experiment.** MD-15 fixes equal regional demand shares, so it cannot
answer its own governing question, whether the distributed thesis dies from distribution or from
construction; what remains measurable is shorter transit and site redundancy, both of which S8 already
supplies. The acquisition target set for registered node-scale US aseptic lines may be empty, and
buying a non-aseptic shell reverts to the build clock (L503B-S21). **Two judges asked for it as the
paired ablation arm of S8**, and a clean negative there would be a publishable refutation of the
original pitch; it is the first candidate to add if S20 is spent.

**`hub_quality_registered_spokes`** - hub_and_spoke. *Total 8.61, keeps 1.* A central quality unit and
central laboratory releasing product made at several registered third-party spokes under Telo's label.
**Rejected: the central claim is a cost claim and the cost claim is unmeasurable.** Pooling a quality
unit is inherently a portfolio argument and MD-15 runs one product per network, so
`portfolio_fixed_cost_share` is an accounting proxy rather than a simulation of the claim. Every
component is already implemented (central labs, contract labs, owner quality-unit release over
contract sites, Civica label-over-partner-ANDA), and the candidate concedes its moat is prior-art 6.3
in a different wrapper, worth about 30 days plus predictability (F9-S37). Landscape open question 3,
whether any US CDMO currently makes a shortage-list drug under a third party's ANDA, is unanswered,
and a no makes the spokes unavailable at any price. **One judge called it the highest-value non-kept
candidate on his lens**, because it tests the shared-quality-unit question (Phase A ranked human
evidence item 4) without needing the DME rule.

**`os_only_noncorrelating_layer`** - OS-only. *Total 8.09, keeps 1.* A cross-site software and data
layer deliberately built *not* to standardise, so it does not create a shared failure mode.
**Rejected: the service claim is worth 0.0001 fill unless the customer network runs with no capacity
headroom.** Its own smoke run moved fill by 0.0001 at capacity slack, inside MCSE *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*, and the magnitude
is set by `common_cause_events_per_year`, whose declared range 0.02 to 0.3 spans the point where the
mechanism stops mattering. Phase A resolves deviation and rejection in 9 of 16 cells with 0 flips and
the note "unchanged; it was never the constraint". The prior-art review puts the manufacturing OS in
all eight sub-forms on the does-not-survive list, and the argument offered against that is narrow and
self-declared as an absence in its own search rather than a checked vacancy. The buyer it needs is a
multi-site, capacity-tight operator willing to pay for the discipline of *not* standardising, which is
the inverse of what every documented buyer of a multi-site MES is purchasing.

**`PS_A_portfolio_family`** - product_selection. *Total 8.0, keeps 1.* Build two Telo lines and run a
family of five related presentations across them to spread the fixed quality block. **Rejected: it
builds rather than buys**, so both lines wait `node_commissioning_days` of 730, which is the exact
structural gate Phase A names, and it reintroduces the architecture the prior-art review lists as not
surviving. The 1/N shares that carry the entire cost case are constants the optimizer cannot search,
and the engine charges no changeover, cleaning validation, media fill or campaign scheduling cost
against them. Under MD-15 the other four presentations are pure accounting, so a site event that
would remove five presentations at once is modelled as removing one. Shared quality staff and shared
equipment are already implemented two to three orders of magnitude above this scale (F6-S26, F6-S28).

### 4.2 Mid band (6.5 to 8.0): mechanism unmeasurable, occupied, or dominated

**`common_format_dual_container_pool`** - postponement. *Total 7.74, keeps 0.* Qualify two container
systems and pool inventory across them. **Rejected:** the engine has no cost object for a
container-closure qualification programme, so a second qualified system reads as free when it is a
per-application comparative CCI, extractables and leachables, glass durability and full stability
programme (F5-S41). It is therefore likely dominated by simply holding more containers, since
`material_target_days` is a free dial and a second qualification is not. The mechanism it attacks
flips 3 of 16 Phase A cells. P5 with no stated reason Telo beats anyone.

**`f8_pooled_national_reserve`** - inventory_capacity_hybrids. *Total 7.71, keeps 0.* A single pooled
national reserve rather than regional stock. **Rejected under P2, and it earned its rejection by
finding a defect nobody else had.** Its measured advantage is produced by that defect: at its
settings it starts with 657,084 free units (200 days of national demand) against 295,687 (90 days)
for its siblings, a difference of 361,397 units and about 434,000 USD of unbilled variable cost.
Verified in source: `simulation._seed_initial_inventory` seeds `site_fg_days` and `safety_stock_days`
of stock and increments `counters.initial_units` without ever charging `variable_production`. The
category is also firmly occupied (F8-S10, F8-S11, F8-S12, F8-S14, F8-S32). **The finding is escalated
in section 5 and is the single most important thing this sweep produced about the model itself.**

**`upstream_material_reserve`** - upstream_first. *Total 7.53, keeps 0.* Deep API and component
reserves as the primary intervention. **Rejected: two engine biases both run in its favour**, which
makes a positive result unusable. MD-1 makes the material order-up-to level and reorder point
`(target_days + lead) x daily demand`, so `material_target_days`, the one lever it exists to test,
does not measure material policy; and component stock has no shelf life and is never scrapped, so the
engine cannot charge the obsolescence that emptied the federal Strategic API Reserve after five years
and about USD 700 million (LGOV-S20), terminated every SNS vendor-managed-inventory contract in 2017
as not cost-effective (F8-S03), and made Warstopper manufacturers decline to expand because they
could not sell the volume before expiry (F7-S07, F10-S25). No revenue mechanism and no payer, in a
category two GPOs already sell to the same buyers.

**`cold_prefiled_switch_plus_inventory`** - warm_standby. *Total 7.34, keeps 0.* A cold pre-filed
alternate line plus inventory. **Rejected: it already failed its own falsification test.** Deleting
the reserved line changed fill 1.0000 to 0.9994 with p_meet 1.00 in both arms on the capacity-adequate
product, so the option cost 0.83 USD per delivered unit and bought nothing; on the capacity-short
product it reached p_meet 0.00 either way. Dominated by pure inventory in both directions. The engine
also applies no requalification penalty on a failed activation, which understates cold readiness
specifically, so even that null is generous to the design. **One judge asked to keep it as the
inventory-versus-readiness control**, which is a job S15 now does more cheaply.

**`hub_release_rotated_reserve`** - hub_and_spoke. *Total 7.13, keeps 0.* Central release oversight
plus a rotated reserve. **Rejected: no payer for readiness exists anywhere in the evidence base**, and
both historical instruments that funded it ended with the sites leaving the business: GAO records
CIADM sites at 0, 0 and 7 percent utilization, unable to produce reliably when called (F7-S01,
LGOV-S11); Emergent held a USD 542,750,000 Task 1 capacity reservation (F7-S04, LCDM-S35) and still
exited the CDMO business, selling four commercial aseptic lines for about USD 30 million (LCDM-S10).
The engine also credits exercise batches with saleable output, which is right for campaign rotation
and wrong for a media fill, so the warm-standby variant is overvalued.

**`payer_owned_material_reserve`** - public_private. *Total 6.94, keeps 0.* A public payer owns the
material reserve and Telo holds it. **Rejected on three compounding grounds.** Telo cannot be the
offeror in the only channel that pays for this (2 CFR 25.200 requires SAM registration before
application; BioMaP RPPs require Manufacturing Readiness Level 6 with mandatory cost share, LGOV-S23,
R-S1, R-S2, against Telo's MRL 1 to 2). The incumbent contract is sole-source and long-dated. The
mechanism is already implemented by DLA for three decades and now by CMS with third-party holding
permitted, and GAO found the DLA program has no clearly defined outcome-oriented goals or effective
performance measures after three decades. And the engine charges the material carrying cost to Telo
for every unit, so the one item the public buyer is supposed to fund lands on the wrong ledger.

**`public_reserve_rotation`** - public_private. *Total 6.91, keeps 0.* Rotate a publicly funded
reserve through Telo's network. **Rejected:** no payer for civilian generic sterile readiness has been
found anywhere; every federal program in the landscape funds capital and none funds operations; DLA
concluded expanding its access-based program needed no new authority and then did not do it
(LGOV-S07); federal money is already committed sole-source and long-dated to the same architecture
(Phlow to a potential 2030 with roughly USD 697M obligated, LGOV-S18); CIADM is down to one remaining
partner (F13-S35). Telo cannot enter the channel today (F13-S32, R-S1, R-S2), and no gate expresses
that. The engine has no funder entity, so a design whose defining feature is that someone else pays is
costed entirely on Telo's ledger.

**`shared_multiproduct_standby_slice`** - warm_standby. *Total 6.80, keeps 0.* Several sponsors
co-tenant one standby slice. **Rejected: the central claim is unfalsifiable in the current engine.**
The cost mechanism rests entirely on a portfolio the engine cannot represent (MD-15, one product per
network), so `portfolio_capacity_share` and `portfolio_fixed_cost_share` are inputs and the
cross-product demand correlation that decides whether co-tenants can share a line during a shortage is
simply absent. The co-tenancy is also precisely the arrangement GAO records industry refusing at CIADM
for fear of displacement (F7-S01). It reached p_meet 0.00 on the capacity-short product.

**`two_part_capacity_option`** - contracts_procurement. *Total 6.68, keeps 0.* A reservation fee plus
an execution fee, the standard two-part capacity tariff. **Rejected under P4 with affirmative negative
evidence, not merely absent evidence.** Emergent held a USD 542,750,000 federal Task 1 capacity
reservation at its CIADM site (F7-S04) and separately exited the merchant CDMO business, selling
Camden's four commercial aseptic fill lines for about USD 30 million (LCDM-S10). The reserved asset
and the sold lines are different sites: Emergent's CIADM site was Baltimore-Bayview, a drug substance
facility, while Camden was the separate merchant fill-finish site (LCDM-S30, LCDM-S10). That weakens
the inference from a direct observation about one asset to a company-level one, that reservation
revenue did not sustain the merchant fill-finish business. An earlier version of this sentence placed
the reservation over Camden and Rockville and cited LCDM-S35, which is an in-repo pointer row
carrying no quote rather than the primary source; both are corrected here and in
`landscape/cdmos.md`. DLA records manufacturer
reluctance to hold volumes they may not sell (F10-S25); FDA's own root cause states most generic
manufacturers cannot afford redundant capacity (F7-S16). Six of nine `ContractTerms` fields are
unanswerable. The engine's reservation fee is also mis-specified against the instrument, being a
fraction of annualized cost rather than the reservation-plus-execution tariff the literature
specifies (F10-S32).

**`owned_portfolio_node_network`** - telo_architectures. *Total 6.62, keeps 0.* Four owned
distributed nodes running a product portfolio. **Rejected:** owned distributed microplants are on the
prior-art review's does-not-survive list and this candidate does not argue against that evidence, it
accepts it. All four nodes pay `node_commissioning_days` of 730, which Phase A puts at 19.99 percent
of the measured window at the base value (pre-R004 Phase A ablation `abl_20260902_phaseA`; superseded by R004, re-run required), and Civica needed more than 1,600 days from construction
start to a plant still pending approval *with* pre-committed demand (F13-S41, F13-S27, F13-S28). Its
own smoke run put it last of its three siblings on both axes (0.8863 fill at 18.69 USD/unit) *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*. Shared
quality staff, shared equipment and campaign scheduling are already implemented two to three orders
of magnitude above this scale (F6-S26, F6-S28).

**`os_only_activation_layer`** - OS-only. *Total 6.57, keeps 0.* Software that coordinates activation
and allocation of third-party capacity during a shortage. **Rejected under P6: the product is an
allocation right and the engine cannot represent one.** Verified in source: `strategies.py` hard-sets
`criticality_weight` to 1.0 for every region and `simulation.py` calls `allocate()` with criticality
only, never a `minimum_guarantee`, so all four allocation policies collapse to proportional.
Commercially P4 also bars it: no US purchaser has ever been found paying a standing reservation fee
for sterile generic capacity. Its own smoke run was measured at capacity slack, where a reserve is
rarely the binding path *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)*. **This is the highest-leverage engine fix in the whole set**, because
allocation is the central power in every family-3 and family-13 precedent (F3-S10, F3-S1, F3-S23).

### 4.3 Terminal sterilization and route selection (6.0 to 6.5): highest novelty, lowest measurability

The prior-art review calls process-route conversion (6.1) the only intervention found anywhere in the
fourteen families that removes the binding release constraint rather than compressing something that
is not binding, and names release-component decomposition as a selection screen (6.2) alongside it.
None of the three candidates on that line was configured, and the reason is a live contradiction the
orchestrator should resolve before weighting novelty: **Phase A measures release as not binding.** The
whole chemical release queue is worth at most +0.002114 fill anywhere, removing sterility entirely
bought +0.0076 at norepinephrine S7, and sterility delay flips only 4 of 16 cells with small
consequence. The reconciliation is that 6.1's "binding release constraint" means the 14-day sterility
hold, which Phase A measures as small. Any judgement that weights 6.1 heavily is importing a claim the
model's own ablation does not support. The cheap half of the line is the screen (6.2), which costs an
analysis rather than a company; the expensive half is per-product reformulation whose highest-value
input, the sterilization route per marketed presentation, is prior-art open question 11 and was not
obtainable from any US or EU label.

**`ts_route_conversion_dual`** - terminal_sterilization_release. *Total 6.47, keeps 0.* Convert an
aseptically processed presentation to a terminally sterilized route and take parametric release.
**Rejected:** the route is already falsified for one of the two modelled products. Autoclaving sodium
bicarbonate injection at 121 C produced needle-like sodium dawsonite crystals from aluminium leached
out of the glass (F11-S31). What remains is a cost advantage entered as search bounds on
`validation_factor` and `fixed_cost_factor` rather than as evidence, and pinning them at the frozen S2
values collapses the design into S2 plus two correlated-failure groups, which is strictly worse than
S2. All nine `ContractTerms` fields unanswered.

**`ts_route_split_hedge`** - terminal_sterilization_release. *Total 6.45, keeps 0.* Run the same
product by two different sterilization routes to hedge a route-level failure. **Rejected: the
mechanism is an inference with no documented event.** Family 11 section 8.4 states outright that a
shared autoclave, sterility suite or validated method version would be a common-cause coupling and
that nothing read documents such an event. Family 11 cites no LCDM source at all, so the supporting
evidence this review adds (LCDM-S7, FDA telling Jubilant HollisterStier that deficient aseptic process
simulations had been cited at two earlier inspections; LCDM-S2, the Catalent Indiana warning letter;
and the 503B aseptic enforcement surface) is circumstantial and never a measured route-level rate.
The ids were previously written zero-padded (the `landscape/cdmos.md` ids are unpadded, LCDM-S1
through LCDM-S37), so both matched nothing; corrected 2026-09-03. The engine applies one global `common_cause_events_per_year` to every group kind, so
declaring two route groups where S2 declares one raises total exposure, and the independence gain and
the added hazard cannot be separated without a matched control the design does not specify.

**`PS_C_route_screened`** - product_selection. *Total 6.06, keeps 0.* Select products by their release
component vector and prefer terminally sterilizable ones. **Rejected under P6: as written it cannot
test its own claim, and the candidate says so.** `build_strategy` assembles all five release components
from globals, so they are network-wide and a mixed aseptic/terminal network is inexpressible;
`sterility_incubation_days` has low = base = 14, so no sensitivity can move it; and
`release_assurance.NEVER_REDUCIBLE` blocks it by design. What runs today is the topology, which is S2.
Underneath that, the screen's first criterion is prior-art open question 11 and is not obtainable from
any US or EU label. **The cheap half is worth doing anyway as an analysis, not as a strategy:** a
modest engine investment (an optional `release_components_days` override on `SitePlanSpec` or
`StrategyDesign`, two new tier-5 globals, and a new UNCERTAIN gate for a parametric release programme
with treatment `fallback_conventional`) would move family 11 from unrepresentable to testable.

### 4.4 Rejected on a binding mechanism the engine cannot see, or on an instrument that does not exist

**`f8_upstream_reserve_independent_source`** - inventory_capacity_hybrids. *Total 6.37, keeps 0.* An
API reserve plus an independent API source. **Rejected:** prior art puts standalone upstream
diversification on the does-not-survive list as orthogonal to both dominant documented shortage
causes, and the mechanism is already contracted by ProvideGx and mandated in two EU states, so P5
fails. MD-1 is unfixed, so `material_target_days` measures buffer depth rather than lead-time policy
and `api_lead_time` and `component_lead_time` carry the wrong sign in 13 and 14 of 16 cells. It
changes no mass balance, leaves `cc_vial_1` spanning the network, and its measured sodium fill was
identical to its shared-API sibling.

**`dme_consolidated_acquired_network`** - telo_architectures / distributed. *Total 6.18, keeps 0.*
Acquire several lines and register them as one distributed manufacturing establishment under the
proposed DME rule. **Rejected: the enabling instrument does not exist and may never cover this
product class.** The proposed rule's text (FDA-2025-N-6075) contains no occurrence of "sterile",
"aseptic", "503B", "outsourcing facilit" or "real-time release" (F1-S01), so the architecture's only
advantage rests on assumed regulatory availability in a scope the rule may not cover, which the
prohibitions forbid. G14's `no_fleet_claim` treatment blocks the economic claim while UNCERTAIN. One
registration is also one point of regulatory action reaching every unit, which the engine can only
model at the global common-cause rate rather than at the impact 1.0 family 1 asks for, so it
understates its own central risk. As configured with both cost factors pinned at 1.0 it was dominated
by its own separate-registration twin.

**`vn_reserved_campaign_rotation`** - virtual_network. *Total 6.08, keeps 0.* Reserved capacity plus
campaign rotation across the virtual network. **Rejected under P4 with a quantified gap rather than an
absence:** the engine's own fee arithmetic puts readiness at roughly 3.8 USD per reserved unit-year
against a 1.20 USD variable cost and a reference vial price near 1.47 USD, and no US purchaser has
ever been found paying one (F3-S28). Its central claim is separately unmeasurable, because
`activation_failure_probability` is a constant with no link to exercise cadence, so the mechanism GAO
identifies as the cause of CIADM's failure (F3-S7, F3-S8) cannot be expressed. Its 30-run scoping
behaviour showed the reserved lines activating about 15 times in five years, which is intermittent
contracted supply wearing an option's clothes. **S17 carries the same idea with the honest
reclassification stated.**

**`hub_bulk_fill_spokes`** - hub_and_spoke. *Total 5.31, keeps 0.* Central formulation and sterile
filtration, regional fill-finish from held bulk. **Rejected on two independent kills.** Regulatorily,
its 2-day hub-to-spoke lead is already past the EMA 24-hour prolonged-storage threshold for
sterile-filtered aqueous bulk, no US example of the arrangement was found anywhere in fourteen
families, and no gate in `config/regulatory_gates.yaml` covers it. In the engine, material stock has
no shelf life or hold limit, so a spoke will hold roughly 62 days of formulated sterile bulk, which is
physically impossible; the candidate names this itself and concedes its service numbers mean nothing
until it is closed. Fails P3, P6 and prior-art open questions 3 and 4 simultaneously.

**`multi_holder_pool_allocation_call`** - postponement. *Total 5.04, keeps 0.* Several ANDA holders
pool unlabeled units and draw on the pool during a shortage. **Rejected: it probably fails on law
before economics.** No source establishes that one holder may draw finished unlabeled units filled
against another holder's application, and the closest analogue states legislation may be needed
(F5-S33). Reciprocal allocation among competing holders is a Sherman Act question first (F2-S63,
F2-S64), which is intervention point 6.6's stated barrier. It fails P10 and P4 at once with no path to
resolving either inside this project, and MD-15 makes the pooling benefit across NDCs, its entire
rationale, invisible to the engine. The design also has almost no physical redundancy: one line, one
quality unit, one API, one container.

**`leased_exercised_standby`** - mobile_modular. *Total 4.90, keeps 0.* Lease rather than own a warm
standby line, and exercise it. **Rejected:** warm standby as an owned asset is on the prior-art
does-not-survive list, and leasing changes the ledger rather than the demand side, where the evidence
is missing. No purchaser has been found paying a standing reservation fee, and the one operator who
ran a mobile-unit fleet as a business reached going-concern doubt after the lessee declined to lease
any units back. Its own falsification test predicts it loses to inventory before the mobility question
is even reached; family 14 section 8 states that mobility competes with shipping inventory rather than
with building a plant, with a move-plus-requalify cycle longer than `emergency_transport_days` by
construction.

**`modular_host_insertion`** - mobile_modular. *Total 4.82, keeps 0.* Insert a prefabricated modular
cleanroom unit into an existing host facility. **Rejected: the physical premise is unverified for the
one modality that matters.** Family 14 section 7 row 1 records that no fetched source shows a
prefabricated POD or trailer that has hosted an FDA-inspected sterile fill-finish line; every
documented POD deployment is oral solid dose, biologics drug substance or plasmid. The 420-day
commissioning figure is the entire claim and has no source, and `commissioning_days` is a
`SitePlanSpec` constant rather than a design variable, so it cannot be searched or swept. Nine of nine
`ContractTerms` fields unanswered.

**`ts_503b_dating_responder`** - terminal_sterilization_release / 503B. *Total 4.55, keeps 0.* A 503B
responder whose beyond-use dating is the lever, with an approved-CMO plant as the durable core.
**Rejected: verified inert on three independent counts.** `strategies.py` sets `bud_503b_days` from
`glob.base("bud_503b_days")` and the design variable is never read, so the design does nothing as
written (confirmed at runtime: still 90.0 with 14.0 declared). Even after the one-line fix it measures
nothing, because the global base of 90 days already exceeds every Table D cell, so the constraint is
slack. And Table D is an enforcement default for aggregate batch sizes of 1,000 units or fewer against
a modelled batch of 25,000 to 30,000, so the schedule does not govern the modelled facility at all.
Its structure was clean on the prohibitions (`durable = false`, approved-CMO plant as the durable
core), which the `StrategyDesign` validator enforces.

**`dme_modular_fleet`** - mobile_modular / distributed. *Total 3.30, keeps 0.* A fleet of modular
units registered as one distributed establishment, claiming pooled validation and a shared quality
unit. **Rejected, lowest-scored candidate in the sweep.** While G14 is UNCERTAIN its treatment is
`no_fleet_claim`, so the pooled-validation and shared-quality-unit savings that are its entire
economic case may not be claimed at all, leaving frozen S5 plus one extra common-cause group at
`validation_factor` 2.5 and `fixed_cost_factor` 1.4. The enabling registration instrument is a
proposal that may not be finalised, 21 CFR 207.1 still defines an establishment as one management at
one physical location, and even if final it is a *registration* rule that does not set the validation
evidence standard, so the pooled-validation saving may never materialise.

### 4.5 One deliberate omission, recorded so it is not mistaken for an oversight

Of the six unoccupied intervention points the prior-art review lists as surviving, **6.5, a hub
laboratory serving several 503B outsourcing facilities, has no candidate anywhere in the 42.** The
review itself bounds its value, because two named large operators already run rapid sterility on site
(F4-S11, F4-S14), so the omission may be correct. It is recorded here as a deliberate exclusion rather
than a gap in the sweep.

## 5. Engine gaps this sweep surfaced

Three are new and are not in the MD register in `bottleneck_decomposition.md` section 7. They are
listed first because they bias results already in hand.

**NEW-1. Opening inventory is free, and it scales with the strategy's own stock policy.**
`simulation._seed_initial_inventory` seeds `site_fg_days` and `safety_stock_days` worth of stock into
the mass balance and into `counters.initial_units` but never into `variable_production`, so a strategy
is endowed with product in proportion to how deep its own inventory policy is, at zero production
cost. Measured on sodium bicarbonate by `f8_pooled_national_reserve`: 657,084 units (200 days of
national demand) for the deep-stock design against 295,687 units (90 days) for its siblings, a
difference of 361,397 units and about 434,000 USD of unbilled variable cost, which can account for a
whole fill gap over a short window. It biases **every** inventory-led comparison in the battery toward
the deeper policy, including S13 and S15 which are configured, and it compounds MD-4, which R004
already fixed and which invalidated every pre-2026-09-03 safety-stock conclusion. *Minimal fix:*
charge `initial_units` at `variable_materials` plus `variable_conversion` on day 0. **Fix this before
ranking any inventory-led architecture.**

**NEW-2. Allocation rights are inert everywhere.** `strategies.build_strategy` hard-sets
`RegionPolicy.criticality_weight` to 1.0 for every region, and `simulation` calls
`allocation.allocate()` with criticality only, never a `minimum_guarantee`, although `allocation.py`
accepts one. All four `allocation_policy` values therefore collapse to proportional. This silently
voids the declared allocation policy of S18 (annotated in the config), removes the entire product of
`os_only_activation_layer`, and touches the allocation claims of nine other candidates. It is the
single highest-leverage fix across the set, because allocation is the central power in every family-3
and family-13 precedent (BARDA holding final determination of capacity use, F3-S10; the Commission
activating EU FAB, F3-S1; Civica allocating to members, F3-S23). *Minimal fix:* plumb per-region
minima and criticality from `StrategyDesign` into `RegionPolicy` and into the `allocate()` call.

**NEW-3. There is no readiness-decay hazard.** `activation_failure_probability` is a per-plan constant
with no link to `exercise_batches_per_year`, so campaign rotation, warm standby and every option
design cannot demonstrate the mechanism they exist for. Three candidates ran the test themselves and
all three got the same answer: `rotating_campaign_network` moved fill by 0.0001 across
`activation_failure_probability` 0.10 to 0.35 while removing exercise batches moved it 0.997 to 0.985;
`f8_reserve_triggered_campaign` moved p_meet 0.88 to 0.88 with exercise cadence at 0 against 2 per
year; `cold_prefiled_switch_plus_inventory` suffered 25 activation failures against 56 activations at
almost no cost. *(unregistered scoping run, no manifest, pre-R004/R005; model behaviour, not a result; see section 7)* A second reason the cadence half of the test is weak was
found on 2026-09-03: `exercise_due` requires `active_until_batches <= 0`, so on a line that is
activated often a campaign batch substitutes for an exercise batch one for one, and the cadence is
measurable only on a rarely activated line (MD-23). Until that hazard exists, **every "rotation buys readiness" claim in this batch is
measuring production volume**, and the honest reclassification is that S17 is a virtual-network
contracted-supply architecture rather than a standby one. *Minimal fix:* make the failure probability
a function of days since the last exercise or qualified campaign, and on failure apply a
requalification lead rather than repeating the same activation lead.

Existing register entries that bind hardest on this configuration: **MD-17** (four commissioning-family
parameters and `warm_up_days` all at 365, so six designs open on the first measured day at at least
one site and lose 0 percent of the window: S8, S9, S10 at both hosts, S12 at `second_source`, S13 at
`second_source`, and S14; S16, S17, S18, S11, S19 and S12's `cdmo_r2` avoid it), **MD-15** (one product per
network, so no portfolio effect is simulated and the cost case of every tenancy and pooling design is
an accounting proxy), **MD-3** (the frozen regional review rule, decisive in 8 of 16 cells; seven of
the twelve configured designs opt out via `region_base_stock`, so any comparison against S0-S7 must
either give them the same rule or report the gap), and **MD-1** (material order-up-to still coupled to
the lead time).

Structural gaps with no register entry yet, each named by the candidate that hit it: no per-site
ownership boolean independent of the `reserved` flag (S12 measured a 28 percent annual-cost spread
from that convention alone, with bit-identical service); no CDMO margin or per-site variable cost, so
contracted manufacturing is charged at Telo's own conversion cost; `take_or_pay` reachable only inside
the reserved branch, so a buyer-side commitment on a routinely running line cannot be charged; no
failure-to-supply penalty channel, so the enforcement half of every committed contract is unmodelled;
no funder attribution on capital, so cooperative or public equity is charged to Telo (S14); no
purchased-finished-goods price line, so a strategy that owns no plant is costed at the incumbent's
production cost (S15); no shelf life, retest period or hold limit on material stock, so upstream
reserves are free of the obsolescence that emptied every real one, and a hub-and-spoke spoke can hold
62 days of sterile bulk; per-site `commissioning_days`, `activation_lead_days`,
`exercise_batches_per_year`, `activation_failure_probability` and the portfolio shares are all config
constants that no design variable can reach, so several architectures' central latency and readiness
claims cannot be searched or swept; `CommonCauseGroup.kind` cannot express a key-starting-material
tier, a regulatory-action group or a utility; and every group id draws its own Poisson stream at one
global rate, so adding an honest correlation also adds hazard.

### 5.1 Common-cause declaration conventions, settled 2026-09-03

Because every declared group id draws its own Poisson stream at one global rate, group count is not
neutral, and two structurally identical designs given different group counts for a configuration
reason are not comparable. Phase D pairs exactly such designs. Three conventions were therefore
settled and applied to all twelve configurations; each is stated in the engine-limitations header of
`config/strategies/design_space.yaml` as NEW-4.

**`cc_stopper_1` on every site.** Every site of every design draws `stopper_1`, and no design declared
any container-closure group, so all twelve tails were optimistic by exactly one shared-supplier
hazard. Four designs said so in prose (S10, S11, S12, S18) and none corrected it. It bit hardest on
S18, whose entire declared contribution is a clean test of contract-mandated container independence
run with the stopper leg shared and unmodelled: its falsification test, "re-run with `second_source`
moved back onto `vial_1`", is not interpretable until the stopper leg is represented. The group is now
declared on every site plan. The frozen builder gives the `stopper_1` *supplier* no group, so this is
the site-side representation only and S0-S7 do not carry it. That asymmetry is handled the way the
package already handles the MD-3 review rule: the comparison to S0-S7 must either give them the same
group or report the gap, and one labelled matched-membership control (same group count, split
membership) must be run to separate the added Poisson hazard from the added correlation. That control
has been run for S18 first, because its falsification test was uninterpretable while the stopper leg
was absent: with `cc_stopper_1` shared across both sites, fill is 0.98711 (MCSE 0.00289) and p_meet
0.52; with the same group count and split membership it is 0.98721 (MCSE 0.00288) and p_meet 0.52, a
difference of -0.00009, inside MCSE. At the frozen hazard rate the container-closure correlation is
now represented but is not load-bearing *(verification-pass paired run, sodium bicarbonate, master
seed 20260901, n = 25, horizon 2191 d after a 365 d warm-up, no manifest)*.

**`cc_geo_<region_id>` on every site, in the region the site sits in.** This is what R005 already does
for a second node in a region and what the frozen builder does for `central`. It was previously
declared on some sites and not others, which gave structurally identical designs different exposure:
S8 (central R1, second_source R3) carried six groups while S14, the same two-site R1/R3 shape, carried
four, and S17 declared four geography groups across four sites while S16 declared one across three.
Every profile now carries the convention. Residual gap against the frozen set: wave-0 regional nodes
in S5/S6 still carry no geography group, so an S5/S6 comparison still has to equalise or report.

**`cc_quality` wherever one quality unit disposes batches from more than one site.** Batch disposition
is non-delegable under 21 CFR 211.22(a), 21 CFR 200.10(b) treats an extramural facility as an
extension of the manufacturer, and FDA's quality-agreements guidance states that a quality agreement
cannot delegate CGMP responsibility (F3-S42, F3-S43, F3-S41). Five designs omitted the group on a
separate-legal-entities or own-registration rationale while their own regulatory-owner field placed
every site under one application: S9, S10, S11, S14 and S19. All five now declare it and state the
reasoning in `profile.quality_owner`. S15 (one site) and S18 (two partners, two ANDAs, two holders)
are the only designs without it, and S18 now says why. `cc_os` is unchanged: declared only where one
shared software or model version spans the sites, which is S17 alone, with S12, S13 and S16 stating
explicitly why they do not.

Every pre-2026-09-03 run of these twelve designs is superseded by this pass as well as by R004, R005
and R007, because the group counts changed.

## 6. Gate mapping and protocol revision

Protocol revision **R006** (2026-09-03) records this configuration. Two deviations from the
instruction that produced it are recorded there rather than silently: the revision is numbered R006
because R004 and R005 already existed, and it carries 2026-09-03, the day the work was done and the
same date those rows carry.

`config/regulatory_gates.yaml` now names every configured id, so `regulatory.evaluate_strategy`
returns NO_CONCLUSION by analysis rather than by omission:

| gates | added | rule |
|---|---|---|
| G01-G07 | S8-S19 (all twelve) | every design-space site is an owned or contracted approved-CMO site |
| G13, G14 | S8-S14, S16-S19 (eleven) | they replicate manufacture of one product across two or more sites; S15 declares one incumbent line and is excluded |
| G08-G12 | none | no configured design uses a 503B responder site |
| G15 | none | every configured design runs release scenario R0 with the frozen release-component vector and claims no release-assurance component; G15 stays mapped to S6 alone |
| G16 (added later, under R007) | S9, S18, S19 | these three declare a second API or container source, so component and container-closure lot qualification under 21 CFR 211.84 and 211.94 and a Type II DMF letter of authorisation from the alternate API source both apply; treatment `lead_time`, status UNCERTAIN. The gate set is therefore sixteen, G01 to G16, not fifteen |

Every added row keeps `status: UNCERTAIN` with no reviewer and no review date, exactly as S0-S7 do.
Adding a gate to a strategy can only make it less eligible, never more, so no strategy gains
eligibility from this change. After it, `regulatory.evaluate_all` returns NO_CONCLUSION for every id
in `StrategyId`; `gates_mapped` is true for S0 through S19 and false for S20, the only free id left.

## 7. Provenance and what must happen before any of this is quoted

Configuration: `config/strategies/design_space.yaml` (loads through
`configs.load_design_space_strategies`). Falsification tests: `docs/design_space/falsification_register.csv`,
33 rows over 12 strategies. Thirty-one are `status: untested`; the S10 single-host control and the
S19 activation-lead sweep were run in the 2026-09-03 verification pass at n = 25 without a manifest
and are marked `provisional`, awaiting the Phase D battery. Gate mapping:
`config/regulatory_gates.yaml`.
Revisions: `protocol/revisions.csv` rows R006 and R007. Phase A mechanisms: `docs/design_space/bottleneck_decomposition.md`
sections 4, 7 and 8. Prior art and landscape: `docs/design_space/prior_art_review.md`,
`docs/design_space/competitive_landscape.md`, and the family and landscape notes under
`docs/design_space/prior_art/` and `docs/design_space/landscape/`.

Every run made before 2026-09-03 is superseded for quantitative use by revisions R004, R005 and R007,
so the scoping and smoke numbers quoted in section 3 and section 4 are recorded as *model behaviour
that motivated a design choice*, never as results. They come from short unregistered runs without
manifests and must not be quoted; each one is marked at its point of use. The supersession also
covers the Phase A decomposition outputs carried into this document, above all the cost-share
percentages from `abl_20260902_phaseA`, which are not scoping or smoke numbers but are still
pre-R004; those carry their own vintage label where they appear. Where an unregistered number carries
a decision, the decision is provisional until the Phase D battery reruns it with a manifest: S17's
reclassification as routine contracted supply, S10's disposition against a single-host control, and
S19's service prediction at a 386-day activation lead. Before any number from these twelve strategies is reported: fix NEW-1, decide
NEW-2 and NEW-3, separate the measurement boundary from the parameter grid for MD-17, and run the
Phase D battery with run manifests under `results/manifests/`.
