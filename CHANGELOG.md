# Changelog

All notable changes to the feasibility study package. Protocol-level changes
are additionally logged in `protocol/revisions.csv`; analysis runs are
identified by manifests in `results/manifests/`.

## [0.5.0-dev] - 2026-09-02 (session 2, in progress)

### Added
- Sterilization-route screen answering HA-34 from public sources: `docs/route_screen/` with `method.md` (frozen before evidence gathering), four evidence stages, `route_determinations.csv` (13 rows, 15 fields) and `route_screen_results.md`; six new falsification rows `F11-ROUTE-01` to `-06` in `docs/design_space/falsification_register.csv`. Result: the US public record does not carry the route per presentation; 5 of 7 in-scope rows are `unknown` and the two modelled product configs are undetermined at any confidence. No model parameter moves. (2026-09-06)


### Changed (2026-09-06, route-screen audit)
- `method.md`: added evidence tier **E7** (registration and listing metadata, ceiling `unknown`, leads only), an explicit fill-volume load-family exception clause in section 5 item 2, and a post-hoc amendment banner recording that these were added after evidence gathering. E7 is strictly tightening and no rule was loosened.
- `route_determinations.csv`: added the four fields `method.md` section 2 requires and the register omitted (`application_holder`, `application_number`, `document_date`, `contradicted`), populated on all 13 rows.
- Confidence downgrades, none raised: furosemide ANDA 202747 `strongly_inferred` to `weakly_inferred` with `contradicted` set, after the Form FDA 483 behind the cited warning letter was read for the first time; B. Braun sodium chloride EXCEL `established` to `strongly_inferred` and re-dated 2023 to 2014; acetazolamide `established` split so the freeze-drying half and the aseptic-fill half carry separate confidences; two `compatible`/`established` chemistry rows in `evidence_03` to `compatible_with_conditions`.
- Three case-against arguments added to the route-dataset assessment: rapid microbiological methods reach the same release pole; Telo holds no application and so cannot act on the dataset; every input is a free public register, so the dataset cannot be owned.

