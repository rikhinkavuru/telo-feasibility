# OS-only and virtual-network analyses

## 1. Question and banner

Assignment deliverable 14, covering families 2 (OS-only) and 3 (virtual manufacturing network). Two questions: (1) is the strongest first company a software vendor rather than a manufacturer? (2) does a virtual capacity network beat owned nodes?

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input behind every run quoted here is tier 5 (illustrative). Everything below is the behaviour of a model under those inputs, not a statement about sterile-injectable manufacturing in the world, and nothing here may be quoted outside this package. All sixteen regulatory gates in `config/regulatory_gates.yaml` (G01 to G16) stay UNCERTAIN; none is treated as passed. Nothing here is legal or regulatory advice. No interview, partner, customer or review is asserted; none has occurred.

Run artifacts, and every number below is keyed to one of them:

- paired simulation `results/simulation/sim_post_R008/summary.json` (n = 100, master seed 20260901, five measured years after a 365-day warm-up, measured window 1826 days);
- optimization at the frozen target `results/optimization/opt_20260903T220534Z/` (tau 0.99, q 0.90) and at tau 0.98 `results/optimization/opt_20260903T231408Z_tau0.98/summary.json`;
- ablation `results/ablation/abl_post_R008/attribution.csv` (n = 60, designs `optimized:opt_20260903T220534Z`) and interaction study `results/ablation/abl_post_R008_pairs/summary.json` (n = 60);
- feasibility conditions, dominance and contract scenarios `results/design_space/ds_post_R008/` (40 runs; thresholds by bisection over 5 steps on 20 paired runs);
- contract conditions `results/design_space/contract_conditions_sim_post_R008.csv`;
- figures `../../results/figures/ablation_abl_post_R008_sodium_bicarbonate_8_4_50ml_heatmap_fill_rate.png`, `../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_dominance.png`, `../../results/figures/design_space_ds_post_R008_sodium_bicarbonate_8_4_50ml_feasibility.png`.

---

## 2. What the model can and cannot represent for these two families

### 2.1 OS-only

The engine has exactly three OS handles.

| handle | where | what it does |
|---|---|---|
| `deviation_rate_factor` | `strategies.py:74`, `simulation.py:118` | scales `deviation_rate_per_batch` (tier 5; low 0.005, base 0.02, high 0.08) |
| `investigation_duration_factor` | `strategies.py:75`, `simulation.py:119` | scales `investigation_duration_days` (tier 5; low 7, base 21, high 60) |
| `os_integration_usd_per_site_year` | `config/global.yaml:614`, `simulation.py:166` | costs 100,000 / 300,000 / 800,000 USD per site-year, tier 5, `source_locator` "study placeholder" |

Three facts bound what can be said. No configured strategy uses the first two: a grep of `config/strategies/*.yaml` returns nothing, so no run in this package has ever simulated an OS. The OS is also free in every run quoted here, because `os_integration` is charged only when the release scenario is not R0, every design-space strategy is R0, and `ledger_os_integration.mean` is 0.00 in all 40 cells of `sim_post_R008`; S17 declares a shared `cc_os` group across four sites and pays nothing for it (MD-25). And the protocol forbids an OS effect on release time or capacity (`architecture_taxonomy.md` section 1, family 2), while the Phase A decomposition puts deviation and rejection in the "measured but not binding" set.

The engine can therefore give only an upper bound. The `deviation_rejection` ablation arm (`ablation.py:148-157`) sets `deviation_rate_per_batch = 0`, `batch_rejection_rate = 0` and `yield_sd = 0`. That is a perfect OS and then some, since no OS claims to remove batch rejection or yield variance. If a perfect OS is not worth its price, no real one is.

**The engine cannot represent the business at all.** There is no software revenue line, no customer entity, no seat or site count outside Telo's own network, no contract value and no churn. `os_integration_usd_per_site_year` is a cost Telo pays, not a price Telo charges. The model can bound the operational value of an OS; it cannot bound the value of an OS company. Section 6.1 names the evidence that would settle that and who holds it.

### 2.2 Virtual network

Representable: `cdmo_reserved` site plans with `reserved`, `reserved_site_owned`, `activation_lead_days`, `activation_failure_probability`, `exercise_batches_per_year`, `campaign_batches`, `activation_threshold_days` and `take_or_pay_fraction`; per-site `commissioning_days`; per-site supplier assignment and common-cause groups. Since R004 a reserved line Telo does not own carries no capital, fixed operations or validation, only its reservation fee and the batches it runs (MD-14).

Not representable, each with the direction it distorts:

The `NEW-n` ids below are defined in `novel_architectures.md` section 5 (NEW-4 in section 5.1); they are engine gaps found by the Phase B sweep and are not rows of the MD register in `bottleneck_decomposition.md` section 7, so cite them against that section.

