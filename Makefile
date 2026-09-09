.PHONY: help env test test-fast lint type check protocol-hash acquire dossiers deterministic reconcile simulate optimize ablate design-space figures sensitivity backcast report status clean

UV ?= uv
PY := $(UV) run python

help:
	@echo "Telo feasibility study - targets"
	@echo "  env           create/refresh the locked environment (uv sync)"
	@echo "  test          full test suite (unit + integration + regression)"
	@echo "  test-fast     unit tests only"
	@echo "  lint          ruff check + format check"
	@echo "  type          mypy --strict"
	@echo "  check         lint + type + test"
	@echo "  protocol-hash verify protocol/protocol.yaml source hashes against the source documents"
	@echo "  acquire       freeze official source snapshots (network)"
	@echo "  dossiers      build product dossiers from frozen snapshots"
	@echo "  deterministic run the deterministic screen"
	@echo "  reconcile     reconcile the deterministic screen against the Excel workbook"
	@echo "  simulate      run the stochastic network simulation (paired, common random numbers)"
	@echo "  optimize      optimize each eligible strategy to the frozen service target"
	@echo "  ablate        failure decomposition by ablation (leave-one-out and add-one-in)"
	@echo "  design-space  feasibility conditions, dominance, and decision-reversal maps"
	@echo "  figures       ablation and design-space figures for the latest runs"
	@echo "  sensitivity   one-way, Sobol/PRCC, structural, decision-reversal, VOI"
	@echo "  backcast      historical backcasts"
	@echo "  report        build all reports and figures"
	@echo "  status        print which definition-of-finished gates remain incomplete"

env:
	$(UV) sync --all-extras

test:
	$(UV) run python scripts/run_tests_report.py

test-fast:
	$(UV) run pytest tests/unit -q

lint:
	$(UV) run ruff check src tests scripts
	$(UV) run ruff format --check src tests scripts

type:
	$(UV) run mypy

check: lint type test

protocol-hash:
	$(PY) -m telo_feasibility.cli protocol verify

acquire:
	$(PY) scripts/acquire_sources.py

dossiers:
	$(PY) scripts/build_product_dossiers.py

deterministic:
	$(PY) scripts/run_deterministic.py

reconcile:
	$(PY) scripts/run_deterministic.py --reconcile

simulate:
	$(PY) scripts/run_simulation.py

optimize:
	$(PY) scripts/optimize_strategies.py

ablate:
	$(PY) scripts/run_ablation.py

design-space:
	$(PY) scripts/run_design_space_analysis.py

# rebuild figures for the widest ablation run and the newest design-space run
figures:
	$(PY) scripts/build_ablation_figures.py --run $$(ls -1d results/ablation/abl_* | xargs -n1 basename | head -1)
	$(PY) scripts/build_design_space_figures.py --run $$(ls -1d results/design_space/ds_* | xargs -n1 basename | tail -1)

sensitivity:
	$(PY) scripts/run_sensitivity.py

backcast:
	$(PY) scripts/run_backcasts.py

report:
	$(PY) scripts/build_report.py

status:
	$(PY) -m telo_feasibility.cli status

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache
