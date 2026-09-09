# Interview program (protocol `interview_program`)

No interview has been held. Every file here is infrastructure. A conversation counts only when the interviewee has directly relevant experience, consent and attribution are recorded, and the evidence is logged in `data/interview_evidence/<interview_id>.json` with `status: complete`. Nobody is called a partner, advisor, customer, reviewer, or validator without written authorization.

| File | Purpose |
|---|---|
| `target_matrix.md` | Roles, counts, what each role must be able to reject, outreach status (all `not contacted`) |
| `sequencing.md` | What goes out first, what waits, and what the founder settles before any outreach |
| `outreach_templates.md` | Concise outreach text per role |
| `guide_core.md` | 45-minute core guide; the questions asked of everyone are the study's own, not a protocol appendix (see `guide_core.md` section 4) |
| `field_kit.md` | The card the interviewer holds during the call. Interviewer only: never attached, never shown, never left behind |
| `modules/*.md` | Role-specific probes, interviewer copy |
| `modules/handouts/*.md` | The only role material an interviewee ever receives: question text, units and entity level, answer form. No model output |
| `evidence_log_schema.json` | JSON schema for `data/interview_evidence/*.json` |
| `elicitation_worksheet.md` | Structured range elicitation for parameters (low/base/high, confidence, rationale), and the one published timetable |
| `revision_workflow.md` | How an interview changes the model: assumption id, code change, revision log link |

Evidence tiers: an interview produces tier 4 (qualified expert elicitation) values; documents an interviewee provides may be tier 2.

**One rule governs everything sent or said.** No model result may be stated as a finding about the world, in any setting. Model behaviour under stated illustrative assumptions may be described to a named interviewee inside this process, and it may not appear on any public, promotional or fundraising surface, in any email, or in any document sent ahead of a conversation. `guide_core.md` section 7 holds the full claim-discipline text.