- no per-partner qualification state, data rights or channel conflict; a partner site is usable or it is not;
- **NEW-3**, no readiness decay: `activation_failure_probability` is a per-plan constant with no link to `exercise_batches_per_year`, so exercise batches buy production volume and not reliability, and S13, S16, S17 and S19 all depend on that coupling;
- **MD-23**: `exercise_due` requires `active_until_batches <= 0`, so a banked campaign batch blocks an exercise batch and a cadence is measurable only on a rarely activated line;
- **NEW-2**, allocation rights are inert: every region's `criticality_weight` is 1.0 and no minimum guarantee is passed, so all four `allocation_policy` values collapse to proportional, and allocation is the central power in every family-3 precedent;
- **MD-24**: `take_or_pay_fraction` enters only the cost ledger and changes no service quantity;
- **MD-14 residual**: ownership is a property of the `reserved` flag, not of the site, so S16 and S17 carry the incumbent plant's full capital (6,703,202 USD/yr, identical to S0) on their ledgers; their reported cost is not a Telo-only cost and no Telo-only companion design has been run;
- **NEW-1**: opening inventory is seeded without a variable-production charge, which flatters deep-stock designs, and every contracted design that clears below does so near the top of its safety-stock range.

---

## 3. Results

### 3.1 Question 1: what an OS does to the manufacturing system, and what it costs

Perfect-OS ablation, `abl_post_R008/attribution.csv`, factor `deviation_rejection`, 40 cells (2 products x 20 strategies), n = 60 paired runs on the optimizer's best-or-closest designs.

| measure | value | cell |
|---|---|---|
| largest `loo_delta_fill_rate` | +0.008638 | sodium bicarbonate S19 |
| smallest `loo_delta_fill_rate` | -0.001479 | norepinephrine S2 |
| mean over 40 cells | +0.001771 | |
| cells with abs(delta fill) above 0.005 | 4 of 40 | |
| largest `loo_delta_shortage_days_per_year` | -5.6241 d/yr from a base of 50.527 | sodium bicarbonate S15 |
| largest `loo_delta_unmet_units_per_year` | -10,823 units/yr, 0.90% of the 1,200,000-unit annual demand base | sodium bicarbonate S19 |
| feasibility flips at q = 0.90 | 3 of 40: norepinephrine S8 0.883 to 0.900, norepinephrine S18 0.867 to 0.900, sodium bicarbonate S13 0.867 to 0.917 | |

All three flips sit inside 1.3 binomial standard errors (SE at n = 60 and p = 0.9 is 0.0387) and every flipped cell was already beside the requirement. Removing every deviation, every rejection and all yield variance makes three of forty cells cross the requirement, all three from within 1.3 standard errors of it, and makes no cell that was clearly infeasible feasible. Annual cost falls in 34 of 40 cells and rises in 6 (largest rise +25,819 USD/yr at sodium bicarbonate S2, where completing more batches, fill +0.0015, costs more variable production; norepinephrine S2 moves the other way, -25,577 USD/yr at fill -0.0015, and is the smallest fill delta in the table above). Set the largest savings against the OS charge:

| cell | sites | perfect-OS saving [USD/yr] | OS at base 300k/site-year | ratio | OS at low 100k/site-year | ratio |
|---|---|---|---|---|---|---|
| sodium bicarbonate S8 | 2 | 40,684 | 600,000 | 14.7x | 200,000 | 4.9x |
| sodium bicarbonate S17 | 4 | 35,432 | 1,200,000 | 33.9x | 400,000 | 11.3x |
| norepinephrine S8 | 2 | 32,245 | 600,000 | 18.6x | 200,000 | 6.2x |
| sodium bicarbonate S16 | 3 | 28,160 | 900,000 | 32.0x | 300,000 | 10.7x |

Per delivered unit on sodium bicarbonate S17, the OS adds 0.9601 USD/unit to a 15.6660 USD/unit break-even price (+6.1%), against a perfect-OS operational value of 0.0283 USD/unit. Inputs passed to `contracting.contract_requirement` from the package root: `annual_cost_usd` 19,580,125, then the same plus 4 x 300,000; `reference_annual_cost_usd` 12,925,986 (S0); `delivered_units_per_year` 1,249,852; `fixed_and_resilience_cost_usd` 15,943,314 (the `FIXED_LEDGERS` block of `scripts/build_contract_table.py`); `variable_cost_usd_per_unit` 1.2000; `capacity_units_per_year` 1,253,948. The resilience premium against S0 moves from 5.3239 to 6.2841 USD/unit.

