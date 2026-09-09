# AI assistance record

Purpose: an accurate record of what an AI coding agent produced in this package, so the author (Rikhin Kavuru) can review, understand, revise, and defend every part of it. This file is a disclosure, not a credit line. Nothing here claims that the author has already reviewed a given artifact unless the review column says so.

## Session 2026-09-01 (Claude Code, model Claude Fable 5.1)

Instructions given by the author: convert the existing protocol and workbook into a reproducible computational study; audit first; preserve all existing work; no fabricated evidence; negative results acceptable.

| Artifact | How produced | Author review status |
|---|---|---|
| `protocol/protocol.yaml`, `protocol/hypotheses.yaml`, `protocol/revisions.csv` | Agent transcribed the author's DOCX protocol (v1.0) into YAML; two open numbers (q = 0.90, 30-day window) chosen by the agent and flagged in revisions R001 | not yet reviewed |
| `config/regulatory_gates.yaml` | Agent merged workbook 04_Reg_Gates and protocol 4.4; legal-basis text drafted by the agent from general regulatory knowledge, unverified | not yet reviewed; requires qualified regulatory review before any status changes |
| `docs/architecture/design.md` | Agent-authored design | not yet reviewed |
| `docs/audits/*` | Agent-authored from agent audits of the repo, workbook, and conformal experiments; numbers quoted from files or re-runs | not yet reviewed |
| `pyproject.toml`, `Makefile`, `.gitignore`, `LICENSE`, `CITATION.cff`, `CHANGELOG.md`, `README.md` | Agent-authored scaffolding | not yet reviewed |
| `RESEARCH_LOG.md`, `DECISIONS.md`, `ASSUMPTIONS.md`, `CLAIMS_REGISTER.csv` | Agent-authored initial versions | not yet reviewed |
| `src/telo_feasibility/*`, `tests/*`, `scripts/*` | Agent-authored code (see CHANGELOG for versions) | not yet reviewed |

Subagent audits run on 2026-09-01 (read-only on the repository; outputs kept under the session scratchpad and summarized in `docs/audits/`): workbook sheets (4 agents), conformal reproduction (re-ran `experiment_tablet.py`, `experiment.py`, `validate_core.py` in a scratch copy), conformal code review, repository claims, evidence inventory, OS package audit, public-source probe. The planned adversarial verification of major findings (60 skeptic agents) and the requirements-matrix agent did not complete: they were terminated by a session limit. The matrix (`docs/audits/04_requirements_matrix.csv`) was therefore written by the main agent from the protocol and the audit reports, and the anomaly registers have not had an independent second pass beyond the main agent's own reading of the workbook cells and result files.

| `config/sources.yaml`, `src/telo_feasibility/acquire.py` | Agent-authored from the public-source probe; fetches ran 2026-09-01/02 with a descriptive user agent and robots compliance | not yet reviewed |
| `config/longlist.yaml`, `src/telo_feasibility/product_selection.py`, `data/product_dossiers/*` | Agent-authored scoring rules (documented in code) applied to frozen snapshots; expert-pending criteria left unscored | not yet reviewed; scoring rules are the author's to accept or replace |
| `src/telo_feasibility/{rng,disruptions,demand,inventory,allocation,suppliers,production,quality,release_assurance,strategies,simulation,runner,optimization,sensitivity,backcast,figures,release_benchmark}.py`, `scripts/*`, `tests/integration/*` | Agent-authored engine, optimizer, sensitivity, backcasting, figures, and benchmark; two defects found by the agent's own tests are logged in RESEARCH_LOG | not yet reviewed |
| `config/global.yaml` simulation placeholders (32 parameters) | Agent-introduced tier-5 values with named replacement evidence | not yet reviewed |
| `docs/interviews/*`, `docs/reviewer_packets/*`, `reports/*` | Agent-authored templates and skeletons; no entries | not yet reviewed |
| `docs/regulatory/*.md` | Agent-drafted preliminary maps from frozen FDA pages and statute references; legal-status labels are the agent's classification | not yet reviewed; requires HA-31 |

## What the author must be able to explain without the agent

- The central question, the eight hypotheses, the kill criteria, and why the study can end negative.
- Equations 1-11 and B1-B10, including why cost per unit divides by delivered nonexpired units and why an ICER is never shown for a dominated strategy.
- Why regulatory gates are binary and UNCERTAIN is never PASS.
- The daily event order, the mass-balance identity, and how common random numbers pair strategies.
- Why the conformal benchmark supports stop-the-line detection and not automated release (released fraction 1.1%, conditional coverage 32.6% over 23 seeds).
- Every tier-5 input still in the model and what evidence replaces it.

## Ground rules the agent followed

- No numbers invented to fill a blank; placeholders are typed and counted.
- No interviews, reviews, quotes, partners, customers, or regulatory opinions fabricated.
- Existing repository files were not modified or deleted; audits ran on scratch copies.

## Session 2 (2026-09-02, design-space assignment)

- Orchestration: one main agent with forked and fresh subagents (test writing, Phase G, privacy and claims tracks, evidence sweep, decomposition writing) and adversarial verification passes on every document; a session rate limit interrupted 43 agents once, all resumed from cached results.
- Web evidence: every source in `docs/design_space/prior_art/` and `landscape/` carries a verification flag; `fetched_quoted` rows were re-fetched by a separate verifier agent and quotes checked verbatim; failures were removed or downgraded.
- Nothing outside `feasibility/` was modified; no commit, push, history rewrite, or publication was made; the founder's blanket permission is recorded as D018.
- Verification pass (2026-09-03, revision R007): an adversarial review of the Phase D configuration returned 34 findings (4 blockers, 15 majors, 15 minors); the agent applied every blocker and major, took all fifteen minors, and re-ran the two blocker-linked falsification tests at n = 25. Two findings were verified against the code before being acted on rather than accepted as written, and one proposed fix was implemented differently after measurement showed the suggested form did not restore the mechanism (see the MD-19 row in the decomposition). No finding was satisfied by weakening a prohibition.


- Route screen and its audit (2026-09-06, model Claude Opus 5): an agent built `docs/route_screen/` (method frozen before evidence gathering, four evidence stages, a 13-row CSV register and a results narrative) from public sources only, then a separate adversarial audit of that pass returned 40 findings (5 blockers, 20 majors, 15 minors) and a fix pass applied every blocker and major. Every determination that moved, moved **down**: no confidence was raised anywhere in the fix pass, by construction. Sixteen quoted figures, source ids and set ids were re-fetched and checked verbatim during the fix, including three FDA PDFs, a Form FDA 483, an MHRA certificate, an MHRA public assessment report, two DailyMed SPLs, a granted US patent and the openFDA label API; four claims did not survive re-checking and are corrected in place with the failed figure named rather than deleted. Nothing was fabricated and nothing outside `feasibility/` was modified.
