# Phased implementation plan with acceptance tests

Each phase ends with `make check` green, the requirements matrix updated, the research and revision logs updated, and a focused commit (when authorized). Phase order follows the task's first milestone, then the protocol's execution sequence (13.1).

## Phase 0: audit and freeze (this session)

Deliverables: `docs/audits/01-06`, `protocol/protocol.yaml` v1.0.0, `protocol/hypotheses.yaml`, `protocol/revisions.csv`, `config/regulatory_gates.yaml`, package skeleton, integrity files.

Acceptance: protocol YAML parses and its weights sum to 1.0; 15 gates load with status UNCERTAIN; source-document hashes in the YAML match the files in `~/Downloads`; every audit claim cites a file, cell, or key.

## Phase 1: schemas, provenance, deterministic replica, reconciliation

Modules: `schemas.py`, `provenance.py`, `workbook.py`, `deterministic.py`, `economics.py` (CRF, ledgers), `cli.py` (`protocol verify`, `status`, `deterministic`, `reconcile`).

Acceptance tests:
- `tests/unit/test_schemas.py`: probability outside [0,1], negative cost, impossible access date, missing provenance, unit mismatch (days vs months), and an UNCERTAIN gate passed as PASS each raise `ValidationError`.
- `tests/unit/test_economics.py`: CRF(0.10, 10) = 0.162745 (workbook C25 to 5 dp); CRF(0.06, 15) and CRF(0.15, 7) match B25 and D25.
- `tests/regression/test_workbook_reconciliation.py`: replica reproduces all 320 cached values of 09_Deterministic and the 160 of 12_Results within tolerance; corrected variant differs only in the documented cells (WB-01, WB-18 to WB-21) and the deltas are reported.
- `make status` lists all 22 definition-of-finished tests as incomplete and counts tier-5 parameters.

## Phase 2: source acquisition, product screen, dossiers

Modules: `scripts/acquire_sources.py`, `product_selection.py`, `scripts/build_product_dossiers.py`, `regulatory.py` (gate loading, eligibility, 503B state machine).

Acceptance tests:
- Every snapshot has retrieval timestamp, URL, HTTP status, sha256, license note, raw file, transformation script, processed table, and data-dictionary rows; a snapshot missing any field fails to register.
- Sources that cannot be fetched legally or technically produce a human-acquisition task, not an error and not a fabricated file.
- Longlist has >= 5 exact presentations with dated official status; hard gates evaluated with status and evidence per gate; UNCERTAIN blocks selection; weighted score reproduces the protocol weights; per-criterion evidence, confidence, and disagreement fields populated or explicitly empty.
- `regulatory.evaluate_strategy` returns EXCLUDED on any FAIL, NO_CONCLUSION on any UNCERTAIN, ELIGIBLE only when all applicable gates PASS; property test: no combination of statuses containing UNCERTAIN yields ELIGIBLE.

## Phase 3: stochastic network simulation

Modules: `network.py`, `demand.py`, `suppliers.py`, `production.py`, `quality.py`, `inventory.py`, `allocation.py`, `disruptions.py`, `release_assurance.py`, `strategies.py`, `simulation.py`, `validation.py`, `scripts/run_simulation.py`.

Acceptance tests (protocol Appendix C plus task section 21):
- Exact mass balance every day (property-based over random worlds and policies); nonnegative state.
- Zero demand: no shortage, no variable production, fixed cost unchanged. Zero capacity: no production; results depend only on initial stock. Infinite supply: fill rate -> 1, shortage days -> 0. No failures: stochastic throughput equals deterministic within sampling tolerance.
- Perfectly correlated sites: extra sites add no failure resilience. Independent sites: reliability improves with redundancy.
- Zero shelf life: stockpiling infeasible / high waste. Infinite shelf life: zero expiry, carrying cost remains.
- Release assurance off: R1-R3 reduce exactly to R0. Total abstention: no wrong automated release and no release-time benefit; fallback burden appears.
- Seed reproduction: identical config + seed -> identical event-log hash. Common random numbers: paired strategies receive identical exogenous events; adding an entity does not change others' draws.
- Cost-ledger reconciliation: sum of daily accruals equals ledger totals; no double counting across ledgers.
- Recovery metrics computed per the frozen definition (30-day sustained window).

## Phase 4: economics, optimization, outputs

Modules: `economics.py` (complete), `optimization.py`, `reporting.py` (tables), `scripts/optimize_strategies.py`.

Acceptance tests: relaxing a constraint never worsens the optimum beyond tolerance; strategy dominance detected and ICER suppressed for dominated strategies; every output in protocol 10.2 present with mean, median, quantiles, MCSE, and paired differences; optimization record contains bounds, seeds, evaluations, convergence, violations, wall time; grid cross-check agrees with refined optimum within the grid resolution.

## Phase 5: sensitivity, structural uncertainty, value of information

Modules: `sensitivity.py`, `scripts/run_sensitivity.py`.

Acceptance tests: one-way thresholds for every mandatory input; Sobol indices on a test function match analytic values; PRCC monotonicity check; structural alternatives run with identical seeds; decision-reversal map produced; EVPI >= 0 and EVPPI <= EVPI for every parameter.

## Phase 6: backcasting

Modules: `backcast.py`, `data/historical_backcasts/`, `scripts/run_backcasts.py`.

Acceptance tests: at least four episode classes configured (site failure, upstream/common cause, demand shock, resolved shortage) with information frozen at episode start; comparison tables for duration, severity, recovery shape, bottleneck, regional effects; every material mismatch logged with the resulting revision.

## Phase 7: release-assurance benchmark package

Separate package with grouped splits, calibration-transfer/standardization/domain-adaptation/conformal/mandatory-hold baselines, unknown-shift and sensor-fault and label-noise stress tests, repair curves, risk-coverage and cost-coverage curves, bootstrap intervals, a model card, and a claims table; results pinned to commit and hash.

Acceptance tests: all twelve jointly-reported metrics present for every configuration; total-abstention and zero-shift controls behave as expected; every headline number has an interval.

## Phase 8: interviews, review packets, reporting

Deliverables: interview target matrix, guides, consent and evidence schemas, reviewer packets (4), revision-log schema, automated report build with the preliminary banner.

Acceptance tests: templates contain no completed entries; report build fails if any figure lacks title, axes with units, product/scenario, manifest id, source note, or decision caption; banner present until `finished_status()` returns complete.

## Progress (2026-09-02)

Phases 0-3 implemented and tested (100 tests). Phase 4 optimizer implemented and run (no feasible strategy at the frozen target under illustrative inputs). Phase 5 sensitivity implemented and run at modest sizes. Phase 6 framework implemented with three dated ongoing episodes and one template. Phase 7 benchmark package implemented and run in three modes. Phase 8 infrastructure written; report builder runs. What remains is evidence, not code: see the human-action queue.

## Human-action queue (cannot be automated)

See `docs/audits/07_human_action_queue.md`.
