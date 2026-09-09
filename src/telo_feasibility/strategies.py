"""Strategy builders: StrategyDesign + product + global parameters -> runtime topology and policies.

Geography is deliberately simple in the base case: N equal regions R1..RN; a central plant
sits in R1; a regional node sits in its own region; transit is 1 day within a region and
``delivery_days`` (design variable) across regions. Common-cause groups: every site that
shares the API supplier is in ``cc_api``; distributed nodes additionally share ``cc_os``
(one software/model version) and ``cc_quality`` (one quality unit) by default.

S7 is modeled as the status-quo network plus 503B responder capacity; it is not a
durable architecture on its own.

Design-space strategies (S8+, 2026-09 assignment) declare their sites in configuration
(``StrategyDesign.site_plans``) and go through the same runtime builder; S0-S7 keep the
code-defined topologies above, byte for byte (``tests/regression/test_frozen_strategies.py``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .configs import ProductConfig
from .disruptions import DAYS_PER_YEAR, Roster
from .economics import crf
from .inventory import OrderUpToPolicy
from .network import NetworkTopology, default_components, default_regions
from .production import SiteRuntime
from .release_assurance import ReleaseAssuranceParams
from .schemas import (
    CommonCauseGroup,
    Confidence,
    EvidenceTier,
    ManufacturingSite,
    ParameterSet,
    Pathway,
    ReleaseScenario,
    StrategyDesign,
    StrategyId,
    Supplier,
    TransportLane,
    UncertainParameter,
    Unit,
    ValidationStatus,
)


@dataclass
class RegionPolicy:
    region_id: str
    policy: OrderUpToPolicy
    source_order: list[str]  # site ids in priority order
    criticality_weight: float = 1.0
    minimum_guarantee_fraction: float = 0.0


@dataclass
class StrategyRuntime:
    design: StrategyDesign
    topology: NetworkTopology
    sites: dict[str, SiteRuntime]
    region_policies: dict[str, RegionPolicy]
    allocation_policy: str
    release_assurance: ReleaseAssuranceParams
    initial_region_stock_days: float
    initial_site_stock_days: float
    material_target_days: float
    material_reorder_point_days: float
    emergency_transfers: bool
    shelf_life_days: float
    bud_503b_days: float
    site_capital_usd: dict[str, float]
    site_fixed_usd_per_year: dict[str, float]
    site_validation_usd: dict[str, float]
    reserved_fee_usd_per_year: dict[str, float] = field(default_factory=dict)
    take_or_pay_usd_per_year: dict[str, float] = field(default_factory=dict)
    deviation_rate_factor: float = 1.0
    investigation_duration_factor: float = 1.0
    notes: list[str] = field(default_factory=list)

    def roster(self) -> Roster:
        t = self.topology
        return Roster(
            region_ids=tuple(r.id for r in t.regions),
            site_ids=tuple(s.id for s in t.sites),
            supplier_ids=tuple(s.id for s in t.suppliers),
            lane_ids=tuple(ln.id for ln in t.lanes),
            group_ids=tuple(g.id for g in t.common_cause_groups),
        )


# What an incumbent plant already runs on day zero. The workbook's status-quo strategy sets
# capacity_factor 1.05, meaning the plant runs 5% above nominal (WB-29), so anything above
# that is an expansion that has to be built and qualified (model defect MD-7, revision R004).
STATUS_QUO_SCALE = 1.05


def _lead_param(days: float) -> UncertainParameter:
    return UncertainParameter(
        id="supplier.lead_time_days",
        definition="procurement lead time",
        units=Unit.DAYS,
        entity_level="supplier",
        base=days,
        evidence_tier=EvidenceTier.ILLUSTRATIVE,
        confidence=Confidence.LOW,
        validation_status=ValidationStatus.ILLUSTRATIVE,
    )


@dataclass(frozen=True)
class SitePlan:
    id: str
    region_id: str
    archetype: str
    scale: float
    exists_at_t0: bool
    commissioning_days: float
    api_supplier: str
    pathway: Pathway = Pathway.APPROVED_CMO
    reserved: bool = False
    groups: tuple[str, ...] = ()
    # fields below are used only by configuration-declared plans (S8+); defaults reproduce S0-S7
    generic: bool = False
    vial_supplier: str = "vial_1"
    stopper_supplier: str = "stopper_1"
    batch_size_fraction: float | None = None
    serves_all: bool | None = None
    exercise_batches_per_year: float = 0.0
    activation_failure_probability: float = 0.0
    activation_lead_days: float | None = None
    capacity_share: float = 1.0
    fixed_cost_share: float = 1.0
    capital_multiplier: float = 1.0
    fixed_cost_multiplier: float = 1.0
    validation_multiplier: float = 1.0


def _plans_from_spec(
    design: StrategyDesign,
    glob: ParameterSet,
    region_ids: list[str],
    capacity_factor: float,
    dv: dict[str, float],
) -> list[SitePlan]:
    """Configuration-declared sites. ``capacity_factor`` scales every site; ``node_scale``
    (when given as a design variable) scales regional nodes on top of the declared scale."""
    plans: list[SitePlan] = []
    for sp in design.site_plans or []:
        if sp.region_id not in region_ids:
            raise ValueError(f"site {sp.id}: region {sp.region_id} not in {region_ids}")
        scale = sp.scale * capacity_factor
        if sp.archetype == "regional_node" and "node_scale" in dv:
            scale *= float(dv["node_scale"])
        commissioning = (
            sp.commissioning_days
            if sp.commissioning_days is not None
            else (0.0 if sp.exists_at_t0 else glob.base("node_commissioning_days"))
        )
        plans.append(
            SitePlan(
                sp.id,
                sp.region_id,
                sp.archetype,
                scale,
                sp.exists_at_t0,
                commissioning,
                sp.api_supplier,
                pathway=sp.pathway,
                reserved=sp.reserved,
                groups=tuple(sp.groups),
                generic=True,
                vial_supplier=sp.vial_supplier,
                stopper_supplier=sp.stopper_supplier,
                batch_size_fraction=sp.batch_size_fraction,
                serves_all=sp.serves == "all",
                exercise_batches_per_year=sp.exercise_batches_per_year,
                activation_failure_probability=sp.activation_failure_probability,
                activation_lead_days=sp.activation_lead_days,
                capacity_share=sp.portfolio_capacity_share,
                fixed_cost_share=sp.portfolio_fixed_cost_share,
                capital_multiplier=sp.capital_multiplier,
                fixed_cost_multiplier=sp.fixed_cost_multiplier,
                validation_multiplier=sp.validation_multiplier,
            )
        )
    return plans


def universal_roster_ids(n_regions: int, designs: list[StrategyDesign] | None = None) -> Roster:
    """Every entity any strategy can instantiate, so one world serves all strategies.

    The frozen roster covers S0-S7. Entities that design-space strategies declare are
    appended in sorted order; entity-keyed streams keep every frozen entity's draws fixed.
    """
    regions = tuple(f"R{i + 1}" for i in range(n_regions))
    base_sites = (
        "central",
        "second_source",
        "reserved_cdmo",
        "central_expansion",
        "p503b_1",
        *tuple(f"node_{r}" for r in regions),
    )
    base_suppliers = ("api_1", "api_2", "vial_1", "stopper_1")
    base_groups = ("cc_api_1", "cc_api_2", "cc_vial_1", "cc_os", "cc_quality", "cc_geo_R1")
    extra_sites: set[str] = set()
    extra_suppliers: set[str] = set()
    extra_groups: set[str] = set()
    for d in designs or []:
        for sp in d.site_plans or []:
            extra_sites.add(sp.id)
            extra_groups.update(sp.groups)
            extra_suppliers.update((sp.api_supplier, sp.vial_supplier, sp.stopper_supplier))
        for sup in d.extra_suppliers:
            extra_suppliers.add(sup.id)
            extra_groups.update(sup.groups)
    sites = (*base_sites, *sorted(extra_sites - set(base_sites)))
    suppliers = (*base_suppliers, *sorted(extra_suppliers - set(base_suppliers)))
    groups = (*base_groups, *sorted(extra_groups - set(base_groups)))
    lanes: list[str] = []
    for s in sites:
        for r in regions:
            lanes.append(f"{s}->{r}")
    return Roster(regions, sites, suppliers, tuple(lanes), groups)


def _group_kind(gid: str) -> str:
    if "api" in gid:
        return "api_supplier"
    if "vial" in gid:
        return "vial_supplier"
    if "stopper" in gid:
        return "stopper_seal_supplier"
    if gid == "cc_os":
        return "software_model_version"
    if gid in ("cc_quality",) or "owner" in gid or "cdmo" in gid:
        return "ownership"
    if "hub" in gid or "equipment" in gid:
        return "shared_equipment"
    if "lab" in gid:
        return "laboratory"
    if "geo" in gid:
        return "geography"
    return "other"


def build_strategy(
    design: StrategyDesign,
    product: ProductConfig,
    glob: ParameterSet,
    *,
    n_regions: int = 4,
    release_assurance: ReleaseAssuranceParams | None = None,
    shortage_listed_at_t0: bool = False,
    commissioning_offset_days: float = 0.0,
) -> StrategyRuntime:
    """Build the runtime topology for one design.

    ``commissioning_offset_days`` shifts the day a site that does not exist at t0 becomes
    available, so the caller can start the commissioning clock at the first measured day
    instead of at simulation day zero (revision R008, model defect MD-17).
    """
    p = product.parameters
    dv = design.design_variables
    regions = default_regions(
        n_regions,
        criticality_spread=float(dv.get("region_criticality_spread", 0.0)),
        minimum_guarantee_fraction=float(dv.get("region_minimum_guarantee", 0.0)),
    )
    region_ids = [r.id for r in regions]
    nominal_batches = p.base("batches_per_site_year_nominal")
    units_per_batch = p.base("units_per_batch")
    delivery_days = float(dv.get("delivery_days", 2.0))
    safety_days = float(dv.get("safety_stock_days", 30.0))
    capacity_factor = float(dv.get("capacity_factor", 1.0))
    n_sites = int(dv.get("sites", 1))
    node_scale = float(dv.get("node_scale", glob.base("node_scale_fraction")))
    rate = glob.base("discount_rate")
    life = glob.base("capital_economic_life_years")
    cap_exp = glob.base("node_capital_scale_exponent")
    fix_exp = glob.base("node_fixed_cost_scale_exponent")
    lead = p.base("material_lead_time_days")
    # vial/stopper lead time as a fraction of the API lead time (0.5 = legacy default)
    component_lead_fraction = float(dv.get("component_lead_fraction", 0.5))
    notes: list[str] = []

    independent_api = bool(dv.get("independent_api_supplier", 0.0) >= 1.0)
    plans: list[SitePlan] = []
    sid = design.id
    if sid in (StrategyId.S0, StrategyId.S1):
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                capacity_factor,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
    elif sid is StrategyId.S2:
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                capacity_factor,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
        api2 = "api_2" if independent_api else "api_1"
        g2 = ("cc_api_2" if independent_api else "cc_api_1", "cc_vial_1")
        plans.append(
            SitePlan(
                "second_source",
                region_ids[min(2, n_regions - 1)],
                "central",
                capacity_factor,
                bool(dv.get("second_source_exists_at_t0", 0.0) >= 1.0),
                glob.base("second_source_qualification_days"),
                api2,
                groups=g2,
            )
        )
        notes.append("second source shares the API supplier unless independent_api_supplier=1 (H5)")
    elif sid is StrategyId.S3:
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                capacity_factor,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
        plans.append(
            SitePlan(
                "reserved_cdmo",
                region_ids[min(1, n_regions - 1)],
                "cdmo_reserved",
                float(dv.get("reserved_capacity_fraction", 0.25)) * capacity_factor * 4.0,
                True,
                0.0,
                "api_1",
                reserved=True,
                groups=("cc_api_1",),
            )
        )
        notes.append(
            "reserved capacity = reserved_capacity_fraction x 4 x nominal batches, idle until activated"
        )
    elif sid is StrategyId.S4:
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                capacity_factor,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
        plans.append(
            SitePlan(
                "central_expansion",
                "R1",
                "central",
                capacity_factor,
                False,
                glob.base("node_commissioning_days"),
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
    elif sid in (StrategyId.S5, StrategyId.S6):
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                1.0,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
        # nodes are placed one per region and then round-robin, so a design may hold more
        # nodes than regions (model defect MD-13, revision R004). A second node in a region
        # shares that region's geography common-cause group, so redundancy inside one region
        # buys less than redundancy across regions.
        for k in range(n_sites):
            r = region_ids[k % n_regions]
            wave = k // n_regions
            node_groups: tuple[str, ...] = ("cc_api_1", "cc_vial_1", "cc_os", "cc_quality")
            if wave > 0:
                node_groups = (*node_groups, f"cc_geo_{r}")
            plans.append(
                SitePlan(
                    f"node_{r}" if wave == 0 else f"node_{r}_{wave + 1}",
                    r,
                    "regional_node",
                    node_scale * capacity_factor,
                    False,
                    glob.base("node_commissioning_days"),
                    "api_1",
                    groups=node_groups,
                )
            )
        notes.append(
            "nodes share API and vial suppliers, one OS version, and one quality unit by default (FC5)"
        )
    elif sid is StrategyId.S7:
        plans.append(
            SitePlan(
                "central",
                "R1",
                "central",
                1.05,
                True,
                0.0,
                "api_1",
                groups=("cc_api_1", "cc_vial_1", "cc_geo_R1"),
            )
        )
        plans.append(
            SitePlan(
                "p503b_1",
                "R1",
                "503b",
                (capacity_factor - 1.0) if capacity_factor > 1.0 else 0.15,
                True,
                0.0,
                "api_1",
                pathway=Pathway.P503B,
                groups=("cc_api_1",),
            )
        )
        notes.append(
            "S7 = status quo plus a 503B responder that can compound only while the product is on the FDA shortage list"
        )
    if design.site_plans is not None:
        plans = _plans_from_spec(design, glob, region_ids, capacity_factor, dv)
        notes.append(f"{sid.value}: topology declared in configuration ({len(plans)} sites)")

    sites: list[ManufacturingSite] = []
    runtimes: dict[str, SiteRuntime] = {}
    capital: dict[str, float] = {}
    fixed: dict[str, float] = {}
    validation: dict[str, float] = {}
    reserved_fee: dict[str, float] = {}
    take_or_pay: dict[str, float] = {}
    components = {
        "sterility": glob.base("sterility_incubation_days"),
        "environmental_monitoring": glob.base("environmental_monitoring_days"),
        "assay": glob.base("assay_days"),
        "endotoxin": glob.base("endotoxin_days"),
        "qa_review_serial": glob.base("qa_review_days"),
    }
    for plan in plans:
        scale = plan.scale
        # a regional node is a smaller line: batch size scales with node scale, cadence stays
        node_like = plan.archetype == "regional_node"
        if plan.generic:
            # declared plans: capacity = nominal x scale; batch size fraction defaults to the
            # node scale; only the portfolio share of capacity serves this product
            bsf = (
                plan.batch_size_fraction
                if plan.batch_size_fraction is not None
                else (scale if node_like else 1.0)
            )
            batch_units = max(round(units_per_batch * bsf), 1)
            batches_per_year = nominal_batches * scale / bsf * plan.capacity_share
        else:
            batch_units = max(round(units_per_batch * (scale if node_like else 1.0)), 1)
            batches_per_year = nominal_batches * (capacity_factor if node_like else scale)
        cap_usd = (
            p.base("capital_usd_per_site")
            * (scale**cap_exp)
            * plan.capital_multiplier
            * plan.fixed_cost_share
        )
        fix_usd = (
            p.base("fixed_qa_labor_usd_per_site_year")
            * (scale**fix_exp)
            * float(dv.get("fixed_cost_factor", 1.0))
            * plan.fixed_cost_multiplier
            * plan.fixed_cost_share
        )
        val_usd = (
            p.base("validation_usd_one_time")
            * float(dv.get("validation_factor", 1.0))
            * plan.validation_multiplier
            * plan.fixed_cost_share
        )
        site = ManufacturingSite(
            id=plan.id,
            name=plan.id,
            region_id=plan.region_id,
            archetype=plan.archetype,
            batch_size_units=batch_units,
            batches_per_year_nominal=batches_per_year,
            yield_fraction=p.base("yield_fraction"),
            uptime_fraction=p.base("uptime_fraction"),
            production_cycle_days=p.base("production_cycle_days"),
            changeover_days=p.base("changeover_days"),
            release_time_components_days=components,
            capital_usd=cap_usd,
            fixed_cost_usd_per_year=fix_usd,
            validation_cost_usd=val_usd,
            commissioning_lead_time_days=plan.commissioning_days,
            exists_at_t0=plan.exists_at_t0,
            pathway=plan.pathway,
            common_cause_groups=list(plan.groups),
            supplier_ids=[plan.api_supplier, plan.vial_supplier, plan.stopper_supplier],
        )
        sites.append(site)
        serves_all = (
            plan.serves_all if plan.serves_all is not None else plan.archetype != "regional_node"
        )
        served = tuple(region_ids) if serves_all else (plan.region_id,)
        # MD-7 (revision R004): capacity above what the site runs on day zero is an expansion.
        # It becomes available after capacity_expansion_days, the way a new site becomes
        # available after its commissioning time, so the two ways of buying capacity are
        # compared on the same terms. Contracted capacity (reserved, 503B) is not built by
        # Telo and keeps its own activation lead instead.
        baseline_batches: float | None = None
        expansion_day = 0
        eligible_for_ramp = (
            plan.exists_at_t0
            and not plan.reserved
            and plan.pathway is Pathway.APPROVED_CMO
            and scale > STATUS_QUO_SCALE
            and float(dv.get("instant_expansion", 0.0)) < 1.0
        )
        if eligible_for_ramp:
            baseline_scale = STATUS_QUO_SCALE
            if plan.generic:
                bsf_used = (
                    plan.batch_size_fraction
                    if plan.batch_size_fraction is not None
                    else (baseline_scale if node_like else 1.0)
                )
                baseline_batches = nominal_batches * baseline_scale / bsf_used * plan.capacity_share
            else:
                baseline_batches = nominal_batches * baseline_scale
            expansion_day = round(commissioning_offset_days + glob.base("capacity_expansion_days"))
            notes.append(
                f"{plan.id}: runs at the status-quo scale {baseline_scale} until day "
                f"{expansion_day}, then at its design scale {scale:.3g} (MD-7, R008 offset "
                f"{commissioning_offset_days:.0f} d)"
            )
        rt = SiteRuntime(
            spec=site,
            batches_per_year=batches_per_year,
            serves_region_ids=served,
            reserved=plan.reserved,
            activation_threshold_days=float(dv.get("activation_threshold_days", 10.0)),
            activation_lead_days=(
                plan.activation_lead_days
                if plan.activation_lead_days is not None
                else glob.base("reserved_capacity_activation_days")
            ),
            campaign_batches=int(dv.get("campaign_batches", 3)),
            available_from_day=(
                0
                if plan.exists_at_t0
                else round(commissioning_offset_days + plan.commissioning_days)
            ),
            fg_target_days=float(dv.get("site_fg_days", 30.0)),
            common_cause_groups=plan.groups,
            supplier_ids=tuple(site.supplier_ids),
            exercise_interval_days=(
                DAYS_PER_YEAR / plan.exercise_batches_per_year
                if plan.exercise_batches_per_year > 0
                else 0.0
            ),
            activation_failure_probability=plan.activation_failure_probability,
            baseline_batches_per_year=baseline_batches,
            expansion_available_day=expansion_day,
        )
        runtimes[plan.id] = rt
        # MD-14 (revision R004): a reserved line Telo does not own is somebody else's asset.
        # Charging its capital, fixed operations and validation and then a reservation fee on
        # top double counts, which the protocol's cost boundary forbids. Telo pays the fee,
        # plus variable and testing cost on the batches it actually runs. Set the design
        # variable reserved_site_owned to 1 for a standby line Telo builds and owns.
        reserved_owned = float(dv.get("reserved_site_owned", 0.0)) >= 1.0
        pays_asset = (not plan.reserved) or reserved_owned
        capital[plan.id] = cap_usd if pays_asset else 0.0
        fixed[plan.id] = fix_usd if pays_asset else 0.0
        validation[plan.id] = val_usd if pays_asset else 0.0
        if plan.reserved:
            # the fee is a share of what the line costs its owner, so the basis stays the
            # notional annual cost even when Telo carries none of it on its own ledger
            annual = fix_usd + cap_usd * crf(rate, life)
            reserved_fee[plan.id] = glob.base("reserved_capacity_fee_fraction") * annual
            if reserved_owned:
                notes.append(
                    f"{plan.id}: reserved capacity is owned, so its capital and fixed cost are "
                    "on the ledger and the reservation fee is charged on top"
                )
            # take-or-pay: a minimum purchase on the reserved line whether it runs or not.
            # Charged as a fraction of the variable cost of the reserved annual volume, so a
            # contract that guarantees the CDMO revenue shows up as cost even in quiet years.
            top_fraction = float(dv.get("take_or_pay_fraction", 0.0))
            if top_fraction > 0.0:
                reserved_units = batches_per_year * batch_units * p.base("yield_fraction")
                unit_cost = p.base("variable_materials_usd_per_unit") + p.base(
                    "variable_conversion_usd_per_unit"
                )
                take_or_pay[plan.id] = top_fraction * reserved_units * unit_cost

    suppliers = [
        Supplier(
            id="api_1",
            name="API supplier 1",
            component_ids=["api"],
            lead_time_days=_lead_param(lead),
            common_cause_groups=["cc_api_1"],
        ),
        Supplier(
            id="api_2",
            name="API supplier 2",
            component_ids=["api"],
            lead_time_days=_lead_param(lead),
            common_cause_groups=["cc_api_2"],
        ),
        Supplier(
            id="vial_1",
            name="vial supplier 1",
            component_ids=["vial"],
            lead_time_days=_lead_param(lead * component_lead_fraction),
            common_cause_groups=["cc_vial_1"],
        ),
        Supplier(
            id="stopper_1",
            name="stopper and seal supplier 1",
            component_ids=["stopper_seal"],
            lead_time_days=_lead_param(lead * component_lead_fraction),
            common_cause_groups=[],
        ),
    ]
    for extra in design.extra_suppliers:
        days = (
            extra.lead_time_days
            if extra.lead_time_days is not None
            else lead * float(extra.lead_time_factor or 0.0)
        )
        suppliers.append(
            Supplier(
                id=extra.id,
                name=extra.name,
                component_ids=list(extra.component_ids),
                lead_time_days=_lead_param(days),
                common_cause_groups=list(extra.groups),
            )
        )
    used_suppliers = {s for site in sites for s in site.supplier_ids}
    missing = used_suppliers - {s.id for s in suppliers}
    if missing:
        raise ValueError(f"{sid.value}: sites reference undeclared suppliers {sorted(missing)}")
    suppliers = [s for s in suppliers if s.id in used_suppliers]

    lanes: list[TransportLane] = []
    dist_cost = p.base("distribution_usd_per_unit")
    for site in sites:
        for r in region_ids:
            days = 1.0 if site.region_id == r else delivery_days
            lanes.append(
                TransportLane(
                    id=f"{site.id}->{r}",
                    origin_id=site.id,
                    destination_region_id=r,
                    days=days,
                    cost_usd_per_unit=dist_cost,
                    emergency_days=glob.base("emergency_transport_days"),
                    emergency_cost_usd_per_unit=dist_cost
                    * glob.base("emergency_transport_premium"),
                )
            )

    group_ids = sorted(
        {g for plan in plans for g in plan.groups}
        | {g for s in suppliers for g in s.common_cause_groups}
    )
    groups = []
    for gid in group_ids:
        members = [plan.id for plan in plans if gid in plan.groups] + [
            s.id for s in suppliers if gid in s.common_cause_groups
        ]
        kind = _group_kind(gid)
        groups.append(CommonCauseGroup(id=gid, kind=kind, member_ids=members))

    topology = NetworkTopology(
        regions=regions,
        sites=sites,
        suppliers=suppliers,
        components=default_components(),
        lanes=lanes,
        common_cause_groups=groups,
    )
    topology.validate()

    region_policies: dict[str, RegionPolicy] = {}
    for r in region_ids:
        local = [
            s.id for s in sites if s.region_id == r and runtimes[s.id].serves_region_ids == (r,)
        ]
        central = [
            s.id
            for s in sites
            if len(runtimes[s.id].serves_region_ids) > 1 and not runtimes[s.id].reserved
        ]
        others = [s.id for s in sites if s.id not in local + central]

        # MD-24 (revision R009): a volume commitment buys priority access, which is the
        # only service channel a take-or-pay term has. Without it the commitment enters the
        # ledger and nothing else, so any optimizer choosing on cost among feasible designs
        # drives the fraction to its lower bound and the instrument optimizes itself away.
        # Committed lines are served from first, in descending order of commitment.
        def _commitment(site_id: str) -> float:
            return take_or_pay.get(site_id, 0.0)

        central = sorted(central, key=lambda sid: -_commitment(sid))
        others = sorted(others, key=lambda sid: -_commitment(sid))
        order = local + central + others
        lane_days = 1.0 if local else delivery_days
        target_days = safety_days + lane_days
        # Regional review rule. Legacy (S0-S7 as frozen): reorder only when the position falls
        # to lane time + 1 day, then order up to target, i.e. an (s, S) rule with a tiny s.
        # ``region_base_stock`` = 1 reviews daily and orders up to target whenever below it
        # (a base-stock rule); ``region_reorder_point_days`` sets s explicitly in days.
        if float(dv.get("region_base_stock", 0.0)) >= 1.0:
            reorder_days = target_days
        elif "region_reorder_point_days" in dv:
            reorder_days = float(dv["region_reorder_point_days"])
        else:
            reorder_days = lane_days + 1.0
        region_policies[r] = RegionPolicy(
            region_id=r,
            policy=OrderUpToPolicy(target_days=target_days, reorder_point_days=reorder_days),
            source_order=order,
            criticality_weight=topology.region(r).criticality_weight,
            minimum_guarantee_fraction=topology.region(r).minimum_guarantee_fraction,
        )

    if float(dv.get("region_base_stock", 0.0)) >= 1.0:
        notes.append(
            "regional inventory reviewed daily to a base-stock target (not the frozen rule)"
        )
    if take_or_pay:
        notes.append(
            f"take-or-pay charges {float(dv['take_or_pay_fraction']):.0%} of the reserved line's "
            "annual variable cost whether or not it runs"
        )
    if (
        float(dv.get("deviation_rate_factor", 1.0)) != 1.0
        or float(dv.get("investigation_duration_factor", 1.0)) != 1.0
    ):
        notes.append(
            "quality workflow scaled by this strategy's own factors (an operating-system "
            "effect on deviation rate and investigation duration); illustrative, no evidence"
        )
    ra = release_assurance or ReleaseAssuranceParams(
        scenario=design.release_scenario
        if design.release_scenario is not ReleaseScenario.R3
        else ReleaseScenario.R0,
        release_time_cv=glob.base("release_time_cv"),
    )
    return StrategyRuntime(
        design=design,
        topology=topology,
        sites=runtimes,
        region_policies=region_policies,
        allocation_policy=design.allocation_policy,
        release_assurance=ra,
        initial_region_stock_days=safety_days,
        initial_site_stock_days=float(dv.get("site_fg_days", 30.0)),
        material_target_days=float(dv.get("material_target_days", 60.0)),
        material_reorder_point_days=float(dv.get("material_reorder_days", 14.0)),
        emergency_transfers=bool(dv.get("emergency_transfers", 1.0) >= 1.0),
        shelf_life_days=p.base("shelf_life_months") * DAYS_PER_YEAR / 12.0,
        bud_503b_days=glob.base("bud_503b_days"),
        site_capital_usd=capital,
        site_fixed_usd_per_year=fixed,
        site_validation_usd=validation,
        reserved_fee_usd_per_year=reserved_fee,
        take_or_pay_usd_per_year=take_or_pay,
        deviation_rate_factor=float(dv.get("deviation_rate_factor", 1.0)),
        investigation_duration_factor=float(dv.get("investigation_duration_factor", 1.0)),
        notes=notes,
    )
