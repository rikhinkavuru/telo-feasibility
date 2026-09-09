# Product dossier: furosemide - 10 mg/mL vial (2, 4, or 10 mL; exact fill not fixed)

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS**

Role (protocol 2.5): reserve (repository scorecard pick 2026-07-16). Generated 2026-09-02T04:07:44.861355+00:00 under protocol v1.0.0. Status: partial. Hard-gate outcome: UNCERTAIN.

## Frozen evidence

- S01 (sha256 2ea0ff3bb44c, retrieved 2026-09-02T04:01:34.502579+00:00): {"rows_ingredient": 33, "rows_presentation_match": 1, "status_counts": {"To Be Discontinued": 3, "Current": 30}, "earliest_initial_posting": "2020-04-07", "reasons": ["Demand increase for the drug", "Discontinuation of the manufacture of the drug", "Other", "Requirements related to complying with good manufacturing practices", "Shortage of an inactive ingredient component"], "companies": ["Accord Healthcare Inc.", "Avet Pharmaceuticals, Inc.", "Baxter Healthcare", "Eugia US LLC", "Fresenius Kabi USA, LLC", "Gland Pharma Limited", "Hikma Pharmaceuticals USA, Inc.", "Hospira, Inc., a Pfizer Comp
- S01B (sha256 417de7856556, retrieved 2026-09-01T22:55:09.181438+00:00): {"records": 33, "status_counts": {"Current": 30, "To Be Discontinued": 3}}
- S16 (sha256 52e1277513bc, retrieved 2026-09-01T23:08:16.146757+00:00): {"products_ingredient_form": 37, "products_strength_match": 37, "applications": 37, "application_types": {"NDA": 10, "ANDA": 27}, "sponsors": ["ABRAXIS PHARM", "ACCORD HLTHCARE", "AM REGENT", "AMNEAL PHARMS CO", "APOTEX", "AREVA PHARMS", "ASPIRO", "ASTRAZENECA", "AVET LIFESCIENCES", "BAXTER HLTHCARE CORP", "EUGIA PHARMA", "FRESENIUS KABI USA", "GLAND", "HIKMA", "HOSPIRA", "IGI LABS INC", "INTL MEDICATION", "MANKIND PHARMA", "MARSAM PHARMS LLC", "MEITHEAL", "MICRO LABS", "SABA ILAC SANAYIVE", "SAGENT", "SANOFI AVENTIS US", "SMITH AND NEPHEW", "WARNER CHILCOTT", "WATSON LABS", "WYETH AYERST"], "
- S17 (sha256 caaa826d4ba7, retrieved 2026-09-01T23:08:46.549281+00:00): {"products": 37, "applicants": ["ABRAXIS PHARM", "ACCORD HLTHCARE", "AM REGENT", "AMNEAL PHARMS CO", "APOTEX", "AREVA PHARMS", "ASPIRO", "ASTRAZENECA", "AVET LIFESCIENCES", "BAXTER HLTHCARE CORP", "EUGIA PHARMA", "FRESENIUS KABI USA", "GLAND", "HIKMA", "HOSPIRA", "IGI LABS INC", "INTL MEDICATION", "MANKIND PHARMA", "MARSAM PHARMS LLC", "MEITHEAL", "MICRO LABS", "SABA ILAC SANAYIVE", "SAGENT", "SANOFI AVENTIS US", "SMITH AND NEPHEW", "WARNER CHILCOTT", "WATSON LABS", "WYETH AYERST"], "rld_products": 2, "strength_matches": 37}
- S18 (sha256 e464b6b51f69, retrieved 2026-09-01T23:08:57.885672+00:00): {"spls": 100, "injectable_titles": 31, "strength_matches": 0, "sample_titles": ["FUROSEMIDE INJECTION, SOLUTION [MEDICAL PURCHASING SOLUTIONS, LLC]", "FUROSCIX (FUROSEMIDE) INJECTION FUROSCIX (FUROSEMIDE INJECTION 80 MG/ 10 ML) INJECTION [SCPHARMACEUTICALS INC., A WHOLLY OWNED SUBSIDIARY OF MANNKIND CORPORATION]", "FUROSEMIDE INJECTION [CIVICA, INC.]", "FUROSEMIDE INJECTION, SOLUTION [HF ACQUISITION CO LLC, DBA HEALTHFIRST]", "FUROSEMIDE INJECTION, SOLUTION [CARDINAL HEALTH 107, LLC]", "FUROSEMIDE INJECTION, SOLUTION [CARDINAL HEALTH 107, LLC]", "FUROSEMIDE INJECTION, SOLUTION [HOSPIRA, INC.]"
- S14 (sha256 7f00a4d2672a, retrieved 2026-09-01T23:05:44.417140+00:00): {"bulks_list_status": "absent"}
- S19 (sha256 986deefa094d, retrieved 2026-09-01T23:09:14.344925+00:00): {"rows": 1, "note": "utilization/reimbursement proxy only; never cost"}

## Hard gates

| Gate | Status | Rationale | Human task |
|---|---|---|---|
| PG1 Product identity | UNCERTAIN | exact fill volume/container not yet fixed | fix the exact presentation from DailyMed labels |
| PG2 Manufacturing fit | PASS | aqueous small-molecule solution in a standard vial (config flags; process train review pending) |  |
| PG3 Control status | PASS | non-controlled (config flag) |  |
| PG4 Regulatory pathway | UNCERTAIN | approved applications exist (37 Drugs@FDA, 37 Orange Book products); whether Telo can own, contract, or license one needs regulatory review | regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31) |
| PG5 Demand observability | UNCERTAIN | national/regional utilization requires hospital, GPO, or wholesaler evidence; CMS is a proxy | obtain utilization evidence (HA-11) |
| PG6 Clinical substitutability | UNCERTAIN | presentation-specific substitution behavior must be described by clinicians or pharmacists | hospital pharmacy interviews (HA-20) |
| PG7 Input feasibility | UNCERTAIN | API, vial, stopper, seal, label, and testing dependencies not yet mapped | supplier and component map (HA-12) |
| PG8 Economic relevance | UNCERTAIN | volume plausibly compatible with micro nodes; needs demand evidence | demand evidence (HA-11) and node sizing |

## Weighted criteria

| Criterion | Weight | Data score | Basis | Rule / evidence | Confidence | Workbook provisional (tier 5) |
|---|---|---|---|---|---|---|
| clinical_criticality | 0.20 | - | expert_pending | hospital role, substitution difficulty, patient consequences: pharmacist/clinician judgment | low | 4 |
| shortage_recurrence_duration | 0.20 | 5 | data_rule | 30 current rows; earliest initial posting 2020-04-07 (6.4 y ago) | medium | 4 |
| supplier_vulnerability | 0.15 | 1 | data_rule | 28 distinct application holders (fewer holders = higher vulnerability = higher score); finished-dose only, API and component concentration not yet mapped | low | 3 |
| manufacturing_fit | 0.15 | - | expert_pending | scored against the actual first-node train by a sterile-manufacturing professional | low | 5 |
| public_data_strength | 0.10 | 5 | data_rule | 6 of 6 official sources return records for the ingredient | medium | 4 |
| regional_relevance | 0.10 | - | expert_pending | whether geography or response speed matters after release/material delays: needs release-time and logistics evidence | low | 3 |
| demand_contract_fit | 0.10 | - | expert_pending | bounded demand and a credible institutional purchasing model: GPO/wholesaler evidence | low | 4 |

Data-based partial score: 1.65 over weight 0.45 of 1.00. Workbook provisional total (tier 5, not evidence): 3.9000000000000004.

## Open human tasks

- demand evidence (HA-11) and node sizing
- fix the exact presentation from DailyMed labels
- hospital pharmacy interviews (HA-20)
- obtain utilization evidence (HA-11)
- regulatory professional maps an approved-generic/CMO architecture (HA-23, HA-31)
- supplier and component map (HA-12)