### Fixed (2026-09-06, route-screen audit)
- Non-reproducible counts corrected against their cited sources: openFDA negative-phrase hits (eight to 4 exact / 12 loose), S18 snapshot rows (916 to 520 held of 1,061 reported), acyclovir applications (7 to 6), sterile-water applications (9 to 8), and the corpus arithmetic now reconciles to 50.
- The claim that Drugs@FDA holds zero `Review`-type documents for every candidate application was false on the frozen S16 snapshot cited for it; three exist (NDA 007513, ANDA 074930, ANDA 200880), all were fetched, none carries a route statement, and the claim is narrowed to "no published chemistry or product-quality review".
- Superseded ablation figures relabelled: `bounds:ss365+base_stock` 13 of 16 (pre-R004) to 11 of 16 on `abl_post_R008`, with the supersession warning carried at every occurrence.
- Draft status restored to the 503B Appendix B Table D dating lever (nonbinding, "Draft - Not for Implementation"), and its confinement to the time-varying 503B state stated.
- Source-provenance repairs under `method.md` rule 8: `RS2-S08` given its URL, `RS2-S10` marked unusable as cited, `E01-S08` resolved to two named certificates, a new `E01-S09` for the public-assessment-report quote (which describes a solvent, not a drug product), and truncated DailyMed set ids written in full.
- A negative asserted in `evidence_03` as fetched ("a morphine SPL contains no sterilization or autoclave statement") is false; the label reads "Do not autoclave."
- The tier-5-driven percentage in the release-decomposition table withdrawn, per `CLAUDE.md`'s rule against presenting tier-5-driven outputs as findings.
- Phase A failure decomposition by ablation: `ablation.py` (22 factors as parameter, design-variable, and settings overrides; leave-one-out and add-one-in configurations on common random numbers; attribution table with Shapley brackets), `scripts/run_ablation.py`, `scripts/build_ablation_figures.py`, `scripts/build_bottleneck_tables.py`, `figures.attribution_bars` and `figures.config_heatmap`; runs `abl_20260902_phaseA` (41 configurations x 100 runs), `abl_20260902_phaseA_mb`, `abl_20260902_phaseA_pairs` (six-factor factorial); 33 unit tests.
- Opt-in strategy design variables that leave S0-S7 byte-identical: `region_base_stock`, `region_reorder_point_days` (regional review rule), `component_lead_fraction`; frozen-digest regression `tests/regression/test_frozen_strategies.py`.
- Design-space engine infrastructure for S8+: `StrategyId` S8-S20, `SitePlanSpec`, `SupplierSpec`, `DesignVariableSpec`, `StrategyProfile`, `configs.load_design_space_strategies` / `load_all_strategies`, configuration-declared topologies in `strategies.build_strategy`, warm-standby exercise batches and activation failure (`RandomStream.ACTIVATION`), hub-as-supplier, portfolio capacity and fixed-cost shares, `optimization.space_for`, unmapped-gate guard in `regulatory` (NO_CONCLUSION when no gate names a strategy); 25 tests; matrix rows R101-R102, R109-R113.
- `product_architecture.py` feature layer for product-architecture matching from the frozen dossiers (5 tests).
- Two opt-in strategy levers for the design-space families, both defaulting to off: `take_or_pay_fraction` (a volume commitment on reserved capacity, charged whether or not the line runs) and `deviation_rate_factor` / `investigation_duration_factor` (an operating-system effect on the quality workflow only); 6 tests; matrix rows R122-R123.
- Deterministic screening for S8+ (`deterministic.screen_inputs`): runtime-derived capacity and cost with a common-impact factor computed from the common-cause groups; the workbook replica refuses a declared topology, so the 448/448 reconciliation is unchanged; 5 tests; matrix row R121.
- `contracting.py`: contract terms with a completeness check over the nine commercial questions, and the volume arithmetic (resilience premium per unit, break-even price, committed volume, take-or-pay share, implied utilization, maximum fixed cost per site); 6 tests; matrix row R120.
- `design_space_analysis.py` (Phase E): feasibility-condition bisection along 30 named inputs, dominance with an explicit cost-noise tolerance, decision-reversal maps over two or three axes; `scripts/run_design_space_analysis.py` and `scripts/build_design_space_figures.py`; 7 tests; matrix rows R116-R119.
- Design-space documents: `docs/design_space/privacy_remediation_plan.md`, `public_claims_corrections.md` (CLAIMS_REGISTER extended to C024), `prior_art/` family notes, `landscape/` category notes.
- Release-assurance benchmark extensions (Phase G): direct standardization and per-wavelength instrument standardization baselines on transfer standards, selective-prediction metrics (AURC, E-AURC, oracle), held-out shift-type protocol, USD operational cost curves with provenance-carrying inputs and the new tier-5 global parameter `wrong_release_cost_usd`, repair with n = 3, R2 per instrument, gate-statistic (`q_residual`) and component-selection options for leakage effect sizes; five 50-seed runs `ra_20260902T2224..2231Z`; `docs/design_space/release_assurance_followup.md` (615-vs-654 audit, claims-to-results map, leakage audit, product answer); 9 unit tests; matrix rows R103-R108. Legacy benchmark keys are bit-identical.

