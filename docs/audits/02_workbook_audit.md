# Workbook audit: `Telo_Feasibility_Model.xlsx`

Audit date 2026-09-01. File sha256 `367069513203098f0157dfca83272e7bda35b045ecd67139bb268d483b9be9f8` (55,725 bytes). Cover: "0.1 research scaffold", as of 2026-09-01, status "ILLUSTRATIVE - DO NOT CITE OUTPUTS". Method: every cell of every sheet dumped with openpyxl (formulas and cached values, fills, comments, validations); four audit agents read the dump sheet by sheet and recomputed every formula; the author of this document read sheets 03-06, 08-10, 12, 13 directly. Cached values match recomputation for all 320 formulas on 09_Deterministic (1e-9 relative) and all 165 on 12_Results/13_Checks. No circular references, no defined names, no comments, no `#REF!`; the only cached errors are four deliberate `NA()` cells (12_Results!H5, H6, H13, H14).

The workbook does what its cover says: it is an auditable scaffold, not evidence. The findings below are what the Python deterministic model must reproduce exactly (for reconciliation) and what it must then correct (in a separately labeled variant).

## 1. Structure

| Sheet | Rows x cols | Role | Formulas | Yellow inputs |
|---|---|---|---|---|
| 00_Cover | 23 x 8 | version, decision rule, status | 0 | 1 |
| 01_ReadMe | 14 x 8 | operating steps with status list | 0 | 0 |
| 02_Sources | 29 x 9 | source register S01-S25 with URL, tier, status | 0 | 0 |
| 03_Product_Score | 15 x 16 | 6 candidates, 5 hard gates, 7 criteria, weighted score | 6 | 0 |
| 04_Reg_Gates | 19 x 9 | 15 gates, all UNCERTAIN, reviewer columns empty | 0 | 0 |
| 05_Assumptions | 25 x 8 | 21 global parameters, low/base/high | 0 | 63 |
| 06_Product_A | 24 x 8 | sodium bicarbonate 8.4% 50 mL, 20 parameters | 0 | 60 |
| 07_Product_B | 24 x 8 | norepinephrine 1 mg/mL 4 mL, 20 parameters | 0 | 60 |
| 08_Strategies | 12 x 14 | 8 strategies x 9 multipliers, pathway, eligibility flag | 0 | 72 |
| 09_Deterministic | 20 x 22 | 16 product-strategy rows, 20 computed columns | 320 | 0 |
| 10_MC_Parameters | 18 x 11 | 14 stochastic parameters, distribution family, group | 0 | 84 |
| 11_Sensitivity | 14 x 10 | 10 planned sweeps, all status Planned | 0 | 30 |
| 12_Results | 20 x 13 | dashboard: cost/unit, response days, shortage days, ICER, verdict | 160 | 0 |
| 13_Checks | 17 x 8 | 9 checks, READY/NOT READY | ~25 | 0 |
| 14_Interview_Log | 34 x 10 | empty template, 30 rows Not scheduled | 0 | 0 |
| 15_Revision_Log | 104 x 9 | empty template, 100 rows Pending | 0 | 0 |
| 16_Sim_Output | 5 x 16 | import schema with one example row | 0 | 16 |

Yellow (`FFFFF4CC`) cells total 386. All numeric model inputs are yellow; every product-sheet status cell reads `Illustrative`; 10_MC_Parameters has 7 `Missing` and 7 `Illustrative`, 0 `Sourced`.

## 2. The deterministic chain (09_Deterministic, one row per product x strategy)

Inputs: product sheet base column C (rows 5-13, 15-21, 23), strategy multipliers (08!B-J), globals (05!C7, C8, C16-C23, C25). Row r for Product A uses strategy row r; rows 13-20 for Product B use strategy rows r-8.

