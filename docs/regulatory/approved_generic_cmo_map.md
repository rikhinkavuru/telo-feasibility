# Approved-generic / contract-manufacturing pathway: preliminary decision map

**PRELIMINARY REGULATORY ANALYSIS; NOT LEGAL ADVICE.** No statement below has been reviewed by a qualified generic-drug/CMC regulatory professional. Every gate it feeds is `UNCERTAIN` in `config/regulatory_gates.yaml`. Legal-status labels follow the protocol: law_or_regulation, final_guidance, agency_initiative, proposed_rule, expert_interpretation, unresolved_question. Evidence pointers are frozen snapshots (`data/raw_snapshots/<source>/<date>/`).

## 1. Architectures Telo could occupy (protocol 4.1 item 7)

| Architecture | Who holds the application | Telo's role | Quality-unit responsibility | Gates |
|---|---|---|---|---|
| A. Own application | Telo files and holds an ANDA (or 505(b)(2) NDA) | sponsor and manufacturer | Telo's quality unit | G01-G07, G13, G14 |
| B. Contract manufacturer named in an owner's application | Existing ANDA/NDA holder | fill-finish site added to the owner's application by supplement | owner's quality unit with a quality agreement delegating site operations | G01-G07 |
| C. License of an existing application | Transferee of an approved application | sponsor after transfer of ownership | Telo's quality unit | G01-G07 |
| D. Supply partner | Owner | component or bulk supplier only | owner | G01, G02 |

The workbook's strategies S0-S6 all assume the approved/CMO pathway without naming which architecture. The feasibility model must carry the architecture as part of the strategy design because lead time, cost, and disposition responsibility differ.

## 2. Decision steps (protocol 4.1 items 6-11) and what the frozen evidence says

### Step 6: identify application owners (Drugs@FDA, Orange Book)

Injectable applications with the exact single active ingredient, from the 2026-09-01 Drugs@FDA (S16) and Orange Book (S17) snapshots (dossiers under `data/product_dossiers/`):

| Candidate | Drugs@FDA applications (injectable) | Distinct sponsors | Orange Book injectable products | RLD products |
|---|---|---|---|---|
| sodium bicarbonate | 19 | 13 | 27 | see dossier |
| norepinephrine bitartrate | 26 | 23 | 37 | see dossier |
| furosemide | 37 | 28 | 37 | see dossier |
| acyclovir sodium | 22 | 14 | 34 | see dossier |
| sterile water for injection | 1 | 1 | 0 (ingredient named differently in the Orange Book) | n/a |
| acetazolamide sodium | 10 | 10 | 9 | see dossier |

Owner identity is established (law_or_regulation: 21 CFR 314 application records). Which owner would contract, license, or compete is a commercial question (unresolved_question).

### Step 7: Telo's relationship (own / contract / license / supply)

Not decided. Founder decision HA-03 and the regulatory review HA-31 decide it per product. The model carries all four as strategy design options.

### Step 8: sites and steps in the application; submission category; timing

- Establishment registration and drug listing are required for every manufacturing site: FD&C Act 510; 21 CFR Part 207 (law_or_regulation).
- Changes to an approved application, including adding a manufacturing site, are governed by 21 CFR 314.70 (law_or_regulation). Which reporting category applies to adding a new sterile fill-finish site (prior approval supplement vs changes-being-effected) is expert_interpretation until the reviewer assigns it; the model treats it as gate G07 with a lead time to be elicited, not assumed.
- Distributed manufacturing registration and listing: FR doc 2026-14073 (S11 snapshot: API JSON, full-text XML, govinfo PDF) is a proposed rule (91 FR 42888, Docket FDA-2025-N-6075, RIN 0910-AI94; comments closed 2026-09-11). The base case must not depend on it (protocol 4.3). Its primary text is now frozen but has not been analyzed line by line; the repository's earlier analysis rested on two law-firm reads (HA-15).

### Step 9: development, control strategy, validation set

Required elements (law_or_regulation unless noted): process validation lifecycle (final_guidance, S08 snapshot), aseptic processing validation and media fills for aseptically filled products (final_guidance, S07 snapshot; 21 CFR 211.113(b)), cleaning validation (21 CFR 211.67), analytical method validation and transfer (21 CFR 211.165(e), 211.194; ICH Q2), container-closure integrity and stability (21 CFR 211.166, 211.94; ICH Q1), continued process verification (S08). Whether sodium bicarbonate 8.4% is terminally sterilized or aseptically filled by current holders is presentation-specific and must be read from labels and the reviewer's knowledge (unresolved_question in this map). Gates G03-G06.

### Step 10: quality agreement responsibilities

Deviation, OOS, CAPA, change control, data integrity, batch disposition, recall, pharmacovigilance, and complaint responsibilities must be assigned in a quality agreement (final_guidance: FDA Contract Manufacturing Arrangements for Drugs: Quality Agreements). Under architecture B the owner's quality unit retains disposition authority. The model's release queue must reflect who disposes.

### Step 11: cross-site comparability

No framework grants automatic statistical interchangeability across sites (unresolved_question). Gate G14 blocks any fleet-level equivalence claim until product/site evidence and agency engagement exist. The repository's per-site conformal validity work is a candidate instrument, not an acceptance.

## 3. Gate register for this pathway

| Gate | Treatment | Legal basis type | Status | What resolves it |
|---|---|---|---|---|
| G01 owner or binding CMO relationship | exclude_if_fail | law_or_regulation | UNCERTAIN | executed agreement or Telo application |
| G02 site in application; registered and listed | lead_time | law_or_regulation | UNCERTAIN | supplement approval and registration |
| G03 process and cleaning validation | hard_feasibility | final_guidance | UNCERTAIN | PPQ and cleaning validation reports |
| G04 aseptic or terminal sterilization validated | hard_feasibility | final_guidance | UNCERTAIN | media fills or sterilization validation |
| G05 analytical methods transferred and validated | hard_feasibility | law_or_regulation | UNCERTAIN | method validation and transfer reports |
| G06 stability and container closure | cap | law_or_regulation | UNCERTAIN | stability data and CCI |
| G07 change category and submission identified | lead_time | law_or_regulation | UNCERTAIN | regulatory assessment |
| G13 unit/site registration supportable | lead_time | proposed_rule | UNCERTAIN | counsel review; final rule status |
| G14 cross-site comparability accepted | no_fleet_claim | unresolved_question | UNCERTAIN | product/site evidence and engagement |
| G15 release model in a validated state of control | fallback_conventional | expert_interpretation | UNCERTAIN | prospective validation; not before |

## 4. What this map does not say

It does not estimate a submission or inspection lead time, an approval probability, or a validation cost. Those enter the model only as elicited ranges with a named source (tier 4) or documents (tier 2), never as defaults.
