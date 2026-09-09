# Stochastic network simulation: methods

Implements protocol section 7 and the daily order of section 7.2. Code: `src/telo_feasibility/{rng,disruptions,demand,inventory,allocation,suppliers,production,quality,release_assurance,strategies,simulation,runner}.py`. Tests: `tests/integration/`.

## Entities and world

A run generates one exogenous world for the universal roster (central plant, second source, reserved CDMO, central expansion, a 503B responder, one node per region, four suppliers, every site-to-region lane, six common-cause groups). Every strategy in that run consumes the subset it instantiates, so paired strategies see identical demand, shocks, site failures, supplier disruptions, common-cause events, shortage-list transitions, and transit-time noise (common random numbers; tests `test_paired_strategies_share_demand_and_disruptions`, `test_common_random_numbers_world_identical_across_strategies`).

Random draws are keyed by (run index, stream, BLAKE2b hash of entity id, ordinal) through `numpy.random.SeedSequence`, so adding an entity never changes another entity's draws (`test_adding_an_entity_does_not_change_other_entities_draws`). Eleven named streams match the protocol's list.

## Demand

Daily demand per region = annual demand x regional share / 365.25 x growth x seasonality x routine multiplier x shock multiplier, rounded to integer units. Routine multiplier is a mean-one lognormal AR(1) with the stationary CV and lag-1 autocorrelation from the parameter set. Shocks arrive as a Poisson process; each hits all regions with a stated probability, else one region; magnitude and duration are lognormal. Contracted vs potential demand and substitution are fields in `DemandSpec` and are disabled until evidence exists.

## Disruptions

Site failures and supplier disruptions are per-entity Poisson arrivals with lognormal durations; common-cause events are per-group arrivals whose capacity impact applies to every member (sites and suppliers). A site's effective capacity on a day is the minimum of its idiosyncratic capacity and every group it belongs to. The 503B shortage-list state is a two-state Markov chain with resolution and re-listing hazards.

## Daily order (protocol 7.2)

1. expire FEFO cohorts; 2. demand (pre-generated); 3. disruption states; 4. receive materials, shipments, released batches (shipments that expired in transit go straight to waste); 5. serve each region from its regional stock (503B lots usable only while the product is listed), backorders FIFO with a window, then lost; 6. sites start batches when finished-goods position falls below the target or assigned regions hold backlog, materials permitting; disposition draws yield, deviation, rejection, release time, and release-assurance outcome from entity-keyed streams; 7. regional order-up-to replenishment (primary source, then secondary; emergency transfer when a region is empty and backlogged), reserved-capacity activation on network days of supply, material reorders; 8. cost accrual across the nine ledgers; 9. assertions.

Mass balance, asserted every day in integer units:

    initial + produced_saleable == on_hand + in_transit + in_release_queue + expired + served

The first full-horizon run violated it (a shipment that expired in transit was counted as served); the assertion caught the leak and the fix is in `step4_receive`.

## Release assurance

Release time is the maximum of the concurrent components (sterility incubation, environmental monitoring, assay, endotoxin) plus serial QA review. R0 uses that. R1 subtracts a measured administrative reduction from the serial component only. R2 changes nothing and counts abstentions. R3 may remove only the assay component for batches the layer releases and sends abstained batches through the full conventional path plus a fallback delay; it cannot be instantiated unless gates permit (`ReleaseAssuranceParams` raises). Tests show R1-R3 collapse to R0 at zero benefit, total abstention yields no benefit, and full release saves nothing while the 14-day sterility incubation is the critical path (H7's mechanism), but does when sterility is short.

## Metrics

Fill rate (protocol B1) counts demand eventually met within the backorder window, attributed to its origin day (a property test found the naive served/demand ratio exceeding 1). Shortage days use the frozen daily threshold on immediate service. Episodes are detected from the daily fill series; recovery is the first day followed by 30 days at or above threshold. Costs are annualized over the analysis window; cost per delivered unit divides by units served.

## Known simplifications (to revisit with evidence)

- One product per network; multi-product pooling is not modeled.
- Regions are equal shares; geography is 1 day within region, `delivery_days` across.
- Material policy is a single order-up-to per component; no supplier allocation during scarcity.
- Reserved capacity fee is a fraction of the reserved site's fixed plus capital cost; no take-or-pay volume term yet.
- Provider harm and substitution are not monetized (protocol 5.2).