**Stated plainly.** In this model an operating system is worth at best about three cents per delivered unit and costs about a third of a dollar to a dollar at the low and base OS prices (4 x 100,000 gives 0.3200 and 4 x 300,000 gives 0.9601 USD per delivered unit), and up to about 2.56 USD per delivered unit at the declared high of 800,000 USD per site-year (4 x 800,000 against sodium bicarbonate S17's 1,249,852 delivered units per year). The model bounds the operational value of an OS and says nothing about the business, because it has no revenue side. Whether a software company built on this function is a good company is a question about buyers, contract values and renewal, and no run in this package addresses it.

### 3.2 Question 2: contracted and reserved architectures against owned nodes

Starting designs, `sim_post_R008/summary.json`, sodium bicarbonate.

| | S5 owned nodes | S6 owned nodes + release layer | S8 acquired sites | S12 contracted base | S13 contracted + reserved | S16 reserve-triggered | S17 rotating standby |
|---|---|---|---|---|---|---|---|
| sites owned / contracted | 5 / 0 | 5 / 0 | 2 / 0 | 3 / 0 | 2 / 1 | 1 / 2 | 1 / 3 |
| activation latency [d] | none | none | none | none | 21 (global) | 21 (global) | 30 (declared) |
| regulatory owner (`profile.regulatory_owner`) | no profile recorded | no profile recorded | Telo as ANDA holder, both sites; each site registers itself | Telo as holder or labeler; the DME route is unavailable to an unaffiliated network | Telo as holder or labeler; each site-product pair named before it can supply | the ANDA holder, Telo or a partner; each contracted line named before commercial product (G01, G02, G07, all UNCERTAIN) | one application holder; every contracted line named before t0 |
| quality owner (`profile.quality_owner`) | no profile recorded | no profile recorded | one Telo quality unit disposes both sites | one Telo quality unit, non-delegable | one Telo quality unit across all three sites | one quality unit disposes all three lines; each CDMO keeps its own site system | one quality unit disposes all four; each contract site keeps its own |
| qualification burden, proxied by the declared commissioning lead [d] | 730 (global base, 4 built nodes) | 730 (global base, 4 built nodes) | 365 at `second_source` | 365 at `second_source`, 730 at `cdmo_r2` | 365 at `second_source`; the reserved line exists at t0 | 540 at each of two contracted lines | none: all four sites exist at t0 |
| `capacity_days_lost_to_commissioning_fraction` | 0.287211 | 0.287211 | 0.099945 | 0.090273 | 0.044420 | 0.000000 | 0.000000 |
| equivalent capacity-weighted days of 1826 | 524.4 | 524.4 | 182.5 | 164.8 | 81.1 | 0.0 | 0.0 |
| fixed and resilience cost [M USD/yr] | 40.066 | 42.323 | 19.908 | 19.569 | 17.265 | 13.319 | 15.943 |
| per site [M USD/yr] | 8.013 | 8.465 | 9.954 | 6.523 | 5.755 | 4.440 | 3.986 |
| distinct API / vial / stopper sources | 1 / 1 / 1 | 1 / 1 / 1 | 2 / 1 / 1 | 2 / 2 / 1 | 2 / 2 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| groups spanning every site | cc_api_1, cc_vial_1 | cc_api_1, cc_vial_1 | cc_vial_1, cc_quality, cc_stopper_1 | cc_quality, cc_stopper_1 | cc_quality, cc_stopper_1 | cc_api_1, cc_vial_1, cc_quality, cc_stopper_1 | cc_api_1, cc_vial_1, cc_os, cc_quality, cc_stopper_1 |
| `common_cause_days` mean | 433.40 | 433.40 | 314.76 | 418.16 | 519.90 | 427.85 | 907.33 |
| `activations` / `activation_failures` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 4.11 / 0.78 | 8.84 / 1.05 | 5.57 / 0.58 |
| `exercise_batches` | 0 | 0 | 0 | 0 | 7.50 | 7.74 | 64.93 |
| `cost_per_delivered_unit` [USD] | 40.6039 | 42.6897 | 19.6980 | 19.9909 | 16.6376 | 14.4671 | 15.6660 |

Two rows must not be read at face value. The commissioning metric excludes reserved sites (`simulation.py:696-699`): S16's two contracted lines carry `commissioning_days` 540, which is 29.57% of the measured window, and the metric still reports 0.000000; S17's zero is real, because all four of its sites exist at t0. And `common_cause_days` counts group-days while every declared group draws its own Poisson stream at one global rate (NEW-4), so S17's 907.33 against S16's 427.85 is mostly five groups against four, not five times the dependence. Read the supplier and group rows instead.

**Three of the assignment's eight comparison axes are not scored by any run here.** The assignment asks for virtual against owned on activation latency, qualification burden, fixed cost, data rights, channel conflict, supplier independence, commercial control and regulatory responsibility. Five are in the table above: activation latency, qualification burden through the commissioning-lead proxy, fixed cost per site, supplier independence through the source and group rows, and regulatory responsibility through the two profile fields. **Data rights, channel conflict and commercial control are not represented in the engine at all.** There is no per-partner data record, no ownership of process or release data, no competing channel for the partner's own output and no control right over a partner's calendar; a partner site is usable or it is not. No run in this battery can score them, in either direction. They are decided by the contract fields that section 4.1 already lists as UNANSWERED (allocation rights, default risk, activation condition, term) and by evidence nobody has supplied: **HA-13** and **HA-21** for what a US line will sell, **HA-24** and **HA-33** for who holds the commercial relationship. Two of the frozen comparators cannot be scored on the regulatory axis either, because S5 and S6 carry no `StrategyProfile` at all in `config/strategies/illustrative_baseline.yaml`.

Service at the frozen target, `opt_20260903T220534Z/summary.json`, tau 0.99 and q 0.90, best design per cell:

| strategy | sodium status | sodium fill | sodium p_meet | sodium USD/unit | norepi status | norepi fill | norepi p_meet | norepi USD/unit |
|---|---|---|---|---|---|---|---|---|
| S5 | infeasible | closest 0.865052 | | | infeasible | closest 0.980253 | | |
| S6 | infeasible | closest 0.865052 | | | infeasible | closest 0.980253 | | |
| S8 | infeasible_at_full_n | 0.989909 | 0.70 | 18.8232 | infeasible_at_full_n | 0.994946 | 0.87 | 23.8441 |
| S12 | optimal | 0.998257 | 0.95 | 17.8847 | optimal | 0.998312 | 0.95 | 19.6568 |
| S13 | optimal | 0.996385 | 0.90 | 15.4782 | optimal | 0.995759 | 0.91 | 19.8894 |
| S16 | optimal | 0.996974 | 0.94 | 13.1807 | optimal | 0.997419 | 0.93 | 16.9421 |
| S17 | infeasible_at_full_n | 0.995625 | 0.88 | 15.3207 | optimal | 0.996710 | 0.97 | 19.4114 |

At tau 0.98 (`opt_20260903T231408Z_tau0.98/summary.json`) sodium S17 becomes optimal at 0.991932 / 0.93 and 15.3626 USD/unit, while S5, S6 and sodium S8 stay infeasible. In `ds_post_R008/dominance.csv` (40 runs), on sodium bicarbonate S5 is dominated by 16 strategies and S6 by 17, with the frontier S1, S9, S11, S12, S15, S16; on norepinephrine S5 is dominated by 16 and S6 by 17, with the frontier S9, S11, S15, S16, S17.

Feasibility conditions, `ds_post_R008/thresholds.csv`. Both sweeps are narrower than their names suggest.

- **`commissioning_days`** sweeps the global `node_commissioning_days` over 365 / 730 / 1095. Every S8+ design with a site that does not exist at t0 declares its own `commissioning_days`, so the sweep reaches only S2, S4, S5, S6 and S7. For all five, and for both products, the verdict is `infeasible_everywhere`: no commissioning time in the declared range lets a build-it architecture in this battery reach the frozen target. The `feasible_everywhere` verdict recorded for S8, S12, S13, S16 and S17 is a statement about the sweep's reach, not about their robustness to commissioning.
- **`activation_latency_days`** sweeps the global `reserved_capacity_activation_days` over 7 / 21 / 60 and reaches only reserved sites that do not declare their own lead: S3, S11, S13 and S16. Thresholds found, all `feasible_below`: S3 19.421875 d (both products), sodium S11 27.703125 d, sodium S16 22.734375 d. S13 is feasible across 7 to 60 on both products. S17 declares `activation_lead_days` 30, and S8 and S12 have no reserved site, so the sweep is inert for all three.

Why owned nodes fail, `abl_post_R008_pairs/summary.json`, n = 60: switch capacity shortfall and commissioning delay off together and sodium bicarbonate S5 moves from fill 0.866856 with p_meet 0.00 to 0.997499 with p_meet 0.983, at 50,768,486 USD/yr, while in the same arm S16 reaches 0.999999 with p_meet 1.00 at 17,383,193 USD/yr. The owned-node architecture is not broken by anything exotic. It is broken by having to build the capacity, and it remains about three times as expensive after both mechanisms are removed by hand.

**Answer, as model behaviour.** Under these inputs the contracted and reserved architectures beat the owned nodes on commissioning window lost (0.000 to 0.044 against 0.287), on fixed cost per site (3.99M to 6.52M against 8.01M and 8.47M), on service at the frozen target (three of four clear on both products; S5 and S6 clear on neither), and on cost per delivered unit, where the three clearing designs land at 13.18 to 17.88 USD/unit while S5 and S6 sit at 40.60 and 42.69 USD/unit at their starting designs and still fail the target. They do not beat them on supplier independence. S16 and S17 have exactly as little of it as S5 does: one API, one vial and one stopper source across every line they own or reserve, so a single API or container event stops the whole network. The two designs that do buy supplier independence, S12 and S13, pay for it in commissioning (0.090 and 0.044) and in unit cost (17.88 and 15.48 against S16's 13.18).

**The comparison is not matched, and that is the largest caveat here.** `optimization.DESIGN_SPACES` gives S5 and S6 only `sites`, `node_scale`, `safety_stock_days` bounded at 90 days and `material_target_days`. S12, S13 and S16 search `safety_stock_days` to 365 and `region_base_stock` as a binary. Every winning contracted sodium design sits near the top of that range with the non-frozen review rule on: S12 at 309.2 days with `region_base_stock` 1, S13 at 365 with 1, S16 at 365 with 1. The frozen regional review rule is MD-3, a hard-coded convention the protocol never specifies, decisive in 8 of 16 Phase A cells, and the comparators cannot select the alternative. Part of the measured gap between contracting and owning is a gap between two replenishment rules, and this run cannot say how much.

---

## 4. Commercial conditions

Derived through `src/telo_feasibility/contracting.py` from `sim_post_R008`, with the definitions of `scripts/build_contract_table.py`: fixed and resilience cost is the `FIXED_LEDGERS` block (capital annualized, fixed site operations, product and site launch, resilience contracts, OS integration); variable cost per unit is the product's `variable_materials_usd_per_unit` plus `variable_conversion_usd_per_unit` (1.2000 sodium bicarbonate, 1.1500 norepinephrine); capacity is delivered units divided by mean fill. No market price exists for either presentation, so **every price-shaped number below is a modelled break-even cost used as a stand-in price and labelled as one**; `contracting.py` never infers a price from a cost, and `contract_requirement` writes a note on every row where the break-even figure is substituted for a price. Read the two utilization rows on saleable capacity (`delivered / fill`) and the last row on delivered volume; the bases differ, and the row labels say which.

| sodium bicarbonate | S5 | S6 | S8 | S12 | S13 | S16 | S17 |
|---|---|---|---|---|---|---|---|
| resilience premium vs S0 [USD/unit] | 28.6434 | 30.7280 | 8.7392 | 8.6027 | 6.2480 | 3.1646 | 5.3239 |
| break-even price [USD/unit] | 40.5821 | 42.6666 | 19.6906 | 19.9677 | 16.6355 | 14.4608 | 15.6660 |
| min contracted utilization at own break-even cost, on saleable capacity | 0.8104 | 0.8130 | 0.8578 | 0.8308 | 0.8920 | 0.8003 | 0.8789 |
| min contracted utilization at S0's own break-even cost of 14.4320 USD/unit, a modelled cost used as a stand-in price, on saleable capacity | 2.4119 | 2.5478 | 1.1987 | 1.1783 | 1.0406 | 0.8021 | 0.9609 |
| price required if only 50% of **delivered** volume is committed [USD/unit] | 75.2121 | 79.3812 | 34.9337 | 35.6119 | 28.9489 | 24.4802 | 26.7123 |

A minimum contracted utilization above 1.0 means the architecture cannot cover its fixed and resilience cost at that figure even if every unit it can make is committed. At S0's break-even cost of 14.4320 USD/unit used as a stand-in price, only S16 (0.8021) and S17 (0.9609) cover fixed and resilience cost on sodium bicarbonate. On norepinephrine none does: S16 needs 1.0855, S17 1.2951, S13 1.4015, S12 1.5866, S8 1.6141, S5 3.2486 and S6 3.4316. **No price a purchaser will pay is known for either presentation** (HA-11, HA-24), so none of this is a statement about affordability. The last row uses the Civica-shaped 50% commitment (F8-S14, F10-S01) and shows what the uncommitted half would have to fetch; it divides by delivered volume rather than by saleable capacity, so on sodium bicarbonate S17 it reads 26.7123 against 26.6290 on the capacity base, and the two utilization rows above it use the capacity base throughout.

Take-or-pay, `ds_post_R008/contract_scenarios.csv`, 20 runs, swept 0.00 to 1.00: mean fill is bit-identical across the whole sweep for S13, S16 and S17 on both products, and annual cost is strictly increasing, sodium S17 18,939,830 to 20,883,830 USD/yr (+1.944M, +10.3%), S16 16,023,285 to 16,936,104 (+0.913M, +5.7%), S13 19,203,949 to 19,612,189 (+0.408M, +2.1%). This is MD-24 in full view: the instrument that pays for the reserved line has no service channel, so a cost-minimising optimizer removes it. It is swept as a labelled scenario, never searched.

### 4.1 The nine contract questions, per architecture

Fields are `ContractTerms.REQUIRED` in `contracting.py`. "shape" means a value taken from a published third-party contract and carried as an illustration. No counterparty of Telo's has stated any field, so `missing()` is non-empty for every architecture here and each is recorded as **not contractable, stated**.

| ContractTerms field | S5 / S6 owned nodes | S8 acquired sites | S12 contracted base | S13 contracted + reserved | S16 reserve-triggered | S17 rotating standby |
|---|---|---|---|---|---|---|
| mechanism | none recorded | minimum purchase commitment | take-or-pay committed volume | take-or-pay plus reservation fee | take-or-pay (0.5, illustrative) | two-part capacity option plus committed volume |
| payer | **UNANSWERED** | shape: member hospital via GPO (LSIM-S18) | shape: hospital or GPO (F3-S30) | shape: hospital or GPO | shape: member hospital in the unit price | shape: consortium member |
| purchaser | **UNANSWERED** | shape: GPO or IDN | shape: health system or GPO | shape: health system or GPO | shape: health system or GPO (LSD-S11) | shape: GPO or consortium (LSIM-S20) |
| beneficiary | **UNANSWERED** | shape: same | shape: same | shape: same | shape: member hospitals' patients | shape: member hospitals' patients |
| term_years | **UNANSWERED** | **UNANSWERED** | shape: multi-year (F3-S23, F3-S25) | shape: multi-year | shape: 3 to 10 (F8-S14) | shape: 3 to 10 (F10-S01) |
| committed_units_per_year | **UNANSWERED** | **UNANSWERED** | shape: about 50% of expected | shape: about 50% of expected | shape: about 50% of expected | **UNANSWERED** |
| activation_condition | **UNANSWERED** | **UNANSWERED** | not applicable, no reserved line | shape: days of supply below threshold | shape: days of supply below `activation_threshold_days` | shape: campaign call at a rotated line |
| allocation_rights | **UNANSWERED** | **UNANSWERED** | proportional, inert (NEW-2) | proportional, inert (NEW-2) | proportional, minimum guarantee unsimulable (NEW-2) | proportional, inert (NEW-2) |
| default_risk | **UNANSWERED** | **UNANSWERED** | **UNANSWERED** | **UNANSWERED** | shape: failure-to-supply erosion, low-price walk-away (F10-S10) | **UNANSWERED** |
| price_required_usd_per_unit | **UNANSWERED** | **UNANSWERED** | **UNANSWERED** | **UNANSWERED** | model output only, which is not a price | **UNANSWERED** |
| unanswered, of 9 | 9 | 6 | 2 | 2 | 0 blank, 0 evidenced by a counterparty | 3 |

S16 is the only architecture with a shape in all nine fields and it is still not contractable, because a shape is not a signature. The frozen comparators S5 and S6 carry no `ContractTerms` record at all. No US purchaser has been found to have paid a standing reservation fee for sterile generic capacity (F3-S28), and FDA's own Drug Shortages Task Force records that most generic manufacturers cannot afford redundant capacity (F7-S16).

---

## 5. Prior art and landscape position

**OS-only.** The cross-family review's closing paragraph puts the manufacturing OS on the does-not-survive list "in any of its eight sub-forms", but its own novelty matrix does not classify all eight as `already_implemented`, and the distinction matters for question 1. Six sub-forms are `already_implemented`: the eBR and MES documentation wedge (F2-S01, F2-S05, F2-S04, F2-S07, F2-S12, F2-S09, F2-S13, F2-S71; Korber PAS-X at over half the top 30, LPMS-S01, LPMS-S02); deviation and CAPA orchestration and QMS workflow automation (F2-S15, F2-S16, F2-S23, F2-S24, F2-S25, F2-S29; Veeva LQBR-S04, MasterControl LQBR-S07 to LQBR-S09, TrackWise LQBR-S10); sensor interoperability and data lineage (F2-S21, F2-S22, F2-S17, F2-S26); multivariate drift detection, whose falsifier is recorded as "nothing; it exists" (F2-S20, F2-S17, F2-S19, F2-S18; Sartorius SIMCA-online LPMS-S13); cross-site process intelligence within one owner (F2-S14, F2-S09, F2-S71); hospital and GPO shortage-response coordination (F2-S33, F2-S35, F2-S37, F2-S38, F2-S43, F2-S44; Bluesight LSD-S14, USP LSD-S4, Vizient LSD-S9). Emerson already ships the furthest an OS can go toward release, immediate release once exceptions close (LPMS-S03, LPMS-S26).

The remaining OS-shaped positions in the same matrix are not `already_implemented`, and one of them is the answer to question 1 rather than a footnote to it. **Process scheduling and campaign optimization (sub-form 2c)** appears as "multi-owner campaign scheduling against an external shortage signal", classified `uncertain`: scheduling exists inside single owners and nothing was found across independent owners (F2-S84, F2-S14, F2-S63). **Drift detection and mandatory-hold decision support (2f)** splits: the monitoring half is `already_implemented` (Sartorius SIMCA-online, LPMS-S13), while "validated model-driven mandatory hold as the disposition mechanism" is `uncertain`, with no vendor found selling one under the FDA AI credibility framework or draft Annex 22 (F2-S57, F2-S48). **Cross-site process intelligence across independent owners (2g)** is `commercially_novel, pre-release` (Axio Lattice "is being developed"; L7 EXCHANGE "estimated 2027"; F2-S32, F2-S26), as against the within-one-owner version listed above. And **manufacturer-side reserved-capacity coordination across independent owners (2h)** is `uncertain, with documented structural barriers`, which the review carries as surviving unoccupied position 6.6 (F2-S63, F2-S64, F3-S19). 6.6 is OS-shaped, so it belongs to the answer here and not only to the virtual-network paragraph below: the one software position this review records as unoccupied is a coordination and allocation layer across owners, not a plant OS, and it is a contracting and antitrust question before it is a product.

Two constraints bound the category whatever the product quality: 21 CFR 211.22(a) puts approve-or-reject authority in the customer's own quality unit (LPMS-S20), and FDA has applied 21 CFR 211.22(c) to AI-generated GMP records in Warning Letter 320-26-58 (F2-S52, LPMS-S21), which is `architecture_taxonomy.md` incompatibility 15: an OS that writes records transfers inspection exposure to the buyer. All three OS candidates generated in Phase B were rejected before configuration (`novel_architectures.md` sections 4.1, 4.2): `os_only_replenishment_layer` (judge total 9.28) under P2 and P5, because its whole effect is the MD-3 artifact; `os_only_noncorrelating_layer` (8.09), whose own scoping run moved fill by 0.0001; `os_only_activation_layer` (6.57) under P6, because the product is an allocation right and the engine has none.

**Virtual network.** Every element is `already_implemented`: prequalifying capacity across existing CDMOs (BARDA FFMN 2013 and the 2021 CDMO network, EU FAB, CEPI VMFN, Civica supplier audits; F3-S11, F3-S18, F3-S1, F3-S21, F3-S28); reserved third-party capacity paid a standby fee, called the most thoroughly implemented sub-idea in the design space and with published prices (F3-S3, F3-S9, F7-S04, F7-S08, F7-S10, F7-S21, F10-S24); a non-manufacturer coordinating activation and allocation, where BARDA held the exclusive right of final determination, the Commission activates EU FAB and Civica allocates under member contracts (F3-S10, F3-S1, F3-S23); and the asset-light operator holding only label, application or contracts, implemented with a documented reversal, since Civica was virtual from 2018 to 2023 and then built Petersburg with contamination control among the stated reasons (F3-S23, F3-S25, F3-S29, F3-S52, F3-S31). Telo has no evidenced reason it beats Civica; falsification register row 15 records that plainly.

Three narrow positions survive prior art, and all three belong to the standby and rotation designs rather than to plain contracting: a maintained regulator-pre-agreed switching package (6.3, F9-S37, capped at CBE-30 rather than CBE-0), campaign rotation across several prequalified sites as a scheduling policy (6.4, F7-S02), and manufacturer-side capacity coordination across independent owners (6.6), which HDA frames as a Sherman Act and DOJ/FTC question before it is a product (F2-S63, F2-S64, F3-S19) and which ASPR is already part-funding on the registry side (LGOV-S17, LGOV-S51). Against them: CDMO partners refused BARDA capacity over the risk of being displaced when the government called (F7-S01); the one disclosed US CDMO capacity agreement puts the obligation on the buyer and none on the seller (LCDM-S14); and merchant US aseptic capacity is going captive (LCDM-S1, LCDM-S9, LCDM-S10).

---

## 6. What is weak, and what evidence would change the answer

### 6.1 The OS business question, which the model cannot reach

1. **Number of sites on one contract and annual contract value per site.** The engine prices an OS as a cost of 100k to 800k USD per site-year and has no revenue side, so it cannot say whether a vendor selling to many owners is a good business. Holder: manufacturing quality and IT budget owners at generic sterile-injectable firms and CDMOs. Proposed here for deliverable 23 as a new interview row beside HA-20 to HA-25, question: how many sites, at what annual contract value, displacing what. That row now exists as **HA-37**, rank 29 in `../audits/07_human_action_queue.md`.
2. **True deviation rate per batch and investigation duration at node scale.** Both are tier 5 with `source_locator` "study placeholder". At the declared low corner (0.005 per batch) the perfect-OS bound above shrinks by roughly a factor of four. **HA-22**, with **HA-21** for site and campaign context.
3. **Whether a buyer will pay when the disposition decision stays with their own quality unit and AI-generated records carry inspection exposure.** **HA-23** for the regulatory reading, **HA-31** for reviewer sign-off, **HA-22** for the acceptable AI role.
4. **Whether the named incumbents already serve the target segment.** The falsifier is written into the prior-art row: a sterile or 503B segment no listed vendor serves and where Korber's small-site product does not ship (F2-S01). Search work; no human action needed.

Weaknesses, each with what would change it.

5. **The perfect-OS bound removes rejection and yield variance too**, so it overstates an OS twice over and the three cents per unit is an upper bound on an upper bound. **Change it by** running an OS arm that zeroes only `deviation_rate_per_batch` and `investigation_duration_days`. In-model, no person needed.
6. **No post-R008 sensitivity evidence on the OS levers.** The only analysis that sweeps `deviation_rejection_rate` (0.005 / 0.02 / 0.08) and `investigation_duration` (7 / 21 / 60) is `results/sensitivity/one_way.json`, generated 20260902T045142Z at six runs per scenario over S0-S7 only. It predates 2026-09-03, so it is superseded, and at n = 6 its `p_meet` column carries no information. **Change it by** re-running the one-way sweep post-R008 over S0 to S19 with a manifest. In-model, no person needed; the true rates themselves are **HA-21** and **HA-22**.

### 6.2 The virtual-network answer

1. **Whether adding a third-party sterile fill site to an approved application is a CBE-30-class change or a prior-approval supplement with a preapproval inspection** (F3-S45 VI.A, VI.B.1, VI.B.2, VI.B.4). If the latter, S12's 365-day leg does not exist and the family loses its central advantage over building. **HA-23**, **HA-31**; falsification register rows 13 and 27 (row 13 is the S12 site-product pair under the F3-S45 criteria, row 27 the S17 three-fill-site addition; row 11 carries the same question for S11's labeling site).
2. **Whether any purchaser will fund readiness, and at what price on a low-price vial** (F3-S28, F7-S16). Section 4 states the thresholds a purchaser must clear at S0's break-even cost used as a stand-in price: 0.8021 of saleable capacity committed for sodium S16, 0.9609 for S17, above 1.0 for everything else and for both on norepinephrine. **HA-24**, **HA-33**, **HA-20**.
3. **Reservation fee, minimum campaign size and tenancy price at a named US line.** No public rate card exists (competitive landscape 1.2) and the only published reservation price has the per-batch figure redacted (F7-S04). **HA-13**, **HA-21**.
4. **Installed capacity and true national demand for the exact presentation**, which decides whether the capacity mode that breaks the owned nodes exists at all. **HA-11**, **HA-12**.
5. **Readiness decay.** Until the engine links `activation_failure_probability` to `exercise_batches_per_year` (NEW-3) and MD-23 is closed, no design here can show that exercising a line keeps it ready. S17's norepinephrine cell is the clearest symptom: 0 activations and 72.54 exercise batches over five years, so its perfect service comes from routine contracted output and not from standby at all. Engine work first, then **HA-21** and **HA-22** for the decay rate.

Weaknesses, each with what would change it.

6. **The comparison is not matched (MD-3).** The winning contracted designs got a safety-stock bound four times higher than S5 and S6 and a replenishment rule those comparators cannot select, so the measured gap is part architecture and part MD-3. **Change it by** giving the comparators the same bounds and the same review rule under a revision (in-model), and by obtaining what replenishment policy real regional stocking points run: **HA-20**, reviewed by **HA-33**.
7. **Opening inventory is free (NEW-1)**, which flatters exactly those designs. **Change it by** charging opening units at variable materials plus conversion on day 0 and re-running. In-model, no person needed.
8. **S16 and S17 carry the incumbent plant's capital on their ledgers (MD-14 residual)**, so their cost is not a Telo-only cost and no cost ranking here is clean. **Change it by** running a labelled Telo-only companion design with `capital_multiplier`, `fixed_cost_multiplier` and `validation_multiplier` at 0.0 on the incumbent line. In-model, no person needed.
9. **The commissioning metric excludes reserved sites and expansions**, so S16's 540-day qualification lead is invisible in the headline row. **Change it by** extending `_commissioning_window_loss` to reserved sites and to `expansion_available_day`. In-model, no person needed.
10. **Allocation rights and take-or-pay are both inert** (NEW-2, MD-24), which are the two instruments that make a virtual network a company rather than a purchasing arrangement. **Change it by** plumbing per-region minima and criticality into `RegionPolicy`, and by giving take-or-pay a service channel, each under its own revision. In-model; what a counterparty would actually sign is **HA-24** and **HA-33**.
11. **Two products are not a portfolio.** WB-26 records the dossiers as near-clones on several axes, and norepinephrine failed beachhead verification, so it functions here as a control rather than a second case. **Change it by** configuring a presentation that is not a near-clone, which needs the founder's longlist decision **HA-03** and the demand denominator **HA-11**.
