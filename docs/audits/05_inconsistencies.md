# Inconsistencies: protocol, workbook, repository, and public claims

Audit date 2026-09-01. Each row names the conflict, the artifacts, which one is authoritative (most recent with a primary source, or the protocol where it governs), and the effect on this study. Items the study cannot resolve are routed to `07_human_action_queue.md`.

## A. Protocol vs workbook

| ID | Conflict | Authoritative | Effect |
|---|---|---|---|
| I-A1 | Protocol Eq. 4 divides by saleable units delivered; workbook 09!T divides by annual demand | protocol | replica keeps demand; corrected variant and simulation use delivered nonexpired units |
| I-A2 | Protocol requires each durable strategy optimized to the same service target; workbook holds fixed multipliers and its own 08!A2 admits nothing optimizes | protocol | strategies become design variables (phase 4) |
| I-A3 | Protocol 4.4 makes gates binary with UNCERTAIN blocking conclusions; workbook results key eligibility to a typed YES flag unlinked to the gate sheet | protocol | eligibility derived only from gate statuses |
| I-A4 | Protocol 2.4 weights 20/20/15/15/10/10/10 over seven criteria; workbook formula matches but its documented weights table lists five entries summing to 0.80 | protocol | weights load from protocol.yaml |
| I-A5 | Protocol lists eight hard product gates (identity, manufacturing fit, control status, pathway, demand observability, clinical substitutability, input feasibility, economic relevance); workbook scores five (non-controlled, small molecule, aqueous, standard vial, no cytotoxic/HP) | protocol | all eight implemented; workbook's five map onto PG2 and PG3 |
| I-A6 | Protocol names the CRF formula; workbook types CRF as a constant and its discount rate has no consumer | protocol | CRF computed |
| I-A7 | Protocol requires shelf life to cap inventory; workbook shelf life feeds nothing | protocol | expiry cohorts in simulation |
| I-A8 | Protocol's four regions in the base case; workbook has a "Regions served" input with no consumer | protocol | network topology |
| I-A9 | Protocol requires recovery defined as sustained service; workbook has no recovery metric | protocol | recovery metrics in simulation |
| I-A10 | Protocol source register S25 says "Lee et al., Management Science"; workbook 02!G29 says "Published 2026" while the DOI string reads 10.1287/mnsc.2024.08337 | unresolved | verify DOI and year before citing |
| I-A11 | Workbook 03_Product_Score lists six candidates with decisions (sodium bicarbonate "Advance to diligence", norepinephrine "Advance as comparator"); protocol 2.5 says provisional, not final | protocol | candidates remain provisional; no decision until frozen snapshots and gates |

## B. Protocol/workbook vs repository

| ID | Conflict | Authoritative | Effect |
|---|---|---|---|
| I-B1 | Protocol provisional comparator is norepinephrine 1 mg/mL 4 mL ("resolved/recurrent"); repo's `beachhead-verification.md` (2026-07-16) shows ASHP resolved 2022-06-07 with a single bulletin ever (opened 2017-02-09) and 0 openFDA records | repo memo (primary sources) | norepinephrine qualifies as a *resolved* comparator only; its "recurrent" label is unsupported until the FDA shortage history snapshot is frozen |
| I-B2 | Protocol provisional case is sodium bicarbonate 8.4% 50 mL; repo scorecard ranks sodium bicarbonate 10th of 26 (34.6) with regulatory sub-score 1 and no presentation-level evidence | neither; different criteria | sodium bicarbonate stays on the longlist; the study's own screen decides |
| I-B3 | Repo scorecard's pick furosemide 10 mg/mL (42.1) is a protocol "reserve" | protocol governs the study; repo evidence is prior | furosemide stays on the longlist as reserve with the repo evidence attached (HA-03, HA-18) |
| I-B4 | Workbook product sheets give release time 14 d (A) and 12 d (B) as single numbers; repo memo decomposes release into sterility >= 14 d (critical path), EM 5-7 d, assay 5-7 d, endotoxin 2-3 d, QA 0-4 d | repo memo (tier 1) | release time modeled as components; release-assurance can touch only the validated chemical component |
| I-B5 | Workbook 08!E11 = 0.6 release-time factor for S6 (illustrative); repo memo says chemical RTR saves about zero days for aseptic injectables | repo memo | S6 base case: zero release-time benefit; rapid-micro package as a separate scenario with vendor-claim tier |
| I-B6 | Workbook 07_Product_B is a near-clone of 06_Product_A (9 of 60 cells differ); repo memo gives norepinephrine-specific facts (light protection, RTU premium, supplier count ~20 companies / 23 applications) | repo memo | product configs must differ where evidence differs |
| I-B7 | Workbook assumes 503B strategy as a row with typed multipliers; repo `dme-rule.md` and `beachhead-verification.md` establish 503B is blocked absent shortage and can never be the convoy | repo memos and protocol 4.2 | S7 is a time-varying state machine gated by shortage-list status |
| I-B8 | Workbook site-failure and common-cause rates are "Expert estimate" with no expert; repo has no failure-rate evidence either | none | tier 5 until elicitation or historical-episode calibration |