### Changed
- Revisions R009 to R011 fix the six model defects that carried the architecture ranking. **R009 (NEW-1)**: opening inventory is purchased, not inherited, and is charged once at the production unit value into a new `opening_inventory` ledger field; the carrying half stays in `inventory_logistics` and is not double counted. It had been free while its quantity scaled with the design's own stock policy, so a design whose optimum is a year of safety stock was handed that year for nothing. **R010 (MD-3, MD-12, MD-11)**: every frozen comparator now searches the same inventory space the design-space strategies declare, with the previous spaces kept as `LEGACY_DESIGN_SPACES`; and the infeasible tie-break ranks on fill only beyond a noise band derived from the screen size, having previously bought a 9.26M USD/yr cost increase for 0.00004 of fill. **R011 (MD-1, NEW-2, MD-23, MD-24)**: the material policy separates pipeline cover from safety and cycle cover and the opening component position no longer tracks the lead; regions may carry differing criticality weights and minimum guarantees, which is what lets the four allocation policies differ at all; any batch restarts a reserved line's readiness clock; and a take-or-pay commitment buys priority access, which is the only service channel it has. 13 new tests in `tests/integration/test_ranking_defect_fixes.py`; matrix rows R148 to R153; frozen snapshot re-captured with the pre-R009 digest, cost and fill retained.
- Revision R008 (model defect MD-17, found by the Phase B judge panel): a site that does not exist at t0 starts its commissioning clock at the first measured day instead of at simulation day zero, and `capacity_expansion_days` moves from 365 to 270. Three commissioning parameters had coincided with `warm_up_days`, so any lead time at or below a year was served by the warm-up period and cost nothing that the metrics measured. Dual sourcing benefited most: its second source was free inside the window. Every run now reports `capacity_days_lost_to_commissioning_fraction`.
- Revisions R004 and R005 (2026-09-03): the model-defect fixes the Phase A decomposition called for. Capacity above a site's day-zero scale is now an expansion that waits `capacity_expansion_days` before it can run, so enlarging an existing plant and building a new site are compared on the same terms (MD-7; `instant_expansion` restores the old behaviour). Fixed site operations accrue only while a site exists, capital and validation stay sunk from day zero, and backlog still inside its backorder window at the horizon is reported as `open_backlog_units_at_horizon` instead of counted lost (MD-6). Opening stock is seeded as four shelf-life cohorts instead of all at half shelf life, which had put its expiry on the first measured day (MD-4). A reserved line Telo does not own carries only its reservation fee, not capital, fixed operations, and validation as well (MD-14; `reserved_site_owned` models an owned standby line). Also: the material reorder point covers at least one batch draw (MD-2), nodes may exceed the region count (MD-13), the utilization denominator covers the sites the numerator counts (MD-9), the Shapley bracket is undefined rather than zero when an add-one-in arm is absent (MD-10), and `p_meet` carries its binomial standard error (MD-16). Effect on the frozen snapshot: 12 of 32 event digests and 20 of 32 costs change; sodium bicarbonate S4 loses 0.171 fill in run 0 and the reserved-capacity strategy S3 costs about 40% less. 19 tests in `tests/integration/test_model_defect_fixes.py`; matrix rows R126-R130.
- Revision R007 (2026-09-03): verification-pass corrections to the Phase D configuration and three engine defects it exposed. MD-19: a supplier's daily capacity is a fraction, not a switch, so a common-cause group declared on a supplier is no longer structurally inert (a supplier at fraction `f` ships at most `f` of one full order per day, the same proportional stretch a degraded line already applied); frozen S0-S7 service is unchanged, twelve of thirty-two frozen costs move by at most 8.6e-7 relative. MD-20: the deterministic screen credits a reserved line its exercise duty cycle and charges its reservation fee and take-or-pay, so S11, S13, S16, S17 and S19 no longer screen byte-identical to S0; `cmd_deterministic`, `ablation` and `backcast` moved to `load_all_strategies`, so Phase D screening and ablation see S8-S19 at all (the workbook replica keeps the frozen eight and reconciles 448/448 unchanged). MD-21: a reservation fee and a take-or-pay commitment accrue only while the reserved site exists. Configuration: `cc_stopper_1` and `cc_geo_<region>` declared on every site plan of all twelve designs under one stated convention, `cc_quality` added to S9, S10, S11, S14 and S19 where one holder's quality unit performs the non-delegable disposition, `take_or_pay_fraction` removed from the S11 and S13 search blocks (MD-24, no service channel) and swept instead as a labelled contract scenario in `scripts/run_design_space_analysis.py`, the inert `sites` variable deleted from S11, S10's falsification test restated as an internal single-host control. Gate G16 added (component and container-closure lot qualification, plus the alternate API source's Type II DMF letter of authorisation) for S9, S18 and S19, UNCERTAIN. MD-19 to MD-25 recorded in the decomposition; 8 tests in `tests/integration/test_model_defect_fixes.py`; matrix rows R131-R136.
- Revision R003 (MD-1): raw-material stock now carries inventory carrying cost; S0-S7 events unchanged, annual cost +0.10% to +0.36%; frozen snapshot re-captured with `cost_before_R003` retained.
- `Protocol` and `workbook` iterate `FROZEN_STRATEGY_IDS` instead of the enum, which now holds S8-S20.