| Col | Name | Formula (row 5 shown) | Notes |
|---|---|---|---|
| C | Sites | `='08_Strategies'!B5` | |
| D | Annual demand | `='06_Product_A'!C5` | demand, not delivered units |
| E | Units/batch | `='06_Product_A'!C6` | |
| F | Batches/site-year | `='06_Product_A'!C7*'08_Strategies'!C5` | nominal x capacity factor |
| G, H | Yield, Uptime | product C8, C9 | |
| I | Saleable capacity | `=C5*E5*F5*G5*H5` | protocol Eq. 1 |
| J | Utilization | `=IFERROR(D5/I5,0)` | Eq. 2; zero capacity silently yields 0 |
| K | Annualized capex | `=C5*'06_Product_A'!C19*'05_Assumptions'!C25` | CRF is a typed constant |
| L | Fixed QA/labor | `=C5*'06_Product_A'!C18*'08_Strategies'!H5` | |
| M | Validation annualized | `=C5*'06_Product_A'!C20/'05_Assumptions'!C7*'08_Strategies'!I5` | straight-line, not CRF |
| N | Variable production | `=D5*(C15+C16)/(1-C23)` | grossed up by scrap |
| O | Testing | `=IFERROR(D5/E5,0)*C17` | batches = demand/units per batch, no yield |
| P | Inventory carrying + expiry | `=N5*'08'!D5/365*'05'!C8 + N5*C23` | scrap charged again |
| Q | Distribution | `=D5*C21` | |
| R | Reserved capacity cost | `=D5*(C15+C16)*'08'!J5` | fee as fraction of variable cost, not capacity |
| S | Total annual cost | `=SUM(K5:R5)` | |
| T | Cost/unit | `=IFERROR(S5/D5,0)` | divides by demand (Eq. 4 wants delivered units) |
| U | Response days | `=C12+C13+C10+(C11*'08'!E5)+'08'!F5` | Eq. 5; release scaled by strategy factor |
| V | Expected shortage-days (screen) | site term + common-cause term + demand-shock term (see below) | heuristic; not derived |

V5 in full: `MAX(0, C*λ_site*dur_site*MAX(0, J-(C-1)/C)/MAX(J,1e-4) + λ_cc*dur_cc*MAX(0, J-(1-impact_cc*G_strat))/MAX(J,1e-4) + λ_shock*dur_shock*MAX(0, mult-I/D)/mult)`. It counts event-driven days only and ignores chronic shortfall, safety stock, and response time.

12_Results: F = shortage-days avoided vs the status-quo row; G = incremental cost vs status quo; H = G/F (ICER) or `NA()`; I = approximate fill rate `1 - E/365 * severity(05!C24)`; J = verdict keyed on `08_Strategies!L = "YES"`, then I vs target fill (05!C9), then sign of G.

13_Checks: nine checks; READY only when all nine are OK. Currently 3 OK (capacity > 0, cost/unit > 0, source register >= 20 active) and 6 ATTENTION (15 gates unresolved, 20 + 20 illustrative product inputs, 14 MC parameters missing/illustrative, utilization <= 1 fails for 2 of 16 rows, 0 accepted reviews of 3 required).

## 3. Anomaly register

Severity: blocker = invalidates a headline number; major = changes a comparison or violates a stated rule; minor = local error; info = naming or documentation. Cross-references: wb-A/B/C/D are the agent reports in the session scratchpad.

