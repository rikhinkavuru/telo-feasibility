# Field kit (two pages, interviewer only)

**INTERVIEWER ONLY. This card is not shown to the interviewee, not attached to any message, and not left
behind.** Page 1 is what you read out. Page 2 is the reference you turn to *after* the person has answered, per
the anchoring rule in `elicitation_worksheet.md` section 3. The interviewee's own copy is the role handout in
`modules/handouts/`, which carries the question, the units and the answer form and no model output at all.

Written 2026-09-05, corrected 2026-09-06. Long form: `guide_core.md`; elicitation order and the parameter card:
`elicitation_worksheet.md`; the one published timetable: `elicitation_worksheet.md` section 2.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value below is evidence tier 5 (illustrative),
87 of 91 parameters. None of it is a statement about sterile-injectable manufacturing. Nothing in this
conversation is a partnership, endorsement, customer, pilot, review or regulatory opinion. All sixteen
regulatory gates are UNCERTAIN with no reviewer, and UNCERTAIN is never PASS. No interview has been held, so
nothing here is tested in use.

**Ask for their range before showing yours.** A range with a reason is the preferred answer, not a fallback. A
rate needs three numbers: how often, how long, how much capacity lost. Attribution is by role and organization
type only, unless authorized in writing. Say who you are and who you work for in the first minute
(`guide_core.md` section 2).

---

# Page 1: what you say

**Everyone, at the front.** "During a shortage, what actually stops supply from responding first, and what gets
blamed incorrectly?" Then: "Which number from your own domain is furthest from reality in this study, and what
range would you use instead? Give me your range before I show you mine."

**Then the cards below that this person can answer. Skip the rest.**

**1. Demand denominator (HA-11a, queue rank 5).** "For this exact presentation, how many units a year does your
data actually show being consumed, and what does that number cover: which sites, which years, and does it
include what you could not get?"

**2. Regional replenishment policy (HA-40, rank 6).** "At a regional stocking point you know, how often is the
position reviewed, at what level do you reorder, and what level do you order up to?"

**3a. Line data, to a line engineer (HA-21, rank 8).** "For a small aseptic vial line: realistic saleable batch
size, batches of one presentation per line-year, campaign length, changeover days, and the uptime you actually
see."

**3b. Line cost, to a CDMO commercial lead or engineering vendor (HA-13, rank 7).** "Installed and qualified
capital for a line at that capacity, annual fixed operating cost, and for an existing registered line: what a
reserved-capacity agreement costs in dollars per year, what the fee covers, and the minimum campaign."

**4a. Ask this first, and alone (HA-38, rank 15).** "Does your organization ever pay for standing availability
of a generic injectable, separately from the units it ships? If yes, how much a year, for what committed
response time, and on what activation trigger?"

*A yes changes what card 4b means, so it has to come first. Do not append it to a price question.*

**4b. Then price and commitment (HA-36, HA-24, ranks 9 and 10).** "For this presentation, what price per unit
and what committed annual volume could you actually sign, over what term, and what is the remedy if the
supplier fails to supply?"

**5. Reporting category (HA-23, rank 12).** "Is adding a named third-party sterile fill site to an approved
application a CBE-30-class change, or a prior-approval supplement with a preapproval inspection?"

*HA-31, the sixteen gate statuses, is not asked on a call. It is `../reviewer_packets/packet_2_regulatory.md`,
made once, in writing, after the sequencing gate clears.*

**6. Multi-site disruption (HA-39, rank 14).** "What events take out more than one nominally separate site or
supplier at once, how often, for how long, and how much capacity do they remove?"

**7. Sterilization route (HA-34, rank 13).** "For products you have personally worked on, is the marketed
product terminally sterilized or aseptically processed, and how do you know? If terminal, what is the cycle?"

**The close, in two parts.** "Which single assumption would you attack first, and what would you use instead?"
Then, after they have finished: "If that conclusion held, what would change in your own work, and what would
you need to see before changing it?" Write both verbatim. Then: may we follow up once, and may we cite you by
role. Log within 24 hours per `evidence_log_schema.json`.

**Four things that must never be said.** Names only; the exact sentences are in `guide_core.md` section 7 and
in `../../CLAIMS_REGISTER.csv`. Read them before the call. Do not carry them into the room.

1. **C009**, the two-week-lab-hold sentence.
2. **C010**, the automates-release and certifies-in-real-time sentences.
3. **C015**, the operating-system positioning.
4. **C025**, the sentence attributed to the 2004 aseptic guidance section XI.B.

