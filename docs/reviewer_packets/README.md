# Independent review packets

**PRELIMINARY / ILLUSTRATIVE / NOT FOR EXTERNAL CLAIMS.** Every numeric input behind every result named in
these packets is evidence tier 5 (illustrative) except four release components. 87 of 91 parameters are
illustrative (`uv run python -m telo_feasibility.cli status`, DF09). Nothing here is a statement about
sterile-injectable manufacturing in the world, a recommendation to a purchaser, or legal or regulatory advice.
All sixteen gates in `config/regulatory_gates.yaml` are UNCERTAIN with no reviewer and no review date, so no
strategy carries a favourable decision class and `regulatory.evaluate_all` returns NO_CONCLUSION for every id.
UNCERTAIN is never PASS. 503B is a time-varying legal state and never a durable pathway. No interview, partner,
customer, pilot, purchaser, reviewer or regulatory opinion is asserted anywhere in this directory, because none
has occurred.

**Status on 2026-09-05: four packets written, none sent, zero reviews complete.** The protocol requires three
(`protocol/protocol.yaml` `independent_review.minimum_completed`; DF19).

Paths below are relative to `~/telo/feasibility/` unless they begin with `../`, which is relative to this
directory.

---

## 1. Sequencing gate: nothing is sent yet

These packets are not to be sent until both of the following are true.

**(a) The open defects that carry the ranking are fixed. This condition is now met.** Revisions R009, R010
and R011, all dated 2026-09-05, land every one of them in code. Statuses are in
`docs/design_space/bottleneck_decomposition.md` section 7, "Status after revisions R009 to R011"; each fix
carries a test named for its id in `tests/integration/test_ranking_defect_fixes.py`.

| id | what it did to the ranking | status |
|---|---|---|
| NEW-1 | opening inventory was seeded with no ledger charge and scaled with the design's own stock policy, so every inventory-led design was flattered | fixed, R009 |
| MD-3 | the regional review rule was hard-coded and the protocol never specifies it; it decided 8 of 16 Phase A cells | fixed, R010 |
| MD-12 | search spaces were not matched across architectures, so a comparison measured search freedom as well as architecture | fixed, R010, for the inventory space |
| MD-11 | the optimizer tie-break had no Monte Carlo standard error tolerance on a screen whose binomial standard error is 0.067 near q = 0.90 | fixed, R010 |
| NEW-2 | allocation rights were inert; all four `allocation_policy` values collapsed to proportional | fixed, R011, with the finding that identical regions make three of the four coincide by arithmetic |
| MD-23 | the exercise cadence was nearly unmeasurable on a frequently activated line, because a campaign batch substituted for an exercise batch one for one | fixed, R011 |
| MD-24 | take-or-pay entered cost only and had no service channel, so an optimizer drove it to its lower bound | fixed, R011 |
| MD-1 | the material order-up-to level and reorder point were `(target_days + lead) x daily demand`, so cutting a lead cut the buffer | fixed, R011, with a stated residual |

NEW-3 (no readiness-decay hazard) is not addressed by those revisions and stays open, as do MD-5, MD-8, MD-15,
MD-17, MD-18, MD-22 and MD-25. They belong in the packets as stated limits rather than as surprises.

**(b) The battery is re-run on the fixed engine and every number in the packets is replaced.** Optimize,
simulate, ablate, design-space, matched-space, figures, contract table. Section 5 gives the commands. **This
condition is not met, and it is the only thing still holding the packets.** Until that run exists, a reviewer
would be attacking a result the author already intends to withdraw, and that is a waste of the one resource
these packets spend.

A post-fix paired simulation exists (`results/simulation/sim_post_R009/`, manifest 2026-09-06T03:02:03Z, 20
strategies, both products, n = 100, at the illustrative baseline designs). The optimization, ablation,
design-space, matched-space, figures and contract table have not been re-run:
`results/optimization/opt_20260906T032432Z/` is an empty directory with that run still in flight. Check
`results/manifests/` for a completed post-R011 battery, and check that `make check` is green, before sending
anything.

---

## 2. What changed, and why the packets were rewritten

The study was built around one question: under what conditions does distributed regional capacity beat safety
stock, dual sourcing, reserved contract capacity, or added central capacity. Under the model's inputs that
question is answered, and the answer is that it does not beat them anywhere in any recorded range. Distributed
owned nodes (S5, S6) meet the frozen service target in no region of any recorded range of any swept input, on
either product, and giving them the same inventory freedom that makes the alternatives feasible does not rescue
them (`docs/design_space/feasibility_regions.md` section 6 family 1, and section 8).

