# Working rules: Telo feasibility package (`~/telo/feasibility/`)

Read `HANDOFF.md` first; it holds the state and pointers. These rules apply to every session working in this directory. They inherit the repository's `../CLAUDE.md` ground rules (SOTA or don't ship, thorough over fast, no slop, clean repo, say plainly when the work isn't there).

- The frozen protocol (`protocol/protocol.yaml` v1.0.0) governs. Decision-relevant changes need a `protocol/revisions.csv` row and a version bump.
- Every numeric input is an `UncertainParameter` with provenance and tier; tier 5 (illustrative) is allowed only for scaffold testing and is counted by `make status`. Never present tier-5-driven outputs as findings; keep the banner `PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS` until the definition-of-finished tests pass.
- Regulatory gates (`config/regulatory_gates.yaml`) are binary constraints. UNCERTAIN is never PASS. No penalty-cost path. R3 release assurance stays disabled unless gates permit. 503B is a time-varying state, never a permanent pathway.
- Reimbursement, market price, willingness to pay, provider harm, and production cost are separate concepts; CMS ASP and Part B are proxies only.
- Nothing fabricated: interviews, reviews, quotes, partners, customers, commitments, regulatory opinions. Templates stay empty until real. Record human-dependent items in `docs/audits/07_human_action_queue.md` with role, question, field, evidence, model entry point, and reversible result.
- Claims: apply the claim-discipline table in `protocol.yaml`; log public-claim status in `CLAIMS_REGISTER.csv`; no novelty claims without a prior-art search.
- Comparators S0-S7 are frozen; new architectures get S8+ ids in new config files; every new mechanism gets tests (unit + the relevant Appendix C extreme cases) and a matrix row in `docs/audits/04_requirements_matrix.csv`.
- Reproducibility: results only through scripts that write run manifests (`results/manifests/`); seeds via `rng.RunStreams`; figures only through `figures.save_figure` (refuses missing metadata).
- Before saying a phase is done: `make check` (ruff, mypy --strict, tests), `scripts/run_tests_report.py`, `make status`, update `RESEARCH_LOG.md`, `CHANGELOG.md`, `AI_ASSISTANCE.md`, the requirements matrix, and the human-action queue.
- Repository hygiene: do not modify, delete, or commit anything outside `feasibility/`; do not commit inside it without explicit authorization (HA-05); never rewrite history; large re-fetchable archives stay ignored with manifests tracked.
- Tooling: if the editing MCP tool is capped, write files with shell heredocs or Python patch scripts, then verify the patch landed (grep the symbol) because `ruff format` reflows anchors. Long jobs: `nohup` with logs under `results/manifests/logs/`.
- Voice: plain, sourced, no hype, no em-dashes; say what is weak.
