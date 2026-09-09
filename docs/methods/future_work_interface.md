# Future-work interface: shelved assets (out of scope)

The drug-shortage feasibility study does not model shelved-asset acquisition, licensing, or development. That program needs separate biological, IP, CMC, clinical, regulatory, and financial diligence, and its economics (clinical success probabilities, priority-review vouchers, foundation-model sourcing) must never enter this study's conclusions.

The only interface this study exposes to such a program is structural:

| This study provides | Form | Condition |
|---|---|---|
| A validated node cost model for the first archetype (aqueous small-molecule sterile solution, standard vial) | `economics.CostLedger` per site with provenance | Only after tier-5 inputs are replaced and the deterministic model reconciles |
| A tested network simulation with common random numbers | `simulation.run_paired` | Product-specific demand, stability, and pathway inputs must be supplied; no inheritance of this study's product parameters |
| Regulatory gate schema | `config/regulatory_gates.yaml` structure | Gate content is product- and pathway-specific and must be re-mapped |

Anything a shelved-asset program derives from these interfaces is its own result and carries none of this study's validation status.
