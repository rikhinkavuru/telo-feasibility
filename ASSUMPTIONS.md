# Assumptions register (human-readable index)

The machine-readable register is the set of `UncertainParameter` records in `config/` (validated by `telo_feasibility.schemas`). This file indexes them by area, states the current evidence tier, and names what evidence replaces each illustrative value. `make status` counts remaining tier-5 (illustrative) parameters.

Evidence tiers (protocol 5.3): 1 official/legal, 2 direct operational, 3 peer-reviewed, 4 qualified expert elicitation, 5 illustrative placeholder (scaffold testing only; never a result).

## Current state (2026-09-01)

Every material numeric input inherited from the workbook is **tier 5**. The workbook marks them yellow (386 cells across sheets 05, 06, 07, 08, 10, 11, 16). Nothing below may appear in an external claim.

| Area | Parameters (workbook origin) | Tier | Replacement evidence needed |
|---|---|---|---|
| Global | horizon 3/5/10 y; discount 6/10/15%; capital life 7/10/15 y; carrying rate 12/20/30%; target fill 98/99/99.5%; shortage-day threshold 0.90/0.95/0.99; iterations 5k/10k/50k; regions 3/4/8; demand growth -2/1/5%; demand CV 8/15/30%; shock multiplier 1.1/1.35/2.0; shocks/yr 0.1/0.4/1.0; shock duration 7/30/90 d; site failures 0.05/0.2/0.6 per site-yr; failure duration 7/45/180 d; common-cause 0.02/0.1/0.3 per yr; common-cause duration 14/60/240 d; common-cause impact 20/50/100%; unmet severity 10/35/80%; CRF 0.103/0.163/0.240 (05_Assumptions) | 5 (thresholds and horizon are protocol choices, not evidence) | Protocol choices are frozen; rates and durations need historical shortage-episode data (FDA/ASHP histories, GAO), plant records (tier 2), or structured elicitation (tier 4) |
| Product A (sodium bicarbonate 8.4% 50 mL, provisional) | annual demand 0.6/1.2/2.4 M vials; units/batch 10k/25k/60k; batches/site-yr 30/45/70; yield 0.90/0.96/0.99; uptime 0.70/0.85/0.95; production cycle 1/3/7 d; release 5/14/28 d; material lead time 30/90/240 d; changeover 1/3/10 d; shelf life 12/24/36 mo; variable materials $0.25/0.60/1.50; conversion $0.20/0.60/1.50; testing $10k/30k/100k per batch; fixed QA/labor $1.5/3/6 M per site-yr; capital $15/40/100 M per site; validation $1/4/12 M; distribution $0.05/0.20/0.80 per vial; delivery 1/2/5 d; expiry/scrap 0.5/2/8%; safety stock 30/60/180 d (06_Product_A) | 5 | Demand: hospital/GPO/wholesaler utilization (tier 2) with CMS Part B only as a labeled proxy; batch/yield/uptime/cycle/changeover: manufacturer interviews (tier 4) or plant records (tier 2); release time decomposition: quality interviews; shelf life: DailyMed label and stability (tier 1); costs: supplier quotes, vendor/engineering estimates (tier 2/4) |
| Product B (norepinephrine 1 mg/mL 4 mL, provisional) | same structure as Product A with its own yellow values (07_Product_B) | 5 | same |
| Strategies (08_Strategies) | per-strategy sites, capacity factor, safety-stock days, release-time factor, delivery days, common-impact factor, fixed-cost factor, validation factor, reserved-capacity % | 5 | Optimized design variables replace fixed factors; factors that remain (common-impact, validation replication) need expert elicitation |
| Monte Carlo (10_MC_Parameters) | distribution families and low/base/high for demand noise, shocks, site failures, common cause, yield, uptime, release time, rejection, API lead time, transport | 5 (14 rows marked Missing/Illustrative) | Same sources as above; structural form chosen by posterior predictive checks, not in-sample fit |
| Regulatory gates (04_Reg_Gates) | 15 gates | UNCERTAIN (not a numeric assumption) | Qualified generic-drug/CMC and 503B regulatory review |

## Rules

- A parameter moves up a tier only with a source, access date, and (for tiers 2 and 4) a logged interview or document id in `data/interview_evidence/` or `data/expert_elicitation/`.
- Reimbursement (ASP, Part B spending, FSS price) is never entered as production cost.
- Any parameter whose change can reverse the preferred strategy is listed in its `outputs_it_can_reverse` field once the decision-reversal map exists.
