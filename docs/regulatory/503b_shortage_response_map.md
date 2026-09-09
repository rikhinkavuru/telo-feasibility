# 503B shortage-response pathway: preliminary decision map

**PRELIMINARY REGULATORY ANALYSIS; NOT LEGAL ADVICE.** Not reviewed by a qualified 503B regulatory professional. Gates G08-G12 are `UNCERTAIN`. This pathway is modeled as a time-varying state (strategy S7); it is never a bridge to an ANDA and never a permanent supply source (protocol 4.2).

## 1. Legal structure (labels per protocol)

| Element | Basis | Label | Snapshot |
|---|---|---|---|
| Outsourcing facility registration, CGMP, reporting | FD&C Act 503B (21 U.S.C. 353b); 21 CFR Part 211 as applied | law_or_regulation | S06 (CFR XML) |
| Bulk drug substance eligibility: on the 503B bulks list, or the drug is on FDA's shortage list at the time of compounding, distribution, and dispensing | FD&C 503B(a)(2)(A) | law_or_regulation | S14 (bulks policy page, final list, categories March 2025, interim policy) |
| Essentially-a-copy restriction and its shortage exception | FD&C 503B(a)(5); FDA guidance January 2018 | law_or_regulation; final_guidance | S15 (503B and 503A guidances) |
| FDA statement on compounding when drugs are on the shortage list | agency web page (content current 2025-08-08) | agency_initiative (explanatory) | S13 |
| Interim policy on bulk substances under evaluation (Category 1 enforcement discretion) | FDA interim policy | agency_initiative (enforcement discretion) | S14 interim policy PDF |
| State licensure and distribution permissions | state law | law_or_regulation (varies) | none frozen (HA-23) |
| Beyond-use dating and release-before-sterility practice | FDA 503B CGMP guidance; USP chapters (paywalled) | final_guidance; compendial (not frozen) | HA-17 |

## 2. State machine used by the model

`Shortage503BState.eligible_today = on_shortage_list AND static_gates_pass AND state_permission`

- `on_shortage_list` is exogenous and product-specific. It is read from the frozen FDA shortage snapshot at model start and evolves through the regulatory random stream (arrival of resolution, re-listing) in the simulation. It must hold at compounding, at distribution, and at dispensing; the model therefore checks it on the day a batch is compounded and again on each shipment and issue day.
- `static_gates_pass` requires G08 (registration and CGMP status) and G11 (BUD, sterility, testing package) to be PASS.
- `state_permission` requires G12 (state-by-state map) for each served region; regions without permission are removed from S7's service set.
- When `on_shortage_list` turns false, compounding of an essentially-a-copy product stops; inventory already compounded may not be distributed or dispensed under the exception after that date (law_or_regulation as written in 503B(a)(5); whether any transition relief exists is an unresolved_question for the reviewer).

## 3. Per-candidate predicates from the 2026-09-02 snapshots

| Candidate | FDA shortage list (S01, 2026-09-02) | 503B bulks list (S14) | Copy-restriction exception available today | Note |
|---|---|---|---|---|
| sodium bicarbonate 8.4% | 19 rows, 15 Current, first posted 2017-03-01 | explicitly NOT INCLUDED (88 FR 20531, 2023-04-06) | yes while listed; bulk compounding permitted only through the shortage-list predicate | presentation-level listing (11 rows match 8.4% / 84 mg/mL) |
| norepinephrine 1 mg/mL | 0 rows | absent from both tables | no | S7 ineligible today; repository memo reached the same conclusion 2026-07-16 |
| furosemide 10 mg/mL | 33 rows, 30 Current, first posted 2020-04-07 | absent | yes while listed | |
| acyclovir sodium | 0 rows | absent | no | |
| sterile water for injection | 21 rows, Current, first posted 2021-11-23 | absent | yes while listed | scale question (PG8) |
| acetazolamide sodium 500 mg | 0 rows | absent | no | out of archetype |

"Absent" means the substance appears on neither the Included nor the Not Included table of the final 503B bulks list page; it may sit in a category under evaluation (interim policy), which is enforcement discretion, not eligibility.

## 4. Gate register for this pathway

| Gate | Treatment | Status | What resolves it |
|---|---|---|---|
| G08 facility registered and CGMP-compliant | exclude_if_fail | UNCERTAIN | a registered outsourcing facility (Telo's or a partner's) with inspection history |
| G09 bulk substance eligible at compounding, distribution, dispensing | dynamic_state | UNCERTAIN | product-specific reading of 503B(a)(2) against the frozen shortage snapshot, then continuous monitoring |
| G10 not barred as essentially a copy | dynamic_state | UNCERTAIN | product-specific legal analysis of the exception and of any clinical-difference route |
| G11 BUD, sterility, and testing package | cap | UNCERTAIN | stability, sterility, and release package under 503B CGMP expectations |
| G12 state licensure and distribution | region_restriction | UNCERTAIN | state-by-state map |

## 5. What this map does not say

It does not say 503B production is lawful or unlawful for any product. It records which statutory predicates are currently satisfied on the frozen FDA data, which are unknown, and how the model turns the pathway off when the predicates lapse. It does not assign a BUD; the repository's 6-day at-risk / 90-day assured figures are secondary-sourced (HA-17).