The earlier packets opened with the old framing. They asked people to help settle a question the model had
already settled, and they did not ask for the inputs that decide anything. The rewrite does three things:

1. Each packet names one specific claim to attack, rather than a topic.
2. Each packet carries the register of known model defects with status, so a reviewer can skip what is already
   recorded. A reviewer who finds a defect the author already knew about has wasted their time.
3. Each packet asks for numbers and categories with ranges, because every input is illustrative and an opinion
   about architecture changes nothing here.

---

## 3. The reviewer plan

Four packets, mapped to `protocol/protocol.yaml` `independent_review` and to the ranked human-action queue
(`docs/audits/07_human_action_queue.md`).

| Packet | Reviewer id | Queue id | Rank | Can reject | Required |
|---|---|---|---|---|---|
| `packet_1_manufacturing_quality.md` | reviewer_1 | HA-30 | 25 | process and cost assumptions | yes |
| `packet_2_regulatory.md` | reviewer_2 | HA-31, with HA-23 supplying the professional reading | 11, 12 | pathway map and every gate status | yes |
| `packet_3_operations_research.md` | reviewer_3 | HA-32 | 26 | model structure, optimization, uncertainty methods | yes |
| `packet_4_hospital_gpo.md` | reviewer_4 | HA-33 | 24 | demand, inventory, contract assumptions | preferred, not required |

Three completed reviews close DF19. Packet 2 also carries the only route to DF08, because gate statuses need a
named qualified reviewer and a date, and zero of sixteen are reviewed today.

Order of sending, once the sequencing gate clears: packet 2 first, because a single reporting category (G07)
can remove an architecture and every decision class in the package depends on the gates; then packet 3, because
it audits the machine that produced the ranking; then packets 1 and 4 in parallel, because they are the two
that buy the highest-decision-value numbers.

---

## 4. Qualification bar

Qualification is recorded in the reviewer's own words and is checked against the packet before the review is
counted. The bar per packet:

- **Packet 1.** Direct responsibility for sterile injectable manufacturing or quality at a registered facility:
  aseptic fill-finish operations, process or cleaning validation, a quality unit with batch disposition
  authority, or fill-finish engineering with commissioning and qualification experience. Vendor sales without
  operating responsibility does not meet the bar for the cost ledger, and is recorded as such if the numbers
  are still useful.
- **Packet 2.** Generic-drug CMC or 503B regulatory practice with filings actually made: ANDA or NDA
  supplements, site additions, change-control categorisation, or outsourcing-facility registration and CGMP.
  A reading of the statute without filing experience is recorded as a reading, not as a professional opinion.
- **Packet 3.** Operations research, discrete-event or Monte Carlo simulation, stochastic inventory theory, or
  simulation-based optimization, with published or shipped work. Reviewers who work on drug supply chains
  specifically are preferred but not required, because the questions in packet 3 are method questions.
- **Packet 4.** Operating responsibility for demand, allocation, inventory or contracting at a hospital
  pharmacy, IDN, GPO, wholesaler or distributor. Contract-signing authority is preferred for the price
  questions and is recorded separately from the demand questions, because a reviewer may be qualified for one
  and not the other.

The counting rule is the protocol's: count only reviewers with directly relevant experience and logged
evidence. A reviewer who is qualified on part of a packet reviews that part, and the record says which part.

---

## 5. Reproduction, identical in every packet

```
cd ~/telo/feasibility
uv sync --all-extras
uv run python -m telo_feasibility.cli status          # definition-of-finished gates
uv run python -m telo_feasibility.cli protocol verify  # source-document hashes
make check                                             # ruff, mypy --strict, full test suite
```

The last recorded gate run is `results/manifests/test_report.json` (243 passed, 0 failed, 0 skipped,
2026-09-06T02:59:55Z). Re-read that file at send time and quote whatever it then holds. If `make check`
fails, the tree is mid-change and the packet is not ready to send.

Fast checks that finish in seconds:

```
uv run python scripts/run_deterministic.py --reconcile
uv run python scripts/run_simulation.py --runs 20 --strategies S0,S5,S11,S16 --run-id review_check
```

Full battery, with wall times from the recorded runs on the author's machine:

```
uv run python scripts/optimize_strategies.py                                          # 4113 s
uv run python scripts/run_simulation.py --runs 100                                    # all 20 strategies, both products
uv run python scripts/run_ablation.py --runs 60 --opt-run opt_20260903T220534Z        # 10014 s, 42 configs
uv run python scripts/run_design_space_analysis.py --opt-run opt_20260903T220534Z     # 6574 s
uv run python scripts/run_matched_space_check.py --strategies S1,S4,S5,S6             # 3706 s
make figures
```

