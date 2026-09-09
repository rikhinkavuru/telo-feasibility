# Where the interview target list and the outreach drafts live

Written 2026-09-07.

## The short version

The ranked interview target list, the six per-category source lists behind it, and the wave-one outreach drafts are
**not in this repository and must never be added to it**. They live outside the working tree at:

```
~/telo-private/outreach_feasibility/
```

That directory holds one merged ranked list, one drafts file, six per-category source lists, and nothing else.

## Why they live outside

They contain personal names and professional email addresses. This project has already exposed a contact list in a
public repository once: `docs/design_space/privacy_remediation_plan.md` records two files under `outreach/` carrying
addresses for roughly thirty and up to eighteen people respectively, present in seventeen of nineteen commit
snapshots, with clones and views recorded against the public repository while the exposure was live.

Three queue items close that incident, and the third one is the reason this note exists:

- **HA-06** (queue rank 1): make the public repository private.
- **HA-07** (rank 2): decide whether to rewrite history, force-push and request a support purge, since making the
  repository private does not remove the files from the commits that already contain them.
- **HA-08** (rank 3): **relocate the contact lists out of the repository and adopt the `.gitignore` entries, the
  secret-scanning configuration and the pre-commit hook that stop new ones arriving.** That is prevention, not
  cleanup, and it is aimed squarely at the outreach these interviews are about to generate.

`docs/audits/07_human_action_queue.md` states the reason those three sit above every analytical item in the queue:
the exposure is live, the first action costs one command, and no analysis in this package is worth more than that.
The same file records HA-08's fallback if it is skipped, which is to keep contact data out of the repository by
convention alone. That is the control that already failed.

The new lists are larger than the exposed ones. Repeating the failure with a bigger file, immediately after writing
a remediation plan for the smaller one, is the specific outcome this note exists to prevent.

## The rule

**No contact detail may be committed to this repository at any time.** In full:

1. No personal names of outreach targets, and no email addresses, in any file under `feasibility/`. This includes
   commit messages, test fixtures, notebook output, example configuration, and anything pasted into a docstring.
2. No file that is a contact list, however partial, however anonymised it looks. An anonymised list plus one
   reference elsewhere reconstructs the original.
3. Interview evidence records under `data/interview_evidence/` carry **role and organisation type only**, which is
   what the protocol's attribution rule already requires and what `evidence_log_schema.json` already permits. Names
   go in there only where the person has authorised their name in writing, and the authorisation is recorded.
4. Contact status stays in `target_matrix.md` as counts and status values per role. Counts are not contact details.
   Individual rows naming individual people are not permitted, and the matrix does not have any.
5. `outreach_templates.md` section K already forbids attaching the contact lists to an outgoing message. That rule
   and this one are the same rule seen from two sides.

## What is in the repository, and is meant to be

Everything about the *instrument* rather than the *people*: the role definitions and counts in `target_matrix.md`,
the modules and handouts under `modules/`, the elicitation worksheet, the field kit, the sequencing plan, the
outreach templates, the evidence-log schema, and the reviewer packets. All of that is method, it carries no personal
data, and it belongs here.

## If you find contact data in this repository

Treat it as a live incident rather than a tidy-up. Stop, do not commit anything else, and follow
`docs/design_space/privacy_remediation_plan.md`, which covers the private-repository decision, the history rewrite
and its authorisation requirement, and the support-purge request. Adding a commit that deletes the file does not
remove it from history, which is the whole reason HA-07 exists as a separate decision from HA-06.
