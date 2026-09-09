# Product dossier: sterile water for injection - single-dose vial (fill not fixed)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Role (protocol 2.5): include only if scale can be represented meaningfully. Generated 2026-09-02T04:07:45.053518+00:00 under protocol v1.0.0. Status: partial. Hard-gate outcome: UNCERTAIN.

## Frozen evidence

- S01 (sha256 2ea0ff3bb44c, retrieved 2026-09-02T04:01:34.502579+00:00): {"rows_ingredient": 21, "rows_presentation_match": 21, "status_counts": {"Current": 21}, "earliest_initial_posting": "2021-11-23", "reasons": ["Demand increase for the drug", "Discontinuation of the manufacture of the drug", "Other"], "companies": ["B. Braun Medical Inc.", "Baxter Healthcare", "Fresenius Kabi USA, LLC", "Hikma Pharmaceuticals USA, Inc.", "Hospira, Inc., a Pfizer Company", "Medefil, Inc.", "Nephron Pharmaceuticals Corporation", "Otsuka ICU Medical LLC"], "presentations": ["Bacteriostatic Water For Injection In Plastic Container, Injection, 1 mL/1 mL (NDC 0409-3977-03)", "Steril
- S01B (sha256 417de7856556, retrieved 2026-09-01T22:55:09.181438+00:00): {"records": 21, "status_counts": {"Current": 21}}
- S16 (sha256 52e1277513bc, retrieved 2026-09-01T23:08:16.146757+00:00): {"products_ingredient_form": 1, "products_strength_match": 1, "applications": 1, "application_types": {"ANDA": 1}, "sponsors": ["TARO"], "forms": ["INJECTABLE; INJECTION"]}
- S17 (sha256 caaa826d4ba7, retrieved 2026-09-01T23:08:46.549281+00:00): {"products": 0, "applicants": [], "rld_products": 0, "strength_matches": 0}
- S18 (sha256 32f17469d12c, retrieved 2026-09-01T23:09:08.712512+00:00): {"spls": 100, "injectable_titles": 38, "strength_matches": 38, "sample_titles": ["STERILE WATER (WATER) INJECTION [REMEDYREPACK INC.]", "STERILE WATER (WATER) INJECTION [CARDINAL HEALTH 107, LLC]", "STERILE WATER (WATER) INJECTION [CARDINAL HEALTH 107, LLC]", "ABRYSVO (RESPIRATORY SYNCYTIAL VIRUS VACCINE) KIT ABRYSVO (RESPIRATORY SYNCYTIAL VIRUS VACCINE) INJECTION, POWDER, LYOPHILIZED, FOR SOLUTION [PFIZER LABORATORIES DIV PFIZER INC]", "STERILE WATER (WATER) INJECTION, SOLUTION [ICU MEDICAL INC.]", "STERILE WATER (WATER) INJECTION, SOLUTION [ICU MEDICAL INC.]", "STERILE WATER (WATER) INJECTIO
- S14 (sha256 7f00a4d2672a, retrieved 2026-09-01T23:05:44.417140+00:00): {"bulks_list_status": "absent"}
- S19 (sha256 986deefa094d, retrieved 2026-09-01T23:09:14.344925+00:00): {"rows": 1, "note": "utilization/reimbursement proxy only; never cost"}

## Hard gates

| Gate | Status | Rationale | Human task |
|---|---|---|---|
| PG1 Product identity | UNCERTAIN | exact fill volume/container not yet fixed | fix the exact presentation from DailyMed labels |
| PG2 Manufacturing fit | PASS | aqueous small-molecule solution in a standard vial (config flags; process train review pending) |  |
| PG3 Control status | PASS | non-controlled (config flag) |  |
| PG4 Regulatory pathway | UNCERTAIN | approved applications exist (1 Drugs@FDA, 0 Orange Book products); whether Telo can own, contract, or license one needs regulatory review | regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31) |
| PG5 Demand observability | UNCERTAIN | national/regional utilization requires hospital, GPO, or wholesaler evidence; CMS is a proxy | obtain utilization evidence (HA-11) |
| PG6 Clinical substitutability | UNCERTAIN | presentation-specific substitution behavior must be described by clinicians or pharmacists | hospital pharmacy interviews (HA-20) |
| PG7 Input feasibility | UNCERTAIN | API, vial, stopper, seal, label, and testing dependencies not yet mapped | supplier and component map (HA-12) |
| PG8 Economic relevance | UNCERTAIN | diluent volumes are very large relative to a micro node; the workbook flagged scale mismatch | demand evidence (HA-11) and node sizing |

## Weighted criteria

| Criterion | Weight | Data score | Basis | Rule / evidence | Confidence | Workbook provisional (tier 5) |
|---|---|---|---|---|---|---|
| clinical_criticality | 0.20 | - | expert_pending | hospital role, substitution difficulty, patient consequences: pharmacist/clinician judgment | low | 5 |
| shortage_recurrence_duration | 0.20 | 5 | data_rule | 21 current rows; earliest initial posting 2021-11-23 (4.8 y ago) | medium | 5 |
| supplier_vulnerability | 0.15 | 5 | data_rule | 1 distinct application holders (fewer holders = higher vulnerability = higher score); finished-dose only, API and component concentration not yet mapped | low | 3 |
| manufacturing_fit | 0.15 | - | expert_pending | scored against the actual first-node train by a sterile-manufacturing professional | low | 5 |
| public_data_strength | 0.10 | 5 | data_rule | 5 of 6 official sources return records for the ingredient | medium | 4 |
| regional_relevance | 0.10 | - | expert_pending | whether geography or response speed matters after release/material delays: needs release-time and logistics evidence | low | 1 |
| demand_contract_fit | 0.10 | - | expert_pending | bounded demand and a credible institutional purchasing model: GPO/wholesaler evidence | low | 1 |

Data-based partial score: 2.25 over weight 0.45 of 1.00. Workbook provisional total (tier 5, not evidence): 3.8.

## Open human tasks

- demand evidence (HA-11) and node sizing
- fix the exact presentation from DailyMed labels
- hospital pharmacy interviews (HA-20)
- obtain utilization evidence (HA-11)
- regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31)
- supplier and component map (HA-12)
