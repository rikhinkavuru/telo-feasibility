"""Run the release-assurance benchmark on the frozen public tablet spectra.

Modes (see docs/methods/release_benchmark.md): the default selects PLS components by
5-fold CV on the training partition without per-wavelength standardization;
``--n-components 8 --pls-scale`` reproduces the repository script. ``--gate-score``
and ``--component-selection`` exist to measure the gate-choice and selection leaks.
"""

from __future__ import annotations

import argparse
import time

from telo_feasibility.release_benchmark import (
    COMPONENT_SELECTIONS,
    GATE_SCORES,
    BenchmarkConfig,
    run_benchmark,
    write_results,
)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=50)
    ap.add_argument("--n-components", type=int, default=None)
    ap.add_argument("--pls-scale", action="store_true")
    ap.add_argument("--gate-score", choices=GATE_SCORES, default="nn")
    ap.add_argument("--component-selection", choices=COMPONENT_SELECTIONS, default="train_cv")
    ap.add_argument("--cost-product", default="sodium_bicarbonate_8_4_50ml")
    args = ap.parse_args()
    t0 = time.time()
    res = run_benchmark(
        BenchmarkConfig(
            seeds=args.seeds,
            n_components=args.n_components,
            pls_scale=args.pls_scale,
            gate_score=args.gate_score,
            component_selection=args.component_selection,
            cost_product_id=args.cost_product,
        )
    )
    out = write_results(res)
    print(f"results -> {out} ({time.time() - t0:.0f}s)")
    print(res.banner)
