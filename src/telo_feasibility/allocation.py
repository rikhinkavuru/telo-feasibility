"""Allocation of scarce supply across regions (protocol 8.3).

Policies: proportional to requested quantity; criticality-weighted; minimum regional
guarantee then proportional; optimization-based (a small linear program minimizing
weighted unmet demand). All return integer allocations that never exceed availability
or requests.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
from scipy.optimize import linprog


def _largest_remainder(shares: np.ndarray, total: int, caps: np.ndarray) -> np.ndarray:
    """Integer apportionment of ``total`` by ``shares`` without exceeding ``caps``."""
    if total <= 0 or shares.sum() <= 0:
        return np.zeros_like(caps)
    raw = shares / shares.sum() * total
    base = np.minimum(np.floor(raw), caps).astype(np.int64)
    left = total - int(base.sum())
    order = np.argsort(-(raw - base))
    for i in order:
        if left <= 0:
            break
        if base[i] < caps[i]:
            base[i] += 1
            left -= 1
    # if some caps bind, give the rest to uncapped in order
    while left > 0:
        room = np.where(base < caps)[0]
        if room.size == 0:
            break
        base[room[0]] += 1
        left -= 1
    return np.asarray(base, dtype=np.int64)


def allocate(
    requests: Mapping[str, int],
    available: int,
    policy: str,
    criticality: Mapping[str, float] | None = None,
    minimum_guarantee: Mapping[str, int] | None = None,
) -> dict[str, int]:
    ids = list(requests)
    req = np.array([max(int(requests[i]), 0) for i in ids], dtype=np.int64)
    avail = max(int(available), 0)
    if req.sum() <= avail:
        return {i: int(q) for i, q in zip(ids, req, strict=True)}
    if policy == "proportional":
        alloc = _largest_remainder(req.astype(float), avail, req)
    elif policy == "criticality_weighted":
        w = np.array([float((criticality or {}).get(i, 1.0)) for i in ids])
        alloc = _largest_remainder(req * w, avail, req)
    elif policy == "minimum_guarantee":
        mg = np.array(
            [
                min(int((minimum_guarantee or {}).get(i, 0)), int(r))
                for i, r in zip(ids, req, strict=True)
            ],
            dtype=np.int64,
        )
        if mg.sum() > avail:
            alloc = _largest_remainder(mg.astype(float), avail, mg)
        else:
            rest = _largest_remainder((req - mg).astype(float), avail - int(mg.sum()), req - mg)
            alloc = mg + rest
    elif policy == "optimization":
        w = np.array([float((criticality or {}).get(i, 1.0)) for i in ids])
        # minimize sum w_i * unmet_i  s.t. alloc_i + unmet_i = req_i, sum alloc <= avail, alloc_i >= 0
        n = len(ids)
        c = np.concatenate([np.zeros(n), w])
        a_eq = np.hstack([np.eye(n), np.eye(n)])
        a_ub = np.concatenate([np.ones(n), np.zeros(n)])[None, :]
        res = linprog(
            c,
            A_ub=a_ub,
            b_ub=[avail],
            A_eq=a_eq,
            b_eq=req.astype(float),
            bounds=[(0, None)] * (2 * n),
            method="highs",
        )
        x = res.x[:n] if res.success else req * (avail / req.sum())
        alloc = _largest_remainder(np.maximum(x, 1e-9), avail, req)
    else:
        raise ValueError(f"unknown allocation policy {policy}")
    alloc = np.minimum(alloc, req)
    return {i: int(q) for i, q in zip(ids, alloc, strict=True)}


def regional_disparity(metric_by_region: Mapping[str, float]) -> float:
    """Protocol B5: max - min across regions."""
    if not metric_by_region:
        return 0.0
    vals = list(metric_by_region.values())
    return max(vals) - min(vals)
