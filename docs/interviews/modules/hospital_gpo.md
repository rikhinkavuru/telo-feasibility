# Module: hospital pharmacy, IDN and GPO

Roles: pharmacy or supply-chain leader with purchase data, a replenishment planner, and where possible someone with
contracting authority. Queue items this module settles: HA-11a, HA-40, HA-43, HA-35, and HA-36, HA-38 and HA-24 in part, if this person
has signing authority; if they do, run `purchaser.md` instead.
Length: the whole call is 45 minutes and this module has about 28 of them; the one published timetable is
`../elicitation_worksheet.md` section 2. Run the parameter cards inside the module, not before it.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value in the "Now" column is a model input at evidence
tier 5, not a measurement. Everything in the last column is behaviour of the engine under those inputs, not a statement
about sterile-injectable manufacturing. All sixteen regulatory gates are UNCERTAIN and no strategy carries a favourable
decision class. Nothing here asserts a partnership, endorsement, customer, pilot or regulatory opinion, because none
exists.

**Why the questions changed.** The study was built around one question: under what conditions distributed regional
capacity beats safety stock, dual sourcing, reserved contract capacity or added central capacity. Under the model's own
inputs that question is answered, and the answer is that it does not beat them anywhere in any recorded range. So this
module no longer asks anyone to rank architectures. It asks for numbers and categories, because every input in the model
is illustrative and only evidence moves a verdict.

**Two notes on scope.** The installed capacity that serves the presentation is **not** asked here. That is HA-11b,
an evidence-acquisition task run against FDA establishment registration and drug listing, the ANDA and RLD holder
set, DQSA section 506C notifications or a commercial data vendor; the only interview half of it is line rates, which
belong to `manufacturing.md`. This module asks only for the demand denominator, HA-11a. And questions 7 and 8 need
someone with signing authority: if this person has it, run `purchaser.md` instead, which asks them in the right
order.

**How to run it.** Ask for the person's range before revealing the "Now" column, per `../elicitation_worksheet.md`. A
range is a better answer than a point estimate, and "I do not know, but X would" is a good answer. Name the exact
presentation. The two configured presentations are norepinephrine 1 mg/mL 4 mL and sodium bicarbonate 8.4% 50 mL, both
provisional comparators; furosemide 10 mg/mL is a candidate whose longlist status is undecided. Attribution is by role
only unless the person authorizes more. Log within 24 hours per `../evidence_log_schema.json`; an answer here becomes
evidence tier 4.

## Questions

