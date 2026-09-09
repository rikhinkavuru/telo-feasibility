# Product dossier: norepinephrine - 1 mg/mL (4 mg/4 mL) single-dose vial

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Role (protocol 2.5): resolved/recurrent comparator. Generated 2026-09-02T04:07:44.472767+00:00 under protocol v1.0.0. Status: partial. Hard-gate outcome: UNCERTAIN.

## Frozen evidence

- S01 (sha256 2ea0ff3bb44c, retrieved 2026-09-02T04:01:34.502579+00:00): {"rows_ingredient": 0, "rows_presentation_match": 0, "status_counts": {}, "earliest_initial_posting": null, "reasons": [], "companies": [], "presentations": []}
- S01B (sha256 417de7856556, retrieved 2026-09-01T22:55:09.181438+00:00): {"records": 0, "status_counts": {}}
- S16 (sha256 52e1277513bc, retrieved 2026-09-01T23:08:16.146757+00:00): {"products_ingredient_form": 37, "products_strength_match": 21, "applications": 26, "application_types": {"NDA": 4, "ANDA": 22}, "sponsors": ["AMNEAL", "ANTHEA PHARMA", "ASPIRO", "BAXTER HLTHCARE CORP", "BIOCON PHARMA", "BRECKENRIDGE", "CAPLIN", "FRESENIUS KABI USA", "GLAND", "HIKMA", "HOSPIRA", "INFORLIFE", "LONG GROVE PHARMS", "MEITHEAL", "METRICS PHARM", "MSN", "MYLAN LABS LTD", "NEPHRON", "RISING", "SAGENT", "SANDOZ", "SUN PHARM", "ZYDUS PHARMS"], "forms": ["INJECTABLE;INJECTION", "SOLUTION;INTRAVENOUS"]}
- S17 (sha256 caaa826d4ba7, retrieved 2026-09-01T23:08:46.549281+00:00): {"products": 37, "applicants": ["AMNEAL", "ANTHEA PHARMA", "ASPIRO", "BAXTER HLTHCARE CORP", "BIOCON PHARMA", "BRECKENRIDGE", "CAPLIN", "FRESENIUS KABI USA", "GLAND", "HIKMA", "HOSPIRA", "INFORLIFE", "LONG GROVE PHARMS", "MEITHEAL", "METRICS PHARM", "MSN", "MYLAN LABS LTD", "NEPHRON", "RISING", "SAGENT", "SANDOZ", "SUN PHARM", "ZYDUS PHARMS"], "rld_products": 14, "strength_matches": 21}
- S18 (sha256 8f9cb72e5257, retrieved 2026-09-01T23:08:52.487796+00:00): {"spls": 55, "injectable_titles": 31, "strength_matches": 0, "sample_titles": ["NOREPINEPHRINE BITARTRATE INJECTION, SOLUTION, CONCENTRATE [SANDOZ INC]", "NOREPINEPHRINE BITARTRATE INJECTION [BAXTER HEALTHCARE COMPANY]", "NOREPINEPHRINE BITARTRATE INJECTION, SOLUTION, CONCENTRATE [MYLAN INSTITUTIONAL LLC]", "NOREPINEPHRINE BITARTRATE INJECTION [HF ACQUISITION CO LLC, DBA HEALTHFIRST]", "NOREPINEPHRINE BITARTRATE IN SODIUM CHLORIDE (NOREPINEPHRINE BITARTRATE) INJECTION, SOLUTION [WG CRITICAL CARE, LLC]", "NOREPINEPHRINE BITARTRATE INJECTION, SOLUTION [BAXTER HEALTHCARE CORPORATION]", "NOREPINEP
- S14 (sha256 7f00a4d2672a, retrieved 2026-09-01T23:05:44.417140+00:00): {"bulks_list_status": "absent"}
- S19 (sha256 986deefa094d, retrieved 2026-09-01T23:09:14.344925+00:00): {"rows": 0, "note": "utilization/reimbursement proxy only; never cost"}

## Hard gates

| Gate | Status | Rationale | Human task |
|---|---|---|---|
| PG1 Product identity | PASS | presentation fully specified in config |  |
| PG2 Manufacturing fit | PASS | aqueous small-molecule solution in a standard vial (config flags; process train review pending) |  |
| PG3 Control status | PASS | non-controlled (config flag) |  |
| PG4 Regulatory pathway | UNCERTAIN | approved applications exist (26 Drugs@FDA, 37 Orange Book products); whether Telo can own, contract, or license one needs regulatory review | regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31) |
| PG5 Demand observability | UNCERTAIN | national/regional utilization requires hospital, GPO, or wholesaler evidence; CMS is a proxy | obtain utilization evidence (HA-11) |
| PG6 Clinical substitutability | UNCERTAIN | presentation-specific substitution behavior must be described by clinicians or pharmacists | hospital pharmacy interviews (HA-20) |
| PG7 Input feasibility | UNCERTAIN | API, vial, stopper, seal, label, and testing dependencies not yet mapped | supplier and component map (HA-12) |
| PG8 Economic relevance | UNCERTAIN | volume plausibly compatible with micro nodes; needs demand evidence | demand evidence (HA-11) and node sizing |

## Weighted criteria

| Criterion | Weight | Data score | Basis | Rule / evidence | Confidence | Workbook provisional (tier 5) |
|---|---|---|---|---|---|---|
| clinical_criticality | 0.20 | - | expert_pending | hospital role, substitution difficulty, patient consequences: pharmacist/clinician judgment | low | 5 |
| shortage_recurrence_duration | 0.20 | 1 | data_rule | no current FDA shortage rows (0 rows total); resolved history not visible in a single snapshot | low | 4 |
| supplier_vulnerability | 0.15 | 1 | data_rule | 23 distinct application holders (fewer holders = higher vulnerability = higher score); finished-dose only, API and component concentration not yet mapped | low | 2 |
| manufacturing_fit | 0.15 | - | expert_pending | scored against the actual first-node train by a sterile-manufacturing professional | low | 4 |
| public_data_strength | 0.10 | 3 | data_rule | 3 of 6 official sources return records for the ingredient | medium | 4 |
| regional_relevance | 0.10 | - | expert_pending | whether geography or response speed matters after release/material delays: needs release-time and logistics evidence | low | 3 |
| demand_contract_fit | 0.10 | - | expert_pending | bounded demand and a credible institutional purchasing model: GPO/wholesaler evidence | low | 3 |

Data-based partial score: 0.65 over weight 0.45 of 1.00. Workbook provisional total (tier 5, not evidence): 3.7.

## Open human tasks

- demand evidence (HA-11) and node sizing
- hospital pharmacy interviews (HA-20)
- obtain utilization evidence (HA-11)
- regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31)
- supplier and component map (HA-12)
