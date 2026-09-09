# Telo feasibility study

**Status: PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Run `make status` for the definition-of-finished gate list (8 of 22 at 2026-09-02: dated screen, eight strategies represented, optimization run, pathway maps, workbook reconciliation, engine tests, common random numbers, common-cause failures). Every numeric input except four release-time components is illustrative; all regulatory gates are unresolved; no interview or review has occurred.

This directory is a self-contained research package inside the Telo repository. It implements the frozen protocol *Distributed Sterile-Injectable Manufacturing Under Real-World Constraints* (v1.0, 1 September 2026) as reproducible code, configuration, tests, and reports.

Central question (protocol/protocol.yaml):

> Under what product, demand, regulatory, and operating conditions can distributed regional capacity reduce sterile-injectable shortages more cost-effectively than additional safety stock, dual sourcing, reserved contract capacity, or additional centralized capacity?

The study is designed to permit a negative conclusion. It can find that distributed capacity works only narrowly, is dominated by another intervention, or is infeasible.

## What is here

| Path | Contents |
|---|---|
| `protocol/` | Frozen protocol (`protocol.yaml`), hypotheses H1-H8, revision log with source-document hashes |
| `config/` | Regulatory gates (all `UNCERTAIN` until qualified review), product and strategy configurations, simulation and sensitivity settings |
| `src/telo_feasibility/` | Typed schemas, provenance, product selection, regulatory gates, deterministic screen, stochastic network simulation, optimization, sensitivity, backcasting, reporting |
| `scripts/` | Entry points: acquire sources, build dossiers, run deterministic/simulation/optimization/sensitivity/backcasts, build report |
| `data/` | Frozen raw snapshots with manifests, processed tables, product dossiers, interview and elicitation evidence (empty until real) |
| `tests/` | Unit, integration, regression tests; property-based invariants |
| `results/` | Run manifests and outputs (every figure carries its manifest id) |
| `reports/` | Paper, executive summary, appendices; rendered output is regenerated |
| `docs/audits/` | Repository audit, workbook audit, requirements matrix, inconsistencies, phased plan |
| `docs/regulatory/` | Preliminary decision maps (not legal advice) |
| `docs/methods/` | Product screen (dated), simulation, optimization, sensitivity, release benchmark methods |
| `docs/interviews/`, `docs/reviewer_packets/` | Interview and review infrastructure; no fabricated entries |

Integrity records live at the package root: `RESEARCH_LOG.md`, `DECISIONS.md`, `ASSUMPTIONS.md`, `AI_ASSISTANCE.md`, `CLAIMS_REGISTER.csv`.

## Running

```
make env          # uv sync --all-extras
make check        # ruff + mypy --strict + pytest
make status       # which definition-of-finished gates remain incomplete
make reconcile    # deterministic screen vs the Excel workbook
```

Python 3.11+ (locked with 3.12). Dependencies are pinned in `uv.lock`.

## Evidence and claim rules

- Every parameter carries provenance (source, access date, tier, confidence). Illustrative (tier 5) inputs are allowed only for scaffold testing and are counted by `make status`.
- Regulatory gates are binary. `UNCERTAIN` is never treated as `PASS`.
- The release-assurance scenario R3 is disabled by default and cannot be enabled unless its gates pass.
- CMS reimbursement and ASP data are utilization or price proxies, never manufacturing cost.
- Interviews, reviews, quotes, and commitments are logged only when they actually happened.

See `protocol/protocol.yaml` (`claim_discipline`) for the wording rules that apply to anything external.
