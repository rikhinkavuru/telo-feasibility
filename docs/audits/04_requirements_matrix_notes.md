# Requirements matrix: notes

Companion to `04_requirements_matrix.csv` (100 rows, R001-R100). Status counts at 2026-09-02: exists 27, partial 46, missing 27. Human-required rows: 26.

The matrix was written by the author-facing agent after the audits, not by the planned workflow agent: that agent, and the adversarial verification pass over major findings, terminated on a session limit before returning anything. Consequence: the anomaly registers in `02_workbook_audit.md` and `03_conformal_reproduction_audit.md` carry one audit reading plus the author-facing agent's own direct reading of the sheets and result files (recorded in RESEARCH_LOG), not an independent second pass. Treat every finding as reviewable.

## Ambiguities resolved (with the choice made)

| Item | Ambiguity | Resolution |
|---|---|---|
| Eq. 5 overlap | Workbook sums lead + changeover + cycle + release + delivery serially; protocol says terms overlap only where valid | Replica keeps the serial sum; `ManufacturingSite.release_time_days` takes the maximum of concurrent release components plus any serial QA component; the simulation uses queues (R035) |
| Tail confidence q | Protocol names q but gives no number | 0.90 pre-specified (R001); sensitivity none because it is a decision rule, not an estimate |
| Recovery window | Protocol offers 14 or 30 days | 30 base, 14 sensitivity |
| Gate set | Protocol 4.4 has 8 rows; workbook 15 | 15-gate superset with protocol_ref per gate |
| Product hard gates | Workbook scores 5 gates; protocol lists 8 | 8 implemented; UNCERTAIN blocks selection (workbook let it pass) |
| CRF | Workbook typed | Replica keeps typed value for exact reconciliation; corrected variant computes |
| "654 tablets" | Task statement vs file (655) vs experiment (615) | Report 615 |
| Reserved capacity fee | Workbook charges a fraction of variable cost | Kept in both deterministic modes with the WB-21 label; contract terms become explicit in the simulation |
| S6 in the deterministic screen | Workbook's 0.6 release factor | Kept as an illustrative design variable; release scenario stays R0 |
| Provisional candidates in shortage | Task lists acyclovir and norepinephrine; 2026-09-02 FDA snapshot shows 0 rows for both | Kept on the longlist with dated evidence; scored 1 on recurrence by rule; selection deferred |

## Requirements the protocol implies but does not state

- A universal entity roster so common random numbers survive strategies with different site counts (design.md section 4).
- A whitelist of release-time components a release-assurance scenario may reduce (R056).
- A per-product 503B bulks-list status (sodium bicarbonate is explicitly not included) feeding gate G09 (I-D6).
- A visiting-hours rule for accessdata.fda.gov, honored by scheduling the fetch inside the window (done 2026-09-02 00:01 EDT).
