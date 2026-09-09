# Handoff: Telo feasibility package (state at 2026-09-02, end of session 1)

Read this first in a new session. It is the single document that says where everything is, what is real, what is illustrative, how the work was done, and what comes next. Working rules for any session are in `CLAUDE.md` in this directory; the next assignment is stored verbatim in `docs/design_space/ASSIGNMENT.md`.

## 1. Where things are

| Item | Path |
|---|---|
| Package root | `~/telo/feasibility/` (subproject of the Telo repo; own `pyproject.toml`, `uv.lock`, Python 3.12) |
| Frozen protocol | `protocol/protocol.yaml` v1.0.0, `protocol/hypotheses.yaml`, `protocol/revisions.csv` (R000-R002), source docs under `protocol/source/` with hashes |
| Configs | `config/global.yaml` (15 workbook + 32 study placeholders, tier 5, plus 4 sourced release components), `config/products/*.yaml` (2 provisional products), `config/strategies/illustrative_baseline.yaml` (S0-S7), `config/regulatory_gates.yaml` (15 gates, all UNCERTAIN), `config/sources.yaml` (28 sources), `config/longlist.yaml` (6 presentations), `config/simulation.yaml` |
| Code | `src/telo_feasibility/`: schemas, provenance, configs, economics, workbook, deterministic, regulatory, acquire, product_selection, rng, disruptions, demand, inventory, allocation, suppliers, production, quality, release_assurance, strategies, simulation, runner, optimization, sensitivity, backcast, figures, release_benchmark, reporting, cli |
| Scripts | `scripts/`: acquire_sources, build_product_dossiers, run_deterministic (+ `--reconcile`), run_simulation, optimize_strategies (`--tau/--q` sensitivity overrides), run_sensitivity, run_backcasts, run_release_benchmark, build_report, run_tests_report |
| Tests | `tests/unit`, `tests/integration`, `tests/regression`; 100 pass; `make check` = ruff + mypy --strict + tests |
| Data | `data/raw_snapshots/<source>/<date>/` (42 payloads, per-fetch `*.manifest.json`; zips/mat re-fetchable), `data/product_dossiers/` (6 + `screen_manifest.json`), `data/historical_backcasts/episodes.yaml`, `data/data_dictionary.csv` |
| Results | `results/deterministic/` (replica + corrected CSVs, `reconciliation.json` 448/448), `results/simulation/sim_20260902T043039Z/` (100 runs), `results/optimization/opt_20260902T043854Z/` (frozen target) and `opt_20260902T050443Z_tau0.98/`, `results/sensitivity/` (one_way, decision_reversal, global, voi, summary), `results/backcasts/back_20260902T044015Z/`, `results/release_assurance/ra_20260902T044654Z` (CV components), `ra_20260902T044739Z` (8 comps, no scaling), `ra_20260902T045127Z` (reproduction mode), `results/figures/`, `results/manifests/` (run manifests, `test_report.json`, `nonobvious_finding_candidates.json`, logs) |
| Reports and docs | `reports/rendered/results_report.md` (auto-built), `reports/executive_summary/`, `reports/paper/outline.md`, `reports/appendices/{reproducibility,limitations}.md`; `docs/audits/01-07`; `docs/architecture/design.md`; `docs/methods/{product_screen_2026-09-02,simulation,optimization,sensitivity,release_benchmark,future_work_interface}.md`; `docs/regulatory/{approved_generic_cmo_map,503b_shortage_response_map}.md`; `docs/interviews/`, `docs/reviewer_packets/` (infrastructure only, nothing populated) |
| Integrity files | `RESEARCH_LOG.md`, `DECISIONS.md` (D001-D015), `ASSUMPTIONS.md`, `AI_ASSISTANCE.md`, `CLAIMS_REGISTER.csv` (C001-C010), `CHANGELOG.md` (0.4.0) |

`make status` prints the definition-of-finished list: 10 of 22 pass (DF02 dated screen, DF05 eight strategies, DF06 optimization run, DF07 pathway maps, DF11 workbook reconciliation, DF12-14 tests/CRN/common cause, DF16-17 sensitivity and VOI). Everything else waits on human evidence or founder decisions.

## 2. What is real and what is illustrative

Real (tier 1-4, cite by snapshot): FDA shortage export (S01, 2026-09-02), openFDA bulk, Drugs@FDA, Orange Book, DailyMed queries, 503B bulks list, CMS Part B (proxy only), FR 2026-14073 record, GovInfo CFR XML, GAO/DSTF PDFs, USASpending awards, IDRC tablet data (S28), and four release-time components from `regulatory/release-constraints.md`.

Illustrative (tier 5): every other numeric input, including all demand, batch, yield, cost, disruption-rate, and policy parameters. Every simulation, optimization, sensitivity, and backcast output therefore carries `PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS` and describes model behavior, not the world.

Reproducible facts established this session (usable externally with their pointers):
- Workbook replica reconciles 448/448 cells; the workbook's defects are listed in `docs/audits/02_workbook_audit.md` (WB-01 to WB-31).
- `research/conformal/experiment_tablet.py` reproduces byte-for-byte; the "32.6% conditional coverage" is a mean over 23 of 200 seeds; no intervals in the source.
- Independent benchmark (S28): the repo's stop-the-line headline reproduces only with 8 PLS components plus per-wavelength standardization (shifted coverage 0.41 [0.33, 0.49], 1.0% released [0.1%, 2.7%]); without that standardization coverage is 0.77 and 30-40% released; CV-selected components give 56% released at 29% conditional error. In no mode is the gate operationally useful under shift (`docs/methods/release_benchmark.md`, candidate finding NF-1).
- Product screen: sodium bicarbonate 19 FDA rows current since 2017-03-01, 13 injectable holders, not on the 503B bulks list; furosemide 33 rows since 2020-04-07; sterile water 21 rows since 2021-11-23; norepinephrine, acyclovir, acetazolamide 0 rows; acetazolamide fails the archetype gate (lyophilized).
- Phlow contract: USASpending 75A50120C00092 shows $696,665,953.98; the press release says up to $812 M.

