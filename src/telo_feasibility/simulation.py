"""Daily discrete-time network simulation (protocol section 7).

One call to ``simulate_run`` executes the nine-step daily order for one strategy in one
exogenous world. ``run_paired`` generates the world once per run for the universal
roster and runs every strategy against it (common random numbers).

Integer units everywhere; the mass-balance identity is asserted every day:

    initial + produced_saleable == on_hand + in_transit + in_release_queue + expired + served
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field

import numpy as np

from .allocation import allocate, regional_disparity
from .configs import ProductConfig
from .demand import DemandSpec, generate_demand_paths
from .disruptions import DAYS_PER_YEAR, ExogenousWorld, WorldParams, generate_world
from .economics import CostLedger, crf
from .inventory import InventoryBook, Lot
from .quality import QualityParams, QueuedBatch, disposition
from .release_assurance import ReleaseAssuranceParams
from .rng import RunStreams
from .schemas import ParameterSet, RandomStream, ReleaseScenario, StrategyDesign
from .strategies import StrategyRuntime, build_strategy, universal_roster_ids
from .suppliers import MaterialStore


@dataclass(frozen=True)
class SimSettings:
    horizon_days: int
    warm_up_days: int
    shortage_day_threshold: float
    fill_rate_mean_min: float
    recovery_window_days: int
    n_regions: int = 4
    record_events: bool = True
    shortage_listed_at_t0: bool = False
    # A site that does not exist at t0 starts its commissioning clock at the first measured
    # day rather than at simulation day zero (revision R008, model defect MD-17). Without
    # this, any lead time at or below ``warm_up_days`` is served entirely by the warm-up
    # period and costs nothing inside the window the metrics cover, which made the whole
    # commissioning family of parameters unobservable at their own base values.
    commissioning_from_measurement_start: bool = True


@dataclass
class Shipment:
    region_id: str
    origin_id: str
    units: int
    arrival_day: int
    release_day: int
    expiry_day: int
    unit_value_usd: float
    pathway: str
    emergency: bool


@dataclass
class Counters:
    initial_units: int = 0
    produced_filled: int = 0
    produced_saleable: int = 0
    rejected_units: int = 0
    released_units: int = 0
    expired_units: int = 0
    served_units: int = 0
    lost_units: int = 0
    shipped_units: int = 0
    emergency_shipments: int = 0
    batches_started: int = 0
    deviations: int = 0
    rejections: int = 0
    abstentions: int = 0
    wrong_releases: int = 0
    site_failure_days: int = 0
    common_cause_days: int = 0
    supplier_disruption_days: int = 0
    material_stockouts: int = 0
    activations: int = 0
    activation_failures: int = 0
    exercise_batches: int = 0
    p503b_eligible_days: int = 0


@dataclass
class RunResult:
    strategy_id: str
    run_index: int
    metrics: dict[str, float]
    regional: dict[str, dict[str, float]]
    ledger: CostLedger
    counters: Counters
    episodes: list[dict[str, float]]
    event_digest: str
    daily_fill: np.ndarray
    daily_demand: np.ndarray
    daily_served: np.ndarray
    notes: list[str] = field(default_factory=list)


def _quality_params(glob: ParameterSet, runtime: StrategyRuntime | None = None) -> QualityParams:
    """Global quality parameters, scaled by any strategy-level factors.

    ``deviation_rate_factor`` and ``investigation_duration_factor`` default to 1.0, so
    S0-S7 are unchanged. They exist so an operating-system architecture can be modeled as
    what it actually claims: fewer deviations and faster closure, not shorter release time.
    """
    dev = glob.base("deviation_rate_per_batch")
    inv = glob.base("investigation_duration_days")
    if runtime is not None:
        dev = min(max(dev * runtime.deviation_rate_factor, 0.0), 1.0)
        inv = max(inv * runtime.investigation_duration_factor, 0.0)
    return QualityParams(
        deviation_rate=dev,
        rejection_rate=glob.base("batch_rejection_rate"),
        investigation_median_days=inv,
        duration_cv=glob.base("disruption_duration_cv"),
        yield_sd=glob.base("yield_sd"),
    )


def demand_spec(product: ProductConfig, runtime: StrategyRuntime, glob: ParameterSet) -> DemandSpec:
    return DemandSpec(
        annual_demand_units=product.parameters.base("annual_demand_units"),
        region_shares={r.id: r.share for r in runtime.topology.regions},
        annual_growth=glob.base("annual_demand_growth"),
    )


class _Sim:
    """Mutable simulation state and the nine daily steps."""

    def __init__(
        self,
        runtime: StrategyRuntime,
        product: ProductConfig,
        glob: ParameterSet,
        world: ExogenousWorld,
        streams: RunStreams,
        settings: SimSettings,
    ) -> None:
        self.rt = runtime
        self.product = product
        self.glob = glob
        self.world = world
        self.streams = streams
        self.s = settings
        self.n_days = settings.horizon_days
        p = product.parameters
        self.unit_value = p.base("variable_materials_usd_per_unit") + p.base(
            "variable_conversion_usd_per_unit"
        )
        self.testing_per_batch = p.base("testing_usd_per_batch")
        self.material_unit_value = p.base("variable_materials_usd_per_unit") / 3.0
        self.investigation_cost = glob.base("investigation_cost_usd")
        self.carrying_rate = glob.base("inventory_carrying_rate")
        self.crf = crf(glob.base("discount_rate"), glob.base("capital_economic_life_years"))
        self.os_cost = (
            glob.base("os_integration_usd_per_site_year")
            if runtime.release_assurance.scenario is not ReleaseScenario.R0
            else 0.0
        )
        self.backorder_window = round(glob.base("backorder_window_days"))
        self.qp = _quality_params(glob, runtime)
        self.spec = demand_spec(product, runtime, glob)
        self.demand = generate_demand_paths(self.spec, world)
        self.regions = [r.id for r in runtime.topology.regions]
        self.book = InventoryBook()
        self.backlog: dict[str, deque[list[int]]] = {r: deque() for r in self.regions}
        self.transit: list[Shipment] = []
        self.queue: list[QueuedBatch] = []
        self.c = Counters()
        self.ledger = CostLedger()
        self.events: list[str] = []
        self.lot_seq = 0
        self.site_cap = {
            sid: world.effective_site_capacity(sid, list(rt.common_cause_groups))
            for sid, rt in runtime.sites.items()
        }
        self.sup_cap = {
            sup.id: world.effective_supplier_capacity(sup.id, list(sup.common_cause_groups))
            for sup in runtime.topology.suppliers
        }
        self.materials: dict[str, MaterialStore] = {}
        for sid, rt in runtime.sites.items():
            comp_supplier = {
                "api": rt.supplier_ids[0],
                "vial": rt.supplier_ids[1],
                "stopper_seal": rt.supplier_ids[2],
            }
            lead = {
                c: runtime.topology.supplier(s).lead_time_days.base or 0.0
                for c, s in comp_supplier.items()
            }
            daily = self._site_daily_demand(sid, 0) / max(rt.spec.yield_fraction, 1e-9)
            # MD-1 (revision R009): the opening component position is the policy position,
            # safety plus cycle cover, and is deliberately independent of the lead time.
            # It used to be (target + lead) days, so a site with a fast supplier started
            # with a smaller buffer and did worse under disruption, which is the second
            # half of the wrong-sign defect and the larger half.
            init = {
                c: round(
                    (runtime.material_reorder_point_days + runtime.material_target_days) * daily
                )
                for c in comp_supplier
            }
            self.materials[sid] = MaterialStore(
                sid,
                init,
                comp_supplier,
                lead,
                runtime.material_target_days,
                runtime.material_reorder_point_days,
                batch_units=round(rt.spec.batch_size_units),
            )
        self.d_demand = np.zeros(self.n_days, dtype=np.int64)
        self.d_served = np.zeros(self.n_days, dtype=np.int64)
        self.d_fill = np.ones(self.n_days)
        self.r_demand = {r: np.zeros(self.n_days, dtype=np.int64) for r in self.regions}
        self.r_served = {r: np.zeros(self.n_days, dtype=np.int64) for r in self.regions}
        self.d_lost = np.zeros(self.n_days, dtype=np.int64)
        self.lost_by_origin = np.zeros(self.n_days, dtype=np.int64)
        self.r_lost_by_origin = {r: np.zeros(self.n_days, dtype=np.int64) for r in self.regions}
        self._seed_initial_inventory()

    # ------------------------------------------------------------------ helpers
    def _mean_daily(self, region_id: str, day: int) -> float:
        return self.spec.mean_daily(region_id, day)

    def _site_daily_demand(self, site_id: str, day: int) -> float:
        rt = self.rt.sites[site_id]
        return sum(self._mean_daily(r, day) for r in rt.serves_region_ids)

    def _new_lot_id(self) -> str:
        self.lot_seq += 1
        return f"lot{self.lot_seq}"

    def _log(self, day: int, kind: str, entity: str, qty: int | float) -> None:
        if self.s.record_events:
            self.events.append(f"{day}|{kind}|{entity}|{qty}")

    INITIAL_COHORTS = 4

    def _seed_cohorts(self, location_id: str, units: int) -> None:
        """Add opening stock as cohorts whose remaining shelf life is spread, not identical.

        MD-4 (revision R004): the opening stock used to be stamped at half the shelf life,
        which for a 24-month product is day 365, the first measured day, so a larger opening
        position expired at once and more safety stock read as harmful. A stocking point in
        steady state holds a mix of ages, so the cohorts here are spread evenly over the
        interval from one replenishment cycle to the full shelf life. The split is a
        modelling convention, not evidence; the number of cohorts is arbitrary and the
        integer split preserves the mass balance exactly.
        """
        if units <= 0:
            return
        # NEW-1 (revision R009): opening stock is purchased, not inherited. A feasibility
        # study asking whether to build this network must pay for the position it starts
        # with, otherwise a design whose optimum is a year of safety stock is handed that
        # year for nothing and every comparison between a deep-stock design and a capacity
        # design is unsound. The units are charged once at the same unit value production
        # pays (materials plus conversion); the ledger's horizon scaling then spreads the
        # lump across the measured window. The cost of *carrying* the position is not added
        # here because it is already charged every day through ``inventory_logistics``,
        # which values the whole book including these lots; adding it again would double
        # count.
        self.ledger.opening_inventory += units * self.unit_value
        shelf = round(self.rt.shelf_life_days)
        cycle = min(max(round(self.rt.initial_region_stock_days), 1), shelf)
        n = self.INITIAL_COHORTS
        base, extra = divmod(units, n)
        for i in range(n):
            qty = base + (1 if i < extra else 0)
            if qty <= 0:
                continue
            expiry = round(cycle + (shelf - cycle) * (i + 1) / n)
            self.book.add(
                Lot(self._new_lot_id(), location_id, qty, 0, max(expiry, 1), self.unit_value)
            )
        self.c.initial_units += units

    def _seed_initial_inventory(self) -> None:
        for r in self.regions:
            self._seed_cohorts(
                f"{r}:stock", round(self.rt.initial_region_stock_days * self._mean_daily(r, 0))
            )
        for sid, rt in self.rt.sites.items():
            if not rt.exists(0) or rt.reserved or rt.is_503b():
                continue
            self._seed_cohorts(
                sid, round(self.rt.initial_site_stock_days * self._site_daily_demand(sid, 0))
            )

    def _in_transit_units(self, region_id: str | None = None, origin_id: str | None = None) -> int:
        return sum(
            sh.units
            for sh in self.transit
            if (region_id is None or sh.region_id == region_id)
            and (origin_id is None or sh.origin_id == origin_id)
        )

    def _queued_saleable(self, site_id: str | None = None) -> int:
        return sum(q.saleable_units for q in self.queue if site_id is None or q.site_id == site_id)

    # ------------------------------------------------------------------ steps
    def step1_expire(self, day: int) -> None:
        before = self.book.expired_value_usd
        expired = self.book.expire(day)
        self.c.expired_units += expired
        self.ledger.failure_waste += self.book.expired_value_usd - before
        if expired:
            self._log(day, "expire", "all", expired)

    def step3_disruption_counters(self, day: int) -> None:
        for sid, rt in self.rt.sites.items():
            if rt.exists(day) and self.world.site_capacity[sid][day] < 1.0:
                self.c.site_failure_days += 1
            if rt.exists(day) and any(
                self.world.group_capacity[g][day] < 1.0 for g in rt.common_cause_groups
            ):
                self.c.common_cause_days += 1
        for sup in self.rt.topology.suppliers:
            if self.sup_cap[sup.id][day] <= 0.0:
                self.c.supplier_disruption_days += 1
        if self.world.shortage_listed[day]:
            self.c.p503b_eligible_days += 1

    def step4_receive(self, day: int) -> None:
        for store in self.materials.values():
            store.receive(day, self.sup_cap)
        arrived: list[Shipment] = []
        keep: list[Shipment] = []
        for sh in self.transit:
            (arrived if sh.arrival_day <= day else keep).append(sh)
        self.transit = keep
        for sh in arrived:
            if sh.expiry_day <= day:
                # expired in transit: never enters usable stock
                self.c.expired_units += sh.units
                self.ledger.failure_waste += sh.units * sh.unit_value_usd
                self._log(day, "expire_in_transit", sh.region_id, sh.units)
                continue
            self.book.add(
                Lot(
                    self._new_lot_id(),
                    f"{sh.region_id}:stock",
                    sh.units,
                    sh.release_day,
                    sh.expiry_day,
                    sh.unit_value_usd,
                    sh.pathway,
                )
            )
        released: list[QueuedBatch] = []
        keep_q: list[QueuedBatch] = []
        for q in self.queue:
            (released if q.release_day <= day else keep_q).append(q)
        self.queue = keep_q
        for q in released:
            if q.rejected or q.saleable_units == 0:
                continue
            shelf = self.rt.bud_503b_days if q.pathway == "p503b" else self.rt.shelf_life_days
            self.book.add(
                Lot(
                    self._new_lot_id(),
                    q.site_id,
                    q.saleable_units,
                    day,
                    day + round(shelf),
                    self.unit_value,
                    q.pathway,
                )
            )
            self.c.released_units += q.saleable_units
            self.ledger.quality_testing += self.testing_per_batch
            self._log(day, "release", q.site_id, q.saleable_units)

    def step5_serve(self, day: int) -> None:
        listed = bool(self.world.shortage_listed[day])
        total_demand = 0
        total_served = 0
        lost_today = 0
        for r in self.regions:
            d = int(self.demand[r][day])
            loc = f"{r}:stock"
            bl = self.backlog[r]
            while bl and day - bl[0][0] > self.backorder_window:
                origin, units_lost = bl.popleft()
                lost_today += units_lost
                self.lost_by_origin[origin] += units_lost
                self.r_lost_by_origin[r][origin] += units_lost
            need = d + sum(u for _, u in bl)
            avail = self.book.on_hand(loc, allow_503b=listed)
            served = 0
            if min(need, avail) > 0:
                served = sum(
                    q for _, q in self.book.issue(loc, min(need, avail), day, allow_503b=listed)
                )
            remaining = served
            while remaining > 0 and bl:
                take = min(remaining, bl[0][1])
                bl[0][1] -= take
                remaining -= take
                if bl[0][1] == 0:
                    bl.popleft()
            unmet_today = d - remaining
            if unmet_today > 0:
                bl.append([day, unmet_today])
            self.r_demand[r][day] = d
            self.r_served[r][day] = served
            total_demand += d
            total_served += served
        self.c.served_units += total_served
        self.c.lost_units += lost_today
        self.d_demand[day] = total_demand
        self.d_served[day] = total_served
        self.d_lost[day] = lost_today
        self.d_fill[day] = min(total_served / total_demand, 1.0) if total_demand > 0 else 1.0

    def step6_production(self, day: int) -> None:
        listed = bool(self.world.shortage_listed[day])
        for sid, rt in self.rt.sites.items():
            if rt.reserved and rt.activation_due(day):
                u = (
                    float(
                        self.streams.generator(
                            RandomStream.ACTIVATION, sid, rt.activation_attempts
                        ).random()
                    )
                    if rt.activation_failure_probability > 0.0
                    else 1.0
                )
                if rt.advance_activation(day, u):
                    self.c.activations += 1
                    self._log(day, "activate", sid, rt.campaign_batches)
                else:
                    self.c.activation_failures += 1
                    self._log(day, "activation_failed", sid, rt.activation_attempts)
            exercising = False
            if rt.exercise_due(day):
                rt.start_exercise(day)
                exercising = True
            cap = float(self.site_cap[sid][day])
            if not rt.can_start(day, cap, listed):
                continue
            daily = self._site_daily_demand(sid, day)
            position = (
                self.book.on_hand(sid)
                + self._queued_saleable(sid)
                + self._in_transit_units(origin_id=sid)
            )
            backlog = sum(u for r in rt.serves_region_ids for _, u in self.backlog[r])
            if position >= rt.fg_target_days * daily and backlog == 0 and not rt.reserved:
                continue
            if exercising:
                self.c.exercise_batches += 1
                self._log(day, "exercise", sid, 1)
            filled = round(rt.spec.batch_size_units)
            need = {"api": filled, "vial": filled, "stopper_seal": filled}
            store = self.materials[sid]
            if not store.can_consume(need):
                self.c.material_stockouts += 1
                continue
            store.consume(need)
            ordinal, completion = rt.start_batch(day, cap)
            qb = disposition(
                batch_id=f"{sid}:{ordinal}",
                site_id=sid,
                ordinal=ordinal,
                filled_units=filled,
                start_day=day,
                completion_day=completion,
                yield_mean=rt.spec.yield_fraction,
                components=rt.spec.release_time_components_days,
                qp=self.qp,
                ra=self.rt.release_assurance,
                streams=self.streams,
                pathway="p503b" if rt.is_503b() else "approved_cmo",
            )
            self.queue.append(qb)
            self.c.batches_started += 1
            self.c.produced_filled += filled
            self.c.produced_saleable += qb.saleable_units
            if qb.rejected:
                self.c.rejections += 1
                self.c.rejected_units += int(np.floor(filled * rt.spec.yield_fraction))
            if qb.deviation:
                self.c.deviations += 1
                self.ledger.quality_testing += self.investigation_cost
            if qb.abstained:
                self.c.abstentions += 1
            if qb.wrong_release:
                self.c.wrong_releases += 1
            self.ledger.variable_production += filled * self.unit_value
            self._log(day, "batch", sid, filled)

    def step7_policies(self, day: int) -> None:
        listed = bool(self.world.shortage_listed[day])
        total_daily = sum(self._mean_daily(r, day) for r in self.regions)
        network_stock = self.book.total() + self._in_transit_units()
        days_of_supply = network_stock / total_daily if total_daily > 0 else float("inf")
        for rt in self.rt.sites.values():
            if rt.reserved and days_of_supply < rt.activation_threshold_days:
                rt.request_activation(day)
        requests: dict[str, int] = {}
        for r in self.regions:
            pol = self.rt.region_policies[r].policy
            position = self.book.on_hand(f"{r}:stock") + self._in_transit_units(region_id=r)
            requests[r] = pol.order_quantity(self._mean_daily(r, day), position)
        for pass_idx in (0, 1):
            by_site: dict[str, dict[str, int]] = {}
            for r, q in requests.items():
                if q <= 0:
                    continue
                order = self.rt.region_policies[r].source_order
                candidates = order[:1] if pass_idx == 0 else order[1:]
                for sid in candidates:
                    rt = self.rt.sites[sid]
                    if not rt.exists(day):
                        continue
                    if self.book.on_hand(sid, allow_503b=listed) > 0:
                        by_site.setdefault(sid, {})[r] = q
                        break
            for sid, reqs in by_site.items():
                avail = self.book.on_hand(sid, allow_503b=listed)
                alloc = allocate(
                    reqs,
                    avail,
                    self.rt.allocation_policy,
                    criticality={r: self.rt.region_policies[r].criticality_weight for r in reqs},
                    # NEW-2 (revision R009): a minimum regional guarantee is what makes the
                    # minimum_guarantee policy differ from proportional. It is expressed as
                    # a fraction of the region's own request.
                    minimum_guarantee={
                        r: round(self.rt.region_policies[r].minimum_guarantee_fraction * float(q))
                        for r, q in reqs.items()
                    },
                )
                for r, q in alloc.items():
                    if q <= 0:
                        continue
                    emergency = (
                        pass_idx == 1
                        and self.book.on_hand(f"{r}:stock", allow_503b=listed) == 0
                        and bool(self.backlog[r])
                        and self.rt.emergency_transfers
                    )
                    self._ship(day, sid, r, q, emergency)
                    requests[r] -= q
        for sid, rt in self.rt.sites.items():
            if rt.exists(day):
                daily = self._site_daily_demand(sid, day) / max(rt.spec.yield_fraction, 1e-9)
                self.materials[sid].place_orders(day, daily)

    def _ship(self, day: int, site_id: str, region_id: str, units: int, emergency: bool) -> None:
        lane = next(
            ln
            for ln in self.rt.topology.lanes
            if ln.origin_id == site_id and ln.destination_region_id == region_id
        )
        listed = bool(self.world.shortage_listed[day])
        taken = self.book.issue(site_id, units, day, allow_503b=listed)
        mult = float(self.world.transport_multiplier[lane.id][day])
        if emergency and lane.emergency_days is not None:
            days = max(round(lane.emergency_days), 1)
            cost = lane.emergency_cost_usd_per_unit or lane.cost_usd_per_unit
            self.c.emergency_shipments += 1
        else:
            days = max(round(lane.days * mult), 1)
            cost = lane.cost_usd_per_unit
        for lot, q in taken:
            self.transit.append(
                Shipment(
                    region_id,
                    site_id,
                    q,
                    day + days,
                    lot.release_day,
                    lot.expiry_day,
                    lot.unit_value_usd,
                    lot.pathway,
                    emergency,
                )
            )
            self.c.shipped_units += q
            self.ledger.inventory_logistics += q * cost
        self._log(
            day,
            "ship" if not emergency else "emergency",
            f"{site_id}->{region_id}",
            sum(q for _, q in taken),
        )

    def step8_costs(self, day: int) -> None:
        # MD-6 (revision R004): capital and validation are sunk from day zero, because the
        # money is spent building and qualifying the site before it opens. Operating cost is
        # not incurred before the site operates, so fixed site operations start at exists().
        for sid, rt in self.rt.sites.items():
            self.ledger.capital_annualized += (
                self.rt.site_capital_usd[sid] * self.crf / DAYS_PER_YEAR
            )
            self.ledger.product_site_launch += (
                self.rt.site_validation_usd[sid] * self.crf / DAYS_PER_YEAR
            )
            if rt.exists(day):
                self.ledger.fixed_site_operations += (
                    self.rt.site_fixed_usd_per_year[sid] / DAYS_PER_YEAR
                )
                self.ledger.os_integration += self.os_cost / DAYS_PER_YEAR
                # MD-21 (revision R007): a reservation fee and a take-or-pay commitment buy
                # access to a line. Before the line is qualified there is no line to access:
                # `exercise_due` and `can_start` both require exists(day), so nothing is
                # bought. R005 put this guard on fixed operations and did not extend it to
                # the contract lines, which charged a design like S16 for 540 days of
                # unavailable capacity. Capital and validation stay sunk from day zero.
                self.ledger.resilience_contracts += (
                    self.rt.reserved_fee_usd_per_year.get(sid, 0.0) / DAYS_PER_YEAR
                )
                self.ledger.resilience_contracts += (
                    self.rt.take_or_pay_usd_per_year.get(sid, 0.0) / DAYS_PER_YEAR
                )
        inv_value = self.book.value() + sum(sh.units * sh.unit_value_usd for sh in self.transit)
        # raw-material stock (API, vial, stopper) valued at the materials cost split equally
        # across the three components (MD-1, revision R003); open orders carry nothing
        material_value = sum(
            sum(store.stock.values()) * self.material_unit_value
            for store in self.materials.values()
        )
        self.ledger.inventory_logistics += (
            (inv_value + material_value) * self.carrying_rate / DAYS_PER_YEAR
        )

    def step9_assert(self, day: int) -> None:
        lhs = self.c.initial_units + self.c.produced_saleable
        rhs = (
            self.book.total()
            + self._in_transit_units()
            + self._queued_saleable()
            + self.c.expired_units
            + self.c.served_units
        )
        if lhs != rhs:
            raise AssertionError(f"mass balance violated on day {day}: {lhs} != {rhs}")
        if self.book.total() < 0 or any(sh.units < 0 for sh in self.transit):
            raise AssertionError("negative inventory")

    def run(self) -> None:
        for day in range(self.n_days):
            self.step1_expire(day)
            # step 2 (demand) is pre-generated from the shared world
            self.step3_disruption_counters(day)
            self.step4_receive(day)
            self.step5_serve(day)
            self.step6_production(day)
            self.step7_policies(day)
            self.step8_costs(day)
            self.step9_assert(day)

    # ------------------------------------------------------------------ metrics
    def episodes(self, start: int) -> list[dict[str, float]]:
        tau = self.s.shortage_day_threshold
        w = self.s.recovery_window_days
        fill = self.d_fill[start:]
        gap = np.maximum(self.d_demand[start:] - self.d_served[start:], 0)
        out: list[dict[str, float]] = []
        t = 0
        n = fill.shape[0]
        while t < n:
            if fill[t] >= tau:
                t += 1
                continue
            s0 = t
            first_response: int | None = None
            stable: int | None = None
            u = t
            while u < n:
                if fill[u] >= tau and first_response is None:
                    first_response = u
                if fill[u] >= tau and u + w <= n and bool(np.all(fill[u : u + w] >= tau)):
                    stable = u
                    break
                u += 1
            end = stable if stable is not None else n
            out.append(
                {
                    "start_day": float(s0),
                    "time_to_first_response_days": float(first_response - s0)
                    if first_response is not None
                    else float("nan"),
                    "time_to_stable_recovery_days": float(stable - s0)
                    if stable is not None
                    else float("nan"),
                    "unmet_area_units": float(gap[s0:end].sum()),
                    "peak_unmet_units": float(gap[s0:end].max()) if end > s0 else 0.0,
                    "recovered": 1.0 if stable is not None else 0.0,
                }
            )
            t = end + 1
        return out

    def _commissioning_window_loss(self, warm_up: int) -> float:
        """Capacity-weighted share of the measured window during which a site did not exist.

        Zero means every durable site was producing from the first measured day, which is
        what happens when a commissioning time equals ``warm_up_days``: the site is built
        during warm-up and its lead time costs nothing inside the window the metrics cover
        (model defect MD-17). Reporting it on every run makes that visible rather than
        leaving a commissioning comparison to look free.
        """
        measured = self.n_days - warm_up
        if measured <= 0:
            return 0.0
        total = 0.0
        lost = 0.0
        for rt in self.rt.sites.values():
            if rt.reserved or rt.is_503b() or rt.batches_per_year <= 0:
                continue
            weight = rt.batches_per_year * rt.spec.batch_size_units
            total += weight
            missing = min(max(rt.available_from_day - warm_up, 0), measured)
            lost += weight * missing
        return lost / (total * measured) if total > 0 else 0.0

    def result(self, strategy_id: str, run_index: int) -> RunResult:
        w0 = self.s.warm_up_days
        years = (self.n_days - w0) / DAYS_PER_YEAR
        demand = int(self.d_demand[w0:].sum())
        served = int(self.d_served[w0:].sum())
        # protocol B1: fulfilled = demand met within the backorder window, attributed to origin day
        # MD-6 (revision R004): backlog still open at the end of the measured window used to be
        # counted as lost at any age, which charged the last week of demand to the strategy
        # even though it had not yet had its backorder window to fill it. Only backlog that
        # has already outlived the window is lost; the rest is reported as still open.
        lost_origin = self.lost_by_origin.copy()
        r_lost_origin = {r: a.copy() for r, a in self.r_lost_by_origin.items()}
        last_day = self.n_days - 1
        open_backlog = 0
        for r, bl in self.backlog.items():
            for origin, units in bl:
                if last_day - origin > self.backorder_window:
                    lost_origin[origin] += units
                    r_lost_origin[r][origin] += units
                else:
                    open_backlog += units
        lost = int(lost_origin[w0:].sum())
        fill_rate = (demand - lost) / demand if demand > 0 else 1.0
        shortage_days = int((self.d_fill[w0:] < self.s.shortage_day_threshold).sum())
        gap = np.maximum(self.d_demand[w0:] - self.d_served[w0:], 0)
        regional: dict[str, dict[str, float]] = {}
        for r in self.regions:
            dr = int(self.r_demand[r][w0:].sum())
            sr = int(self.r_served[r][w0:].sum())
            lr = int(r_lost_origin[r][w0:].sum())
            regional[r] = {
                "fill_rate": (dr - lr) / dr if dr > 0 else 1.0,
                "demand": float(dr),
                "served": float(sr),
                "unmet": float(lr),
            }
        eps = self.episodes(w0)
        rec = [e["time_to_stable_recovery_days"] for e in eps if e["recovered"] == 1.0]
        first = [
            e["time_to_first_response_days"]
            for e in eps
            if not np.isnan(e["time_to_first_response_days"])
        ]
        share = (self.n_days - w0) / self.n_days
        ledger = CostLedger(
            capital_annualized=self.ledger.capital_annualized * share / years,
            fixed_site_operations=self.ledger.fixed_site_operations * share / years,
            product_site_launch=self.ledger.product_site_launch * share / years,
            variable_production=self.ledger.variable_production * share / years,
            opening_inventory=self.ledger.opening_inventory * share / years,
            quality_testing=self.ledger.quality_testing * share / years,
            failure_waste=self.ledger.failure_waste * share / years,
            inventory_logistics=self.ledger.inventory_logistics * share / years,
            resilience_contracts=self.ledger.resilience_contracts * share / years,
            os_integration=self.ledger.os_integration * share / years,
        )
        ledger.check_nonnegative()
        total = ledger.total()
        delivered_per_year = served / years
        metrics: dict[str, float] = {
            "annual_total_cost": total,
            "cost_per_delivered_unit": total / delivered_per_year
            if delivered_per_year > 0
            else float("inf"),
            "fill_rate": fill_rate,
            "shortage_days_per_year": shortage_days / years,
            "shortage_days": float(shortage_days),
            "unmet_units_per_year": lost / years,
            "immediate_fill_rate": min(served / demand, 1.0) if demand > 0 else 1.0,
            "peak_shortfall_units": float(gap.max()) if gap.size else 0.0,
            "open_backlog_units_at_horizon": float(open_backlog),
            "episodes": float(len(eps)),
            "time_to_first_response_median_days": float(np.median(first)) if first else 0.0,
            "time_to_stable_recovery_median_days": float(np.median(rec)) if rec else 0.0,
            "episodes_recovered_fraction": (sum(1 for e in eps if e["recovered"] == 1.0) / len(eps))
            if eps
            else 1.0,
            "meets_fill_rate": 1.0 if fill_rate >= self.s.fill_rate_mean_min else 0.0,
            "regional_disparity_fill_rate": regional_disparity(
                {r: v["fill_rate"] for r, v in regional.items()}
            ),
            "expiry_rate": self.c.expired_units
            / max(self.c.released_units + self.c.initial_units, 1),
            "batches_started_per_year": self.c.batches_started / (self.n_days / DAYS_PER_YEAR),
            "deviations": float(self.c.deviations),
            "rejections": float(self.c.rejections),
            "abstentions": float(self.c.abstentions),
            "wrong_releases": float(self.c.wrong_releases),
            "emergency_shipments": float(self.c.emergency_shipments),
            "site_failure_days": float(self.c.site_failure_days),
            "common_cause_days": float(self.c.common_cause_days),
            "supplier_disruption_days": float(self.c.supplier_disruption_days),
            "material_stockouts": float(self.c.material_stockouts),
            "capacity_days_lost_to_commissioning_fraction": self._commissioning_window_loss(w0),
            "activations": float(self.c.activations),
            "activation_failures": float(self.c.activation_failures),
            "exercise_batches": float(self.c.exercise_batches),
            "p503b_eligible_days": float(self.c.p503b_eligible_days),
            "served_units": float(served),
            "demand_units": float(demand),
        }
        digest = hashlib.sha256("\n".join(self.events).encode()).hexdigest()
        return RunResult(
            strategy_id,
            run_index,
            metrics,
            regional,
            ledger,
            self.c,
            eps,
            digest,
            self.d_fill.copy(),
            self.d_demand.copy(),
            self.d_served.copy(),
            notes=list(self.rt.notes),
        )


def simulate_run(
    runtime: StrategyRuntime,
    product: ProductConfig,
    glob: ParameterSet,
    world: ExogenousWorld,
    streams: RunStreams,
    settings: SimSettings,
) -> RunResult:
    sim = _Sim(runtime, product, glob, world, streams, settings)
    sim.run()
    return sim.result(runtime.design.id.value, streams.run_index)


def world_for_run(
    glob: ParameterSet,
    settings: SimSettings,
    master_seed: int,
    run_index: int,
    designs: list[StrategyDesign] | None = None,
) -> tuple[ExogenousWorld, RunStreams]:
    """One exogenous world for the universal roster plus any entity the given designs add.

    Entity-keyed streams mean adding an entity never changes another entity's draws, so
    the world a frozen strategy sees is identical whether or not design-space strategies
    are in the batch (tested in ``test_reproducibility``).
    """
    streams = RunStreams(master_seed, run_index)
    params = WorldParams.from_parameters(
        glob, settings.horizon_days, settings.shortage_listed_at_t0
    )
    world = generate_world(params, universal_roster_ids(settings.n_regions, designs), streams)
    return world, streams


def run_paired(
    designs: list[StrategyDesign],
    product: ProductConfig,
    glob: ParameterSet,
    settings: SimSettings,
    master_seed: int,
    run_indices: list[int],
    release_assurance_by_strategy: dict[str, ReleaseAssuranceParams] | None = None,
) -> list[RunResult]:
    """Every strategy faces the same world in each run (common random numbers)."""
    results: list[RunResult] = []
    for run_index in run_indices:
        world, streams = world_for_run(glob, settings, master_seed, run_index, designs)
        for design in designs:
            ra = (release_assurance_by_strategy or {}).get(design.id.value)
            runtime = build_strategy(
                design,
                product,
                glob,
                n_regions=settings.n_regions,
                release_assurance=ra,
                shortage_listed_at_t0=settings.shortage_listed_at_t0,
                commissioning_offset_days=(
                    float(settings.warm_up_days)
                    if settings.commissioning_from_measurement_start
                    else 0.0
                ),
            )
            results.append(simulate_run(runtime, product, glob, world, streams, settings))
    return results
