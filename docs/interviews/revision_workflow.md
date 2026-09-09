# Post-interview revision workflow

1. Log the record in `data/interview_evidence/INT-YYYY-NNN.json` (schema in this directory) at `status: "pending_confirmation"`, within 24 hours.
2. Send the record, or the part of it that quotes them, back to the interviewee for correction. Promote to `status: "complete"` on their reply, or after the stated wait. Only `complete` counts toward DF18.
3. For each claim: decide accept / partial / reject with a one-line rationale.
4. Accepted: change the parameter record (value, tier 4, source_ids include the interview id, access_date), add a row to `protocol/revisions.csv` if decision-relevant, and note in `RESEARCH_LOG.md`.
5. Re-run `make check` and the affected analysis; record before/after behavior in the revision row.
6. Contradictions between interviewees stay visible. Record the substance in the `disagreement` field of both records, add a `contradicts` token naming the other record on each side (`elicitation_worksheet.md` rule D3), and widen the parameter's low and high to the union of both ranges. Never average, never pick, never quietly drop the outlier.