## [0.4.0] - 2026-09-02

### Added
- `HANDOFF.md`, `CLAUDE.md`, `docs/design_space/ASSIGNMENT.md` for session continuity.
- Release-assurance benchmark package on the frozen IDRC tablet data (S28): three pipeline modes, baselines (no gate, mandatory hold, mean-centering, slope/bias, PDS, recalibrated quantile), synthetic stress tests, label noise, risk-coverage and cost-coverage curves, bootstrap intervals, model card and claims table.
- Optimizer threshold overrides for pre-registered sensitivity values; optimization run at the frozen target for both products (no strategy feasible under illustrative inputs).
- Executive-summary template, paper outline, reproducibility and limitations appendices; candidate non-obvious findings file.

### Changed
- CLAIMS_REGISTER C005/C006 carry the implementation-sensitivity caveat established by the benchmark.

## [0.3.0] - 2026-09-02

### Added
- Stochastic daily network engine with common random numbers, nine-step order, mass-balance assertion; runner with multiprocessing and paired statistics.
- Auditable optimizer (grid + refinement + full-N), sensitivity (one-way, Sobol, PRCC, decision-reversal map, EVPI/EVPPI), backcasting framework with three dated episodes, figure builders with mandatory metadata, report builder.
- Interview infrastructure (matrix, templates, guide, modules, schema, worksheet, workflow) and four reviewer packets; nothing populated.
- 32 simulation parameters introduced as tier-5 placeholders plus 4 release components sourced from the repo memo.
- Tests: 96 (extreme cases, reproducibility, property mass balance, optimization monotonicity, backcast, figures).

### Fixed
- Fill-rate definition (origin-day attribution) and expired-in-transit accounting, both found by tests.

## [0.2.0] - 2026-09-02

### Added
- `src/telo_feasibility/`: schemas, provenance, configs, economics, workbook reader, deterministic screen (replica + corrected), regulatory gate evaluation with R3 lock and 503B state, reporting status, acquisition pipeline, product-selection pipeline, CLI (`protocol verify`, `status`, `deterministic`, `reconcile`, `acquire`, `dossiers`).
- `config/`: global and product parameter sets (all tier 5), strategy baseline, source registry (27 sources), longlist (6 presentations).
- `data/raw_snapshots/`: 41 frozen payloads with per-fetch manifests; 3 human-acquisition tasks.
- `data/product_dossiers/`: six dossiers and `screen_manifest.json`.
- `docs/audits/01-07`, `docs/regulatory/` two decision maps, `docs/methods/product_screen_2026-09-02.md`, `docs/architecture/design.md`.
- Tests: 68 (unit, regression); workbook reconciliation exact.

### Fixed
- FDA shortage CSV export parsing (leading blank line, padded headers).
- Drugs@FDA and Orange Book ingredient matching (exact single-ingredient field match).

## [0.1.0] - 2026-09-01

### Added
- Package skeleton under `feasibility/` inside the Telo repository.
- `protocol/protocol.yaml`, `protocol/hypotheses.yaml`, `protocol/revisions.csv`:
  machine-readable, frozen representation of protocol v1.0 (1 September 2026)
  with source-document hashes.
- `config/regulatory_gates.yaml`: 15 preliminary gates, all `UNCERTAIN`,
  labeled "preliminary regulatory analysis; not legal advice".
- Audit documents under `docs/audits/` (repository audit, workbook audit,
  requirements matrix, inconsistencies, phased plan).

### Status
- PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS. No definition-of-finished gate passes yet.
