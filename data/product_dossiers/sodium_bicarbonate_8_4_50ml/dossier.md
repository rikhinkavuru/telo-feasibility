# Product dossier: sodium bicarbonate - 8.4% (50 mEq/50 mL) single-dose vial

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Role (protocol 2.5): current/recurrent case candidate. Generated 2026-09-02T04:07:44.243193+00:00 under protocol v1.0.0. Status: partial. Hard-gate outcome: UNCERTAIN.

## Frozen evidence

- S01 (sha256 2ea0ff3bb44c, retrieved 2026-09-02T04:01:34.502579+00:00): {"rows_ingredient": 19, "rows_presentation_match": 11, "status_counts": {"Current": 15, "To Be Discontinued": 4}, "earliest_initial_posting": "2017-03-01", "reasons": ["Demand increase for the drug", "Discontinuation of the manufacture of the drug", "Other"], "companies": ["Amphastar Pharmaceuticals, Inc.", "Exela Pharma Sciences, LLC", "Fresenius Kabi USA, LLC", "Hospira, Inc., a Pfizer Company", "Long Grove Pharmaceuticals LLC"], "presentations": ["Sodium Bicarbonate, Injection, 10 mEq/10 mL (8.4%, 1 mEq/mL) Syringes (NDC 0409-4900-14)", "Sodium Bicarbonate, Injection, 2.5 mEq/5 mL (4.2%, 0.
- S01B (sha256 417de7856556, retrieved 2026-09-01T22:55:09.181438+00:00): {"records": 19, "status_counts": {"Current": 15, "To Be Discontinued": 4}}
- S16 (sha256 52e1277513bc, retrieved 2026-09-01T23:08:16.146757+00:00): {"products_ingredient_form": 28, "products_strength_match": 19, "applications": 19, "application_types": {"NDA": 3, "ANDA": 16}, "sponsors": ["ABBOTT", "AMNEAL", "ANTHEA PHARMA", "ASPIRO", "BAXTER HLTHCARE CORP", "EXELA PHARMA", "FRESENIUS KABI USA", "HOSPIRA", "INTL MEDICATION SYS", "LONG GROVE PHARMS", "MILLA PHARMS", "OMNIVIUM PHARMS", "STERISCIENCE"], "forms": ["SOLUTION;INTRAVENOUS"]}
- S17 (sha256 caaa826d4ba7, retrieved 2026-09-01T23:08:46.549281+00:00): {"products": 27, "applicants": ["ABBOTT", "AMNEAL", "ANTHEA PHARMA", "ASPIRO", "EXELA PHARMA", "FRESENIUS KABI USA", "HOSPIRA", "INTL MEDICATION SYS", "LONG GROVE PHARMS", "MILLA PHARMS", "OMNIVIUM PHARMS", "STERISCIENCE"], "rld_products": 3, "strength_matches": 18}
- S18 (sha256 b6d09135744c, retrieved 2026-09-01T23:08:47.091216+00:00): {"spls": 100, "injectable_titles": 24, "strength_matches": 0, "sample_titles": ["SODIUM BICARBONATE INJECTION [REMEDYREPACK INC.]", "SODIUM BICARBONATE INJECTION, SOLUTION [BAXTER HEALTHCARE CORPORATION]", "SODIUM BICARBONATE INJECTION, SOLUTION [EXELA PHARMA SCIENCES, LLC]", "SODIUM BICARBONATE (SODIUM BICARBONATE, INJECTION) SOLUTION [CIVICA, INC.]", "SODIUM BICARBONATE INJECTION, SOLUTION [MILLA PHARMACEUTICALS INC.]", "NEOGENVET SODIUM BICARBONATE (SODIUM BICARBONATE) INJECTION [NEOGEN CORPORATION]", "SODIUM BICARBONATE INJECTION, SOLUTION [AMNEAL PHARMACEUTICALS PRIVATE LIMITED]", "PRISMA
- S14 (sha256 7f00a4d2672a, retrieved 2026-09-01T23:05:44.417140+00:00): {"bulks_list_status": "not_included"}
- S19 (sha256 986deefa094d, retrieved 2026-09-01T23:09:14.344925+00:00): {"rows": 0, "note": "utilization/reimbursement proxy only; never cost"}

## Hard gates

| Gate | Status | Rationale | Human task |
|---|---|---|---|
| PG1 Product identity | PASS | presentation fully specified in config |  |
| PG2 Manufacturing fit | PASS | aqueous small-molecule solution in a standard vial (config flags; process train review pending) |  |
| PG3 Control status | PASS | non-controlled (config flag) |  |
| PG4 Regulatory pathway | UNCERTAIN | approved applications exist (19 Drugs@FDA, 27 Orange Book products); whether Telo can own, contract, or license one needs regulatory review | regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31) |
| PG5 Demand observability | UNCERTAIN | national/regional utilization requires hospital, GPO, or wholesaler evidence; CMS is a proxy | obtain utilization evidence (HA-11) |
| PG6 Clinical substitutability | UNCERTAIN | presentation-specific substitution behavior must be described by clinicians or pharmacists | hospital pharmacy interviews (HA-20) |
| PG7 Input feasibility | UNCERTAIN | API, vial, stopper, seal, label, and testing dependencies not yet mapped | supplier and component map (HA-12) |
| PG8 Economic relevance | UNCERTAIN | volume plausibly compatible with micro nodes; needs demand evidence | demand evidence (HA-11) and node sizing |

## Weighted criteria

| Criterion | Weight | Data score | Basis | Rule / evidence | Confidence | Workbook provisional (tier 5) |
|---|---|---|---|---|---|---|
| clinical_criticality | 0.20 | - | expert_pending | hospital role, substitution difficulty, patient consequences: pharmacist/clinician judgment | low | 5 |
| shortage_recurrence_duration | 0.20 | 5 | data_rule | 15 current rows; earliest initial posting 2017-03-01 (9.5 y ago) | medium | 5 |
| supplier_vulnerability | 0.15 | 1 | data_rule | 13 distinct application holders (fewer holders = higher vulnerability = higher score); finished-dose only, API and component concentration not yet mapped | low | 4 |
| manufacturing_fit | 0.15 | - | expert_pending | scored against the actual first-node train by a sterile-manufacturing professional | low | 5 |
| public_data_strength | 0.10 | 5 | data_rule | 5 of 6 official sources return records for the ingredient | medium | 3 |
| regional_relevance | 0.10 | - | expert_pending | whether geography or response speed matters after release/material delays: needs release-time and logistics evidence | low | 4 |
| demand_contract_fit | 0.10 | - | expert_pending | bounded demand and a credible institutional purchasing model: GPO/wholesaler evidence | low | 4 |

Data-based partial score: 1.65 over weight 0.45 of 1.00. Workbook provisional total (tier 5, not evidence): 4.45.

## Open human tasks

- demand evidence (HA-11) and node sizing
- hospital pharmacy interviews (HA-20)
- obtain utilization evidence (HA-11)
- regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31)
- supplier and component map (HA-12)
