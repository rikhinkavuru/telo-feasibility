# Module: purchaser with budget and contracting authority

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every value in the "Now" column is a tier-5 illustrative
model input, not a measurement. The last column is engine behaviour, not a claim about the world.

Role: the person who can sign, or refuse to sign, a multi-year commitment for a sterile injectable. In a health
system that is the contracting or sourcing executive rather than the pharmacy director; in a group purchasing
organization it is the category owner with budget; in government it is the contracting officer or programme lead.

Queue items this module settles: HA-36 (a price and a committed volume someone with authority would sign), HA-38
(whether anyone funds standing availability at all), HA-24 (contract terms), and the commercial half of HA-13.

## Why this role exists at all

The study added it because the model kept returning the same verdict from a direction it could not test. Every
architecture that meets the service target does so by holding capacity or stock that is not always used, and the
engine has no revenue side, so it can price that readiness as a cost and never as a product. `ContractTerms.missing()`
returns unanswered fields for every one of the twenty strategies. The synthesis states the consequence plainly: no
architecture in the battery is contractable today, and that is a statement about missing evidence rather than about
the architectures.

This is also the role most easily mistaken for a sales call. Read the guardrail in `target_matrix.md` before making
contact. Nothing in this conversation may describe a partnership, a pilot, a customer, or an endorsement, and no
number from this study may be offered as a finding.

## Questions

| # | Question in plain language | Parameter or gate | Now, and its declared range | Answer form | What it could reverse |
|---|---|---|---|---|---|
| 1 | For a generic sterile injectable you buy today, what do you pay per unit, and what is the highest you have ever paid during a shortage? | price input to `contracting.contract_requirement`; no model parameter exists, which is itself the finding | no price exists in the package. The only price datum is a 4.52 USD FSS vial proxy in the norepinephrine config header | two numbers, or a range, in USD per unit | every commercial threshold in `feasibility_regions.md` section 3 row 1, which is currently computed at an assumed 18.00 USD |
| 2 | Would you sign a multi-year commitment for a fixed volume at a premium over the spot price, and if so what premium and what volume? | `contracting.ContractTerms.price_required_usd_per_unit`, `committed_units_per_year` | unanswered for all twenty strategies | a premium as a percentage or a per-unit figure, plus an annual volume, or a refusal with the reason | whether any architecture is contractable; today the answer for all twenty is "not contractable, stated" |
| 3 | Have you ever paid for capacity you did not use, in any category, and what was it called on the invoice? | `reserved_capacity_fee_fraction`, and the take-or-pay term | fee fraction 0.3 of the annualized cost of the reserved line, range 0.1 to 0.6, tier 5 | a yes or no with an example, and the mechanism name | the reservation fee, which is currently a guess, and whether standing availability has a buyer at all |
| 4 | If a supplier guaranteed you would never go short of this product, what would that be worth per year to your organization? | no parameter; this is the missing revenue side | absent from the engine | an annual figure, or a statement that it is not budgetable and why | whether the OS-first and readiness-first roadmaps have a business at the other end |
| 5 | Who inside your organization actually pays when a shortage happens, and what does it cost them? | `unmet_demand_severity`, 0.35 of a unit's value, range 0.1 to 0.8, tier 5 | the parameter exists but nothing has ever measured it | the cost centre, and a cost per shortage day or per unit missed | the shortage cost that every incremental-cost comparison in the study rests on |
| 6 | What would make you switch a committed volume away from an incumbent supplier? | none; this is prior-art and moat evidence | the prior-art review records that Telo has no evidenced reason it beats the nonprofit incumbent | the two or three conditions, in the person's own words | falsification register row 15, which currently asks for exactly this and has no answer |
| 7 | If a new supplier had regulatory approval but no track record, what would you require before a first order? | gates G01 to G07, and the qualification lead time | all sixteen gates are UNCERTAIN with no reviewer | a list of requirements, and a rough elapsed time | the commissioning and qualification lead times, which decide the whole build-versus-contract comparison |
| 8 | Is there any budget line, in your organization or in any programme you know of, that pays for readiness rather than for product? | HA-38 | the study found no evidence either way | a yes with the programme name, or a no | whether availability payments are a real instrument or an idea from the operations literature |

## How to run it

Ask for the person's number before showing any of ours. Take ranges. If the answer to question 2 is a refusal, that
is a result and should be logged as one, not treated as a failed conversation: a documented refusal from someone with
authority is stronger evidence about contractability than an enthusiastic yes from someone without it. Record the
person's authority level explicitly, because an answer from someone who cannot sign does not settle HA-36.

## What is not asked here, and why

Nothing about the release layer, the operating system, or distributed manufacturing. This role's time is worth more
spent on price, volume and readiness, and the model already answers the architecture questions without them. Nothing
about clinical criticality either; that belongs to the hospital and pharmacy module.
