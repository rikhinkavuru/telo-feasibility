# Product screen: dated longlist, gates, and data-based scores (2026-09-02)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** This screen selects nothing. It records what the frozen official snapshots say about six exact presentations, which hard gates can be evaluated from data, and which criteria await expert scores.

Snapshots (sha256 prefixes in `data/product_dossiers/screen_manifest.json`): FDA drug shortages CSV export (S01, retrieved 2026-09-02 04:01 UTC inside the accessdata visiting window), openFDA shortages bulk (S01B, 2026-09-01), Drugs@FDA (S16), Orange Book (S17), DailyMed SPL queries (S18), FDA 503B bulks list (S14), CMS Part B spending 2024 (S19, proxy only). ASHP bulletins are a human task (S21).

## Longlist and hard gates

| Candidate | Protocol role | PG1 identity | PG2 fit | PG3 control | PG4 pathway | PG5-PG8 | Outcome |
|---|---|---|---|---|---|---|---|
| sodium bicarbonate 8.4% 50 mL vial | current/recurrent case candidate | PASS | PASS | PASS | UNCERTAIN (19 applications, 13 holders) | UNCERTAIN | UNCERTAIN |
| norepinephrine 1 mg/mL 4 mL vial | resolved comparator | PASS | PASS | PASS | UNCERTAIN (26 applications, 23 holders) | UNCERTAIN | UNCERTAIN |
| acyclovir sodium 50 mg/mL vial | reserve | UNCERTAIN (fill not fixed) | PASS | PASS | UNCERTAIN (22, 14) | UNCERTAIN | UNCERTAIN |
| furosemide 10 mg/mL vial | reserve (repo pick) | UNCERTAIN (fill not fixed) | PASS | PASS | UNCERTAIN (37, 28) | UNCERTAIN | UNCERTAIN |
| sterile water for injection vial | scale question | UNCERTAIN | PASS | PASS | UNCERTAIN (1, 1) | UNCERTAIN; PG8 scale mismatch | UNCERTAIN |
| acetazolamide sodium 500 mg vial | out-of-archetype comparator | PASS | FAIL (lyophilized) | PASS | UNCERTAIN (10, 10) | UNCERTAIN | FAIL |

PG5-PG8 (demand observability, clinical substitutability, input feasibility, economic relevance) cannot be evaluated from public data; they wait on HA-11, HA-12, HA-20.

## Shortage evidence (FDA export, 1,635 rows, 2026-09-02)

| Candidate | Rows | Current | Earliest initial posting | Stated reasons |
|---|---|---|---|---|
| sodium bicarbonate | 19 (11 match 8.4%) | 15 | 2017-03-01 | demand increase; discontinuation; other |
| furosemide | 33 (1 matches 10 mg/mL text) | 30 | 2020-04-07 | demand increase; discontinuation; CGMP requirements; inactive-ingredient shortage; other |
| sterile water for injection | 21 | 21 | 2021-11-23 | demand increase; discontinuation; other |
| norepinephrine | 0 | 0 | none | none |
| acyclovir | 0 | 0 | none | none |
| acetazolamide | 0 | 0 | none | none |

A single export shows current state only (7 Resolved rows in the whole file). Recurrence and resolved history need repeated snapshots or ASHP bulletins. The workbook's "resolved/recurrent" label for norepinephrine is unsupported by this snapshot; the repository's 2026-07-16 memo found one ASHP bulletin ever (2017-2022).

## Data-based criterion scores (rules in `product_selection.py`)

| Candidate | Recurrence/duration (0.20) | Supplier vulnerability (0.15) | Public-data strength (0.10) | Data partial score (of 0.45) | Workbook provisional total (tier 5) |
|---|---|---|---|---|---|
| sodium bicarbonate | 5 (current since 2017) | 1 (13 holders) | 5 | 1.65 | 4.45 |
| furosemide | 5 (current since 2020) | 1 (28 holders) | 5 | 1.65 | 3.90 |
| sterile water | 5 (current since 2021) | 5 (1 holder; Orange Book names the ingredient differently, so low confidence) | 5 | 2.25 | 3.80 |
| acyclovir sodium | 1 | 1 (14 holders) | 4 | 0.75 | 3.55 |
| norepinephrine | 1 | 1 (23 holders) | 3 | 0.65 | 3.70 |
| acetazolamide | 1 | 1 (10 holders) | 4 | 0.75 | excluded (gate FAIL) |

Clinical criticality, manufacturing fit, regional relevance, and demand/contract fit (0.55 of the weight) are expert-pending. The workbook's provisional totals are the author's unsourced scaffold values and are shown only to make the gap visible.

## What the screen already changes

1. Norepinephrine is a resolved comparator, not a recurrent one, on today's data. Its supplier base (23 holders) is the least concentrated of the six.
2. Sodium bicarbonate and furosemide are both long-running current shortages with many approved holders, which is itself informative: holder count has not prevented shortage, consistent with the repository's supplier-concentration thesis being about API and component dependence rather than application count (PG7, still unmapped).
3. 503B for sodium bicarbonate depends entirely on the shortage-list predicate because the substance is explicitly not on the bulks list.
4. Sterile water is the strongest on the data rules and the weakest on scale; the workbook's "scale mismatch" verdict is a judgment the data cannot make.

## Next steps

Expert scoring (HA-20, HA-21), ASHP retrieval (HA-10), supplier and component map (HA-12), founder decision on furosemide's role (HA-03), then the challenge step (protocol 2.2 step 5) before any selection.
