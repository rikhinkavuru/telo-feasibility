# Sterilization-route screen, evidence 04: the shortage population the screen would be applied to

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS. NOT LEGAL ADVICE.** Nothing here has been reviewed by a qualified sterile-manufacturing, microbiology or generic-drug CMC professional.

**This file contains no route determination and no determination of dosage form.** It counts and describes the population, and it estimates how much of that population a route question could even be asked about. Every classification below is derived from listing text in a frozen snapshot. Listing text is a shortage-reporting artefact, not a pharmaceutical description. Method and confidence ladder: `method.md`. Determinations, when they exist, go in `determinations.md`.

---

## 1. Sources and what each carries

| id | file read | retrieved | rows |
|---|---|---|---|
| S01 | `data/raw_snapshots/S01/2026-09-02/Drugshortages.csv` | 2026-09-02T04:01:34Z, HTTP 200, sha256 `2ea0ff3b...` | 1,635 data rows, 22 columns |
| S01B | `data/raw_snapshots/S01B/2026-09-01/drug-shortages-0001-of-0001.json.zip`, member `drug-shortages-0001-of-0001.json` | 2026-09-01T22:55:09Z, HTTP 200, sha256 `417de785...`, `meta.last_updated` 2026-08-31 | 1,623 records |

The two are the same FDA shortage database one day apart, with two differences that matter here.

1. **S01B carries a `dosage_form` field; S01 does not.** The S01 CSV columns are `Generic Name, Company Name, Contact Info, Presentation, Type of Update, Date of Update, Availability Information, Related Information, Resolved Note, Reason for Shortage, Therapeutic Category, Status, Change Date, Date Discontinued, Initial Posting Date` plus six link columns. Dosage form is absent, so on S01 alone the injectable subset has to be recovered from the text of `Generic Name`. That text rule reproduces the S01B field exactly: within S01B, the 833 records with `dosage_form == "Injection"` and the 833 records whose `generic_name` matches `\binject` are the same 833 records, with zero rows on either side of the difference.
2. **S01B carries an `openfda` enrichment block** (application number, UNII, substance name, route, SPL ids, pharmacologic class) on 789 of the 833 injectable records. S01 carries none of it. Section 10 records one confirmed defect in that join.

Keying both exports on (generic name, company, presentation) gives 1,609 distinct keys in S01 and 1,597 in S01B, 1,590 shared, 19 in S01 only and 7 in S01B only. The one-day gap accounts for the drift. Nothing in this file turns on it; where the two disagree the figure quoted is S01B, and the S01 figure is given alongside.

The openFDA export carries its own warning, quoted verbatim from `meta.disclaimer`: "Do not rely on openFDA to make decisions regarding medical care. While we make every effort to ensure that data is accurate, you should assume all results are unvalidated."

---

## 2. The population, counted

Status values in S01B are `Current` (1,173), `To Be Discontinued` (443) and `Resolved` (7). The population for this file is **`Current` and `dosage_form == "Injection"`**.

| level | S01B count |
|---|---|
| rows (one per package NDC per listing) | **833** |
| distinct shortage entries (`generic_name`) | **50** |
| distinct application holders (`company_name`) | **59** |
| distinct entry-holder pairs | **221** |
| distinct presentation keys (holder, product name, strength string) | **522** |
| distinct package NDCs | 828 (5 repeated) |
| distinct product NDCs, among the 789 rows with an openFDA link | 573 |
| distinct application numbers | **284** (212 ANDA, 72 NDA, **0 BLA**) |
| distinct UNII codes | 76, across 62 UNII sets (51 single-substance, 11 multi) |

S01 at one day later gives 1,176 `Current` rows, of which 836 match the injectable text rule, across the same 50 entries.

Injectables are 833 of 1,173 currently listed rows (71.0%) and 50 of 70 currently listed entries (71.4%).

**The unit the screen needs is not the row.** `method.md` section 2 defines the unit of determination as one presentation-holder pair. On the snapshot's own fields that is **522 presentation keys** or **221 entry-holder pairs**, depending on whether strength separates a presentation. Neither number is the number of distinct manufacturing processes, because one holder can run one process across several strengths and several holders can buy from one contract manufacturer. 284 application numbers is the closest snapshot-internal proxy for the number of separate regulatory records a route question would have to be asked against.

Concentration is high. Six holders account for 550 of 833 rows: Hospira/Pfizer 167, Fresenius Kabi 160, Hikma 83, Baxter 62, Eugia 42, Pfizer Inc. 36.

Persistence is high. Median time since initial posting is **6.41 years**, mean 7.14; 559 of 833 rows (67%) have been listed five years or more and 384 (46%) eight years or more. The oldest postings date to 2012: fentanyl citrate and atropine sulfate at 14.66 years, lidocaine hydrochloride and the lidocaine/epinephrine combination at 14.52. No row in the population was first posted before 2012.

