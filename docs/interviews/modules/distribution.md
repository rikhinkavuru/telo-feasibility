# Module: GPO, wholesaler and distributor

Roles: a distribution or network-design lead, and where possible someone with contracting authority for question 7.
Queue items this module settles: HA-24, the channel half of HA-11a, the lane input behind HA-40, and the allocation and
mechanism fields of HA-36. Length: the whole call is 45 minutes and this module has about 28 of them; the one published timetable is
`../elicitation_worksheet.md` section 2. Run the parameter cards inside the module, not before it.

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value in the "Now" column is a model input at evidence
tier 5, not a measurement, and everything in the last column is behaviour of the engine under those inputs. Nothing
here asserts a partnership, endorsement, customer, pilot or regulatory opinion, because none exists.

**Why the questions changed.** Two of this module's inputs are cost only, and a purely economic input cannot cross the
study's service test by construction, so a surprising answer there changes the ledger and not a verdict. The two
questions that decide something are allocation rights, which block contractability for every architecture in the
battery, and the resilience premium, which is the only place a capacity leg could be funded. Both are asked as
categories and prices, not as opinions.

**How to run it.** Ask for the range before revealing the "Now" column. Name the exact presentation.

## Questions

| # | Question | Lands on | Now (declared range) | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | Where does inventory for this presentation sit, and how many days are held at each echelon? | `product.target_safety_stock_days`, plus the site and region split in the engine | 60 days (30 to 180) | days per echelon | Where the model places stock. The regional layer is where the replenishment rule in the hospital and GPO module bites hardest |
| 2 | What are the lane times from manufacturer to distribution centre to hospital? Then, for variability, ask two observables rather than a coefficient of variation: **what is the 90th-percentile transit day, and what fraction of shipments arrive more than a day late?** | `product.delivery_days`; `global.transport_time_cv` | 2 days (1 to 5). The variability record is a transit coefficient of variation of 0.25 (0.1 to 0.5), which nobody measures; derive it from their two observables and log the conversion | a typical lane time in days, a 90th-percentile day, and a late fraction. Never ask for a coefficient of variation | More than transit time. The hard-coded regional reorder point is lane days plus one, so the lane time sets the review rule the model is most sensitive to |
| 3 | What does warehousing and transport cost per unit for a product like this? | `product.distribution_usd_per_unit` | 0.20 USD per unit (0.05 to 0.80) | a range in USD per unit, with the scope named | Cost only. A purely economic input cannot cross a service boundary in this study, so this changes the ledger and never a feasibility verdict |
| 4 | For an emergency transfer, how fast, and at what multiple of normal cost? | `global.emergency_transport_days`; `global.emergency_transport_premium` | 1 day (1 to 2); 3.0 times normal distribution cost (1.5 to 6.0) | a range in days and a multiplier | The cost of the response mechanism every design leans on during an event |
| 5 | When supply is short, what allocation rule actually runs, who holds the right to direct product, and can that right be sold or contracted away? | the policy argument in `allocation.py` (proportional, criticality weighted, minimum guarantee, optimization); `ContractTerms.allocation_rights` (HA-24) | all four policy values collapse to proportional in the engine today, so the field is a contract requirement rather than a number | a category for the rule, plus who signs, plus yes or no on whether the right is sellable | `ContractTerms.missing()` names `allocation_rights` for every architecture, which is one of the reasons every design in the battery reads NOT CONTRACTABLE. It also names an engine gap that has to be closed before the field means anything numerically |
| 6 | During an event, how far does order data drift from actual use: hoarding, allocation-capped orders, substitution masking? | the definition of the demand denominator behind `product.annual_demand_units` (HA-11a) | no dataset exists. Purchase history is the only candidate denominator | a category for the mechanisms, plus a correction range if one exists | Whether purchase history can serve as the utilization denominator at all. Demand is the highest-decision-value input in the queue, and this question decides whether the available data can answer it |
| 7 | What does a resilience premium look like in a contract that has actually been signed: capacity reservation, take-or-pay, failure-to-supply remedy, and what was paid? | `global.reserved_capacity_fee_fraction`; the `take_or_pay_fraction` design variable; `ContractTerms` mechanism, activation condition and default risk (HA-24, HA-36) | fee 0.3 of the reserved site's annualized fixed plus capital cost (0.1 to 0.6). No price evidence exists: across 313 sources the landscape review found no published rate card, minimum order value or reservation fee for US sterile fill-finish | a category for the mechanism plus a price range, or a plain no | The commercial half of every capacity-carrying design. One engine limit before reading an answer in: take-or-pay changes cost and no service quantity today, so an answer improves the contract description before it improves a number. If this person holds contracting authority, ask the price and committed-volume question from the hospital and GPO module here as well |

## What was dropped, and why

- **Nothing was dropped.** All four questions from the previous version survive, in questions 1 to 5 and 7.
- **Two questions were added.** Who holds allocation rights and whether that right is sellable, because that field
  blocks contractability for every architecture. And how far order data drifts from use during an event, because the
  demand denominator is the highest-value input in the queue and purchase history is the only candidate source for it.
- **No question asks which architecture a distributor would prefer.** The study no longer asks anyone to rank
  architectures. It asks for the transport numbers, the allocation rule, and a price that was actually paid.
