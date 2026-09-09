# Repository audit: `~/telo` (github.com/rikhinkavuru/Telo)

Audit date 2026-09-01. Read-only. Sources: local working tree, `git status`/`git diff`, GitHub API for the public tree and README, and agent reports (repo claims, evidence inventory, conformal reproduction and code review, OS package). The launch directory `~/feasibilitymodel_telo` was empty and sits inside a home-directory git root with no remote; it was not used.

## 1. State

| Item | Value |
|---|---|
| Remote | `git@github.com:rikhinkavuru/Telo.git`, branch `main`, HEAD c3b31b9 (2026-07-26 "Add the marketing site, and make it work on a phone") |
| Visibility | **public** (`"private": false`, `license: null`); `updated_at` 2026-09-01 (a non-push change on the audit date; nature undetermined) |
| Working tree | 12 modified files (+9,239 / -1,225 lines), 51 untracked entries; newest mtime 2026-07-30 (OS package README); dormant 33 days |
| Environment | root `pyproject.toml` (py3.12 research env, `package = false`), `.venv` present, `uv.lock` present locally but gitignored |
| Tests | research layer: none (a 12-check `validate_core.py` script run by hand); OS package: 13 pytest files, 471 `def test_` (untracked); web: none |
| CI, LICENSE, CITATION.cff, CHANGELOG | none |
| Stray artifacts | `.playwright-mcp/` logs tracked; `mobile-hero.png` at root untracked |

## 2. Layout and purpose

| Path | Purpose | Tracked at HEAD |
|---|---|---|
| `README.md`, `CLAUDE.md` | public front page; working rules (evidence tags, five things that must stay straight) | yes |
| `docs/` | `startup-outline.md` (canonical thesis), `paper-outline.md`, `roadmap.md` (three phases, dated 2026-07-26 findings), `os-architecture.md`, `brand/` | roadmap and os-architecture untracked |
| `research/` | `beachhead-verification.md` (2026-07-16, kills norepinephrine/epinephrine), `drug-selection-scorecard.md` (furosemide 10 mg/mL pick), `market-research.md`, `conformal/` (release-decision layer: core, 20 experiment scripts, results, investor artifact) | 19 of ~50 conformal files tracked; `data/*.mat` gitignored |
| `paper/` | Journal of Chemometrics manuscript, SI, review log, submission checklist, build outputs | untracked |
| `regulatory/` | `release-constraints.md` (sterility critical path; Annex 17/22), `dme-rule.md` (FDA DME proposed rule, comments closed 2026-09-11) | untracked |
| `os/quality-intelligence/` | shippable release-decision package (26 modules, proprietary license) | untracked |
| `funding/`, `outreach/` | applications, deck, EV proposal; facility and lab-contact lists | tracked and public |
| `telo-web/` | Next.js marketing site | `src/` tracked |
| `graphify-out/` | knowledge graph | tracked |

## 3. What the repository has established (usable by this study)

- **Release-time decomposition for aseptically filled injectables** (`regulatory/release-constraints.md`, tier 1 citations): USP <71> sterility incubation >= 14 days is the critical path; environmental-monitoring yeast/mould plates 5-7 days; assay 5-7 business days contract or 1-2 in-house; endotoxin 2-3 days (15 min PTS); QA review 0-4 days. Chemical real-time release therefore saves about zero days unless rapid sterility (1-3 days, vendor claims, product-specific acceptance) is validated. This directly parameterizes the release queue and the R1-R3 scenarios.
- **Norepinephrine and epinephrine are not in shortage** (openFDA 0 records; ASHP resolved 2022-06-07 and 2025-08-18, checked 2026-07-16). Norepinephrine vial FSS $1.47 (Big4) / $4.52; RTU bag $13.42-14.68 (VA FSS 2026-01-01); no ASP entry (bundled). These are reimbursement/price proxies, never cost.
- **Furosemide 10 mg/mL** is the repo's independent scorecard pick (42.1 vs dopamine 41.7 of 50); shortage status in 2026 is secondary-source only; 15 Drugs@FDA applications, all 10 mg/mL vial, no RTU premix.
- **95 registered 503B outsourcing facilities** (FDA table, 2026-07-23); 503B essentially-a-copy rule blocks RTU compounding absent a current shortage (FD&C 503B(a)(5); FDA 2018 guidance).
- **Conformal release layer**: methods proof on public tablet and corn NIR data; reproduces byte-for-byte (see `03_conformal_reproduction_audit.md`). Headline in the current uncommitted README: 86.9% release yield at a proved 90% coverage (RRCM), with 22 logged self-corrections.
- **DME proposed rule** (FR doc 2026-14073): analysis rests on two law-firm reads; primary text not read; comment window closed 2026-09-11.

