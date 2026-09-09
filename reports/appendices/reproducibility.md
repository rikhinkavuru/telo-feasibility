# Reproducibility appendix

- Environment: Python 3.12 locked in `uv.lock`; `make env`.
- Protocol: `protocol/protocol.yaml` v1.0.0; source hashes verified by `telo-feasibility protocol verify`.
- Data: `data/raw_snapshots/<source>/<date>/*.manifest.json` (URL, retrieval time, HTTP status, sha256, license, robots). Large archives are re-fetched by `scripts/acquire_sources.py --source <id>` and checked against the manifest hash.
- Seeds: every simulation manifest records `master_seed`; run index and entity id determine every draw (`rng.RunStreams`).
- Commands, in order: `make check`; `scripts/run_deterministic.py --reconcile`; `scripts/build_product_dossiers.py`; `scripts/run_simulation.py`; `scripts/optimize_strategies.py`; `scripts/run_sensitivity.py`; `scripts/run_backcasts.py`; `scripts/run_release_benchmark.py`; `scripts/build_report.py`.
- Manifests: `results/manifests/<run_id>.json` carry protocol hash, config hashes, package version, git commit and dirty flag, platform, seeds, gate outcomes, illustrative flag.
- Tests: `results/manifests/test_report.json` from `scripts/run_tests_report.py`.