Model behavior under illustrative inputs (never present as findings):
- Frozen target (mean fill >= 0.99, 90% of runs): no strategy feasible for either product; tail constraint binds; safety-stock designs at their search bound. At tau = 0.98 only S2 (dual source) clears for both products.
- A fully validated chemical release layer saves zero release days while the 14-day sterility incubation binds (test `test_full_release_assurance_saves_no_days_when_sterility_binds`).
- Sobol total-order on the S5-minus-S4 cost: node_scale 0.86, fixed QA labor 0.11; EVPI 4.8 M USD/yr (artifacts of tier-5 ranges).
- Backcasts of the three ongoing shortages are "consistent" only because a 124%-utilization scaffold never recovers; weak check.

## 3. Standing rules used throughout (keep them)

1. Protocol is data; thresholds, weights, gates, decision classes load from YAML. Changing a decision rule needs a `revisions.csv` row.
2. Every parameter carries provenance; tier 5 is legal only as `illustrative`; `make status` counts them.
3. Gates are binary; UNCERTAIN is never PASS; PASS needs a named reviewer and date; R3 refuses to instantiate without permission.
4. Reimbursement, price, and cost stay separate fields. CMS data are proxies.
5. Nothing fabricated: interviews, reviews, quotes, partners, commitments stay empty until real (`docs/interviews`, `docs/reviewer_packets`).
6. Claim discipline table in `protocol.yaml`; public-claim status in `CLAIMS_REGISTER.csv`.
7. New comparators get new strategy IDs (S8+); never overwrite S0-S7.
8. Figures must carry title, units, product, scenario, manifest id, source note, decision caption (`figures.save_figure` refuses otherwise).
9. Commit only when the user authorizes (HA-05); never touch files outside `feasibility/`; never rewrite history.

## 4. How the work was done (tooling notes that matter)

- Environment: `uv` (`make env`), Python 3.12; `uv run python ...` for everything; `make check` before any claim of "done".
- The WOZCODE Edit/Search MCP tools hit a plan cap on 2026-09-02 (resets 2026-10-01). Files were then written with shell heredocs (`cat > path <<'EOF'`) and Python patch scripts. Two patch scripts silently missed their anchor because `ruff format` had reflowed the target text; both were caught by mypy or a run log. Rule: after any patch, run `ruff format`, `ruff check`, `mypy`, and the relevant tests, and grep for the inserted symbol.
- Long jobs run with `nohup ... &` and logs under `results/manifests/logs/`; the simulation runner and optimizer use `ProcessPoolExecutor` (all CPUs minus one).
- Runtime: 0.04-0.08 s per strategy-run; 100 paired runs x 8 strategies x 2 products in 25 s; optimizer ~10-12 min; sensitivity ~7 min; benchmark ~1 min per mode.
- Subagent audits ran once (10 agents); the adversarial verification pass and the matrix agent were killed by a session limit, so the anomaly registers carry one audit reading plus the main agent's own reading.

## 5. Known weak spots to fix or at least remember

- Material policy is a single order-up-to per component; nodes and the central plant both showed material stockouts under illustrative lead times.
- S7 is modeled as the status-quo network plus a 503B responder; regions are equal shares; one product per network (portfolio pooling absent).
- Reserved capacity has a fee but no take-or-pay volume term; commissioning charges capital from day 0.
- Release components come from a repo memo (tier 1 citation carrier), not from USP text (paywalled).
- Optimizer search bounds (e.g., safety stock <= 120 d) were binding; the tail constraint decides feasibility.
- `results/backcasts` needs product-specific inputs and a documented single-site failure episode.
- Public surfaces (root README, `telo-web`) still carry claims the audits contradict (see `CLAIMS_REGISTER.csv`, `docs/audits/05_inconsistencies.md`); nothing was edited outside `feasibility/`.

## 6. Open decisions for the founder (from `docs/audits/07_human_action_queue.md`)

HA-01 location and license; HA-02 sign-off on frozen thresholds (R001); HA-03 furosemide's role on the longlist; HA-04 public-surface corrections (654 vs 615 tablets, "near 3%" vs 0.7%, benchmark rows, beachhead line); HA-05 commit authorization. Privacy: `github.com/rikhinkavuru/Telo` is public and exposes `outreach/lab-contacts.md` with 21 people's e-mails, contrary to `paper/SUBMISSION.md` (session 2 correction: 29 people with addresses in that file and up to 18 more in `outreach/facilities.md`; see `docs/design_space/privacy_remediation_plan.md`).

## 7. Next assignment

`docs/design_space/ASSIGNMENT.md` (adversarial design-space expansion and strategic redesign). Suggested first hour in the new session:
1. `cd ~/telo/feasibility && make check && make status && git -C ~/telo status --short | head`.
2. Read this file, `reports/rendered/results_report.md`, `docs/audits/04_requirements_matrix.csv`, `docs/audits/07_human_action_queue.md`, the three model cards under `results/release_assurance/*/model_card.md`, `protocol/revisions.csv`.
3. Phase A: failure decomposition by ablation using `tests/integration/conftest.py::override` and `run_paired`; write `docs/design_space/bottleneck_decomposition.md` before generating any new architecture.
4. Add new strategies as S8+ in a new config file and extend `strategies.build_strategy` and `optimization.DESIGN_SPACES` without touching S0-S7 semantics; add tests for every new mechanism.
