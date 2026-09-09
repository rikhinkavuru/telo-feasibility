"""Commercial conditions implied by a simulation run (assignment Phase B family 10).

For every product and strategy in a paired simulation run, reports what the architecture
would have to be paid for and how much of its capacity would have to be committed. Prices
are never assumed: the break-even price is derived from the run, and the committed volume
is reported at that price and at any price the caller supplies with --price.

Usage: uv run python scripts/build_contract_table.py [--sim <run>] [--price 15.0]
Writes results/design_space/contract_conditions_<sim>.csv and prints a markdown table.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict

from telo_feasibility.configs import load_products
from telo_feasibility.contracting import contract_requirement, minimum_contracted_utilization
from telo_feasibility.design_space_analysis import RESULTS_DS
from telo_feasibility.provenance import PACKAGE_ROOT

RESULTS_SIM = PACKAGE_ROOT / "results" / "simulation"
FIXED_LEDGERS = (
    "ledger_capital_annualized",
    "ledger_opening_inventory",
    "ledger_fixed_site_operations",
    "ledger_product_site_launch",
    "ledger_resilience_contracts",
    "ledger_os_integration",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", default="", help="simulation run id (default: newest)")
    ap.add_argument("--price", type=float, default=None, help="assumed price per unit, if any")
    ap.add_argument("--reference", default="S0")
    args = ap.parse_args()
    runs = sorted(RESULTS_SIM.glob("sim_*/summary.json"))
    if not runs:
        raise SystemExit("no simulation run found")
    path = (RESULTS_SIM / args.sim / "summary.json") if args.sim else runs[-1]
    summary = json.loads(path.read_text(encoding="utf-8"))
    by = summary["by_strategy"]
    products = load_products()
    rows: list[dict[str, object]] = []
    for key, stats in sorted(by.items()):
        pid, sid = key.split("|")
        ref = by.get(f"{pid}|{args.reference}")
        if ref is None:
            continue
        p = products[pid].parameters
        delivered = stats["served_units"]["mean"] / (summary["config"]["horizon_years"])
        fixed = sum(stats[k]["mean"] for k in FIXED_LEDGERS if k in stats)
        variable_unit = p.base("variable_materials_usd_per_unit") + p.base(
            "variable_conversion_usd_per_unit"
        )
        # saleable capacity of the network as the run's own utilization implies it
        cost = stats["annual_total_cost"]["mean"]
        capacity = delivered / max(stats["fill_rate"]["mean"], 1e-9)
        req = contract_requirement(
            strategy_id=sid,
            reference_strategy_id=args.reference,
            annual_cost_usd=cost,
            reference_annual_cost_usd=ref["annual_total_cost"]["mean"],
            delivered_units_per_year=delivered,
            fixed_and_resilience_cost_usd=fixed,
            variable_cost_usd_per_unit=variable_unit,
            capacity_units_per_year=capacity,
            price_usd_per_unit=args.price,
        )
        row = {"product_id": pid, **asdict(req)}
        row["fixed_share_of_cost"] = fixed / cost if cost > 0 else float("nan")
        row["min_contracted_utilization_at_break_even"] = minimum_contracted_utilization(
            fixed_and_resilience_cost_usd=fixed,
            contribution_margin_usd_per_unit=req.break_even_price_usd_per_unit - variable_unit,
            capacity_units_per_year=capacity,
        )
        row["notes"] = "; ".join(req.notes)
        rows.append(row)
    out_dir = RESULTS_DS
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.parent.name
    out = out_dir / f"contract_conditions_{stem}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(
        f"| Product | Strategy | Annual cost [USD/yr] | Delivered [units/yr] | Fixed share | "
        f"Break-even price [USD/unit] | Resilience premium vs {args.reference} [USD/unit] | "
        f"Min contracted utilization |"
    )
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(
            f"| {r['product_id']} | {r['strategy_id']} | {float(r['annual_cost_usd']):,.0f} | "
            f"{float(r['delivered_units_per_year']):,.0f} | {float(r['fixed_share_of_cost']):.2f} | "
            f"{float(r['break_even_price_usd_per_unit']):.2f} | "
            f"{float(r['resilience_premium_usd_per_unit']):.2f} | "
            f"{float(r['min_contracted_utilization_at_break_even']):.2f} |"
        )
    print()
    print(f"source: {path.relative_to(PACKAGE_ROOT)}; written to {out.relative_to(PACKAGE_ROOT)}")
    print("PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