The `--opt-run` default on `run_ablation.py` and `run_design_space_analysis.py` is `opt_20260902T043854Z`,
which is superseded. Pass `--opt-run` explicitly. Every run made before 2026-09-03 is superseded for
quantitative use.

---

## 6. What counts as a completed review

A review counts when `docs/reviewer_packets/reviews/<review_id>.json` exists with `status: complete` and the schema in
`docs/reviewer_packets/reviews/README.md`: `review_id`, `date`, `reviewer_qualification`, `packet`, `status`, `compensated`,
`relationship_disclosure`, `declined_sections`, and `issues`, where
each issue carries `issue`, `decision`, `rationale`, `affected_files`, `before` and `after`. The protocol
requires four things published per review: the issue, the decision, the exact model change, and the rationale
(`protocol.yaml` `independent_review.publish_per_review`). `affected_files` with `before` and `after` is how
the exact model change is recorded.

Every issue is answered with one of three decisions, and the rationale is written for the ones we reject as
carefully as for the ones we accept:

- **accepted**, with the code, config or document change that followed and the run that re-measured it;
- **partially accepted**, with the part taken and the part not;
- **rejected**, with the reason.

One row per issue is appended to `docs/reviewer_packets/reviews/revision_log.csv`
(`review_id, date, reviewer_qualification, packet, compensated, relationship_disclosure, declined_sections,
issue, decision, rationale, affected_files, before, after`).

Three fields are a convention of these packets rather than a protocol requirement, and are recorded in the
review file for honesty about provenance: `compensated`, whether the reviewer was compensated and how;
`relationship_disclosure`, any relationship between the reviewer and any organisation named in the package; and
`declined_sections`, which parts of the packet the reviewer declined to review. All three are in the record
schema in `reviews/README.md` and in the header of `reviews/revision_log.csv`, so they cannot be lost when the
first review arrives.

**On compensation.** No compensation is offered today, and each packet says so where it states the time cost.
Packet 2's primary deliverable, sixteen written gate statuses with rationale and qualification, is billable
consulting work, and asking for it unpaid is a real reason a qualified reviewer will decline. If compensation
is later offered, it is recorded in `compensated` and it changes nothing about how an issue is decided.

**A review is not complete when** it is a conversation with no written record, a set of comments with no
decisions taken, or approval of the framing without engagement with a specific claim. A logo, a name, a
flattering quote and a willingness to be listed are not validation
(`protocol.yaml` `independent_review.logo_or_quote_is_not_validation`).

**A review that rejects everything is a complete review.** Every packet asks the reviewer to reject rather than
to approve, and a packet that comes back with the headline claim destroyed and three numbers attached has done
more than one that comes back agreeing.

---

## 7. Rules that bind us

These bind the author, not the reviewer.

- Nothing a reviewer says may be presented as a partnership, endorsement, customer, pilot, or regulatory
  opinion. Reviewing is not advising, and an issue accepted is not an endorsement of what remains.
- Attribution is by role and organisation type only, unless the reviewer authorises more in writing. Never
  "partner", "validator" or "advisor" without written authorisation. **One carve-out, and packet 2's reviewer
  has to decide on it before starting.** A gate status counts for nothing without a named qualified reviewer
  and a date (section 3), so HA-31's deliverable is recorded with a name in `config/regulatory_gates.yaml`, and
  that file is published with the package. A reviewer who will not be named is logged as an unnamed
  professional reading that does not close DF08, which is an acceptable outcome and better than a name they did
  not intend to give.
- No number from this study may be presented externally as a finding about the world, because every input
  behind it is illustrative.
- Anything said about the release layer is governed by the claim-discipline table in `protocol.yaml` and
  logged in `CLAIMS_REGISTER.csv`. C009, C010, C015 and C025 are recorded as contradicted or unsupported and
  their wording may not be repeated in a packet, a covering note, or a conversation with a reviewer.
- The packets stay empty of results until real ones exist. `docs/reviewer_packets/reviews/` holds no fabricated entry.

---

## 8. Files in this directory

| File | Contents |
|---|---|
| `packet_1_manufacturing_quality.md` | sterile-injectable manufacturing and quality |
| `packet_2_regulatory.md` | generic-drug CMC or 503B regulatory |
| `packet_3_operations_research.md` | operations research and simulation |
| `packet_4_hospital_gpo.md` | hospital pharmacy, GPO, wholesaler |
| `reviews/README.md` | the review-record schema |
| `reviews/revision_log.csv` | one row per issue, with the decision and the model change |
