# Handoff: Telo feasibility package (state at 2026-09-05, end of session 2)

Read this first in a new session. Working rules are in `CLAUDE.md`; the assignment session 2 executed is
`docs/design_space/ASSIGNMENT.md`, and its answer is `docs/design_space/strategic_synthesis.md`. Read that
synthesis before anything else: it answers the twelve closing questions and states its own provisionality.

## 1. What session 2 did

All twenty-four assignment deliverables are complete. `docs/design_space/` holds them: the architecture taxonomy and
a 130-option morphological matrix, the Phase A bottleneck decomposition, prior-art and competitive-landscape reviews
over 798 verified sources, twelve new architectures as S8 to S19 with a 33-row falsification register, four family
analyses, the feasibility regions, four roadmaps, the prioritized human-action queue, the definition-of-finished
status, and the strategic synthesis.

The engine grew to match: an ablation harness with 22 named failure mechanisms, feasibility-condition bisection,
dominance and reversal maps, contract economics, a product-feature layer, and configuration-declared topologies for
S8+. 230 tests pass; `make check` is green.

## 2. The answer, and why it is provisional

The strongest intervention this evidence supports is a shape, not a strategy id: one approved presentation supplied
from US aseptic lines that are already registered and already inspected, bought as contracted campaigns rather than
built, paired with a deep positioned finished-goods tier, sold as units. S11 and S16 carry it and the package cannot
separate them.

It is provisional because the engine seeds opening inventory free (NEW-1), because a hard-coded regional review rule
the protocol never specifies decides eight of sixteen Phase A cells (MD-3), and because search spaces were not matched
across architectures (MD-12). When four comparators were re-optimized over one common inventory space, added central
capacity became feasible on both products and the cost gap narrowed to about a third
(`docs/design_space/feasibility_regions.md` section 8).

## 3. What is settled enough to act on

- Owned distributed microplants meet the target in no region of any recorded range of any swept input, on either
  product, and the fair-comparison correction does not rescue them.
- A manufacturing operating system is worth about three cents per delivered unit at best against a charge between
  0.32 and 2.56 dollars, and the prior-art review puts it on the does-not-survive list in all eight sub-forms.
- Chemical release-time reduction is worth 2 of 16 release days and moves fill by at most 0.008.
- Process-route conversion to terminal sterilization with parametric release is the only intervention found anywhere
  in fourteen families that removes the binding release constraint. The enabling data does not exist: sterilization
  route is not published per presentation (HA-34).

**Route screen, added 2026-09-06: `docs/route_screen/`.** That last bullet was tested against the public record and it
holds. Read `route_screen_results.md` sections 1 and 5. Across 65 manufacturer labels and 50 applications behind the six
longlist candidates, zero state a sterilization method; the FDA document that carries it publishes the field with the
value redacted; and for the two product configs the model runs on the screen determined nothing at any confidence.
One in-archetype determination exists, furosemide under ANDA 202747, and it stands at `weakly_inferred` with a
contradiction recorded, on a reserve candidate with no product config. Nothing in this screen moves a model parameter.

Its recommendation is **do not build a route dataset yet**, on three grounds that are worth carrying forward even if
the screen itself is never revisited: a validated rapid microbiological method reaches the same release pole as
terminal plus parametric release, with no supplement and no autoclave, and the study's own release memo calls it a
buy-and-validate; both route conversion and parametric release are prior approval supplements filed by an application
holder, and Telo holds no application; and every input to the proposed pipeline is a free public register, so the
dataset can be built and cannot be owned. Six falsification rows are in the register as `F11-ROUTE-01` to `-06`.

## 4. Model defects, the honest list

Twenty-four are recorded across `docs/design_space/bottleneck_decomposition.md` section 7 and the later documents.
Nine were fixed under revisions R004, R005 and R008; the rest are deferred with reasons. The four that most affect
any future number are NEW-1 (free opening inventory), MD-3 (the regional review rule), MD-12 (unmatched search
spaces) and MD-15 (one product per network). Fix those before quoting a cost or service comparison again.

The ablation harness turned out to be a defect detector as much as an attribution tool: a factor whose sign is wrong
is usually a bug, and that is how most of the twenty-four were found.

## 5. Protocol revisions awaiting sign-off

R000 to R008, of which R001, R004, R006, R007 and R008 are decision-relevant. None is signed. DF01 fails until they
are (HA-02).

## 6. What needs the founder, in order

The synthesis section 12 has the full list of sixteen. The first five: make the GitHub repository private today
(HA-06, the exposure is 29 people with addresses and up to 18 more in a second file), authorize history remediation
(HA-07), relocate the contact lists (HA-08), sign off the thresholds and revisions (HA-02), and authorize commits
(HA-05, now partly exercised: session 2 committed inside `feasibility/` only, on the founder's blanket instruction,
recorded as D018).

Also outstanding and specific: `regulatory/release-constraints.md` lines 96 to 98 attribute to FDA's 2004 aseptic
guidance a sentence that is not in it (C025, HA-10). The memo's conclusion is unaffected; the citation is not.

## 7. Standing rules (unchanged, keep them)

Protocol is data. Every parameter carries provenance and tier 5 is illustrative only. Gates are binary and UNCERTAIN
is never PASS. Reimbursement, price and cost stay separate. Nothing fabricated. New comparators get new ids; S0-S7
are frozen and pinned by `tests/regression/test_frozen_strategies.py`. Figures carry their metadata or `save_figure`
refuses them. Commit only inside `feasibility/`, never rewrite history, never push.

## 8. Tooling notes that cost time in session 2

- Orphaned multiprocessing workers from a finished run block the next pool silently. The parent shows elapsed hours
  with seconds of CPU. Kill `spawn_main` processes before starting another pooled job.
- Workflow scripts are plain JavaScript template literals: an inline backtick inside a prompt string breaks the
  parser. Write prompts without code spans.
- Session and model rate limits interrupted long workflows three times. Every workflow resumed from cache without
  losing completed agents.

## 9. First hour in a new session

1. `cd ~/telo/feasibility && make check && make status`.
2. Read `docs/design_space/strategic_synthesis.md`, then `feasibility_regions.md` section 8, then
   `bottleneck_decomposition.md` section 7.
3. Decide with the founder whether to fix NEW-1, MD-3, MD-12 and MD-15 and re-run the battery, or to stop modelling
   and buy the three inputs the synthesis names as decision-critical.
