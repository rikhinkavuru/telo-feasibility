# Module: operations research and drug-supply economics

Roles: an operations researcher or drug-supply economist, and separately a reliability engineer or the owner of a
multi-site disruption dataset for questions 1 to 4. Queue items this module settles: HA-39 first, then HA-25 and the
structural half of HA-32. Length: the whole call is 45 minutes and this module has about 28 of them; the one published timetable is
`../elicitation_worksheet.md` section 2. Run the parameter cards inside the module, not before it.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value in the "Now" column is a model input at evidence
tier 5, not a measurement, and everything in the last column is behaviour of the engine under those inputs. Nothing
here asserts a partnership, endorsement, customer, pilot or regulatory opinion, because none exists.

**Why the questions changed.** The comparison the study was built to run is finished under its own inputs, and
distributed capacity does not win anywhere. What is still open is whether the dependence structure is right, because
the multi-site disruption rate is the axis on which the feasible set collapses, and whether the harness itself is
sound, because a fair-comparison check already reversed one headline. Two dependence questions were retired: demand
variance and demand covariance bind nowhere in the decomposition.

**This module carries the multi-site disruption question for the whole programme.** The core guide used to ask
"which nominally separate sites, suppliers or lanes fail together, at what rate, for how long, losing what fraction
of capacity?" of every interviewee. It is HA-39, `../sequencing.md` wave 1b routes it to this role alone, and questions
1 and 2 below already ask it properly. Nobody else is asked it.

**Confirm the entity level on questions 1 and 2 explicitly.** The parameter record in `config/global.yaml` declares
`units: per_year` and `entity_level: network`, and the engine applies the rate **per common-cause group**:
`disruptions.generate_world` draws the Poisson events inside `for gid in roster.group_ids`. Ask for the rate per
group of things that fail together, and record which level the person answered at (`../elicitation_worksheet.md`
rule A1).

**How to run it.** Ask for the range before revealing the "Now" column. Where an answer is a distribution rather than a
number, take the distribution.

## Questions

| # | Question | Lands on | Now (declared range) | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | At what annual rate do events occur that remove more than one nominally independent site or supplier at once? | `global.common_cause_events_per_year` (HA-39) | 0.1 events per group-year (0.02 to 0.3). Source locator is a workbook cell with no named expert | a rate per year, with the event definition and the dataset or elicitation behind it | 20 threshold crossings. At base demand the feasible set collapses from 11 strategies to 3 on one product and from 10 to 2 on the other as the rate moves from 0.02 to 0.3, and at the declared low of 0.02 the one-way sweep returns the frozen dual-sourcing comparator to feasible. Read those counts as direction: the reversal map runs at 10 paired runs |
| 2 | When such an event happens, how long does it last and how much capacity does it remove at the sites it touches? | `common_cause_duration_days`; `common_cause_capacity_impact`; `common_cause_capacity_impact_sd` (HA-39) | 60 days (14 to 240); impact 0.5 of capacity (0.2 to 1.0); impact standard deviation 0.15 (0.05 to 0.3) | ranges, or a distribution family with parameters | Whether a multi-site event is a slowdown or a removal. The engine draws the impact from a distribution whose mean never reaches total loss, which was itself the source of a defect fixed in September 2026 |
| 3 | For a single sterile site, what is the annual rate of a failure that stops or degrades production, how long does it last, and does any capacity survive it? | `site_failures_per_site_year`; `site_failure_duration_days`; `site_failure_residual_capacity` | 0.2 per site-year (0.05 to 0.6); 45 days (7 to 180); residual capacity 0.0 (0.0 to 0.5) | three ranges | **No threshold crossing exists on this axis in `results/design_space/ds_post_R008/thresholds.csv`, so there is no direction to watch and no answer here removes a design.** It moves shortage days and time to stable recovery, which are the two outputs the failure-rate parameter record itself names |
| 4 | For a single API or component supplier, what is the annual disruption rate and the typical duration? | `supplier_disruptions_per_supplier_year`; `supplier_disruption_duration_days` | 0.2 per supplier-year (0.05 to 0.6); 45 days (14 to 120) | two ranges | 16 threshold crossings. The tightest supplier condition in the whole grid is 0.213 per supplier-year, so a real rate near the top of this range removes designs |
| 5 | Which dependencies actually make nominally separate sites or suppliers fail together, and are named common-cause groups the right representation, or does this need a copula or an explicit shared-resource model? | the group declarations in `strategies.build_strategy` (`cc_api`, `cc_vial`, `cc_quality`, `cc_os`, geography) and `disruptions.py` (HA-25) | groups with one shared rate. Every frozen plan carries an API or a vial group, so adding sites cannot reduce supplier exposure | a structural answer, and if groups survive, a rate per group | The topology conclusion. Note that a group declared on a supplier was structurally inert until a fix on 2026-09-03, so any earlier result about upstream dependence in this package is superseded |
| 6 | Is a daily discrete-time engine with common random numbers the right harness for this comparison, and what would you change? Then one specific: **what would you run to check that the common-random-number pairing actually holds across architectures with different site counts?** The three defects that prompted the question, all now fixed, were an optimizer tie-break with no Monte Carlo standard error tolerance on a 20-run screen whose binomial standard error at the 0.90 tail requirement is 0.067; search spaces never matched across architectures; and opening inventory seeded with no charge to the ledger. | `optimization.optimize_strategy`; `optimization.DESIGN_SPACES`; `simulation._seed_initial_inventory` (HA-32) | fixed under revisions R010, R010 and R009 respectively; the battery has not been re-run on the fixed engine | yes or no on the harness, with named changes, and a test they would run for the pairing. **Do not ask for the run count at which contrasts stabilize:** that depends on this model's variance, which they have not measured, and it is speculation outside their own work (`../elicitation_worksheet.md` section 3, "Never") | The ranking. The matched-space check already reversed one headline: added central capacity meets the frozen target on both products once it is searched over the same inventory space, at roughly 60% of its declared-space cost. The symmetric test, narrowing the newer designs to the comparators' space, has not been run |
| 7 | What belongs in the objective and what must not be monetized: purchaser cost, provider harm, patient harm? | the protocol's welfare boundary; `unmet_demand_severity`, which the deterministic screen uses and the simulation never does (HA-25) | the objective is purchaser cost with a service constraint. Severity 0.35 (0.1 to 0.8), screen only | a boundary statement, plus what must stay unpriced | **No threshold crossing exists here and none can: this is a decision rule, not a swept input.** It changes what the study is allowed to conclude rather than any number in it. It pairs with the substitution question in the hospital and GPO module, since nothing today distinguishes a critical miss from a substitutable one |

## What was dropped, and why

- **The demand-process question** (lognormal AR(1) against negative binomial against block bootstrap, chosen by
  posterior predictive checks). Demand variance and demand covariance bind nowhere in the current decomposition, so the
  choice of family cannot move a verdict. Re-ask when a real order series exists, which is also the only thing that
  could fit one.
- **The standalone optimization question.** Folded into question 6, attached to two named defects rather than asked in
  the abstract, so the answer lands somewhere.
- **Any request for an opinion on distributed manufacturing.** Under the model's inputs it is dominated on both
  products and the fair-comparison correction does not rescue it. The useful contribution from this role is the
  disruption rate and the critique of the harness.