---

## 3. Dosage-form mix, and the two things the listing does not say

FDA's `dosage_form` field is one value, `Injection`, for all 833. It does not distinguish solution from powder, suspension or emulsion. Across the 833 records' `presentation` and `generic_name` text combined, the following strings occur **zero times**: `suspension`, `emulsion`, `lyophil`, `powder`, `liposom`, `reconstitut`, `diluent`, `ampul`, `prefilled`, `aqueous`, `aseptic`, `terminal`, `autoclav`. The word `solution` appears once, inside one product name: "Infumorph 200 (Preservative-Free Morphine Sulfate Sterile Solution)".

So the listing never states physical form directly. The one usable proxy is **strength syntax**: a strength that carries a volume unit asserts a liquid; a mass-only strength implies a solid to be reconstituted.

| strength syntax | rows | entries touched |
|---|---|---|
| carries a volume unit, e.g. "10 mg/1 mL", "150 mg/15 mL (10 mg/mL)", "0.25 mg/mL, 4 mL" | 799 | 48 |
| mass only, e.g. "600 mg", "1 mg per vial", "10 mg, single dose vial", "1 g" | 22 | 8 |
| not parseable | 12 | 1 (Amino Acid Injection, whose strength field reads "0.1" or "0.15") |

The eight entries with at least one mass-only row are azacitidine (6 rows), remifentanil (5), rifampin (3), carboplatin (3), methotrexate sodium (2), hydroxocobalamin (1), ifosfamide (1), pentostatin (1). Only rifampin and pentostatin are mass-only across every row; the other six are mixed, so within one shortage entry the listing shows both syntaxes and does not say which rows are which product.

**This proxy under-detects and the size of the miss is not knowable from the snapshot.** A lyophilized product whose listing quotes a reconstituted or per-vial concentration reads as a liquid. Remifentanil is the visible case: 5 of its 9 rows are mass-only and 4 are not, from the same listing. Whatever fraction of the 799 is actually solid, the snapshot cannot name it.

---

## 4. Container mix, where stated

| container as stated in `presentation` text | rows |
|---|---|
| not stated | **711 (85.4%)** |
| flexible or plastic container (`In Plastic Container`, `VIAFLEX`) | 89 |
| syringe (`Syringe`, `Abboject`, `LifeShield`) | 21 |
| vial | 10 |
| bottle | 2 |

Container is stated for 122 of 833 rows, and for 89 of those the statement is a large-volume plastic container carrying dextrose, a dextrose premix, metronidazole, heparin in sodium chloride, or an amino-acid solution. Vial, the container type all six longlist candidates assume, is named in **10 rows out of 833**.

This matters for the screen because container is one of the E6 inference lines in `method.md` section 3, and E6 has a `weakly_inferred` ceiling in any case. On this population the line is not merely weak, it is mostly absent.

---

## 5. Reasons given

| `shortage_reason` (S01B) | rows | share |
|---|---|---|
| not stated | **528** | 63.4% |
| Other | 127 | 15.2% |
| Demand increase for the drug | 90 | 10.8% |
| Discontinuation of the manufacture of the drug | 46 | 5.5% |
| Delay in shipping of the drug | 22 | 2.6% |
| Requirements related to complying with good manufacturing practices | 12 | 1.4% |
| Shortage of an active ingredient | 7 | 0.8% |
| Shortage of an inactive ingredient component | 1 | 0.1% |

S01 one day later: 531 blank, 128 Other, 90, 46, 21, 12, 7, 1.

Roughly four in five injectable rows carry either no reason or "Other". Twelve rows in 833 name a GMP cause. Nothing in this field speaks to sterilization route, and nothing in it should be read as evidence about release time.

Availability, a separate field, reads `Available` on 533 rows, `Unavailable` on 238, `Limited Availability` on 61, and `Unvailable` (sic) on 1.

Therapeutic categories are multi-valued (554 rows carry one, 137 two, 48 three, 75 four, 19 ten). Row-weighted: Anesthesia 353, Pediatric 218, Gastroenterology 129, Analgesia/Addiction 128, Endocrinology/Metabolism 112, Other 88, Oncology 79, Neurology 77, Cardiovascular 68, Rheumatology 57, Anti-Infective 31, Pulmonary/Allergy 29, Hematology 27, Dermatology 19, Ophthalmology 19, Total Parenteral Nutrition 15, Renal 10, Medical Imaging 3.

---

## 6. Scoping estimate: how much of this could a route question even be asked about

**This is a scoping estimate from listing text. It is not a route determination, and it is not a determination of dosage form.** Every step below states what it filters on and what it cannot see.

