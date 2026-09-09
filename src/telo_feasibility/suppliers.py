"""Raw-material and component inventory per site, purchase orders, supplier disruptions."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class PurchaseOrder:
    component_id: str
    supplier_id: str
    units: int  # units still outstanding
    planned_arrival_day: int
    original_units: int = 0  # units at placement; the daily ceiling under a degraded supplier

    def __post_init__(self) -> None:
        if self.original_units <= 0:
            self.original_units = self.units


@dataclass
class MaterialStore:
    """Component stock at one site with a per-component supplier and an order-up-to policy."""

    site_id: str
    stock: dict[str, int]
    supplier_for: dict[str, str]
    lead_time_days: dict[str, float]
    target_days: float
    reorder_point_days: float
    # MD-2 (revision R004): the reorder point is expressed in days of mean demand, so at a
    # short lead time it can fall below a single batch's component draw and the store stalls,
    # ordering only after it is already unable to start a batch. The reorder point covers at
    # least one batch.
    batch_units: int = 0
    open_orders: list[PurchaseOrder] = field(default_factory=list)
    units_ordered: int = 0
    units_received: int = 0
    delayed_order_days: int = 0

    def position(self, component_id: str) -> int:
        return self.stock.get(component_id, 0) + sum(
            o.units for o in self.open_orders if o.component_id == component_id
        )

    def can_consume(self, units_per_component: dict[str, int]) -> bool:
        return all(self.stock.get(c, 0) >= u for c, u in units_per_component.items())

    def consume(self, units_per_component: dict[str, int]) -> None:
        for c, u in units_per_component.items():
            if self.stock.get(c, 0) < u:
                raise RuntimeError(f"site {self.site_id}: insufficient {c}")
            self.stock[c] -= u

    def place_orders(self, day: int, daily_consumption: float) -> list[PurchaseOrder]:
        placed: list[PurchaseOrder] = []
        if daily_consumption <= 0:
            return placed
        for c, sup in self.supplier_for.items():
            lt = self.lead_time_days.get(c, 0.0)
            # MD-1 (revision R009): separate the physics from the policy. Pipeline cover is
            # lead-time demand and belongs to the supplier; safety and cycle cover are the
            # buyer's policy and must not shrink when the lead shortens. The previous form
            # set both the reorder point and the order-up-to level to (policy + lead) days,
            # so cutting a lead cut the buffer, and the two lead-time ablation factors came
            # out with the wrong sign in 13 and 14 of 16 cells: a supplier that promises
            # faster resupply appeared to make service worse. During a disruption nothing
            # arrives whatever the nominal lead, so the only protection is the position
            # held, and that position must be set by policy.
            pipeline = lt * daily_consumption
            safety = self.reorder_point_days * daily_consumption
            rop = max(pipeline + safety, float(self.batch_units))
            target = round(max(rop + self.target_days * daily_consumption, rop))
            if self.position(c) <= rop:
                qty = max(target - self.position(c), 0)
                if qty > 0:
                    po = PurchaseOrder(c, sup, qty, day + round(lt))
                    self.open_orders.append(po)
                    self.units_ordered += qty
                    placed.append(po)
        return placed

    def receive(self, day: int, supplier_capacity: dict[str, np.ndarray]) -> int:
        """Receive due orders at the supplier's capacity fraction for the day.

        MD-19 (revision R007). A supplier's daily capacity is a fraction, not a switch.
        A supplier-specific disruption drives it to 0.0, but a common-cause group sets its
        members to ``1 - impact`` with impact drawn from a Beta of mean 0.5, so a group
        capacity never reaches zero. Gating shipment on ``cap > 0`` therefore made every
        common-cause group declared on a *supplier* structurally inert: a degraded day
        still shipped the whole order, so a shared upstream tier (a key starting material,
        a shared container source) could not reach the material channel at all.

        A supplier at capacity fraction ``f`` now ships at most ``f`` of one full order per
        day, so an order takes ``1 / f`` times as long to complete. That is the same
        proportional time stretch ``SiteRuntime.start_batch`` already applies to a degraded
        line (``occupancy / capacity_fraction``), so sites and suppliers read the fraction
        the same way. ``f = 1`` and ``f = 0`` behave exactly as before the revision.

        Fixing the structure does not by itself make the mechanism visible: at the frozen
        illustrative hazard rate (0.1 common-cause events per group-year) and the slack the
        illustrative networks carry, the measured effect on S9's matched-membership control
        is zero. The defect was that no parameter value could ever have made it non-zero.
        """
        received = 0
        keep: list[PurchaseOrder] = []
        for po in self.open_orders:
            if day >= po.planned_arrival_day:
                cap = supplier_capacity.get(po.supplier_id)
                fraction = (
                    1.0
                    if cap is None or day >= cap.shape[0]
                    else max(0.0, min(1.0, float(cap[day])))
                )
                ship = min(po.units, int(po.original_units * fraction))
                if ship > 0:
                    self.stock[po.component_id] = self.stock.get(po.component_id, 0) + ship
                    received += ship
                    po.units -= ship
                if po.units <= 0:
                    continue
                self.delayed_order_days += 1
            keep.append(po)
        self.open_orders = keep
        self.units_received += received
        return received
