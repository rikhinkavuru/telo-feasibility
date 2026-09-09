from __future__ import annotations

import numpy as np

from telo_feasibility.sensitivity import prcc


def test_prcc_recovers_monotone_dependence() -> None:
    rng = np.random.default_rng(0)
    x = rng.uniform(size=(400, 3))
    y = 5 * x[:, 0] ** 2 + 0.1 * rng.normal(size=400)  # monotone in x0 only
    r = prcc(x, y)
    assert r[0] > 0.9
    assert abs(r[1]) < 0.2 and abs(r[2]) < 0.2


def test_sobol_on_ishigami_matches_known_indices() -> None:
    from SALib.analyze import sobol as sa
    from SALib.sample import sobol as ss
    from SALib.test_functions import Ishigami

    problem = {"num_vars": 3, "names": ["x1", "x2", "x3"], "bounds": [[-np.pi, np.pi]] * 3}
    x = ss.sample(problem, 1024, calc_second_order=False, seed=1)
    y = Ishigami.evaluate(x)
    si = sa.analyze(problem, y, calc_second_order=False, print_to_console=False)
    # analytic: S1 = (0.3139, 0.4424, 0.0); ST = (0.5576, 0.4424, 0.2437)
    assert (
        abs(si["S1"][0] - 0.3139) < 0.06
        and abs(si["S1"][1] - 0.4424) < 0.06
        and abs(si["S1"][2]) < 0.06
    )
    assert abs(si["ST"][2] - 0.2437) < 0.08