The archetype is defined by the flag block in `config/longlist.yaml`, which the five in-archetype candidates all carry identically: `small_molecule: true`, `aqueous_solution: true`, `standard_vial: true`, `lyophilized: false`, `suspension_or_emulsion: false`, `biologic_or_vaccine: false`, `cytotoxic_or_high_potency: false`, `controlled_substance: false`, `drug_device_combination: false`, `cold_chain_intensive: false`.

### 6.1 Which of the ten flags the snapshot can evaluate

| flag | evaluable from S01/S01B? | on what |
|---|---|---|
| `lyophilized` | **partially** | mass-only strength syntax; under-detects by an unknown amount (section 3) |
| `biologic_or_vaccine` | **partially** | application number prefix. 0 of 284 are BLA. Peptides and heparins approved under NDA are not caught |
| `drug_device_combination` | **partially** | syringe text on 21 rows; silent on the other 812 |
| `cytotoxic_or_high_potency` | **proxy only** | `therapeutic_category == "Oncology"`, which is a therapeutic label, not a potency classification |
| `controlled_substance` | **proxy only** | `therapeutic_category == "Analgesia/Addiction"`, which over- and under-includes |
| `standard_vial` | **negative only** | 89 rows say plastic container, 21 syringe; 711 say nothing |
| `aqueous_solution` | **no** | liquid can be inferred from strength syntax; aqueous cannot. Vehicle is never stated |
| `suspension_or_emulsion` | **no** | zero occurrences of either word in the whole population |
| `small_molecule` | **no** | UNII identifies a substance, not its size or class |
| `cold_chain_intensive` | **no** | no storage field in either export |

Four of ten flags cannot be evaluated at all, two only through a proxy that is not the thing, one only as a negative, and three only partially. **The exclusions the task names, suspensions and emulsions, are precisely the two the snapshot is blind to.**

### 6.2 The funnel

| step | filter | rows | entries | holder pairs | presentation keys |
|---|---|---|---|---|---|
| P0 | Current, `dosage_form == "Injection"` | 833 | 50 | 221 | 522 |
| P1 | strength carries a volume unit | 799 | 48 | 206 | 492 |
| P2 | entry has no mass-only or unparseable sibling row | **743** | **41** | **184** | **457** |
| P3 | P2 minus rows tagged Oncology | 724 | 40 | 179 | 447 |
| P4 | P3 minus rows whose text names a syringe | 701 | 40 | 176 | 424 |
| P5 | P4 minus rows tagged Analgesia/Addiction | 591 | 33 | 151 | 351 |

**The estimate to carry forward is P2: about 740 rows, 41 shortage entries, 184 entry-holder pairs, 457 presentation keys.** P1 is the permissive bound, since it drops only rows the listing text itself contradicts. P3 to P5 apply the proxies in 6.1 and should be read as a sensitivity, not a result: P3 removes 19 dexamethasone sodium phosphate rows purely because the entry carries an Oncology therapeutic tag, which is a therapeutic-use tag and says nothing about potency, and P5 removes 110 rows on a therapeutic tag rather than a schedule.

Stated as a share, **the listing text is consistent with an in-scope liquid presentation for roughly 89% of currently listed injectable rows (743 of 833) and 82% of entries (41 of 50).** That is an upper bound on scope, not a count of solutions.

### 6.3 Why P2 is an upper bound, demonstrably

Six of the 41 entries that survive P2 are named in a way that should stop anyone from treating the number as a count of aqueous small-molecule solutions:

- three entries whose names carry an ester or salt form characteristic of depot presentations, methylprednisolone acetate (23 rows), penicillin G benzathine (4) and triamcinolone hexacetonide (1). Whether these are solutions or suspensions is on the label and is not in the snapshot;
- liraglutide (9 rows), a peptide approved under an NDA, so the BLA test in 6.1 does not catch it;
- heparin sodium (8 rows), a heterogeneous animal-derived polysaccharide, which the `small_molecule` flag would have to adjudicate and the snapshot cannot;
- Technetium Tc-99m pyrophosphate kit (3 rows), a radiopharmaceutical kit, whose entry name contains the word "Kit" and which the strength filter passes anyway.

That is 48 rows in six entries visible by inspection of the names alone. Because the visible cases were found by reading names rather than by any rule in the snapshot, **48 is a floor on the P2 over-count, not an estimate of it.** Resolving any of them requires a label, which is a different evidence tier and a different piece of work.

---

## 7. Longlist candidates against this population

| longlist id | S01B rows, all statuses | Current + Injection |
|---|---|---|
| `sodium_bicarbonate_8_4_50ml` | 19 (15 Current, 4 To Be Discontinued) | 15 |
| `furosemide_10mgml_vial` | 33 (27 Current Injection, 3 To Be Discontinued Injection, 3 Current Oral Solution) | 27 |
| `sterile_water_for_injection_vial` | 21 (12 Injection, 9 Irrigant, all Current) | 12 |
| `norepinephrine_1mgml_4ml` | **0** | 0 |
| `acyclovir_sodium_50mgml_vial` | **0** | 0 |
| `acetazolamide_500mg_vial` | **0** | 0 |