From the claim-discipline table: never "distributed manufacturing solves shortages", never a CMS figure called
a manufacturing cost, never "partnered with" after an interview. No model number is a finding.

---

# Page 2: reference, after they have answered

Everything on this page is model behaviour under illustrative inputs. It is shown to nobody.

**1. Demand denominator (HA-11a).**
**Lands on:** `product.annual_demand_units` and regional shares in `config/products/*.yaml`, then `demand.py`
and the deterministic screen.
**Now:** norepinephrine 500,000 / 900,000 / 1,800,000 units per year; sodium bicarbonate 600,000 / 1,200,000 /
2,400,000.
**If far:** the two surviving designs lose the target above 1.09M and 1.19M units per year (S11) and 0.93M and
1.25M (S16) (`results/design_space/ds_post_R008/thresholds.csv`, `capacity_utilization` rows). At twice base demand no strategy of
the twenty meets it in any recorded reversal cell. Demand carries 46 of 138 crossings and is the only axis with
a region where nothing qualifies.
**Not asked here:** installed capacity serving the presentation is HA-11b, an evidence-acquisition task against
FDA establishment registration and drug listing, the ANDA and RLD holder set, DQSA section 506C notifications
or a commercial data vendor. The only interview half of it is line rates, which is card 3a.

**2. Regional replenishment policy (HA-40).**
**Lands on:** `region_base_stock`, `region_reorder_point_days`, the region policy block in
`strategies.build_strategy`.
**Now:** hard-coded and never specified by the protocol. Reorder when the position falls to lane time plus one
day, then order up to safety plus lane days. The daily base-stock alternative exists in code and ships unused.
**If far:** MD-3 decides 8 of 16 Phase A cells at +0.82% cost. On the post-R008 bounds ablation the review rule
alone moves P(fill >= 0.99) from 0.28 to 1.00 for both S0 and S1 on norepinephrine, and the comparators are
feasible in 0 of 16 cells with the frozen rule against 11 of 16 with daily review
(`results/ablation/abl_post_R008/summary.json`, configs `bounds:ss365` and `bounds:ss365+base_stock`, n = 60).
The 0.56-to-0.90 and 0.65-to-0.94 figures that stood here until 2026-09-06 came from the superseded pre-R004
run and must not be quoted.
**Trip-wire:** "daily order-up-to" is the arm that takes the comparators from 0 of 16 feasible cells to 11 of
16. If they name it, say so in the log.

**3a. Line data (HA-21).**
**Lands on:** `product.units_per_batch`, `batches_per_site_year_nominal`, `product.changeover_days`,
`uptime_fraction`; `production.py`.
**Now:** batch size 30,000 (10,000 to 75,000) norepinephrine and 25,000 (10,000 to 60,000) sodium bicarbonate;
45 batches per site-year (30 to 70); changeover 3 days (1 to 10); uptime 0.85 (0.70 to 0.95).
**If far:** changeover produces 20 crossings, and three of the five designs feasible on both products lose the
target inside 6.5 days, one at 3.39 days against a 3-day base. The five need 35.6 to 44.4 batches per site-year
(`results/design_space/ds_post_R008/thresholds.csv`, `batches_per_site_year` rows: S9 35.6 and 40.6, S11 36.9 and
44.4, S12 44.4 and 44.4, S13 38.1 and 43.1, S16 43.1 and 43.1) against a base of 45 and a low of 30.

**3b. Line cost and reserved capacity (HA-13).**
**Lands on:** `capital_usd_per_site`, `fixed_qa_labor_usd_per_site_year`,
`global.reserved_capacity_fee_fraction`, `reserved_capacity_activation_days`.
**Now:** capital 15M / 40M / 100M USD per site; fixed quality, operations and metrology labour 1.5M / 3.0M /
6.0M USD per site-year; activation 21 days (7 to 60).
**How to reveal the reservation fee.** The model carries it as a *fraction* of the reserved site's annualized
fixed plus capital cost, 0.1 / 0.3 / 0.6. Nobody prices a line that way. Ask instead for **dollars per year for
a reserved slot at a line of that size, and what the fee covers**, and derive the fraction afterwards. Same for
the two scaling exponents: ask them to reject "a line at 35% of the central plant's capacity costs 53% of its
capital and 43% of its annual fixed quality cost", which is 0.35^0.6 and 0.35^0.8.
**If far:** fixed and resilience cost is 81.0% to 93.7% of annual cost in all eight comparators, so every
absolute cost here is a statement about the scaffold until this lands. Activation latency binds in three cells
at 19.4, 22.7 and 27.7 days. Across 313 sources the landscape review found no published rate card, minimum
order value or reservation fee for US sterile fill-finish, and the one published reservation price has its
per-batch figure redacted (F7-S04).