| # | Question | Lands on | Now (declared range) | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | How many units of this presentation does your system buy in a year, and what does that number cover: which sites, which years, and does it include what you could not get? | `product.annual_demand_units` (HA-11a) | norepinephrine 900,000 units/yr (500,000 to 1,800,000); sodium bicarbonate 1,200,000 (600,000 to 2,400,000) | a range in units per year, with the denominator named | **Surprising is above roughly 0.9 to 1.25M units a year: the two surviving designs lose the target above 1.09M and 1.19M (S11) and 0.93M and 1.25M (S16).** The densest axis in the map: 46 of 138 threshold crossings, and the only axis with a region where nothing qualifies. At twice base demand no strategy of the twenty meets the frozen service target in any of the 18 reversal cells |
| 2 | Of that volume, how much moves through a regional stocking point rather than direct, and how uneven is it across regions? | regional shares in `demand.py`; the engine splits demand equally across four regions (engine limit MD-15) | equal shares, no declared range | a percentage split, or a statement that no stable split exists | Whether regional pooling is modelled at the right granularity. Equal shares is an engine limit, not a considered assumption |
| 3 | At a regional stocking point, how often is the position reviewed, and to what level do you order up? | `region_base_stock`, `region_reorder_point_days` (HA-40) | hard coded, not a parameter: order-up-to equals safety-stock days plus lane days, reorder point equals lane days plus 1.0 day. The protocol never specifies the rule | a category (continuous review, periodic at a stated frequency, daily order-up-to) plus the level in days of cover | **Surprising is "daily order-up-to": that is the arm that takes the comparators from 0 of 16 feasible cells to 11 of 16.** The largest single model artifact found in the Phase A decomposition. The rule alone decides 8 of 16 cells at +0.82% cost, and on the post-R008 bounds ablation it moves P(fill at or above 0.99) from 0.28 to 1.00 for the status quo on norepinephrine (`results/ablation/abl_post_R008/summary.json`, n = 60). The 0.56-to-0.90 figure that stood here until 2026-09-06 was pre-R004 and is superseded |
| 4 | How many days of supply do you hold for this presentation in normal times, and where does it physically sit? | `product.target_safety_stock_days`, plus the site and region split | 60 days (30 to 180) | a range in days per echelon | Every inventory-led design in the battery. In the matched-space check every winning design sits at 253 to 365 days of safety stock, which is above the top of this declared range |
| 5 | When an order cannot be filled, how long does it stay open before the demand is lost or substituted? Does that differ by presentation and by customer? | `global.backorder_window_days` (HA-43) | 7 days (3 to 30) | a range in days, plus whether it varies | **There is no direction to watch here: the effect is not monotone in the window (MD-5), so any answer other than 7 days changes what the metric means rather than which way it points.** At 7 days the reported fill rate is closer to a weekly service level than to an annual fill rate |
| 6 | When this presentation is unavailable, what happens clinically, and how hard is substitution in practice? | `ProductFeatures.substitution_difficulty`; product gate PG6 (HA-35) | no field exists. Nothing in the objective distinguishes a critical miss from a substitutable one | a category (routine substitute, difficult substitute, no acceptable substitute) with the reason | The service target itself, and therefore every feasibility verdict, because one uniform target is applied to every presentation today |
| 7 | Would your organization pay for standing availability of a generic injectable, separately from the units it ships? If yes, how much per year, for what committed response time, and on what activation trigger? | an availability-payment term `contracting.py` does not have; `ContractTerms.price_required_usd_per_unit` (HA-38) | the package assumes no. No US hospital system, GPO or state was found paying a standing reservation fee for sterile generic capacity (F3-S28) | yes or no with a reason; if yes, an annual amount, a response time and an activation condition | Every capacity-carrying design is unfunded by construction today. A yes creates a revenue line the engine does not have. A no confirms the standing assumption and closes that family |
| 8 | What price per unit and what committed annual volume could you actually sign, over what term, and what is the remedy if the supplier fails to supply? | `ContractTerms` price, committed volume, term, default risk (HA-36, HA-24) | 18.00 USD per unit is an illustration, not evidence. Under illustrative costs the status quo breaks even at 14.26 to 14.43 USD per unit and the distributed-node designs at 40.58 to 49.11. Public context: USP reports 74% of sterile injectables in shortage price below 15 USD per unit and 44% below 5, n = 61 (F12-S14) | a range in USD per unit, a committed volume in units per year, a term in years, and the remedy as a category | Five of the thirteen strategy-product cells that meet the service target move from commercially possible to impossible as the price falls from break-even to 18.00 USD. Below break-even the commercial case goes for all of them |
| 9 | Can you share purchase history by presentation and by site, and on what terms? | the utilization dataset behind `product.annual_demand_units` (HA-11a evidence) | no dataset exists. CMS Part B is an outpatient proxy that misses inpatient essential injectables | yes or no, plus format, granularity and terms | Whether question 1 can ever be answered at evidence tier 2 rather than tier 4 |

## What was dropped, and why

- **Allocation during a shortage** moved to `distribution.md`. All four allocation policy values collapse to
  proportional in the engine today, so an answer changes a contract field rather than a number, and the channel is
  closer to the rule than the buyer is.
- **503B, gray market and import sourcing.** The 503B half moved to `regulatory.md`, where 503B is modelled as a
  time-varying legal state rather than a sourcing option. Gray market and imports were dropped outright: no model entry
  point exists for either.
- **Any question asking which architecture the interviewee prefers.** The model has already answered that under its own
  inputs, and an opinion cannot move a tier-5 input. Question 7 is the one place a judgement still decides something,
  and it is asked as a commitment rather than as a preference.
