"""Deterministic techno-economic screen (protocol section 6) and workbook reconciliation.

Two modes, never mixed in one table:

* ``workbook_replica`` reproduces the Excel scaffold's 09_Deterministic and 12_Results
  formulas exactly, defects included, so that reconciliation is meaningful.
* ``corrected`` applies the documented corrections (docs/audits/02_workbook_audit.md):
  WB-01 capacity cap and delivered-unit denominator, WB-09/WB-19 CRF computed from
  rate and life for capital and validation alike, WB-18 no second expiry charge,
  WB-20 testing batches net of yield, and adds a chronic-shortfall column.

The screen is a screening and audit layer only (protocol 6). Its shortage-day column
is a heuristic that ignores safety stock and release time (WB-02, WB-03); it never
ranks strategies. Outputs from illustrative inputs carry the preliminary banner.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Literal

from .configs import ProductConfig, StrategySet
from .economics import crf as crf_fn
from .schemas import Eligibility, ParameterSet, StrategyDesign, StrategyId
from .workbook import WORKBOOK_ELIGIBILITY_FLAG, WorkbookRow

Mode = Literal["workbook_replica", "corrected"]
DAYS_PER_YEAR = 365.0
UTILIZATION_GUARD = 1e-4  # the workbook's MAX(J, 0.0001) division guard

PRELIMINARY_BANNER = "PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS"


@dataclass(frozen=True)
class ScreenRow:
    product_id: str
    strategy_id: str
    mode: str
    # inputs echoed (09!C-H)
    sites: float
    annual_demand: float
    units_per_batch: float
    batches_per_site_year: float
    yield_fraction: float
    uptime: float
    # Eq. 1-2
    saleable_capacity: float
    utilization: float
    # ledgers (09!K-R)
    annualized_capex: float
    fixed_qa_labor: float
    validation_annualized: float
    variable_production: float
    testing: float
    inventory_carrying_expiry: float
    distribution: float
    reserved_capacity_cost: float
    # totals (09!S-V)
    total_annual_cost: float
    cost_per_unit: float
    response_days: float
    expected_shortage_days_screen: float
    # corrected-mode extras (equal to workbook conventions in replica mode)
    delivered_units: float
    chronic_shortfall_days: float
    crf_used: float
    illustrative: bool

    def as_dict(self) -> dict[str, float | str | bool]:
        return asdict(self)


def _dv(strategy: StrategyDesign, key: str, default: float | None = None) -> float:
    try:
        return float(strategy.design_variables[key])
    except KeyError as e:
        if default is not None:
            return default
        raise KeyError(f"strategy {strategy.id.value} lacks design variable {key!r}") from e


@dataclass(frozen=True)
class ScreenInputs:
    """The workbook-shaped screen inputs: multipliers for S0-S7, runtime values for S8+."""

    sites: float
    batches_per_site_year: float
    saleable_capacity: float
    capital_total: float
    fixed_total: float
    validation_total: float
    common_impact_factor: float
    release_time_factor: float
    delivery_days: float
    safety_stock_days: float
    reserved_fraction: float
    reserved_contract_usd_per_year: float
    source: str  # workbook_multipliers | runtime_topology


def screen_inputs(
    product: ProductConfig, strategy: StrategyDesign, glob: ParameterSet
) -> ScreenInputs:
    """Screen inputs for one strategy.

    S0-S7 keep the workbook's multiplier arithmetic exactly (reconciliation depends on it).
    A design-space strategy (S8+) declares a topology instead of multipliers, so its
    capacity and cost come from the built runtime: capacity is the sum over durable sites
    of batches x batch size x yield x uptime, and the common-impact factor is the largest
    share of that capacity sitting in one common-cause group, which is the screen's own
    definition of how much of the network one event can take out.

    A reserved line contributes both its contracted duty cycle and its cost. Duty cycle is
    the exercise cadence (``exercise_batches_per_year`` as a fraction of the line's design
    batch rate); campaign activation is a stochastic event this deterministic screen cannot
    see, so the credit is a lower bound and a reserved line with no exercise cadence is
    credited nothing. Cost is the reservation fee plus any take-or-pay commitment, both of
    which the simulation charges and which ``reserved_capacity_fraction`` (the workbook's
    S3-only fee proxy) does not reach for a declared topology. Before revision R007 the
    screen dropped reserved sites entirely and charged nothing for them, so every
    contracted-capacity architecture screened byte-identical to S0 (MD-20).
    """
    p = product.parameters
    y = p.base("yield_fraction")
    u = p.base("uptime_fraction")
    units_per_batch = p.base("units_per_batch")
    if strategy.site_plans is None:
        sites = _dv(strategy, "sites")
        batches = p.base("batches_per_site_year_nominal") * _dv(strategy, "capacity_factor")
        return ScreenInputs(
            sites=sites,
            batches_per_site_year=batches,
            saleable_capacity=sites * units_per_batch * batches * y * u,
            capital_total=sites * p.base("capital_usd_per_site"),
            fixed_total=sites
            * p.base("fixed_qa_labor_usd_per_site_year")
            * _dv(strategy, "fixed_cost_factor"),
            validation_total=sites
            * p.base("validation_usd_one_time")
            * _dv(strategy, "validation_factor"),
            common_impact_factor=_dv(strategy, "common_impact_factor"),
            release_time_factor=_dv(strategy, "release_time_factor"),
            delivery_days=_dv(strategy, "delivery_days"),
            safety_stock_days=_dv(strategy, "safety_stock_days"),
            reserved_fraction=_dv(strategy, "reserved_capacity_fraction"),
            reserved_contract_usd_per_year=0.0,
            source="workbook_multipliers",
        )
    from .strategies import build_strategy

    rt = build_strategy(strategy, product, glob)
    capacity = 0.0
    by_group: dict[str, float] = {}
    n_sites = 0.0
    batches_total = 0.0
    for site in rt.sites.values():
        if site.is_503b():
            continue
        cap = (
            site.batches_per_year
            * site.spec.batch_size_units
            * site.spec.yield_fraction
            * site.spec.uptime_fraction
        )
        duty = 1.0
        if site.reserved:
            exercise_per_year = (
                DAYS_PER_YEAR / site.exercise_interval_days
                if site.exercise_interval_days > 0
                else 0.0
            )
            duty = (
                min(1.0, exercise_per_year / site.batches_per_year)
                if site.batches_per_year > 0
                else 0.0
            )
            if duty <= 0.0:
                continue
            cap *= duty
        n_sites += duty
        batches_total += site.batches_per_year * duty
        capacity += cap
        for g in site.common_cause_groups:
            by_group[g] = by_group.get(g, 0.0) + cap
    largest = max(by_group.values(), default=0.0)
    return ScreenInputs(
        sites=n_sites,
        batches_per_site_year=batches_total / n_sites if n_sites > 0 else 0.0,
        saleable_capacity=capacity,
        capital_total=sum(rt.site_capital_usd.values()),
        fixed_total=sum(rt.site_fixed_usd_per_year.values()),
        validation_total=sum(rt.site_validation_usd.values()),
        common_impact_factor=(largest / capacity) if capacity > 0 else 1.0,
        release_time_factor=_dv(strategy, "release_time_factor", 1.0),
        delivery_days=_dv(strategy, "delivery_days", 2.0),
        safety_stock_days=_dv(strategy, "safety_stock_days", 30.0),
        reserved_fraction=_dv(strategy, "reserved_capacity_fraction", 0.0),
        reserved_contract_usd_per_year=(
            sum(rt.reserved_fee_usd_per_year.values()) + sum(rt.take_or_pay_usd_per_year.values())
        ),
        source="runtime_topology",
    )


def screen_shortage_days(
    *,
    sites: float,
    utilization: float,
    saleable_capacity: float,
    annual_demand: float,
    common_impact_factor: float,
    glob: ParameterSet,
) -> float:
    """09_Deterministic!V: event-driven expected shortage days (workbook heuristic).

    Site term: sites x lambda_site x duration x max(0, J - (sites-1)/sites) / max(J, guard).
    Common-cause term: lambda_cc x duration_cc x max(0, J - (1 - impact x factor)) / max(J, guard).
    Demand-shock term: lambda_shock x duration_shock x max(0, mult - I/D) / mult.
    """
    j = utilization
    lam_site = glob.base("site_failures_per_site_year")
    dur_site = glob.base("site_failure_duration_days")
    lam_cc = glob.base("common_cause_events_per_year")
    dur_cc = glob.base("common_cause_duration_days")
    impact = glob.base("common_cause_capacity_impact")
    lam_sh = glob.base("demand_shocks_per_year")
    dur_sh = glob.base("demand_shock_duration_days")
    mult = glob.base("demand_shock_multiplier")
    guard = max(j, UTILIZATION_GUARD)
    site_term = (
        sites * lam_site * dur_site * max(0.0, j - (sites - 1.0) / sites) / guard
        if sites > 0
        else 0.0
    )
    cc_term = lam_cc * dur_cc * max(0.0, j - (1.0 - impact * common_impact_factor)) / guard
    ratio = saleable_capacity / annual_demand if annual_demand > 0 else mult
    shock_term = lam_sh * dur_sh * max(0.0, mult - ratio) / mult if mult > 0 else 0.0
    return max(0.0, site_term + cc_term + shock_term)


def screen_row(
    product: ProductConfig, strategy: StrategyDesign, glob: ParameterSet, mode: Mode
) -> ScreenRow:
    p = product.parameters
    if strategy.site_plans is not None and mode == "workbook_replica":
        raise ValueError(
            f"{strategy.id.value} declares a topology; the workbook replica has no arithmetic "
            "for it. Screen design-space strategies in 'corrected' mode."
        )
    si = screen_inputs(product, strategy, glob)
    sites = si.sites
    demand = p.base("annual_demand_units")
    units_per_batch = p.base("units_per_batch")
    batches = si.batches_per_site_year
    y = p.base("yield_fraction")
    u = p.base("uptime_fraction")
    capacity = si.saleable_capacity  # Eq. 1
    utilization = demand / capacity if capacity > 0 else 0.0  # Eq. 2 (workbook IFERROR -> 0)

    life = glob.base("capital_economic_life_years")
    rate = glob.base("discount_rate")
    v_unit = p.base("variable_materials_usd_per_unit") + p.base("variable_conversion_usd_per_unit")
    scrap = p.base("expiry_scrap_fraction")
    test_per_batch = p.base("testing_usd_per_batch")
    carry = glob.base("inventory_carrying_rate")
    ssd = si.safety_stock_days
    dist = p.base("distribution_usd_per_unit")
    reserved = si.reserved_fraction

    if mode == "workbook_replica":
        crf_used = glob.base("capital_recovery_factor_typed")  # WB-09 (D015)
        capex = si.capital_total * crf_used
        val = si.validation_total / life  # straight line (WB-19)
        if scrap >= 1.0:
            raise ValueError("expiry/scrap fraction must be < 1")
        variable = demand * v_unit / (1.0 - scrap)
        testing = (
            demand / units_per_batch if units_per_batch > 0 else 0.0
        ) * test_per_batch  # WB-20
        inventory = (
            variable * ssd / DAYS_PER_YEAR * carry + variable * scrap
        )  # WB-18 double count kept
        distribution = demand * dist
        delivered = demand  # workbook convention (WB-01)
        chronic = 0.0
    elif mode == "corrected":
        crf_used = crf_fn(rate, life)
        capex = si.capital_total * crf_used
        val = si.validation_total * crf_used
        if scrap >= 1.0:
            raise ValueError("expiry/scrap fraction must be < 1")
        deliverable_capacity = capacity * (1.0 - scrap)
        delivered = min(demand, deliverable_capacity)
        produced = delivered / (1.0 - scrap)
        variable = produced * v_unit
        batches_run = produced / (units_per_batch * y) if units_per_batch * y > 0 else 0.0
        testing = batches_run * test_per_batch
        inventory = variable * ssd / DAYS_PER_YEAR * carry
        distribution = delivered * dist
        chronic = DAYS_PER_YEAR * (1.0 - delivered / demand) if demand > 0 else 0.0
    else:  # pragma: no cover - Literal guards this
        raise ValueError(mode)

    fixed_total = si.fixed_total
    # WB-21: the workbook's fee definition, kept in both modes for S0-S7. A declared
    # topology (S8+) carries the reservation fee and take-or-pay commitment the simulation
    # actually charges, which the workbook proxy cannot express (MD-20, revision R007).
    reserved_cost = demand * v_unit * reserved + si.reserved_contract_usd_per_year
    total = (
        capex + fixed_total + val + variable + testing + inventory + distribution + reserved_cost
    )
    denominator = demand if mode == "workbook_replica" else delivered
    cost_per_unit = (
        total / denominator if denominator > 0 else 0.0 if mode == "workbook_replica" else math.inf
    )

    response = (
        p.base("material_lead_time_days")
        + p.base("changeover_days")
        + p.base("production_cycle_days")
        + p.base("release_time_days") * si.release_time_factor
        + si.delivery_days
    )  # Eq. 5 as the workbook sums it (serial, no overlap)
    shortage = screen_shortage_days(
        sites=sites,
        utilization=utilization,
        saleable_capacity=capacity,
        annual_demand=demand,
        common_impact_factor=si.common_impact_factor,
        glob=glob,
    )
    illustrative = bool(p.illustrative_ids() or glob.illustrative_ids())
    return ScreenRow(
        product_id=product.id,
        strategy_id=strategy.id.value,
        mode=mode,
        sites=sites,
        annual_demand=demand,
        units_per_batch=units_per_batch,
        batches_per_site_year=batches,
        yield_fraction=y,
        uptime=u,
        saleable_capacity=capacity,
        utilization=utilization,
        annualized_capex=capex,
        fixed_qa_labor=fixed_total,
        validation_annualized=val,
        variable_production=variable,
        testing=testing,
        inventory_carrying_expiry=inventory,
        distribution=distribution,
        reserved_capacity_cost=reserved_cost,
        total_annual_cost=total,
        cost_per_unit=cost_per_unit,
        response_days=response,
        expected_shortage_days_screen=shortage,
        delivered_units=delivered,
        chronic_shortfall_days=chronic,
        crf_used=crf_used,
        illustrative=illustrative,
    )


def run_screen(
    products: dict[str, ProductConfig], strategies: StrategySet, glob: ParameterSet, mode: Mode
) -> list[ScreenRow]:
    return [
        screen_row(prod, design, glob, mode)
        for prod in products.values()
        for design in strategies.designs
    ]


# ---------------------------------------------------------------------------
# Dashboard (12_Results replica)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DashboardRow:
    product_id: str
    strategy_id: str
    mode: str
    cost_per_unit: float
    response_days: float
    expected_shortage_days: float
    shortage_days_avoided: float
    incremental_annual_cost: float
    cost_per_shortage_day_avoided: float | None
    approx_fill_rate: float
    interpretation: str
    eligibility: str

    def as_dict(self) -> dict[str, float | str | None]:
        return asdict(self)


def dashboard_rows(
    rows: list[ScreenRow],
    glob: ParameterSet,
    target_fill_rate: float,
    eligibility: dict[StrategyId, Eligibility] | None,
) -> list[DashboardRow]:
    """12_Results replica. ``eligibility=None`` uses the workbook's typed YES flags (replica);
    otherwise the gate-derived eligibility governs and UNCERTAIN never passes."""
    severity = glob.base("unmet_demand_severity")
    out: list[DashboardRow] = []
    refs = {r.product_id: r for r in rows if r.strategy_id == StrategyId.S0.value}
    for r in rows:
        ref = refs[r.product_id]
        avoided = max(0.0, ref.expected_shortage_days_screen - r.expected_shortage_days_screen)
        incremental = r.total_annual_cost - ref.total_annual_cost
        ratio = incremental / avoided if avoided > 0 else None
        fill = max(0.0, 1.0 - r.expected_shortage_days_screen / DAYS_PER_YEAR * severity)
        sid = StrategyId(r.strategy_id)
        if eligibility is None:
            elig_ok = WORKBOOK_ELIGIBILITY_FLAG[sid] == "YES"
            elig_label = WORKBOOK_ELIGIBILITY_FLAG[sid]
        else:
            elig_ok = eligibility[sid] is Eligibility.ELIGIBLE
            elig_label = eligibility[sid].value
        if not elig_ok:
            interp = "Regulatory eligibility unresolved"
        elif fill < target_fill_rate:
            interp = "Below service target"
        elif incremental < 0:
            interp = "Cost-saving candidate"
        else:
            interp = "Resilience premium required"
        out.append(
            DashboardRow(
                product_id=r.product_id,
                strategy_id=r.strategy_id,
                mode=r.mode,
                cost_per_unit=r.cost_per_unit,
                response_days=r.response_days,
                expected_shortage_days=r.expected_shortage_days_screen,
                shortage_days_avoided=avoided,
                incremental_annual_cost=incremental,
                cost_per_shortage_day_avoided=ratio,
                approx_fill_rate=fill,
                interpretation=interp,
                eligibility=elig_label,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CellComparison:
    sheet: str
    row: int
    column: str
    product_id: str
    strategy_id: str
    workbook_value: float | str | None
    python_value: float | str | None
    abs_diff: float | None
    rel_diff: float | None
    ok: bool


@dataclass(frozen=True)
class ReconciliationReport:
    comparisons: list[CellComparison]
    abs_tolerance: float
    rel_tolerance: float

    @property
    def n(self) -> int:
        return len(self.comparisons)

    @property
    def mismatches(self) -> list[CellComparison]:
        return [c for c in self.comparisons if not c.ok]

    @property
    def ok(self) -> bool:
        return not self.mismatches


def _compare(
    wv: object, pv: object, abs_tol: float, rel_tol: float
) -> tuple[float | None, float | None, bool]:
    if (
        isinstance(wv, int | float)
        and not isinstance(wv, bool)
        and isinstance(pv, int | float)
        and not isinstance(pv, bool)
    ):
        a = abs(float(wv) - float(pv))
        scale = max(abs(float(wv)), abs(float(pv)))
        rel = a / scale if scale > 0 else 0.0
        return a, rel, a <= abs_tol or rel <= rel_tol
    if wv is None or (isinstance(wv, str) and wv.startswith("#")):
        return None, None, pv is None
    return None, None, str(wv) == str(pv)


def reconcile_screen(
    cached: list[WorkbookRow],
    rows: list[ScreenRow],
    *,
    abs_tol: float = 1e-6,
    rel_tol: float = 1e-9,
) -> ReconciliationReport:
    from .workbook import SCREEN_COLUMNS

    by_key = {(r.product_id, r.strategy_id): r for r in rows}
    comps: list[CellComparison] = []
    for wr in cached:
        pr = by_key[(wr.product_id, wr.strategy_id.value)]
        pd = pr.as_dict()
        for col, name in SCREEN_COLUMNS.items():
            wv = wr.values[name]
            pv = pd[name]
            a, rel, ok = _compare(wv, pv, abs_tol, rel_tol)
            comps.append(
                CellComparison(
                    wr.sheet,
                    wr.row,
                    col,
                    wr.product_id,
                    wr.strategy_id.value,
                    _cell_value(wv),
                    _cell_value(pv),
                    a,
                    rel,
                    ok,
                )
            )
    return ReconciliationReport(comps, abs_tol, rel_tol)


def _cell_value(v: object) -> float | str | None:
    if v is None or isinstance(v, bool):
        return None if v is None else str(v)
    if isinstance(v, int | float):
        return float(v)
    return str(v)


def reconcile_dashboard(
    cached: list[WorkbookRow],
    rows: list[DashboardRow],
    *,
    abs_tol: float = 1e-6,
    rel_tol: float = 1e-9,
) -> ReconciliationReport:
    from .workbook import DASHBOARD_COLUMNS

    by_key = {(r.product_id, r.strategy_id): r for r in rows}
    comps: list[CellComparison] = []
    for wr in cached:
        pr = by_key[(wr.product_id, wr.strategy_id.value)]
        pd = pr.as_dict()
        for col, name in DASHBOARD_COLUMNS.items():
            wv = wr.values[name]
            pv = pd[name]
            a, rel, ok = _compare(wv, pv, abs_tol, rel_tol)
            comps.append(
                CellComparison(
                    wr.sheet,
                    wr.row,
                    col,
                    wr.product_id,
                    wr.strategy_id.value,
                    _cell_value(wv),
                    _cell_value(pv),
                    a,
                    rel,
                    ok,
                )
            )
    return ReconciliationReport(comps, abs_tol, rel_tol)