Three of six longlist candidates do not appear anywhere in the current shortage database, in any status. Norepinephrine is the study's resolved comparator, so its absence is expected and correct. Acyclovir and acetazolamide are carried as reserve and out-of-archetype comparators respectively, and neither is a current shortage.

One reconciliation note: `docs/audits/07_human_action_queue.md` row HA-03 describes furosemide as "30 current rows over 6.40 years". Both frozen exports give 27 `Current` plus 3 `To Be Discontinued` injectable rows, which sums to 30 across the two statuses. Median listing age across all 833 injectable rows is 6.41 years, which is the population median rather than a furosemide figure. Neither observation changes HA-03's substance; both are worth fixing before the number is quoted externally.

---

## 8. Error sources

1. **Under-detection of solids.** Section 3. The strength-syntax proxy catches 22 rows; remifentanil alone shows the proxy failing on 4 of its own 9 rows. Direction: P1 and P2 are too high. Magnitude: unknown from the snapshot.
2. **Total blindness to suspensions and emulsions.** Zero text signal across 833 rows. Direction: P1 and P2 are too high, by at least the 28 rows in the three depot-named entries in 6.3.
3. **Vehicle is never stated.** "Liquid" is not "aqueous". Products formulated in propylene glycol, polyethylene glycol or ethanol read identically to water-based ones in this listing. Direction: P1 and P2 are too high, magnitude unknown.
4. **Entry is not process.** Rows collapse to 50 entries but expand to 284 application numbers. One entry can span autoclaved large-volume bags and aseptically filled vials from different holders, which is exactly the failure `method.md` section 5 items 1 and 2 warns against. Any count at entry level overstates homogeneity.
5. **A confirmed openFDA join defect.** The S01B record with `package_ndc` "71288-205-03" and `presentation` "Furosemide, Injection, 10 mg/mL, 2 mL (NDC 71288-205-03)" carries an `openfda` block for **hydralazine hydrochloride** (`brand_name` and `substance_name` both "HYDRALAZINE HYDROCHLORIDE", `application_number` ANDA217501, UNII FD171B778Y), and that block's own `package_ndc` list contains only "71288-205-01" and "71288-205-02", not the "-03" the shortage row was matched on. Any downstream use of S01B's application numbers, UNIIs or SPL ids must treat the join as fallible. A token-overlap check between the shortage generic name and the linked substance flags 4 rows in 833; three are the Travasol amino-acid rows, where the mismatch is benign, and one is this defect.
6. **44 rows carry no openFDA block at all** and 2 more carry one with no application number, so 46 of 833 rows are outside every application-level test in 6.1. They are spread across 17 entries, led by bupivacaine (7), dexmedetomidine (4), atropine (4) and meperidine (4).
7. **Snapshot drift.** S01 and S01B are one day apart and disagree on 19 plus 7 keys. Shortage listings change weekly. Every count here is dated to its snapshot and should be re-derived, not carried forward.
8. **Small data defects observed.** One availability value reads "Unvailable"; twelve amino-acid rows carry a strength of "0.1" or "0.15" with no unit; five package NDCs appear on more than one row.
9. **Listing is not market.** The shortage database records what firms report about products in shortage. It is not a census of marketed injectable presentations, so no share computed here describes the US injectable market.

---

## 9. What this changes for the screen

1. **The population that could carry a route question is about 740 rows in 41 entries, and it is 184 entry-holder pairs, not 6.** The screen as scoped in `method.md` runs on six longlist presentations. The shortage-driven population behind it is roughly thirty times larger at the holder-pair level and about two hundred times larger than six at the row level. The screen's method scales; the evidence gathering does not, because each row above still needs the E1 or E2 document that HA-34 says is generally confidential.
2. **The enabling dataset is missing one level below where the prior-art review located it.** Section 6.1 of `prior_art_review.md` records that route is not published per marketed presentation. This population shows the gap is wider: **the shortage listing does not carry dosage form either.** Physical state, vehicle, and container are absent or near-absent, and container is stated on 14.6% of rows. A route screen applied to the shortage list has to first reconstruct what kind of product each row is, from labels, before the route question can be posed at all. That is a prior step HA-34 does not currently name.
3. **Three of six longlist candidates are not current shortages, and the shortage population is dominated by anesthesia and analgesia products in large-volume plastic containers.** The 89 plastic-container rows are the presentations most likely to be terminally sterilized on general grounds, and they are also the presentations the study's vial-based archetype does not represent. If family 11 turns out to exist as an intervention anywhere on this list, the snapshot says the likeliest place is the part of the population the current product configurations do not cover.