## 4. What the repository does not have

- No feasibility model of any kind: no demand data, no cost model, no supply-network representation, no comparator strategies, no optimization, no sensitivity analysis. The workbook and protocol in `~/Downloads` are the only scaffold.
- No demand, cost, batch, yield, deviation, or lead-time evidence at tier 1 or 2 for any presentation.
- No interviews logged; no independent reviews; no regulatory opinion.
- No Telo data, no wet lab, no target-chemistry spectra.
- No tests, CI, license, or citation metadata at the repository level.

## 5. Integrity and exposure findings (for the author, outside this study's scope to fix)

1. **Public repository contradicts its own instruction.** `paper/SUBMISSION.md` (2026-07-26) says the repository "holds company strategy documents ... and must not be published" and records it as returning 404; the GitHub API reports it public. The public tree (128 paths) includes `docs/startup-outline.md`, `funding/applications.md`, the deck PDF, the EV proposal draft, `outreach/lab-contacts.md` (21 named academics with e-mail addresses and conflict notes), and `outreach/facilities.md` with vendor contract terms. Meanwhile the manuscript's headline experiments are not on the public repo; only the 2026-07-17 corn/tablet scripts are. The repo publishes the strategy and withholds the science, the inverse of the stated policy. Decision HA-04/HA-05 in `07_human_action_queue.md`.
2. **Public README is the stalest artifact**: norepinephrine -> epinephrine beachhead, 503B "fastest legal path", and the two-week-hold value proposition, all contradicted by the repo's later primary-sourced memos.
3. **Website research page** labels itself "Preprint" (nothing submitted), carries the retracted 89%/"verified >= 90%" headline, the retracted information-theoretic-ceiling and reference-noise claims, a "near 3%" tablet mis-release figure that matches no result (stored 0.7%), and benchmark rows (split, CV+, crepes, RTRT) that match no result JSON opened in the audit.
4. **Phlow contract value**: $812 M (announced "up to" figure, confirmed by press release) vs $696.7 M in the shipped investor deck (no source anywhere).
5. **Self-reported counts disagree**: `validate_core.py` described as 16, 7, and fifteen checks in three documents (source has 12 `check_*` functions at HEAD-era; the reproduction run reports 16 passing in the working tree); OS package "102 tests" vs 471 `def test_`.

## 6. Reuse decisions for the feasibility package

| Asset | Reuse? | How |
|---|---|---|
| `regulatory/release-constraints.md` release-time components | yes, as tier-1 cited parameters with the memo's own verification-debt flags carried | `config/products/*.yaml` release-time decomposition |
| `research/beachhead-verification.md` prices and shortage status | yes, as dated price proxies and shortage-history evidence | product dossiers |
| `research/drug-selection-scorecard.md` | as prior evidence in the candidate screen, not as the screen (different weights, paper-oriented criteria) | product dossiers, `05_inconsistencies.md` |
| `research/conformal/results/tablet_summary.json` | yes, as the only quantitative release-assurance evidence, tier 5 for target chemistry, with intervals from the audit | `release_assurance.py` parameters |
| `os/quality-intelligence` | interfaces and vocabulary only (release / decline / OOS / drift-excursion states); no import of code or validation claims | see addendum below when the OS audit completes |
| `docs/roadmap.md` dated findings | as context with their `[V, secondary]` tags | `docs/regulatory/` |

## 7. Preservation

Nothing under `~/telo` outside `feasibility/` was created, modified, or deleted by this work. All audit runs used scratch copies. Existing uncommitted changes remain uncommitted.