**4a. Is availability funded at all (HA-38).**
**Lands on:** no field exists. The reservation-fee and take-or-pay ledger in `simulation.step8_costs` is the
nearest thing.
**Now:** the package assumes no. No US hospital system, GPO or state was found paying a standing reservation
fee for sterile generic capacity (F3-S28).
**If far:** a "no" leaves every capacity-carrying design unfunded by construction, and the recorded rule is to
assume no until a purchaser says otherwise. A "yes" creates a revenue line the engine does not have.

**4b. Price, committed volume, term, remedy (HA-36, HA-24).**
**Lands on:** `ContractTerms`, all nine required fields: payer, purchaser, beneficiary, term, committed volume,
activation condition, allocation rights, default risk (the failure-to-supply remedy), price
(`contracting.ContractTerms.REQUIRED`).
**Now:** no price evidence exists anywhere in the study. The package assumes 18.00 USD per unit against a
per-unit variable cost of 1.15 (norepinephrine) and 1.20 (sodium bicarbonate) USD, so the contribution margin
used in the contract table is 16.85 and 16.80 USD per unit. Break-even for S16 is 13.18 (sodium bicarbonate)
and 16.94 (norepinephrine) USD per unit at the optimized designs
(`../design_space/inventory_capacity_hybrids.md` section 4, computed from `opt_20260903T220534Z`); the
simulation-side contract table gives 14.46 and 17.10 for the same strategy
(`results/design_space/contract_conditions_sim_post_R008.csv`). Every design reads NOT CONTRACTABLE.
**If far:** at 18.00 USD, five of the thirteen cells that meet the service target need more than 100% of
saleable capacity committed. USP reports 74% of sterile injectables in shortage priced below 15 USD per unit
and 44% below 5, n = 61.

**5. Reporting category (HA-23).**
**Lands on:** gate G07 in `config/regulatory_gates.yaml`, and the activation and qualification leads for S12
and S16 in `config/strategies/design_space.yaml`.
**Now:** all sixteen gates UNCERTAIN, zero reviewed, no reviewer and no date; `regulatory.evaluate_all` returns
NO_CONCLUSION for all twenty strategies.
**If far:** a prior-approval supplement with a preapproval inspection removes S12's 365-day leg and takes the
contracted family's central advantage over building; three falsification-register rows turn on it. Ask for the
reading and its citation in writing, with qualification and date. Offer no regulatory opinion in either
direction, and accept none as settled in conversation.

**6. Multi-site disruption (HA-39).**
**Lands on:** `global.common_cause_events_per_year`, `common_cause_duration_days`,
`common_cause_capacity_impact`, then `disruptions.py` and the common-cause groups in
`strategies.build_strategy`.
**Now:** 0.02 / 0.1 / 0.3 events per year, 14 / 60 / 240 days, 0.2 / 0.5 / 1.0 of capacity lost at affected
sites.
**Confirm the entity level explicitly (worksheet rule A1).** The parameter record in `config/global.yaml`
declares `units: per_year` and `entity_level: network`, and the engine applies it **per common-cause group**:
`disruptions.generate_world` draws the Poisson events inside `for gid in roster.group_ids`. Ask for the rate
per group of things that fail together, and record which level the person answered at.
**If far:** 20 crossings. At base demand the feasible set collapses from 11 strategies to 3 on norepinephrine
and from 10 to 2 on sodium bicarbonate across 0.02 to 0.3. The two surviving designs cross between 0.138 and
0.182, so the base of 0.1 sits within a factor of two of failing.

**7. Sterilization route (HA-34).**
**Lands on:** `ProductFeatures.sterilization_route`, unset for both dossiers, and a parametric-release scenario
in `ReleaseScenario`.
**Now:** no route recorded for either product. Sterility incubation is 14 days base over a 14 to 18 day range,
and 14 days is the argmax of the parallel release set at every corner of that box.
**If far:** the terminal route with parametric release is the only intervention found across fourteen families
that acts on the binding release constraint rather than on components that do not bind. "Aseptic" everywhere
closes that family permanently.
**Where the answer actually comes from.** HA-34 is a document task first and an interview second. Label text
does not carry the route. The accessible sources are the reference product's approval package on Drugs@FDA
(the chemistry review's sterility-assurance section), a redacted establishment inspection report or Form 483
for the named site, and the USP monograph's sterility requirement. Ask a person only about products they have
personally worked on; the route for somebody else's marketed product is generally confidential to its holder,
so the person who could settle it is usually the person who may not.
