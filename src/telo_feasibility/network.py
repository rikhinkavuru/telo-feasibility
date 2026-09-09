"""Network topology: regions, sites, suppliers, components, lanes, common-cause groups.

The universal roster (every entity any strategy can instantiate) is what the exogenous
world is generated for, so that strategies with different site counts share one world.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .schemas import (
    CommonCauseGroup,
    Component,
    ComponentKind,
    DemandRegion,
    ManufacturingSite,
    Pathway,
    Supplier,
    TransportLane,
)


@dataclass
class NetworkTopology:
    regions: list[DemandRegion]
    sites: list[ManufacturingSite]
    suppliers: list[Supplier]
    components: list[Component]
    lanes: list[TransportLane]
    common_cause_groups: list[CommonCauseGroup] = field(default_factory=list)

    def region(self, rid: str) -> DemandRegion:
        for r in self.regions:
            if r.id == rid:
                return r
        raise KeyError(rid)

    def site(self, sid: str) -> ManufacturingSite:
        for s in self.sites:
            if s.id == sid:
                return s
        raise KeyError(sid)

    def supplier(self, sid: str) -> Supplier:
        for s in self.suppliers:
            if s.id == sid:
                return s
        raise KeyError(sid)

    def lanes_from(self, origin_id: str) -> list[TransportLane]:
        return [ln for ln in self.lanes if ln.origin_id == origin_id]

    def lanes_to(self, region_id: str) -> list[TransportLane]:
        return [ln for ln in self.lanes if ln.destination_region_id == region_id]

    def groups_of(self, member_id: str) -> list[CommonCauseGroup]:
        return [g for g in self.common_cause_groups if member_id in g.member_ids]

    def validate(self) -> None:
        ids = (
            [r.id for r in self.regions]
            + [s.id for s in self.sites]
            + [s.id for s in self.suppliers]
            + [c.id for c in self.components]
            + [ln.id for ln in self.lanes]
        )
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate entity ids across the topology")
        share = sum(r.share for r in self.regions)
        if abs(share - 1.0) > 1e-9:
            raise ValueError(f"region shares sum to {share}, not 1")
        region_ids = {r.id for r in self.regions}
        site_ids = {s.id for s in self.sites}
        supplier_ids = {s.id for s in self.suppliers}
        for ln in self.lanes:
            if ln.destination_region_id not in region_ids:
                raise ValueError(f"lane {ln.id} destination {ln.destination_region_id} unknown")
            if ln.origin_id not in site_ids:
                raise ValueError(f"lane {ln.id} origin {ln.origin_id} unknown")
        for s in self.sites:
            if s.region_id not in region_ids:
                raise ValueError(f"site {s.id} region {s.region_id} unknown")
            for sup in s.supplier_ids:
                if sup not in supplier_ids:
                    raise ValueError(f"site {s.id} supplier {sup} unknown")
            if not self.lanes_from(s.id):
                raise ValueError(f"site {s.id} has no outbound lane")
        for r in self.regions:
            if not self.lanes_to(r.id):
                raise ValueError(f"region {r.id} has no inbound lane")
        all_ids = set(ids)
        for g in self.common_cause_groups:
            for m in g.member_ids:
                if m not in all_ids:
                    raise ValueError(f"common-cause group {g.id} member {m} unknown")


@dataclass(frozen=True)
class SiteSpec:
    """Compact site description used by strategy builders."""

    id: str
    region_id: str
    archetype: str
    scale: float  # multiplier on nominal batches per year
    batch_size_units: float
    exists_at_t0: bool
    commissioning_lead_time_days: float
    supplier_ids: tuple[str, ...]
    common_cause_groups: tuple[str, ...]
    pathway: Pathway = Pathway.APPROVED_CMO
    capital_multiplier: float = 1.0
    fixed_cost_multiplier: float = 1.0
    validation_multiplier: float = 1.0


def default_regions(
    n: int, criticality_spread: float = 0.0, minimum_guarantee_fraction: float = 0.0
) -> list[DemandRegion]:
    """Equal-share regions R1..Rn (the base case; shares are replaced by data when available).

    ``criticality_spread`` makes regions differ in allocation priority: 0.0 leaves every
    region at weight 1.0, which is the frozen base case, and a positive value spreads the
    weights linearly from ``1 - spread`` at R1 to ``1 + spread`` at Rn. It exists because
    with identical regions the four allocation policies in ``allocation.allocate`` are
    arithmetically the same function (defect NEW-2), so allocation rights cannot be
    measured at all. No evidence in this package says regions differ, so the default keeps
    them identical; a real spread needs hospital and GPO evidence (HA-20, HA-33).
    """
    if n < 1:
        raise ValueError("need at least one region")
    if not 0.0 <= criticality_spread <= 1.0:
        raise ValueError("criticality spread must be between 0 and 1")
    if not 0.0 <= minimum_guarantee_fraction <= 1.0:
        raise ValueError("minimum guarantee fraction must be between 0 and 1")
    out: list[DemandRegion] = []
    for i in range(n):
        w = 1.0 if n == 1 else 1.0 - criticality_spread + 2.0 * criticality_spread * i / (n - 1)
        out.append(
            DemandRegion(
                id=f"R{i + 1}",
                name=f"Region {i + 1}",
                share=1.0 / n,
                criticality_weight=w,
                minimum_guarantee_fraction=minimum_guarantee_fraction,
            )
        )
    return out


def default_components() -> list[Component]:
    return [
        Component(
            id="api",
            name="active pharmaceutical ingredient",
            kind=ComponentKind.API,
            supplier_ids=[],
            quantity_per_unit=1.0,
            quantity_unit="dose-equivalent",
        ),
        Component(
            id="vial",
            name="glass vial",
            kind=ComponentKind.VIAL,
            supplier_ids=[],
            quantity_per_unit=1.0,
            quantity_unit="each",
        ),
        Component(
            id="stopper_seal",
            name="stopper and seal",
            kind=ComponentKind.STOPPER,
            supplier_ids=[],
            quantity_per_unit=1.0,
            quantity_unit="each",
        ),
    ]