| ID | Sev | Finding | Evidence | Treatment in code |
|---|---|---|---|---|
| WB-01 | blocker | Product A status quo is capacity-infeasible (utilization 124.5%) but every cost column scales with demand and cost/unit divides by demand, so the row prices 1.2 M vials from a plant that makes 963,900 | 09!J5=J6=1.2449; 13_Checks!B10=14 of 16 | Replica reproduces; corrected variant caps delivered units at capacity and divides by delivered units; both reported |
| WB-02 | blocker | Safety stock has no effect on shortage days or response days; strategy S1 shows only carrying cost | V6=V5=17.45; U6=U5=115; 08!D never enters U or V | Screen cannot rank S1; documented as a screen limitation; simulation is the only place S1 is ranked |
| WB-03 | blocker | Release time does not feed the shortage metric; S6 is strictly dominated in the screen (+$2.0 M, -5.6 days, 0 shortage change) | U11=106.4 vs U10=112; V11=V10=0 | Same as WB-02; the screen cannot test H7 |
| WB-04 | blocker | Node scale is not parameterized: distributed nodes use the same $40 M capital, $3 M fixed, 25,000 units/batch as the central plant, and capacity factor 1.35 makes each node larger than status quo (1.05) | 08!C10=1.35; K10=4x K5; L10=5.6x L5; fixed items 93.6% of S10 | Distributed cost/unit ($41.71 A, $54.47 B) is an artifact; node size becomes a design variable in code |
| WB-05 | major | Regulatory eligibility is a typed constant (08!L) not linked to 04_Reg_Gates; four strategies pass as YES while all 15 gates are UNCERTAIN | 08!L5:L8=YES; 04!E5:E19=UNCERTAIN | Code derives eligibility only from gate statuses; UNCERTAIN is never PASS |
| WB-06 | major | UNCERTAIN strategies (S4-S7) compute identically to eligible rows and flow into the dashboard unflagged | 09 rows 9-12, 17-20 | Code tags every row with eligibility and excludes NO_CONCLUSION rows from favorable classes |
| WB-07 | major | Product hard gate zeroes score only on FAIL; UNCERTAIN would score as PASS (latent) | 03!O5:O10 formula | Code: any UNCERTAIN gate blocks final selection |
| WB-08 | major | Scoring weights hard-coded in formulas; the documented weights table has 5 entries summing to 0.80 and is referenced by nothing | 03!C15:G15 vs formula 20/20/15/10/15/10/10 | Weights load from protocol.yaml (sum checked = 1.0) |
| WB-09 | major | CRF is a typed constant labeled "Calculated"; discount rate (05!C6) has zero consumers; low CRF pairs low rate with high life | 05!C25=0.16275 = CRF(0.10,10); B25 = CRF(0.06,15); D25 = CRF(0.15,7) | Code computes CRF from rate and life; low/high pairing documented |
| WB-10 | major | Most of 05_Assumptions is unwired: horizon, discount rate, shortage-day threshold, iterations, time step, regions, growth, demand CV have no consumers; no Low/High cell is used anywhere | consumer scan of all formulas | Protocol values now live in protocol.yaml; screen uses only what it uses, documented |
| WB-11 | major | Each product carries the full network capital and fixed cost; shared-site allocation absent | K10=K18=26.04 M; L10=L18=16.8 M | Multi-product pooling is a design variable; screen labels per-product totals as unallocated |
| WB-12 | major | 10_MC_Parameters: 0 sourced; values are typed duplicates of 05/06 (drift risk); five rows contain the string "Product sheet"; no units column; no correlation coefficients, autocorrelation, or variance components despite naming them | 10!D5:F18, K5:K18 | Config parameters carry distribution, units, dependence group, and provenance; no duplicated literals |
| WB-13 | major | 11_Sensitivity ranges disagree with the input sheets they sweep (release 3/14/35 vs 5/14/28; QA 1.5/3/7 M vs 1.5/3/6 M; yield, uptime, CV, lead time, shelf life all differ); "capacity utilization" is an output; "common-cause correlation" has no input counterpart; nothing has been run | 11!B5:D14, J5:J14=Planned | Sensitivity ranges come from the same parameter records as the base case |
| WB-14 | major | Dashboard verdict "Below service target" flips inside the workbook's own low/high range of an illustrative severity scalar (05!C24 = 0.35, low 0.1, high 0.8) | 12!I5 = 0.9952 at 0.1, 0.9833 at 0.35, 0.9618 at 0.8 vs target 0.99 | Screen fill-rate proxy labeled as such; service verdicts come only from simulation |
| WB-15 | major | Fill rate and cost/unit are defined differently in the dashboard (severity-scaled; per demand unit) and the simulation import schema (units supplied / demand; per supplied unit) | 12!I vs 16!G; 09!T vs 16!M | One definition set in schemas.py; every table states its denominator |
| WB-16 | major | Check 13 counts accepted revision-log issues, not completed qualified reviews | 13!B13 formula | Review completion is tracked per reviewer with qualification in docs/reviewer_packets |
| WB-17 | major | Readiness gate ignores 05_Assumptions, 08_Strategies, 11_Sensitivity, 14_Interview_Log, 16_Sim_Output; READY is reachable with every global input yellow and zero interviews | 13_Checks coverage | `make status` counts every tier-5 parameter and every definition-of-finished test |
| WB-18 | minor | Expiry/scrap double counted: N grosses up by 1/(1-scrap), P adds N x scrap again ($29,388 at base A) | 09!N5, P5 | Corrected variant removes the second charge; unit label "fraction/year" vs production-scrap use flagged |
| WB-19 | minor | Capital annualized by CRF, validation straight-line over life (M5 = $400 k vs $651 k at CRF) | 09!K5 vs M5 | Corrected variant annualizes both with CRF; replica keeps straight-line |
| WB-20 | minor | Testing batches ignore yield and available batches (48 vs 50 needed vs 47.25 available) | 09!O5 | Corrected variant uses batches actually produced |
| WB-21 | minor | Reserved capacity % is charged as a fraction of annual variable cost of all demand, not as reserved capacity | 09!R; 08!J header | Reserved capacity becomes an explicit contract term (reserved units, fee per reserved unit, take-or-pay) |
| WB-22 | minor | Shortage-day screen is a knife-edge at utilization 0.5 for 2-site strategies; V = 0 for 10 of 16 rows | 09!V7:V9 | Labeled screening heuristic; not used for ranking |
| WB-23 | minor | Orphan product rows: shelf life (C14), delivery time (C22), target safety stock (C24) have no consumers; strategy sheet carries different delivery and safety-stock values | 06!C14, C22, C24 vs 08!D, F | One source of truth per parameter in config |
| WB-24 | minor | Hard-coded constants inside formulas (365; 0.0001 guard; 9 in the READY test; expected counts 16, 20, 3) | 09!P, V; 13!B17, C9:C13 | Named constants in code |
| WB-25 | minor | Unguarded divisions (life, 1-scrap, shock multiplier) can produce #DIV/0! | 09!M, N, V | Validated at load: life > 0, scrap < 1, multiplier > 0 |
| WB-26 | minor | Product B is a near-clone of Product A (9 of 60 numeric cells differ); a 4 mL light-sensitive vial shares capital, QA, testing, and distribution values with a 50 mL vial | 06 vs 07 | Product configs must carry product-specific evidence before any comparison is reported |
| WB-27 | minor | Number-format bugs: 11!B6:D6 (days) and B7:D7 (dollars) formatted as percent | 11_Sensitivity | none (workbook) |
| WB-28 | minor | Source IDs: 05!G and 06/07!G hold prose ("Expert estimate", "...needed") not S-IDs; 02_Sources access dates all stamped 2026-09-01; column I has two overlapping validations; S01-S03, S07-S09, S21, S24 referenced nowhere | 02, 05, 06, 07 | Provenance ids are required fields in schemas |
| WB-29 | minor | Status-quo capacity factor is 1.05, so "nominal" is not status quo | 08!C5 | Nominal batches defined as status quo; capacity factors become design variables |
| WB-30 | info | Baseline rows self-reference (G5 = S5-S5); interview and revision templates pre-fill 130 phantom statuses; example simulation row contradicts the screen for the same case (annual cost 8.5 M vs 13.1 M) | 12!G5; 14!J; 15!G; 16 row 5 | Templates start empty; example rows never imported |
| WB-31 | info | Naming drift across sheets (Sites vs Sites/nodes; Material vs API vs Raw-material lead time; Delivery time vs Delivery days vs Transport time; three fill-rate notions) | headers | Controlled vocabulary in schemas |

## 4. What the workbook cannot do (and therefore what the code must)

- Rank S1 (safety stock) or S6 (release assurance): their mechanisms do not enter the screen metric (WB-02, WB-03).
- Represent node scale (WB-04), multi-product pooling (WB-11), shelf life (WB-23), regional structure, common-cause groups beyond one scalar, or any queue.
- Enforce the same service target across strategies; 08!A2 says it must, nothing does.
- Tie eligibility to gates (WB-05).
- Run any sensitivity (WB-13).

## 5. Reconciliation plan

`telo_feasibility.deterministic.run_screen(mode="workbook_replica")` reproduces columns C-V for all 16 rows from the same base inputs; `reconcile_with_workbook` reads the cached values with openpyxl and reports any absolute difference above 1e-6 (currency) or 1e-9 (fractions). `mode="corrected"` applies WB-01 (delivered-unit denominator and capacity cap), WB-18, WB-19, WB-20, WB-21 and reports the deltas as a separate table so that a reader never mistakes a correction for a reconciliation failure. Test: `tests/regression/test_workbook_reconciliation.py`.
