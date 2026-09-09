"""Inventory: released lots by location and expiry cohort, FEFO issue, expiry, policies.

Units are integers so the mass-balance identity is exact.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Lot:
    id: str
    location_id: str
    units: int
    release_day: int
    expiry_day: int
    unit_value_usd: float
    pathway: str = "approved_cmo"  # lots compounded under 503B carry 'p503b'


@dataclass
class InventoryBook:
    lots: dict[str, list[Lot]] = field(default_factory=dict)
    expired_units: int = 0
    expired_value_usd: float = 0.0

    def add(self, lot: Lot) -> None:
        if lot.units < 0:
            raise ValueError("negative lot")
        if lot.units == 0:
            return
        bucket = self.lots.setdefault(lot.location_id, [])
        bucket.append(lot)
        bucket.sort(key=lambda x: (x.expiry_day, x.release_day, x.id))

    def on_hand(self, location_id: str, allow_503b: bool = True) -> int:
        return sum(
            x.units for x in self.lots.get(location_id, []) if allow_503b or x.pathway != "p503b"
        )

    def total(self) -> int:
        return sum(x.units for b in self.lots.values() for x in b)

    def value(self, location_id: str | None = None) -> float:
        buckets = [self.lots.get(location_id, [])] if location_id else list(self.lots.values())
        return sum(x.units * x.unit_value_usd for b in buckets for x in b)

    def issue(
        self, location_id: str, units: int, day: int, allow_503b: bool = True
    ) -> list[tuple[Lot, int]]:
        """Issue up to ``units`` first-expire-first-out; returns (lot, units taken) pairs."""
        if units < 0:
            raise ValueError("negative issue")
        taken: list[tuple[Lot, int]] = []
        remaining = units
        bucket = self.lots.get(location_id, [])
        for lot in bucket:
            if remaining == 0:
                break
            if lot.expiry_day <= day or lot.units == 0:
                continue
            if not allow_503b and lot.pathway == "p503b":
                continue
            q = min(lot.units, remaining)
            lot.units -= q
            remaining -= q
            taken.append((lot, q))
        self.lots[location_id] = [x for x in bucket if x.units > 0]
        return taken

    def expire(self, day: int) -> int:
        """Remove lots whose expiry day has arrived; returns expired units."""
        expired = 0
        for loc, bucket in self.lots.items():
            keep: list[Lot] = []
            for lot in bucket:
                if lot.expiry_day <= day:
                    expired += lot.units
                    self.expired_value_usd += lot.units * lot.unit_value_usd
                else:
                    keep.append(lot)
            self.lots[loc] = keep
        self.expired_units += expired
        return expired

    def transfer(self, lot: Lot, units: int, to_location: str, new_id: str) -> Lot:
        """Create a child lot at another location (used when a shipment arrives)."""
        child = Lot(
            new_id,
            to_location,
            units,
            lot.release_day,
            lot.expiry_day,
            lot.unit_value_usd,
            lot.pathway,
        )
        self.add(child)
        return child


@dataclass(frozen=True)
class OrderUpToPolicy:
    """Order-up-to policy in days of expected demand with a reorder point in days."""

    target_days: float
    reorder_point_days: float

    def order_quantity(self, mean_daily_demand: float, inventory_position: int) -> int:
        if mean_daily_demand <= 0:
            return 0
        target = round(self.target_days * mean_daily_demand)
        rop = self.reorder_point_days * mean_daily_demand
        if inventory_position <= rop:
            return max(target - inventory_position, 0)
        return 0
