# Architecture design

Status: design baseline for package v0.1 (2026-09-01). Every module listed here is either implemented under `src/telo_feasibility/` or marked *planned* in `docs/audits/04_phased_plan.md`. This document describes mechanisms, not intentions; if the code and this file disagree, the code is wrong or this file is stale, and either way it is a defect to fix.

## 1. Design principles

1. **Protocol is data.** `protocol/protocol.yaml` is loaded and validated at start of every command. Thresholds, gates, weights, and decision classes are read from it, never hard-coded.
2. **Provenance or it does not load.** Every parameter is an `UncertainParameter` with source, access date, evidence tier, confidence, and validation status. Tier-5 (illustrative) values load only when the run is explicitly tagged `illustrative`, and every output produced from them carries the banner `PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS`.
3. **Gates are binary and default to UNCERTAIN.** `regulatory.py` maps strategy to `ELIGIBLE`, `EXCLUDED`, or `NO_CONCLUSION`. `NO_CONCLUSION` strategies may be simulated for information but are excluded from any favorable decision class. There is no penalty cost path.
4. **One exogenous world per run.** All randomness that does not depend on the strategy is generated once per run from named, seeded substreams keyed by stable entity ids. Strategies consume the same world (common random numbers). Strategy-dependent randomness (e.g., a batch's yield at a node that exists only in S5) is keyed by the node id and batch ordinal so it is reproducible and identical wherever the same node/batch exists.
5. **Transparent engine.** A daily discrete-time loop in plain Python with numpy for arrays. No simulation framework. Every day executes the nine protocol steps in order and ends with invariant assertions.
6. **Separate concepts stay separate.** Production cost, reimbursement, market price, willingness to pay, and provider shortage cost are distinct fields; the code never adds them together.
7. **Nothing fabricated.** Interview logs, reviews, quotes, and commitments are typed placeholders with `status: pending` until real. The CLI `status` command lists exactly which definition-of-finished tests remain incomplete.

## 2. Package map

| Module | Responsibility | Key types / functions |
|---|---|---|
| `schemas.py` | Pydantic v2 models for every entity, parameter, gate, config, manifest, and result; unit and range validation | `ProductPresentation`, `Supplier`, `Component`, `ManufacturingSite`, `Batch`, `InventoryLot`, `DemandRegion`, `TransportLane`, `DisruptionEvent`, `RegulatoryGate`, `StrategyDesign`, `SimulationConfig`, `UncertainParameter`, `EvidenceSource`, `RunManifest`, `ResultRecord`, `Protocol` |
| `provenance.py` | Source registry, snapshot manifests, hashing, run manifests, environment capture | `SnapshotManifest`, `hash_file`, `build_run_manifest`, `verify_protocol_hashes` |
| `product_selection.py` | Longlist from frozen snapshots, hard gates, weighted score with per-criterion evidence, dossier writer | `apply_hard_gates`, `score_candidates`, `build_dossier` |
| `regulatory.py` | Gate loading, per-strategy eligibility, 503B state machine, legal-status labels | `GateSet`, `Eligibility`, `evaluate_strategy`, `Shortage503BState` |
| `network.py` | Topology: regions, sites, suppliers, components, lanes, common-cause groups; dependency graph | `NetworkTopology`, `CommonCauseGroup`, `build_topology` |
| `demand.py` | Routine demand process (lognormal AR(1), negative binomial, block bootstrap), seasonality, regional shares, shocks, contracted vs potential demand, substitution | `DemandModel`, `generate_demand_paths`, `ShockProcess` |
| `suppliers.py` | Purchase orders, lead times, supplier disruption impact, qualification lead time | `SupplierState`, `PurchaseOrder`, `advance_supply` |
| `production.py` | Site state (uptime, campaign, changeover), batch lifecycle, capacity, yield sampling | `SiteState`, `BatchState`, `advance_production` |
| `quality.py` | Deviations, rejection, investigation, testing/release queue, holds | `QualityState`, `advance_release_queue` |
| `release_assurance.py` | R0-R3 scenarios, abstention and fallback, R3 gate enforcement, risk-coverage parameters imported from benchmark results | `ReleaseAssuranceScenario`, `apply_release_assurance` |
| `inventory.py` | Expiry cohorts, FEFO, policies (days-of-supply, reorder point, order-up-to), rotation, transfers, holds | `InventoryBook`, `fefo_issue`, `expire`, `InventoryPolicy` |
| `allocation.py` | Proportional, criticality-weighted, minimum-guarantee, optimization-based (LP) allocation; equity metrics | `allocate`, `AllocationPolicy` |
| `disruptions.py` | Exogenous world generation: site failures, supplier disruptions, common-cause events, regulatory transitions, transport delays, demand shocks | `ExogenousWorld`, `generate_world` |
| `economics.py` | Cost ledgers, CRF, annualization, break-even, resilience premium, ICER, dominance | `CostLedger`, `crf`, `icer`, `dominance_table` |
| `deterministic.py` | Protocol Eq. 1-7 screening model; strategy rows; reconciliation with the workbook | `run_screen`, `reconcile_with_workbook` |
| `workbook.py` | Read the Excel scaffold (formulas and cached values) into typed inputs; cell map | `load_workbook_inputs`, `workbook_cached_outputs` |
| `strategies.py` | S0-S7 designs from config, design-variable bounds, strategy-specific policies | `StrategyDesign`, `build_strategy` |
| `simulation.py` | Daily engine, state, nine-step order, invariants, event log, tidy results, paired runs | `SimulationState`, `simulate_run`, `run_paired` |
| `optimization.py` | Per-strategy constrained minimization with auditable grid plus local refinement; convergence and budget records | `optimize_strategy`, `OptimizationRecord` |
| `sensitivity.py` | One-way thresholds, Sobol (SALib), PRCC, structural alternatives, decision-reversal maps, EVPI/EVPPI | `one_way`, `sobol`, `prcc`, `decision_reversal_map`, `evpi` |
| `backcast.py` | Episode definitions, information freeze, simulate-vs-observed comparison | `Episode`, `backcast` |
| `validation.py` | Invariant checks and extreme-case runners used by tests and the CLI | `check_mass_balance`, `extreme_cases` |
| `reporting.py` | Figures and tables with required metadata, markdown reports, banner logic, definition-of-finished status | `figure`, `build_reports`, `finished_status` |
| `cli.py` | argparse entry point wrapping the scripts | `main` |

## 3. Entity model

```
ProductPresentation (exact: ingredient, strength, form, route, container, fill, label, pathway)
  |-- Component[]        (API, excipient, vial, stopper, seal, label, packaging) -> Supplier[]
  |-- StabilityProfile    (shelf life, storage, BUD for 503B)
NetworkTopology
  |-- DemandRegion[]      (share, criticality weight, hospital classes optional)
  |-- ManufacturingSite[] (archetype, capacity, batch size, uptime, campaign rules, pathway state)
  |-- Supplier[]          (component, lead time, capacity, qualification state)
  |-- TransportLane[]     (site/DC -> region, days, emergency option)
  |-- CommonCauseGroup[]  (member ids: sites, suppliers, methods, software, geography, ownership, regulatory)
StrategyDesign (S0-S7 + design variables + policies + release scenario)
SimulationConfig (horizon, warm-up, N runs, streams, thresholds from protocol)
```

Every entity has a stable string id. Ids are the keys for random substreams, so adding an entity never perturbs another entity's draws.

## 4. Randomness and common random numbers

- Master seed -> `numpy.random.SeedSequence(master_seed)`.
- Per run *r*: `run_seq = master.spawn(N)[r]`.
- Per stream *s* (routine_demand, demand_shocks, site_failures, supplier_disruptions, common_cause_events, yield, deviations, batch_rejection, release_time, transport_delay, regulatory_state_transitions): `stream_seq = SeedSequence(entropy=run_seq.entropy, spawn_key=(STREAM_INDEX[s],))`.
- Per entity *e* within a stream: `SeedSequence(entropy=run_seq.entropy, spawn_key=(STREAM_INDEX[s], stable_hash(e)))`. `stable_hash` is BLAKE2b of the entity id, truncated to 64 bits, so it is stable across processes and Python versions.
- Exogenous streams (demand, shocks, site failures, supplier disruptions, common cause, regulatory, transport) are materialized once per run into an `ExogenousWorld` object covering the *universal entity roster* (every site/supplier/lane that any strategy can instantiate). A strategy consumes the subset it uses.
- Endogenous streams (yield, deviations, rejection, release time) are drawn lazily but keyed by (entity id, batch ordinal), so two strategies that produce the k-th batch at the same site see the same draw.
- Tests: `test_seed_reproduction` (identical config + seed -> identical event-log hash), `test_crn_pairing` (paired strategies receive identical exogenous events by run), `test_entity_isolation` (adding a site does not change another site's failure times).

## 5. Daily engine

State per run-strategy: inventory book (lots by product, location, status, expiry day), backlog by region, raw-material inventory and open POs by site, site states, batch queues (setup, production, inspection, testing, investigation, release), transport in transit, disruption states, regulatory state, cost ledger, counters.

Order each day (protocol 7.2), implemented as separate functions so tests can call them individually:

1. `expire_inventory` (FEFO cohorts; counts expired units)
2. `advance_demand` (routine + active shocks; contracted vs potential split)
3. `advance_disruptions` (site, supplier, common cause, regulatory, transport)
4. `receive` (POs and released batches whose lead times complete)
5. `allocate_and_serve` (policy; records served, backorders, unmet, shortage flag per region)
6. `advance_queues` (setup -> production -> inspection -> testing -> investigation -> release; yield, rejection, release time, release-assurance abstention)
7. `trigger_policies` (reorder, campaign start, emergency transfer, reserved-capacity activation, 503B activation when eligible)
8. `accrue_costs_and_log`
9. `assert_invariants` (mass balance, nonnegativity, regulatory eligibility)

Mass balance per product: `on_hand[t] = on_hand[t-1] + released_receipts - shipments - expired - holds + hold_releases`, and cumulative `produced = released + rejected + held + in_process`. Assertion tolerance is exact integer units.

Tracked separately: produced, released, held, rejected, expired, shipped, fulfilled demand, backlog, lost/substituted demand.

## 6. Strategy representation

S0-S6 use the approved/CMO pathway; S7 is 503B with a time-varying eligibility state driven by the shortage-list state in the exogenous world and gates G08-G12. A strategy that does not exist on day zero (new site, new supplier qualification, reserved-capacity qualification) carries a commissioning lead time during which it contributes nothing but cost, per fair-comparison rule FC4.

Design variables per strategy follow `protocol.yaml` `strategies[*].design_variables`; bounds live in `config/strategies/*.yaml`.

## 7. Release-assurance submodel

- R0 default. R1 reduces only the administrative component of release time by a measured fraction (parameter with provenance; illustrative until measured). R2 changes nothing in release time; it adds detection events (used for reporting only). R3 reduces only the named validated component and only when gate G15 = PASS and the strategy's gates pass; abstention sends the batch to the conventional testing and investigation queue, adding fallback time. The sterility, endotoxin, compendial, disposition, investigation, validation, and change-control components are never reducible by any scenario (enforced in code by a whitelist of reducible components).
- Parameters: released fraction, conditional error among released, false-hold rate, and their dependence on shift state come from `results/release_assurance/` benchmark outputs with a manifest, or from tier-5 placeholders tagged illustrative.
- Test: total abstention yields no release-time benefit and shows fallback burden; zero-benefit parameters reduce R1-R3 exactly to R0.

## 8. Deterministic screen and workbook reconciliation

`deterministic.py` implements Eq. 1-7 and the workbook's 22-column strategy row exactly as the workbook computes them (so reconciliation is meaningful), plus a *corrected* variant that fixes documented workbook defects (validation annualization, expiry double count, testing batches net of yield, cost-per-unit denominator). `reconcile_with_workbook` compares the Python replica against cached workbook values cell by cell with a tolerance of 1e-9 relative and reports every difference, then reports the corrected-variant deltas separately so the two are never confused.

## 9. Optimization

Sample-average approximation on a fixed common-random-number batch. Stage 1: coarse full-factorial grid over discretized design variables (auditable; every point stored). Stage 2: local refinement (Nelder-Mead on continuous variables, neighborhood search on integers) from the best feasible grid points. Stage 3: re-evaluate the final designs on the full run set and report Monte Carlo standard errors. Constraints from protocol `service_thresholds`; infeasible points are never assigned a penalty and never enter the frontier. Records: bounds, seeds, evaluations, convergence, violations, wall time.

## 10. Sensitivity and value of information

- One-way thresholds on the mandatory input set with decision-reversal detection.
- Sobol indices via SALib Saltelli sampling on the simulator with reduced N per point and CRN; PRCC computed in-package on the same samples where monotone.
- Structural alternatives run as separate configurations with identical seeds.
- Feasibility map: grid over utilization x release time x common-cause dependence, coloring the minimum-cost eligible strategy, with gate-masked regions.
- EVPI from the decision-analytic definition over the probabilistic sensitivity sample; EVPPI by regression (Strong, Oakley, Brennan 2014) on the same sample.

## 11. Results and provenance

Every run writes `results/manifests/<run_id>.json` (protocol version and hash, config hashes, package version, git commit, python/platform, seeds, N, wall time, gate outcomes, illustrative flag) and tidy tables (one row per run-product-strategy) as parquet plus a CSV summary. Figures embed the run id, product, scenario, source note, and decision caption.

## 12. Testing strategy

- Unit: schemas (unit/range validation failures), provenance hashing, CRF, FEFO, allocation policies, demand moments, gate logic (UNCERTAIN never PASS), release-assurance whitelist.
- Integration: full daily engine on tiny topologies for the protocol Appendix C cases (zero demand, zero capacity, infinite supply, no failures, perfectly correlated sites, independent sites, zero and infinite shelf life, release assurance off, total abstention), seed reproduction, CRN pairing, cost-ledger reconciliation, strategy dominance, optimization monotonicity.
- Property-based (hypothesis): mass balance and nonnegativity under random policies and random worlds.
- Regression: frozen reference runs with stored hashes; workbook reconciliation.

## 13. Performance budget

Target <= 0.5 s per run-strategy at daily resolution over 2,191 days (365 warm-up + 5 x 365.25) with 4 regions, <= 8 sites, <= 8 suppliers. Runs are embarrassingly parallel across processes (`multiprocessing` with spawn); CRN is preserved because seeds derive from run index, not from process. N is a config value; the protocol's rule (increase N until decision-relevant contrasts stabilize) is enforced by reporting MCSE next to every paired contrast.

## 14. Out of scope by design

Shelved-asset economics, clinical-success prediction, priority-review vouchers, foundation-model sourcing (future-work interface only in `docs/methods/future_work_interface.md`); generalization to excluded modalities.