## C. Repository internal and public claims

| ID | Conflict | Authoritative | Effect on study |
|---|---|---|---|
| I-C1 | Beachhead: README and `startup-outline.md` §5 say norepinephrine -> epinephrine [V]; `beachhead-verification.md` kills both; scorecard says furosemide; roadmap says furosemide pending | beachhead memo (kill) and roadmap (pending) | product selection starts from evidence, not from any of these |
| I-C2 | Value proposition: README, outline, deck, website say the two-week hold is removed; `release-constraints.md` says ~0 days for aseptic injectables | release-constraints | H7 is tested as stated; S6 gets no free release-time benefit |
| I-C3 | AI headline: website says 89% at verified >= 90%; README says that conflated measurement with proof (CV+ proves 71.5%) and reports 86.9% at proved 90% | README + result JSONs | CLAIMS_REGISTER |
| I-C4 | Tablet gated mis-release: website "near 3%" vs stored 0.7% | `tablet_summary.json` | CLAIMS_REGISTER C007 |
| I-C5 | Website benchmark rows (split, CV+, crepes, RTRT) match no result JSON | result JSONs | not used by this study |
| I-C6 | Phlow contract $812 M vs $696.7 M | both have sources: the 2020 press release says "up to $812 million" ($354 M base + $458 M options); USASpending contract 75A50120C00092 shows $696,665,953.98 (ASPR, 2020-05-18 to 2027-01-13) as of the 2026-09-01 probe. State which one is meant. | not a model input |
| I-C7 | Shortage count ~270 (2026) vs 227 (Q2 2026), both [V], neither sourced | neither | study freezes its own snapshot |
| I-C8 | "44% of injectables in shortage sell under $5": [V] in outline, [U] in later memos | later memos | not used |
| I-C9 | 503B facility count ~80 vs 95 | 95 (FDA table 2026-07-23) | context only |
| I-C10 | NIH SBIR standing date 2026-09-05 vs 2026-09-08 | `applications.md` | none |
| I-C11 | Annex 22: "final expected mid-2026" vs OS README "still draft, EMA reconsidering" | OS README (latest); both secondary | gate G15 legal basis stays unresolved |
| I-C12 | Check counts: `validate_core.py` 16 / 7 / fifteen; OS tests 102 / 471 | source | none |
| I-C13 | Website "automates the release decision" / "operating system"; OS docs "advisory only; not a release decision"; deck prompt says do not call it an OS | OS architecture docs | claim discipline |
| I-C14 | `paper/SUBMISSION.md` says repo must not be published and is 404; repo is public | GitHub state | HA-04, HA-05 |
| I-C15 | Website says every hyperparameter is selected by cross-validation on calibration data; `experiment_tablet.py` hard-codes `N_PLS = 8` with no selection code | code | CLAIMS_REGISTER |

## D. Task statement vs evidence

| ID | Conflict | Resolution |
|---|---|---|
| I-D1 | Task says "654 tablets"; file holds 655, experiment uses 615 | report 615 (155 + 460) |
| I-D2 | Task says exposure reduced "to around 1%"; stored 0.74% | report 0.7% with the abstention rate beside it |
| I-D3 | Task says conditional coverage 32.6%; that is a mean over 23 seeds, pooled 30.5% | report both with the seed count |
| I-D4 | Task and repo call FR doc 2026-14073 the "DME rule"; the Federal Register record titles it "Drug Establishment Registration and Drug Listing Requirements for Establishments Engaged in Distributed Manufacturing and Certain Foreign Establishments" (proposed rule, 91 FR 42888, Docket FDA-2025-N-6075, RIN 0910-AI94, 21 CFR 207, comments closed 2026-09-11) | gate G13 cites the record by title; "DME" is used only as the repo's shorthand |
| I-D5 | Task lists acyclovir sodium injection and norepinephrine as shortage-related candidates; on 2026-09-01 both have 0 rows in the FDA shortage CSV (1,635 rows) and 0 openFDA records; sodium bicarbonate has 19 rows (current since 2017-03-01) and furosemide 33 | longlist keeps them only with a dated historical basis (repeated snapshots, Wayback, or ASHP by human retrieval) |
| I-D6 | Workbook and task treat S7 (503B) uniformly across products; FDA's 503B bulks list explicitly does not include sodium bicarbonate (88 FR 20531), so bulk-substance compounding of Product A is limited to the shortage-list pathway; norepinephrine appears on neither list | gate G09 evaluated per product |
